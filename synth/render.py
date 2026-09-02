#!/usr/bin/env python3
"""Offline renderer for focus-music clips: 60 s, stereo, 44.1 kHz, deterministic.

No AI model, no samples, no reference audio: every sound is synthesised from
oscillators and filters, and the arrangement is a set of rules. Same seed +
palette + BPM always yields bit-identical output.

Genre rules enforced structurally (not by prompt): constant pulse, one key, no
chord changes, no risers/drops/breaks/fills, no fade in or out. Only slow,
hidden movement (filter cutoff, echo colour, percussion level), each on its own
period.

Loop-safety: the clip length is a whole number of bars, every modulator has a
period that divides that length, and the renderer computes two cycles and keeps
the second - so echo and reverb tails from the previous cycle are already
present at sample 0. The clip butt-splices without a click and without a fade.

Thickness: the kick has a tuned 100-200 Hz body on top of the pitch-enveloped
sine, the sub is driven through tanh saturation so its 2nd/3rd harmonics carry
it on small speakers, and a continuous filtered chord bed sits under the stabs -
because a body region of ~46 % of total energy (ref01) cannot be reached with
transient stabs alone.

Usage:
    python render.py --palette b --seed 41 --bpm 117 --out ./out
"""

import argparse
import json
import os

import numpy as np
import soundfile as sf
from scipy.optimize import lsq_linear

import dsp
from dsp import SR
from master import master_chain, normalize_lufs, true_peak_db, integrated_lufs

STEMS = ["kick", "sub", "chords", "motif", "fx"]          # exported stems
BUSES = ["kick", "sub", "chords", "motif", "perc", "fx"]  # balanced separately

# Where we aim each band, as a share of total power. Anchored on ref01 ("Late
# Autumn"), the track Daniel calls perfect: 27.6 / 21.2 / 46.5 / 4.2 / .44 / .11
BAND_EDGES = [0, 60, 150, 500, 2000, 8000, SR / 2]
BAND_LABELS = ["<60Hz", "60-150Hz", "150-500Hz", "500-2kHz", "2-8kHz", ">8kHz"]
BAND_TARGET = np.array([0.235, 0.215, 0.455, 0.082, 0.010, 0.003])


# Arrangement variants. These change balance and arrangement only - same seed,
# same grid, same key, same tempo, same synthesis. `None` reproduces the base
# clips byte for byte. Escalating on the three things Daniel asked for: less
# echoey pad, thicker bass, more motif through the delay.
VARIANT_SPECS = {
    "v1": dict(pad=0.55, stab=0.70, chord_verb=0.10, chord_delay_send=0.26,
               chord_width=0.60, verb_seconds=1.7,
               sub_drive=3.2, bass_oct=0.45, bass_body=0.20, kick_body=1.25, kick_decay=1.30,
               bass_glue=1.50,
               motif_on=True, motif=0.85, motif_send=1.10, motif_oct=0.30, motif_fixed=True,
               feedback=0.58, repeats=14),
    "v2": dict(pad=0.28, stab=0.45, chord_verb=0.05, chord_delay_send=0.16,
               chord_width=0.45, verb_seconds=1.5,
               sub_drive=3.8, bass_oct=0.60, bass_body=0.55, kick_body=1.50, kick_decay=1.55,
               bass_glue=1.80,
               motif_on=True, motif=1.50, motif_send=1.60, motif_oct=0.50, motif_fixed=True,
               feedback=0.64, repeats=16),
    "v3": dict(pad=0.06, stab=0.12, chord_verb=0.02, chord_delay_send=0.06,
               chord_width=0.35, verb_seconds=1.4,
               sub_drive=4.2, bass_oct=0.75, bass_body=0.60, kick_body=1.70, kick_decay=1.75,
               bass_glue=2.00,
               motif_on=True, motif=1.70, motif_send=1.85, motif_oct=0.70, motif_fixed=True,
               feedback=0.68, repeats=18, sparse_fx=True),
}


def variant_params(palette, variant):
    """Base values reproduce the original clips exactly; a variant overrides."""
    base = dict(pad=1.00, stab=0.95, chord_verb=0.25,
                chord_delay_send=(0.45 if palette == "a" else 0.30),
                chord_width=1.00,
                verb_seconds=(2.2 if palette == "a" else 2.9),
                sub_drive=2.6, bass_oct=0.0, bass_body=0.0, kick_body=1.0, kick_decay=1.0,
                bass_glue=0.0,
                motif_on=(palette == "b"), motif=0.90, motif_send=1.20,
                motif_oct=0.0, motif_fixed=False,
                feedback=(0.52 if palette == "a" else 0.62), repeats=12,
                sparse_fx=False)
    if variant:
        base.update(VARIANT_SPECS[variant])
    return base


