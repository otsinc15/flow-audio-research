# Initial technique cards — 2026-09-05

These are mechanisms to test, not Endel patch identifications. Raw captions and model reports remain outside the repository.

## Filtered saw bass — Alex Rome, 12:22–14:20

Source: [How To Make Any Sound From Scratch](https://www.youtube.com/watch?v=p1-WmITJqBk&t=742s).

- User anchor: Daniel likes the sound at **12:51**. This is separate from his rolling-bass link. His preference has not yet been localized to the bass versus the accompanying upper sound.
- Verified visually near 12:49: Serum 2, initialized patch, oscillator A saw, single unison voice, Filter 1 enabled and A routed into **MG Low 24**. The displayed amplitude envelope has a gate-like shape. The presenter introduces a bass underneath an existing upper part.
- Captions: 12:35–13:20 low-register notes plus a tight low-pass; 13:23 square comparison; 13:44–14:15 saw/unison comparison. These are different demonstrations, not settings all active at 12:51.
- Unknown: exact 12:51 cutoff and envelope timing, the upper layer's actual patch, and hidden FX. Gemini supplied a second-by-second cutoff list, but these numbers were not independently verified and are not retained as facts. Its reading of a “Classic Electric Piano” region label does not identify the upper instrument.
- Adaptation: single saw in Operator or Analog, low register, 24 dB low-pass, high amp sustain and short release. Compare a dark fixed cutoff against a slow opening; initially keep FM and unison off. Native circuit differences mean this is a mechanism reconstruction, not identical Serum output.
- Test: same MIDI through saw versus square, gain-matched; then bass alone versus bass with a quiet, separately shaped upper pulse. Candidate values must be recorded as our choices, not the creator's settings.
- Status: captions read in full, key frames inspected, bounded audiovisual model analysis completed; adaptation not yet user-kept.

## Filter envelope versus amp envelope — Alex Rome, 18:19–23:35

Source: [Modulation demonstration](https://www.youtube.com/watch?v=p1-WmITJqBk&t=1099s).

- Caption evidence: one saw, low-pass closed, separate envelope opens cutoff, zero filter-envelope sustain, decay shapes brightness; later adds reverb/echo and contrasts envelope with a repeating LFO.
- Root visual check at **19:46**: Serum 2 oscillator A single saw, MG Low 24 routed from A, ENV 2 selected with a blue cutoff modulation arc. ENV 2 reads attack **0.5 ms**, hold **0.0 ms**, decay **1.51 s**, sustain at the bottom, release **15 ms**. These are this frame's settings, not a timeless final preset.
- Interpretation: amplitude can retain body while harmonics fade. This provides a different result from shortening every sound with the amp envelope.
- Adaptation: Operator single saw, nonzero amp sustain, short filter decay and zero filter sustain; compare with a version using amp decay only. Hold MIDI and output loudness constant. Add filtered Echo only after the dry comparison.
- Do not promote the presenter's broad claim that modulated sounds are inherently warmer into a synthesis rule.
- Local experiment: R6 tracks 08/09 hold the same MIDI and gate-like amp shape; track 09 initially added a filter envelope with our chosen 240 ms decay. A second native export changed only decay to the observed 1.51 s. Kick/context players B/D both measure -16.21 LUFS; no listening verdict exists. The other native settings remain our choices, so this is an adaptation and controlled contour test, not faithful preset reconstruction.
- Status: full captions, selected actual frames and bounded audiovisual model analysis (18:10–22:10). Model-only claims about exact cutoff, reverb settings and later sustain changes remain unverified. Operator's filter-envelope sustain uses a different display from its oscillator-envelope sustain; inspect native units instead of copying the model's “-inf dB” suggestion.

## Rolling bass and context — Dilby

Source: [3 levels of Rolling Bass](https://www.youtube.com/watch?v=xZDNpDJmOwg).

- 1:44–4:50: sixteenth notes, mono plucky Diva source, kick ducking; compare removing the first one or two sixteenths of each beat.
- 4:55–8:05: MIDI velocity must be connected to amplitude and/or filter response to change the sound. Accents can create a second pattern inside the repeated notes.
- 16:08–19:58: separate a steady sub role from rolling mid-bass; avoid making every layer complex.
- 20:26–22:38: contrasting FM accents above a predictable bass; adding a third busy layer demonstrates crowding.
- 22:40 onward: change surrounding drums/accents to demonstrate context's contribution. Do not claim the bass stays identical throughout the whole section: later examples also combine and switch bass ideas.
- Adaptation for our focus brief: preserve the accepted FM base, compare one quiet contrasting pulse and restrained percussion with the identical baseline. Do not import the lesson's melodic progressions, disco drums, or full-density house arrangement by default.
- Status: full captions read; actual frame at 26:45 shows Session View with an upper MIDI loop. Bounded audiovisual analysis covers 22:40–27:20. Exact MIDI cycle length was not legible, and the model incorrectly called the visible Session View Arrangement View; retain the context mechanism, not that label or an invented note pattern.

## Continuous FM movement — Zonal Audio

Source: [Operator FM bass](https://www.youtube.com/watch?v=rMEBjOqf3CU).

- Previously studied captions and selected frames: separate external LFO devices move modulator attack, sustain and level; bounds avoid the plain/harsh extremes. Echo filter modulation moves the repeats separately.
- Operator has one internal LFO. A Coarse 0.5 and B Coarse 3 means a 6:1 modulator/carrier ratio. Mapping percentages are neither seconds nor dB.
- Local R5 adaptation: 2:1 sine FM, distinct carrier/modulator envelopes, external slow modulation of B level and filtered Echo.
- User verdict on `LISTEN-R5-FM.mp3`: “a decent base - pretty generic but doesnt sound horrible.” This accepts a starting point, not a finished Endel match. Preserve the original study export.

## Match shape before timbre — Eric Bowman

Source: [How I Recreated Over 1000 Sounds](https://www.youtube.com/watch?v=MZpZaucYI4E).

- 2:55–4:23: rapid level-matched comparison and separate attention to amplitude evolution. Test one attack or release change before rebuilding the oscillator.
- 7:18–9:27: compare different pitches to distinguish features that follow harmonics from features that stay at a fixed frequency. This guides waveform editing versus fixed EQ and filter key tracking. A one-pitch reference cannot uniquely resolve this distinction.
- 9:27–9:58: edit selected harmonics rather than adding unrelated oscillators. Operator's harmonic editor can implement the mechanism; keep normalization consistent and compensate output gain.
- 12:12–14:43: inspect stereo sides to distinguish source width from spatial effects. Side energy alone does not identify an effect uniquely.
- Evidence: full auto-captions, bounded audiovisual analysis 8:12–9:58, agent-inspected 9:29 frame showing Vital single saw, Analog 24 dB filter and short curved amp envelope. Numeric key tracking was not independently legible. Stereo method is caption-based.
- Test: two temporary notes an octave apart, identical patch/envelope, compare filter key tracking 0% versus 100%. Diagnostic notes are not a proposed melody for the final focus track. Not yet rendered or user-kept.

## Add selected harmonics simply — Akayo

Source: [How To Create ANY Sound from ANY Song, 5:47–6:07](https://www.youtube.com/watch?v=TSx1w2G0m98&t=347s).

- Captions compare a pure sine with a triangle. Root frame at **5:58** confirms Serum 2 A triangle, one voice, Noise AC hum1 on; main Filter 1/2 off. ENV1: attack 23 ms, hold 0, decay 602 ms, sustain -22.6 dB, release 18 ms. FX page is hidden, so effects are not assumed off.
- Mechanism: a triangle supplies upper harmonics while keeping a strong fundamental. A more complex FM patch is not necessary to test this change.
- Test: upper pulse sine versus triangle, same envelope/MIDI and initially no FX, level-matched above an unchanged bass. These are our test conditions, not all settings used by Akayo. This example is separate from Daniel's Alex Rome 12:51 preference.
- Evidence: full captions, bounded audiovisual analysis 3:55–6:07 and root frame. The model's claim that Operator categorically lacks internal distortion was rejected; modeled filter drive exists. Not yet rendered or user-kept.

## Compose movement against the kick — Pick Yourself

Source: [The Hypnotic Techno Bass Pros Use Instead Of Rumble](https://www.youtube.com/watch?v=illbDcxNI5M).

- 2:48–3:22: draw deliberate pitch-bend shapes. Root actual frame near 2:53 confirms Pitch Bend selected in the MIDI clip and drawn ramps above/below center. Bend range is unreadable.
- 3:39–4:20: captions shift only the second bar one grid step. Exact grid division is unverified. At 5:15–5:54 the tutor rejects a nine-step experiment that weakens this arrangement; complexity is not the goal.
- Two separate tests: flat versus one drawn bend with the same notes/patch, then original versus displaced second-bar timing with note count/gates/velocities preserved. Verify bend range and return to center. Glide on identical repeated pitches is not a useful glide test.
- Evidence: full captions, audiovisual analysis 2:35–5:55, one independently inspected pitch-bend frame. Timing-grid details remain provisional. Not yet rendered or user-kept.

## Preserve a performed tone change in the repeats — Underdog

Source: [The most educational bass, 9:29–11:23](https://www.youtube.com/watch?v=75p5puCwbL0&t=569s).

- Captions demonstrate changing decay and using low-wet delay plus reverb to carry tone changes across subsequent notes. The audiovisual report identifies Wavetable's filter envelope, later wavetable-position movement, then Delay and ValhallaRoom; those precise UI identifications were not independently frame-verified.
- Test in stages: fixed versus performed filter-envelope decay with the amplitude envelope unchanged; then the identical performance dry versus a quiet filtered spatial return. Preserve the dry pulse. The tutorial's large wash is not established as suitable for our bass.
- Evidence: full captions and bounded audiovisual analysis, not a complete visual watch. No copied knob values. Not yet rendered or user-kept.

## Articulation after space — Chris Avantgarde / DJ Mag

Source: [Track from scratch, 1:55–4:00](https://www.youtube.com/watch?v=tOY35nO37A8&t=115s).

- Bounded audiovisual analysis reports reverb before rhythmic gating, then a second voice with a contrasting rhythmic density. Gating the tail is a different mechanism from placing reverb after already-short notes.
- Test: identical upper source and MIDI, compare Echo/Reverb before versus after a gentle amplitude stage. Choose a restrained rate/depth; the source's aggressive cinematic stutter is not the focus brief.
- Evidence limit: no supported captions; only an actual 3:12 frame of Serum's source selection was independently inspected. Effect order and density remain model-observed hypotheses requiring direct verification before exact reconstruction. This early passage does not establish kick/bass mixing. Not yet reconstructed.

## Make support audibly contribute — Audioreakt

Source: [Full Hypnotic Techno track from Scratch, mixing at 44:40](https://www.youtube.com/watch?v=5C2IekPMnaQ&t=2680s).

- Audiovisual analysis 44:40–48:20 reports foundation-first balancing and separate support entries. Root actual frames near **46:24 and 46:41** show changing support activators/faders; the visible Ohh chain has an EQ dip near 9.79 kHz and Reverb. They do **not** establish the model's claim of high-pass removal of percussion low-mids. Do not retain that claim or its inferred off-grid MIDI edit.
- Test: choose a passage after all intended entries. Compare accepted baseline against baseline plus each support separately. Remove a layer to confirm its role; adjust level and contour until it contributes without obscuring the foundation. Avoid copying the tutorial's fader numbers, which depend on its source levels.
- Local diagnosis: R5 wood/air/shadow stems are nonzero but extremely quiet even in the last 32 seconds. Their measured presence is not audible mix completion. Preserve this as an unresolved balance/contour issue, not a taste-approved seven-layer result.
- Evidence: bounded audiovisual model analysis and root-selected frames, no full video watch. Exact bass-return settings remain unverified. Support experiment not yet user-kept.
