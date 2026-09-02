#!/usr/bin/env python3
"""Audition and layer commercial loops AS-IS. Gain is the only processing.

Two commands:

  audition  - "hear the library first": render each chosen loop on its own,
              16 s, looped, gain-trimmed only. No EQ, no drive, no
              band-limiting, no reverb, no limiter.
  combos    - layer kick + bass + chord/atmos + top/hat + perc into 60 s
              arrangements. Loops enter and leave on bar boundaries with
              equal-power crossfades. The sources are never filtered.

The one filter anywhere in this file is `mono_below(120 Hz)` on the final mix
bus, which the brief asks for as an arrangement constraint. It is applied to the
sum, never to a source.

    python layer.py audition --inv pack.json --out <dir>
    python layer.py combos   --inv pack.json --out <dir>
"""

import argparse
import json
import os
import shutil
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

import packs
from dsp import mono_below

SR = 44100
# Decision, 2026-09-02: "no processing" wins. No transposition and no
# time-stretch of any size. A loop qualifies only if its BPM already matches the
# target and its key already matches; anything else is reported as a gap, never
# resampled into place. Plain sample-rate conversion (a 48 kHz file into a
# 44.1 kHz engine) is NOT a stretch - it changes neither tempo nor pitch - and is
# the one resample still allowed.
MAX_STRETCH_PCT = 0.0
MAX_TRANSPOSE_SEMI = 0.0


# ------------------------------------------------------------- gain-only bus

def true_peak_db(x, sr=SR, oversample=4):
    up = resample_poly(np.asarray(x, dtype=np.float64), oversample, 1, axis=0)
    return float(20 * np.log10(np.max(np.abs(up)) + 1e-12))


def integrated_lufs(x, sr=SR):
    import pyloudnorm as pyln
    return float(pyln.Meter(sr).integrated_loudness(np.asarray(x, dtype=np.float64)))


def gain_only_master(x, sr=SR, target_lufs=-16.0, ceiling_dbtp=-1.0):
    """Trim gain to the loudness target, then back off if the ceiling is hit.

    Deliberately not a limiter and not a compressor: if holding -1 dBTP costs
    loudness, the clip ends up quieter than the target and the shortfall is
    reported rather than squashed away.
    """
    i0 = integrated_lufs(x, sr)
    g = 10 ** ((target_lufs - i0) / 20.0) if np.isfinite(i0) else 1.0
    y = np.asarray(x, dtype=np.float32) * g
    tp = true_peak_db(y, sr)
    if tp > ceiling_dbtp:
        y = y * 10 ** ((ceiling_dbtp - tp) / 20.0)
    return y.astype(np.float32), {
        "integrated_lufs": round(integrated_lufs(y, sr), 2),
        "true_peak_dbfs": round(true_peak_db(y, sr), 2),
        "gain_db": round(20 * np.log10(max(g, 1e-12)), 2),
        "shortfall_db": round(target_lufs - integrated_lufs(y, sr), 2),
    }


# ------------------------------------------------------------ loop mechanics

def load(root, entry, target_bpm=None, semitones=0.0):
    """Load a loop untouched. Rejects anything that would need pitch or tempo work."""
    y, sr = sf.read(os.path.join(root, entry["path"]), dtype="float32", always_2d=True)
    if y.shape[1] == 1:
        y = np.repeat(y, 2, axis=1)
    if semitones:
        raise ValueError(f"transpose {semitones:+g} semitones refused: no processing")
    if target_bpm and entry.get("bpm") and int(entry["bpm"]) != int(target_bpm):
        raise ValueError(f"{entry['bpm']} BPM against a {target_bpm} BPM target: "
                         "refused, no time-stretch")
    if sr != SR:
        # sample-rate conversion only - same duration, same pitch
        y = resample_poly(y, SR, sr, axis=0).astype(np.float32)
    return y


def tile_to(y, n):
    if len(y) == 0:
        return np.zeros((n, 2), dtype=np.float32)
    reps = int(np.ceil(n / len(y)))
    return np.tile(y, (reps, 1))[:n].astype(np.float32)