def band_energy(x, n_fft=8192, hop=2048):
    """Power per band of a mono signal (matches the measurement script's STFT)."""
    x = np.asarray(x, dtype=np.float64)
    pad = n_fft // 2
    xp = np.pad(x, pad, mode="reflect")
    win = np.hanning(n_fft + 1)[:-1]
    nframes = 1 + (len(xp) - n_fft) // hop
    idx = np.arange(n_fft)[None, :] + hop * np.arange(nframes)[:, None]
    S = np.abs(np.fft.rfft(xp[idx] * win, axis=1)) ** 2
    freqs = np.fft.rfftfreq(n_fft, 1.0 / SR)
    return np.array([S[:, (freqs >= BAND_EDGES[i]) & (freqs < BAND_EDGES[i + 1])].sum()
                     for i in range(len(BAND_LABELS))])


def band_shares(stereo):
    e = band_energy(np.asarray(stereo).mean(axis=1))
    return dict(zip(BAND_LABELS, np.round(100 * e / e.sum(), 2)))


# ---------------------------------------------------------------- generators

def make_kick(rng, body=1.0, decay=1.0):
    """909-flavoured kick with real body.

    Three parts: a sine whose pitch falls from ~155 Hz to ~53 Hz (the thump), a
    pair of damped resonances at 130 and 190 Hz (the body - this is the part
    that makes a kick read as 'fat' on a laptop speaker), and a click.
    """
    n = int(0.70 * SR)
    t = np.arange(n) / SR
    f = 55.0 + 103.0 * np.exp(-t / 0.028)
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.082)
    bodysig = body * (0.90 * np.sin(2 * np.pi * 138.0 * t) * np.exp(-t / (0.085 * decay))
                      + 0.72 * np.sin(2 * np.pi * 196.0 * t + 0.8) * np.exp(-t / (0.055 * decay))
                      + 0.32 * np.sin(2 * np.pi * 254.0 * t + 1.9) * np.exp(-t / (0.034 * decay)))
    click = np.sin(2 * np.pi * 1750 * t) * np.exp(-t / 0.0013)
    tick = dsp.bandpass(dsp.noise(rng, n) * np.exp(-t / 0.0016).astype(np.float32),
                        3200.0, 0.9)
    k = (thump + bodysig).astype(np.float32) + 0.26 * click.astype(np.float32) + 0.20 * tick
    return dsp.soft_clip(k * 1.55, 0.78)          # drive: more harmonics, more body


def make_hat(rng, decay=0.026, f0=5600.0):
    n = int(0.10 * SR)
    return dsp.bandpass(dsp.noise(rng, n) * dsp.exp_decay(n, decay), f0, 1.1) * 0.6


def saw_stack(freqs, n, detune_cents, phases, max_hz=5000.0):
    out = np.zeros(n, dtype=np.float32)
    for i, f in enumerate(freqs):
        for j, c in enumerate(detune_cents):
            out += dsp.saw(f * 2 ** (c / 1200.0), n, max_hz=max_hz,
                           phase0=phases[(i * len(detune_cents) + j) % len(phases)])
    return out / (len(freqs) * len(detune_cents))


def chord_stab(freqs, n, detune_cents, phases, decay):
    env = dsp.exp_decay(n, decay) * np.clip(np.arange(n) / (0.004 * SR), 0, 1).astype(np.float32)
    return saw_stack(freqs, n, detune_cents, phases) * env


def horn(root, n, rng):
    """Distant muted horn-like pad: FM, slow attack, dark, reverb-soaked."""
    t = np.arange(n) / SR
    idx = 1.7 * np.clip(t / 1.1, 0, 1) * np.exp(-t / 2.4)
    v = dsp.fm(root, 1.0, idx, n) + 0.5 * dsp.fm(root * 1.005, 2.0, idx * 0.6, n)
    return dsp.lowpass(v * dsp.ar_env(n, 1.15, 2.1), 760.0, 0.8) * 0.5


# ------------------------------------------------------------------ arranger

