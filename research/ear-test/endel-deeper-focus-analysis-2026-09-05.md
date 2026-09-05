# ref02 teardown — Endel "Deeper Focus" (Plastikman stems), 2026-09-05

Source: `~/Documents/AI Agent Outputs/Artifacts/flow-audio-references/ref02-endel-deeper-focus-iphone-screenrec.m4a`
— 7:47, AAC 44.1 kHz stereo, iPhone screen recording. **Copyrighted study material.** Never uploaded,
never fed to a generator, never copied into this repo. Working audio and stems live in
`~/Documents/AI Agent Outputs/Artifacts/flow-audio-references/endel-analysis/` (uncommitted).

Method: `research/ear-test/analyse-endel.py`, reusing the conventions of `measure-clips.py` —
**band shares are power-domain** (a 60 Hz sine carries far more energy than an equally loud hat, so
compare rows to rows, never to an intuition about brightness), **LRA is the honest constancy figure**,
and the iPhone capture rolls off the sub so **absolute sub level is untrustworthy**. Stems: htdemucs
4-stem. Full numbers: `endel-analysis/results.json`. Plots: `research/ear-test/plots/endel/`.

**I cannot hear. Every statement below is a number or arithmetic on one.** Each claim in the rebuild
brief is tagged `[measured]` or `[inferred]`.

---

## (a) Summary in plain English

1. It is a **seven-and-a-half-minute loop at 120.2 BPM that essentially never changes** — one bar is
   2.00 seconds, and the same bar repeats about 234 times.
2. There are really only **three layers**: a kick, a bass, and one pad/chord layer. A fourth stem came
   back as near-silence.
3. The **kick hits on every beat** — four-to-the-floor, 919 hits, spaced 0.4992 s apart with almost no
   variation. It is tuned to **C2 (66 Hz)** and rings for about **370 ms**, so it is nearly gapless.
4. The **bass is not a drone and not kick-tied — it is a two-note see-saw**. It alternates between two
   notes every half-bar (every 2 beats), holding an **E2 pedal** against a partner note.
5. That partner note is the only thing in the whole track that changes: **D2 for the first 20 bars,
   then C2 for about 75 bars, then G2 for the rest**, resolving onto a held **C2** at the end.
6. The bass **level barely moves at all** — 97 % of every second sits within 3 dB of its own median.
   The movement is in pitch, not volume.
7. The **pad is the thing that moves.** Its brightness sweeps up and down by about **1.65 octaves**
   (roughly 1000 Hz to 3150 Hz) and its level swells by about **22 dB**, both on a **4-bar cycle**,
   with slower 8-, 16- and 32-bar arcs layered on top.
8. There is a **tempo-synced echo at the dotted quarter** (0.75 s) — it is the single strongest repeat
   in the track, stronger even than the kick's own beat. That is the classic dub-techno delay.
9. **Almost nothing "happens".** Two brief silences (1 s at 2:17, 2 s at 2:24), three places where the
   kick steps up ~4 dB, one extra element that fades in for 50 s around 6:00, and an outro from 6:55
   where the kick pulls back and the bass comes forward. That is the entire arrangement.
10. It is **very dark and very bass-heavy**: 81 % of all energy sits below 150 Hz and only 0.08 % above
    2 kHz. Note the sub caveat — the phone capture may be hiding what is under 60 Hz.

---

## (b) Tables

### Global

| | value | note |
|---|---|---|
| Duration | 467.4 s (7:47) | |
| **Tempo (settled)** | **120.19 BPM** | from kick inter-onset intervals, see below |
| Bar length | 1.997 s | 4/4 assumed |
| Beat length | 0.4992 s | |
| Root / pitch set | **C**, set = C D E G B | chroma rank C(0.99) C#(0.61) D(0.56) E(0.51) B(0.45) |
| Integrated loudness | −14.9 LUFS | from spec-from-references.md; a phone-playback figure, not a master |
| **LRA** | **4.1 LU** | the transferable constancy number |
| Onsets / min | 346 | |

**The 120 vs 79.5 vs 161.5 ambiguity is settled at 120.2 BPM**, by three independent measurements
that agree:

