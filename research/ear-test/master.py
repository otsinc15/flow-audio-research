#!/usr/bin/env python3
"""
Mastering-chain probe: does mastering alone close the low-body gap measured in
spec-from-references.md (el-a-1 / el-b-2 sit at 87-97% of energy below 150 Hz,
150-500 Hz body starved at 3-12%, vs ref01's ~46.5%)?

Chain: HPF 28 Hz -> low-shelf cut ~70 Hz + bell boost ~220 Hz -> 2-band split at
150 Hz with tanh saturation on the low band -> bus compression (30ms attack,
200ms release, 2:1, target 2-4 dB GR) -> soft clip -> true-peak limiter (-1 dBTP)
-> loudness normalize to -14 LUFS integrated.

Also produces loudness-matched copies of the untouched originals at -14 LUFS so
the mastered vs. original comparison is level-fair.

Usage:
    uvx --with numpy --with scipy --with soundfile --with pyloudnorm python3 master.py

Run with no args: processes el-a-1.mp3 and el-b-2.mp3 from the flow-audio-candidates
folder, writes *-mastered.wav and *-orig14.wav next to them, and prints a 4-row
measurement table (integrated LUFS, true peak, band energy shares).
"""

import subprocess
import sys
import tempfile
import os
from pathlib import Path

import numpy as np
import scipy.signal as sig
import soundfile as sf
import pyloudnorm as pyln

SR = 44100
CANDIDATES_DIR = Path(
    "~/Documents/AI Agent Outputs/Artifacts/flow-audio-candidates"
).expanduser()
FFMPEG = "/opt/homebrew/bin/ffmpeg"

BANDS = [
    ("<60 Hz", 0, 60),
    ("60-150 Hz", 60, 150),
    ("150-500 Hz", 150, 500),
    ("500-2k Hz", 500, 2000),
    ("2k-8k Hz", 2000, 8000),
    (">8k Hz", 8000, None),
]


# --------------------------------------------------------------------------
# I/O
# --------------------------------------------------------------------------

