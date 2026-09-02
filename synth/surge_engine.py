#!/usr/bin/env python3
"""Arm 2's voices rebuilt on the licence-clean stack: Surge XT + Faust.

Same sequencer, same grid, tempo, key, seeds and five-stem layout as the numpy
engine in render.py. What changes is where the sound comes from:

    sub + bass layers   Surge XT, one patch, three oscillators (sine at the root,
                        sine an octave up, sine a fifth above that)
    motif               Surge XT, detuned saw + sine through a resonant low-pass
    pad / chord bed     Surge XT, three unison saws, low-passed
    chord stabs         Surge XT, same voicing with a plucked envelope
    kick                Faust `sy.kick` compiled by DawDreamer - no plugin at all -
                        with per-hit drift, so no two kicks are identical
    dub delay           Surge XT Effects, fx_type "Delay": tempo-synced times,
                        damped feedback, crossfeed for ping-pong, and its own
                        modulation for tape wow
    reverb, saturation  pedalboard's Reverb and Distortion (see NOTE below)

Licence position (research/production-options/synth-instruments-2026-09-02.md §1):
Surge XT, pedalboard and DawDreamer are all GPLv3, which is fine here because
only rendered audio ever leaves this machine. The Faust standard library carries
an explicit exception permitting the compiled output under any licence, so the
kick is the one voice that could also ship inside an app later.

NOTE, found by running it: pedalboard caches Surge XT Effects' parameter names
from whichever fx_type was set when the plugin was loaded. After switching
fx_type the *names* stay those of the first effect while the *meanings* change.
So each effect gets its own freshly loaded instance, and reverb and saturation
use pedalboard's own well-named effects rather than guessing at aliased slots.
Every patch here is checked at audio level, never by reading a parameter back -
the disabled-module trap in §0 of that document.
"""

import os

import numpy as np

import dsp
from dsp import SR

SURGE_DIR = os.environ.get(
    "FLOW_SURGE_DIR", os.path.expanduser("~/flow-synth/vendor/surge-xt-1.3.4"))
INST_PATH = os.path.join(SURGE_DIR, "Surge XT.vst3")
FX_PATH = os.path.join(SURGE_DIR, "Surge XT Effects.vst3")

_AUDIT = []


def audit():
    return list(_AUDIT)


# ------------------------------------------------------------------ helpers

def hz_to_midi(f):
    return int(round(69 + 12 * np.log2(f / 440.0)))


def _parse_unit(text):
    """'250.0 ms' -> 0.25, '1.01 s' -> 1.01, '8.00 cents' -> 8.0, '-inf' -> -inf."""
    t = str(text).strip()
    for unit, mul in (("ms", 1e-3), ("cents", 1.0), ("semitones", 1.0),
                      ("Hz", 1.0), ("dB", 1.0), ("%", 1.0), ("s", 1.0)):
        if t.endswith(unit):
            try:
                return float(t[: -len(unit)].strip()) * mul
            except ValueError:
                return None
    try:
        return float(t)
    except ValueError:
        return None


def set_near(plug, name, value):
    """Set a Surge parameter to the nearest value it will actually accept.

    Surge exposes most continuous parameters through pedalboard as a quantised
    list of formatted strings ('996.5 ms', '1.01 s', ...), and assigning a value
    that is not literally in that list raises. Times are in SECONDS here, pitch
    in semitones, detune in cents, everything else in its own displayed unit.
    """
    pr = plug.parameters[name]
    opts = getattr(pr, "valid_values", None)
    if not opts:
        setattr(plug, name, value)
        return
    opts = list(opts)
    if all(isinstance(o, (int, float)) for o in opts):
        setattr(plug, name, min(opts, key=lambda o: abs(o - value)))
        return
    parsed = [(_parse_unit(o), o) for o in opts]
    parsed = [(v, o) for v, o in parsed if v is not None]
    if not parsed:
        setattr(plug, name, value)
        return
    setattr(plug, name, min(parsed, key=lambda t: abs(t[0] - value))[1])


def _load(path, **params):
    import pedalboard
    return pedalboard.load_plugin(path, parameter_values=params) if params \
        else pedalboard.load_plugin(path)


def render_notes(plug, notes, duration, sr=SR):
    """notes: list of (t_on, t_off, midi_note, velocity). Returns (N, 2) float32."""
    import mido
    msgs = []
    for on, off, note, vel in notes:
        msgs.append(mido.Message("note_on", note=int(note), velocity=int(vel), time=float(on)))
        msgs.append(mido.Message("note_off", note=int(note), time=float(off)))
    msgs.sort(key=lambda m: m.time)
    out = plug(msgs, duration=duration, sample_rate=sr, num_channels=2)
    return np.ascontiguousarray(np.asarray(out, dtype=np.float32).T)