| evidence | result |
|---|---|
| Kick inter-onset intervals (drums stem, low-passed, envelope peak-picking) | 919 onsets, **median gap 0.4992 s**; 889 of 919 gaps fall in 0.49–0.51 s → 120.19 BPM |
| Spacing of high-frequency transients | clusters at exact multiples of **0.125 s** (0.125 / 0.25 / 0.375 / 0.5 / 0.625 / 0.75) = a 16th grid at 120 BPM |
| Spacing of the >10 kHz percussive element (164–220 s) | **0.499 s** = exactly one beat |
| librosa tempogram (prior-free) | 120.2 (1.00), 79.5 (0.97), 234.9 (0.92), 246.1 (0.91), 161.5 (0.86) |

The tempogram alone remains weak evidence (peak/median only 3.2, and 79.5 sits at 0.97 relative
strength) — exactly the caveat the spec raised. **The kick IOI settles it and the 16th-grid spacing
confirms it.** 79.5 BPM is a spurious two-thirds relative of 120; 161.5 is not supported by any
onset-interval measurement.

### Click artefacts (screen taps)

| | |
|---|---|
| HF transients found (>4 kHz, ≥14 dB over 4 s running-median floor) | **755** |
| …of those, sitting on the musical grid | **747 (98.9 %)** |
| **Candidate taps (off-grid)** | **8** |
| Audio excluded (±150 ms each) | 2.4 s = **0.50 %** |

Timestamps: **16.73, 93.84, 431.16, 431.39, 432.69, 438.09, 446.24, 460.76 s.**

**Confidence: low-to-moderate, and the negative result is the more useful finding.** The naive
approach the brief suggested — "energy above 4 kHz where the music has almost none" — returns 755
events and is unusable, because the music *does* have HF percussive content: a per-bar tick on a
2.000 s grid around 97–157 s, and a per-beat element above 10 kHz from 164–220 s. What separates taps
from music here is **rhythm, not spectrum**: a musical element has a partner at a whole multiple of a
16th note; a fingertip does not. Applying that test leaves 8 events.

Reasons for caution: (i) the 8 survivors are **weak** — 14–21 dB over the local floor, against 25–36 dB
for the confirmed musical transients — so they may be low-level musical variation rather than taps;
(ii) six of the eight fall in the **last 36 seconds** (431–461 s) and one at 16.7 s, which is exactly
where you would expect a person to start and stop a recording, and that pattern is the strongest
argument that they are real; (iii) an iOS screen recording captures app audio only unless the mic is
enabled, so whether physical taps could be present at all is unknown to me. **Excluding them changes
nothing material** — 0.5 % of the audio, and every headline number is unchanged with or without them.

### Per stem (htdemucs)

Demucs labels are **not musical truth** — per `lyria-stems-2026-09-02.md`, it files the sub under
`drums` and its `bass` is really the 60–150 Hz body. That holds here.

| stem | RMS dBFS | % of mix energy | <60 Hz | 60–150 | 150–500 | 0.5–2 k | 2–8 k | centroid |
|---|---|---|---|---|---|---|---|---|
| drums | −18.0 | **61.2 %** | 4.7 % | **78.9 %** | 15.1 % | 1.2 % | 0.04 % | 1096 Hz |
| bass | −22.2 | 23.5 % | 4.3 % | **86.9 %** | 7.0 % | 1.8 % | 0.04 % | 506 Hz |
| other | −30.6 | **3.4 %** | 0.3 % | 5.9 % | **45.1 %** | **48.3 %** | 0.43 % | 1728 Hz |
| vocals | −50.6 | 0.03 % | 0.05 % | 0.2 % | 99.4 % | 0.3 % | 0.03 % | 5022 Hz |
| **mix** | | | **4.5 %** | **76.7 %** | **14.7 %** | **4.0 %** | **0.07 %** | 788 Hz |

Same shape as the Lyria finding: the pad layer is a **tiny fraction of total energy (3.4 %)** yet owns
the entire midrange — it is the only thing living in 150 Hz–2 kHz.

### Arrangement (8-bar blocks, dB relative to that stem's loudest block)

Full 29-row table is in `results.json`; this is the shape.

