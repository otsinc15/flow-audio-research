#!/usr/bin/env python3
"""Throwaway fixture: a fake loop pack, purely to exercise packs.py and layer.py.

THIS IS NOT AUDITION MATERIAL. Round 5 exists because synthesised sound was
rejected; nothing this script produces should ever reach a listening folder. It
exists so the ingest and layering code can be run end to end before the real
pack arrives - filenames in the Riemann convention, whole numbers of bars, a
mix of categories and keys.

    python make_test_pack.py --out ~/flow-synth/testpack
"""

import argparse
import os

import numpy as np
import soundfile as sf

SR = 44100
BPM = 124
KEY = "Am"
BARS = 2


def _n(bars=BARS, bpm=BPM):
    return int(round(bars * 4 * 60.0 / bpm * SR))


def _st(m):
    return np.stack([m, m], axis=1).astype(np.float32)


def _wide(m, d=400):
    r = np.concatenate([np.zeros(d, dtype=np.float32), m])[: len(m)]
    return np.stack([m, r], axis=1).astype(np.float32)


def make(rng, kind):
    n = _n()
    t = np.arange(n) / SR
    beat = 60.0 / BPM
    if kind.startswith("kick"):
        deep = 42.0 if "deep" in kind else 58.0
        out = np.zeros(n, dtype=np.float32)
        for b in range(8):
            s = int(b * beat * SR)
            k = int(0.45 * SR)
            tt = np.arange(k) / SR
            f = deep + 90 * np.exp(-tt / 0.03)
            v = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.12)
            out[s:s + k] += v.astype(np.float32)
        return _st(out * 0.7)
    if kind.startswith("bass"):
        f0 = 55.0 if "sub" in kind else 82.4
        env = np.ones(n, dtype=np.float32)
        for b in range(8):
            s = int(b * beat * SR)
            env[s:s + int(0.06 * SR)] = 0.0
        v = np.sin(2 * np.pi * f0 * t) + (0.4 * np.sin(2 * np.pi * f0 * 2 * t)
                                          if "harm" in kind else 0.0)
        return _st((v * env * 0.5).astype(np.float32))
    if kind.startswith("chord"):
        v = sum(np.sin(2 * np.pi * f * t) for f in (220.0, 261.6, 329.6)) / 3
        env = np.zeros(n, dtype=np.float32)
        for b in (1, 3, 5, 7):
            s = int(b * beat * SR)
            k = int(0.35 * SR)
            env[s:s + k] = np.exp(-np.arange(k) / (0.12 * SR))
        return _wide((v * env * 0.6).astype(np.float32))
    if kind.startswith("atmos"):
        v = rng.standard_normal(n).astype(np.float32) * 0.05
        return _wide(np.convolve(v, np.ones(400) / 400, mode="same").astype(np.float32), 900)
    if kind.startswith("hat"):
        out = np.zeros(n, dtype=np.float32)
        for b in range(16):
            s = int((b * beat / 2 + beat / 2) * SR)
            k = int(0.05 * SR)
            if s + k < n:
                out[s:s + k] += (rng.standard_normal(k) * np.exp(-np.arange(k) / (0.006 * SR))).astype(np.float32)
        return _wide(out * 0.25, 120)
    if kind.startswith("perc"):
        out = np.zeros(n, dtype=np.float32)
        for b in (2, 6, 11):
            s = int(b * beat / 2 * SR)
            k = int(0.2 * SR)
            if s + k < n:
                tt = np.arange(k) / SR
                out[s:s + k] += (np.sin(2 * np.pi * 380 * tt) * np.exp(-tt / 0.05)).astype(np.float32)
        return _wide(out * 0.4, 300)
    out = rng.standard_normal(n).astype(np.float32) * 0.03
    return _wide(out, 700)


SPECS = [
    ("Kick", ["kick_deep", "kick_deep2", "kick_tight", "kick_tight2"]),
    ("Bass", ["bass_sub", "bass_sub_harm", "bass_mid", "bass_mid_harm",
              "bass_sub_b", "bass_mid_b"]),
    ("Chord", ["chord_a", "chord_b", "chord_c", "chord_d"]),
    ("Atmosphere", ["atmos_a", "atmos_b", "atmos_c", "atmos_d"]),
    ("Hihat", ["hat_a", "hat_b"]),
    ("Percussion", ["perc_a", "perc_b"]),
    ("Top", ["top_a", "top_b"]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rng = np.random.default_rng(5)
    total = 0
    for folder, kinds in SPECS:
        d = os.path.join(a.out, folder)
        os.makedirs(d, exist_ok=True)
        for k in kinds:
            y = make(rng, k)
            name = f"TESTPACK_{folder}_{k.title().replace('_', '')}_{BPM}_{KEY}.wav"
            sf.write(os.path.join(d, name), y, SR, subtype="PCM_24")
            total += 1
    # one deliberately broken file, so the "not a whole number of bars" path is exercised
    d = os.path.join(a.out, "Bass")
    y = make(rng, "bass_sub")[: int(len(make(rng, "bass_sub")) * 0.63)]
    sf.write(os.path.join(d, f"TESTPACK_Bass_Ragged_{BPM}_{KEY}.wav"), y, SR, subtype="PCM_24")
    total += 1
    print(f"wrote {total} test loops to {a.out}")


if __name__ == "__main__":
    main()