def assert_audible(name, audio, min_rms=2e-5):
    """A patch is proven by its audio, never by reading a parameter back."""
    rms = float(np.sqrt(np.mean(np.asarray(audio, dtype=np.float64) ** 2)))
    _AUDIT.append((name, "audible", round(rms, 8)))
    if not np.isfinite(rms) or rms < min_rms:
        raise RuntimeError(f"Surge patch '{name}' is silent (rms={rms:.3e}). "
                           "A parameter probably belongs to a disabled module.")
    return rms


def assert_param_matters(name, plug, notes, duration, param, val_a, val_b):
    """Prove a parameter is live by rendering twice and comparing the audio."""
    set_near(plug, param, val_a)
    a = render_notes(plug, notes, duration)
    set_near(plug, param, val_b)
    b = render_notes(plug, notes, duration)
    diff = float(np.max(np.abs(a - b)))
    _AUDIT.append((name, f"param:{param}", round(diff, 8)))
    if diff < 1e-6:
        raise RuntimeError(f"'{param}' on '{name}' changed nothing in the audio "
                           f"(max diff {diff:.2e}) - inert parameter.")
    return diff


# ------------------------------------------------------------------- patches

def patch_bass(cutoff=430.0, oct_db=-7.0, fifth_db=-13.0):
    """Sub plus two bass layers in one patch: root, +12, +19 semitones.

    The octave-up and fifth-above-octave sines are the 110 Hz and 165 Hz layers
    the numpy engine added by hand - here they are oscillators 2 and 3.
    """
    p = _load(INST_PATH)
    p.a_osc_1_type = "Sine"
    p.a_osc_2_type = "Sine"
    p.a_osc_3_type = "Sine"
    set_near(p, "a_osc_2_octave", 1.0)
    set_near(p, "a_osc_3_octave", 1.0)
    set_near(p, "a_osc_3_pitch", 7.0)
    set_near(p, "a_osc_1_volume", 0.0)
    set_near(p, "a_osc_2_volume", oct_db)
    set_near(p, "a_osc_3_volume", fifth_db)
    p.a_filter_1_type = "LP 24 dB"
    set_near(p, "a_filter_1_cutoff", float(cutoff))
    set_near(p, "a_filter_1_resonance", 4.0)
    set_near(p, "a_amp_eg_attack", 0.004)
    set_near(p, "a_amp_eg_decay", 1.0)
    set_near(p, "a_amp_eg_sustain", 100.0)
    set_near(p, "a_amp_eg_release", 0.08)
    return p


def patch_motif(cutoff=760.0, resonance=18.0):
    p = _load(INST_PATH)
    p.a_osc_1_type = "Classic"
    p.a_osc_1_unison_voices = "3 voices"
    set_near(p, "a_osc_1_unison_detune", 8.0)
    p.a_osc_2_type = "Sine"
    set_near(p, "a_osc_2_volume", -6.0)
    set_near(p, "a_osc_3_volume", -96.0)
    p.a_filter_1_type = "LP 24 dB"
    set_near(p, "a_filter_1_cutoff", float(cutoff))
    set_near(p, "a_filter_1_resonance", float(resonance))
    set_near(p, "a_amp_eg_attack", 0.004)
    set_near(p, "a_amp_eg_decay", 0.20)
    set_near(p, "a_amp_eg_sustain", 0.0)
    set_near(p, "a_amp_eg_release", 0.09)
    return p


def patch_pad(cutoff=430.0, sustain=100.0, decay=1.2, release=0.4, detune=12.0):
    p = _load(INST_PATH)
    for i in (1, 2, 3):
        setattr(p, f"a_osc_{i}_type", "Classic")
        setattr(p, f"a_osc_{i}_unison_voices", "3 voices")
        set_near(p, f"a_osc_{i}_unison_detune", detune)
    set_near(p, "a_osc_2_pitch", 0.07)
    set_near(p, "a_osc_3_pitch", -0.09)
    set_near(p, "a_osc_2_volume", -4.0)
    set_near(p, "a_osc_3_volume", -6.0)
    p.a_filter_1_type = "LP 24 dB"
    set_near(p, "a_filter_1_cutoff", float(cutoff))
    set_near(p, "a_filter_1_resonance", 8.0)
    set_near(p, "a_amp_eg_attack", 0.04)
    set_near(p, "a_amp_eg_decay", decay)
    set_near(p, "a_amp_eg_sustain", float(sustain))
    set_near(p, "a_amp_eg_release", release)
    return p