| bars | time | drums | bass | other | what the numbers say |
|---|---|---|---|---|---|
| 1–16 | 0:00–0:32 | −4.6 | −3.9 | −3.4 → −6.1 | full bed from bar 1, no intro fade |
| 17–48 | 0:32–1:36 | −4.4 | −3.8 | −10.8 → −14.5 | pad recedes |
| 49–56 | 1:36–1:52 | **−0.8** | −3.7 | −20.9 | kick steps up ~4 dB, pad nearly gone |
| 65–80 | 2:08–2:40 | −5.4 → **−16.6** | −4.4 → **−19.0** | −9.7 → −17.0 | **the two silences land here** |
| 81–112 | 2:40–3:44 | −4.5 | −3.6 | −11.4 → −1.6 | pad climbs back to near-peak |
| 113–120 | 3:44–4:00 | **0.0** | −3.4 | −2.5 | loudest kick block |
| 129–176 | 4:16–5:52 | −4.5 | −3.8 | 0.0 → −5.6 | pad at its loudest, then eases |
| 177–184 | 5:52–6:07 | **0.0** | −3.7 | −19.3 | kick up, pad out |
| 185–208 | 6:07–6:55 | −4.7 | −3.6 | −9.9 → −2.5 | pad returns |
| 209–232 | 6:55–7:43 | **−14.3 → −7.6** | **0.0 → −0.9** | −14.1 → −23.0 | **outro: kick drops, bass comes forward** |

Drums and bass sit at **−18.6 and −22.9 dBFS for 26 of 29 blocks** — a spread of well under 1 dB
across nearly seven minutes. That is what LRA 4.1 LU looks like from the inside.

**Discrete events — the complete list:**

| time | bars | event |
|---|---|---|
| 136.75–137.75 s | ~69.5–70.0 | **1.00 s near-silence** (>25 dB below median) |
| 144.00–148.00 s | ~73.1–75.1 | **4.00 s near-silence** |
| 95.8–111.8 s | 49–56 | kick +4 dB |
| 223.6–239.6 s | 113–120 | kick +4 dB |
| 351.4–367.4 s | 177–184 | kick +4 dB |
| 358–408 s | 180–205 | `vocals` stem rises from −85 to **−34 dBFS** — a distinct extra element for ~50 s |
| 415.3 s → end | 209–232 | outro: drums −14 dB, bass to its loudest, pad chopped into ~8 s bursts |

Both silences are **exact durations (1.00 s = half a bar, 4.00 s = 2 bars)**. That regularity argues
they are engine- or app-driven layer swaps rather than random recording dropouts, but I cannot tell
those apart from measurement alone.

### Loop length (self-similarity, MFCC + chroma)

| lag | bars | mean similarity |
|---|---|---|
| 2.0 s | 1.0 | 4.277 |
| 4.0 s | 2.0 | 4.264 |
| 6.0 s | 3.0 | 4.257 |

The headline is not which lag wins — it is that **every lag scores within 0.03 of every other**
(4.25–4.29). The track is almost equally similar to itself at *all* time offsets. There is no
section structure for the matrix to find. **The loop is 1 bar; everything above that is modulation,
not arrangement.**

### Hypnotic movement

| | `other` (pad) | `bass` |
|---|---|---|
| Centroid mean | 1726 Hz | 505 Hz |
| Centroid p10 → p90 | 1003 → 3152 Hz | 260 → 669 Hz |
| **Centroid sweep depth** | **1.65 octaves** | 1.37 octaves |
| Centroid slow CV (1 s) | 0.565 | 0.976 |
| Rolloff-85 p10 → p90 | 1150 → 7262 Hz | 213 → 1353 Hz |
| **Dominant centroid period** | **7.66 s = 3.84 bars** (acf 0.61) | 9.61 s (acf 0.22 — weak) |
| Secondary periods | 15.79 s (7.9 bars), 23.82 s (11.9), 19.55 s | 7.71 s (acf 0.22) |
| **AM depth (1 s RMS p10–p90)** | **21.8 dB** | **3.7 dB** |
| **Dominant AM period** | **8.0 s = 4.01 bars** (acf 0.50) | 10.0 s (acf 0.09 — negligible) |
| Secondary AM periods | 24.0 s (12 bars), 16.0 s (8 bars), 32.0 s (16 bars) | — |
| Frames within 3 dB of median | — | **96.6 %** |

**The pad sweeps and swells on a 4-bar cycle.** Filter and amplitude agree: 7.66 s and 8.00 s are one
autocorrelation lag-step apart (dt = 0.46 s), and one bar is 1.997 s, so both are 4 bars. The 8-, 12-
and 16-bar secondaries are the slower arcs riding on top. **The bass does neither** — its AM depth is
3.7 dB against the pad's 21.8 dB, and its modulation autocorrelations are at noise level (0.09–0.22).

### Delay / echo structure (autocorrelation of the onset envelope)

