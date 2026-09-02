#!/usr/bin/env python3
"""A sampler voice, so the instruments can be recordings of real synthesisers.

Rounds 1-3 built every voice from parameters. Round 3 established that only one
plugin's factory presets could be loaded at all. This module takes the other
route: Legowelt's free multisample packs are recordings of actual hardware
(Prophet 600, Jupiter 8, Oberheim Matrix 1000), one WAV per note, so playing them
from our own sequencer gives real analogue synth tone in our key and tempo.

Two parts:
  * an inventory pass that measures every WAV once (pitch, length, loop points,
    channels) and caches it as JSON - pitch detection is too slow to redo per render;
  * a Sampler that plays a note by choosing the nearest-pitched sample and
    resampling it, never further than +/-7 semitones so nothing sounds chipmunked.

    python sampler.py --inventory ~/flow-synth/samples --out inventory.json
"""

import argparse
import json
import os
import re
import struct

import numpy as np
from scipy.signal import resample_poly

SR = 44100
MAX_SHIFT_SEMITONES = 7.0


# ------------------------------------------------------------------ WAV bits

def read_loop_points(path):
    """Return (start, end) from a WAV 'smpl' chunk, or None."""
    try:
        with open(path, "rb") as f:
            data = f.read(4096 * 16)
        i = data.find(b"smpl")
        if i < 0:
            return None
        body = data[i + 8:]
        if len(body) < 36 + 24:
            return None
        num_loops = struct.unpack_from("<I", body, 28)[0]
        if num_loops < 1:
            return None
        start, end = struct.unpack_from("<II", body, 36 + 8)
        return (int(start), int(end)) if end > start else None
    except Exception:
        return None


NOTE_RE = re.compile(r"(?:^|[^A-Za-z])([A-Ga-g])([#b]?)(-?[0-9])(?:[^0-9]|$)")
NOTE_BASE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def note_from_name(fname):
    """Many multisample packs name the file after the note - free and exact."""
    m = NOTE_RE.search(os.path.splitext(os.path.basename(fname))[0])
    if not m:
        return None
    letter, acc, octv = m.group(1).upper(), m.group(2), int(m.group(3))
    n = NOTE_BASE[letter] + (1 if acc == "#" else -1 if acc == "b" else 0)
    return 12 * (octv + 1) + n


