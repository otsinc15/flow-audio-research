#!/usr/bin/env python3
"""Measure clips on exactly the axes used in research/ear-test/spec-from-references.md.

The tempo / band / onset / centroid block is a port of the script that produced
that file (same librosa calls, same n_fft, same band edges) so the numbers are
comparable row for row. Loudness comes from ffmpeg's EBU R128 filter when an
ffmpeg binary is available, and from a BS.1770 implementation on top of
pyloudnorm otherwise; the two agree to about 0.1 LU on these clips.

    python measure.py clip1.wav clip2.wav > measurements.json
"""

import json
import re
import shutil
import subprocess
import sys

import numpy as np
import librosa


# ------------------------------------------------------------------ loudness

def _ffmpeg_bin():
    b = shutil.which("ffmpeg")
    if b:
        return b
    try:
        import contextlib
        from static_ffmpeg import run
        # static-ffmpeg prints its download banner to stdout; this file's stdout
        # is the JSON result, so send that chatter to stderr.
        with contextlib.redirect_stdout(sys.stderr):
            return run.get_or_fetch_platform_executables_else_raise()[0]
    except Exception:
        return None


def loudness_ffmpeg(path):
    b = _ffmpeg_bin()
    if not b:
        return None
    p = subprocess.run([b, "-hide_banner", "-nostats", "-i", path,
                        "-filter_complex", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    tail = p.stderr[-3000:]

    def grab(label):
        m = re.findall(rf"{label}:\s*(-?\d+\.?\d*)", tail)
        return float(m[-1]) if m else None

    return {"integrated_lufs": grab("I"), "lra_lu": grab("LRA"),
            "true_peak_dbfs": grab("Peak"), "source": "ffmpeg-ebur128"}


def loudness_python(y, sr):
    """BS.1770 integrated loudness (pyloudnorm) + EBU LRA + 4x-oversampled peak."""
    import pyloudnorm as pyln
    from scipy.signal import resample_poly
    meter = pyln.Meter(sr)
    integrated = float(meter.integrated_loudness(y))
    # short-term (3 s window, 1 s hop) for LRA
    w, h = int(3 * sr), int(sr)
    st = []
    for s in range(0, max(1, len(y) - w + 1), h):
        seg = y[s:s + w]
        if len(seg) < w:
            break
        try:
            st.append(meter.integrated_loudness(seg))
        except Exception:
            pass
    st = np.array([v for v in st if np.isfinite(v) and v > -70.0])
    if len(st) >= 3:
        gate = st[st > (10 * np.log10(np.mean(10 ** (st / 10))) - 20.0)] if len(st) else st
        gate = gate if len(gate) >= 3 else st
        lra = float(np.percentile(gate, 95) - np.percentile(gate, 10))
    else:
        lra = None
    up = resample_poly(y.astype(np.float64), 4, 1)
    tp = float(20 * np.log10(np.max(np.abs(up)) + 1e-12))
    return {"integrated_lufs": round(integrated, 2),
            "lra_lu": round(lra, 2) if lra is not None else None,
            "true_peak_dbfs": round(tp, 2), "source": "pyloudnorm+bs1770"}


# -------------------------------------------------------- spectral / rhythmic

def analyze(path):
    y, sr = librosa.load(path, sr=44100, mono=True)
    dur = len(y) / sr
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    tempo = float(np.atleast_1d(tempo)[0])
    tg = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr)
    ac = np.mean(tg, axis=1)
    ac_norm = (ac - ac.min()) / (ac.max() - ac.min() + 1e-12)
    peak_ratio = float(ac_norm.max() / (np.median(ac_norm) + 1e-12))
    tempi = librosa.tempo_frequencies(len(ac), sr=sr)
    valid = np.isfinite(tempi) & (tempi > 40) & (tempi < 220)
    idx = np.argsort(ac[valid])[::-1]
    tv, av = tempi[valid], ac[valid]
    cands, seen = [], []
    for i in idx:
        t = float(tv[i])
        if any(abs(t - s2) < 4 for s2 in seen):
            continue
        seen.append(t)
        cands.append([round(t, 1), round(float(av[i] / av.max()), 3)])
        if len(cands) == 3:
            break
    bt = librosa.frames_to_time(beats, sr=sr)
    ibi_cv = float(np.std(np.diff(bt)) / np.mean(np.diff(bt))) if len(bt) > 3 else None

    S = np.abs(librosa.stft(y, n_fft=8192, hop_length=2048)) ** 2
    freqs = librosa.fft_frequencies(sr=sr, n_fft=8192)
    edges = [0, 60, 150, 500, 2000, 8000, sr / 2]
    labels = ["<60Hz", "60-150Hz", "150-500Hz", "500-2kHz", "2-8kHz", ">8kHz"]
    total = S.sum()
    bands = {}
    for i, lab in enumerate(labels):
        m = (freqs >= edges[i]) & (freqs < edges[i + 1])
        bands[lab] = float(100.0 * S[m].sum() / total)

    on = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units='time')
    onsets_per_min = float(len(on) / (dur / 60.0))

    cent = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=8192, hop_length=2048)[0]
    cent_mean, cent_std = float(np.mean(cent)), float(np.std(cent))
    w = max(1, int(round(sr / 2048)))
    cent_s = np.convolve(cent, np.ones(w) / w, mode='valid')
    slow_cv = float(np.std(cent_s) / (np.mean(cent_s) + 1e-12))

    rms = librosa.feature.rms(y=y, hop_length=2048)[0]
    rms_db = 20 * np.log10(rms + 1e-9)
    head = float(20 * np.log10(np.sqrt(np.mean(y[:3 * sr] ** 2)) + 1e-9))
    tail = float(20 * np.log10(np.sqrt(np.mean(y[-3 * sr:] ** 2)) + 1e-9))
    # butt-splice check: the sample-to-sample step across the loop point,
    # relative to the largest step that already occurs inside the clip. <= 0 dB
    # means the splice is no more of a discontinuity than the music itself.
    step = abs(float(y[0]) - float(y[-1]))
    typical = float(np.max(np.abs(np.diff(y)))) + 1e-9
    seam = float(20 * np.log10(step / typical + 1e-12))

    loud = loudness_ffmpeg(path) or loudness_python(y, sr)

    return {
        "file": path.split("/")[-1],
        "duration_s": round(dur, 1),
        "tempo_bpm": round(tempo, 1),
        "tempo_peak_ratio": round(peak_ratio, 2),
        "tempo_candidates_bpm_strength": cands,
        "beat_interval_cv": round(ibi_cv, 4) if ibi_cv is not None else None,
        **{k: (round(v, 2) if v is not None else None) for k, v in loud.items()
           if k != "source"},
        "loudness_source": loud["source"],
        "bands_pct": {k2: round(v, 2) for k2, v in bands.items()},
        "sum_below_150_pct": round(bands["<60Hz"] + bands["60-150Hz"], 2),
        "onsets_per_min": round(onsets_per_min, 1),
        "centroid_mean_hz": round(cent_mean, 0),
        "centroid_cv": round(cent_std / cent_mean, 3),
        "centroid_slow_cv_1s": round(slow_cv, 3),
        "rms_db_p10_p90_spread": round(float(np.percentile(rms_db, 90)
                                             - np.percentile(rms_db, 10)), 1),
        "head3s_db": round(head, 1),
        "tail3s_db": round(tail, 1),
        "loop_seam_vs_max_step_db": round(seam, 2),
    }


if __name__ == "__main__":
    print(json.dumps([analyze(p) for p in sys.argv[1:]], indent=1))
