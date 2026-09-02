#!/usr/bin/env python3
"""Round 4: a bass-only audition. Eight designed layer stacks over kick alone.

Daniel on round 3: the basses "sound terrible - we need something way more
bassy, deep, wide", and nothing else can be judged until the bass is right. So
this renders bass and kick and nothing else: no hats, no clap, no chord, no hook.

Every candidate is a STACK, not a preset:
  (a) mono sub      - sine at the root (55 Hz, A1), ducked under the kick
  (b) body 80-250Hz - a real Legowelt synth bass sample, or a synthetic
                      saturated square, band-passed into the body region
  (c) drive         - tape/tube-style saturation on the body only
  (d) width         - Haas plus mid/side on the BODY only; the sub stays mono,
                      and mono_below(120 Hz) is applied at the end to guarantee it
  (e) glue          - kick and sub through one shared saturator

The bass is deliberately mixed at or above the kick, and the target is ref02
(Endel Deeper Focus): about 80 % of energy below 150 Hz with the body region
still clearly present.

    python bass_audition.py --out <dir>
"""

import argparse
import json
import os
import shutil
import subprocess

import numpy as np
import soundfile as sf

import dsp
from dsp import SR
import sampler as smp
import surge_engine as se
from master import master_chain
from render import bass_glue

BPM = 114.8
BARS = 16
ROOT_HZ = 55.0
ROOT_MIDI = 33
SAMPLE_ROOT = os.path.expanduser("~/flow-synth/samples")


# ------------------------------------------------------------------ helpers

def pick_bass(inv, pack, contains="Bass"):
    """Nearest-pitched, low-heavy bass sample from a pack."""
    ents = smp.select(inv, pack=pack, path_contains=contains,
                      min_midi=26, max_midi=42, min_low=0.55)
    if not ents:
        ents = smp.select(inv, pack=pack, path_contains=contains,
                          min_midi=26, max_midi=42)
    if not ents:
        raise RuntimeError(f"no bass samples in {pack}")
    return sorted(ents, key=lambda e: (abs(e["midi"] - ROOT_MIDI), -e.get("low", 0)))[0]


def widen(x, haas_ms=6.5, side=1.0):
    """Width on the body only: a short Haas offset plus a mid/side lift."""
    d = int(haas_ms * 1e-3 * SR)
    r = np.concatenate([np.zeros(d, dtype=np.float32), x[:, 1]])[: len(x)]
    y = np.stack([x[:, 0], r], axis=1)
    mid = 0.5 * (y[:, 0] + y[:, 1])
    sd = 0.5 * (y[:, 0] - y[:, 1])
    return np.stack([mid + side * sd, mid - side * sd], axis=1).astype(np.float32)


def rms(x):
    return float(np.sqrt(np.mean(np.asarray(x, dtype=np.float64) ** 2)))


# -------------------------------------------------------------------- parts

def build_grid():
    beat = 60.0 / BPM
    bar = 4 * beat
    n = int(round(BARS * bar * SR))
    rng = np.random.default_rng(11)
    kicks = se.faust_kicks(rng, n_variants=8)
    kbuf = np.zeros(n, dtype=np.float32)
    times = []
    for b in range(BARS * 4):
        t0 = b * beat
        times.append(t0)
        dsp.add_at(kbuf, t0 * SR, kicks[b % len(kicks)], 1.0 + 0.05 * np.sin(b * 2.399963))
    kbuf = dsp.peaking(kbuf, ROOT_HZ, 1.4, -4.5)
    duck = np.zeros(n, dtype=np.float32)
    dc = dsp.exp_decay(int(0.45 * SR), 0.080)
    for t0 in times:
        dsp.add_at(duck, t0 * SR, dc)
    return n, beat, bar, kbuf, np.clip(duck, 0, 1).astype(np.float32), times


def bass_gate(n, beat, ramp_ms=3.0):
    """Pattern-book rule 7: the first 16th of every beat is empty in the bass."""
    step = beat / 4.0
    g = np.ones(n, dtype=np.float32)
    r = int(ramp_ms * 1e-3 * SR)
    for b in range(BARS * 4):
        s0 = int(round(b * beat * SR))
        if s0 >= n:
            break
        e0 = min(n, s0 + int(round(step * SR)))
        g[s0:e0] = 0.0
        if e0 + r < n:
            g[e0:e0 + r] = np.linspace(0, 1, r, dtype=np.float32)
        if s0 - r >= 0:
            g[s0 - r:s0] = np.linspace(1, 0, r, dtype=np.float32)
    return g