| lag | mix | `other` |
|---|---|---|
| 16th (0.125 s) | 0.416 | 0.388 |
| triplet-8th (0.166 s) | 0.416 | 0.388 |
| dotted-16th (0.187 s) | **−0.095** | **−0.057** |
| 8th (0.250 s) | 0.509 | 0.365 |
| dotted-8th (0.374 s) | 0.470 | 0.468 |
| quarter (0.499 s) | 0.669 | 0.511 |
| **dotted-quarter (0.749 s)** | **0.728** | **0.601** |
| half (0.998 s) | 0.661 | 0.518 |
| bar (1.997 s) | 0.634 | 0.481 |
| 2 bars (3.994 s) | 0.557 | 0.411 |

**The dotted quarter is the strongest lag in the track, beating the quarter note** (0.728 vs 0.669 in
the mix, 0.601 vs 0.511 in the pad). This matters because the quarter-note figure is inflated by the
four-to-the-floor kick — so a lag that *beats* it, and which sits off the kick's own 0.5 s grid, is
strong evidence of a **tempo-synced delay at the dotted quarter (3/8 of a bar, 750 ms)**. It shows up
independently in the raw HF transient spacing (0.745 s, 60 occurrences). The dotted-16th being the
only *negative* correlation in the table is a useful control: the structure is genuinely dotted-quarter,
not a generic "everything correlates" artefact.

### Drums

| | value |
|---|---|
| Kick onsets | 919 over 467 s |
| Median inter-onset | **0.4992 s** (CV 0.132) |
| IOI histogram | 0.50 s ×740, 0.51 ×117, 0.49 ×32, 0.75 ×12, 1.00 ×4 |
| Pattern | **four-to-the-floor** — grid occupancy repeats every 4 steps of 16 |
| 16-step grid | `[59, 82, 48, 41, 61, 83, 45, 41, 59, 81, 49, 41, 60, 82, 46, 41]` |
| **Kick spectral peak** | **65.95 Hz = C2** (long-window FFT; the 64.0 Hz in results.json is bin-limited) |
| **Kick decay to −20 dB** | **369 ms** median (p10–p90: 224–398 ms) |
| Hat band (>4 kHz) RMS | −55.6 dBFS |
| Clap band (1–4 kHz) RMS | −39.7 dBFS |

The 16-step occupancy repeating every 4 steps confirms a hit on every quarter. The apparent smearing
into the neighbouring step (82 vs 59) is phase drift in the grid fit (dev std 36.5 ms), not swing.

**There is no clap and no snare.** The 1–4 kHz band sits at −39.7 dBFS with onsets spread evenly
across all 16 steps (127–166 per step) rather than concentrating on steps 4 and 12 where a backbeat
would be. That flat distribution is the signature of a broadband wash, not a hit. The >4 kHz band is
lower still at −55.6 dBFS. **What HF content exists is a quiet per-bar tick (2.000 s spacing, ~97–157 s)
and a per-beat element above 10 kHz (0.499 s spacing, ~164–220 s)** — not a backbeat.

Because the kick rings 369 ms into a 499 ms gap, it occupies **74 % of every beat**. That, not a
separate bass part, is why 60–150 Hz holds 77 % of the track's energy.

### Bass

Dominant spectral peak per half-bar, 55–140 Hz band:

| note | share of half-bars |
|---|---|
| **E2 (82.1 Hz)** | **43.2 %** |
| C2 (65.9 Hz) | 25.0 % |
| G2 (98.3 Hz) | 23.1 % |
| D2 (72.7 Hz) | 5.3 % |
| B2 (123.8 Hz) | 2.6 % |

**It is a riff, not a drone and not kick-tied.** The note changes between consecutive half-bars
**91.4 % of the time** — a strict two-note alternation at half-bar (2-beat, 1.0 s) rate. Cross-
correlation with the drums stem peaks at only **0.404** (at 0 ms lag), so it is not simply following
the kick.

The pedal note is **E2 throughout**; the partner note is the only long-form change in the track:

| bars | time | pair |
|---|---|---|
| 1–20 | 0:00–0:40 | **E2 ↔ D2** |
| 21–96 | 0:40–3:12 | **E2 ↔ C2** |
| 97–208 | 3:12–6:55 | **E2 ↔ G2** (with C2 recurring) |
| 209–232 | 6:55–7:43 | **C2 held** (88 %), B2 appearing — alternation stops |

Sub vs body split: **6.4 % below 60 Hz, 92.7 % in 60–250 Hz.** Read with the capture caveat.

The pad's own peaks — C3, E3, C4, **D4 (dominant)**, C5, D5, E5, G5 — give the same pitch set,
with a prominent D over a C root, i.e. an added-9th colour.