def patch_stab():
    return patch_pad(cutoff=560.0, sustain=0.0, decay=0.26, release=0.12, detune=7.0)


# ------------------------------------------------------------- Faust kick

KICK_DSP = """import("stdfaust.lib");
gate = ba.time < {gatelen};
process = sy.kick({pitch}, {click}, {attack}, {decay}, {drive}, gate) <: _,_;
"""


def faust_kicks(rng, n_variants=12, seconds=0.9):
    """Compile a ladder of drifted 909-style kicks - no plugin involved.

    Section 5.2 of the instrument study: a sample is one machine on one day,
    while a parameterised voice can jitter pitch, decay and drive per hit. Twelve
    variants is more round-robin than a sampled kit usually ships with.
    """
    import dawdreamer as daw
    out = []
    for i in range(n_variants):
        pitch = 53.0 * float(np.exp(rng.normal(0, 0.012)))
        decay = 0.42 * float(np.exp(rng.normal(0, 0.06)))
        drive = 5.6 * float(np.exp(rng.normal(0, 0.05)))
        click = 0.22 * float(np.exp(rng.normal(0, 0.10)))
        eng = daw.RenderEngine(SR, 512)
        f = eng.make_faust_processor(f"k{i}")
        f.set_dsp_string(KICK_DSP.format(gatelen=180, pitch=round(pitch, 4),
                                         click=round(click, 4), attack=0.004,
                                         decay=round(decay, 4), drive=round(drive, 4)))
        if not f.compile():
            raise RuntimeError("Faust kick failed to compile")
        eng.load_graph([(f, [])])
        eng.render(seconds)
        a = np.asarray(eng.get_audio(), dtype=np.float32)
        a = a[0] if a.ndim == 2 else a
        assert_audible(f"faust_kick_{i}", a)
        out.append(a)
    return out


# ------------------------------------------------------------------ effects

def surge_dub_delay(x_stereo, delay_s, feedback_pct, high_cut, wow_cents,
                    wow_hz, crossfeed=55.0):
    """Surge XT Effects, fx_type 'Delay' - the dub delay, as a real effect.

    A fresh instance is loaded with fx_type already set, because the parameter
    names pedalboard exposes are fixed at load time.
    """
    fx = _load(FX_PATH)
    fx.fx_type = "Delay"
    set_near(fx, "delay_time_left", float(delay_s))
    set_near(fx, "delay_time_right", float(delay_s) * 1.5)
    set_near(fx, "feedback_eq_feedback", float(feedback_pct))
    set_near(fx, "feedback_eq_crossfeed", float(crossfeed))
    set_near(fx, "feedback_eq_low_cut", 120.0)
    set_near(fx, "feedback_eq_high_cut", float(high_cut))
    set_near(fx, "modulation_rate", float(wow_hz))
    set_near(fx, "modulation_depth", float(wow_cents))
    set_near(fx, "output_mix", 100.0)          # send/return: wet only
    y = fx(np.ascontiguousarray(x_stereo.T), sample_rate=SR)
    return np.ascontiguousarray(np.asarray(y, dtype=np.float32).T)


def pb_reverb(x_stereo, room_size=0.62, damping=0.72, width=0.85):
    import pedalboard
    b = pedalboard.Pedalboard([
        pedalboard.Reverb(room_size=room_size, damping=damping, width=width,
                          wet_level=1.0, dry_level=0.0),
        pedalboard.HighpassFilter(cutoff_frequency_hz=140.0),
    ])
    y = b(np.ascontiguousarray(x_stereo.T), SR)
    return np.ascontiguousarray(np.asarray(y, dtype=np.float32).T)


def pb_saturate(x_stereo, drive_db):
    """Odd-harmonic drive on the bass bus (instrument study §5.1)."""
    import pedalboard
    b = pedalboard.Pedalboard([pedalboard.Distortion(drive_db=float(drive_db)),
                               pedalboard.LowpassFilter(cutoff_frequency_hz=3200.0)])
    y = b(np.ascontiguousarray(x_stereo.T), SR)
    return np.ascontiguousarray(np.asarray(y, dtype=np.float32).T)


# ------------------------------------------------------------------ arranger