def sub_layer(n, gate, duck, duck_depth=0.55, decay_808=None, beat=None):
    """Pure sine at the root, mono, ducked. Optionally an 808-style long decay."""
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * ROOT_HZ * t).astype(np.float32)
    if decay_808 and beat:
        env = np.zeros(n, dtype=np.float32)
        d = dsp.exp_decay(int(min(decay_808 * 4, 3.0) * SR), decay_808)
        for b in range(BARS * 4):
            dsp.add_at(env, b * beat * SR, d)
        s = s * np.clip(env, 0, 1.4)
    return s * gate * (1.0 - duck_depth * duck)


def sampled_body(entry, n, beat, gate, lo=78.0, hi=205.0):
    sp = smp.Sampler(SAMPLE_ROOT, [entry])
    notes = [(b * beat, beat * 1.05, ROOT_MIDI, 1.0) for b in range(BARS * 4)]
    y = sp.render(notes, n)
    y = np.stack([dsp.highpass(dsp.lowpass(y[:, i], hi, 0.8), lo, 0.9)
                  for i in (0, 1)], axis=1)
    return y * gate[:, None]


def synthetic_body(n, beat, gate, lo=78.0, hi=205.0):
    """A saturated square through a warm low-pass - the no-sample control."""
    t = np.arange(n) / SR
    sq = np.sign(np.sin(2 * np.pi * ROOT_HZ * 2 * t)).astype(np.float32) * 0.5
    saw = dsp.saw(ROOT_HZ * 2, n, max_hz=1800.0)
    v = dsp.soft_clip((sq + 0.7 * saw) * 1.8, 0.7)
    v = dsp.highpass(dsp.lowpass(v, hi, 0.8), lo, 0.9)
    return np.stack([v, v], axis=1) * gate[:, None]


def drive(x, drive_db):
    import pedalboard
    b = pedalboard.Pedalboard([pedalboard.Distortion(drive_db=float(drive_db)),
                               pedalboard.LowpassFilter(cutoff_frequency_hz=620.0)])
    y = b(np.ascontiguousarray(x.T), SR)
    return np.ascontiguousarray(np.asarray(y, dtype=np.float32).T)


# ---------------------------------------------------------------- candidates

CANDIDATES = [
    ("deep sub + Prophet 600 body, light drive, wide", "Legowelt Prophet 600",
     dict(pack="prophet600", drive_db=6, haas=7.0, side=1.35, sub=1.00, body=0.42)),
    ("deep sub + Prophet 600 body, heavy drive, narrow", "Legowelt Prophet 600",
     dict(pack="prophet600", drive_db=17, haas=2.0, side=0.6, sub=1.00, body=0.50)),
    ("deep sub + Jupiter 8 body, medium drive, wide", "Legowelt Jupiter 8",
     dict(pack="jupiter8", drive_db=11, haas=8.0, side=1.45, sub=1.00, body=0.46)),
    ("deep sub + Matrix 1000 body, medium drive, wide", "Legowelt Matrix 1000",
     dict(pack="matrix1000", drive_db=11, haas=7.5, side=1.40, sub=1.00, body=0.46)),
    ("sub-forward 70-30, Prophet 600 body, light drive", "Legowelt Prophet 600",
     dict(pack="prophet600", drive_db=5, haas=5.0, side=1.10, sub=1.30, body=0.24)),
    ("body-forward 40-60, Matrix 1000 body, heavy drive", "Legowelt Matrix 1000",
     dict(pack="matrix1000", drive_db=19, haas=6.0, side=1.30, sub=0.75, body=0.72)),
    ("synthetic saturated square body, no samples", "synthetic",
     dict(pack=None, drive_db=13, haas=6.0, side=1.25, sub=1.00, body=0.46)),
    ("long 808-style sustained sub + Jupiter 8 body", "Legowelt Jupiter 8",
     dict(pack="jupiter8", drive_db=9, haas=7.0, side=1.30, sub=1.15, body=0.40,
          decay_808=0.62)),
]