def decode_to_wav(src: Path) -> np.ndarray:
    """Decode any ffmpeg-readable file to float32 stereo @ SR via a temp wav."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        subprocess.run(
            [
                FFMPEG, "-y", "-i", str(src),
                "-ar", str(SR), "-ac", "2",
                "-c:a", "pcm_f32le", tmp_path,
            ],
            check=True, capture_output=True,
        )
        audio, sr = sf.read(tmp_path, dtype="float32", always_2d=True)
        assert sr == SR
    finally:
        os.unlink(tmp_path)
    return audio  # shape (n, 2)


def write_wav(path: Path, audio: np.ndarray):
    sf.write(str(path), audio, SR, subtype="PCM_24")


# --------------------------------------------------------------------------
# Filters
# --------------------------------------------------------------------------

def highpass(audio: np.ndarray, freq: float, order: int = 2) -> np.ndarray:
    sos = sig.butter(order, freq, btype="highpass", fs=SR, output="sos")
    return sig.sosfiltfilt(sos, audio, axis=0)


def peaking_eq(audio: np.ndarray, freq: float, gain_db: float, q: float) -> np.ndarray:
    """RBJ audio-EQ-cookbook peaking filter, applied per channel."""
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * freq / SR
    alpha = np.sin(w0) / (2 * q)
    cos_w0 = np.cos(w0)

    b0 = 1 + alpha * A
    b1 = -2 * cos_w0
    b2 = 1 - alpha * A
    a0 = 1 + alpha / A
    a1 = -2 * cos_w0
    a2 = 1 - alpha / A

    b = np.array([b0, b1, b2]) / a0
    a = np.array([1.0, a1 / a0, a2 / a0])
    return sig.filtfilt(b, a, audio, axis=0)


def low_shelf(audio: np.ndarray, freq: float, gain_db: float, slope: float = 0.9) -> np.ndarray:
    """RBJ audio-EQ-cookbook low-shelf filter."""
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * freq / SR
    cos_w0 = np.cos(w0)
    sin_w0 = np.sin(w0)
    alpha = sin_w0 / 2 * np.sqrt((A + 1 / A) * (1 / slope - 1) + 2)
    two_sqrtA_alpha = 2 * np.sqrt(A) * alpha

    b0 = A * ((A + 1) - (A - 1) * cos_w0 + two_sqrtA_alpha)
    b1 = 2 * A * ((A - 1) - (A + 1) * cos_w0)
    b2 = A * ((A + 1) - (A - 1) * cos_w0 - two_sqrtA_alpha)
    a0 = (A + 1) + (A - 1) * cos_w0 + two_sqrtA_alpha
    a1 = -2 * ((A - 1) + (A + 1) * cos_w0)
    a2 = (A + 1) + (A - 1) * cos_w0 - two_sqrtA_alpha

    b = np.array([b0, b1, b2]) / a0
    a = np.array([1.0, a1 / a0, a2 / a0])
    return sig.filtfilt(b, a, audio, axis=0)


def linkwitz_riley_split(audio: np.ndarray, freq: float, order: int = 4):
    """4th-order Linkwitz-Riley split: two cascaded Butterworths, phase-matched
    via filtfilt on both bands so low+high sums back to (approximately) flat."""
    sos_lo = sig.butter(order // 2, freq, btype="lowpass", fs=SR, output="sos")
    sos_hi = sig.butter(order // 2, freq, btype="highpass", fs=SR, output="sos")
    low = sig.sosfiltfilt(sos_lo, audio, axis=0)
    low = sig.sosfiltfilt(sos_lo, low, axis=0)  # cascade -> 4th order
    high = sig.sosfiltfilt(sos_hi, audio, axis=0)
    high = sig.sosfiltfilt(sos_hi, high, axis=0)
    return low, high


def tanh_saturate(audio: np.ndarray, drive: float) -> np.ndarray:
    """Tape-style tanh saturation: drive up, saturate, compensate makeup gain."""
    driven = audio * drive
    saturated = np.tanh(driven)
    makeup = np.tanh(drive) or 1.0
    return saturated / makeup


# --------------------------------------------------------------------------
# Dynamics
# --------------------------------------------------------------------------

def bus_compressor(
    audio: np.ndarray,
    threshold_db: float,
    ratio: float,
    attack_ms: float,
    release_ms: float,
    makeup_db: float,
) -> np.ndarray:
    """Feed-forward RMS-detector compressor, stereo-linked (mono sidechain)."""
    attack_coef = np.exp(-1.0 / (SR * attack_ms / 1000.0))
    release_coef = np.exp(-1.0 / (SR * release_ms / 1000.0))

    mono = audio.mean(axis=1)
    eps = 1e-9
    level_db = 20 * np.log10(np.abs(mono) + eps)

    env_db = np.zeros_like(level_db)
    prev = -60.0
    for i in range(len(level_db)):
        target = level_db[i]
        coef = attack_coef if target > prev else release_coef
        prev = coef * prev + (1 - coef) * target
        env_db[i] = prev

    over = env_db - threshold_db
    gain_reduction_db = np.where(over > 0, over * (1 - 1 / ratio), 0.0)
    gain_lin = 10 ** ((-gain_reduction_db + makeup_db) / 20)

    return audio * gain_lin[:, None], gain_reduction_db.max()


def soft_clip(audio: np.ndarray, threshold: float = 0.9) -> np.ndarray:
    """Gentle tanh soft-clip above `threshold` (linear amplitude)."""
    def clip_sample(x):
        sign = np.sign(x)
        mag = np.abs(x)
        over = mag > threshold
        clipped = np.where(
            over,
            threshold + (1 - threshold) * np.tanh((mag - threshold) / (1 - threshold)),
            mag,
        )
        return sign * clipped
    return clip_sample(audio)


def true_peak_limit(audio: np.ndarray, ceiling_dbtp: float = -1.0, oversample: int = 4) -> np.ndarray:
    """Brick-wall limiter referenced to an oversampled (true) peak estimate."""
    ceiling_lin = 10 ** (ceiling_dbtp / 20)
    up = sig.resample_poly(audio, oversample, 1, axis=0)
    true_peak = np.max(np.abs(up))
    if true_peak > ceiling_lin:
        audio = audio * (ceiling_lin / true_peak)
    return audio


# --------------------------------------------------------------------------
# Loudness
# --------------------------------------------------------------------------

def measure_lufs(audio: np.ndarray) -> float:
    meter = pyln.Meter(SR)
    return meter.integrated_loudness(audio)


def normalize_lufs(audio: np.ndarray, target_lufs: float = -14.0) -> np.ndarray:
    current = measure_lufs(audio)
    if not np.isfinite(current):
        return audio
    return pyln.normalize.loudness(audio, current, target_lufs)


def true_peak_dbtp(audio: np.ndarray, oversample: int = 4) -> float:
    up = sig.resample_poly(audio, oversample, 1, axis=0)
    peak = np.max(np.abs(up))
    return 20 * np.log10(peak + 1e-12)


# --------------------------------------------------------------------------
# Chain
# --------------------------------------------------------------------------

def master(audio: np.ndarray) -> np.ndarray:
    x = audio.copy()

    # 1. High-pass ~28 Hz to remove sub-sonic junk.
    x = highpass(x, 28.0, order=2)

    # 2. Low-shelf cut ~70 Hz (sub is dominant per the measured spec) + bell
    #    boost ~220 Hz to rebuild the 150-500 Hz body.
    x = low_shelf(x, 70.0, gain_db=-3.0, slope=0.9)
    x = peaking_eq(x, 220.0, gain_db=3.0, q=0.7)

    # 3. 2-band split at 150 Hz, tanh-saturate the low band for harmonic
    #    content (so the sub reads as body, not just felt weight), mix back.
    low, high = linkwitz_riley_split(x, 150.0, order=4)
    low_sat = tanh_saturate(low, drive=2.5)
    x = low_sat + high

    # 4. Bus compression: slow attack, medium release, gentle ratio.
    x, max_gr = bus_compressor(
        x, threshold_db=-18.0, ratio=2.0,
        attack_ms=30.0, release_ms=200.0, makeup_db=2.0,
    )

    # 5. Soft clip then brick-wall true-peak limit.
    x = soft_clip(x, threshold=0.9)
    x = true_peak_limit(x, ceiling_dbtp=-1.0)

    # 6. Normalize to -14 LUFS integrated, then re-check/re-limit true peak.
    x = normalize_lufs(x, target_lufs=-14.0)
    x = true_peak_limit(x, ceiling_dbtp=-1.0)

    return x, max_gr


# --------------------------------------------------------------------------
# Measurement (power-domain STFT band shares, matches spec-from-references.md
# methodology: n_fft=8192, hop=2048, share of total energy)
# --------------------------------------------------------------------------

def band_energy_shares(audio: np.ndarray, n_fft: int = 8192, hop: int = 2048):
    mono = audio.mean(axis=1)
    freqs = np.fft.rfftfreq(n_fft, d=1.0 / SR)
    window = np.hanning(n_fft)

    total_power = np.zeros(len(freqs))
    n_frames = 0
    for start in range(0, len(mono) - n_fft, hop):
        frame = mono[start:start + n_fft] * window
        spec = np.fft.rfft(frame)
        total_power += np.abs(spec) ** 2
        n_frames += 1

    if n_frames == 0:
        frame = np.pad(mono, (0, n_fft - len(mono))) * window
        spec = np.fft.rfft(frame)
        total_power = np.abs(spec) ** 2

    grand_total = total_power.sum()
    shares = {}
    for name, lo, hi in BANDS:
        hi_val = hi if hi is not None else freqs[-1] + 1
        mask = (freqs >= lo) & (freqs < hi_val)
        shares[name] = 100.0 * total_power[mask].sum() / grand_total
    return shares


def measure_file(path: Path) -> dict:
    audio, sr = sf.read(str(path), dtype="float32", always_2d=True)
    assert sr == SR, f"{path} is {sr} Hz, expected {SR}"
    lufs = measure_lufs(audio)
    tp = true_peak_dbtp(audio)
    shares = band_energy_shares(audio)
    return {"lufs": lufs, "true_peak": tp, **shares}


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def process_one(name: str):
    src = CANDIDATES_DIR / f"{name}.mp3"
    print(f"-- {name} --", file=sys.stderr)

    audio = decode_to_wav(src)

    mastered, max_gr = master(audio)
    mastered_path = CANDIDATES_DIR / f"{name}-mastered.wav"
    write_wav(mastered_path, mastered)
    print(f"   wrote {mastered_path.name} (peak GR ~{max_gr:.1f} dB)", file=sys.stderr)

    orig14 = normalize_lufs(audio.copy(), target_lufs=-14.0)
    orig14 = true_peak_limit(orig14, ceiling_dbtp=-1.0)
    orig14_path = CANDIDATES_DIR / f"{name}-orig14.wav"
    write_wav(orig14_path, orig14)
    print(f"   wrote {orig14_path.name}", file=sys.stderr)

    return mastered_path, orig14_path


def main():
    names = ["el-a-1", "el-b-2"]
    rows = []

    for name in names:
        mastered_path, orig14_path = process_one(name)
        rows.append((f"{name} (orig @ -14 LUFS)", measure_file(orig14_path)))
        rows.append((f"{name} (mastered)", measure_file(mastered_path)))

    band_names = [b[0] for b in BANDS]
    header = ["file", "LUFS", "TP dBTP"] + band_names
    col_w = [28, 8, 8] + [11] * len(band_names)

    def fmt_row(cells):
        return " | ".join(str(c).ljust(w) for c, w in zip(cells, col_w))

    print()
    print(fmt_row(header))
    print("-" * (sum(col_w) + 3 * (len(col_w) - 1)))
    for label, m in rows:
        cells = [
            label,
            f"{m['lufs']:.1f}",
            f"{m['true_peak']:.1f}",
        ] + [f"{m[b]:.1f}%" for b in band_names]
        print(fmt_row(cells))
    print()
    print("Reference (ref01, human techno master): 150-500 Hz = 46.5%, <60 Hz = 27.6%, 60-150 Hz = 21.2%")


if __name__ == "__main__":
    main()