def render_surge_clip(palette, seed, bpm, seconds=60.0, variant=None):
    """Same schedule as render.render_clip, different sound sources.

    Returns (buses, meta) with the identical bus names, so the balance solver,
    stem export and master chain in render.py all work unchanged.
    """
    from render import variant_params

    rng = np.random.default_rng(seed)
    palette = palette.lower()
    V = variant_params(palette, variant)
    V["motif_fixed"] = True          # the Surge arm always uses the fixed phrase

    beat = 60.0 / bpm
    bar = 4 * beat
    bars = max(1, int(round(seconds / bar)))
    n = int(round(bars * bar * SR))
    n2 = 2 * n
    dur2 = n2 / SR

    # identical first two draws as the numpy engine, so the same seed gives the
    # same key and the same modulator phases
    root = float(rng.choice([51.91, 55.00, 58.27]))
    phases = rng.uniform(0, 2 * np.pi, 16)
    base = hz_to_midi(root)
    m3, p5 = 3, 7

    # ---- kick: Faust, per-hit drift -----------------------------------------
    variants = faust_kicks(rng)
    kick_buf = np.zeros(n2, dtype=np.float32)
    kick_times = []
    for b in range(bars * 8):                     # two cycles
        t0 = b * beat
        if t0 * SR >= n2:
            break
        kick_times.append(t0)
        bb = b % (bars * 4)                        # index within ONE cycle
        k = variants[bb % len(variants)]
        vel = 1.0 + 0.05 * np.sin(bb * 2.399963)   # deterministic velocity drift
        dsp.add_at(kick_buf, t0 * SR, k, float(vel))

    # ---- sidechain duck ------------------------------------------------------
    duck = np.zeros(n2, dtype=np.float32)
    dcurve = dsp.exp_decay(int(0.45 * SR), 0.080)
    for t0 in kick_times:
        dsp.add_at(duck, t0 * SR, dcurve)
    duck_env = (1.0 - 0.72 * np.clip(duck, 0, 1)).astype(np.float32)

    # ---- bass: Surge, three oscillators --------------------------------------
    bass = patch_bass(cutoff=430.0 + 60.0 * (V["sub_drive"] - 2.6),
                      oct_db=-7.0 if V["bass_oct"] == 0 else -4.0,
                      fifth_db=-13.0 if V["bass_body"] == 0 else -9.0)
    sub_notes = []
    if palette == "b":
        for b in range(bars * 2):
            t0, t3 = b * bar, b * bar + 3 * beat
            sub_notes.append((t0, t3, base, 100))
            sub_notes.append((t3, (b + 1) * bar, base + m3, 100))
    else:
        sub_notes.append((0.0, dur2, base, 100))
    probe = [(0.0, 1.0, base, 100)]
    assert_param_matters("bass", bass, probe, 1.5, "a_filter_1_cutoff", 120.0, 1200.0)
    set_near(bass, "a_filter_1_cutoff", 430.0 + 60.0 * (V["sub_drive"] - 2.6))
    sub_audio = render_notes(bass, sub_notes, dur2)
    assert_audible("bass", sub_audio)
    sub_audio = sub_audio * duck_env[:, None]

    # ---- pad / chord bed and stabs ------------------------------------------
    triad = [base + 24, base + 24 + m3, base + 24 + p5]
    bed = patch_pad()
    assert_param_matters("pad", bed, [(0.0, 1.0, triad[0], 90)], 1.6,
                         "a_filter_1_cutoff", 150.0, 1500.0)
    set_near(bed, "a_filter_1_cutoff", 430.0)
    bed_audio = render_notes(bed, [(0.0, dur2, t, 88) for t in triad], dur2)
    assert_audible("pad", bed_audio)

    stabp = patch_stab()
    stab_notes = []
    for b in range(bars * 2):
        for off in (1.5, 3.5):
            t0 = b * bar + off * beat
            if t0 >= dur2:
                break
            stab_notes += [(t0, t0 + 0.30, t, 96) for t in triad]
    stab_audio = render_notes(stabp, stab_notes, dur2)
    assert_audible("stab", stab_audio)

    # ---- motif: ONE fixed phrase, identical every bar ------------------------
    # Daniel on the previous generation: "like a drunk child pressing buttons".
    # The cause was a conditional gate - the third note only fired every fourth
    # bar - smeared by a dotted-eighth echo. There is now no gate, no choice and
    # no variation: three notes, same pitches, same positions, every single bar.
    motif_audio = np.zeros((n2, 2), dtype=np.float32)
    if V["motif_on"]:
        MOTIF_PHRASE = [(0.00, 0), (1.50, p5), (2.50, m3)]      # beat, semitone
        mp = patch_motif()
        assert_param_matters("motif", mp, [(0.0, 0.4, base + 24, 100)], 1.2,
                             "a_filter_1_cutoff", 200.0, 2000.0)
        set_near(mp, "a_filter_1_cutoff", 760.0)
        mnotes = []
        for b in range(bars * 2):
            for off, semi in MOTIF_PHRASE:
                t0 = b * bar + off * beat
                if t0 >= dur2:
                    break
                mnotes.append((t0, t0 + 0.28, base + 24 + semi, 100))
        motif_audio = render_notes(mp, mnotes, dur2)
        assert_audible("motif", motif_audio)

    # ---- percussion: unchanged from the numpy engine (hats are noise) --------
    perc = np.zeros(n2, dtype=np.float32)
    hat, hat_o = _hat(rng), _hat(rng, decay=0.017, f0=7400.0)
    for b in range(bars * 8):
        t0 = b * beat
        if t0 * SR >= n2:
            break
        dsp.add_at(perc, (t0 + 0.5 * beat) * SR, hat, 0.22)
        dsp.add_at(perc, t0 * SR, hat, 0.07)
        dsp.add_at(perc, (t0 + 0.75 * beat) * SR, hat_o, 0.10)
        if b % 2 == 0:
            dsp.add_at(perc, (t0 + 0.25 * beat) * SR, hat_o, 0.07)

    # ---- slow, hidden movement ----------------------------------------------
    cyc = 2 * np.pi * np.arange(n2, dtype=np.float64) / n
    bed_cut = 190.0 + 950.0 * 0.5 * (1 - np.cos(cyc * 2 + phases[6]))
    motif_cut = 380.0 + 1250.0 * 0.5 * (1 - np.cos(cyc + phases[0]))
    perc_drift = (0.10 + 0.90 * 0.5 * (1 - np.cos(2 * cyc + phases[1]))).astype(np.float32)

    bed_audio = np.stack([dsp.tv_lowpass(bed_audio[:, 0], bed_cut, q=1.6, block=512),
                          dsp.tv_lowpass(bed_audio[:, 1], bed_cut * 1.03, q=1.6, block=512)], axis=1)
    if V["motif_on"]:
        # the only thing that moves on the motif: a very slow filter opening
        motif_audio = np.stack(
            [dsp.tv_lowpass(motif_audio[:, 0], motif_cut, q=1.1, block=512),
             dsp.tv_lowpass(motif_audio[:, 1], motif_cut * 1.02, q=1.1, block=512)], axis=1)

    chords = V["pad"] * bed_audio + V["stab"] * stab_audio
    if V["chord_width"] != 1.0:
        mid = 0.5 * (chords[:, 0] + chords[:, 1])
        side = 0.5 * (chords[:, 0] - chords[:, 1])
        chords = np.stack([mid + V["chord_width"] * side,
                           mid - V["chord_width"] * side], axis=1)

    # ---- effects -------------------------------------------------------------
    send = (V["chord_delay_send"] * stab_audio
            + V["motif_send"] * V["motif"] * motif_audio)
    d_time = beat * 0.75
    echo = surge_dub_delay(send, d_time, feedback_pct=100.0 * V["feedback"],
                           high_cut=2400.0, wow_cents=6.0,
                           wow_hz=max(0.01, 1.0 / (bar * 4)))
    verb_in = 0.25 * V["motif"] * motif_audio + V["chord_verb"] * bed_audio
    verb = pb_reverb(verb_in, room_size=min(0.9, 0.30 + 0.16 * V["verb_seconds"]))
    fx = echo + 0.9 * verb

    half = slice(n, n2)
    buses = {
        "kick": np.stack([kick_buf[half]] * 2, axis=1),
        "sub": sub_audio[half],
        "chords": chords[half],
        "motif": motif_audio[half] * V["motif"],
        "perc": np.stack([0.85 * (perc * perc_drift)[half],
                          1.10 * (perc * perc_drift)[half]], axis=1),
        "fx": fx[half],
    }
    meta = dict(palette=palette, seed=int(seed), bpm=float(bpm), bars=bars,
                length_s=round(n / SR, 3), root_hz=round(root, 2),
                root_midi=base, delay_s=round(d_time, 4), feedback=V["feedback"],
                variant=variant, engine="surge",
                motif_phrase="beats 0.0/1.5/2.5, root/fifth/minor-third, every bar",
                variant_params={k: v for k, v in V.items()},
                surge_dir=SURGE_DIR, audit=audit())
    return buses, meta


def _hat(rng, decay=0.026, f0=5600.0):
    nn = int(0.10 * SR)
    return dsp.bandpass(dsp.noise(rng, nn) * dsp.exp_decay(nn, decay), f0, 1.1) * 0.6
