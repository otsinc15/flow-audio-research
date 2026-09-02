# Lyria RealTime render harness

Records text-steered instrumental music from Google's **Lyria RealTime**
(`models/lyria-realtime-exp`, Gemini API, WebSocket streaming) to WAV, for the
hypnotic-techno ear test.

Docs read 2026-09-02:
- https://ai.google.dev/gemini-api/docs/realtime-music-generation
- https://ai.google.dev/gemini-api/docs/models/lyria-realtime-exp

## Install

```sh
python3.13 -m venv ~/.venvs/lyria
~/.venvs/lyria/bin/pip install google-genai
```

Verified against `google-genai` 2.21.0 on Python 3.13.

The API key is read from `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) in the
environment, falling back to `~/.claude/.env`. It is never printed or logged —
only the source it came from.

## Run

Validate a config without connecting to anything:

```sh
~/.venvs/lyria/bin/python lyria/render.py --batch lyria/batch.json --dry-run
```

**The 8-clip batch, one line:**

```sh
~/.venvs/lyria/bin/python lyria/render.py --batch lyria/batch.json --out-dir out
```

Writes `out/<name>.wav` per clip and prints a JSON stats array (sample rate,
chunk count, first-chunk latency, max inter-chunk gap, reconnects, any
safety-filtered prompts). `out/` is gitignored — **never commit audio.**

A single clip:

```sh
~/.venvs/lyria/bin/python lyria/render.py \
  --seconds 90 --bpm 118 --scale A_MINOR \
  --density 0.4 --brightness 0.35 --guidance 4 \
  --prompts "hypnotic minimal dub techno:1.0, deep sub bass:0.8" \
  --out out/probe.wav
