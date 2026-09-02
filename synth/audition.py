#!/usr/bin/env python3
"""Sound audition: one element at a time over the same kick+hat grid.

Round 3 exists because the sequencer passed and the sound source failed. Every
voice so far was a patch built from parameters by an agent that cannot hear,
and Daniel's verdict was "very generic, very computer-like". The fix is to stop
inventing patches and start loading ones that human sound designers made.

Only ONE plugin survived the preset test (see load_obxd_preset below and the
write-up): OB-Xd, whose .fxp files are XML lists of indexed parameter values
that can be applied straight to the plugin. Surge XT's factory patches, Dexed's
cartridges and TAL-NoiseMaker did not survive; the reasons are in the doc.

    python audition.py --out <dir>
"""

import argparse
import os
import re
import shutil
import xml.etree.ElementTree as ET

import numpy as np
import soundfile as sf

import dsp
from dsp import SR
import surge_engine as se
from master import master_chain

VENDOR = os.environ.get("FLOW_VENDOR", os.path.expanduser("~/flow-synth/vendor"))
OBXD_VST3 = os.path.join(VENDOR, "obxd", "OB-Xd.vst3")
OBXD_PRESETS = os.path.join(VENDOR, "obxd", "content", "Presets")

BPM = 114.8
ROOT_HZ = 55.0                       # A1, the palette key
ROOT_MIDI = 33


# --------------------------------------------------------------- preset load

def _fxp_xml(path):
    raw = open(path, "rb").read()
    i = raw.find(b"<?xml")
    if i < 0:
        raise ValueError(f"no XML chunk in {path}")
    return raw[i:].split(b"\x00")[0].decode("utf-8", "replace")


def load_obxd_preset(plug, path):
    """Apply an OB-Xd .fxp to a loaded plugin.

    OB-Xd writes its patches as `<discoDSP Val_0=".." Val_1=".." .../>` inside
    the FXP chunk - normalised values in plugin parameter order - so the preset
    can be applied by index. This is a real preset load, not an approximation:
    80 of the plugin's 82 parameters come straight from the file.
    """
    names = list(plug.parameters.keys())
    xml = re.sub(r"^\s*<\?xml[^>]*\?>", "", _fxp_xml(path)).strip()
    root = ET.fromstring(xml)
    node = root if root.attrib else (list(root)[0] if len(root) else root)
    applied = 0
    for key, val in node.attrib.items():
        m = re.match(r"Val_(\d+)$", key)
        if not m:
            continue
        i = int(m.group(1))
        if i < len(names):
            try:
                plug.parameters[names[i]].raw_value = float(val)
                applied += 1
            except Exception:
                pass
    if applied < 40:
        raise RuntimeError(f"only {applied} parameters applied from {path}")
    return applied


def obxd(preset_relpath):
    import pedalboard
    p = pedalboard.load_plugin(OBXD_VST3)
    n = load_obxd_preset(p, os.path.join(OBXD_PRESETS, preset_relpath))
    se._AUDIT.append((preset_relpath, "params_applied", n))
    return p


# ------------------------------------------------------------------ the grid

def grid(bars, kick_long=False):
    """Kick, off-beat hat and one clap per bar - identical under every candidate."""
    beat = 60.0 / BPM
    bar = 4 * beat
    n = int(round(bars * bar * SR))
    rng = np.random.default_rng(11)
    kicks = se.faust_kicks(rng, n_variants=8) if not kick_long else faust_kicks_long(rng)
    kbuf = np.zeros(n, dtype=np.float32)
    times = []
    for b in range(bars * 4):
        t0 = b * beat
        times.append(t0)
        dsp.add_at(kbuf, t0 * SR, kicks[b % len(kicks)], 1.0 + 0.05 * np.sin(b * 2.399963))
    kbuf = dsp.peaking(kbuf, ROOT_HZ, 1.4, -4.5)
    hat = se._hat(rng)
    clap = se.make_clap(np.random.default_rng(11 + se.CLAP_SEED_OFFSET))
    pbuf = np.zeros(n, dtype=np.float32)
    sw = dsp.swing_offset_s(BPM, 52.0)
    for b in range(bars * 4):
        dsp.add_at(pbuf, (b * beat + 0.5 * beat + sw) * SR, hat, 0.18)
    for b in range(bars):
        dsp.add_at(pbuf, (b * bar + 1.0 * beat) * SR, clap, 0.42)
    duck = np.zeros(n, dtype=np.float32)
    dc = dsp.exp_decay(int(0.45 * SR), 0.080)
    for t0 in times:
        dsp.add_at(duck, t0 * SR, dc)
    return n, beat, bar, kbuf, pbuf, (1.0 - 0.55 * np.clip(duck, 0, 1)).astype(np.float32)


