# ElevenLabs Music generation log — 2026-09-02

Every API call made for the first ear-test slice. No API key appears in this file. Generated audio
lives in `~/Documents/AI Agent Outputs/Artifacts/flow-audio-candidates/` and is **not committed**.

## Call parameters (identical for all six generations)

```
POST https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128
Content-Type: application/json
body: {"prompt": "<see below>", "music_length_ms": 60000, "force_instrumental": true}
```

`model_id` was left unset, so the API default (`music_v1`) applied.

## Prompt-design rules applied to all six

Every prompt states: instrumental only, no vocals, no intro, no outro, no risers, no drops,
loop-friendly, and an explicit BPM. Plus, per palette: no melody, no lead line, constant energy.

**One constraint had to be worked around.** The ElevenLabs music terms prohibit prompt inputs
containing "any artist's… real name or stage name", "any song title", or "any music label's name"
(`../production-options/src-elevenlabs-music-terms.txt`). Palette B was briefed as
"Basic Channel-style chords" — that is a label/artist name and **was deliberately not used in any
prompt**. It is described functionally instead: heavily filtered minor chord stab on the offbeat,
long feedback delay, cavernous reverb tail, tape hiss.

## The six calls

| # | File | Palette | Prompted BPM | HTTP | Bytes | `song-id` (response header) |
|---|---|---|---|---|---|---|
| 1 | `el-a-1.mp3` | A — minimal techno | 122 | **200** | 960,515 | `HtajMd4egFsko500DAys` |
| 2 | `el-a-2.mp3` | A — minimal techno | 120 | **200** | 960,515 | `Cwp0vg2l2SX76fAvaAos` |
| 3 | `el-a-3.mp3` | A — minimal techno | 126 | **200** | 961,351 | `OrRgCe9Za8Wo72mWvLmx` |
| 4 | `el-b-1.mp3` | B — dub techno | 118 | **200** | 960,515 | `7g9QR4DTVoc2C7o4sZvN` |
| 5 | `el-b-2.mp3` | B — dub techno | 122 | **200** | 960,515 | `eFOf5eeN0nmvJceeyOoq` |
| 6 | `el-b-3.mp3` | B — dub techno | 115 | **200** | 960,515 | `xcVERDabFltHCJKNv7s5` |

All six returned `content-type: audio/mpeg` and decoded to 60.0 s (a-3: 60.1 s), 44.1 kHz.

`song-id` is worth keeping: it is the handle for `conditioning_ref` (generate a variation conditioned
on a previous song) and for inpainting via `source_from`, both of which need `store_for_inpainting`
set at generation time — which was **not** set on these six, so the inpainting path is closed for
this batch.

## Prompts, verbatim

### 1. el-a-1 — palette A

> Hypnotic monotone minimal techno at 122 BPM, instrumental only, no vocals. One unchanging four-on-the-floor kick, deep clean sub bass locked to the kick, a single soft filtered minor chord pad held low in the mix, closed hats quiet and even. Absolutely constant energy from the first bar to the last: no intro, no outro, no build-ups, no risers, no drops, no fills, no arrangement changes, no melody, no lead line. Dry, warm, analogue, low-mid weight, gentle high end. Loop-friendly seamless groove, background listening for deep concentration, great production quality.

### 2. el-a-2 — palette A

> Deep hypnotic minimal techno at 120 BPM, instrumental only, no vocals. Very deep round sub bass with a soft rounded kick, one dark filtered chord washing quietly underneath, hats barely there and soft, almost no top end. Constant unchanging energy throughout: no intro, no outro, no build-ups, no risers, no drops, no fills, no melody, no lead, no variation in intensity. Warm analogue low end, subdued mids, muted highs. Loop-friendly seamless groove for long focus sessions, great production quality.

### 3. el-a-3 — palette A

> Dry hypnotic minimal techno at 126 BPM, instrumental only, no vocals. Tight short kick, firm sub bass, a repeating muted percussive tick and soft shaker, one heavily low-pass-filtered chord that never changes shape. Completely constant energy, strictly repetitive, no intro, no outro, no build-ups, no risers, no drops, no fills, no melody, no lead, no breakdowns. Clean modern mix, controlled highs, no crash cymbals. Loop-friendly seamless groove designed as focus background music, great production quality.

### 4. el-b-1 — palette B

> Cavernous dub techno at 118 BPM, instrumental only, no vocals. Soft muffled four-on-the-floor kick, deep warm sub bass, one heavily filtered minor chord stab on the offbeat drenched in long feedback delay and a huge reverb tail, soft brushed hats, faint tape hiss and vinyl crackle. Constant unchanging energy for the whole take: no intro, no outro, no build-ups, no risers, no drops, no fills, no melody, no lead line. Murky, submerged, spacious, warm analogue. Loop-friendly seamless groove for deep focus, great production quality.

