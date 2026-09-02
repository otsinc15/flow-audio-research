#!/usr/bin/env python3
"""Standalone mastering chain: glue compressor -> soft clip -> lookahead limiter.

Written as a plain function over a numpy array so it can be applied to clips
from any arm of the ear test, not just this renderer:

    from master import master_chain
    out, info = master_chain(audio, sr, target_lufs=-14.0, ceiling_dbtp=-1.0)

or from the shell, on any WAV:

    python master.py in.wav out.wav --lufs -14 --ceiling -1

Design notes. The glue compressor is a feed-forward bus compressor with an RMS
detector and a smoothed gain signal - on material whose only transient is a kick
that is what a 2:1 bus compressor is doing anyway, and it has no attack/release
artefacts to argue about. The soft clip (tanh) shaves the remaining kick crest
without the pumping a hard limiter would introduce. The limiter is last and only
catches what is left; the whole chain then re-normalises and re-checks the true
peak on a 4x-oversampled copy, looping until the ceiling actually holds - so the
reported true peak is measured, not assumed.
"""

import argparse

import numpy as np
from scipy.signal import lfilter, lfilter_zi, resample_poly
from scipy.ndimage import maximum_filter1d


def _settled(x, a):
    """One-pole smoother whose state starts settled on x[0].

    A zero-state smoother on a gain signal puts a fade-in on the front of the
    file - fatal here, because these clips have to butt-splice as loops.
    """
    b, aa = [a], [1.0, -(1.0 - a)]
    zi = lfilter_zi(b, aa) * float(x[0])
    y, _ = lfilter(b, aa, x, zi=zi)
    return y


def _stereo(x):
    x = np.asarray(x, dtype=np.float64)
    return x[:, None] if x.ndim == 1 else x


def true_peak_db(x, sr, oversample=4):
    up = resample_poly(np.asarray(x, dtype=np.float64), oversample, 1, axis=0)
    return float(20 * np.log10(np.max(np.abs(up)) + 1e-12))


def integrated_lufs(x, sr):
    import pyloudnorm as pyln
    return float(pyln.Meter(sr).integrated_loudness(np.asarray(x, dtype=np.float64)))


def normalize_lufs(x, sr, target=-16.0):
    g = 10 ** ((target - integrated_lufs(x, sr)) / 20.0)
    return (np.asarray(x) * g), float(g)


def glue_compress(x, sr, threshold_db=-20.0, ratio=2.0, attack_ms=30.0,
                  release_ms=280.0, makeup="auto"):
    """Gentle stereo-linked bus compressor. Returns (audio, mean gain reduction dB)."""
    x = _stereo(x)
    det = np.sqrt(np.mean(x ** 2, axis=1) + 1e-12)
    a_att = 1.0 - np.exp(-1.0 / (attack_ms * 1e-3 * sr))
    lvl = _settled(det, a_att)
    lvl_db = 20 * np.log10(lvl + 1e-12)
    over = np.maximum(0.0, lvl_db - threshold_db)
    gr_db = -over * (1.0 - 1.0 / ratio)
    a_rel = 1.0 - np.exp(-1.0 / (release_ms * 1e-3 * sr))
    gr_db = _settled(gr_db, a_rel)
    g = 10 ** (gr_db / 20.0)
    y = x * g[:, None]
    if makeup == "auto":
        y = y * 10 ** (-float(np.mean(gr_db)) / 20.0)
    return y, float(np.mean(gr_db))


def soft_clip(x, threshold):
    return threshold * np.tanh(np.asarray(x, dtype=np.float64) / threshold)


def limiter(x, sr, ceiling=0.891, lookahead_ms=1.5, release_ms=60.0):
    """Lookahead peak limiter (sliding-max detector, smoothed gain)."""
    x = _stereo(x)
    la = max(2, int(lookahead_ms * 1e-3 * sr))
    peak = maximum_filter1d(np.max(np.abs(x), axis=1), size=2 * la + 1, mode="nearest")
    g = np.minimum(1.0, ceiling / (peak + 1e-12))
    a = 1.0 - np.exp(-1.0 / (release_ms * 1e-3 * sr))
    g = _settled(g, a)
    g = np.minimum(g, np.minimum(1.0, ceiling / (peak + 1e-12)))
    return x * g[:, None]


def master_chain(x, sr, target_lufs=-14.0, ceiling_dbtp=-1.0, glue=True,
                 clip_drive_db=4.0, threshold_db=-20.0, ratio=2.0):
    """Full chain. Returns (audio float32, info dict of measured values)."""
    x = _stereo(x)
    pre_lufs = integrated_lufs(x, sr)
    y, gr = (glue_compress(x, sr, threshold_db, ratio) if glue else (x, 0.0))
    y, _ = normalize_lufs(y, sr, target_lufs)

    ceiling = 10 ** (ceiling_dbtp / 20.0)
    info_iters = 0
    head = ceiling
    for _ in range(8):
        info_iters += 1
        z = soft_clip(y, head * 10 ** (-clip_drive_db / 20.0) * 2.0)
        z = limiter(z, sr, ceiling=head)
        z, _ = normalize_lufs(z, sr, target_lufs)
        z = limiter(z, sr, ceiling=head)
        tp = true_peak_db(z, sr)
        if tp <= ceiling_dbtp - 0.02:
            break
        head *= 10 ** (-0.25 / 20.0)          # back the ceiling off and retry
    out = np.clip(z, -1.0, 1.0).astype(np.float32)
    return out, {
        "pre_lufs": round(pre_lufs, 2),
        "glue_gain_reduction_db": round(gr, 2),
        "integrated_lufs": round(integrated_lufs(out, sr), 2),
        "true_peak_dbfs": round(true_peak_db(out, sr), 2),
        "limiter_passes": info_iters,
    }


def main():
    import soundfile as sf
    ap = argparse.ArgumentParser(description="Master a WAV: glue comp -> soft clip -> limiter.")
    ap.add_argument("infile")
    ap.add_argument("outfile")
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--ceiling", type=float, default=-1.0)
    ap.add_argument("--no-glue", action="store_true")
    a = ap.parse_args()
    x, sr = sf.read(a.infile, always_2d=True)
    y, info = master_chain(x, sr, a.lufs, a.ceiling, glue=not a.no_glue)
    sf.write(a.outfile, y, sr, subtype="PCM_24")
    print(info)


if __name__ == "__main__":
    main()
