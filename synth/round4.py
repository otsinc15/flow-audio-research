#!/usr/bin/env python3
"""Round 4: five 60-second clips whose instruments are recordings of real synths.

Bass, hook and chord come from Legowelt's free sample packs (Prophet 600,
Jupiter 8, Oberheim Matrix 1000) played through the sampler voice in sampler.py;
the grid, the pattern-book rules, the fixed one-bar hook and the chord-as-a-short-
dry-accent all stay exactly as they were in round 2.

    python round4.py --out <dir>
"""

import argparse
import json
import os
import shutil

import numpy as np

from render import render_and_write

ROOT = os.path.expanduser("~/flow-synth/samples")

# Samples are chosen by MEASURED content, not by filename order, and every
# pitch range is set so the sampler never has to shift more than +/-7 semitones
# from the sample's own root: bass plays A1 (midi 33), hook and chord play the
# triad two octaves up (midi 57/60/64).
P600_BASS = dict(root=ROOT, pack="prophet600", contains="Bass ", min_midi=27, max_midi=40,
                 sort_by="sub")
MTX_BASS = dict(root=ROOT, pack="matrix1000", contains="Bass", min_midi=27, max_midi=40,
                sort_by="low")
JUP_HOOK = dict(root=ROOT, pack="jupiter8", contains="Synth", exclude=["FX "],
                min_midi=51, max_midi=64, max_seconds=4.0, sort_by="body")
P600_PAD = dict(root=ROOT, pack="prophet600", contains="Pad ", min_midi=38, max_midi=52,
                sort_by="body", transpose=-12)
P600_CHORD = dict(root=ROOT, pack="prophet600", contains="Synth ", exclude=["FX "],
                  min_midi=38, max_midi=52, max_seconds=6.0, sort_by="body",
                  transpose=-12)
MTX_CHORD = dict(root=ROOT, pack="matrix1000", min_midi=38, max_midi=52, sort_by="body",
                 transpose=-12)
DRUM_KICK = dict(root=ROOT, pack="drumnibus", contains="Bassdrums", max_seconds=2.6,
                 sort_by="sub")

CLIPS = [
    ("01", "palette A, Prophet 600 bass + Jupiter 8 hook",
     "Prophet 600, Jupiter 8, Matrix 1000",
     dict(palette="a", seed=11, bpm=114.8, variant="v1",
          samples=dict(bass=P600_BASS, hook=JUP_HOOK, chord=P600_CHORD))),
    ("02", "palette A, Matrix 1000 bass + Prophet pad accent",
     "Matrix 1000, Prophet 600, Jupiter 8",
     dict(palette="a", seed=11, bpm=114.8, variant="v1",
          samples=dict(bass=MTX_BASS, hook=JUP_HOOK, chord=P600_PAD))),
    ("03", "palette A, no hook, sampled everything",
     "Prophet 600, Matrix 1000",
     dict(palette="a", seed=11, bpm=114.8, variant=None,
          samples=dict(bass=P600_BASS, chord=MTX_CHORD))),
    ("04", "palette B deep bass, Prophet and Matrix",
     "Prophet 600, Matrix 1000, Jupiter 8",
     dict(palette="b", seed=41, bpm=114.8, variant=None,
          samples=dict(bass=P600_BASS, hook=JUP_HOOK, chord=MTX_CHORD))),
    ("05", "alternate kick: Drumnibus 808 instead of the Faust 909",
     "Prophet 600, Jupiter 8, Matrix 1000, Drumnibus",
     dict(palette="a", seed=11, bpm=114.8, variant="v1",
          samples=dict(bass=P600_BASS, hook=JUP_HOOK, chord=MTX_CHORD, kick=DRUM_KICK))),
]

READ_ME = """ROUND 4 - real synthesizers, sampled
====================================

Same sequencer, same tempo, same key as last time. What changed is that the bass,
the hook and the chord are no longer patches I built by setting numbers - they are
recordings of actual hardware: a Sequential Prophet 600, a Roland Jupiter 8 and an
Oberheim Matrix 1000, from Legowelt's free sample packs, played from our sequencer
and pitched into our key.

The chord is deliberately a SHORT DRY ACCENT, not a pad wash - third time asking,
so it is now an eighth-note long with no reverb and the level held right down.

Listen in order, 01 to 05, and answer three questions:

  1. Do these sound like real synthesizers now - crisp and warm?
  2. Which number is closest to Endel Deeper Focus?
  3. What still sounds wrong?

05 is the same arrangement as 01 with one change: the kick is a sampled 808 from
the Drumnibus pack instead of the synthesised 909. That is an A/B on the kick only.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--copy-to", default=None)
    a = ap.parse_args()
    if os.path.isdir(a.out):
        shutil.rmtree(a.out)
    os.makedirs(a.out, exist_ok=True)
    rows = []
    for num, label, packs, kw in CLIPS:
        name = f"{num} - {label} ({packs})"
        _, meta = render_and_write(kw["palette"], kw["seed"], kw["bpm"], a.out,
                                   name=name, variant=kw.get("variant"),
                                   engine="surge", samples=kw["samples"])
        used = meta.get("samples") or {}
        rows.append(dict(file=name + ".wav", packs=packs,
                         bass=os.path.basename(used.get("bass", "-")),
                         hook=os.path.basename(used.get("hook", "-")),
                         chord=os.path.basename(used.get("chord", "-")),
                         kick=("Drumnibus BD_808A1200" if "kick" in kw["samples"]
                               else "Faust sy.kick 909"),
                         bands=meta["bands_post_master_pct"],
                         lufs=meta["mastered"]["integrated_lufs"],
                         tp=meta["mastered"]["true_peak_dbfs"]))
        print("wrote", name)
    with open(os.path.join(a.out, "00 - READ ME.txt"), "w") as f:
        f.write(READ_ME)
    # drop the -unmastered and stems out of the listening folder: only the five clips
    for fn in os.listdir(a.out):
        if fn.endswith("-unmastered-16lufs.wav"):
            os.remove(os.path.join(a.out, fn))
    st = os.path.join(a.out, "stems")
    if os.path.isdir(st):
        shutil.rmtree(st)
    if a.copy_to:
        os.makedirs(a.copy_to, exist_ok=True)
        for fn in os.listdir(a.out):
            shutil.copy2(os.path.join(a.out, fn), os.path.join(a.copy_to, fn))
    print(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
