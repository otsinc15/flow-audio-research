#!/usr/bin/env python3
"""Objective measurement pass for ear-test audio. No listening judgement is made.

Reproduces the metric set in spec-from-references.md so generated candidates can be
compared against the two references on identical footing.

  ffmpeg (EBU R128)  -> integrated LUFS, LRA, true peak
  librosa 0.11       -> tempo, onset density, spectral balance, centroid drift

Audio itself is never committed. Usage:
    python measure-clips.py FILE [FILE ...]            # table to stdout
    python measure-clips.py --json out.json FILE ...
"""
import argparse, json, re, subprocess, sys
import numpy as np
import librosa

FFMPEG = "/opt/homebrew/bin/ffmpeg"
SR = 44100                 # analysis rate; 2048-sample frames = 46 ms, as in the spec
N_FFT = 8192
HOP = 2048
BANDS = [(0, 60), (60, 150), (150, 500), (500, 2000), (2000, 8000), (8000, None)]
BAND_NAMES = ["<60 Hz", "60-150 Hz", "150-500 Hz", "500 Hz-2 kHz", "2-8 kHz", ">8 kHz"]


def ebur128(path):
    """Integrated loudness, loudness range and true peak via ffmpeg."""
    p = subprocess.run(
        [FFMPEG, "-nostdin", "-i", path, "-filter_complex", "ebur128=peak=true",
         "-f", "null", "-"],
        capture_output=True, text=True)
    tail = p.stderr[-4000:]
    def grab(label):
        m = re.search(label + r":\s*(-?\d+\.?\d*)", tail)
        return float(m.group(1)) if m else None
    return dict(integrated_lufs=grab("I"), lra_lu=grab("LRA"),
                true_peak_dbfs=grab("Peak"))


def analyse(path):
    y, sr = librosa.load(path, sr=SR, mono=True)
    dur = len(y) / sr
    out = dict(file=path.split("/")[-1], duration_s=round(dur, 1))
    out.update(ebur128(path))

    # --- tempo -------------------------------------------------------------
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    out["bpm"] = round(float(np.atleast_1d(tempo)[0]), 1)
    tg = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr)
    agg = tg.mean(axis=1)
    freqs = librosa.tempo_frequencies(tg.shape[0], sr=sr)
    valid = np.isfinite(freqs) & (freqs > 30) & (freqs < 300)
    a, f = agg[valid], freqs[valid]
    order = np.argsort(a)[::-1]
    picked = []
    for i in order:
        if all(abs(f[i] - q) > 5 for q in picked):
            picked.append(float(f[i]))
        if len(picked) == 3:
            break
    peak = a.max()
    out["tempo_candidates"] = [round(x, 1) for x in picked]
    out["tempo_peak_over_median"] = round(float(peak / np.median(a)), 1)
    bt = librosa.frames_to_time(beats, sr=sr)
    ibi = np.diff(bt)
    out["beat_interval_cv"] = round(float(ibi.std() / ibi.mean()), 3) if len(ibi) > 2 else None

    # --- spectral balance (power-domain shares) ----------------------------
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP)) ** 2
    fb = librosa.fft_frequencies(sr=sr, n_fft=N_FFT)
    total = S.sum()
    shares = {}
    for (lo, hi), name in zip(BANDS, BAND_NAMES):
        m = (fb >= lo) & ((fb < hi) if hi else np.ones_like(fb, bool))
        shares[name] = round(float(S[m].sum() / total * 100), 2)
    out["bands_pct"] = shares
    out["sub150_pct"] = round(shares["<60 Hz"] + shares["60-150 Hz"], 2)

    # --- event density ------------------------------------------------------
    on = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units="time")
    out["onsets_per_min"] = round(len(on) / (dur / 60))
    # per-10 s onset rate, to test "does the arrangement stay constant"
    edges = np.arange(0, dur + 1e-9, 10.0)
    per10 = [int(((on >= edges[i]) & (on < edges[i + 1])).sum()) for i in range(len(edges) - 1)]
    out["onsets_per_10s"] = per10
    out["onsets_per_10s_cv"] = round(float(np.std(per10) / np.mean(per10)), 3) if np.mean(per10) else None

    # --- timbre drift -------------------------------------------------------
    cen = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=N_FFT, hop_length=HOP)[0]
    out["centroid_mean_hz"] = round(float(cen.mean()))
    out["centroid_cv"] = round(float(cen.std() / cen.mean()), 2)
    w = max(1, int(round(sr / HOP)))                       # ~1 s smoothing
    slow = np.convolve(cen, np.ones(w) / w, mode="valid")
    out["centroid_slow_cv_1s"] = round(float(slow.std() / slow.mean()), 2)

    # --- level shape --------------------------------------------------------
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    db = 20 * np.log10(np.maximum(rms, 1e-10))
    out["rms_spread_p10_p90_db"] = round(float(np.percentile(db, 90) - np.percentile(db, 10)), 1)
    seg = int(3 * sr)
    head = 20 * np.log10(max(float(np.sqrt((y[:seg] ** 2).mean())), 1e-10))
    tail = 20 * np.log10(max(float(np.sqrt((y[-seg:] ** 2).mean())), 1e-10))
    out["head3s_db"] = round(head, 1)
    out["tail3s_db"] = round(tail, 1)
    out["head_to_tail_db"] = round(tail - head, 1)
    # per-10 s RMS, to test "no build-ups, no drops" as a level statement
    n10 = int(10 * sr)
    r10 = [round(20 * np.log10(max(float(np.sqrt((y[i:i + n10] ** 2).mean())), 1e-10)), 1)
           for i in range(0, len(y) - n10 + 1, n10)]
    out["rms_per_10s_db"] = r10
    out["rms_per_10s_range_db"] = round(max(r10) - min(r10), 1)
    # silence: fraction of 46 ms frames more than 40 dB below the clip median
    med = float(np.median(db))
    out["frames_below_median_minus40db_pct"] = round(float((db < med - 40).mean() * 100), 2)
    out["sample_peak_dbfs"] = round(20 * np.log10(max(float(np.abs(y).max()), 1e-10)), 2)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json")
    a = ap.parse_args()
    rows = []
    for f in a.files:
        r = analyse(f)
        rows.append(r)
        print(json.dumps(r), flush=True)
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(rows, fh, indent=2)


if __name__ == "__main__":
    main()
