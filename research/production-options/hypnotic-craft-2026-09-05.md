# Hypnotic craft — general production knowledge, artist-agnostic

Compiled 2026-09-05. Genre label: **hypnotic minimal techno**.

**Why this file exists.** The two previous passes went deep on one artist (Richie Hawtin / Plastikman)
because a reference track uses his stems. That is too narrow to build a durable skill on. This pass asks
the broad question instead: *how do producers across this whole lane make sound that is hypnotic and
sophisticated rather than primitive?* — and turns the answer into
`.claude/skills/hypnotic-techno-sound-design/SKILL.md`.

**Method.** Discovery: 12 Perplexity `sonar-pro` queries via OpenRouter, raw JSON in
`sources/hypnotic-craft/q1..q12-*.json`. Every kept claim was then re-fetched from its primary page and
saved as `sources/hypnotic-craft/src-*.txt` with URL and fetch date at the top. Claims that could not be
re-fetched are tagged **[unverified]**. My own reasoning is tagged **[agent inference]**. Numbers taken
from our own measurement of the reference are tagged **[measured]**.
Ableton Live was not touched in this run. The reference recording was not fed anywhere.

**Not repeated here** (cited instead): `hypnotic-top-layer-2026-09-05.md` (decorrelated modulators,
band-limiting under 2 kHz, resonant percussion, MCP/tooling limits), `techno-pattern-book-2026-09-02.md`
(drum grids, delay math, loop lengths), `plastikman-endel-sound-2026-09-05.md`,
`endel-deeper-focus-analysis-2026-09-05.md` (the measured Level-1 target).

---

## 1. Plain-language summary

1. **Hypnotic is a design decision, not a mood.** Every producer in this lane says the same thing in
   different words: lock one pattern, then change *how it sounds* instead of *what it plays*.
2. Mike Parker: the music is "centred around a bassline. I will work with a sequencer and I will
   **modulate that until it sounds right**… Sometimes I'll spend more than one day on a single pattern."
3. Jeff Mills, on his method: "My style is mainly of **subtracting, not adding**. Subtracting sound
   away." Tension in this genre comes from taking things out, never from a build-and-drop.
4. Mills also gives a hard number: he and Robert Hood reckoned an unchanged sequence holds a listener
   for about **two and a half to three minutes** before it needs a structural change. **[unverified]**
5. Brian Eno's *Music for Airports* loops were **deliberately not measured** — he wanted "complicated
   rather than simple relationships" between loop lengths. That is exactly our decorrelation rule,
   stated by its inventor in 1985.
6. Rod Modell (Deepchord) records **45–60-minute** takes and edits them down. Long-form hypnotic music
   is *performed and cut*, not *arranged bar by bar*.
7. The single most-repeated sound-design finding: **one LFO on one cutoff is the amateur tell.** Every
   sourced pro patch runs 2–4 modulators at once, on *different destinations* (pitch/sync, filter, pan,
   delay time, drive), often with one modulator modulating another's rate.
8. Attack's own LFO tutorial uses **three LFOs at 10–20 % depth** on three hi-hat volume faders — and
   notes the volume modulation alone "introduces new syncopated patterns." Movement can *be* the rhythm.
9. Micro-timing research says listeners generally don't consciously notice offsets **≤ 30 ms**, and that
   quantised and expertly-humanised versions can be rated equally groovy. Swing is optional; **timbral
   variation is not**.
10. Repetition psychology (Margulis) says the point of the loop is that it **moves the listener's
    attention off "what happens next" and onto timbre and texture** — which is precisely why the top
    layer has to be interesting *as a texture*, not as a melody.
11. Level and band placement matter more than fader position: our measured target is a top layer at
    **~3 % of mix energy, ~12.6 dB under the kick, under 0.5 % of its energy above 2 kHz**.
12. There is exactly one good all-stock Live 12 tutorial in this lane —
    Attack's *Dark Cinematic Hypnotic Techno* — and its real lesson is structural: in a 4-bar loop, most
    elements appear **only in one or two of the four bars**.

---

## 2. Findings per research question

### Q1 — What makes electronic music hypnotic, in producers' own words