---

## (c) Rebuild brief

For an Ableton agent. Every claim tagged. Note that all of this describes **one 2-second bar** plus
its modulation; there is no second section to build.

**Session setup** — 120.2 BPM `[measured]`, 4/4 `[inferred]` (assumed by the grid fit; nothing in the
data distinguishes 4/4 from 8/8), key centre **C** `[measured]`, pitch set C D E G B `[measured]`.
Master to about −16 to −14 LUFS with ≥1 dB true-peak headroom, and target **LRA ≤ 4 LU** `[measured
from the reference, though the absolute level is a phone-playback figure, not a master]`.

**Layer 1 — Kick.** One hit on every beat, four-to-the-floor, 919 hits with a median spacing of
0.4992 s and essentially no variation `[measured]`. Tuned to **C2, spectral peak 65.95 Hz**
`[measured]`. It decays to −20 dB in **369 ms** `[measured]`, which is 74 % of the 499 ms beat — so it
is a long, round, nearly gapless kick, not a short click `[measured]`. There is **no transient click
component**: the drums stem holds only 1.2 % of its energy in 0.5–2 kHz and 0.04 % above 2 kHz
`[measured]`. Build it as a sine or triangle body with a pitch envelope settling on C2 and a ~370 ms
amplitude decay, with the top end rolled off hard `[inferred]`. Hold it at a constant level for the
whole track, with three +4 dB lifts at bars 49–56, 113–120 and 177–184 `[measured]`. Effect chain
guess: saturation for body, a low-pass around 200 Hz, no reverb `[inferred from the near-absent
150 Hz–2 kHz content in the drums stem]`.

**Layer 2 — Bass.** A **two-note alternation at half-bar rate** — one note for beats 1–2, the other
for beats 3–4, repeating every bar `[measured: the note changes between consecutive half-bars 91.4 %
of the time]`. Hold **E2 (82.1 Hz)** as the constant pedal `[measured]` and change only its partner:
**D2 for bars 1–20, C2 for bars 21–96, G2 for bars 97–208, then a held C2 from bar 209 to the end**
`[measured]`. Keep the level dead flat — 96.6 % of one-second frames sit within 3 dB of the median,
and its total AM depth is only 3.7 dB `[measured]`. Register is **C2–C3, not C1** `[measured by
long-window FFT; note that pyin on a low-passed signal reported C1–E1, an octave error, and that
figure in results.json should not be used]`. Voice it so the energy lands in **60–150 Hz (86.9 % of
the stem)** with only 4.3 % below 60 Hz `[measured, but the capture rolls off sub so the real mix may
carry more down there]`. Effect chain guess: a simple sine/triangle sub with a little harmonic
saturation for the 60–150 Hz body, gentle sidechain to the kick or none at all — the drums/bass
envelope cross-correlation is only 0.404, so any ducking is mild `[inferred]`.

**Layer 3 — Pad / chord.** This is the layer that carries all the movement, and it is **quiet — 3.4 %
of total energy, −30.6 dBFS** `[measured]`, yet it owns the whole midrange (45.1 % of it in
150–500 Hz, 48.3 % in 500 Hz–2 kHz) `[measured]`. Pitch content: C3, E3, C4, **D4 strongest**, C5,
D5, E5, G5 `[measured]` — so a C-rooted voicing with a prominent added 9th `[inferred]`. Give it two
synchronised modulations, both on a **4-bar cycle** `[measured: centroid period 7.66 s, AM period
8.00 s, bar = 1.997 s]`:

- a **filter sweep of 1.65 octaves**, centroid travelling roughly **1000 Hz → 3150 Hz** and back
  `[measured]`, and
- an **amplitude swell of about 22 dB** `[measured]`.

Layer slower arcs at **8, 12 and 16 bars** on top `[measured: secondary periods 15.79 s, 23.82 s and
32.0 s]`. Effect chain guess: a low-passed saw or wavetable pad into an LFO- or envelope-driven filter
at 1/4 bar-cycle rate, plus an auto-pan or tremolo for the level movement `[inferred]`.

**Layer 4 — The delay, which is a layer in its own right.** Put a **tempo-synced delay at the dotted
quarter (0.749 s, 3/8 of a bar)** on the pad `[measured: it is the strongest autocorrelation lag in
the track at 0.728, beating the quarter note's 0.669, and it shows independently in the raw HF
transient spacing at 0.745 s]`. Feedback high enough that echoes persist across at least two bars
`[inferred from the 2-bar lag still scoring 0.557]`. This is the classic dub-techno delay and is
probably doing more of the perceived "movement" than the pad's own filter `[inferred]`.

