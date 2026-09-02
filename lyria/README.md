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

Each step may set `prompts`, `bpm`, `density`, `brightness`, `guidance` or
`scale`. Two behaviours come straight from the docs and are implemented here:

- **The whole config is resent every time.** "You can't just update a parameter,
  you need to set the whole configuration otherwise the other fields will be
  reset back to their default values."
- **`bpm` and `scale` changes trigger `reset_context()`.** It doesn't stop the
  stream, but it is a hard transition. No other field needs it.

## The 8-clip batch plan

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
| Vocals | none — instrumental only |
| Watermark | always applied (SynthID, per Google's Responsible AI policy) |

The harness reads the real sample rate out of each chunk's `mime_type`
(e.g. `audio/L16;codec=pcm;rate=48000`) and puts that in the WAV header, rather
than trusting the documented value. (The docs' JS sample contradicts itself and
shows 44100; the spec table and the model page both say 48 kHz.)

Safety-filtered prompts arrive as `filtered_prompt` on the server message and
are logged loudly — a filtered prompt is *silently ignored* by the model
otherwise.

## Notes and gotchas

- **API version is load-bearing.** The SDK builds the socket URL as
  `.../ws/google.ai.generativelanguage.{api_version}.GenerativeService.BidiGenerateMusic`.
  Default here is `v1alpha`, with one automatic retry on `v1beta` (what the docs'
  sample currently uses). Override with `--api-version`.
- **Prompt weights may not be `0`** — the harness rejects it up front.
- PCM streams to `<out>.wav.part` first, so a crashed run leaves salvageable
  audio; the `.part` is removed once the WAV header is written.
- A dropped stream reconnects up to 3 times and continues appending (audible
  seam, logged). No chunk for 30 s counts as a drop.
- **No session length limit is documented** on either page. Assume long runs may
  be cut and rely on the reconnect path.
- Lyria RealTime is **text-only**. Never send reference audio — there is no
  input for it, and the licensing questions that come with it stay off the table.
