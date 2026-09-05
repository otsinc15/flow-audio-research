---
name: hypnotic-techno-sound-design
description: Use for any build round on this project's focus-music track — designing or fixing a hypnotic minimal techno layer in Ableton Live 12 Suite, choosing modulation, setting level and band placement against the kick and bass, or writing variation across 4/8/16/32 bars. Examples - "build the top layer for round 3", "this pad sounds primitive/preset-y, fix it", "why does this layer stick out?", "make the loop stop sounding like a loop", "check this before we export".
---

# Hypnotic minimal techno — sound design

Genre label is **hypnotic minimal techno**. Never write "dub techno".

Every rule below is traceable to `research/production-options/hypnotic-craft-2026-09-05.md`
(tag `[craft]`), `hypnotic-top-layer-2026-09-05.md` (`[top-layer]`),
`techno-pattern-book-2026-09-02.md` (`[pattern-book]`), or our own measurement of the reference
(`[measured]`). `[inference]` = reasoning, not a source. **You cannot hear. Every claim you make must be
a number, or arithmetic on one.**

## Level-1 target (the thing we are trying to hit)

| | value | tag |
|---|---|---|
| Tempo / bar / beat | **120.2 BPM**, bar 2.00 s, beat 0.499 s | `[measured]` |
| Key / pitch set | **C**, set C D E G B; no chord change, one key for the whole track | `[measured]` |
| Layers | **three**: kick, bass, one top layer. Not four. | `[measured]` |
| Top-layer energy | **~3.4 % of mix**, **−12.6 dB vs the kick stem** | `[measured]` |
| Top-layer spectrum | ~45 % in 150–500 Hz, ~48 % in 500 Hz–2 kHz, **< 0.5 % above 2 kHz** | `[measured]` |
| Whole-mix 2–8 kHz | **0.07 %** — there is nothing up there to hide behind | `[measured]` |
| Filter cycle / volume cycle | **7.66 s (0.1305 Hz)** and **8.00 s (0.1250 Hz)** — deliberately unequal | `[measured]` |
| Echo | dotted quarter, **0.75 s** | `[measured]` |
| Constancy | **LRA 4.1 LU** | `[measured]` |
| Master bounce | peak **−6 dBFS**, no limiter | `[craft, Ian Shepherd]` |

## A. Hypnotic top layers — recipes

Pick one lane per candidate. All devices confirmed installed on this Mac `[top-layer]`.

**Lane 1 — resonant percussion (default; the sourced lane).**
DS Tom (or Operator single-sine impulse: A 0 / D ~80 ms / S 0) → Auto Filter (Band-pass, Res ~70 %,
Freq ≈ 600 Hz) → Resonators or Corpus tuned to C/E/G, long decay, Dry/Wet 35–60 % → EQ Eight (HP 150 /
LP 2 k) → Echo → Utility. `[top-layer]`

**Lane 2 — stacked, band-limited breathing pad.**
Wavetable/Poli, **four voices at −1 / 0 / +1 / +2 octaves** at descending levels (Attack's −INF / −11 /
−8 / −12 dB); amp env **A 5 s, D 1.5 s, S −3 dB, R 1 s**, plus a duplicate layer at **15 s attack**.
Band-limit **before** anything else: LP 24 dB ~720 Hz, **HP 280 Hz**, then LP 2 kHz. Voicing C3 E3 C4
**D4 loudest** C5 D5 — added 9th, no third low down. `[craft; measured voicing]`

**Lane 3 — granular / spectral texture.**
Granulator III or Spectral Resonator (Mode Wander, low Mod Rate, Pch Mod ~0.3 st, Dry/Wet 20 %) over a
resampled bounce of an earlier layer. `[craft]`

**Always, whatever the lane:**
- Band-limit first: **EQ Eight HP 150 Hz (48 dB) / LP 2.0 kHz**. This is the single change most likely to
  fix "too loud". `[measured + inference]`