**Layer 5 — Percussive HF, very quiet and intermittent.** No clap, no snare `[measured]`. Instead: a
per-bar tick on a 2.000 s grid roughly 1:37–2:37, and a per-beat element above 10 kHz roughly
2:44–3:40 `[measured]`. Both are extremely quiet — the >4 kHz band sits at −55.6 dBFS `[measured]`.
Treat as seasoning, not a groove element `[inferred]`.

**Arrangement.** Build **one 2-second bar** and repeat it ~234 times `[measured: self-similarity is
within 0.03 across every lag from 1 bar to 3 bars, i.e. no section structure exists]`. Then add only:
the three kick lifts; a **1.00 s silence at 2:17** and a **4.00 s silence at 2:24** `[measured]`; an
extra mid-register element fading in for ~50 s from 5:58 `[measured — it appears in Demucs's `vocals`
stem rising from −85 to −34 dBFS, which given the 0.03 % total energy of that stem is almost certainly
a mislabelled instrumental layer rather than a voice]`; and an **outro from 6:55** where the kick drops
14 dB, the bass rises to its loudest of the track, and the pad is chopped into roughly 8-second bursts
`[measured]`.

**What to copy, in one line:** a constant, tuned, long-decay kick on every beat; a flat-level two-note
bass see-saw on an E pedal whose partner note changes every few minutes; and one quiet pad whose
filter and volume breathe on a 4-bar cycle through a dotted-quarter delay `[measured]`. The
hypnotic quality is the **4-bar breathing and the dotted delay**, not any arrangement event
`[inferred, but it is the only movement the measurements find]`.

---

## (d) Caveats

1. **I cannot hear any of this.** No audio playback was available. Every claim is measurement-derived.
   The ear test remains the real test.
2. **This is an iPhone screen recording, not a master.** The −14.9 LUFS integrated and 0.0 dBFS true
   peak from the spec describe the phone's playback chain at whatever volume the device was set to.
   **Absolute sub level is untrustworthy**: 4.5 % below 60 Hz against 76.7 % in 60–150 Hz may be
   Endel's earbud voicing *or* the capture rolling off the bottom, and this measurement cannot tell
   those apart. The kick's C2 fundamental at 66 Hz and the bass's 60–150 Hz concentration are both
   *above* the suspect region, so those are safe; anything I say about what is under 60 Hz is not.
3. **Click detection is a weak positive and a strong negative.** 8 candidate taps at 14–21 dB over
   the local floor, against 25–36 dB for confirmed musical transients — they may not be taps at all.
   The reliable finding is that **747 of 755 HF transients are musical**, and that the brief's
   proposed spectral test does not work on this track because the music has real HF percussion. The
   rhythm test is what separates them. Excluding all 8 changes 0.5 % of the audio and moves no
   headline number.
4. **Demucs labels are not musical truth.** htdemucs is trained on recorded band music. Consistent
   with `lyria-stems-2026-09-02.md`, its `drums` stem here holds the sub (78.9 % in 60–150 Hz) and its
   `bass` stem is really the 60–150 Hz body. The `vocals` stem is 0.03 % of energy and is silence plus
   leakage — except for the 358–408 s window, where it holds a real element that is almost certainly
   a mislabelled instrumental layer. **The three-layer reading is my interpretation of four Demucs
   stems, not a statement about how Endel actually built the track.**
5. **`results.json` contains one figure that should not be used**: `bass.median_hz = 37.8 / D#1` and
   its note histogram. pyin on the low-passed signal locked to subharmonics. The long-window FFT
   peaks (C2/D2/E2/G2) are correct and are what the tables above use. The `kick_spectral_peak_hz` of
   64.0 Hz is likewise bin-limited; 65.95 Hz is the better figure.
6. **4/4 is assumed, not measured.** The kick is isochronous at 0.4992 s; nothing in the data
   establishes where the bar line falls or that bars are four beats long. The bass's half-bar
   alternation is consistent with 4/4 but would equally fit 2/4.
7. **Endel is a generative engine.** This is one 7:47 render of a system that recombines Plastikman
   stems, not a fixed composition. A second capture would very likely differ in the long-form details
   (the partner-note changes, the silences, the outro) while keeping the tempo, register and
   modulation rates. Nothing here should be read as "the track"; it is one instance of the generator.