```

## Steering mid-stream

`--steer-script script.json` takes a list of timed changes. `at_seconds` is
measured in **recorded audio**, not wall clock:

```json
[
  { "at_seconds": 30, "brightness": 0.5 },
  { "at_seconds": 60, "bpm": 124, "prompts": "hypnotic minimal dub techno:1.0, acid 303 line:0.5" }
]
```

Each step may set `prompts` or **any** `LiveMusicGenerationConfig` field —
`bpm`, `density`, `brightness`, `guidance`, `scale`, `temperature`, `top_k`,
`seed`, `mute_bass`, `mute_drums`, `only_bass_and_drums`,
`music_generation_mode`. Unknown keys are rejected rather than ignored. Two behaviours come straight from the docs and are implemented here:

- **The whole config is resent every time.** "You can't just update a parameter,
  you need to set the whole configuration otherwise the other fields will be
  reset back to their default values."
- **`bpm` and `scale` changes trigger `reset_context()`.** It doesn't stop the
  stream, but it is a hard transition. No other field needs it.

## Batches

`batch.json` — round 5, the 8 × 90 s tempo/density/brightness sweep described below.

`batch-round6.json` — round 6, a **knob audition**: one parameter changed per clip
against a fixed base and a **fixed seed**, so each difference is attributable to
that one knob. Covers `temperature`, `guidance`, `brightness`, `density`, negative-
weight prompts, a mid-stream `only_bass_and_drums` release, and a bit-exact repeat
of the base to prove the seed reproduces. Findings:
`research/ear-test/lyria-round6-2026-09-02.md`.

```sh
~/.venvs/lyria/bin/python lyria/render.py --batch lyria/batch-round6.json --out-dir out6
```

## The round-5 8-clip batch plan

`batch.json` — 8 × 90 s, same base prompt set throughout:

> `hypnotic minimal dub techno:1.0, deep sub bass:0.8, dry analog kick:0.6, dubby chord stabs with delay:0.6, sparse percussion:0.4`

with `scale: C_MAJOR_A_MINOR` (the A-minor enum — the model does not
distinguish relative keys) and `guidance: 4.0`.

| clip | bpm | density | brightness | steer |
| --- | --- | --- | --- | --- |
| `t118-d30-b30` | 118 | 0.3 | 0.3 | — |
| `t118-d40-b40` | 118 | 0.4 | 0.4 | — |
| `t118-d50-b50` | 118 | 0.5 | 0.5 | — |
| `t118-d40-bsweep` | 118 | 0.4 | 0.3 | brightness 0.30 → 0.55 over 60 s |
| `t122-d30-b30` | 122 | 0.3 | 0.3 | — |
| `t122-d40-b40` | 122 | 0.4 | 0.4 | — |
| `t122-d50-b50` | 122 | 0.5 | 0.5 | — |
| `t122-d40-bsweep` | 122 | 0.4 | 0.3 | brightness 0.30 → 0.55 over 60 s |

Three clips per tempo walk density and brightness together so the ear test can
tell "too sparse" from "too busy"; the fourth holds everything but brightness
so a slow rise is audible as the only moving part.

## What the API gives back

| | |
| --- | --- |
| Model | `models/lyria-realtime-exp` (experimental) |
| Output | Raw 16-bit PCM, **48 kHz, 2ch stereo** |
| Control latency | max 2 s |
| Input | **text only** — `Input: Text (Weighted prompts)`; no audio or image reference input exists |
| Vocals | none — instrumental only |
| Watermark | always applied (SynthID, per Google's Responsible AI policy) |

The harness reads the real sample rate out of each chunk's `mime_type`
(e.g. `audio/L16;codec=pcm;rate=48000`) and puts that in the WAV header, rather
than trusting the documented value. (The docs' JS sample contradicts itself and
shows 44100; the spec table and the model page both say 48 kHz.)

Safety-filtered prompts arrive as `filtered_prompt` on the server message and
are logged loudly — a filtered prompt is *silently ignored* by the model
otherwise.

## The other Lyria models (not used here)

Per https://ai.google.dev/gemini-api/docs/music-generation, the Gemini API also
exposes two **Lyria 3** models. They are a different product to Lyria RealTime
and are *not* rendered by this harness:

| | `lyria-3-clip-preview` | `lyria-3-pro-preview` |
| --- | --- | --- |
| Best for | short clips, loops, previews | full songs with verses/choruses |
| Duration | always 30 s | "a couple of minutes", steered by prompt |
| Output | MP3, 44.1 kHz stereo | MP3, 44.1 kHz stereo |
| API | Interactions API (`interactions.create`) | same |
| Input | text **and images** | text and images |

**Neither accepts a structured `bpm` or instrumental control.** There is no
config object at all — the docs' only guidance is "Be specific. Vague prompts
produce generic results. Mention instruments, BPM, key, mood, and structure for
the best output." So tempo and key are *prose inside the prompt*, not parameters,
and there is nothing equivalent to `density`, `brightness`, `scale` or
`mute_drums`.

They also **sing by default**: the response returns generated lyrics alongside
the audio (`interaction.output_text`), and instrumental-only has to be asked for
in words. Generation is single-turn — "Iterative editing or refining a generated
clip through multiple prompts is not supported" — so there is no mid-stream
steering, and results are explicitly non-deterministic between calls.

For a continuously-steered functional-audio product that shape is wrong, which is
why the ear test uses Lyria RealTime. Both Lyria 3 models watermark with SynthID.

## Terms

Google's Gemini API [Additional Terms of Service](https://ai.google.dev/gemini-api/terms)
on ownership of generated output:

> "Google won't claim ownership over that content. You acknowledge that Google
> may generate the same or similar content for others and that we reserve all
> rights to do so."

and on responsibility:

> "You're responsible for your use of generated content, and for the use of that
> content by anyone you share it with."

**No explicit commercial-use grant or prohibition for music output was found**
on either Lyria page or in those terms — the terms neither authorise nor forbid
commercial use in so many words, and they place no production/commercial
restriction on Preview or Experimental models beyond "The Services include
experimental technology and may sometimes provide inaccurate or offensive
content." Data handling does differ by tier: on unpaid use "Google uses the
content you submit to the Services and any generated responses to provide,
improve, and develop Google products and services and machine learning
technologies", whereas on paid use "Google doesn't use your prompts ... or
responses to improve our products." Treat commercial licensing as an open
question needing Google's own confirmation before anything ships.

## Notes and gotchas

- **API version is load-bearing.** The SDK builds the socket URL as
  `.../ws/google.ai.generativelanguage.{api_version}.GenerativeService.BidiGenerateMusic`.
  Default here is `v1alpha`, with one automatic retry on `v1beta` (what the docs'
  sample currently uses). Override with `--api-version`.
- **Prompt weights may not be `0`** — the harness rejects it up front. **Negative
  weights work**: `"ambient pads:-0.6"` is accepted by the API and acts as
  repulsion (verified live 2026-09-02, no error and no `filtered_prompt`).
- **Prompt text cannot contain a comma** in the `"text:weight,..."` string form —
  the comma is the delimiter, so `"ambient pads, spacey reverb:-0.6"` silently
  becomes *two* prompts, the first at the default weight 1.0. Use separate
  prompts, or the JSON list form (`[{"text": ..., "weight": ...}]`) in a batch
  file. Always check `--dry-run` output before spending API time.
- **`seed` makes renders bit-exact.** Two runs of the same config and seed came
  back byte-identical (Pearson r = 1.0000). Pin a seed whenever you want to change
  one parameter and attribute the difference to it. Not promised across model
  versions — `lyria-realtime-exp` is experimental.
- PCM streams to `<out>.wav.part` first, so a crashed run leaves salvageable
  audio; the `.part` is removed once the WAV header is written.
- A dropped stream reconnects up to 3 times and continues appending (audible
  seam, logged). No chunk for 30 s counts as a drop.
- **No session length limit is documented** on either page. Assume long runs may
  be cut and rely on the reconnect path.

Observed live on 2026-09-02 (laptop, single API key):

- `v1alpha` is the version that actually works. `v1beta` — what the docs' Python
  sample shows — returns **HTTP 404** on the websocket upgrade.
- Real `mime_type` on the wire is `audio/l16;rate=48000;channels=2`, confirming
  48 kHz stereo. Chunks arrive roughly every 2 s of audio.
- **It does not stream at 1x realtime**: 90 s of audio took ~125 s of wall clock,
  with inter-chunk gaps up to ~5 s. Budget ~1.4x the clip length per render.
- Sessions drop with `APIError: 1006 abnormal closure [internal]` at random.
  This is transient — a 60 s and several 90 s renders completed clean afterwards
  — but it is frequent enough that the reconnect path is load-bearing, not
  decorative. A reconnect restarts the model's musical context, so the seam is
  audible; the stats JSON reports `reconnects` per clip so a seamed clip can be
  thrown out rather than trusted.
- Lyria RealTime is **text-only**. Never send reference audio — there is no
  input for it, and the licensing questions that come with it stay off the table.