def equal_power_window(n_total, fade):
    """1-2 bar equal-power in/out ramps."""
    w = np.ones(n_total, dtype=np.float32)
    f = int(min(fade, n_total // 2))
    if f > 0:
        r = np.linspace(0, 1, f, dtype=np.float32)
        w[:f] = np.sqrt(r)
        w[-f:] = np.sqrt(r[::-1])
    return w


def low_fundamental(root, entry, fmax=250.0):
    """Frequency of peak energy below fmax - 'how deep is this kick'."""
    y, sr = sf.read(os.path.join(root, entry["path"]), dtype="float32", always_2d=True)
    m = y.mean(axis=1)[: 1 << 17]
    if len(m) < 2048:
        return None
    S = np.abs(np.fft.rfft(m * np.hanning(len(m)))) ** 2
    fr = np.fft.rfftfreq(len(m), 1.0 / sr)
    band = (fr > 20) & (fr < fmax)
    if not band.any():
        return None
    return float(fr[band][int(np.argmax(S[band]))])


def key_distance(a, b):
    if a is None or b is None:
        return 0
    d = (a - b) % 12
    return min(d, 12 - d)


# ----------------------------------------------------------------- encoding

def encode(out_dir, base, audio, sr=SR):
    from measure import _ffmpeg_bin
    wav = os.path.join(out_dir, base + ".wav")
    sf.write(wav, audio, sr, subtype="PCM_24")
    ff = _ffmpeg_bin()
    m4a = base + ".m4a"
    if ff:
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", wav,
                        "-c:a", "aac", "-b:a", "160k", os.path.join(out_dir, m4a)],
                       check=False)
        return m4a
    return base + ".wav"


# ---------------------------------------------------------------- audition

def pick_for_audition(entries, root):
    def usable(e):
        return e.get("bars_integer") is not False and e["seconds"] >= 1.0
    low = lambda e: e["bands"]["<60"] + e["bands"]["60-150"]
    bass = sorted([e for e in entries if e["category"] == "bass" and usable(e)],
                  key=low, reverse=True)[:6]
    kicks = [e for e in entries if e["category"] == "kick" and usable(e)]
    kf = [(e, low_fundamental(root, e) or 1e9) for e in kicks]
    kick = [e for e, _ in sorted(kf, key=lambda t: t[1])[:4]]
    chord = sorted([e for e in entries if e["category"] in ("chord", "pad") and usable(e)],
                   key=lambda e: e["bands"]["150-600"], reverse=True)[:4]
    atmos = sorted([e for e in entries if e["category"] == "atmos" and usable(e)],
                   key=lambda e: e["width"], reverse=True)[:4]
    funds = {e["file"]: f for e, f in kf}
    return {"bass": bass, "kick": kick, "chord": chord, "atmos": atmos}, funds


def describe(cat, e, fundamental=None):
    b = e["bands"]
    if cat == "kick":
        d = f"fundamental about {fundamental:.0f} Hz" if fundamental else "kick"
        return f"{d}, {b['<60'] + b['60-150']:.0f}% of its energy under 150 Hz"
    if cat == "bass":
        return (f"{b['<60'] + b['60-150']:.0f}% under 150 Hz, "
                f"{b['150-600']:.0f}% in the body, width {e['width']:.2f}")
    if cat in ("chord", "pad"):
        return f"{b['150-600']:.0f}% in the body region, width {e['width']:.2f}"
    return f"width {e['width']:.2f}, {b['>2k']:.1f}% above 2 kHz"