def render_clip(palette, seed, bpm, seconds=60.0, variant=None):
    rng = np.random.default_rng(seed)
    palette = palette.lower()
    V = variant_params(palette, variant)

    beat = 60.0 / bpm
    bar = 4 * beat
    bars = max(1, int(round(seconds / bar)))
    n = int(round(bars * bar * SR))          # one cycle, exactly bar-aligned
    n2 = 2 * n                                # two cycles; we keep the second

    # Root kept just under 60 Hz (G#1-A#1). The band edges in the reference
    # spec fall at 60 Hz, so where the sub's fundamental sits decides the <60 Hz
    # share outright: a root of 69 Hz put the whole fundamental in 60-150 and
    # dropped the sub band to 6 %. Three keys, one per clip.
    root = float(rng.choice([51.91, 55.00, 58.27]))
    m3, p5, m7 = 2 ** (3 / 12), 2 ** (7 / 12), 2 ** (10 / 12)
    phases = rng.uniform(0, 2 * np.pi, 16)

    dry = {k: np.zeros(n, dtype=np.float32) for k in ["kick", "sub", "motif", "perc"]}
    send_delay = np.zeros(n, dtype=np.float32)
    send_verb = np.zeros(n, dtype=np.float32)

    # ---- kick: four to the floor, never varies -------------------------------
    kick = make_kick(rng, body=V["kick_body"], decay=V["kick_decay"])
    kick_times = [b * beat for b in range(bars * 4)]
    for t0 in kick_times:
        dsp.add_at(dry["kick"], t0 * SR, kick)

    # ---- sub: locked to the kick, sidechain-ducked, saturated ----------------
    duck = np.zeros(n, dtype=np.float32)
    dcurve = dsp.exp_decay(int(0.45 * SR), 0.080)
    for t0 in kick_times:
        dsp.add_at(duck, t0 * SR, dcurve)
    duck_env = 1.0 - 0.72 * np.clip(duck, 0, 1)

    sub_f = np.full(n, root, dtype=np.float32)
    if palette == "b":
        # 1-2 note pattern: root, lifting a minor third on the last beat of every
        # fourth bar. That is the only pitch event in the whole clip.
        for b in range(bars):
            if b % 4 == 3:
                s, e = int((b * bar + 3 * beat) * SR), int((b * bar + 4 * beat) * SR)
                sub_f[s:min(e, n)] = root * m3
    sub_f = dsp.smooth_steps(sub_f, n, tau=0.035)
    # tape/tube-style drive: the 2nd and 3rd harmonics (110-210 Hz) are what
    # make a 55 Hz sub audible on a phone speaker.
    sub = dsp.soft_clip(dsp.sine(sub_f, n) * V["sub_drive"], 0.62)
    sub = dsp.lowpass(sub, 420.0, 0.7)
    if V["bass_oct"] > 0:
        # second bass layer an octave up, saturated then low-passed: its
        # harmonics land at 220-330 Hz, which is where a bass reads as "fat" on
        # headphones rather than just loud on a subwoofer.
        oct_up = dsp.soft_clip(dsp.sine(sub_f * 2.0, n) * 2.8, 0.62)
        sub = sub + V["bass_oct"] * dsp.lowpass(oct_up, 420.0, 0.9)
    if V["bass_body"] > 0:
        body_l = dsp.soft_clip(dsp.sine(sub_f * 3.0, n) * 2.4, 0.62)
        sub = sub + V["bass_body"] * dsp.lowpass(body_l, 520.0, 0.9)
    dry["sub"] = (sub * duck_env).astype(np.float32)

    # ---- chords: one triad, one key, no chord changes ------------------------
    triad = [root * 4, root * 4 * m3, root * 4 * p5]
    chords_l = np.zeros(n, dtype=np.float32)
    chords_r = np.zeros(n, dtype=np.float32)

    # continuous bed: the body of the track. Constant level - it never swells.
    bed_l = saw_stack(triad, n, [-8.0, -0.5, 7.0], phases, max_hz=2200.0)
    bed_r = saw_stack(triad, n, [-6.0, 1.0, 9.0], phases[::-1], max_hz=2200.0)
    bed_l = dsp.highpass(bed_l, 135.0, 0.7) * V["pad"]
    bed_r = dsp.highpass(bed_r, 135.0, 0.7) * V["pad"]
    # pure-sine pad on the same triad, very slightly detuned against itself so
    # it breathes. The beat rate divides the clip length, so it still loops.
    beat_hz = 3.0 / (n / SR)
    for i, f in enumerate(triad):
        d = f * (1.0 + beat_hz / f)
        bed_l += V["pad"] * 0.55 * (dsp.sine(f, n, phase0=phases[i])
                                    + 0.8 * dsp.sine(d, n, phase0=phases[i + 3])) / 1.8
        bed_r += V["pad"] * 0.55 * (dsp.sine(f, n, phase0=phases[i + 6])
                                    + 0.8 * dsp.sine(d, n, phase0=phases[i + 1])) / 1.8

    stab_n = int(0.62 * SR)
    stab = chord_stab(triad, stab_n, [-7.0, 0.0, 6.0], phases, 0.30)
    stab_r = chord_stab(triad, stab_n, [-5.0, 1.5, 8.0], phases[::-1], 0.30)
    for b in range(bars):
        for off in (1.5, 3.5):               # the "and" of 2 and of 4, every bar
            t0 = b * bar + off * beat
            dsp.add_at(chords_l, t0 * SR, stab, V["stab"])
            dsp.add_at(chords_r, t0 * SR + int(0.004 * SR), stab_r, V["stab"])
            dsp.add_at(send_delay, t0 * SR, stab, V["chord_delay_send"])

    # ---- motif: 2-3 notes, one key, no runs. The echoes make the rhythm. -----
    if V["motif_on"]:
        if V["motif_fixed"]:
            # ONE phrase: three notes, same pitches, same positions, every bar,
            # for the whole clip. The previous generation gated the third note to
            # every fourth bar and let a dotted-eighth echo smear the result;
            # Daniel's verdict was "like a drunk child pressing buttons". A
            # one-bar phrase also tiles any bar count, so the loop point is clean.
            phrase = [(0.00, 1.0), (1.50, p5), (2.50, m3)]
            bar_gate, note_gate = 1, ()
        else:
            phrase = [(0.00, 1.0), (1.75, m3), (2.50, p5)]
            bar_gate, note_gate = 2, (2,)
        motif_steps = [st for st, _ in phrase]
        motif_notes = [r for _, r in phrase]
        mn = int(0.7 * SR)
        for b in range(bars):
            if b % bar_gate != 0:
                continue
            for i, st in enumerate(motif_steps):
                if i in note_gate and (b % 4 != 0):
                    continue
                f = root * 4 * motif_notes[i]
                v = (dsp.saw(f, mn, max_hz=4200.0, phase0=phases[i]) * 0.6
                     + dsp.sine(f, mn) * 0.5)
                if V["motif_oct"] > 0:
                    # detuned unison plus a quiet octave up: more presence
                    # without adding notes, so it stays monotone.
                    v = v + V["motif_oct"] * (
                        dsp.sine(f * 2 ** (7.0 / 1200.0), mn, phase0=phases[i + 2]) * 0.7
                        + dsp.sine(f * 2.0, mn, phase0=phases[i + 4]) * 0.45)
                v = dsp.lowpass((v * dsp.exp_decay(mn, 0.20)).astype(np.float32), 900.0, 1.4)
                t0 = b * bar + st * beat
                dsp.add_at(dry["motif"], t0 * SR, v, V["motif"])
                dsp.add_at(send_delay, t0 * SR, v, V["motif_send"])
                dsp.add_at(send_verb, t0 * SR, v, 0.25)

    if palette == "b":
        rave_n = int(0.5 * SR)
        rave = chord_stab([root * 8, root * 8 * m3, root * 8 * p5, root * 8 * m7],
                          rave_n, [-9.0, 0.0, 9.0], phases[3:], 0.16)
        rave = dsp.lowpass(dsp.lowpass(rave, 620.0, 1.3), 620.0, 0.8)
        for b in range(bars):
            if b % 8 == 5:                    # far back, a hint, not party music
                t0 = b * bar + 2.5 * beat
                dsp.add_at(chords_l, t0 * SR, rave, 0.20)
                dsp.add_at(chords_r, t0 * SR + int(0.007 * SR), rave, 0.20)
                dsp.add_at(send_verb, t0 * SR, rave, 0.55)

        hn = int(4.5 * SR)
        hv = horn(root * 4, hn, rng)
        for b in range(bars):
            if b % 12 == 7:
                t0 = b * bar + 0.5 * beat
                dsp.add_at(chords_l, t0 * SR, hv, 0.13)
                dsp.add_at(chords_r, t0 * SR + int(0.011 * SR), hv, 0.13)
                dsp.add_at(send_verb, t0 * SR, hv, 0.55)

    if V["sparse_fx"]:
        # v3 keeps kick + bass + motif and exactly one atmospheric element: a
        # distant horn-like pad, twice in the clip, reverb only.
        hn = int(4.5 * SR)
        hv = horn(root * 4, hn, rng)
        for b in range(bars):
            if b % 12 == 7:
                t0 = b * bar + 0.5 * beat
                dsp.add_at(send_verb, t0 * SR, hv, 0.75)

    # ---- percussion: soft, constant ------------------------------------------
    hat, hat_o = make_hat(rng), make_hat(rng, decay=0.017, f0=7400.0)
    for b in range(bars * 4):
        dsp.add_at(dry["perc"], (b * beat + 0.5 * beat) * SR, hat, 0.22)
        dsp.add_at(dry["perc"], b * beat * SR, hat, 0.07)          # soft on-beat tick
        dsp.add_at(dry["perc"], (b * beat + 0.75 * beat) * SR, hat_o, 0.10)
        if b % 2 == 0:
            dsp.add_at(dry["perc"], (b * beat + 0.25 * beat) * SR, hat_o, 0.07)
        if palette == "b" and (b % 8 == 6):
            dsp.add_at(dry["perc"], (b * beat + 0.25 * beat) * SR, hat_o, 0.08)

    # ---- two cycles, then keep the second ------------------------------------
    tile = lambda x: np.tile(x, 2)
    cyc = 2 * np.pi * np.arange(n2, dtype=np.float64) / n     # 1 cycle per clip

    # slow, hidden movement. Periods divide the clip length so the loop stays
    # seamless; phases differ so the moves do not line up.
    cut_lo, cut_hi = (250.0, 1900.0) if palette == "a" else (230.0, 1700.0)
    cutoff = cut_lo + (cut_hi - cut_lo) * 0.5 * (1 - np.cos(cyc + phases[0]))
    bed_cut = 200.0 + 1300.0 * 0.5 * (1 - np.cos(cyc * 2 + phases[6]))
    perc_drift = (0.10 + 0.90 * 0.5 * (1 - np.cos(2 * cyc + phases[1]))).astype(np.float32)
    echo_damp = 700.0 + 3200.0 * 0.5 * (1 - np.cos(cyc + phases[2]))

    ch_l = dsp.tv_lowpass(tile(chords_l), cutoff, q=2.6, block=512)
    ch_r = dsp.tv_lowpass(tile(chords_r), cutoff * 1.02, q=2.6, block=512)
    bd_l = dsp.tv_lowpass(tile(bed_l), bed_cut, q=1.6, block=512)
    bd_r = dsp.tv_lowpass(tile(bed_r), bed_cut * 1.03, q=1.6, block=512)
    ch_l, ch_r = ch_l + bd_l, ch_r + bd_r
    if V["chord_width"] != 1.0:
        mid, side = 0.5 * (ch_l + ch_r), 0.5 * (ch_l - ch_r)
        ch_l, ch_r = mid + V["chord_width"] * side, mid - V["chord_width"] * side

    # dub delay: dotted eighth, tempo-synced, damped feedback, tape wow
    d_time = beat * 0.75
    fb = V["feedback"]
    wow_hz = 1.0 / (bar * 4)                  # divides the clip -> loops cleanly
    dl, dr = dsp.dub_delay(tile(send_delay), d_time, fb, 2400.0,
                           0.0016, wow_hz, repeats=V["repeats"], pingpong=True,
                           wow_phase=float(phases[4]))
    if palette == "b":
        dl2, dr2 = dsp.dub_delay(tile(send_delay), beat * 1.5, 0.45, 1500.0,
                                 0.0024, wow_hz * 2, repeats=8, pingpong=False,
                                 wow_phase=float(phases[5]))
        dl, dr = dl + 0.5 * dl2, dr + 0.5 * dr2

    ir = dsp.reverb_ir(rng, seconds=V["verb_seconds"], damp_hz=1800.0)
    rvl, rvr = dsp.convolve_stereo(tile(send_verb) + V["chord_verb"] * tile(chords_l), ir)
    fx_l = dsp.tv_lowpass(dsp.highpass(dl + 0.9 * rvl, 120.0), echo_damp, q=0.7, block=512)
    fx_r = dsp.tv_lowpass(dsp.highpass(dr + 0.9 * rvr, 120.0), echo_damp * 1.05,
                          q=0.7, block=512)
    perc2 = tile(dry["perc"]) * perc_drift

    half = slice(n, n2)
    buses = {
        "kick": np.stack([tile(dry["kick"])[half]] * 2, axis=1),
        "sub": np.stack([tile(dry["sub"])[half]] * 2, axis=1),
        "chords": np.stack([ch_l[half], ch_r[half]], axis=1),
        "motif": np.stack([tile(dry["motif"])[half]] * 2, axis=1),
        "perc": np.stack([0.85 * perc2[half], 1.10 * perc2[half]], axis=1),
        "fx": np.stack([fx_l[half], fx_r[half]], axis=1),
    }
    meta = dict(palette=palette, seed=int(seed), bpm=float(bpm), bars=bars,
                length_s=round(n / SR, 3), root_hz=round(root, 2),
                delay_s=round(d_time, 4), feedback=fb, variant=variant,
                variant_params={k: v for k, v in V.items()})
    return buses, meta


