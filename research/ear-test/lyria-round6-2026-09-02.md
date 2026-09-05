# Lyria round 6 — knob audition, 2026-09-02

Eight 90 s clips, **one knob changed per clip**, everything else held identical.
Base = round-5 clip 01's settings with the pad/melody wording stripped out:
118 BPM, `C_MAJOR_A_MINOR`, density 0.3, brightness 0.3, guidance 4.0, **seed 730118**.

Audio: `~/Documents/AI Agent Outputs/Artifacts/flow-audio-candidates/round6-lyria/`
(wav + m4a 112k + `manifest.json`, 10.57 MB of m4a) — **uncommitted.**
Batch: `lyria/batch-round6.json`. Metrics: `out6/round6-analysis.json` (uncommitted).

Transport was clean: 8/8 at exactly 90.0 s, 45 chunks each, **zero reconnects**,
no safety-filtered prompts. ~12 min of API time as budgeted.

---

## The headline: seed makes Lyria bit-exactly reproducible

Clip 07 is the base re-rendered with the same seed. It came back **byte-identical**
to clip 00 — Pearson r = 1.0000 on the raw waveform and `np.array_equal` True on
every sample, against a control correlation of −0.145 between 00 and 01.

This is the finding that matters most, because it retroactively validates the
whole experiment design: with the seed pinned, every difference below is *caused*
by the named knob, not by generation variance. Round 5 could not make that claim —
its ±2.1 LU level spread across identically-configured clips was pure noise. It
also means a shipped product can store a seed + config and reproduce a track
exactly, rather than storing audio.

Caveat worth stating: this is reproducibility on **one model version within one
day**. `lyria-realtime-exp` is experimental, and nothing in the docs promises seed
stability across model updates.

---

## Did the knobs do anything?

Long-term band percentages, spectral centroid, onset rate and a 4-bar repetition
score. Base row is the reference; deltas are causal because the seed is fixed.

| clip | knob | <60 Hz | 60–150 | 150–500 | centroid | onsets/min | repeat |
|---|---|---|---|---|---|---|---|
| 00 | *base* | 81.8 | 14.8 | 2.6 | 1804 | 379 | 0.984 |
| 01 | temperature 0.6 | 67.9 | 26.0 | 4.3 | **2419** | 357 | 0.966 |
| 02 | guidance 6.0 | 61.5 | 36.0 | 2.3 | 1824 | **303** | 0.993 |
| 03 | brightness 0.15 | 75.8 | 18.8 | 5.2 | **1309** | 448 | 0.996 |
| 04 | density 0.2 | 53.4 | 41.3 | 3.8 | 2120 | **514** | 0.990 |
| 05 | negative prompts | 60.2 | 33.8 | **5.0** | 2073 | **285** | 0.996 |
| 06 | only_bass_and_drums 45 s | 65.5 | 32.7 | 1.6 | 2181 | 405 | 0.993 |
| 07 | *base repeat* | 81.8 | 14.8 | 2.6 | 1804 | 379 | 0.984 |

**Ranked by how much the knob actually moved the audio:**

1. **`density` — strong, but inverted.** Lowering density 0.3 → 0.2 *raised* onset
   rate from 379 to 514/min, and moved 28 points of energy out of the sub band.
   This is the second round in a row density has behaved non-monotonically (round 5:
   483 → 365 → 487 at 122 BPM). **Do not build a "calm ↔ busy" control on this dial.**
2. **`brightness` — strong and correct.** 0.3 → 0.15 dropped the centroid 1804 → 1309,
   the largest timbral move of any knob, in the expected direction. Consistent with
   round 5. This is the most trustworthy timbre control.
3. **Negative-weight prompts — strong, and they work.** See below.
4. **`temperature` — moderate.** 1.1 → 0.6 raised the centroid by 616 Hz and pulled
   14 points out of the sub band. Notably it *lowered* the repetition score (0.984 →
   0.966), the opposite of the intuition that low temperature = more locked.
5. **`guidance` — weak on timbre, real on density.** 4.0 → 6.0 left the centroid
   essentially unchanged (+20 Hz) but cut onsets 379 → 303, the second-largest
   reduction. Max adherence buys you restraint, not colour.
6. **`only_bass_and_drums` — near-inert here.** Across the flag's on/off boundary the
   spectrum barely moves: 0–45 s reads 98.4 % below 150 Hz / 1.41 % in 150–500 Hz,
   and 45–90 s reads 97.9 % / 1.75 %. Releasing the flag did **not** bring the stab
   back in any measurable way. Caveat: the stab was only weighted 0.3, so there was
   little to restore — this is not proof the flag is broken, only that it did nothing
   useful at this weighting.