def cmd_audition(inv, out_dir, seconds=16.0):
    root, entries = inv["root"], inv["entries"]
    picks, funds = pick_for_audition(entries, root)
    os.makedirs(out_dir, exist_ok=True)
    n = int(seconds * SR)
    groups, i = [], 1
    for cat in ("kick", "bass", "chord", "atmos"):
        clips = []
        for e in picks[cat]:
            try:
                y = tile_to(load(root, e), n)
            except Exception as ex:
                print("skip", e["file"], ex)
                continue
            audio, info = gain_only_master(y)
            label = describe(cat, e, funds.get(e["file"]))
            base = f"{i:02d} - {cat} - {label}"
            fn = encode(out_dir, base, audio)
            clips.append({"n": f"{i:02d}", "label": label, "source": e["file"],
                          "file": fn, "lufs": info["integrated_lufs"],
                          "true_peak": info["true_peak_dbfs"]})
            i += 1
        if clips:
            groups.append({"name": cat, "hint": f"{len(clips)} {cat} loops, "
                           "played as they came out of the pack - gain only",
                           "clips": clips})
    manifest = {
        "round": "Round 5 - loop pack audition",
        "date": "2 Sep 2026",
        "intro": ("Every clip here is a loop from the pack played untouched and "
                  "repeated for 16 seconds. The only thing done to it is a gain "
                  "trim to a common loudness and a peak ceiling. No EQ, no drive, "
                  "no filtering, no reverb - so what you are hearing is the "
                  "pack's own sound."),
        "questions": ["Which kick and which bass sound right?",
                      "Is this the quality level you were missing?",
                      "Which ones should the engine build with?"],
        "groups": groups,
    }
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    return manifest


# ------------------------------------------------------------------ combos

LAYER_PLAN = [("kick", None), ("bass", None), ("chord", 8), ("atmos", 12),
              ("hat", 12), ("perc", 20), ("top", 20)]


def compatible(a, b):
    """Same BPM and same key, or unkeyed. Nothing is bent to fit."""
    if a is None or b is None:
        return True
    if a.get("bpm") and b.get("bpm") and a["bpm"] != b["bpm"]:
        return False
    return key_distance(a.get("key_pc"), b.get("key_pc")) == 0


def report_gaps(entries, bpm, key_pc, categories):
    """Which categories have nothing usable at the target BPM and key, and why.

    With transposition and time-stretching both refused, an empty category is a
    fact about the pack that has to be surfaced rather than worked around.
    """
    gaps = {}
    for cat in categories:
        rows = [e for e in entries if e["category"] == cat]
        ragged = [e for e in rows if e.get("bars_integer") is False]
        wrong_bpm = [e for e in rows if e.get("bpm") and e["bpm"] != bpm]
        wrong_key = [e for e in rows if e.get("key_pc") is not None and key_pc is not None
                     and key_distance(e["key_pc"], key_pc) != 0]
        usable = [e for e in rows
                  if e.get("bars_integer") is not False
                  and not (e.get("bpm") and e["bpm"] != bpm)
                  and not (e.get("key_pc") is not None and key_pc is not None
                           and key_distance(e["key_pc"], key_pc) != 0)]
        gaps[cat] = {"total": len(rows), "usable": len(usable),
                     "rejected_wrong_bpm": len(wrong_bpm),
                     "rejected_wrong_key": len(wrong_key),
                     "rejected_ragged": len(ragged)}
    return gaps