# ------------------------------------------------------------------- mixdown

NOMINAL = {"kick": 0.80, "sub": 0.42, "chords": 0.85, "motif": 0.45,
           "perc": 0.45, "fx": 0.50}
GAIN_BOUNDS = (0.30, 3.2)
# On a variant the arrangement is the point, so the solver is held tight on the
# elements the variant is *about* (pad, motif, fx) and given room on the bass,
# where its only job is to keep the band balance honest.
VARIANT_GAIN_BOUNDS = {"kick": (0.65, 1.80), "sub": (0.65, 1.80),
                       "chords": (0.80, 1.25), "motif": (0.85, 1.25),
                       "perc": (0.60, 1.60), "fx": (0.85, 1.25)}
# Pattern-book renders fix the chord's SHAPE - high-passed at 80 Hz, scooped at
# 600 Hz, capped at 4.5 kHz, short envelope - so its level no longer carries the
# "sits behind" intent and the solver can move it freely. With the variant's
# 1.25x chord ceiling it could not: v1 sat at 39.6 % in the body region with
# 35 % below 60 Hz, because the chord was the binding constraint, not the bass.
VARIANT_GAIN_BOUNDS_BOOK = dict(VARIANT_GAIN_BOUNDS,
                                kick=(0.35, 1.80), sub=(0.30, 1.80),
                                chords=(0.60, 3.20), fx=(0.15, 2.00))


