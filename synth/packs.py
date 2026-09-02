#!/usr/bin/env python3
"""Ingest a commercial loop pack: parse, categorise, measure, inventory.

Round 5 abandons synthesis. Daniel's verdict on round 4 was that all eight bass
candidates sounded "all the same, computer-generated", and measurement agreed:
they sat within about 1 dB of each other in every band, because a chain of
band-limiting, drive and loudness normalisation erases whatever made the source
distinctive. So the sources are now professionally produced loops, and the code
is forbidden from processing them - it may only select, layer, crossfade and
trim gain.

This module is the read-only half: it never writes audio.

    python packs.py --pack ~/flow-synth/packs/riemann --name riemann-techno-starter \
        --out research/ear-test/pack-inventory-riemann-techno-starter.md
"""

import argparse
import json
import os
import re

import numpy as np

SR = 44100
BAND_EDGES = [0, 60, 150, 600, 2000, SR / 2]
BAND_LABELS = ["<60", "60-150", "150-600", "600-2k", ">2k"]

CATEGORIES = [
    ("kick", ("kick", "bd", "bassdrum")),
    ("bass", ("bass", "sub", "808")),
    ("chord", ("chord", "stab", "keys", "rhodes")),
    ("pad", ("pad", "string")),
    ("atmos", ("atmos", "atmo", "ambient", "drone", "texture", "noise")),
    ("top", ("top", "loop_top", "tops")),
    ("hat", ("hat", "hh", "hihat", "openhat", "closedhat")),
    ("perc", ("perc", "percussion", "conga", "bongo", "shaker", "tom")),
    ("clap", ("clap", "snap")),
    ("snare", ("snare", "sd", "rim")),
    ("ride", ("ride", "crash", "cymbal")),
    ("synth", ("synth", "lead", "arp", "pluck", "seq")),
    ("groove", ("groove", "beat", "drums", "fullbeat")),
    ("fx", ("fx", "riser", "impact", "sweep", "downlifter", "uplifter")),
]

NOTE_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
PC_NAME = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

_BPM_PATTERNS = [
    re.compile(r"(?:^|[_\-\s])(\d{2,3})\s*bpm", re.I),
    re.compile(r"bpm\s*[_\-]?\s*(\d{2,3})", re.I),
    re.compile(r"(?:^|[_\-\s])(\d{2,3})(?=[_\-\s])"),
]
_KEY_RE = re.compile(
    r"(?:^|[_\-\s])([A-G])\s*([#b]?)\s*"
    r"(m(?:in(?:or)?)?|maj(?:or)?|M)?(?=[_\-\s.]|$)")


def parse_bpm(name):
    for pat in _BPM_PATTERNS:
        for m in pat.finditer(name):
            v = int(m.group(1))
            if 60 <= v <= 200:
                return v
    return None


def parse_key(name):
    """Returns (pitch_class, mode) with mode in {'min','maj'}, or (None, None).

    Handles the Riemann convention (`..._124_Am.wav`) plus 'A min', 'Amin',
    'Aminor', 'F#m', 'Cmaj'. A bare letter with no mode is read as minor, which
    is what this genre uses and what the packs mean by 'Am'.
    """
    stem = os.path.splitext(os.path.basename(name))[0]
    best = None
    for m in _KEY_RE.finditer(stem):
        letter, acc, mode = m.group(1), m.group(2) or "", (m.group(3) or "").lower()
        # a lone capital letter mid-word is usually not a key; require a mode
        # marker or a trailing position
        if not mode and m.end() < len(stem) - 1:
            continue
        pc = (NOTE_PC[letter] + (1 if acc == "#" else -1 if acc == "b" else 0)) % 12
        md = "maj" if mode.startswith("maj") or mode == "m".upper() else "min"
        if mode in ("maj", "major", "m") and mode != "m":
            md = "maj"
        best = (pc, md)
    return best if best else (None, None)


def categorise(path):
    parts = [p.lower() for p in path.replace("\\", "/").split("/")]
    hay = " ".join(parts)
    for cat, tokens in CATEGORIES:
        for t in tokens:
            # prefix match, not whole-word: pack folders say "Atmosphere",
            # "Percussion", "Hihats", and a trailing word boundary misses all of
            # them. Category order resolves the overlaps (a "bassdrum" is caught
            # by kick before bass ever sees it).
            if re.search(rf"(?:^|[^a-z]){re.escape(t)}", hay):
                return cat
    return "other"


def stereo_width(y):
    """0 = mono, 1 = fully decorrelated. side/mid energy, capped."""
    if y.shape[1] < 2:
        return 0.0
    mid = 0.5 * (y[:, 0] + y[:, 1])
    side = 0.5 * (y[:, 0] - y[:, 1])
    m = float(np.sqrt(np.mean(mid ** 2))) + 1e-12
    s = float(np.sqrt(np.mean(side ** 2)))
    return float(min(1.0, s / m))


def band_shares(mono, sr):
    n = min(len(mono), 1 << 18)
    w = mono[:n] * np.hanning(n)
    S = np.abs(np.fft.rfft(w)) ** 2
    fr = np.fft.rfftfreq(n, 1.0 / sr)
    tot = float(S.sum()) + 1e-30
    out = {}
    for i, lab in enumerate(BAND_LABELS):
        hi = BAND_EDGES[i + 1] if i + 1 < len(BAND_EDGES) else sr / 2
        out[lab] = round(float(S[(fr >= BAND_EDGES[i]) & (fr < hi)].sum() / tot * 100), 2)
    return out