### 5. el-b-2 — palette B

> Deep dub techno at 122 BPM, instrumental only, no vocals. Steady soft kick, thick sub bass, a single dark chord stab echoing on the offbeat through long dub delay feedback and cavernous reverb, hats soft and distant, hiss and room noise in the background. Strictly constant energy, hypnotic and repetitive: no intro, no outro, no build-ups, no risers, no drops, no fills, no melody, no lead, no structure changes. Warm, foggy, wide stereo tail, restrained high end. Loop-friendly seamless groove, background music for concentration, great production quality.

### 6. el-b-3 — palette B

> Slow sparse dub techno at 115 BPM, instrumental only, no vocals. Distant soft kick, deep sub bass swell, one heavily filtered chord stab every other bar disappearing into an enormous delay and reverb tail, whispered soft hats, gentle tape hiss. Constant low energy throughout, meditative and unchanging: no intro, no outro, no build-ups, no risers, no drops, no fills, no melody, no lead, no crescendo. Dark, underwater, cavernous, warm. Loop-friendly seamless groove for long deep work sessions, great production quality.

## Call 7 — stem separation

```
POST https://api.elevenlabs.io/v1/music/stem-separation?output_format=mp3_44100_128
Content-Type: multipart/form-data
file=@el-a-1.mp3
```

**HTTP 200**, `content-type: application/zip`, 5,766,186 bytes. Unzipped to
`flow-audio-candidates/stems/el-a-1/`. **Demucs was not needed and was not run.**

**Six stems, fixed names:** `bass.mp3`, `drums.mp3`, `guitar.mp3`, `other.mp3`, `piano.mp3`,
`vocals.mp3` — each a full-length 60 s file. This answers open question 10 in the tool matrix
("how many stems ElevenLabs' stem-separation returns, and what they are called"): **it is a
fixed six-way pop/rock taxonomy, not an adaptive decomposition of whatever was uploaded.**

Measured level of each stem (`ffmpeg volumedetect` / `ebur128`):

| Stem | Mean volume | Integrated |
|---|---|---|
| `drums.mp3` | −11.8 dB | −13.0 LUFS |
| `other.mp3` | −30.1 dB | −27.6 LUFS |
| `bass.mp3` | −91.0 dB | −70.0 LUFS |
| `guitar.mp3` | −91.0 dB | −70.0 LUFS |
| `piano.mp3` | −91.0 dB | −70.0 LUFS |
| `vocals.mp3` | −91.0 dB | −70.0 LUFS |

**Four of the six stems are digital silence.** A silent `vocals.mp3` is the expected and welcome
confirmation that `force_instrumental: true` worked. But `bass.mp3` is silent too, on a clip whose
band analysis puts **76.9 % of its total energy below 60 Hz** — so the separator did not split the
sub bass out at all; the kick and the sub both went into `drums`, and the filtered chord went into
`other` at 18 dB below it.

**Consequence for the product thesis.** The Endel-style architecture is stem layering — the app holds
a library of separate elements and recombines them. If the plan were "generate a mix with ElevenLabs,
separate it into stems, then recombine", this result says that path does not work on this material:
one call returns one loud drums-plus-sub stem, one quiet everything-else stem, and four empty files.
It is a mix separator built for a band, run on music that has no band in it. Generating the layers
separately (one call per element) is the alternative worth testing next, and it is untested.

Note also the licence constraint that sits over all of this: ElevenLabs' "Music Libraries &
Repositories" clause is **Prohibited on every self-serve tier**, and it is written broadly enough to
cover building a catalogue of Output for licensing to third parties. That is a separate question from
whether the stems are technically usable, and it is not resolved by this test.

## Spend

| Item | Basis | Cost |
|---|---|---|
| 6 × 60 s music generation | 6.0 min @ $0.15/min (published card) | **$0.90** |
| 1 × stem separation | Not priced on the published card; billing basis unknown | unknown, assumed 0 for this budget |
| **Total against the $3 cap** | 7 API calls of a hard cap of 8 | **≈$0.90** |

No call failed; no retry was needed; one call of the eight-call budget is unspent.

## Unblinded first listen (Daniel, 2026-09-02)

Heard `el-a-1.mp3` and `el-b-2.mp3` unblinded, as a ballpark check only: "for the first shot, really good!" Not a test result; these two clips are now known to him and must be excluded from the blind set.

Follow-up feedback (Daniel): "definitely elements that need to be worked on — Endel sounds really fat and bassy, thick like in a real techno club; the clips are not. Not sure if it is a mastering thing." Objective correlate: the clips put 87–97% of energy <150 Hz with a starved 150–500 Hz body; "thick" lives in ~80–400 Hz (kick body, bass harmonics, chord low-mids) plus saturation/glue. Test planned: apply a mastering chain to the same clips and re-listen (isolates mastering from mix balance).