def detect_pitch(y, sr):
    import librosa
    try:
        f0 = librosa.yin(y.astype(np.float32), fmin=27.5, fmax=2000.0, sr=sr,
                         frame_length=2048)
        f0 = f0[np.isfinite(f0)]
        if len(f0) < 4:
            return None
        mid = f0[len(f0) // 6: max(len(f0) // 6 + 1, len(f0) * 2 // 3)]
        hz = float(np.median(mid if len(mid) else f0))
        if not (20.0 < hz < 4000.0):
            return None
        return 69.0 + 12.0 * np.log2(hz / 440.0)
    except Exception:
        return None


def inventory(root, limit_seconds=3.0):
    """Measure every WAV under `root` once. Returns a list of dicts."""
    import soundfile as sf
    out = []
    for dirpath, _, files in os.walk(root):
        for fn in sorted(files):
            if not fn.lower().endswith(".wav"):
                continue
            p = os.path.join(dirpath, fn)
            try:
                info = sf.info(p)
                y, sr = sf.read(p, frames=int(limit_seconds * info.samplerate),
                                dtype="float32", always_2d=True)
            except Exception:
                continue
            mono = y.mean(axis=1)
            # band shares, so an instrument can be chosen by what it actually
            # contains rather than by where its filename sorts. The first pass
            # picked "Bass Acidiscrete" simply because it was alphabetically
            # first, and it turned out to have 1.3 % of its energy below 60 Hz.
            w = mono[: 1 << 16]
            if len(w) >= 4096:
                S = np.abs(np.fft.rfft(w * np.hanning(len(w)))) ** 2
                fr = np.fft.rfftfreq(len(w), 1.0 / sr)
                tot = float(S.sum()) + 1e-30
                shares = {"sub": float(S[fr < 60].sum() / tot),
                          "low": float(S[fr < 150].sum() / tot),
                          "body": float(S[(fr >= 150) & (fr < 500)].sum() / tot),
                          "mid": float(S[(fr >= 500) & (fr < 2000)].sum() / tot),
                          "hi": float(S[fr >= 2000].sum() / tot)}
            else:
                shares = {k: 0.0 for k in ("sub", "low", "body", "mid", "hi")}
            named = note_from_name(fn)
            det = detect_pitch(mono[: int(2.0 * sr)], sr)
            # trust the filename when it exists and roughly agrees, else the detector
            midi = named if named is not None and (det is None or abs(det - named) < 2.0) \
                else (det if det is not None else named)
            rel = os.path.relpath(p, root)
            out.append({
                "path": rel,
                "pack": rel.split(os.sep)[0],
                "category": os.path.basename(dirpath),
                "sr": int(info.samplerate),
                "seconds": round(info.frames / info.samplerate, 3),
                "channels": int(info.channels),
                "midi": round(float(midi), 2) if midi is not None else None,
                "midi_source": ("name" if named is not None and midi == named
                                else ("detected" if det is not None else None)),
                "loop": read_loop_points(p),
                "rms": round(float(np.sqrt(np.mean(mono ** 2))), 6),
                **{k: round(v, 5) for k, v in shares.items()},
            })
    return out


# -------------------------------------------------------------------- voice

class Sampler:
    """Plays one 'instrument' - a set of multisamples of the same synth patch."""

    def __init__(self, root_dir, entries, sr=SR, gain=1.0):
        self.root = root_dir
        self.entries = [e for e in entries if e.get("midi") is not None]
        if not self.entries:
            raise ValueError("sampler instrument has no pitched samples")
        self.sr = sr
        self.gain = gain
        self._cache = {}

    def _audio(self, e):
        if e["path"] not in self._cache:
            import soundfile as sf
            y, sr = sf.read(os.path.join(self.root, e["path"]),
                            dtype="float32", always_2d=True)
            if sr != self.sr:
                y = resample_poly(y, self.sr, sr, axis=0).astype(np.float32)
            self._cache[e["path"]] = y
        return self._cache[e["path"]]

    def pick(self, midi):
        return min(self.entries, key=lambda e: abs(e["midi"] - midi))

    def note(self, midi, seconds, velocity=1.0, attack=0.004, decay=None,
             sustain=1.0, release=0.08):
        """Render one note. Resampling is capped at +/-7 semitones."""
        e = self.pick(midi)
        shift = midi - e["midi"]
        if abs(shift) > MAX_SHIFT_SEMITONES:
            shift = float(np.clip(shift, -MAX_SHIFT_SEMITONES, MAX_SHIFT_SEMITONES))
        y = self._audio(e)
        n_out = int(round((seconds + release) * self.sr))
        ratio = 2.0 ** (shift / 12.0)
        src_len = y.shape[0]
        idx = np.arange(n_out, dtype=np.float64) * ratio
        loop = e.get("loop")
        if loop and loop[1] > loop[0] + 64:
            ls, le = loop
            over = idx >= le
            if over.any():
                span = le - ls
                idx = np.where(over, ls + np.mod(idx - ls, span), idx)
        else:
            idx = np.clip(idx, 0, src_len - 1)
        idx = np.clip(idx, 0, src_len - 1)
        src = np.arange(src_len, dtype=np.float64)
        out = np.stack([np.interp(idx, src, y[:, c % y.shape[1]])
                        for c in range(2)], axis=1).astype(np.float32)
        t = np.arange(n_out) / self.sr
        env = np.clip(t / max(attack, 1e-4), 0, 1)
        if decay:
            env = env * (sustain + (1 - sustain) * np.exp(-np.clip(t - attack, 0, None) / decay))
        rel = np.ones(n_out, dtype=np.float64)
        r0 = int(seconds * self.sr)
        if r0 < n_out:
            rel[r0:] = np.exp(-(t[r0:] - t[r0]) / max(release, 1e-4))
        return out * (env * rel * velocity * self.gain)[:, None].astype(np.float32)

    def render(self, notes, total_samples):
        """notes: (t_on, duration_s, midi, velocity)."""
        buf = np.zeros((total_samples, 2), dtype=np.float32)
        for t0, dur, midi, vel in notes:
            v = self.note(midi, dur, vel)
            s = int(round(t0 * self.sr))
            if s >= total_samples:
                continue
            e = min(total_samples, s + v.shape[0])
            buf[s:e] += v[: e - s]
        return buf


def load_inventory(path):
    with open(path) as f:
        return json.load(f)


def select(entries, pack=None, path_contains=None, category=None,
           min_midi=None, max_midi=None, min_seconds=None, max_seconds=None,
           exclude=None, min_low=None, max_mid=None, sort_by=None, descending=True):
    out = []
    for e in entries:
        if pack and e["pack"] != pack:
            continue
        if path_contains and path_contains.lower() not in e["path"].lower():
            continue
        if category and category.lower() not in (e["category"] or "").lower():
            continue
        if e.get("midi") is None:
            continue
        if min_midi is not None and e["midi"] < min_midi:
            continue
        if max_midi is not None and e["midi"] > max_midi:
            continue
        if min_seconds is not None and e["seconds"] < min_seconds:
            continue
        if max_seconds is not None and e["seconds"] > max_seconds:
            continue
        if exclude and any(x.lower() in e["path"].lower() for x in exclude):
            continue
        if min_low is not None and e.get("low", 0.0) < min_low:
            continue
        if max_mid is not None and e.get("mid", 1.0) > max_mid:
            continue
        out.append(e)
    if sort_by:
        out.sort(key=lambda e: e.get(sort_by, 0.0), reverse=descending)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    inv = inventory(a.inventory)
    with open(a.out, "w") as f:
        json.dump(inv, f)
    packs = {}
    for e in inv:
        d = packs.setdefault(e["pack"], {"n": 0, "pitched": 0, "looped": 0, "cats": set()})
        d["n"] += 1
        d["pitched"] += e["midi"] is not None
        d["looped"] += e["loop"] is not None
        d["cats"].add(e["category"])
    for k, v in sorted(packs.items()):
        print(f"{k:14s} files={v['n']:4d} pitched={v['pitched']:4d} "
              f"looped={v['looped']:4d} folders={len(v['cats'])}")


if __name__ == "__main__":
    main()