- Aim the bus at **−12.6 dB relative to the kick stem's RMS**. `[measured]`
- Echo at **dotted quarter (749 ms)**, feedback path HP ~200 Hz / LP ~5 kHz. `[measured + pattern-book]`
- Write the texture layer **first**, then fit the beat to it. `[craft, Rod Modell]`

## B. Movement and modulation — the anti-primitive checklist

The amateur tell is **one modulator on one cutoff**. Every sourced pro patch avoids it. `[craft]`

- [ ] **At least two modulators**, on **different destination classes** — pitch/osc-sync, filter, amplitude,
      pan, delay time, drive. Not two on the filter. `[craft]`
- [ ] Rates are **free-running Hz**, not synced divisions, and **a few percent apart**. Start from
      0.1305 Hz and 0.1250 Hz; add a third at **0.042 Hz** (24 s) and a fourth at **0.031 Hz** (32 s).
      `[measured + top-layer]`
- [ ] **One modulator modulates another.** Cheapest stock version: LFO (Random shape) → the **Velocity MIDI
      device's Random knob**. Or an envelope with a long attack → an LFO's rate. `[craft]`
- [ ] **Depths are small.** 10–20 % on volumes; tiny amounts on filter offsets. Subtlety is the technique.
      `[craft]`
- [ ] At least one modulator uses a **non-repeating shape** — Auto Filter **Wander** or **S&H**
      (Quantization = Steps), Roar **Noise: Simplex/Wander/Brown**, Echo **Wobble**. A sine repeats
      forever. `[craft + top-layer]`
- [ ] **Delay time is modulated** (Echo → Modulation tab → Mod Delay ~8 %), offset so long times are
      avoided. `[craft]`
- [ ] **Stereo is decorrelated**: Auto Filter **Spin** ~12 %, or Echo L/R **Phase** ~140°, so left and
      right drift apart. `[top-layer]`
- [ ] Modulating **volume alone counts as rhythm** — three LFOs at 10–20 % on three sample volumes
      generate new syncopations without new notes. `[craft, Attack]`

**Devices whose modulation is scriptable with no UI click**: Auto Filter (LFO + envelope follower),
Echo (Modulation tab + Wobble), Roar (matrix *amounts*; routing is a click), Spectral Resonator,
Auto Pan-Tremolo, Phaser-Flanger, Shifter, Chorus-Ensemble, Corpus. `[top-layer]`
**⚠️ UI-only, cannot be scripted**: the M4L LFO/Shaper/Envelope-Follower **Map** button, any **sidechain
source** dropdown, Corpus / Spectral Resonator **MIDI sidechain** routing, Drift's mod matrix routing,
Roar matrix *routing*. Design around these; don't plan a recipe that needs one. `[top-layer, craft]`

## C. Level and band placement relative to kick and bass

- Top layer: **−12.6 dB under the kick stem**, **~3 % of mix energy**. `[measured]`
- Top layer spectrum: **150 Hz–2 kHz**, under **0.5 %** of its own energy above 2 kHz. `[measured]`
- If a layer "sticks out", the cause is usually **brightness, not level** — the mix has 0.07 % of its
  energy above 2 kHz, so anything up there is unmasked and audible at any fader. Low-pass it; don't just
  pull the fader. `[inference from measured]`
- Expect a **~7 dB spread** across percussive elements (sourced example: hat −8, open hat −10, conga
  −15 dB) and an atmosphere send around **18 % wet**. `[craft, Attack]`
- **Duck gently or not at all.** Reference drums↔bass envelope correlation is 0.404, bass AM depth
  3.7 dB. If you sidechain, prefer Attack's method — **Auto Filter with sidechain on, keyed from the kick
  pre-FX** — over a compressor. ⚠️ source dropdown is a UI click. `[measured + top-layer]`
- Low end mono below ~120 Hz is the folk consensus, sourced only from SEO blogs — the *mechanism* (M/S,
  high-pass the Sides) is from SOS. Apply it, but don't quote a number as fact. `[craft, unverified]`