## 2026-09-02 ~03:20 CEST — Daniel, unblinded, headphones: first Magenta RT2 clip

- File: `mrt2-a-1.wav` (mrt2_small, warm start, Palette A prompt).
- Verdict, verbatim: "the ingredients are not bad — but there is no rhythm, it sounds wrong." Earlier in the same listen: "not music, just weird sounds, no real rhythm."
- Reading: timbre/texture acceptable, temporal structure absent. Consistent with a 400M-param real-time model that has no beat grid. Magenta is not a candidate as a whole-track source; at most a texture-stem source layered over a coded rhythm section.
- Effect on the blind set: mrt2-a-1 is now known to Daniel → excluded. Remaining mrt2 clips only enter Gate 1 if an objective rhythm screen (tempo peak ratio, beat-interval CV) passes.
- Synth arm not yet auditioned by Daniel at this point.

## 2026-09-02 ~03:30 CEST — Daniel, unblinded, headphones: first coded-synthesis clip

- File: `synth-a-11.wav` (arm 2, Palette A, mastered −14 LUFS copy).
- Verdict, verbatim: "not bad at all."
- Reading: the rhythm section and structure from code work; the remaining lever is sound quality (thickness/warmth/organic drift), i.e. the sound source, not the sequencer. Direction for arm 2: keep the grid and stem layout, swap the numpy tones for real synth/drum-machine emulations once the instrument research ranks a pip-only, licence-clean stack.
- Effect on the blind set: synth-a-11 is now known to Daniel → excluded (joins el-a-1, el-b-2, mrt2-a-1).
- Score so far, unblinded, one clip each: ElevenLabs "really good for a first shot, but thin"; Magenta "no rhythm, sounds wrong"; coded synthesis "not bad at all."

## 2026-09-02 ~04:00 CEST — Daniel, unblinded, headphones: synth-a-11 v1/v2/v3

- Files: `synth-a-11-v1.wav`, `-v2`, `-v3` (pad down, bass fatter, motif generator added to palette A at 0.85/1.50/1.70).
- Verdict, verbatim: "all three ... like a drunk child pressing buttons."
- Reading: the base clip (no motif) was "not bad at all"; the only new melodic element across all three is the motif generator, so the motif's note/timing choices read as random. "Hypnotic" means a short fixed phrase repeating on the grid, not stochastic note picking. Bass/pad changes cannot be judged from this listen because the motif dominates.
- Action: motif becomes a fixed 2–3 note phrase, repeated every 1–2 bars, identical each time, through the tempo-synced delay; no random note selection, no random timing. Re-audition before any further balance judgements.
- Blind-set effect: all three variants known to Daniel → excluded.

## 2026-09-02 ~05:30 CEST — Daniel, unblinded, headphones: surge round 2 (r2)

- Files: `surge-a-11-r2.wav`, `surge-a-11-v1-r2.wav`, `surge-b-41-r2.wav` (LISTEN-NOW 01–03).
- Verdict, paraphrased closely: "the arrangement is not bad." All three are "very paddy" — the sustained washy chord element dominates every clip. "The sounds themselves, the instruments, the bass, everything sounds very generic, very computer-like; it's missing the right nice real synthesizer sounds."
- Reading: sequencer/arrangement rules from the pattern book pass; the sound source fails. Patches built from parameters by an agent with no ears = generic. Two levers: (1) human-designed patches (Surge factory library, OB-Xd, Dexed, TAL) and analogue-modelled synths; (2) chord/stab element far smaller, shorter, drier — second time Daniel has asked for less pad.
- Process change: audition sounds individually (4-bar solo renders of candidate bass/hook/chord patches in LISTEN-NOW) and let Daniel pick before the next arrangement render. His ear is the patch designer.
- Blind-set effect: the three r2 clips known to Daniel → excluded.

## 2026-09-02 ~07:00 CEST — Daniel, on phone via the Listening Room player: round 3 audition

- Verdict, paraphrased closely: the basses "sound terrible"; "we need something way more bassy, deep, wide" — first priority, because a bad bass makes every other sound impossible to evaluate. Overall "all these sounds sound very generic and kind of bad" (OB-Xd presets included).
- Reading: preset-picking by name does not produce a club bass; the bass needs a designed layer stack (mono sub + saturated body + width on the harmonics only), and Daniel's ear must approve the bass ALONE before any other element is auditioned.
- Action: round 4 redirected to bass-only audition over kick only; sampled real synths (Legowelt) and Riemann bass loops included as candidates; no full mixes until a bass passes.
- Blind-set effect: none new (audition clips are not blind candidates).

