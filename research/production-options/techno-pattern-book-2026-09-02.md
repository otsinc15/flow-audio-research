# Techno pattern book — hypnotic dub / minimal techno for focus audio

Date: 2026-09-02. Written for a **code-driven sequencer**: every rule below is meant to become a
number, a grid, or a range in `synth/render.py`, not a paragraph a human interprets.

**Scope.** Hypnotic dub / minimal techno in the Basic Channel · Maurizio · Rhythm & Sound ·
Plastikman · Robert Hood lane, at **112–120 BPM**, used as *focus* music. Explicitly out of scope:
psytrance, rolling acid basslines, risers, drops, breaks, vocals, key changes.

**Method and its honest limits.**

- Discovery ran through Perplexity `sonar-pro` over OpenRouter (`sonar-*.json` in this directory).
  **Every claim below was then re-fetched from the primary page by this agent** and saved as
  `src-<slug>.txt` with URL and fetch date at the top. Where a Perplexity answer could not be
  re-verified from a primary page, it is **not** reproduced — see §11 "Not found".
- **Attack Magazine's Beat Dissected grids are images.** This agent fetched the article text, not the
  grid pictures, and cannot see them. Every step grid in §2 is therefore **reconstructed from the
  article's own prose** ("the tom sounds at measures 7 and 15", "hat plays straight off-beats"), or
  marked as a house default derived from the genre's standard. Where a grid is a derivation rather
  than a transcription, it says so.
- Arithmetic (delay-time tables, swing-offset milliseconds) is computed here from a cited formula and
  labelled **derived**. It is not attributed to any source.
- Nobody involved in producing this file can hear. Nothing here is a listening judgement.

**Notation used throughout.** One bar of 4/4 = **16 steps**, numbered **1–16**. Downbeats (quarter
notes) are steps 1, 5, 9, 13. Straight off-beat eighths are 3, 7, 11, 15. Velocity is MIDI 0–127.

---

# PART 1 — Patterns and arrangement

## 1. Global grid rules

| Rule | Value | Source |
|---|---|---|
| Tempo window for this product | 112–120 BPM (house target 114–118) | Repo brief + `research/ear-test/palettes.md`; measured reference ref01 = 114.8 BPM (`research/ear-test/spec-from-references.md`) |
| Resolution | 16 steps/bar; motif and delay events may need 1/32 resolution for swing offsets | derived |
| Meter | 4/4 only, no bar-length changes | all cited beat-dissected articles are 4/4 |
| Key | one key for the whole session, no chord change | brief; consistent with Attack's dub-techno beat, which stays on a single D♯ minor chord (`src-attack-basic-channel-dub.txt`) |

**Tempo reality check on the sources.** The single most on-brief tutorial found — Attack Magazine's
*Basic Channel-Style Dub Techno* — is written at **145 BPM**, well above this product's window
(`src-attack-basic-channel-dub.txt`, Spec block: "Tempo 145 BPM / Swing NONE"). Attack's *Dark Berlin
Techno* runs **120–130 BPM, swing 50–55 %**; *Sub-Zero Minimal Techno* runs **125–130 BPM, swing
55–70 %**; *Thumping Techno* runs **130–135 BPM, swing 50–60 %**. **No fetched tutorial is written at
112–120 BPM.** The *patterns* transfer; the *tempo* is this product's own choice, and the sequencer
should treat the tempo window as a product constraint, not an inherited genre fact.

## 2. Drum programming

### 2.1 The canonical grid

Steps marked `x` = hit, `.` = silent, `o` = ghost (low velocity).

```
step:      1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
kick       x  .  .  .  x  .  .  .  x  .  .  .  x  .  .  .
clap/snr   .  .  .  .  x  .  .  .  .  .  .  .  x  .  .  .
closed hat .  .  x  .  .  .  x  .  .  .  x  .  .  .  x  .
open hat   .  .  .  .  .  .  .  .  .  .  .  .  .  .  x  .
ride/perc  .  .  .  .  .  .  x  .  .  .  .  .  .  .  x  .
```

Sourcing, line by line:

- **Kick, four-to-the-floor on 1/5/9/13.** "The first step in laying down a vintage dub techno beat is
  the four-to-the-floor kick and the off-beat hat. The pattern is as straightforward as can be"
  (`src-attack-basic-channel-dub.txt`). Same in `src-attack-dark-berlin-techno.txt` ("the kick hits
  four-to-the-floor"), `src-attack-sub-zero-minimal-techno.txt` ("a simple four-to-the-floor
  pattern"), and `src-musicradar-minimal-groove.txt` ("We program kicks on each beat").
- **Closed hat on straight off-beats 3/7/11/15.** "hi-hats on off-beats"
  (`src-musicradar-minimal-groove.txt`); "Hat 2 plays straight off-beats"
  (`src-attack-sub-zero-minimal-techno.txt`); "the off-beat hat"
  (`src-attack-basic-channel-dub.txt`).
- **Open hat.** Attack's Basic Channel beat uses an **open** hat as the off-beat hat itself, not a
  closed one ("For the open hat we used 'rit_oh_weurgh'… Use an EQ to cut the unnecessary low
  frequencies while boosting the top end", `src-attack-basic-channel-dub.txt`). Attack's Dark Berlin
  beat uses "a heavily compressed 909 open hi-hat… added to the off-beat, with a subtle variation at
  the end of every couple of bars" (`src-attack-dark-berlin-techno.txt`). **The single-open-hat-on-15
  row above is a derived house default**, not a transcription: the sourced practice is either *all*
  off-beats open (Basic Channel style) or off-beat open with a periodic variation. Both are encodable;
  pick one per palette and hold it.
- **Clap/snare on 5 and 13 (beats 2 and 4).** "a clap and snare hit on two and four"
  (`src-musicradar-minimal-groove.txt`); "program a hit on every other downbeat"
  (`src-attack-basic-channel-dub.txt`); "sounds on the 2nd and 4th beat of each bar"
  (`src-attack-sub-zero-minimal-techno.txt`).
- **The sparser dub variant that this product should prefer:** Attack's Dark Berlin beat puts the clap
  **only on beat 2** — "The clap is only triggered on the second kick of each bar, rather than the
  more common technique of a clap/snare on the second and fourth kick"
  (`src-attack-dark-berlin-techno.txt`). One clap per bar instead of two is the single cheapest way to
  halve the perceived event density without touching anything else.

### 2.2 Multi-bar placements (the 4-bar loop is the real unit)

Sourced placements that only exist across more than one bar:

| Element | Placement | Source |
|---|---|---|
| Filtered low tom acting as second kick | steps **7** and **15**, "with a simple variation at the end of the four bar loop" | `src-attack-dark-berlin-techno.txt` |
| Distorted noise stab | on the **third kick of each bar** (step 9), plus "just before the fourth kick in every other bar" (≈ step 12) | `src-attack-dark-berlin-techno.txt` |
| Ghost snare | "immediately before each new bar" (step 16 or a 1/32 before step 1) | `src-attack-sub-zero-minimal-techno.txt` |
| Ghost hat | "an additional ghost hit at a lower velocity on the eighth division of each bar" (step 9, off the 8th-note grid) | `src-attack-sub-zero-minimal-techno.txt` |
| Sparse noise/FX layer | a **3-bar** sequence against a 4-bar loop, "which will result in slightly unusual phrasing" | `src-musicradar-minimal-groove.txt` |

**The 3-against-4 trick is the highest-value arrangement primitive found.** A short sequence whose
length is coprime with the main loop (3 bars against 4, or 5 against 8) produces years of
non-repeating placement from two integers, with no randomness and no "event". Encode it as
`period_bars` per element, not as a hand-written 16-bar pattern.

### 2.3 Swing / shuffle

Attack publishes a **swing percentage** in every Beat Dissected spec block. The convention is
MPC-style: 50 % = straight, higher values push every *even* subdivision later, with 66.7 % ≈ a full
triplet feel.

| Article | Tempo | Published swing | Source |
|---|---|---|---|
| Basic Channel-Style Dub Techno | 145 BPM | **NONE** | `src-attack-basic-channel-dub.txt` |
| Dark Berlin Techno | 120–130 BPM | **50–55 %** | `src-attack-dark-berlin-techno.txt` |
| Thumping Techno (peak-time) | 130–135 BPM | **50–60 %** | `src-attack-thumping-techno.txt` |
| Sub-Zero Minimal Techno | 125–130 BPM | **55–70 %** | `src-attack-sub-zero-minimal-techno.txt` |

**Verbatim, and this is the rule that matters most for this lane:** dub techno gets its movement from
the echoes, not from the sequencer. Attack, programming the Basic Channel beat, writes that a
percussion loop should be placed "exactly on offbeat 16th notes to keep everything quantized. This is
by no means a rule but **one of the hallmarks of dub techno is groove and movement resulting from
delay instead of heavily swung drum parts**" (`src-attack-basic-channel-dub.txt`).

Attack's own editor, answering a reader in the Dark Berlin comments, on whether one swing setting
covers the whole track: "In this example, yes – although it's a fairly straight beat with a pretty
gentle swing so it is not having a huge impact. with more complex beats it can be interesting to use
different swing settings on different drum parts" (`src-attack-dark-berlin-techno.txt`).

**Encodable swing (derived arithmetic, not sourced).** For swing percentage `s` and 16th-note
duration `d16 = 15000 / BPM` ms, delay every even 16th (steps 2, 4, 6, …) by
`offset_ms = d16 × (s − 50) / 50`. At 115 BPM, `d16 = 130.4 ms`:

| Swing | Offset applied to even 16ths |
|---|---|
| 50 % (straight) | 0.0 ms |
| 52 % | 5.2 ms |
| 55 % | 13.0 ms |
| 58 % | 20.9 ms |
| 66.7 % (triplet) | 43.5 ms |

**House recommendation for this product: 50–54 %, applied to hats and sparse percussion only, never
to kick or clap.** That sits inside the Dark Berlin range, honours the Basic Channel "NONE", and
respects the source's own statement that different parts can carry different swing.

### 2.4 Velocity and ghost notes

**No fetched primary source publishes numeric MIDI velocity values for this genre.** Attack states
the principle without numbers — "Velocity play a fundamental role here, making the pattern feel more
humanised and adding a subtle groove" (`src-attack-thumping-techno.txt`, quoted in
`synth-instruments-2026-09-02.md` §5.2) — and describes ghosts qualitatively ("an additional ghost hit
at a lower velocity", `src-attack-sub-zero-minimal-techno.txt`). Perplexity returned a numeric table
(accents ~100–115, ghosts ~40–60) but attributed it to nothing re-fetchable: **treated as unverified,
see §11.**

The defensible substitute is **per-hit parameter jitter rather than velocity curves**, which the
sources *do* support for this genre. A Hacker News commenter who has owned three TR-808s: "I can
confirm that each one sounds different" (quoted with URL in `synth-instruments-2026-09-02.md` §5.2).
Attack, on the same idea in software: "slightly tweak the sample settings for the alternate clap hits
… altering the sample's decay envelope or pitch to generate movement"
(`src-attack-dark-berlin-techno.txt`).

**Encodable house defaults (derived, flagged as house policy not source):**

| Element | Accent | Ghost | Per-hit jitter |
|---|---|---|---|
| Kick | fixed, no accent pattern | none | pitch ±1 %, decay ±3 % |
| Clap | full | — | decay ±8 %, pitch ±2 % on the alternate bar (sourced technique, Dark Berlin) |
| Closed hat | off-beats full | ghosts at ~45 % of accent amplitude | decay ±10 % |
| Ride/perc | ~85 % of hat accent | — | — |

The kick keeps a *fixed* velocity on purpose: the product's measured target is LRA ≤ 4 LU
(`research/ear-test/spec-from-references.md`), and an accent pattern on the loudest element in the mix
is the fastest way to lose that.

### 2.5 How dub techno differs from peak-time techno

| Axis | Dub techno (this lane) | Peak-time techno | Evidence |
|---|---|---|---|
| Swing | none to gentle (0–55 %) | comparable or higher (50–70 %) | spec blocks, §2.3 |
| Source of groove | the delay repeats | the drum programming | "groove and movement resulting from delay instead of heavily swung drum parts" (`src-attack-basic-channel-dub.txt`) |
| Clap density | often 1/bar (beat 2 only) | 2/bar (beats 2 and 4) | `src-attack-dark-berlin-techno.txt` vs `src-musicradar-minimal-groove.txt` |
| Hat layers | 1–2 | 2+ layered, saturated, plate-reverbed, HP-filtered to sit above the mids | `src-attack-thumping-techno.txt` (via `synth-instruments-2026-09-02.md` §5.3) |
| Harmonic content | one chord, held | stabs, progressions, parallel movement | `src-attack-basic-channel-dub.txt` vs `src-attack-parallel-chord-stabs.txt` |
| Where the space is | deliberately empty mids, filled by echo tails | filled by percussion layers | `src-rbma-moritz-von-oswald.txt` (§7.1 below) |

**Kick rule with a hard source: the kick does not go into the dub effects.** Attack, setting up a dub
drum chain: "every sound will get its own Dub Machines plugin **except for the kick**, as we want this
to be the anchor that holds the beat down" (`src-attack-dub-drum-processing.txt`). Everything else in
the kit can be echo-soaked; the kick stays dry and on the grid.

## 3. Bass

### 3.1 Sub and bass are two parts, not one

Attack's warehouse-bass tutorial builds the low end from **three** layers — "A sub sample / A bassline
/ A percussive layer" — and processes each differently (`src-attack-warehouse-rolling-bass.txt`). The
same split appears in the Basic Channel beat, where the sub is added *last*, after the kick was
deliberately chosen to lack sustain: the kick sample "has a good thumpy transient as well as some
subby low end that lacks sustain. This works out well because we are going to add sub bass in the
final step" (`src-attack-basic-channel-dub.txt`).

| Layer | Register | Job | Source |
|---|---|---|---|
| Sub | root, one octave; low-passed at **~80 Hz, 12 dB/oct** | the felt weight | `src-attack-warehouse-rolling-bass.txt` |
| Bass | root, octave above the sub (the tutorial uses G2 ≈ 98 Hz) | the audible note on small speakers | same |
| Percussive top | copy of the kick through a **1/16 delay**, then widened | lets the bass groove read on speakers with no sub | same |

That third layer is a cheap, fully deterministic trick worth stealing verbatim: duplicate the kick,
run it into a 1/16 delay at 100 % wet, EQ it, widen it. No new voice needed.

### 3.2 Note patterns

Sourced patterns, all from `src-attack-basic-channel-dub.txt` and
`src-attack-warehouse-rolling-bass.txt`:

- **Two pitches, not a riff.** Attack's Basic Channel sub uses exactly two notes: the sample tuned
  "down two semitones to get it to a D♯ note" and a second copy "up three semitones for a G♯" — the
  root and its fifth, nothing else, in the same key as the chord.
- **Leave step 1 of every beat empty.** "Leaving the first 16th-note of every beat empty is important
  to prevent clashing with the kick" (`src-attack-warehouse-rolling-bass.txt`). That is a *sequencing*
  solution to kick/bass masking and it costs nothing at runtime.
- **Short notes under program control.** "shorten the sample and set a short release time to have
  total control over the note lengths while drawing them in the piano roll"
  (`src-attack-basic-channel-dub.txt`).

Encodable pattern set for this product (derived from the above; the first is a transcription of the
"leave the first 16th empty" rule):

```
step:            1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
A: offbeat 8ths  .  .  x  .  .  .  x  .  .  .  x  .  .  .  x  .     (sub, root)
B: gap-on-beat   .  x  x  x  .  x  x  x  .  x  x  x  .  x  x  x     (bass, 16ths, beat-1 gap)
C: root pulse    x  .  .  .  x  .  .  .  x  .  .  .  x  .  .  .     (sub locked to kick, ducked)
D: fifth accent  .  .  .  .  .  .  .  .  .  .  .  .  x  .  .  .     (the G# in the D#-minor example)
```

Pattern C only works with ducking (§3.3). Pattern A is the safest default for a *focus* product: the
sub never coincides with the kick at all, so no dynamic processing is needed to keep them apart.

### 3.3 How kick and bass share the low end

Four mechanisms, all sourced, in the order the sequencer should apply them:

1. **Tune the kick and the bass to the same note.** "tuning a kick to a note that matches the key of
   your track. This could create a sense that all of the low end works together"
   (`src-izotope-mix-kick-bass.txt`). Same source gives the worked example: a TR-808 kick with "a
   fundamental frequency around 50 Hz, with harmonics multiplying up at 100 Hz and 200 Hz. That places
   it just between G and G# on the scale."
2. **Carve the bass's note out of the kick with a narrow EQ cut.** Attack cuts "around **-4.5 dB at
   around 98 Hz** with a bell-shaped curve… because this will determine the key of the bassline… As
   you can see in the chart, G2's frequency is exactly 98, which is why we scooped out that frequency
   in the kick" (`src-attack-warehouse-rolling-bass.txt`). This is a *computable* rule: cut the kick
   at `f = 440 × 2^((n−69)/12)` for the bass's MIDI note `n`.
3. **Remove the kick's sustain rather than ducking the bass.** Same tutorial: a transient shaper with
   "the Sustain down to -62, while making up for the gain lost by raising the Output to 2.4" — and on
   the sub, "Reducing the attack also technically sidechains the sub to the kick. The sub will now
   duck its initial transient that would have otherwise competed with the kick's."
4. **Only then, sidechain.** "in most cases, it will be better and easier to duck the bass when the
   kick plays" (`src-izotope-mix-kick-bass.txt`). For dub techno specifically, Attack sets the
   compressor's "attack to its fastest setting and reduce the threshold to taste", then **copies that
   same compressor onto every non-kick element** — chords, second chord layer, both percussion
   layers (`src-attack-basic-channel-dub.txt`).

**Numeric sidechain settings (ratio, gain reduction in dB, release ms) were NOT found in any
re-fetchable primary source.** Perplexity offered 3–6 dB GR and 1–10 ms attack citing third-party
blogs; that is recorded in `sonar-bass-lowend.json` and is **unverified**. What *is* verified is the
topology (fast attack, kick as key, applied to everything except the kick) and the fact that the same
compressor instance is reused across parts.

### 3.4 Octave choice

`src-attack-warehouse-rolling-bass.txt` places its bassline "in the key of G within the C2 octave
range", with the sub low-passed at 80 Hz below it. Translating to this product's measured envelope:
ref01 puts 27.6 % of its energy below 60 Hz and 21.2 % in 60–150 Hz
(`research/ear-test/spec-from-references.md`), i.e. sub fundamental in the **A1/A0 region (55 Hz or
27.5 Hz doubled)** and the bass body an octave up. The repo's own renderer already uses root 55 Hz
with layers at 110 Hz and 165 Hz (`research/ear-test/synth-arm-2026-09-02.md`), and that arrangement
is what moved the 150–500 Hz body share from 3–12 % (ElevenLabs arm) to 46–54 % (synth arm).

## 4. Chords and stabs

### 4.1 Voicing

- **One minor chord, held for the whole track.** Attack's Basic Channel walkthrough pitches a chord
  sample "down -7 tones – this will get us an D♯ minor chord" and never changes it
  (`src-attack-basic-channel-dub.txt`).
- **Instrument lineage.** "The Basic Channel guys are notoriously tight-lipped about the gear they
  used, but the general consensus has it that they employed a **Sequential Circuits Prophet-5**"
  (`src-attack-dub-techno-synth-chords.txt`). Attack accordingly programs the sound on a Jupiter-6
  init patch as the nearest analogue-modelling starting point.
- **Stab length: one 16th.** "Shorten the chords to make them each last only one 16th-note and
  experiment with different rhythms. Make sure to **emphasize hits that don't occur on downbeats to
  introduce syncopation**" (`src-attack-parallel-chord-stabs.txt`).
- **Parallel movement is the genre's harmonic device — and this product should decline it.** Attack
  documents shifting a fixed chord shape up and down by fixed intervals ("all chords need to have the
  same shape (inversions)", `src-attack-parallel-chord-stabs.txt`). That is a *change* event; the
  brief forbids it. Recorded here so the sequencer's author knows what is being deliberately left out.

### 4.2 The full Attack dub-chord recipe, with its numbers

All from `src-attack-dub-techno-synth-chords.txt` (Adam Douglas, 9 March 2021), programmed on u-he
Diva. Values are Diva's own 0–100 scales unless a unit is given.

| Stage | Setting | Verbatim |
|---|---|---|
| Osc | noise circuit **on** in VCO 1 | "This will add a chuff to the notes and **give the delays something to grab onto**" |
| Osc | saw + square on VCO 2, pulse width **~70**, osc mix at 2 o'clock favouring VCO 2 | "Let's use pulse width to thin out our square wave" |
| Filter | **high-pass**, cutoff **80**, resonance **~20** | "We won't be using the lowpass filter but the highpass as we want a sound that is thin and airy, one that will float above the sub-bass" |
| Filter mod | LFO 2 → cutoff at 1 o'clock; LFO rate 1 o'clock, depth mod 9 o'clock | "Let's add some movement to the filter" |
| Amp env | A **11**, D **35**, S **8–15** | "This may seem short but don't worry, **all of the echoes will fill it out**" |
| Filter env | A **80**, S **90** | "This will give our filter envelope a **slow onset – key to getting the sound right**" |
| Keyboard follow | **65** | — |
| EQ | **−7 dB at 600 Hz, wide Q**; HP below **100 Hz**; LP above **4.5 kHz** | "Synth chords in dub techno have a **particularly hollow sound** to them. We need to scoop out the mids" |
| Tape echo | RE-201 emulation, "Dub" preset, its own reverb off | — |
| Send filter | high-pass shelf at **280 Hz**, very low resonance, LFO amount **22**, rate **0.25 Hz** | "This is going to create some movement in the delay channel" |
| Send delay tap 1 | **1/8 dotted**, feedback **~20 %** | — |
| Send delay tap 2 | **free-running 264 ms**, feedback **~85 %** | — |
| Send level | 100 % from the chord channel | "we want very prominent delays" |

**Two things in that table deserve to be read as design rules, not settings.** First, the chord is
**high-passed, not low-passed** — the low-pass instinct is wrong here; the sound is thinned so it can
"float above the sub-bass", and the darkness comes from the −7 dB mid scoop and the 4.5 kHz ceiling.
Second, the **short amplitude envelope is deliberate because the delay supplies the sustain**. A code
sequencer that lengthens the chord envelope to make it sound fuller is undoing the mechanism.

Attack's *other* dub-chord approach (`src-attack-basic-channel-dub.txt`) reaches the same place from a
sample: bit-reduce a chord one-shot to 6 bits, then rescue it with a **band-pass filter, 12 dB/oct
slope, cutoff around 450 Hz**, plus "LFO amount to around 10 with a slow rate to add a little more
movement". "In bandpass mode, moving the cutoff greatly changes the character of the sound and if this
is done with a slightly higher resonance the result is new textures that sound great when run through
dub-style delays."

### 4.3 How the chord "breathes"

The breathing is **two slow modulators plus the delay**, not a single sweep:

1. LFO on the synth's own filter cutoff (Diva LFO 2, rate ~1 o'clock).
2. A **second, much slower** LFO on the *send channel's* filter — **0.25 Hz**, i.e. a 4-second cycle,
   amount 22 (`src-attack-dub-techno-synth-chords.txt`). This modulates the echoes, not the source.
3. Long-form automation of the cutoff on top of both — "some filter cutoff automation" in the same
   article; Attack's stab tutorial recommends automating "the Filter Cutoff, Reverb and Auto Pan
   macros" and adds "We recommend doing extended automation takes live and then choose your best
   moments" (`src-attack-parallel-chord-stabs.txt`).

For a code sequencer: three modulators of clearly separated period (audio-rate-ish LFO, ~4 s LFO,
minutes-long drift), each with an independent phase, so they never line up into a "section". That is
already the repo's approach (`research/ear-test/synth-arm-2026-09-02.md`), and the measured shortfall
there — slow-centroid CV 0.29–0.34 against the references' 0.41–0.46 — is a *depth* problem, not a
topology problem.

## 5. Motifs and hooks — what makes a phrase hypnotic

The strongest evidence in this whole file is a single sentence from Richie Hawtin, describing his own
method (`src-rbma-hawtin-2014.txt`, Red Bull Music Academy lecture, 2014):

> "I like just adding these little notes around and letting the delays and the interplays between the
> delays and the reverbs really open up space that people can climb into and dance around with their
> feet and also in their mind."

The note count is small; the *rhythm* is manufactured by the echoes. Three corroborating sources:

- **The delay is the rhythm section.** "one of the hallmarks of dub techno is groove and movement
  resulting from delay instead of heavily swung drum parts" (`src-attack-basic-channel-dub.txt`).
- **The material must be echo-friendly by design.** The noise circuit is switched on specifically to
  "give the delays something to grab onto" (`src-attack-dub-techno-synth-chords.txt`).
- **Moritz von Oswald on the resulting state** (`src-rbma-moritz-von-oswald.txt`, RBMA 2008):
  > "We used patterns that weren't really defined, but they work with each other and are constantly
  > changing. It's a state where the music is **not moving, just kept like a Polaroid**, in a way,
  > where you have something going on rhythmically, but it actually stands still at the same time."

  and on why the elements stay few: "leaving some space for the six or eight elements that are working
  together really well… if it's put together very well, you can bring out that small number of
  elements and play with them."

**Encodable definition of "hypnotic", derived from those four statements:**

| Property | Value |
|---|---|
| Distinct pitches in the motif | **2–3**, one key, no runs, no arpeggios |
| Notes actually triggered per bar | **1–2** (the rest of the density is echo) |
| Repetition period of the motif | 1 or 2 bars, unchanged for ≥ 32 bars |
| Rhythm-generating mechanism | **delay**, not extra notes |
| Element count in the whole track | 6–8 (von Oswald's number) |

**Delay-generated polyrhythm, the mechanism in numbers (derived).** A dotted-8th delay is 3/16 long.
Against a 16-step bar, a repeat chain from a single note on step 1 lands on steps 1, 4, 7, 10, 13,
16 — then 3, 6, 9, 12, 15 in bar 2 — and only realigns with the downbeat after **3 bars**. One
trigger, an emergent 3-against-4 pattern lasting 48 steps, zero extra sequencing. This is why dotted
eighths dominate the genre and why Attack keeps reaching for them (Echo "on a 1/8 dotted delay",
`src-attack-basic-channel-dub.txt`; "dotted eighth notes are great for dub",
`src-attack-creating-dub-delays.txt`; "subtle dotted eighth note delay",
`src-musicradar-minimal-groove.txt`).

A **5/16** delay does the same thing with a longer cycle: it realigns after 5 bars. Attack uses
exactly that on its second chord layer — "add some 5/16 echoes via Live's Delay"
(`src-attack-basic-channel-dub.txt`). **Running one element on 3/16 and another on 5/16 gives a
combined realignment period of 15 bars from two constants.**

## 6. Delay and reverb timing math

### 6.1 The formula

"60,000 ms (1 minute) / Tempo (BPM) = Delay Time in ms for quarter-note beats"
(`src-sengpiel-bpm-delay.txt`). Everything else is that beat times the note's fraction of a beat.

### 6.2 Table for this product's tempo window (derived from the formula above)

Milliseconds, rounded to 0.1.

| BPM | 1/4 | 1/8 | **dotted 1/8 (3/16)** | 1/8 triplet | 1/16 | dotted 1/16 | **5/16** | 1 bar |
|---|---|---|---|---|---|---|---|---|
| 114.0 | 526.3 | 263.2 | **394.7** | 175.4 | 131.6 | 197.4 | **657.9** | 2105.3 |
| 114.8 | 522.6 | 261.3 | **392.0** | 174.2 | 130.7 | 196.0 | **653.3** | 2090.6 |
| 115.0 | 521.7 | 260.9 | **391.3** | 173.9 | 130.4 | 195.7 | **652.2** | 2087.0 |
| 116.0 | 517.2 | 258.6 | **387.9** | 172.4 | 129.3 | 194.0 | **646.6** | 2069.0 |
| 117.0 | 512.8 | 256.4 | **384.6** | 170.9 | 128.2 | 192.3 | **641.0** | 2051.3 |
| 118.0 | 508.5 | 254.2 | **381.4** | 169.5 | 127.1 | 190.7 | **635.6** | 2033.9 |
| 120.0 | 500.0 | 250.0 | **375.0** | 166.7 | 125.0 | 187.5 | **625.0** | 2000.0 |

**Observation worth acting on (derived).** The two "free-running, deliberately not synced" delay times
in the primary sources land almost exactly on this table's tempo window: Attack's second dub-chord tap
is **264 ms**, which is an eighth note at 113.6 BPM (`src-attack-dub-techno-synth-chords.txt`); its
dub-delay demo is **373 ms**, "it sounds wonkier than synced to DAW tempo", which is a dotted eighth
at 120.6 BPM (`src-attack-ultimate-delay-guide.txt`). The technique is not "unsynced" so much as
**synced to a slightly different tempo**. That is trivially encodable: run the second delay tap at
`3/16 × 60000 / (BPM × k)` with `k` ≈ 1.01–1.05, giving a slow phase drift against the grid instead of
a fixed offset — movement with no automation.

### 6.3 Feedback, filtering and routing

| Parameter | Sourced value | Source |
|---|---|---|
| Primary synced tap feedback | **~20 %** | `src-attack-dub-techno-synth-chords.txt` |
| Secondary free tap feedback | **~85 %** | same |
| Send delay before adding external feedback | **~30 %** ("We don't need much, as we'll be adding our own feedback later") | `src-attack-creating-dub-delays.txt` |
| BBD-style analogue delay feedback | **~44** | `src-attack-ultimate-delay-guide.txt` |
| Feedback-path high cut | **~5 kHz** ("Tape naturally rolls off highs… we play it by ear and cut highs around 5kHz") | `src-attack-creating-dub-delays.txt` |
| Feedback-path low cut | **~200 Hz** ("roll off a little of the low end around 200Hz just to keep it from clashing") | same |
| Send-channel filter on the echoes | HP shelf **280 Hz**, LFO amount 22, rate **0.25 Hz** | `src-attack-dub-techno-synth-chords.txt` |
| Saturation in the feedback path | multiband, low band **disabled**, mix ~50 % | `src-attack-creating-dub-delays.txt` |
| Pitch wobble (wow/flutter) | present, "small, authentic changes", intermittent and irregular | same |
| Safety | limiter at the end of the feedback loop, ceiling 0 dB | same |

**Ping-pong, defined by the source:** "Rather than all of the delays occurring in mono, in a ping-pong
delay the repeats alternate from left to right across the stereo spectrum. This can be a useful way to
add width to a sound" (`src-attack-ultimate-delay-guide.txt`).

**Multi-tap is the dub-techno idiom, not a single delay.** Attack stacks Live's Echo (1/8 dotted)
*followed by* Live's Filter Delay: "To many, Filter Delay is the ultimate dub techno delay as you have
total control over which frequencies of the three delay channels are let through via their individual
filters" (`src-attack-basic-channel-dub.txt`). Encode as ≥ 2 taps, each with its own band-pass.

### 6.4 Reverb

| Parameter | Sourced value | Source |
|---|---|---|
| Reverb after the delay, not before | "Delays sound great when run through a bit of reverb" — Live's Reverb "with a low decay time" placed after both delays | `src-attack-basic-channel-dub.txt` |
| Pre-delay on a techno stab | **~3 ms**, with decay "about the same" | `src-attack-techno-synth-stabs.txt` |
| Reverb type for a dub clap | "shortish reverb… dark chamber patches or even **spring reverb** emulations. Aim for a **decay time which allows the tail to ease into the next kick**" | `src-attack-dark-berlin-techno.txt` |
| Modulated spring on a dub snare | Modnetic "501 Spring", modulation = Phaser/Analog, **rate ~30 %, amount 10 %** | `src-attack-dub-drum-processing.txt` |
| Reverb placement trick | put the reverb **first** in the chain so the distortion after it drives the tail | `src-attack-techno-synth-stabs.txt` |

**"Decay that eases into the next kick" is an encodable rule, not a taste statement.** At 115 BPM one
beat is 521.7 ms; a reverb whose RT60 sits at roughly 0.8–1.5 beats (≈ 420–780 ms) decays into the
next kick without accumulating. Longer numeric reverb decays for dub chords were **not found** in a
re-fetchable primary source (§11).

## 7. Arrangement over time

### 7.1 Phrase lengths

- **8 and 16 bars are the unit.** "Dance music (and most other popular forms of music) tend to be
  arranged in patterns of **eight or 16 bars**… most people have a feel for when something in a song
  is going to change… Start with the kick drum and continue adding new musical elements **every eight
  or 16 bars**" (`src-attack-break-out-of-the-loop.txt`).
- **The loop itself is 4 bars** in the Beat Dissected articles ("a simple variation at the end of the
  four bar loop", `src-attack-dark-berlin-techno.txt`).
- **A deliberately mismatched 3-bar FX sequence** runs against it (`src-musicradar-minimal-groove.txt`,
  §2.2).
- **Optional variation elements are placed at 8/16-bar boundaries:** a vocal stab "you could use this
  one at the end of an 8/16-bar section" (`src-attack-sub-zero-minimal-techno.txt`).

### 7.2 What replaces drops

Hawtin, on a DJ set (`src-rbma-hawtin-2014.txt`):

> "Sometimes I'll have one loop going as a bed loop that I start within the first five minutes of my
> set, and that could be going for **half an hour**. Every time I try to take it away I kind of lose
> this whole foundation of what that set's about."

and on the Plastikman album *Sheet One*, made for the hours after the club:

> "if that clubnight had continued for another two or three hours, if people had finished their energy
> of dancing but still wanted to keep hearing and they were lying on the dancefloor as the sun came
> up, that was kind of the record for them."

and on how his own listening works when material is unfamiliar — a useful negative constraint: "Just
check that there's **nothing random happening in the song**, which you don't want to be too surprised
when you're playing."

Von Oswald, on how long the process is allowed to be (`src-rbma-moritz-von-oswald.txt`): "I like long
pieces, the repetitive patterns and seeing how people treat the few elements that are there… If you're
setting up a track, **give it some time. Listen to it over and over**."

Robert Hood, on naming the thing (`src-gridface-robert-hood.txt`): he nearly called minimal techno
"**access-authorized repetition**. Something repetitive."

### 7.3 Automation timescales

**No primary source found publishes numeric automation lengths in seconds or bars for this genre.**
Perplexity returned "16 bars", "16–32 bars", "cutoff climbs from 400 Hz to 2 kHz across 64 bars"
attributed to third-party blogs (TrackSensei, plugg-supply); those are recorded in
`sonar-arrangement-hypnotic.json` and are **unverified** (§11). What *is* verified from primary
sources is only the shape: one slow send-filter LFO at **0.25 Hz** (4 s), plus long automation takes
recorded live and edited (`src-attack-dub-techno-synth-chords.txt`,
`src-attack-parallel-chord-stabs.txt`).

Derived, and consistent with both the verified LFO and the repo's own measurements: at 115 BPM a bar
is 2.087 s, so **16 bars = 33 s, 32 bars = 67 s, 64 bars = 134 s, 128 bars = 4 min 27 s**. A sweep
that must not read as an "event" needs to be at least the longer end of that.

### 7.4 Translating this to a focus product

The genre wants slow change. A focus product wants change that **never captures attention**. Those are
not the same constraint, and one vendor has published its rationale explicitly. Brain.fm
(`src-brainfm-neuroscience-focus.txt` — **vendor marketing, not peer review**; read it as a statement
of design intent, not evidence):

> "Your brain is biologically wired to track change. A new song section, an unexpected chord, a
> memorable hook — each of these is a **micro-interrupt** that pulls processing resources away from
> your primary task."

> "Brain.fm music is composed to minimize the elements that trigger attentional capture: **no strong
> emotional arcs designed to generate peak moments, no unexpected transitions, no lyrics, no sections
> engineered to be memorable**."

and, on the awkward implication for a product Daniel has to want to listen to:

> "The most pleasurable music tends to be the most attention-capturing. The most neurologically
> effective focus music tends to sound quieter, more ambient, and less immediately interesting — by
> design."

The same page names one specific failure mode that is directly relevant to a *palette-rotation*
product: "the transition between songs — different tempo, different key, different timbre, sometimes a
different genre — is itself a novelty event that reliably breaks concentration." **If palettes rotate,
the rotation must not cross tempo or key**, or it becomes the very event the product exists to avoid.
It also claims a warm-up time — "designed to engage attentional networks within approximately five
minutes of listening" — which argues for long unbroken sessions over short clips.

Peer-reviewed grounding for the underlying mechanism (involuntary attention capture by acoustic
deviants: mismatch negativity, novelty-P3, reorienting negativity) was identified by the Perplexity
pass — Escera & Corral 2007 — but **the PDF timed out on fetch and was not verified**; see §11.

**Encodable focus constraints, derived from the above plus the repo's own measurements:**

| Constraint | Value | Basis |
|---|---|---|
| Loudness range over a session | **LRA ≤ 4 LU** | both references measured 4.1 LU (`research/ear-test/spec-from-references.md`) |
| Event density | **≤ ~400 onsets/min** | ref01 393, ref02 346, same file |
| Tempo change within a session | **none** | Brain.fm transition claim |
| Key change within a session | **none** | brief + Brain.fm transition claim |
| Fastest structural change | nothing shorter than **~2 minutes** end-to-end | derived from §7.3 (64 bars ≈ 134 s) |
| Element entries/exits | at 16/32-bar boundaries, **one element at a time**, cross-faded over ≥ 8 bars | derived from §7.1 |
| Session length | ≥ 30 min unbroken, ideally matching Daniel's 3.5 h and 5 h blocks (`research/ear-test/palettes.md`) | Brain.fm 5-min warm-up claim |

## 8. Mix

### 8.1 Level relationships

**Numeric level relationships between kick, bass, chords and hats in dB were NOT found in any
re-fetchable primary source.** This is a real gap, and it is recorded as such rather than filled with
a plausible-sounding table (§11).

What replaces it, and is arguably better for a code sequencer, is the repo's own **band-share
target**, which is measurable and already implemented as a bounded least-squares solve in
`synth/render.py`:

| Band | Target share of total power | Basis |
|---|---|---|
| < 60 Hz | ~25 % | ref01 27.6 % |
| 60–150 Hz | ~22 % | ref01 21.2 % |
| **Σ < 150 Hz** | **40–55 %** | ref01 48.8 %, ref02 81.2 %, spec compromise |
| **150–500 Hz (body)** | **15–45 %, and in practice ≥ 45 % is where the synth arm landed** | ref01 46.5 % |
| 500 Hz – 2 kHz | ~4 % | ref01 4.2 % |
| > 2 kHz | **< 0.5 %** | both references |

All from `research/ear-test/spec-from-references.md`.

### 8.2 The 150–500 Hz body region

This is the band the ear-test arm identified as the product's actual weakness, and the primary sources
say something counter-intuitive about it: **it is filled by saturation harmonics and layered
mid-range elements, then selectively carved — never EQ-boosted.**

- Attack, on the kick after overdrive: boosted the low end and made "a small cut around **250 Hz**"
  (`src-attack-thumping-techno.txt`, quoted in `synth-instruments-2026-09-02.md` §5.1).
- A KVR poster reverse-engineering a mid-90s kick: after hard clipping, "eq again … with some **dip
  around 180-200hz and 800-2000hz**" (same).
- Hugh Robjohns, Sound On Sound, on why saturation and not EQ: "**the overall tonality is not, in
  itself, enough to introduce warmth.** If it were, all we'd have to do is modify the frequency
  response of our digital systems appropriately"; the mechanism is "significant **third-harmonic
  distortion on loud low-frequency components**" and it "is **always greatest for low frequencies**"
  (`src-sos-analogue-warmth.txt`, February 2010, quoted in `synth-instruments-2026-09-02.md` §5.1).
- iZotope, on the same band from the mix side: "Removing some low-mids, around **300 Hz**, from a bass
  will allow for more mid-focused instruments … to come into focus"
  (`src-izotope-7-tips-low-end.txt`).

### 8.3 Mono below ~120 Hz

"Sum low-frequency energy toward mono **below roughly 100–150 Hz**. This keeps the groove stable
without collapsing the stereo image of everything above it" — and the reason is physical: on vinyl,
"the centre/mono information is cut laterally (side to side) and the stereo information is cut
vertically… too much vertical movement in the low end can literally lift the stylus out of the groove"
(`src-quantara-master-for-vinyl.txt`; **vendor blog for a mastering tool, not an independent
authority**). No independently authored primary source for the exact crossover was fetched.

For a headphone-first product the vinyl rationale does not apply directly, but the rule survives for a
different reason already measured in this repo: mono lows are what let the band-share solver hit a
target reliably, and ref01 puts ~49 % of its energy under 150 Hz. **House value: mono below 120 Hz**,
the midpoint of the sourced range, applied after the kick/sub bus and before the master.

### 8.4 Where saturation goes

Sourced placements, in signal order:

| Position | What | Source |
|---|---|---|
| On the kick itself | "run through **heavy compression and analogue overdrive** to add character and harmonics" | `src-attack-thumping-techno.txt` |
| Parallel bus on the kick | "routed the signal to a parallel bus and then added a **tape saturation** plugin driven fairly hard… Blend the saturated channel back in" | `src-attack-sub-zero-minimal-techno.txt` |
| On the sub | overdrive at **~35 % dry/wet**, "Make sure that the overdrive does not reduce the low end of the sub!" | `src-attack-warehouse-rolling-bass.txt` |
| On the chord layer | Live's Amp for "grit and distortion", output set to Dual to stay stereo | `src-attack-basic-channel-dub.txt` |
| Inside the delay feedback path | multiband saturation with the **low band switched off** | `src-attack-creating-dub-delays.txt` |
| Across the whole drum rack | Live's Drum Buss, **Boom 8 % at ~37 Hz, Damp ~8.5 kHz** — and, unusually for the series, switched on *before* the rest of the beat was written because "the Drum Buss' saturation and character is crucial to the final sound" | `src-attack-basic-channel-dub.txt` |
| Master | EQ below ~37 Hz removed, limiter to prevent clipping | same |
| Master (peak safety) | limiter ceiling **−0.3 dB** with no added gain | `src-attack-warehouse-rolling-bass.txt` |

---

# PART 2 — Instruments by role, and how to build each in Surge XT

All Surge XT parameter names, ranges and descriptions below are quoted from the official manual at
`https://surge-synthesizer.github.io/manual-xt/`, saved as `src-surge-manual-xt.txt`. Surge XT is
GPLv3, verified in `synth-instruments-2026-09-02.md` §3.3 — which also records the load-bearing
constraint: **GPLv3 makes Surge an offline-render tool for this project, not something shippable
inside a closed app.**

## 9. Roles

### 9.1 Kick and drums

**What defines a 909 kick, in numbers.**

The TR-909 bass drum has four front-panel controls. Roland's own manual describes them only
qualitatively (`src-tr909-owners-manual.txt`): Attack "is to control the attack sound"; Decay "adjusts
the decay time"; Tune "is to control the pitch. Whatever the position this knob is set, the Decay knob
works at its set time".

The one hard number found comes from Colin Fraser's circuit analysis of the 909 bass-drum board
(`src-colinfraser-909-mods.txt`):

> "The **Tune control is really a decay control for a simple envelope generator that provides the
> initial falling pitch sweep** on the bass drum oscillator (ENV 3). The standard range is very narrow
> — **from around 30 to 120 milliseconds**."

So: TUNE is *not* a pitch knob, it is the **pitch-sweep decay time, 30–120 ms**. The same page
confirms the amplitude envelope is a separate capacitor discharge (ENV 1) controlling a VCA, and that
the stock sweep depth is a fixed amount set by a resistor ratio.

Sound On Sound's synthesis breakdown gives the topology (`src-sos-practical-bass-drum.txt`): "the
oscillator produces a sawtooth wave whose pitch is defined by EG3, which has an instant Attack and
slow Decay. The output from the oscillator then passes through a waveshaper. **This removes almost all
the overtones, transforming the sawtooth into something very close to a sine wave.** This in turn
passes through a VCA controlled by another contour generator (EG1)". And on the click: because the
amp envelope's attack is zero, "the VCA creates a discontinuity at the start of the sound… this
discontinuity contains (or more properly *is*) a very short burst of high-frequency noise, and it's
this that produces a click". **The click is free — do not synthesise it separately unless you have
smoothed the attack.**

808 vs 909, from the same SOS article: the 808 bass drum is a **self-damping resonant oscillator**
excited by a trigger, not an oscillator-plus-envelope — "The Trigger kicks the oscillator into life…
some of the Trigger+Accent signal… is added into the audio signal path to emulate the beater hitting
the membrane" — and, crucially, "**the TR808 kick drum oscillator goes slightly flat at long decays**,
which is exactly what's required to make the patch sound convincing".

**Surge XT recipe — kick.**

| Element | Surge XT |
|---|---|
| Body | Oscillator type **Sine** (or Classic with shape at full sine), pitch modulated by a fast envelope |
| Pitch sweep | An envelope (or the filter EG routed to Osc pitch) with **attack 0, decay 30–120 ms**, depth ≈ 1.5 octaves (158 Hz → 55 Hz in the repo's own renderer) |
| Amp | Amp EG attack 0, decay 250–800 ms, sustain 0 |
| Click | Comes free from the zero attack; if smoothed, add a 1–3 ms noise burst |
| Saturation | **Waveshaper** in the filter block, or the **Bonsai** FX ("combining a highly non-linear bass boost with an emphasis-filtered waveshaper", Input Gain −24…+24 dB, Bass Boost Amount −24…+24 dB, Distort 0–100 %) |
| Body resonances | second filter as **Comb +** ("plays back the original signal with a delay"; at sub-type 2 with resonance 0 % it is a pure sub-sample-precision delay unit) |
| 808 variant | Vintage Ladder self-oscillating with the envelope on cutoff — reproduces the SOS "oscillating filter as the drum" approach; add a slow downward pitch drift for the "goes slightly flat at long decays" behaviour |

**Note on the licence-clean alternative, already verified in this repo:** Faust's `sy.kick(pitch,
click, attack, decay, drive, gate)` is LGPL-2.1 with an output exception and rendered on this machine
at ~2,400× realtime with no plugin installed (`synth-instruments-2026-09-02.md` §3.1). Its `drive`
parameter is the saturation stage §8.4 requires. **For a shipped app this is the better path; Surge is
the studio/prototyping path.**

**Hats and claps.** Sourced processing rather than synthesis: hats layered from two samples, one
"loose, brushy… almost like a shaker", one "tight, snappy"
(`src-attack-sub-zero-minimal-techno.txt`); the clap layer for a dub snare is pitched up, bit-crushed,
and "EQ to cut the lows until about **150 Hz**" (`src-attack-basic-channel-dub.txt`); hats need "an EQ
to cut the unnecessary low frequencies while boosting the top end… it's important that the hat's more
airy frequencies cut through" (same). In Surge: **S&H Noise** oscillator or **Noise** into a
high-passed band-pass, very short decay, plus the **Waveshaper FX** with its Low Cut (pre) engaged
(13.75 Hz – 25 kHz).

### 9.2 Sub and bass

Reference instruments and their topology:

- **SH-101 / TB-303**: saw or square through a resonant low-pass. Faust's equivalent is `sy.dubDub`,
  "a simple synth based on a sawtooth wave filtered by a resonant lowpass"
  (`synth-instruments-2026-09-02.md` §3.2). Sound On Sound's SH-101 bass-drum patch confirms the
  filter self-oscillates: "we again set the VCF resonance to maximum, the cutoff frequency to minimum,
  and… the 'VCF Env' amount to about **60 percent**… the Decay and Release settings are in the region
  of '6'" (`src-sos-practical-bass-drum.txt`).
- **What the source says about bass oscillators for this genre:** "**Saw or square waves with a fast
  attack or a fast filter envelope work best** for this type of sound. The transients need to be
  audible!" (`src-attack-warehouse-rolling-bass.txt`).
- **The 303 used slowly, with low resonance** is the brief's requirement; Open303 (MIT, C++, no Python
  binding) is the licence-clean implementation, per `synth-instruments-2026-09-02.md` §3.2.

**Surge XT recipe — sub.** Oscillator **Sine** at the root, one voice, no detune → **Waveshaper**
(tanh-like shape) for the third-harmonic content SOS says carries low-frequency warmth → low-pass at
80 Hz for the pure sub layer. For the audible bass layer, a second scene: **Classic** oscillator, saw,
unison 1–2 voices, into **Vintage Ladder** ("4-pole ladder filter… stable self-oscillation") with
cutoff 200–600 Hz and resonance low.

**Surge XT recipe — 303-style, used slowly.** **Classic** oscillator on square, **Diode Ladder**
("4-pole diode ladder filter… does not self-oscillate without feedback") — the non-self-oscillating
behaviour is what keeps low-resonance 303 lines from squealing. Filter EG decay long (this is the
"used slowly" part), envelope-to-cutoff modest.

**Moog-style / Juno bass.** **OB-Xd 24 dB** ("4-pole filters… based on the filters found in the
Oberheim OB-Xa") or **Legacy Ladder** for the cheaper CPU path.

### 9.3 Chords, stabs and pads

The sourced lineage is **Prophet-5** ("the general consensus has it that they employed a Sequential
Circuits Prophet-5", `src-attack-dub-techno-synth-chords.txt`), programmed by Attack on a Jupiter-6
init patch. Juno-106/60, Polysix, JX-3P and JP-8000 were named in the brief but **no primary source
tying any of them specifically to dub-techno stabs was fetched — see §11.**

**Surge XT recipe — the Attack dub chord, port of §4.2.**

| Attack's Diva setting | Surge XT equivalent |
|---|---|
| VCO 1 noise circuit on | Oscillator 2 = **Noise**, mixed low (this is the "give the delays something to grab onto" layer — do not omit it) |
| VCO 2 saw + square, PW ~70 | Oscillator 1 = **Classic**, Shape between saw and pulse, Width ~70 % |
| High-pass, cutoff 80, res 20 | Filter 1 = **K35 Highpass** ("12 dB/Octave filters… inspired by the Korg MS-20 filter topology") or OB-Xd 12 dB Highpass; resonance low |
| LFO 2 → cutoff, slow | Scene LFO, **Sine**, rate ~0.5–2 Hz, routed to Filter 1 Cutoff, small depth |
| Amp env A 11 / D 35 / S 8–15 | Amp EG: short attack, ~200–400 ms decay, sustain ~10 % |
| Filter env A 80 (slow onset) | Filter EG attack **long** — this is the single most characteristic setting in the patch |
| Phaser (Small Stone-like) | FX = **Phaser** |
| Plate reverb, low wet | FX = **Reverb 2** ("more natural and contains less digital artifacts"), Mix low |
| EQ −7 dB @ 600 Hz, HP 100, LP 4.5 k | FX = **EQ** or **Graphic EQ** |
| RE-201 tape echo | FX = **Tape** (Chow Tape Model port: Drive, Saturation, Bias, Speed 1–50 ips, Gap 0.1–20 µm) → **Delay** |
| Send auto-filter HP 280 Hz, LFO 0.25 Hz | second scene's filter with an LFO at **0.25 Hz**, or the Delay's own Low-cut modulated |

**Chorus for Juno-style width.** Surge's **Ensemble** is the correct choice, not **Chorus**: it is
"based on **BBD (bucket-brigade device) delay lines**", exactly the Juno's technology, with **Delay
Type "128 .. 4096 BBD Stages"**, **Clock Rate 1.5 kHz – 100 kHz**, **Saturation 0–100 %** and two
independent modulation frequencies (0.01–20 Hz) and depths. Surge's **Chorus** is a clean 4-stage
digital algorithm (Rate 0.008–512 Hz, Time 0–0.125 s, Feedback −inf…0 dB) — use it when you want width
without BBD colour.

### 9.4 Motif and lead

The brief asks how the motif stays **distant**. The sources answer it four ways, none of which is
"turn it down":

1. **High-pass, don't low-pass.** The dub chord is high-passed at 80 with resonance so it is "thin and
   airy, one that will float above the sub-bass" (`src-attack-dub-techno-synth-chords.txt`).
2. **Scoop the mids.** −7 dB at 600 Hz with a wide Q, "particularly hollow sound" (same).
3. **Cap the top.** Low-pass everything above 4.5 kHz (same). Both this repo's references keep
   > 2 kHz under 0.5 % of total energy (`research/ear-test/spec-from-references.md`).
4. **Let the delay be most of what you hear.** Send at 100 %, source envelope short (same).

**Surge XT recipe — motif.** **Classic** or **Sine** oscillator, 2–3 notes only; **Comb +** as the
second filter to add a metallic resonance without adding notes; FX chain **Waveshaper (light) → Delay
(dotted 1/8, feedback ~20 %, Low-cut 200 Hz, High-cut 5 kHz) → Reverb 2**. Surge's Delay has exactly
the two controls the tape-emulation recipe needs — "**Low/High-cut** — EQ controls of the delayed
signal, 14 Hz .. 25 kHz" — plus **Crossfeed** (−inf…0 dB), which is how you get ping-pong: set
Feedback low and Crossfeed high.

**MS-20-flavoured motif:** the **K35** filter is Surge's MS-20-topology model — "Increasing resonance
will make them sound dirtier and more aggressive".

**FM / DX7 bell:** Surge's **FM2** — "a single sine carrier is modulated by two sine modulators, whose
ratios to the carrier are always integer… However, **M1/2 Offset lets you offset the modulators
slightly in an absolute fashion, creating an evolving and pleasing detune effect**". That offset is a
free, non-repeating slow drift generator; it belongs in a hypnotic patch. **FM3** for more operators.
The licence-clean FM alternative is Dexed, GPLv3 (`synth-instruments-2026-09-02.md` §3.3).

**Rhodes-ish electric piano:** **String** oscillator (String 1/2 Decay, String 2 Detune, String
Balance) or FM2 with a low modulation index, into Ensemble.

### 9.5 Effects — mapping the classic units to Surge XT

| Classic unit | What it actually is | Surge XT |
|---|---|---|
| **Roland RE-201 Space Echo** | "Its **three evenly spaced heads** produced a wider range of echo effects than typical single-head designs, while an innovative free-running tape system provided superior performance with minimal tape wear. **A spring reverb was also built in**" (`src-roland-re201-product.txt`) | **Tape** → **Delay** (two instances for two taps) → **Spring Reverb**. The three-head behaviour = 2–3 Delay units at 1/16, 1/8 and dotted-1/8 summed |
| Tape saturation / wow & flutter | tape distortion + speed instability | **Tape** — a "port of the **Chow Tape Model**… real-time physical model of a reel-to-reel analog tape machine", with Drive, Saturation, Bias, Tone, Speed (1–50 ips), Gap (0.1–20 µm), Spacing, Thickness, and a **Variance** control |
| Spring reverb | | **Spring Reverb** — "based loosely on the algorithm outlined by Parker (EURASIP 2011)"; Size, **Decay 0.5–4.5 s**, Reflections, Damping, **Spin** ("frequency smearing"), **Chaos** ("random modulation used to excite the springs") |
| **Roland Dimension D SDD-320** | BBD chorus, mono-compatible by design | **Ensemble** (BBD stages, clock rate, saturation) with **Width** and low Mix. **The SDD-320's own specs were not verified — the manual PDF timed out on fetch (§11).** |
| Juno-106/60 chorus | two-mode BBD chorus | **Ensemble**, Delay Type at a low BBD stage count, two modulation frequencies |
| Dub delay with self-oscillating feedback | | **Delay** with Feedback near 0 dB, Low-cut ~200 Hz, High-cut ~5 kHz, **plus a limiter after it** (`src-attack-creating-dub-delays.txt`) — Surge's **Conditioner** ("a simple EQ, stereo image control and a **limiter** built into one unit… applies make-up gain automatically") is the safety net |
| Analogue overdrive on the drum bus | | **Distortion**, **Bonsai**, or **Waveshaper** FX; or the **Airwindows** unit ("an integration of **56 diverse effects** by Chris Johnson") — Airwindows is MIT and therefore the one saturation option here that could also ship inside a closed app (`synth-instruments-2026-09-02.md` §3.4) |
| Granular texture / Clouds | | **Nimbus** — "imports the granular texture effect from Émilie Gillet's Eurorack project" |
| Reverb for dub chords | | **Reverb 2**: Pre-Delay 0–2 s, Room Size −100…100 %, **Decay 0–64 s**, Diffusion, **Buildup** ("how long the reverb takes to come to its peak and how 'smeared' in time the effect is"), Modulation, LF/HF Damping. Buildup + Modulation are the two controls that make a reverb "breathe" |

---

## 10. Rules the sequencer should implement first

The ten highest-leverage rules, each one line, each with a number.

1. **Kick on steps 1/5/9/13, closed hat on 3/7/11/15, clap on step 5 only** — one clap per bar, not two, is the cheapest halving of perceived density (`src-attack-dark-berlin-techno.txt`).
2. **Swing 50–54 %, applied to hats and sparse percussion only, never kick or clap** — offset even 16ths by `(15000/BPM) × (s−50)/50` ms; at 115 BPM, 52 % = 5.2 ms (Attack spec blocks + derived arithmetic).
3. **Route every element except the kick into the delay** — "every sound will get its own Dub Machines plugin except for the kick, as we want this to be the anchor" (`src-attack-dub-drum-processing.txt`).
4. **Dotted-eighth (3/16) delay as the default: 391.3 ms at 115 BPM, feedback ~20 %, plus a second free-running tap at ~264 ms with feedback ~85 %** (`src-attack-dub-techno-synth-chords.txt`, `src-sengpiel-bpm-delay.txt`).
5. **Band-limit the delay feedback path: high-cut ~5 kHz, low-cut ~200 Hz, multiband saturation with the low band disabled, limiter last** (`src-attack-creating-dub-delays.txt`).
6. **The chord is high-passed at ~80 with resonance, scooped −7 dB at 600 Hz, capped at 4.5 kHz, with a short amp envelope and a long filter-envelope attack** — the echoes supply the sustain (`src-attack-dub-techno-synth-chords.txt`).
7. **Cut the kick by ~4.5 dB with a bell at the bass note's fundamental** (`f = 440 × 2^((n−69)/12)`; 98 Hz for G2) and leave the first 16th of every beat empty in the bass part (`src-attack-warehouse-rolling-bass.txt`).
8. **Give every sparse element a bar-period coprime with the main loop — 3 against 4, 5 against 8** — one integer buys minutes of non-repeating placement with no randomness (`src-musicradar-minimal-groove.txt`).
9. **Three modulators at separated timescales — ~1 Hz on the source filter, 0.25 Hz on the send filter, and a ≥ 2-minute drift — each on its own phase so they never align into a section** (`src-attack-dub-techno-synth-chords.txt`; §7.3).
10. **Hold LRA ≤ 4 LU, ≤ 400 onsets/min, mono below 120 Hz, and never change tempo or key within a session** — the transition is itself the attention event the product exists to avoid (`research/ear-test/spec-from-references.md`, `src-brainfm-neuroscience-focus.txt`, `src-quantara-master-for-vinyl.txt`).

---

## 11. Not found, or found but unverified

Claims that could not be confirmed from a re-fetched primary page. **Do not encode these as facts.**

| Claim | Status |
|---|---|
| Numeric MIDI velocity values for accents and ghost notes in this genre | **Not found.** Perplexity returned accents 100–115 / ghosts 40–60 with no re-fetchable attribution (`sonar-drum-grids.json`). |
| Sidechain compressor ratio, gain reduction in dB, release time | **Not found in a primary source.** Perplexity gave 4:1, 1–10 ms attack, 3–6 dB GR citing third-party blogs (`sonar-bass-lowend.json`). Topology (fast attack, kick as key, on everything but the kick) *is* verified. |
| Numeric filter-automation lengths for minimal techno (16/32/64 bars, "400 Hz to 2 kHz across 64 bars") | **Unverified.** From TrackSensei and plugg-supply via Perplexity (`sonar-arrangement-hypnotic.json`), not re-fetched. Only the 0.25 Hz send-filter LFO is primary-sourced. |
| Reverb decay time in seconds for dub-techno chords | **Not found.** Sources give "low decay time", "shortish", and "a decay time which allows the tail to ease into the next kick" — qualitative only. |
| dB level relationships between kick, bass, chords, hats | **Not found.** §8.1 substitutes the repo's own measured band-share targets. |
| The Attack Beat Dissected step grids themselves | **Not readable** — they are images; §2 grids are reconstructed from the articles' prose and marked where derived. |
| Roland Dimension D SDD-320 specifications | **Not verified** — the archive.org manual PDF timed out after 60 s. |
| Escera & Corral (2007) on mismatch negativity and involuntary attention | **Not verified** — the ub.edu PDF timed out after 60 s. §7.4 rests on Brain.fm's own marketing page, which is not peer review. |
| Roland TR-909 official technical specifications page | **Not fetched** — support.roland.com returned **HTTP 403** to this client. |
| Sound On Sound TR-909 review | **Not fetched** — returned **HTTP 410 Gone** (`src-sos-909.txt`, fetched in a prior session). |
| Juno-106/60, Polysix, JX-3P, JP-8000 as *dub-techno* stab instruments specifically | **Not found.** Only the Prophet-5 attribution is sourced, and even that is hedged by Attack as "the general consensus". |
| Any production tutorial written at 112–120 BPM for this genre | **Not found.** All four fetched Beat Dissected articles run 120–145 BPM. |
| Endel's own published material on attention capture | **Not found** in this pass. Perplexity declined to supply URLs rather than fabricate them (`sonar-attention-and-change.json`). |

## 12. Sources fetched for this file

Perplexity `sonar-pro` raw JSON (discovery only, never quoted as evidence):
`sonar-drum-grids.json`, `sonar-dub-chords-delay.json`, `sonar-delay-timing-math.json`,
`sonar-arrangement-hypnotic.json`, `sonar-kick-909-params.json`, `sonar-attention-and-change.json`,
`sonar-bass-lowend.json`, `sonar-hood-minimalism.json`, `sonar-gear-and-mono.json`.

Primary pages, re-fetched and saved with URL + fetch date:

| File | Page |
|---|---|
| `src-attack-basic-channel-dub.txt` | Attack Magazine, *Beat Dissected: Basic Channel-Style Dub Techno* (Aykan Esen, 29 Mar 2021) |
| `src-attack-dark-berlin-techno.txt` | Attack Magazine, *Beat Dissected: Dark Berlin Techno* (12 Nov 2012) |
| `src-attack-sub-zero-minimal-techno.txt` | Attack Magazine, *Beat Dissected: Sub-Zero Minimal Techno* (20 Feb 2013) |
| `src-attack-dub-techno-synth-chords.txt` | Attack Magazine, *Synth Secrets: Dub Techno Synth Chords* (Adam Douglas, 9 Mar 2021) |
| `src-attack-techno-synth-stabs.txt` | Attack Magazine, *Synth Secrets: Techno Synth Stabs* (7 Oct 2019) |
| `src-attack-parallel-chord-stabs.txt` | Attack Magazine, *The Theory Of Techno Parallel Chord Stabs* |
| `src-attack-creating-dub-delays.txt` | Attack Magazine, *Creating Dub Delays With Standard Plugins* (Adam Douglas, 20 Aug 2020) |
| `src-attack-ultimate-delay-guide.txt` | Attack Magazine, *The Ultimate Delay Guide* |
| `src-attack-dub-drum-processing.txt` | Attack Magazine, *Dub-Style Drum Processing For Character And Groove* |
| `src-attack-rhythmic-delay-static-melody.txt` | Attack Magazine, *Adding Rhythmic Delay And Reverb To A Static Melody* |
| `src-attack-warehouse-rolling-bass.txt` | Attack Magazine, *Sculpting Warehouse-Style Rolling Techno Basslines* (Aykan Esen, 31 Jul 2020) |
| `src-attack-break-out-of-the-loop.txt` | Attack Magazine, *4 Ways To Break Out Of The Loop* |
| `src-musicradar-minimal-groove.txt` | MusicRadar / Future Music, *How to create a minimal drum groove in your DAW* (20 Jul 2020) |
| `src-sengpiel-bpm-delay.txt` | sengpielaudio, *BPM tempo and delay to time and frequency calculator* |
| `src-finishmoremusic-dub-delay.txt`, `src-buhraudio-dub-delay.txt` | third-party dub-delay guides (fetched, not quoted) |
| `src-sos-practical-bass-drum.txt` | Sound On Sound, *Practical Bass Drum Synthesis* |
| `src-sos-synthesizing-drums-bass-drum.txt` | Sound On Sound, *Synthesizing Drums: The Bass Drum* |
| `src-tr909-owners-manual.txt` | Roland TR-909 Owner's Manual (archive.org OCR text) |
| `src-colinfraser-909-mods.txt` | Colin Fraser, *909 Bass Drum Mod — Enhanced Version* |
| `src-roland-re201-product.txt`, `src-roland-re201-story.txt` | Roland, RE-201 Space Echo product page and history |
| `src-surge-manual-xt.txt` | Surge XT manual (surge-synthesizer.github.io/manual-xt) |
| `src-ableton-groove-manual.txt` | Ableton Live 12 manual, *Using Grooves* |
| `src-izotope-mix-kick-bass.txt`, `src-izotope-7-tips-low-end.txt` | iZotope, mixing kick and bass / low end |
| `src-quantara-master-for-vinyl.txt` | Quantara, *How to master for vinyl* (vendor blog) |
| `src-brainfm-neuroscience-focus.txt`, `src-brainfm-lyrics-focus.txt` | Brain.fm blog (vendor marketing) |
| `src-rbma-hawtin-2014.txt` | Red Bull Music Academy, Richie Hawtin lecture (2014) |
| `src-rbma-moritz-von-oswald.txt` | Red Bull Music Academy, Moritz von Oswald lecture (2008) |
| `src-gridface-robert-hood.txt` | Gridface, Robert Hood interview |
| `src-quietus-robert-hood.txt` | The Quietus, Robert Hood discography interview |
| `src-mvo-selftitled-interview.txt` | Self-Titled, Moritz von Oswald interview |

Also relied on, from earlier passes in this directory: `src-attack-thumping-techno.txt`,
`src-sos-analogue-warmth.txt`, `src-kvr-mid90s-kick.txt`, `src-hn-synth-comments.txt`,
`src-faust-synths-lib.txt`, `src-surge-license.txt` — all quoted via
`synth-instruments-2026-09-02.md` §3 and §5, where their verbatim text is already recorded.