- Bounce at **−6 dBFS peak**, no limiter. More headroom does no harm. `[craft, Ian Shepherd]`

## D. Variation over 4 / 8 / 16 / 32 bars

**Within one bar** — note chance and velocity deviation in the clip. Set chance ~50 % on non-essential
hits; give velocities a range rather than a value. This never repeats and costs no modulator. `[craft]`

**Across 4 bars** — the sourced structure: **most elements appear in only one or two of the four bars**,
and at least one element fires **once per four bars**. Sourced example: snare only on step 5 of bars 2
and 4; open hat on bar 2 steps 5 and 9 plus bar 4 step 5; FX on bar 2 steps 11 and 13; shaker on **one
note, bar 3 step 9**. Copy this shape, not its sounds. `[craft, Attack]`

**Across 5–15 bars** — give a texture layer an **odd step length against the 16-step bar**. It realigns
only at LCM(n,16)/16 bars: 3 → 3 bars, 5 → 5, 7 → 7, 15 → 15. `[craft, derived]`

**Across 8–16 bars** — the free-running modulators do this for free if their rates are unequal
(0.1305 vs 0.1250 Hz beat at ~180 s). Add a slow Auto Pan-Tremolo at 0.031 Hz for the 16-bar arc.
`[measured + top-layer]`

**Across 32+ bars / whole track** — **arrange by subtraction**, and **fade rather than unmute**. Bring an
element in and out over irregular spans (two bars, then four). Assume an unchanged sequence holds ~2.5–3
minutes before it needs a structural change. `[craft, Mills — the 2.5–3 min figure is unverified]`

**Length is an editing decision.** Render 15–25 minutes of the running system and cut the best 8, rather
than arranging 8 minutes bar by bar. `[craft, Rod Modell + inference]`

**Do not**: build/drop, riser, breakdown-with-impact, filter sweep as a "moment", key change, vocal.
Attention capture is the failure mode for focus music — variation must sit **below the threshold of
noticing**. `[craft, Brain.fm/Endel design claims]`

**Swing**: optional. Offsets ≤ 30 ms are largely unnoticed and quantised versions can rate as groovy as
humanised ones. At 120 BPM a 16th is 125 ms, so keep any offset well under 30 ms. Spend the variation
budget on timbre and velocity instead. If using Groove Pool, keep **Random** low — it scatters
simultaneous notes against each other. `[craft, unverified research + Ableton manual]`

## E. Self-review before export — run every line

1. **Does anything repeat identically every 4 bars?** If yes, it is not finished. Name the two
   free-running rates and confirm they differ. `[measured]`
2. **Are there ≥ 2 modulators on different destination classes** for the top layer? Name them.
3. **Is any modulator's shape non-repeating** (Wander / S&H / Noise / Random)?
4. **Energy above 2 kHz**: is the top layer under 0.5 % of its own energy there, and the mix under ~0.1 %?
   Measure; do not assume.
5. **Level**: is the top layer ~12–13 dB under the kick and ~3 % of mix energy?
6. **Layer count**: is it still three? A fourth layer needs a reason.
7. **Element map**: in the 4-bar loop, does every element hit in all four bars? If yes, thin it out.
8. **Ducking**: is the drums↔bass envelope correlation near 0.4, not near 1.0? No pumping.
9. **Peak**: does the bounce peak at ~−6 dBFS with no limiter?
10. **LRA**: is it near 4 LU? A larger figure means the track has "events" it should not have.
11. **Read every write back** with `get_device_parameters` before claiming a value is set. `[top-layer]`
12. **Say what you could not verify.** Nobody in this loop can hear; an unverified claim is worse than a
    gap.

## Known tooling limits

Our remote script (v1.7.0) has **no automation and no clip-envelope API** — a long swell must be faked
with a periodic device unless we add `clip.automation_envelope(parameter)` + `insert_step` to our own
script (small change, recommended). `[top-layer]` Every device parameter, device load and MIDI note *is*
scriptable. Nothing available can click a Map button or a sidechain dropdown. `[top-layer]`
