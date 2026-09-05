# Stem separation of Lyria output — Demucs vs the model's own mute flags, 2026-09-02

Two routes for pulling round-5 clip 01 (`t118-d30-b30`, the clip Daniel called the
best) apart, plus the same separation applied to the round-6 base so both routes
can be judged on a second source.

Audio: `~/Documents/AI Agent Outputs/Artifacts/flow-audio-candidates/round5-lyria-stems/`
(8 × wav + m4a 112k, 9.19 MB, `manifest.json` in three groups) — **uncommitted.**
Metrics: `stems/stem-stats.json` (uncommitted).

Tooling: **htdemucs 4-stem**, `demucs` in a fresh `~/.venvs/demucs` (Python 3.13,
torch 2.14.0, CPU). ~38 s per 90 s clip on the laptop, no sudo and no Homebrew
needed — pip only. `numpy` is **not** pulled in by the `demucs` wheel and must be
installed alongside it or torch silently reports "Failed to initialize NumPy".

---

## The finding that matters: Demucs files the sub under *drums*

htdemucs is trained on band music — drums, bass, vocals, other. Pointed at
synthetic techno it does something semantically odd but consistent: **the deep sub
goes into the `drums` stem, not `bass`.**

Round-5 clip 01, per stem:

| stem | RMS dBFS | % of energy | <60 Hz | 60–150 | 150–500 | 0.5–2 k | centroid |
|---|---|---|---|---|---|---|---|
| drums | −16.9 | **73.9** | 76.2 | 18.8 | 4.70 | 0.07 | 2804 |
| bass | −21.6 | 24.7 | 8.4 | **90.9** | 0.68 | 0.00 | 319 |
| other | −34.3 | **1.34** | 5.3 | 4.7 | **66.3** | 23.6 | 2231 |
| vocals | −48.7 | 0.05 | 100.0 | 0.0 | 0.01 | 0.00 | 1649 |

So Demucs's `bass` stem is really *the 60–150 Hz body*, and its `drums` stem is
*kick + sub + hats*. Anyone reusing these stems needs to know that before routing
them anywhere.

**The `vocals` stem is silence** — −48.7 dBFS, 0.05 % of energy, and 100 % of what
little it holds is below 60 Hz, i.e. leakage rather than voice. Correct for an
instrumental-only model. It is excluded from the delivery.

---

## Where did the pad Daniel disliked actually go?

**Essentially all of it landed in `other`, with almost no bleed into `bass`.**

- The `bass` stem is **99.3 % below 150 Hz** — only 0.7 % of it sits above, so the
  pad/stab is not contaminating it in any meaningful way. Separation is clean.
- Of *all* energy above 150 Hz in the mix, `other` holds **24.3 %**, `bass` holds
  **3.4 %**, and `drums` holds **72.4 %**.

That last number is the surprise. The midrange is not mostly pad — it is mostly
**drum transients** (kick click and hats). The pad element, isolated in `other`, is
only **1.34 % of the clip's total energy** at −34.3 dBFS.

This reframes the round-5 complaint. The thing Daniel called "too much, annoying,
too spacy" is, in absolute terms, very quiet. It reads as prominent because it is
the *only* sustained content in an otherwise empty midrange — 66 % of `other` sits
in 150–500 Hz, a region where nothing else in the mix lives. Turning it down will
not fix it; it is already down. The fix is either to remove it outright or to give
it company.

Round-6 base splits the same way, more extremely: `drums` **95.0 %**, `bass` 3.7 %,
`other` 1.19 %, `vocals` 0.06 %. Consistent with the round-6 measurement that the
base is 96.5 % below 150 Hz — by Demucs's reckoning that clip is almost entirely
one drum stem. Its `other` does differ in character: **20.7 % of it sits in
2–8 kHz** against 0.14 % for round 5, i.e. round 6 swapped a sustained pad for hats.

---

## Lyria's own mute flags — and a second surprise

Same base config and seed 730118, round-6 prompts, one flag each, 46 s. These are
**not stems**: the model regenerates without the element rather than subtracting it.

| | <60 Hz | 60–150 | **150–500** | centroid | RMS |
|---|---|---|---|---|---|
| r6-00-base (reference) | 81.8 | 14.8 | 2.65 | 1804 | −16.7 |
| **`mute_drums=true`** | **50.9** | 35.6 | **12.32** | 2553 | −17.8 |
| `mute_bass=true` | 80.0 | 14.7 | 4.35 | 3041 | −15.7 |

- **`mute_drums` is the single most effective midrange lever found so far.** It cuts
  sub energy from 81.8 % to 50.9 % and raises the 150–500 Hz body from 2.65 % to
  **12.32 % — a 4.6× gain**, far more than brightness, density, guidance or the
  negative prompts managed in round 6.
- **`mute_bass` barely touches the low end**: 81.8 % → 80.0 % below 60 Hz. Muting
  "bass" leaves the sub swamp completely intact.

Both routes independently reach the same conclusion: **the sub that is drowning
these clips is the kick, not the bass part.** Demucs assigns it to `drums`; Lyria
only removes it when you mute `drums`. That is two different methods agreeing, which
is worth more than either alone.

Practical consequence: if the goal is a mix with audible midrange, the lever is the
kick's low end — not the bass prompt, and not the brightness dial.

---

## Caveats

- htdemucs is trained on recorded band music. Its stem *labels* do not map cleanly
  onto synthetic techno, and the drums/bass boundary here is an artefact of that
  training, not a statement about how Lyria built the track.
- The mute-flag renders are 46.0 s, not 45.0 — the harness stops on a chunk boundary
  and chunks are ~2 s, so it overshoots by up to one chunk. Harmless here.
- **I did not listen to any of this.** No audio playback available; every claim above
  is measurement-derived.