def balance(buses, target=BAND_TARGET, passes=2, bounds=GAIN_BOUNDS):
    """`bounds` is either one (lo, hi) pair or a per-bus dict of them."""
    """Choose stem gains so the mix lands on the reference band balance.

    Band power is additive across (near-uncorrelated) stems, so each band's share
    is a linear function of the squared gains - which makes the balance a small
    bounded least-squares problem rather than a guess. Gains are clamped so the
    solver can shape the spectrum but can never mute an element.
    """
    if isinstance(bounds, dict):
        lo = np.array([bounds[k][0] ** 2 for k in BUSES])
        hi = np.array([bounds[k][1] ** 2 for k in BUSES])
    else:
        lo = np.full(len(BUSES), bounds[0] ** 2)
        hi = np.full(len(BUSES), bounds[1] ** 2)
    E = np.stack([band_energy(buses[k].mean(axis=1) * NOMINAL[k]) for k in BUSES], axis=1)
    tgt = np.array(target, dtype=float)
    w = np.ones(len(BUSES))
    for _ in range(passes):
        scale = 1.0 / np.maximum(tgt, 0.004)
        A = (E * scale[:, None]) / (E.sum() + 1e-30)
        sol = lsq_linear(A, tgt * scale, bounds=(lo, hi), max_iter=300)
        w = sol.x
        got = (E @ w)
        got = got / got.sum()
        tgt = np.clip(np.array(target) * (np.array(target) / np.maximum(got, 1e-6)) ** 0.6,
                      1e-5, None)
        tgt = tgt / tgt.sum()
    return {k: float(NOMINAL[k] * np.sqrt(w[i])) for i, k in enumerate(BUSES)}