def faust_kicks_long(rng):
    """Candidate 2: longer body, harder drive - the 'fatter 909' the notes ask for."""
    import dawdreamer as daw
    out = []
    for i in range(8):
        pitch = 51.0 * float(np.exp(rng.normal(0, 0.012)))
        decay = 0.72 * float(np.exp(rng.normal(0, 0.06)))
        drive = 8.5 * float(np.exp(rng.normal(0, 0.05)))
        eng = daw.RenderEngine(SR, 512)
        f = eng.make_faust_processor(f"kl{i}")
        f.set_dsp_string(se.KICK_DSP.format(gatelen=240, pitch=round(pitch, 4),
                                            click=0.18, attack=0.004,
                                            decay=round(decay, 4), drive=round(drive, 4)))
        assert f.compile()
        eng.load_graph([(f, [])])
        eng.render(1.1)
        a = np.asarray(eng.get_audio(), dtype=np.float32)
        out.append(a[0] if a.ndim == 2 else a)
    return out


def stereo(mono):
    return np.stack([mono, mono], axis=1)


def at_ratio(element, base, ratio):
    """Scale a candidate so it sits at a fixed level relative to the drum grid.

    Presets differ in output level by a lot, and the first pass proved the point
    the hard way: three candidates measured identically to the bare grid because
    the element under test was inaudible beneath the kick. An audition is only
    fair if every candidate is equally present, so each one is matched by RMS
    rather than played at whatever level its preset happens to output.
    """
    er = float(np.sqrt(np.mean(np.asarray(element, dtype=np.float64) ** 2)))
    br = float(np.sqrt(np.mean(np.asarray(base, dtype=np.float64) ** 2)))
    if er < 1e-9:
        raise RuntimeError("candidate rendered silent")
    return element * (ratio * br / er)


def finish(path, mix):
    mix = dsp.mono_below(mix, 120.0)
    out, info = master_chain(mix, SR, target_lufs=-14.0, ceiling_dbtp=-1.0)
    sf.write(path, out, SR, subtype="PCM_24")
    return info


# ------------------------------------------------------------------ elements

def bass_take(plug, n, bar, beat, bars, duck):
    notes = [(0.0, n / SR, ROOT_MIDI, 100)]
    a = se.render_notes(plug, notes, n / SR)[:n]
    return a * duck[:, None]


def hook_take(plug, n, bar, beat, bars):
    phrase = [(0.00, 0), (1.50, 7), (2.50, 3)]
    notes = []
    for b in range(bars):
        for off, semi in phrase:
            t0 = b * bar + off * beat
            notes.append((t0, t0 + 0.28, ROOT_MIDI + 24 + semi, 100))
    dry = se.render_notes(plug, notes, n / SR)[:n]
    echo = se.surge_dub_delay(dry, beat * 0.75, 20.0, 5000.0, 5.0,
                              max(0.01, 1.0 / (bar * 4)), crossfeed=55.0, low_cut=200.0)
    tap2 = se.surge_dub_delay(dry, 0.264, 85.0, 5000.0, 8.0,
                              max(0.01, 2.0 / (bar * 4)), crossfeed=20.0,
                              low_cut=200.0, right_ratio=1.0)
    return dry * 0.9 + (echo + 0.55 * tap2)[:n]


def chord_take(plug, n, bar, beat, bars):
    """Short DRY stab: an eighth-note long, <=30 % send, no reverb, capped 2.5 kHz."""
    triad = [ROOT_MIDI + 24, ROOT_MIDI + 27, ROOT_MIDI + 31]
    notes = []
    for b in range(bars):
        for off in (1.5, 3.5):
            t0 = b * bar + off * beat
            notes += [(t0, t0 + 0.5 * beat, t, 96) for t in triad]
    dry = se.render_notes(plug, notes, n / SR)[:n]
    dry = np.stack([dsp.lowpass(dry[:, i], 2500.0, 0.707) for i in (0, 1)], axis=1)
    echo = se.surge_dub_delay(dry * 0.30, beat * 0.75, 20.0, 5000.0, 5.0,
                              max(0.01, 1.0 / (bar * 4)), crossfeed=55.0, low_cut=200.0)
    return dry + echo[:n]


# ---------------------------------------------------------------- candidates