def render_candidate(spec, inv, grid_cache):
    n, beat, bar, kick, duck, _ = grid_cache
    gate = bass_gate(n, beat)
    sub = sub_layer(n, gate, duck, decay_808=spec.get("decay_808"), beat=beat)
    if spec["pack"]:
        entry = pick_bass(inv, spec["pack"])
        body = sampled_body(entry, n, beat, gate)
        src_name = os.path.basename(entry["path"])
    else:
        body = synthetic_body(n, beat, gate)
        src_name = "synthetic square+saw"
    body = drive(body, spec["drive_db"])
    body = widen(body, spec["haas"], spec["side"])
    body = body * (1.0 - 0.35 * duck)[:, None]

    sub_st = np.stack([sub, sub], axis=1) * spec["sub"]
    br = rms(body)
    if br > 1e-9:
        body = body * (rms(sub_st) / br) * spec["body"]
    kick_st = np.stack([kick, kick], axis=1)
    # (e) glue: kick and sub share one saturator so they stop fighting
    kg, sg = bass_glue(kick_st, sub_st, 1.8)
    bass = sg + body
    # the bass is meant to be at least as loud as the kick, not tucked under it
    bass = bass * (1.15 * rms(kg) / max(rms(bass), 1e-9))
    mix = dsp.mono_below(kg + bass, 120.0)
    return mix, src_name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--copy-to", default=None)
    a = ap.parse_args()
    if os.path.isdir(a.out):
        shutil.rmtree(a.out)
    os.makedirs(a.out, exist_ok=True)

    inv = smp.load_inventory(os.path.join(SAMPLE_ROOT, "inventory.json"))
    grid_cache = build_grid()
    from measure import _ffmpeg_bin
    ff = _ffmpeg_bin()
    clips, rows = [], []
    for i, (label, source, spec) in enumerate(CANDIDATES, 1):
        mix, src_name = render_candidate(spec, inv, grid_cache)
        out, info = master_chain(mix, SR, target_lufs=-14.0, ceiling_dbtp=-1.0)
        base = f"{i:02d} - {label} ({source})"
        wav = os.path.join(a.out, base + ".wav")
        sf.write(wav, out, SR, subtype="PCM_24")
        m4a = base + ".m4a"
        if ff:
            subprocess.run([ff, "-y", "-loglevel", "error", "-i", wav,
                            "-c:a", "aac", "-b:a", "192k", os.path.join(a.out, m4a)],
                           check=False)
        clips.append({"file": m4a if ff else base + ".wav", "n": f"{i:02d}",
                      "label": label, "source": f"{source} - {src_name}"})
        rows.append((base, source, src_name, spec, info))
        print("wrote", base)

    manifest = {
        "round": "Round 4 · bass only",
        "date": "2 Sep 2026",
        "intro": ("Bass and kick only - no hats, no clap, no chords, no hook. Every "
                  "candidate is a layer stack: a mono sine sub at 55 Hz ducked under "
                  "the kick, a separate 78-205 Hz body layer from a real Legowelt "
                  "synth sample (or a synthetic square in 07), saturation and width "
                  "on the body only, and the kick and sub glued through one "
                  "saturator. The sub is mono below 120 Hz in every clip."),
        "questions": ["Which bass is deepest and widest?",
                      "Which one sounds like a real club bass, not a computer?",
                      "What is still missing?"],
        "groups": [{"name": "Bass over kick only",
                    "hint": ("Same kick, same pattern, same key and tempo in all eight - "
                             "the only thing changing is how the bass is built."),
                    "clips": clips}],
    }
    with open(os.path.join(a.out, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    if a.copy_to:
        if os.path.isdir(a.copy_to):
            shutil.rmtree(a.copy_to)
        shutil.copytree(a.out, a.copy_to)
    for base, source, src_name, spec, info in rows:
        print(f"| {base} | {source} | {src_name} | drive {spec['drive_db']} dB, "
              f"haas {spec['haas']} ms, side {spec['side']}, sub {spec['sub']}, "
              f"body {spec['body']} | {info['integrated_lufs']} LUFS, TP {info['true_peak_dbfs']} |")


if __name__ == "__main__":
    main()