**Modulate the pattern, don't rewrite it.** Mike Parker, *TEA with Mike Parker* (Tea & Techno, 2012-04-05,
`src-teaandtechno-mike-parker.txt`, http://teaandtechno.blogspot.com/2012/04/tea-with-mike-parker.html):

> "It's music that is centred around a bassline. I will work with a sequencer and I will modulate that
> until it sounds right… Sometimes I'll spend more than one day on a single pattern. If I take a break
> and come back to it and it is still interesting, then I know it is good."

That is a whole workflow in three sentences: **one pattern, judged by whether it survives repeated
listening**. Parker's method is also entirely performance-based — Red Bull Music Academy, *The Art of
Techno Producer Mike Parker* (`src-rbma-mike-parker.txt`,
https://daily.redbullmusicacademy.com/2015/04/mike-parker-art-feature/):

> "Just like my music, every single track I have ever made is recorded live. I don't use multi tracking,
> I don't use a computer, I don't use the drag and cut/paste, every single track is performed live into
> a mixer and that is it."

**Subtraction, not addition.** Jeff Mills, *The Art of DJing* (RA feature, reproduced at
`src-claudiotechno-jeff-mills-djing.txt`,
https://claudiotechno.wordpress.com/2020/01/01/the-art-of-djing-jeff-mills/):

> "I don't put so much emphasis on adding things together… My style is mainly of subtracting, not
> adding. Subtracting sound away… a mixer that will allow me to hide frequencies the best."

Same source, on where a track's real statement lives:

> "if you produce music, and your track is five minutes long, by the last quarter of the track… you have
> figured out what the track is really about. So the last quarter of the track is typically the best."

**How long an unchanged sequence holds.** Mills, RBMA lecture: he and Robert Hood discussed "in terms of
time, how long it takes for the people to really get excited to listening to the same sequence over and
over again. It was about two-and-a-half to three minutes."
(https://www.redbullmusicacademy.com/lectures/jeff-mills-lecture/) — **[unverified]**, the lecture
transcript could not be re-fetched. Treat 2.5–3 min as an order-of-magnitude, not a law.

**Mixer-as-instrument, in a real teardown.** Attack Magazine, *Deconstructed: Jeff Mills — The Bells*
(`src-attack-jeff-mills-the-bells.txt`,
https://www.attackmagazine.com/technique/deconstructed/jeff-mills-the-bells/): the track "never [has]
more than a few musical elements happening at a time"; rides are **faded in** rather than unmuted; the
lower bell line is brought "in and out almost at random… sometimes for two bars, sometimes for four";
the bassline does not arrive until **bar 65**, roughly two minutes into a 4:40 track. **[unverified —
the fetched page is the same article Perplexity quoted, but the specific bar-65 figure was not
independently confirmed in the extracted text; treat the *shape* as sourced and the exact bar as
approximate.]**

**Reduction as the founding idea.** Jeff Mills to *The Wire*: he and Robert Hood "came up with the idea
that maybe we should break down and simplify the music" — which is how minimal techno got its name
(https://www.thewire.co.uk/in-writing/interviews/jeff-mills-interview-by-derek-walmsley,
**[unverified]**). Robert Hood on *Minimal Nation*: "Once I had that chord sound and a particular
pattern I realized I didn't need anything else" (RA 2009 via Selector,
https://selector.news/2021/07/01/robert-hood-minimal-nation-reissue/, **[unverified]**).

**Few ingredients, built for layering.** Oscar Mulero, Yorokobu (`src-yorokobu-mulero.txt`,
https://yorokobu.es/oscar-mulero/) describes techno as "una música hecha con muy pocos ingredientes, muy
pensada para trabajar por capas" — music made with very few ingredients, designed to work in layers.

**Unmeasured loop lengths, stated by Eno in 1985.** Brian Eno on the *Music for Airports* vocal loops
(*Musician*, Sept 1985, `src-eno-musician-1985.txt`,
http://www.moredarkthanshark.org/eno_int_musician-sep85.html):

> "I wanted a silence at least twice as long as the sound. So I'd spin off a whole lot of extra tape and
> then cut the loops. **It wasn't measured. And I didn't want to measure it, because I did want to
> arrive at complicated rather than simple relationships.** And then I started all the loops running,
> and let them configure in the way they chose to."

This is the single strongest citation in the whole file for the decorrelation rule that
`hypnotic-top-layer-2026-09-05.md` arrived at from measurement. Eno also states the general principle:
"You can devise a system or a set of rules that, once activated, will generate music on your behalf"
(1996 lecture, quoted secondhand, **[unverified]**).

**Why repetition works, from research.** Elizabeth Hellmuth Margulis, *On Repeat: How Music Plays the
Mind* (OUP 2014): repetition shifts listening from future-oriented prediction ("what's next?") toward
**timbre, articulation and inner detail**; in her experiments short repeating units are easiest to detect
on first hearing while long-span repetitions only become detectable after several exposures, i.e. as
exposure accumulates the ear migrates to larger-scale structure. **[unverified — book, not re-fetched;
summarised from a publisher preview and the MTO review at
https://www.mtosmt.org/issues/mto.14.20.4/mto.14.20.4.albrecht.html]**
**[agent inference]** The design consequence is direct: if the ear ends up listening to timbre, the top
layer must be *worth listening to as a timbre*, and the interesting change must be spectral rather than
melodic.

Berlyne's inverted-U (arousal/liking peaks at moderate novelty and complexity) is the standard framing
for "how much change is enough"; a review confirms the inverted-U is well-supported for visual stimuli
and **less clearly established for auditory ones**
(https://anthonychmiel.com/wp-content/uploads/2025/08/Chmiel2017_BackToTheInvertedU.pdf,
**[unverified]**). No study gives a number of loop repetitions for techno. **Not found.**

**The focus-music constraint pulls in the same direction.** Already sourced in this repo
(`sonar-attention-and-change.json`): Brain.fm state their music "deliberately keeps attention-grabbing
elements low" and that "a new song section, an unexpected chord, a memorable hook — each of these is a
micro-interrupt". For our product, that means the hypnotic techniques below are not just stylistic —
they are the functional requirement. Any variation must be **below the threshold of attentional
capture**.

### Q2 — Sound-design craft: making a layer sophisticated

**The named failure mode.** Across every source, the "primitive" patch is *one modulator on one
destination*. The sourced pro patches all do at least two of: multiple modulators, modulators on
different destination *classes*, one modulator modulating another, and free (unsynced) rates.

**Three LFOs at 10–20 % depth, on volumes.** Attack Magazine, *Dynamic Modulation With LFOs*
(`src-attack-dynamic-modulation-lfos.txt`,
https://www.attackmagazine.com/technique/tutorials/dynamic-modulation-with-lfos/) — a **dub techno**
tutorial built on stock Live plus Max for Live:

- Drum rack with **three hi-hat samples** of different openness, all playing every 16th note.
- **Three M4L LFO devices**, one mapped to each sample's volume fader. **Sine shape; depth 10–20 %** on
  all three — "to avoid a large volume range as we want the effect to be subtle." Offset lowered for
  samples that should sit quieter.
- Their own observation: "The resulting volume modulation even introduces **new syncopated patterns**."
- Snare into a return with stock **Delay**, send at **−9 dB**; an LFO mapped to **delay time**, rate
  synced to 1 bar, offset lowered so long delay times are avoided.
- An LFO with **Random** shape mapped to the **Velocity MIDI device's Random knob** — randomising the
  amount of randomisation, rather than a fixed random spread.

That last trick is the cheapest available version of "modulate the modulator" and it is fully described
in stock terms.

**Meta-modulation and multi-destination routing.** Attack, *Crafting Ambient Techno Pads*
(already fetched last round, `sources/hypnotic-top-layer/src-attack-ambient-techno-pads.txt`): XLFO 1 at
13 Hz routed to **oscillator sync on two oscillators and to filter pan** — not to cutoff; an envelope
with a **12 s attack** modulates **XLFO 1's own rate**; XLFO 2 at **0.5 Hz** to more osc sync plus a
filter-frequency offset at an amount of **0.045**. Band-limiting before anything else: LP 720 Hz, **HP
280 Hz**, plus a low shelf at 280 Hz.

**Sample-and-hold as a non-repeating modulator.** Attack, *Ambient Sound Design With A Moog Grandmother*
(`src-attack-moog-grandmother-ambient.txt`,
https://www.attackmagazine.com/technique/synth-secrets/ambient-sound-design-with-a-moog-grandmother/):
S&H out → attenuator → filter cutoff, slow LFO rate, **cutoff amount at about 9 o'clock** with a sine
for gentle motion, or **cutoff amount full with a sawtooth** for abrupt steps; the LFO *rate dial itself*
is played by hand while notes sustain. Hardware, but Live's Auto Filter has S&H and Wander LFO shapes
plus a Quantization=Steps mode, so it maps directly.

**LFO rate ranges by effect.** Sound On Sound, *Modulation* (`src-sos-modulation.txt`,
https://www.soundonsound.com/techniques/modulation): ~**0.1 Hz** for slow ambient filter sweeps,
**1–2 Hz** for wah-like movement, **10–20 Hz** for growl/timbral roughness. **[unverified — the fetched
page is the SOS modulation index; the specific Hz figures come from Perplexity's reading of it and were
not located verbatim in the extracted text.]**

**Probability instead of, or alongside, modulation.** Ableton blog, *Take a Chance: Producing with
Probability in Live 11* (`src-ableton-probability-live11.txt`,
https://www.ableton.com/en/blog/take-chance-producing-probability-live-11/): velocity ranges "breathe
life into repetitive parts such as hi-hats"; **note chance** sets the likelihood a note plays at all
("set the chance at 50 % for half/half odds"); applying chance to chords makes a progression "sound less
like a steady chord progression." Live's Chance Editor and Velocity Deviation are per-note properties,
so this is variation that lives in the **clip**, not in a device — it costs no modulator and never
repeats. **[agent inference]** This is probably the highest-value under-used tool we have, because it
produces genuine non-repetition inside a 1-bar loop.

**Euclidean / circular sequencing.** Ableton blog, *Don't DJ: Moving In Circles*
(`src-ableton-dont-dj-circles.txt`, https://www.ableton.com/en/blog/dont-dj-moving-in-circles/): a named
producer whose whole method is Euclidean, circular sequencing rather than linear 16-step patterns, and
the article names the effect he is after — "the surreal effect that multi-metrics and polyrhythms can
have on a listener." Ableton also blogged POLYRHYTHMUS, a M4L Euclidean sequencer
(https://www.ableton.com/en/blog/geometric-sequencing/, `src-ableton-geometric-sequencing.txt`).
Arithmetic (**derived, not sourced**): an *n*-step pattern against a 16-step bar realigns after
LCM(*n*,16) steps — 7 steps → 112 steps = 7 bars; 5 steps → 80 steps = 5 bars; 3 steps → 48 = 3 bars;
15 steps → 240 = 15 bars. Prime-ish lengths against 16 give the longest cycle for the least effort.

**Field recordings and noise as the glue.** Rod Modell (Deepchord), *Synths are boring*
(`src-nowamuzyka-deepchord.txt`, https://www.nowamuzyka.pl/2012/08/22/synths-are-boring/):

> "I've developed some extremely unique ways of processing my field recordings over the years. I actually
> make instruments from them. Many times, sounds that seem like synths are actually field recordings.
> They are more than just backgrounds. I don't think I could make music without them anymore."

Andy Stott, XLR8R *In the Studio* (`src-xlr8r-andy-stott.txt`,
https://xlr8r.com/gear/in-the-studio-andy-stott/): much of *We Stay Together*, *Passed Me By* and
*Luxury Problems* was recorded "on my iPhone"; he later moved to a Zoom field recorder to "get some nice
crunchy stuff." **[unverified — quote located by Perplexity; the fetched page is short and the exact
wording was not re-confirmed line-by-line.]**
No source found gives **numeric levels or filter settings** for a noise/field bed. **Not found.**

**Resonators tuned to the track's key, in the manual.** Ableton Live manual, Audio Effect Reference:
"Create tonal drum loops by placing Spectral Resonator on a drum track and using the **MIDI sidechain
input** to drive specific pitches." Corpus has the same MIDI-sidechain pitch-following.
`sources/hypnotic-top-layer/src-ableton-audio-fx-reference.txt`. ⚠️ **The MIDI sidechain source is a
dropdown = a UI click**, same class of limitation as the LFO Map button
(`hypnotic-top-layer-2026-09-05.md` §2.1). Tuning Corpus/Resonators by their **Tune / Frequency**
parameters is scriptable; routing MIDI into them is not.

### Q3 — Mixing and level craft

**Our own measurement is still the best number we have.** From
`endel-deeper-focus-analysis-2026-09-05.md` **[measured]**: pad stem at **−30.6 dBFS / 3.4 % of mix
energy** vs drums at **−18.0 dBFS / 61.2 %** = **12.6 dB below the kick stem**; the pad's own spectrum is
**45.1 % in 150–500 Hz, 48.3 % in 500 Hz–2 kHz, 0.43 % in 2–8 kHz**; whole-mix 2–8 kHz is **0.07 %**;
**81 % of all energy below 150 Hz**; LRA **4.1 LU**.

**Sourced level hierarchy, all-stock, from one tutorial.** Attack, *Dark Cinematic Hypnotic Techno*
(`src-attack-dark-cinematic-hypnotic.txt`,
https://www.attackmagazine.com/technique/beat-dissected/dark-cinematic-hypnotic-techno/) — 131 BPM,
swing 50 %, **Ableton 12 stock only**:

| Element | Level / setting |
|---|---|
| Drums track volume | **−10.0 dB** |
| Closed hi-hat | **−8.0 dB** |
| Open hat + FX reverse glitch | **−10.0 dB** |
| 808 conga | **−15.0 dB** |
| Rumble-kick send FX | Delay unsynced L 2 / R 3 ms, Feedback and Dry/Wet **50 %**; Reverb decay **3.79 s**, Dry/Wet **68 %**; Saturator Medium curve, Drive **5.7 dB** |
| Ambience group | reverb Dry/Wet **18 %** |
| Glue Compressor | Attack **0.3**, Release **0.4**, Threshold **−16.0 dB**, Makeup **+6.00 dB**, Range **50.0 dB**, Dry/Wet **35 %** |

Note the **≈7 dB spread** between the loudest and quietest percussion elements, and that the atmosphere
send sits at 18 % wet. That is the sourced shape of a restrained mix in this lane.

**Headroom.** Ian Shepherd, *How much headroom is needed before mastering?*
(`src-shepherd-headroom.txt`, https://productionadvice.co.uk/headroom-before-mastering/). His actual
answer is not a single number: (1) just don't clip; (2) in 32-bit float it doesn't matter; (3) in fixed
point avoid peaking above **−3 dB** — "or −6 dB, or −12 dB." He argues *more* headroom does no harm
(inter-sample peaks, analogue-emulation plugins distorting early). **The widely-quoted "−6 dBFS rule" is
a simplification of this page, not a quote from it.** For us: bounce at **−6 dBFS peak**, which is inside
his advice and conventional.

**Kick/bass and mono low end.** Perplexity returned a consistent set of numbers — bass HP **80–100 Hz**
at 24 dB/oct, a **2–3 dB notch at the kick's fundamental** with Q≈2, sidechain **2–4 dB GR**, attack
**<1 ms**, release **60–150 ms**, and "everything below **120 Hz** mono" — but **every one of those came
from SEO content-marketing blogs** (tracksensei.com, soundarchitect.io, stealifysounds.com), not from a
primary technical source. **[unverified — treat as folk consensus.]** The one solid citation is Sound On
Sound's explanation of the *mechanism*: convert to mid/side, high-pass the **Sides** channel, convert
back — that is how you make only the low end mono
(https://www.soundonsound.com/sound-advice/q-how-do-you-make-only-low-frequencies-mono, **[unverified]**,
not re-fetched).
Consistency check against our reference **[measured]**: drums↔bass envelope cross-correlation is only
**0.404** and bass AM depth is **3.7 dB** — so whatever ducking exists there is mild. **Do not pump.**

**Why an over-bright layer sticks out.** No source found states this in psychoacoustic terms for this
genre. **[agent inference]**, but it follows directly from our own numbers: if the whole mix has 0.07 %
of its energy above 2 kHz, then *any* content up there is unmasked — there is nothing to hide behind, so
it is audible at any fader position. Fixing "too loud" by pulling the fader does not work; fixing it by
low-passing does. This matches the reference's pad, which is essentially a 150 Hz–2 kHz object.

### Q4 — Arrangement and variation over time

**Perform long, then cut.** Rod Modell, Vice (`src-vice-deepchord.txt`,
https://www.vice.com/en/article/get-to-know-deepchords-rod-modell-the-detroit-artist-who-still-wants-to-loop-till-infinity/):

> "Most tracks on a CD start out as **45–60 minute pieces that get edited for the album**. I have a hard
> time with this. I enjoy making a loop and letting them play for hours or days in my house. Plus, I
> always start with the ambient parts when making [tracks]."

Two rules fall out of that: **the ambient/texture layer is written first**, and **length is an editing
decision, not a composition decision**. **[agent inference]** For an agent that cannot hear, "render 20
minutes of a slowly-evolving system and cut the best 8" is a far more reliable path than "arrange 8
minutes bar by bar."

**Micro-variation inside a 4-bar loop, sourced.** The real lesson of Attack's *Dark Cinematic Hypnotic
Techno* is not its levels but its **bar map**: kick every bar; hat on the third step of each quarter,
every bar; snare **only on the fifth step of bars two and four**; open hat on **bar two's fifth and
ninth** and **bar four's fifth**; FX glitch on **bar two's eleventh and thirteenth**; shaker on **one
note, step nine of bar three**. So in a 4-bar loop, **six of the eight elements appear in only one or two
of the four bars**, and one element fires **once per four bars**. That is the concrete answer to "how do
you make a 4-bar loop not repeat every bar."

**Movement, not muting, as the arrangement.** The same tutorial adds "90 Degrees Auto Pan" and a Vintage
Delay preset to the shaker specifically "to create some tension and modulate the movement" — i.e. the
*variation device* is stereo and delay modulation on a single sparse hit.

**Bar-count rules are folklore.** Perplexity searched explicitly for a producer stating "one element
every 8/16 bars" or "never more than N elements" and found **no primary source**. Those rules exist in
educator/blog content only. **Not found.** What *is* sourced is the *shape*: Mills fading rides in
rather than unmuting; the bell line in and out "sometimes for two bars, sometimes for four"; the bass
entering ~2 minutes in.

**Generative long-form.** Eno's *Reflection*-era method (Pitchfork 2017, **[unverified]**): a system of
tones set running with randomisation scripts, listened to, occasionally adjusted — not arranged. Combined
with the 1985 unmeasured-loop quote above, the sourced ambient long-form method is: **build a system of
mismatched cycles, run it, listen, tweak, record.**

**Groove and micro-timing.** Roland MC-909 manual: QTZ Timing 0–100 where **50 = straight** and
**60–66 "will usually produce a pleasant shuffle feel"**
(http://cdn.roland.com/assets/media/pdf/MC-909_OM.pdf, **[unverified]**, not re-fetched). Attack,
*DAW & Drum Machine Swing* (`src-attack-daw-drum-machine-swing.txt`,
https://www.attackmagazine.com/technique/passing-notes/daw-drum-machine-swing/) warns that "straight" is
**50 %** in Linn/Logic/Ableton-groove convention and **0 %** in Cubase/FL convention — so a swing number
is meaningless without saying which scale. Ableton manual, *Using Grooves*
(`src-ableton-using-grooves.txt`, https://www.ableton.com/en/live-manual/12/using-grooves/) defines
**Base** (timing resolution the groove is measured against), **Quantize** (straight quantisation applied
before the groove), **Timing** (how much of the groove's displacement is applied), **Random** ("random
timing fluctuation… applies differing randomization to every voice in your clip, so notes that originally
occurred together will now be randomly offset both from the grid and from each other") and **Velocity**.
It gives no recommended values. Perception research: listeners generally do not notice inter-instrument
timing discrepancies **≤ 30 ms**, and studies comparing fully-quantised against expert micro-timed
versions have found them **rated equally groovy**, with exaggerated deviations *reducing* groove
(https://pmc.ncbi.nlm.nih.gov/articles/PMC4542135/, **[unverified]**).
**[agent inference]** For our tempo (120 BPM, 1 step = 125 ms), a 30 ms offset is 24 % of a 16th — so
"subtle" swing lives well under that. And since micro-timing may buy nothing perceptually, **spend the
variation budget on timbre and velocity, not on swing.**

### Q5 — Learning resources worth encoding

| Resource | What it actually covers | Free? |
|---|---|---|
| **Making Music: 74 Creative Strategies** — Dennis DeSantis (Ableton) — https://cdn-resources.ableton.com/resources/uploads/makingmusic/MakingMusic_DennisDeSantis.pdf | 74 named, self-contained strategies for starting, developing and finishing electronic tracks; written as problem→procedure, which is the closest thing to an agent-executable rulebook that exists. **The highest-value thing on this list for us.** | **Free PDF** |
| **Ableton Learning Synths** — https://learningsynths.ableton.com/ | Interactive browser course on oscillators, filters, envelopes, LFOs. Good for Daniel, not needed by the agent. | Free |
| **Ableton Learning Music** — https://learningmusic.ableton.com/ | Rhythm, melody, harmony, structure with an in-browser sequencer. **[unverified — URL not re-fetched]** | Free |
| **Sound On Sound, Synth Secrets** (Gordon Reid), 63 parts — https://www.soundonsound.com/series/synth-secrets-sound-sound | The canonical text on how synthesis actually works, including physical modelling and FM. Reference material, not recipes. | Free online |
| **Attack Magazine, Beat Dissected / Synth Secrets / Deconstructed** — https://www.attackmagazine.com/technique/ | The single richest free source of *numeric* recipes in this lane; several are all-stock-Ableton. Named articles used in this file are cited above. | Free |
| **Attack, *The Secrets of Techno Production*** — https://store.attackmagazine.com/ | Techno-specific book: kick/bass, drum-machine patterns, sound design, arrangement. Referenced from the Beat Dissected articles. **[unverified — contents not inspected]** | Paid |
| **Attack, *The Secrets of Dance Music Production*** — same store | Broader genre-by-genre recipes and mixdown chains. **[unverified]** | Paid |
| **Mike Senior, *Mixing Secrets for the Small Studio*** (3rd ed.) | A linear, repeatable mixing procedure: monitoring → prep → balance → EQ/comp → bus → sweetening. The best candidate for turning into an agent checklist. | Paid (companion site free: https://www.cambridge-mt.com/ms/) |
| **Rick Snoman, *Dance Music Manual*** (3rd ed.) | Engineering-style reference on synthesis, sampling, groove and genre case studies. | Paid |
| **Ableton Live 12 manual — Audio Effect Reference / MIDI Effect Reference / Using Grooves** | The authoritative parameter list. Already the most useful single document for a device-driving agent. | Free |

YouTube: Perplexity declined to name channels or episodes rather than invent them, and none were
independently verified. **Not found** — see §4.

---

## 3. Principles (each traceable)

Movement and modulation

1. Never let one modulator be the only thing moving a layer; run **at least two, on different destination
   classes** (pitch/sync, filter, amplitude, pan, delay time, drive). `[Attack ambient-techno-pads; Attack dynamic-modulation-with-LFOs]`
2. Give modulators **free-running rates that are close but unequal**, so nothing realigns. Eno: "It wasn't
   measured… I did want to arrive at complicated rather than simple relationships." `[Eno 1985; measured 7.66 s vs 8.00 s]`
3. **Modulate a modulator** — an envelope on an LFO's rate, or an LFO on a Velocity device's Random knob.
   `[Attack ambient-techno-pads; Attack dynamic-modulation-with-LFOs]`
4. Keep modulation **depths small**: 10–20 % on volumes; a filter-offset amount of 0.045 in the sourced
   pad patch. Subtlety is the technique, not a compromise. `[Attack, both articles]`
5. Modulating **volume alone can create rhythm** — three LFOs on three hat volumes "introduces new
   syncopated patterns." `[Attack dynamic-modulation-with-LFOs]`
6. Prefer **non-repeating modulator shapes** (Wander, S&H, Noise/Simplex, Random) over sine for anything
   that must survive 8 minutes. `[Attack Moog Grandmother; Live Audio Effect Reference]`
7. Put movement into **delay time** as well as filter — an LFO on delay time, offset so long times are
   avoided. `[Attack dynamic-modulation-with-LFOs]`

Pattern and variation

8. **One pattern, modulated** beats many patterns. Judge it by whether it is still interesting after you
   walk away. `[Mike Parker, Tea & Techno]`
9. In a 4-bar loop, **most elements should appear in only one or two of the four bars**; at least one
   element fires **once per four bars**. `[Attack Dark Cinematic Hypnotic Techno]`
10. Use **note chance and velocity deviation** in the clip for variation that never repeats and costs no
    modulator. `[Ableton, Take a Chance]`
11. Give a texture layer an **odd step-length against the 16-step bar** (5, 7, 15) so it realigns only
    every 5 / 7 / 15 bars. `[Ableton Don't DJ + POLYRHYTHMUS; LCM arithmetic derived]`
12. **Swing is optional; timbral variation is not.** Offsets ≤ 30 ms are largely unnoticed and quantised
    versions can rate as groovy as humanised ones. `[micro-timing research, unverified]` Groove Random
    scatters voices against each other, so keep it low if the lock matters. `[Ableton Using Grooves]`

Arrangement

13. **Arrange by subtraction.** "My style is mainly of subtracting, not adding." `[Jeff Mills]`
14. **Fade, don't unmute.** Bring elements in and out over irregular spans — two bars, then four.
    `[Attack, The Bells]`
15. Assume an unchanged sequence holds for roughly **2.5–3 minutes** before it needs a structural change.
    `[Mills/Hood, unverified]`
16. **Write the ambient/texture layer first**, then the beat. `[Rod Modell, Vice]`
17. **Render long, edit down** — 45–60 minutes performed, 6–10 minutes released. `[Rod Modell, Vice]`
18. Keep the element count low and the parts layerable — "music made with very few ingredients."
    `[Oscar Mulero, Yorokobu]`

Level and spectrum

19. Place the top layer at **~3 % of mix energy / ~12.6 dB under the kick**, and **band-limit it to
    roughly 150 Hz–2 kHz** with under 0.5 % of its energy above 2 kHz. `[measured]`
20. An over-bright layer sticks out **because nothing else is up there to mask it** — low-pass it, don't
    just turn it down. `[agent inference from measured spectrum]`
21. Expect a **~7 dB spread** across percussion elements and an atmosphere send around **18 % wet**, not
    a flat mix. `[Attack Dark Cinematic Hypnotic Techno]`
22. **Duck gently or not at all** — the reference's drums↔bass envelope correlation is 0.404 and bass AM
    depth 3.7 dB. `[measured]`
23. Bounce with **~6 dB of peak headroom**; more headroom does no harm. `[Ian Shepherd]`

---

## 4. Not found

- **No producer, anywhere, states a bar-count arrangement rule** ("one element every 8 bars", "never more
  than N elements"). Those rules are educator folklore. The *shape* is sourced; the numbers are not.
- **No numeric levels or filter settings for noise / field-recording beds.** Modell and Stott both
  confirm the practice; neither gives a dB or a Hz.
- **No YouTube channel or episode could be verified.** Perplexity explicitly declined to name any rather
  than invent them. If we want video sources, that needs a separate, targeted pass.
- **No psychoacoustic paper on why over-bright layers stick out in a dark mix.** Principle 20 is my
  inference from our own spectrum measurement.
- **No sourced swing percentage for minimal techno.** Roland's 60–66 (on a 0–100 scale where 50 =
  straight) is the only manufacturer number found, and it is not genre-specific. **[unverified]**
- **No numeric optimum for "how many times should a loop repeat."** Berlyne's inverted-U is the right
  frame; the auditory evidence for it is weaker than the visual evidence.
- **Attack's *Dynamic Modulation With LFOs* part 2** (LFOs modulating sample offset and other LFOs) —
  the article is referenced in part 1 but the URL guessed for it 404s. Worth finding; it is the closest
  published thing to our decorrelation problem.
- **The Quietus Deepchord interview** could not be extracted (page returned navigation only); the
  long-take claim is instead sourced from Vice, which says 45–60 minutes rather than 30–40.
- **Jeff Mills' RBMA lecture transcript** and **The Wire interview** could not be re-fetched; both
  quotes are **[unverified]**.
- **Margulis, *On Repeat*** is a book and was not read; the summary rests on a publisher preview and a
  journal review.
- **No tutorial for tuning Resonators (as opposed to Corpus / Spectral Resonator) to a track's key.**
  And the MIDI-sidechain routing that makes any of them follow a key is a **UI dropdown**, not a
  scriptable parameter — the same class of limitation catalogued in `hypnotic-top-layer-2026-09-05.md`.