def cmd_combos(inv, out_dir, seconds=60.0, n_combos=4):
    root, entries = inv["root"], inv["entries"]
    bpm = packs.dominant(entries, "bpm") or 124
    key = packs.dominant(entries, "key")
    key_pc = next((e["key_pc"] for e in entries if e["key"] == key), None)
    beat = 60.0 / bpm
    bar = 4 * beat
    bars = max(4, int(round(seconds / bar)))
    n = int(round(bars * bar * SR))
    os.makedirs(out_dir, exist_ok=True)

    def pool(cat):
        out = []
        for e in entries:
            if e["category"] != cat or e.get("bars_integer") is False:
                continue
            if e.get("bpm") and e["bpm"] != bpm:
                continue
            if e.get("key_pc") is not None and key_pc is not None \
                    and key_distance(e["key_pc"], key_pc) > MAX_TRANSPOSE_SEMI:
                continue
            out.append(e)
        return out

    pools = {c: pool(c) for c, _ in LAYER_PLAN}
    gaps = report_gaps(entries, bpm, key_pc, [c for c, _ in LAYER_PLAN])
    empty = [c for c, g in gaps.items() if g["usable"] == 0 and g["total"] > 0]
    for c in empty:
        g = gaps[c]
        print(f"GAP: '{c}' has {g['total']} files but none usable at {bpm} BPM / "
              f"{key or 'no key'} - {g['rejected_wrong_bpm']} wrong BPM, "
              f"{g['rejected_wrong_key']} wrong key, {g['rejected_ragged']} ragged. "
              "Not transposed and not stretched, by decision.")
    for c, g in gaps.items():
        if g["total"] == 0:
            print(f"GAP: no '{c}' loops in this pack at all")
    kicks = sorted(pools["kick"], key=lambda e: low_fundamental(root, e) or 1e9)
    basses = sorted(pools["bass"],
                    key=lambda e: e["bands"]["<60"] + e["bands"]["60-150"], reverse=True)
    if not kicks or not basses:
        raise RuntimeError(
            f"need at least one kick and one bass at {bpm} BPM in "
            f"{key or 'the pack key'} (have {len(kicks)} kicks, {len(basses)} basses). "
            "Nothing is transposed or stretched to fill the gap - see the gap report.")

    clips, rows = [], []
    for ci in range(n_combos):
        used = {}
        mix = np.zeros((n, 2), dtype=np.float32)
        for cat, period in LAYER_PLAN:
            p = kicks if cat == "kick" else basses if cat == "bass" else pools.get(cat, [])
            if not p:
                continue
            e = p[ci % len(p)] if cat in ("kick", "bass") else p[(ci + 1) % len(p)]
            if any(not compatible(e, u) for u in used.values()):
                continue
            try:
                y = load(root, e, target_bpm=bpm)
            except Exception as ex:
                print("skip", e["file"], ex)
                continue
            used[cat] = e
            if period is None:                      # anchors run the whole clip
                mix += tile_to(y, n)
                continue
            # coprime-ish entry/exit cycle with equal-power crossfades
            fade = int(round((2 if cat in ("chord", "atmos") else 1) * bar * SR))
            on = max(2, period - (2 if period >= 12 else 1))
            lay = np.zeros((n, 2), dtype=np.float32)
            b0 = (ci * 2) % period
            while b0 < bars:
                s = int(round(b0 * bar * SR))
                ln = int(round(min(on, bars - b0) * bar * SR))
                if ln > 2 * fade:
                    seg = tile_to(y, ln) * equal_power_window(ln, fade)[:, None]
                    lay[s:s + ln] += seg
                b0 += period
            mix += lay
        mix = mono_below(mix / max(1.0, np.sqrt(len(used))), 120.0)
        audio, info = gain_only_master(mix, target_lufs=-16.0)
        label = (f"{used.get('kick', {}).get('file', '?')} + "
                 f"{used.get('bass', {}).get('file', '?')}")
        base = f"{90 + ci + 1} - combo {ci + 1} - {bpm} BPM {key or 'no key'}"
        fn = encode(out_dir, base, audio)
        clips.append({"n": str(90 + ci + 1), "label": f"combo {ci + 1}: " + label,
                      "source": ", ".join(f"{k}: {v['file']}" for k, v in used.items()),
                      "file": fn, **info})
        rows.append((base, used, info))
        print("wrote", base, "layers:", list(used))
    manifest = {"round": "Round 5 - layered combos", "date": "2 Sep 2026",
                "intro": (f"Four arrangements at {bpm} BPM in {key or 'the pack key'}, "
                          "built only by choosing, layering and crossfading loops from "
                          "the pack. Nothing is EQ'd, driven or filtered; the only "
                          "processing is a gain trim and mono below 120 Hz on the bus."),
                "questions": ["Does this sound like a record now?",
                              "Which combo works best?", "What is still missing?"],
                "gaps": gaps,
                "groups": [{"name": "Layered combos", "hint": "kick + bass + chord/atmos "
                            "+ hat/top + percussion, entering and leaving on bar lines",
                            "clips": clips}]}
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["audition", "combos"])
    ap.add_argument("--inv", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--wipe", action="store_true")
    a = ap.parse_args()
    with open(a.inv) as f:
        inv = json.load(f)
    if a.wipe and os.path.isdir(a.out):
        shutil.rmtree(a.out)
    m = cmd_audition(inv, a.out) if a.cmd == "audition" else cmd_combos(inv, a.out)
    print(json.dumps(m, indent=1)[:1500])


if __name__ == "__main__":
    main()
