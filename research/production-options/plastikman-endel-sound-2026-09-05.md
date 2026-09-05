# Plastikman / Endel "Deeper Focus" — how it's made, and how to rebuild it in Ableton Live 12 stock devices

Compiled 2026-09-05. Method: Perplexity (`sonar-pro`, via OpenRouter) for discovery, then every kept claim
re-fetched from its primary page (WebFetch or curl) and cited by URL. Raw Perplexity JSON in
`research/production-options/sources/plastikman-endel/q1-4-*.json`; re-fetched primary pages as
`src-*.txt`/`src-*.html` in the same folder. This file does not duplicate what's already covered in
`synth-instruments-2026-09-02.md` (code-driven synthesis, licensing) or `techno-pattern-book-2026-09-02.md`
(the fullest existing numeric recipe book for hypnotic dub/minimal techno) — it's cited instead of repeated.

## Summary for a non-programmer

"Deeper Focus" is not a composed track and not AI-generated from scratch. Richie Hawtin (Plastikman)
recorded a fresh batch of sounds specifically for this project — drum hits, basslines, chord stabs, FX —
and handed them to Endel as a "stem pack." Endel's engine is a real-time mixer/arranger: it picks which of
Hawtin's stems to play, how loud, and with what filtering, based on your phone/watch data (time of day,
light, weather, heart rate). Hawtin himself compares it to how the TR-909 drum machine's factory-tuned kick
became "his sound" without him building the circuit — Endel's AI is just another instrument he's playing by
proxy. Nothing is composed on the fly; only which pre-made pieces play, and how they're layered and filtered,
changes. His own words: it's not "such a strange new thing" — he traces the idea to Brian Eno and minimalist
composers Steve Reich and Philip Glass. Separately, his classic Plastikman records (Consumed, Closer, EX)
were built on real hardware — 909, TB-303, samplers, modular synths, and heavy dub-style delay/reverb — not
software presets. No one has published a "make Plastikman with only Ableton stock devices" tutorial; the
table below is this agent's best inference from verified gear behavior plus an existing Attack Magazine dub-
techno recipe already in this repo, and it's labeled accordingly.

---

## Q1. Endel x Plastikman "Deeper Focus" — how it was made

**Primary sources, re-fetched:**
- Beatportal interview — https://www.beatportal.com/articles/452112-we-talk-to-richie-hawtin-about-deeper-focus-his-collaborative-soundscape-with-endel-ai-to-get-you-focused
- Music Ally interview (Hawtin + Endel CEO Oleg Stavitsky) — https://musically.com/2021/04/27/plastikman-and-endel-talk-ai-music-this-is-uncharted-territory (paywalled but the article body renders in full HTML; quotes below pulled directly from the fetched page)
- Endel focus page (soundscape listing only, no technical detail) — https://endel.io/focus
- Endel technology page (general engine description, not Deeper Focus-specific) — already fetched as `src-endel-tech.txt` in the parent directory (2026-09-02)

**Stems / materials.** Hawtin recorded new material specifically for the project — "I've taken newly
recorded Plastikman material, the stems and frequencies samples, and we've fed that into the AI algorithm"
(Music Ally). Stavitsky: "We're basically extracting his DNA in the form of a stem pack, and feeding that
into the algorithm." No source gives a stem count or an instrument-by-instrument stem list — Hawtin
describes handing over "sounds, stems and effects" with "attributes in how they might play" (Beatportal),
and Stavitsky confirms exclusivity: "there are no other sounds in this soundscape except for Richie's
sounds!" (Music Ally).

**Relationship to EX / Consumed.** No source says Deeper Focus reuses stems from a specific album. Beatportal
paraphrases Hawtin as saying "the true spirit of Plastikman lies in the full album length explorations"
including Consumed — offered as conceptual inspiration, not as a sample source. Both interviews are explicit
the audio itself is newly recorded for this project.