**Repetition score is weakly informative and I won't overclaim it.** Mean cosine
self-similarity between non-adjacent 4-bar windows (MFCC + chroma) lands at
0.966–0.996 for every clip. Everything is highly self-similar at bar scale; the
metric saturates and cannot separate "hypnotic" from "monotonous". The onset-rate
column is the more honest proxy for busyness.

---

## Negative weights are accepted, and they did something useful

I probed this live with a 12 s render before spending batch time: a prompt at
weight −0.6 is **accepted** — no API error, no `filtered_prompt`, audio returned.
The docs only say the weight "can take any value except `0`", and that is borne out.

Clip 05 (base **plus** `ambient pads:-0.6, spacey reverb:-0.6`) moved further from
the base than most of the numeric dials: onset rate fell 379 → **285/min** (the
lowest of all eight), and the 150–500 Hz body region nearly doubled, 2.6 % → **5.0 %**
(the highest of any clip). Pushing *away* from pads and reverb made the clip both
calmer and less sub-swamped.

Given Daniel has now asked three rounds running for less pad, **this is the most
promising lever in the set** and the one I would build the next round around.

---

## The problem round 6 created

Stripping the pad words worked — arguably too well. **The base is now 96.5 % below
150 Hz with only 2.6 % in the 150–500 Hz body region**, against a 15–45 % target and
ref01's 46 %. Round 5's clips were 87–97 % below 150 Hz; round 6's base is at the
very worst end of that.

So the round-5 complaint ("too spacy, pad too much") has been answered by removing
almost everything above the bass. On earbuds or a laptop speaker most of these will
read as kick and sub with very little else. Clip 05 (5.0 %) and clip 03 (5.2 %) have
the most body of the set, and they are the two I would listen to first after 00.

Level also runs quiet — base is −17.5 LUFS, LRA 1.1 — and clip 05 peaks at −0.1 dBFS,
so headroom is not reliable even when nothing clips outright.

---

## Listening notes — the caveat stands

**I did not listen to any of these.** No audio playback here, and I am not going to
present measurements as ears. What the numbers license:

- 00 should read as far more locked and less "spacy" than round 5 — fewer onsets in
  the top end, centroid down to 1804 Hz, no sustained element in the data.
- 03 (brightness 0.15) will be the darkest and most closed-in of the set.
- 04 (density 0.2) will, counter-intuitively, sound **busier** than the base.
- 05 (negative prompts) should be the calmest *and* the one with the most audible
  midrange — the two things Daniel asked for, arriving together.
- 06 will likely sound like almost nothing changes at the 45 s mark.
- **07 is bit-identical to 00. Skip it** — it's an experiment, not a candidate.

**The question for Daniel's ears:** is 00 now *hypnotic*, or has stripping the pad
left it *empty*? If empty, the fix is clip 05's approach — keep the stab, push away
from pads with negative weights — rather than adding pad wording back.

---

## Docs confirmations requested

- **Default temperature is 1.1.** Confirmed verbatim on the RealTime docs page:
  "More classical parameters like `temperature` (0.0 to 3.0, default 1.1), `top_k`
  (1 to 1000, default 40), and `seed` ... are also customizable". Noted in the manifest.
- **Lyria RealTime is text-only — no audio-reference input exists.** The model page
  lists `Supported data types → Input: Text (Weighted prompts)`, and Output as
  `Audio (Raw 16-bit PCM)`. There is no audio or image input field anywhere in the
  API surface, and the Limitations section adds "Instrumental only: The model
  generates instrumental music only." Nothing was sent as reference audio, and
  nothing could have been.

---

## Harness changes

`lyria/render.py` now passes through **every** `LiveMusicGenerationConfig` field —
added `top_k`, `mute_bass`, `mute_drums`, `only_bass_and_drums` and
`music_generation_mode` alongside the existing ones, as CLI flags, batch keys **and**
steer-script keys (clip 06 toggles `only_bass_and_drums` mid-stream). Field coercion
and range checking are now driven off one central table, and both batch files and
steer scripts reject unknown keys instead of silently ignoring them — the round-6
batch was written against that and it caught two prompt-parsing mistakes before any
API time was spent.

One trap worth recording: **prompt text cannot contain a comma** in the
`"text:weight,text:weight"` string form. `"ambient pads, spacey reverb:-0.6"` parses
as *two* prompts — "ambient pads" at the default weight 1.0 and "spacey reverb" at
−0.6 — i.e. the exact opposite of the intent on the first half. The `--dry-run`
output is what caught it. Round 6 uses two separate negative prompts instead.
