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