**Engine behavior.** Endel: "The AI takes inputs like location, weather, natural light, and heart rate, then
creates the optimum personalized sound environment based on this information" — "changes in real-time
according to these inputs" (Beatportal). No source gives modulation curves, randomization mechanics, or an
exact mapping (e.g., heart rate → tempo); the press language stays at "beats synced to heart rate" without
detail. Hawtin's framing of the compositional method, in his own words (Music Ally): "This compositional
method goes back to the 70s and 80s, when Brian Eno was working on his ideas of generative music, and then
the minimalist composers of the 80s like Steve Reich and Philip Glass... creating a framework and feeding
the building blocks into the framework and stepping back... and watching this system creating something
out of those building blocks." And on retaining authorial control despite handing off to an algorithm:
"What I delivered wasn't everything I'd done! I gave things that I was confident would mix and match... The
system is only as good as what you feed it, right? So I was very careful in that approach." And his 909
analogy for why this doesn't feel like ceding creative control: "The Roland engineers who made the 909 drum
machine made some very specific decisions in their design that enable me to create music. They made the 909
kick drum! I didn't make that, but that is part of my sound... I see this collaboration as another extension
of that: of me collaborating with technology."

**Practical takeaway for rebuilding this:** there is no public spec to copy. The reproducible part is the
*idea* — a small library of tightly-controlled, mix-and-match one-shots/loops/FX with simple compatibility
rules, played back and filtered by a slow, low-information-rate controller (LFOs/random walks standing in for
Endel's biometric inputs) — not any specific patch or preset.

## Q2. Plastikman sound design — Consumed, Closer, EX, live rig

**Primary source, re-fetched: Sound On Sound "Classic Tracks: Plastikman 'Consumed'"** —
https://www.soundonsound.com/techniques/classic-tracks-plastikman-consumed

Gear used on *Consumed* (1998), per Hawtin's own account in that piece:
- **Roland TR-909** — used largely as a sequencer/clock, not just its own drum sounds: "a big trick was using
  the 909 as a one-note sequencer," with shuffle at setting 3 for syncopation.
- **Doepfer MAQ16/3** — three units, "nine different CV and MIDI 16-step sequences," feeding irregular,
  non-power-of-two patterns ("cyclical five-note patterns, 12-note patterns") to other gear via CV.
- **Akai S3000 sampler** and **Kawai XD-5 drum synth module** — alternate drum/tom/conga voices, sequenced
  from the 909 rather than using its own onboard drums.
- **Serge modular** (STS Serge rebuild) — filter/parameter modulation via sequencer, e.g. the title track's
  "tom/conga sound... which I slowly opened up and closed through a Serge filter with a lot of effects."
- **Korg Wavestation** for ambience; secondhand Roland SH-101 and Korg 303s.
- Effects: **Lexicon PCM90**, **Roland SRV-330** (reverb), **Ensoniq DP/4**, **ART Multiverb** (gated reverb
  on claps), **Yamaha SPX90** ("dirty, great flange").
- Movement mechanism, in Hawtin's words: "Consumed is an album of feedback. Everything was
  cross-modulating everything else." Plus triplet delays for extra syncopation, and MIDI-mute automation on
  an Allen & Heath mixer running an 8/16-bar loop of effects switching on and off.
- Recorded live to 2-track DAT in single takes, edited afterward in Sound Forge ("this part is a good
  beginning, this middle part needs to be shorter, cut") — the "mix" was largely a live performance, not a
  multitrack session.

**Ableton / live-rig era, re-fetched: Ableton's own artist page** —
https://www.ableton.com/en/pages/artists/richie_hawtin/ — Hawtin started using Live "probably in 2001,"
initially as "an external signal processor" for DJ-set effects. For the Plastikman live show he ran "about
twenty-six Plastikman tracks along with external boxes and some 303s"; for DJ sets, "five or six hundred
tracks in Ableton — full compositions, not just loops." For studio arrangement work (*DE9: Transitions*): "I
used Ableton then to fully structure and lay out a basic rough version of the mix in the Arrangement View,
and once the basic structure was done, I piped it via ReWire into Pro Tools for final adjustments."

**Not independently verified (source blocked or gave no technical detail):**
- MusicRadar/Future Music "Plastikman Live Gear Set Up" — page text confirms only that the actual gear list
  was on a DVD-covermount video, not in the article body. Not usable as a citation for specific gear.
- Billboard's CLOSE interview — blocked by a paywall proxy (HTTP 402) on this fetch; not verified.
- No fetched source gives *EX* (2014)-specific gear beyond the general live-rig pattern above (Ableton +
  hardware sequencers + modular, per the Ableton page and general Plastikman Live description).

## Q3. Ableton stock-device tutorials for this sound

**Searched and not found.** No Ableton.com, Attack Magazine, Sound on Sound, Bedroom Producers Blog,
Gearspace, Reddit, or YouTube source describes recreating the Plastikman/hypnotic-minimal-techno sound using
only Ableton Live stock devices with a concrete parameter recipe. What exists instead:
- An Ableton Forum thread says Hawtin's own set used third-party plugins (Drumazon, Nepheton, ADM, ABL2) and
  outboard-style delay emulations (Lexicon PSP42/PSP84), not Ableton's stock Echo/Auto Filter —
  `https://forum.ableton.com/viewtopic.php?t=204730` (not independently re-fetched; treat as unverified).
- Ableton's Kapture Max for Live device (built with Plastikman/Liine) is about live parameter snapshot/recall
  during performance, not sound design — `https://www.ableton.com/en/packs/kapture/`.

Because no stock-device recipe exists in the wild, the table below is built from three things that *are*
independently sourced: (a) the Consumed-era gear behavior above (909-as-sequencer, cross-modulation, slow
filter opens, dub delay/reverb), (b) `techno-pattern-book-2026-09-02.md`'s already-cited Attack Magazine dub
chord recipe (§4.2 there, `src-attack-dub-techno-synth-chords.txt`) mapped from u-he Diva onto Ableton's
Analog/Operator, and (c) this project's own bass/EQ measurements (`research/ear-test/spec-from-references.md`).

## Q4. What makes hypnotic techno hypnotic — numbers

`techno-pattern-book-2026-09-02.md` already has the deepest sourced numeric answer to this question in this
repo — see its §§3–8 for delay-feedback math (BBD-style feedback ~44, feedback-path HF cut ~5 kHz/LF cut
~200 Hz, send filter LFO 0.25 Hz), loop-length reasoning (8/16-bar phrase units, coprime loop lengths for
long realignment periods, e.g. 3-against-4 or 5-against-8), and frequency-balance targets (sub <60 Hz ~25%,
mono below ~120 Hz). Cite that file for those; not reproduced here.

New from this round's Perplexity `sonar-pro` query, **could not be independently re-verified** (the model
disclosed it was working from already-retrieved snippets rather than fresh URLs, and follow-up fetches for
"Villalobos Dexter breakdown," "Crafting Ambient Techno Pads," and "Dark Cinematic Hypnotic Techno" Attack
articles were not attempted this round given budget) — listed in Not Verified below rather than stated as
fact. The one number worth flagging as *plausible but unverified*: 129 BPM cited for Villalobos "Dexter,"
and a claimed Attack "raw hypnotic techno" tutorial at 138 BPM/50% swing — both outside this product's
112–120 BPM window per the existing pattern-book anyway (§1 there), so not actionable regardless of truth.

## Ableton stock-device starting points

| Layer | Device | Settings to try | Source |
|---|---|---|---|
| Kick/909 sequencer feel | Drum Rack + Impulse or Drift (percussion mode), MIDI clip | Sequence one drum voice from a second, off-grid clip acting as a "clock" (e.g. a 9- or 5-step MIDI pattern gating a sample-and-hold on a filter) to emulate 909-as-sequencer cross-triggering | [agent inference] from SOS Consumed gear description (909 used as "a one-note sequencer") |
| Sub bass | Analog or Operator, sine/triangle osc, root ~55 Hz | Low-pass ~80 Hz, 12 dB/oct; keep dry/mono below ~120 Hz | [sourced] techno-pattern-book §8.3, §"Sub" row (Attack warehouse-rolling-bass tutorial); root freq matches this repo's own ear-test findings |
| Chord/stab (the "hollow" dub-techno stab) | Operator or Wavetable → Auto Filter (high-pass ~80–100 on a 0–100-style scale, i.e. cut well below the note) → EQ Eight (−7 dB shelf/bell ~600 Hz wide Q, HP <100 Hz, LP >4.5 kHz) | Filter env: slow attack (roughly 80% of a 0–100 scale) so the chord "opens" over ~1 bar+; amp env short (11/35/8–15 on that same scale) because the delay supplies the sustain | [sourced, mapped from Diva to Ableton] techno-pattern-book §4.2, `src-attack-dub-techno-synth-chords.txt` |
| Filter movement layer 1 (fast) | Auto Filter, LFO device or built-in envelope follower | Cutoff LFO around "1 o'clock" rate (roughly 1–2 Hz feel) | [sourced, mapped] same Attack recipe |
| Filter movement layer 2 (slow, on the send/delay return) | Auto Filter on an Echo return track | High-pass shelf ~280 Hz, low resonance, LFO rate ~0.25 Hz (4 s cycle), depth low (~22/100) | [sourced] techno-pattern-book §4.2/§4.3 |
| Dub delay | Echo (Ableton stock), "Analog"/tape-style character mode | Two taps: 1/8 dotted at ~20% feedback, and a free-running ~264 ms tap at ~85% feedback; feedback path HP ~200 Hz, LP ~5 kHz | [sourced] techno-pattern-book §7 (Attack ultimate-delay-guide, creating-dub-delays) |
| Cross-modulation / "everything modulates everything" | Ableton's Max for Live LFO / Shaper device modulating multiple destinations from one slow source | Route one slow (seconds-long) LFO to 2–3 unrelated targets (a filter, a pan, a send level) simultaneously, rather than one LFO per target | [agent inference] from Hawtin's "Consumed is an album of feedback. Everything was cross-modulating everything else." (SOS) |
| Long-form arrangement automation (Endel-style "which stems play now") | Arrangement-view automation lanes or Follow Actions on session clips, gated by a slow random LFO | Treat each stem/loop as a clip with a probability/follow-action weight that changes on an 8/16-bar cycle, mimicking Endel choosing which of Hawtin's stems to sound | [agent inference] from Q1 findings (Hawtin: "building blocks... fit together" by the algorithm) — no Ableton-specific precedent exists |
| Drum saturation/glue | Drum Buss on the drum rack's group | Boom ~8% around ~37 Hz, Damp ~8.5 kHz | [sourced] techno-pattern-book §6, `src-attack-basic-channel-dub.txt` (this is a 145 BPM Basic Channel-style patch note, tempo doesn't transfer, the Drum Buss settings do) |
| Tempo | Set project tempo | 118–120 BPM | Brief's own target; techno-pattern-book's measured reference tracks sit at 112–120 BPM (ref01 = 114.8 BPM) |