## 2026-09-02 ~07:45 CEST — Daniel, phone player: round 4 bass-only audition

- Verdict, verbatim: "They all sound the same. ... sound computer-generated. It doesn't sound like it's part of a library."
- Measured on the laptop (long-term spectrum, 8 kHz mono): the eight clips are within ~1 dB of each other in EVERY band (sub<80: 48.1–50.1 dB, body 80–250: 48.7–49.6, mid: 39.2–40.1, hi: 31.3–32.2; RMS −11.8 to −13.1). Largest smoothed spectral difference between any pair 2–6.6 dB at narrow spots. Daniel's ear is right: the layer stack (sine sub + body band-limited to 78–205 Hz + drive + −14 LUFS master) erases the source; a Prophet 600, a Jupiter 8 and a synthetic square come out identical.
- Conclusion for the process: four rounds of "agent designs the sound by measurement, Daniel rejects" — sound design by numbers does not converge. Sequencer/arrangement passed by ear (r2); SOUND needs either professionally produced material used as-is or a human sound designer. Measurement stays as a screen only.
- Options put to Daniel: (A) Riemann free Techno Starter (€0 Shopify checkout, his click) and/or 1–2 paid hypnotic/dub-techno packs (~€20–30 each) used as-is with minimal processing, engine = layering/crossfading; (B) micro-commission a sound designer (~€100–300) for a bass/kick/chord/hook stem set in our key/tempo; (C) both.

## 2026-09-02 ~09:30 CEST — Daniel, phone player: round 5 (ACE-Step 2B turbo + Lyria RealTime)

- Overall, verbatim: "definitely massive improvement compared to yesterday."
- ACE-Step (acestep-room, clips 01–08): "the sounds themselves are high quality. the arrangement is very boring though." 01 liked most "but it's too lively, it needs to be much more monotone, but good start." 02: "I like the fat bass line." 04: "tries to be hypnotic, but it's just noisy instead — the mix is bad too." 05 onwards: not liked.
- Lyria RealTime (listening-room, clips 01–08): "the quality is awesome. the arrangements are much more interesting. this could very well be our winner." 01 (t118-d30-b30): "great, but that paddy melody is too much, annoying — too spacy." 02 (t118-d40-b40): same paddy sounds, too much. General: "none of these tracks are hypnotic — just minimal and spacy. we need to stay a lot more minimal, Berlin techno."
- Reading: Lyria is the lead engine; ACE-Step parked (good sound, no arrangement control, model goes silent). Two defects to fix on Lyria: (1) the sustained pad/melody element — third round in a row where Daniel asks for less pad, and the prompt phrase "dubby chord stabs with delay" is the likely source; (2) "spacy, not hypnotic" = too much variation and reverb-wash, not enough locked repetition. Lyria RealTime takes text prompts and numeric config only, no audio reference upload (harness note, docs 2026-09-02).
- Action: round 6 = knob audition. Start from 01's settings, strip every pad/space word, add "monotonous, repetitive, dry" descriptors, then change ONE knob per clip (temperature, guidance, brightness, density, negative-weight "pad" prompt, only_bass_and_drums foundation, fixed seed reproducibility check) so each clip teaches what one knob does.
- Blind-set effect: all round-5 clips known to Daniel → excluded.

## 2026-09-02 ~11:00 CEST — Daniel, phone player: round 6 (Lyria knob audition, same seed)

- Verdict, verbatim: "this actually became worse, not better. ... it's going to be too unpredictable ... we have to go back to the drawing board. That doesn't work."
- Reading: stripping the pad words produced a near-empty sub-bass loop (measured 96.5% below 150 Hz); the single-knob changes did not move it towards "hypnotic Berlin techno" in a way Daniel could steer. Seed reproducibility is real (07 bit-identical to 00) so the problem is not randomness, it is that text+numbers cannot be steered to a specific taste. Lyria-as-songwriter is out; Lyria/Suno remain candidates only as a sound/idea SOURCE curated by a human, with structure from a deterministic engine or a producer in a DAW.
- Daniel pointed to EDM Tips, "My AI WARNING to music producers" (youtu.be/bfY2hfhEwaM, 8 May 2026, Will Darling). Its relevant claims: use generative AI as inspiration only (pull one chord/vocal into Ableton and build around it); stem-separate reference tracks to STUDY arrangement (when bass enters, what changes every 8 bars) — native in Ableton 12; Reinier Zonneveld runs a generative rig that listens to his live set and proposes ideas he mixes back in; and "commodity/background music ... AI is going to take a lot of that, and it's going to do it better and faster" — our product category by his definition, which he calls forgettable unless there is a brand/experience around it.
- Blind-set effect: all round-6 clips known to Daniel → excluded.