BASS = [
    ("deep round Moog-style", "OB-Xd", "Bass/Bass Moog.fxp"),
    ("warm round analogue", "OB-Xd", "Bass/Bass Round Bass.fxp"),
    ("bright analogue saw", "OB-Xd", "Bass/Analog Saw 01.fxp"),
    ("current parameter-built sub", "Surge XT", None),
]
HOOK = [
    ("glassy bell", "OB-Xd", "Plucked/80s Bells.fxp"),
    ("wide analogue lead", "OB-Xd", "Lead Synth/Big Lead OB-Xd.fxp"),
    ("current parameter-built pluck", "Surge XT", None),
]
CHORD = [
    ("hollow band-passed stab", "OB-Xd", "Synth Poly/Bandpass OB.fxp"),
    ("warm brassy stab", "OB-Xd", "Synth Poly/Analog Brass (Chrds).fxp"),
    ("current parameter-built stab", "Surge XT", None),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--copy-to", default=None)
    a = ap.parse_args()
    out = a.out
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out, exist_ok=True)

    n4, beat, bar, k4, p4, duck4 = grid(4)
    n8, _, _, k8, p8, duck8 = grid(8)
    base4 = stereo(k4) * 0.9 + stereo(p4) * 0.8
    base8 = stereo(k8) * 0.9 + stereo(p8) * 0.8
    rows = []
    idx = 1

    def write(role, i, desc, plugin, preset, mix):
        nonlocal idx
        pname = os.path.basename(preset)[:-4] if preset else "built from parameters"
        fn = f"{idx:02d} - {role} {i} - {desc} ({plugin}, {pname}).wav"
        finish(os.path.join(out, fn), mix)
        rows.append((fn, plugin, pname, desc))
        print("wrote", fn)
        idx += 1

    for i, (desc, plugin, preset) in enumerate(BASS, 1):
        if preset:
            v = bass_take(obxd(preset), n4, bar, beat, 4, duck4)
        else:
            b = se.patch_bass(cutoff=430.0)
            v = bass_take(b, n4, bar, beat, 4, duck4)
        write("bass", i, desc, plugin, preset, base4 + at_ratio(v, base4, 0.95))

    for i, (desc, plugin, preset) in enumerate(HOOK, 1):
        plug = obxd(preset) if preset else se.patch_motif()
        write("hook", i, desc, plugin, preset,
              base4 + at_ratio(hook_take(plug, n4, bar, beat, 4), base4, 0.60))

    for i, (desc, plugin, preset) in enumerate(CHORD, 1):
        plug = obxd(preset) if preset else se.patch_stab_hp()
        write("chord", i, desc, plugin, preset,
              base8 + at_ratio(chord_take(plug, n8, bar, beat, 8), base8, 0.55))

    for i, (desc, longk) in enumerate([("current 909", False),
                                       ("longer body, harder drive", True)], 1):
        nn, _, _, kk, pp, _ = grid(4, kick_long=longk)
        write("kick", i, desc, "Faust sy.kick", None,
              stereo(kk) * 0.9 + stereo(pp) * 0.8)

    # ---- 99: the agent's best guess, chord reduced to a short dry accent ----
    nA, _, _, kA, pA, duckA = grid(8)
    baseA = stereo(kA) * 0.9 + stereo(pA) * 0.8
    mix = (baseA
           + at_ratio(bass_take(obxd(BASS[0][2]), nA, bar, beat, 8, duckA), baseA, 0.95)
           + at_ratio(hook_take(obxd(HOOK[0][2]), nA, bar, beat, 8), baseA, 0.60)
           # chord kept deliberately low and dry - this is the wash coming down
           + at_ratio(chord_take(obxd(CHORD[0][2]), nA, bar, beat, 8), baseA, 0.40))
    fn = "99 - full mix preview (agent's best guess).wav"
    finish(os.path.join(out, fn), mix)
    rows.append((fn, "mixed", "-", "best picks, chord at 0.4 as a short dry accent"))
    print("wrote", fn)

    with open(os.path.join(out, "00 - READ ME.txt"), "w") as f:
        f.write(READ_ME)
    if a.copy_to:
        os.makedirs(a.copy_to, exist_ok=True)
        for fn in os.listdir(out):
            shutil.copy2(os.path.join(out, fn), os.path.join(a.copy_to, fn))
    print("\n".join(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |" for r in rows))


READ_ME = """SOUND AUDITION - round 3
========================

This is about the SOUNDS, not the arrangement. Every clip uses the same kick and
hat grid at 114.8 BPM in the same key, and changes exactly one element, so what
you are comparing is the instrument.

HOW TO LISTEN
  1. Play them in order, 01 to 12. They are short (4 bars; the chords are 8).
  2. Note ONE number you like per role: bass, hook, chord, kick.
  3. Tell me which one is closest to "a real synthesizer", and which ones still
     sound computer-like.
  4. 99 is a full mix of my own best guesses, with the chord pulled down to a
     short dry accent - that is there so you can hear how far the pad wash has
     come down, not as a candidate.

WHAT CHANGED SINCE LAST TIME
  Every sound you have heard so far was a patch I built by setting numbers,
  without ears. This round loads presets that human sound designers made. Of the
  four sound sources approved, only OB-Xd's presets could actually be loaded by
  the renderer - the reasons the other three could not are in the write-up. So
  the "OB-Xd" clips are real designed patches, and the "built from parameters"
  clips are the old approach, included so you can hear the difference directly.
"""


if __name__ == "__main__":
    main()