## Not verified

- Exact stem count or per-instrument stem list for Deeper Focus — no source states a number.
- Any explicit statement that Deeper Focus stems derive from *EX* or *Consumed* master material (sources say
  newly recorded).
- Endel press release PDF (`endel.io/pages/newsroom/press-releases/plastikman/...pdf`) — fetched but returned
  as unreadable binary/image content; not usable as a direct quote source. Its claims are corroborated
  instead via Beatportal and Music Ally, both fetched successfully.
- MusicRadar/Future Music "Plastikman Live Gear Set Up" article — text body has no gear detail (it points to
  a DVD video); not usable as a citation.
- Billboard CLOSE interview — blocked by a paywall (tollbit proxy, HTTP 402) on this fetch attempt.
- Ableton Forum thread claiming Hawtin used Drumazon/Nepheton/ABL2/Lexicon PSP42/PSP84 — surfaced by
  Perplexity, not independently re-fetched/verified this round.
- This round's Q4 numeric claims not already in `techno-pattern-book-2026-09-02.md` (129 BPM for Villalobos
  "Dexter," a claimed 138 BPM/50% swing "raw hypnotic techno" Attack tutorial, "Crafting Ambient Techno Pads"
  envelope numbers, "Dark Cinematic Hypnotic Techno" compressor settings) — Perplexity could not supply fresh
  URLs for these on this pass (it disclosed it was reasoning from earlier snippets), so none are re-verified
  or stated as fact above.
- Whether Endel's real-time engine uses randomization, Markov/rule-based selection, or another specific
  mechanism to choose which stems play — sources say "rules and assumptions" and "attributes" but no source
  names the actual algorithm.