def measure_file(path, root):
    import soundfile as sf
    import pyloudnorm as pyln
    try:
        y, sr = sf.read(path, dtype="float32", always_2d=True)
    except Exception as e:
        return {"path": os.path.relpath(path, root), "error": str(e)}
    mono = y.mean(axis=1)
    dur = len(y) / sr
    rel = os.path.relpath(path, root)
    bpm = parse_bpm(os.path.basename(path)) or parse_bpm(rel)
    pc, mode = parse_key(os.path.basename(path))
    bars = None
    bars_ok = None
    if bpm:
        bars = dur / (4 * 60.0 / bpm)
        bars_ok = abs(bars - round(bars)) < 0.02
    try:
        lufs = float(pyln.Meter(sr).integrated_loudness(y.astype(np.float64)))
    except Exception:
        lufs = None
    return {
        "path": rel,
        "file": os.path.basename(path),
        "category": categorise(rel),
        "sr": int(sr),
        "channels": int(y.shape[1]),
        "seconds": round(dur, 3),
        "bpm": bpm,
        "bars": round(bars, 3) if bars is not None else None,
        "bars_integer": bars_ok,
        "key_pc": pc,
        "key": (PC_NAME[pc] + ("m" if mode == "min" else "maj")) if pc is not None else None,
        "mode": mode,
        "lufs": round(lufs, 2) if lufs is not None and np.isfinite(lufs) else None,
        "width": round(stereo_width(y), 3),
        "bands": band_shares(mono, sr),
        "peak_dbfs": round(float(20 * np.log10(np.max(np.abs(y)) + 1e-12)), 2),
    }


def ingest(root):
    out = []
    for dirpath, _, files in os.walk(root):
        for fn in sorted(files):
            if fn.lower().endswith((".wav", ".aif", ".aiff", ".flac")):
                out.append(measure_file(os.path.join(dirpath, fn), root))
    return [e for e in out if "error" not in e]


def dominant(entries, field):
    vals = [e[field] for e in entries if e.get(field) is not None]
    if not vals:
        return None
    return max(set(vals), key=vals.count)


def write_markdown(entries, pack_name, root, out_path):
    from collections import Counter
    cats = Counter(e["category"] for e in entries)
    bpms = Counter(e["bpm"] for e in entries if e["bpm"])
    keys = Counter(e["key"] for e in entries if e["key"])
    noninteger = [e for e in entries if e["bars_integer"] is False]
    nobpm = [e for e in entries if not e["bpm"]]
    lines = []
    A = lines.append
    A(f"# Pack inventory: {pack_name}\n")
    A("Generated by `synth/packs.py`. Read-only: nothing here modifies or writes audio. "
      "Band shares are power shares of the whole file, LUFS is EBU R128 integrated, "
      "width is side/mid energy (0 = mono).\n")
    A(f"- Files: **{len(entries)}**")
    A(f"- Source folder: `{root}`")
    A(f"- Dominant BPM: **{dominant(entries, 'bpm')}** "
      f"({', '.join(f'{k}: {v}' for k, v in bpms.most_common(6))})")
    A(f"- Dominant key: **{dominant(entries, 'key')}** "
      f"({', '.join(f'{k}: {v}' for k, v in keys.most_common(6))})")
    A(f"- Categories: {', '.join(f'{k} {v}' for k, v in cats.most_common())}")
    A(f"- Files with no parseable BPM: **{len(nobpm)}**")
    A(f"- Files whose length is not a whole number of bars at the parsed BPM: "
      f"**{len(noninteger)}**"
      + (" — listed at the end" if noninteger else ""))
    A("")
    for cat, _ in cats.most_common():
        rows = [e for e in entries if e["category"] == cat]
        A(f"## {cat} ({len(rows)})\n")
        A("| File | BPM | Key | Bars | s | LUFS | Peak | Width | <60 | 60-150 | 150-600 | 600-2k | >2k |")
        A("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for e in sorted(rows, key=lambda x: x["file"]):
            b = e["bands"]
            A(f"| `{e['file']}` | {e['bpm'] or '—'} | {e['key'] or '—'} | "
              f"{('%.2f' % e['bars']) if e['bars'] is not None else '—'}"
              f"{'' if e['bars_integer'] is not False else ' ⚠'} | {e['seconds']} | "
              f"{e['lufs'] if e['lufs'] is not None else '—'} | {e['peak_dbfs']} | {e['width']} | "
              f"{b['<60']} | {b['60-150']} | {b['150-600']} | {b['600-2k']} | {b['>2k']} |")
        A("")
    if noninteger:
        A("## Files that are not a whole number of bars\n")
        A("These cannot be layered on the grid without trimming, so the engine skips them.\n")
        for e in noninteger:
            A(f"- `{e['file']}` — {e['seconds']} s = {e['bars']:.3f} bars at {e['bpm']} BPM")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    entries = ingest(a.pack)
    write_markdown(entries, a.name, a.pack, a.out)
    if a.json:
        with open(a.json, "w") as f:
            json.dump({"pack": a.name, "root": a.pack, "entries": entries}, f)
    print(f"{len(entries)} files, dominant BPM {dominant(entries,'bpm')}, "
          f"dominant key {dominant(entries,'key')} -> {a.out}")


if __name__ == "__main__":
    main()