def bass_glue(kick, sub, drive):
    """Interlock kick and sub through one shared saturator.

    Driving the summed bass and then applying the resulting gain curve back to
    each part is what a bus saturator does: the two stop fighting for the same
    peak and start reading as one instrument. Because the same curve is applied
    to both, the stems still sum exactly to the glued bus.
    """
    b = kick + sub
    x = b * drive
    th = 0.85
    ratio = np.where(np.abs(x) > 1e-6, th * np.tanh(x / th) / np.where(np.abs(x) > 1e-6, x, 1.0), 1.0)
    return kick * ratio, sub * ratio


def render_and_write(palette, seed, bpm, outdir, name=None, stems_dir=None,
                     unmastered_lufs=-16.0, mastered_lufs=-14.0, variant=None,
                     engine="numpy", pattern_book=True):
    if engine == "surge":
        from surge_engine import render_surge_clip
        buses, meta = render_surge_clip(palette, seed, bpm, variant=variant,
                                        pattern_book=pattern_book)
    else:
        buses, meta = render_clip(palette, seed, bpm, variant=variant)
    if not variant:
        bounds = GAIN_BOUNDS
    elif meta.get("pattern_book"):
        bounds = VARIANT_GAIN_BOUNDS_BOOK
    else:
        bounds = VARIANT_GAIN_BOUNDS
    gains = balance(buses, bounds=bounds)
    scaled = {k: gains[k] * buses[k] for k in BUSES}
    glue = meta["variant_params"]["bass_glue"]
    if glue > 0:
        scaled["kick"], scaled["sub"] = bass_glue(scaled["kick"], scaled["sub"], glue)
    mixraw = sum(scaled[k] for k in BUSES)
    # exported stems: percussion rides along with the motif stem, at its own
    # solved gain, so the five-stem export still sums to the mix exactly.
    stems = {k: scaled[k] for k in STEMS}
    stems["motif"] = stems["motif"] + scaled["perc"]

    # reference copy: loudness normalised and peak-limited, but no glue
    # compression and no saturation
    unm, g_unm = normalize_lufs(mixraw / (np.max(np.abs(mixraw)) + 1e-9) * 0.5,
                                SR, unmastered_lufs)
    unm, uinfo = master_chain(unm, SR, target_lufs=unmastered_lufs,
                              ceiling_dbtp=-1.0, glue=False, clip_drive_db=12.0)
    mastered, minfo = master_chain(mixraw, SR, target_lufs=mastered_lufs, ceiling_dbtp=-1.0)

    os.makedirs(outdir, exist_ok=True)
    name = name or f"synth-{palette}-{seed}"
    mix_path = os.path.join(outdir, f"{name}.wav")
    unm_path = os.path.join(outdir, f"{name}-unmastered-16lufs.wav")
    sf.write(mix_path, mastered, SR, subtype="PCM_24")
    sf.write(unm_path, unm, SR, subtype="PCM_24")

    meta.update(
        gains={k: round(v, 4) for k, v in gains.items()},
        bands_pre_master_pct={k: float(v) for k, v in band_shares(unm).items()},
        bands_post_master_pct={k: float(v) for k, v in band_shares(mastered).items()},
        unmastered=uinfo,
        mastered=minfo,
    )

    sd = stems_dir or os.path.join(outdir, "stems", name)
    os.makedirs(sd, exist_ok=True)
    for k in STEMS:
        s = (stems[k] * g_unm).astype(np.float32)
        sf.write(os.path.join(sd, f"{name}-{k}.wav"), s, SR, subtype="PCM_24")
    meta["stems_note"] = ("stems are at the -16 LUFS mix level and sum to that mix "
                          "before its peak limiter")
    with open(os.path.join(sd, f"{name}-meta.json"), "w") as f:
        json.dump(meta, f, indent=1)
    return mix_path, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--palette", required=True, choices=["a", "b"])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--bpm", type=float, default=116.0)
    ap.add_argument("--out", default="./out")
    ap.add_argument("--name", default=None)
    ap.add_argument("--variant", default=None, choices=sorted(VARIANT_SPECS))
    ap.add_argument("--no-pattern-book", action="store_true",
                    help="surge engine only: restore the round-1 arrangement")
    ap.add_argument("--engine", default="numpy", choices=["numpy", "surge"],
                    help="numpy = the original oscillators (earlier clips "
                         "reproduce byte for byte); surge = Surge XT + Faust")
    args = ap.parse_args()
    p, meta = render_and_write(args.palette, args.seed, args.bpm, args.out, args.name,
                               variant=args.variant, engine=args.engine,
                               pattern_book=not args.no_pattern_book)
    print(json.dumps({"wav": p, **meta}, indent=1))


if __name__ == "__main__":
    main()
