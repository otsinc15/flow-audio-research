# AI music / audio production options — cited capability matrix

**Compiled 2026-09-02.** Every claim below traces to a file in this directory (`src-*.txt` for primary
pages, `sonar-*.json` for raw Perplexity responses). Where a fact could not be verified from a primary
source it says **not found** — nothing here is inferred or guessed.

Use case this matrix was built against: producing 20+ minute hypnotic, vocal-free minimal / dub-techno
focus music as **separate stems** (kick, bass/drone, pads, textures, hats) that a playback engine can
layer and crossfade endlessly.

No recommendations, no strategy — facts only.

---

## Fetch limitations (read this before trusting any gap)

Three source classes refused this environment's fetchers on 2026-09-02:

| Source | Result |
|---|---|
| `reddit.com` (search + JSON API + WebSearch) | HTTP 403 / domain blocked |
| `reuters.com` | HTTP 401 |
| `bbc.com`, `bbc.co.uk`, `apnews.com` | domain blocked to the fetcher |

Consequences: (a) the lawsuit section is sourced to the **companies' own PRNewswire press releases**
rather than to Reuters/BBC, which is arguably better evidence but does not satisfy the "verify with
Reuters/Bloomberg/BBC" instruction — treat the current *litigation status* items as unverified;
(b) the "user-reported quality" column is thin, because Reddit — where nearly all genre-specific AI-music
quality talk lives — is unreachable. Hacker News comments (`src-hackernews-user-comments.txt`) were
harvested instead via the Algolia API, and two Perplexity `sonar-pro` passes were run; both are recorded
raw. Perplexity itself reported it could not retrieve verbatim Reddit quotes.

---

## The matrix

Legend: **✅** yes · **❌** no · **⚠️** partial/conditional · **?** not found.

### Cloud generation services

| | ElevenLabs Music API | Suno | Udio | Stable Audio 2.5 / 3.0 (cloud) | Google Lyria 3 | Google Lyria RealTime | Mubert API |
|---|---|---|---|---|---|---|---|
| **Official API?** | ✅ `POST /v1/music`, `/v1/music/compose-detailed`, `/v1/music/stem-separation` | ❌ **No public API.** "Suno does not currently offer an official public API." (MBW, 2026-07-02). Exploratory partner intake form opened 2026-07-01 | ? none documented anywhere in the ToS | ✅ `POST /v2beta/audio/stable-audio-2/*` and `/v2beta/audio/stable-audio/text-to-audio` | ✅ Gemini API `lyria-3-clip-preview`, `lyria-3-pro-preview`; also Vertex | ✅ WebSocket `models/lyria-realtime-exp` (experimental) | ✅ `music-api.mubert.com/api/v3` |
| **Max clip length** | API schema: `music_length_ms` **3 000–600 000 ms (10 min)**; docs FAQ says "minimum duration of 3 seconds and a maximum duration of 5 minutes" — **the two ElevenLabs sources disagree** | **8 min** in one shot on V4.5/V5, plus Extend | ? | SA2.x **190 s**; SA3 `duration [1..380]` = **380 s (6 m 20 s)** | Clip = **30 s**; Pro = "A couple of minutes (controllable using prompt)" | Unbounded live stream (session-based; `play`/`pause`/`stop`/`reset_context`) | **15 s – 25 min** (`max_track_duration: 1500`); longer "by request" on enterprise |
| **Outputs stems?** | ⚠️ **Separation, not native multitrack.** `POST /v1/music/stem-separation` returns "ZIP archive containing separated audio stems". Plan table row "API Access (Stems, Streaming, Word Timestamps)" = Yes on Starter and above | ⚠️ **Yes, in Suno Studio only** (Premier plan). "Multitrack — Exports all tracks as stems… giving you maximum flexibility for mixing in your DAW"; all exports are WAV | ? no stem feature documented; **downloads of any kind are contractually prohibited** | ❌ no stem endpoint exists in the API reference | ❌ not mentioned in the docs | ❌ single stereo stream | ⚠️ **marketing claim only** — mubert.com/api says tracks are built from "drums, percs, hats, claps, bass, mids, leads, fx, vocals, pads, riser, and impact which can be grouped into stems". **The v3 API reference documents no stem-level output**; it exposes `mode: track / loop / jingle / mix`, bitrate, format, intensity |
| **Audio-to-audio / reference / continuation** | ✅ Audio Reference (upload ≈30 s, Music v2, all paid plans); `conditioning_ref` + `AudioRefChunk` (reference a prior ElevenLabs `song_id` + time range, `condition_strength` low→xhigh); inpainting via `source_from` / `store_for_inpainting` | ✅ Studio: upload audio, record audio, Remix/Edit, Extend | ? | ✅ `audio-to-audio` (input 6–190 s for SA2.x, 6–380 s for SA3, `strength` 0–1) and `inpaint` (`mask_start` / `mask_end`) | ❌ "multimodal inputs (text and images)"; no audio input documented | ⚠️ text `WeightedPrompt`s only (plus `bpm`, `temperature`, scale); no audio input | ? not documented in the v3 reference |
| **Runs locally on Apple Silicon** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Commercial licence on paid tier (quoted)** | Media Rights, every self-serve tier: *"All online and offline commercial use permitted, except film, TV, radio, & Studio Games."* **But** *"Music Libraries & Repositories: Prohibited"* on every self-serve tier, defined as *"any arrangement in which Customer creates or permits others to create a library, catalogue, database, or other repository of Output with the intent of licensing it or otherwise making it available to third parties."* Reseller Rights also Prohibited on all self-serve. Eligibility: Free/Starter/Creator/Pro *"For Individual Use Only"*; Scale *"fewer than 10 employees"*; Business *"fewer than 50 employees"* | *"if you are a user who has subscribed to the Pro or Premier paid tier of the Service, Suno hereby assigns to you all of its right, title and interest in and to any Output owned by Suno… However, due to the nature of machine learning, Suno makes no representation or warranty to you that any copyright will vest in any Output."* Free/Basic = non-commercial + attribution | **None.** *"you may use Output solely for your personal and non-commercial purposes, provided that you may not download any copies of your Output from the App for any purpose"* (§6.3); *"exploit the Services, any Output, or the outputs of other users for any commercial purpose"* is a listed prohibition (§5.2); Udio owns the Output (§6.1) | ⚠️ **not verified.** The Stability Platform ToS page did not render a commercial-output clause to this fetcher. What is verified: *"Stable Audio models were exclusively trained on licensed data from the AudioSparx music library, honoring opt-out requests… Additionally, Stable Audio 3.0 was pre-trained on licensed data from Freesound"* and *"We do not allow copyrighted content to be uploaded to our platform"* | ⚠️ *"All generated audio includes a SynthID audio watermark… imperceptible to the human ear"*; both models are `-preview`. Commercial clause **not found** on the model page | *"Watermarking: Output audio is always watermarked for identification following our Responsible AI principles."* Commercial clause **not found**. Model is flagged experimental, "Latest update: May 2025" | *"Royalty-free"*, *"DMCA-free"*, *"Cleared for monetization"*; *"Sub-licensing options are available on paid tiers"* (mubert.com/api). Full licence text **not found** — mubert.com/license 404s and mubert.com/api/pricing returns Cloudflare error 1101 to curl |
| **Price** | **$0.15 / minute** ("5 minute duration limit", "Commercial use licensing on Starter+ plans", "44.1kHz, 128-192kbps audio"). Monthly download caps: Starter 30 min, Creator 250, Pro 500, Scale 1,500, Business 4,000 | ? Studio requires the **Premier** plan; the price list lives behind `app.suno.ai/account` and was not fetchable | ? behind login | 1 credit = $0.01. **SA2.5 = 20 credits = $0.20** per ≤3-min generation; **SA3 = 26 credits = $0.26** per ≤6 m 20 s generation. 25 free credits to start | Clip (30 s) **$0.04/song**; Pro (full song) **$0.08/song**. Vertex also lists Lyria 2 at **$0.06 / 1 count** | **not found** — `lyria-realtime` appears nowhere in the Gemini API pricing page | Trial **$49/mo** (100 generations, 100 streaming min); Startup **$199/mo** (5,000/5,000); Startup+ **$499/mo** (30,000/30,000); Custom |
| **Audio format** | MP3 44.1 kHz 128–192 kbps and WAV; API `output_format` also offers `pcm_48000`, `mp3_48000_192` (v2 default `mp3_48000_192`) | WAV from Studio | n/a (no downloads) | mp3 or wav, 44.1 kHz stereo | "44.1 kHz high-fidelity stereo"; MP3 default, WAV available on Pro | Raw 16-bit PCM, **48 kHz**, stereo; control latency max 2 s | wav / mp3, bitrate 32–320, default 128 |
| **User-reported quality for techno/ambient** | **not found** (no dated genre-specific report retrievable) | Thin and non-genre-specific — see §"User-reported quality" below | Thin and non-genre-specific — see below | **not found** | **not found** | **not found** | Weak second-hand only: a 2026-07-30 aggregator summary reports users saying *"genres miss the brief"* and *"tracks feel too similar or generic"* (via Perplexity, `sonar-mubert-endel-quality.json`) — **unverified, aggregator not fetched directly** |
| **Source files** | `src-elevenlabs-music-api.txt`, `src-elevenlabs-docs-music-md.txt`, `src-elevenlabs-api-compose.txt`, `src-elevenlabs-api-compose-detailed.txt`, `src-elevenlabs-separate-stems.txt`, `src-elevenlabs-pricing.txt`, `src-elevenlabs-music-terms.txt`, `src-elevenlabs-music-model-terms.txt`, `src-elevenlabs-plan-rights-table.txt` | `src-suno-terms.txt`, `src-suno-help-commercial.txt`, `src-suno-help-song-length.txt`, `src-suno-help-intro-studio.txt`, `src-suno-help-exporting-studio.txt`, `src-mbw-suno-api.txt`, `src-thirdparty-sunoapi-org.txt` | `src-udio-terms.txt`, `src-pr-umg-udio.txt` | `src-stability-api-reference-audio.txt`, `src-stability-pricing.txt` | `src-google-lyria3-docs.txt`, `src-google-gemini-pricing.txt`, `src-vertex-pricing.txt` | `src-google-lyria-realtime-docs.txt`, `src-google-lyria-realtime-model.txt`, `src-google-live-music-api.txt` | `src-mubert-api-docs.txt`, `src-mubert-api-overview.txt` |

### Local / open-weights models

| | Stable Audio Open 1.0 | Stable Audio Open Small | Magenta RealTime (v1) | **Magenta RealTime 2** | MusicGen / AudioCraft | musicgen-mlx | heartlib-mlx (HeartMuLa) | Demucs / HT-Demucs v4 |
|---|---|---|---|---|---|---|---|---|
| **Official API?** | ❌ weights only | ❌ weights only | ❌ weights + Python lib | ❌ weights + Python lib + C++ engine + AUv3 plugin | ❌ weights + Python lib | ❌ CLI | ❌ CLI + web UI | ❌ CLI/Python |
| **Max clip length** | "variable-length (up to 47s) stereo audio at 44.1kHz" | "variable-length (up to 11s)" | ? (v1 code moved to `v1_legacy` branch) | Unbounded continuous stream; "20s effective receptive field" of context for both sizes | Trained/generated at 30 s; docs example `set_generation_params(duration=8)`; longer via continuation | Benchmarks quoted for 8 s clips | `--duration` flag; 10–20 s in the README examples | n/a (separator) |
| **Outputs stems?** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **This is the stem tool.** "four stereo wav files sampled at 44.1 kHz: `drums.wav`, `bass.wav`, …" plus `vocals`/`other`; `--two-stems=vocals\|drums\|bass` for 2-stem splits |
| **Audio-to-audio / reference / continuation** | ? | ? | ? | ✅ **audio + text + MIDI.** MusicCoCa embeds "Music audio waveforms, 16kHz mono, or text"; the LLM takes "(Context) SpectroStream tokens", "(Style) 12 MusicCoCa tokens", "(MIDI) 128-dim multihot vector" per frame | ✅ melody conditioning (`generate_with_chroma`, `musicgen-melody` / `-melody-large`); audio continuation supported in the training/eval code | Text-to-music only in the CLI (`-m` picks the HF model) | Tags + optional lyrics | Input is the audio to separate |
| **Runs locally on Apple Silicon** | ⚠️ PyTorch; **no official MLX port found** | ⚠️ model card points at an "Arm Learning Path" guide for "maximum performance on Arm CPUs" / mobile; **no Apple-Silicon claim on the card** | ? | ✅ **Yes, and this is its headline feature.** "Real-time streaming requires Apple Silicon (M-series)." `mrt2_small` (230M) "runs real-time on any Apple Silicon Mac, including Air models"; `mrt2_base` (2.4B) needs a Pro/Max chip. C++ engine `magentart::core` "for efficient streaming audio generation on Apple Silicon MacBooks", MLX backend, AUv3 plugin, standalone macOS app | ⚠️ PyTorch/MPS | ✅ MLX. "musicgen-small 300M, 8s audio in 6.3s, **1.3x** realtime"; "musicgen-stereo-large 3.3B, ~24s, 0.3x realtime" on M4 Max | ✅ MLX. "2x faster than PyTorch MPS on Apple Silicon"; "32GB+ unified memory recommended"; HeartMuLa-3B ≈6 GB | ✅ runs on CPU (`-d cpu`, "processing time should be roughly equal to 1.5 times the duration of the track"); README links `docs/mac.md` for macOS |
| **Commercial licence (quoted)** | **Stability AI Community License.** "This Agreement is intended to allow research, non-commercial, and limited commercial uses of the Models free of charge… preserves free access to the Models for people or organizations generating annual revenue of less than US $1,000,000." "If You are using or distributing the Stability AI Materials for a Commercial Purpose, You must register with Stability AI." Attribution required: retain the notice and "prominently display 'Powered by Stability AI'" | same Community License; "For commercial use, please refer to https://stability.ai/license" | ? | ✅ **cleanest of any model here.** "the codebase is licensed under Apache 2.0, and the model weights under Creative Commons Attribution 4.0 International"; **"Google claims no rights in outputs you generate using Magenta RealTime 2. You and your users are solely responsible for outputs and their subsequent uses."** Trained on "~71k hours of stock music from multiple sources, mostly instrumental" | ❌ **Not commercially usable.** "Code is released under MIT, model weights are released under **CC-BY-NC 4.0**" (Attribution-**NonCommercial** 4.0) | inherits MusicGen's CC-BY-NC-4.0 weights → **not commercially usable** | ✅ code **Apache 2.0**; `HeartMuLa/HeartMuLa-oss-3B` model card `license: apache-2.0` | ✅ **MIT License**, "Copyright (c) Meta Platforms, Inc. and affiliates" |
| **Price** | free (subject to licence) | free | free | free | free (non-commercial only) | free | free | free |
| **Output format** | 44.1 kHz stereo | 44.1 kHz stereo | ? | **48 kHz stereo** (SpectroStream codec: "Music audio waveforms, 48kHz stereo") | 32 kHz (config `musicgen_melody_32khz`) | WAV | WAV | 44.1 kHz stereo WAV per stem |
| **User-reported quality for techno/ambient** | **not found** (see caveat below) | **not found** | **not found** | **not found** as a dated user quote. Google's own claim: "At the time of release, Magenta RealTime 2 represents the only open weights model supporting real-time, continuous musical audio generation with low latency control (~200ms)" | **not found** | **not found** | README claims "comparable quality to Suno" — **vendor claim, not a user report** | **not found** |
| **Source files** | `src-hf-stable-audio-open-1.txt`, `src-stability-community-license.txt`, `src-stability-license.txt` | `src-hf-stable-audio-open-small.txt`, `src-stability-community-license.txt` | `src-hf-magenta-realtime.txt`, `src-magenta-site.txt` | `src-magenta-rt-github.txt`, `src-hf-magenta-realtime-2.txt`, `src-magenta-rt-docs-models.txt`, `src-magenta-rt2-page.txt`, `src-magenta-rt2-apps.txt` | `src-audiocraft-readme.txt`, `src-audiocraft-musicgen-docs.txt`, `src-audiocraft-license.txt`, `src-audiocraft-weights-license.txt`, `src-hf-musicgen-large.txt` | `src-musicgen-mlx-readme.txt` | `src-heartlib-mlx-readme.txt`, `src-hf-heartmula-3b.txt` | `src-demucs-readme.txt`, `src-demucs-license.txt` |

### Playback / layering engines

Question asked: *can a 2-person team reuse this for Endel-style stem layering in an iOS app?*

| Engine | What it is | iOS? | Licence / price (quoted) | Fit for endless stem layering | Source |
|---|---|---|---|---|---|
| **FMOD** | Adaptive game-audio middleware + authoring tool | ✅ ("Platforms: All" on every tier) | Games: Indie (dev budget <$600k) "Free or $2,000"; Basic ($600k–$1.8M) $6,000; Premium (>$1.8M) $18,000 — all per game, lifetime, "FMOD Logo Required" (waiver $6k/$12k). Free Indie needs "less than $200k revenue per year". **A focus-music app is not a game:** "For pricing on non-game projects, such as Location Based Entertainment (LBE), automotive, simulators, embedded systems, engines, B2B products, hardware installations… contact us for custom license models." → **price for this use case is not published** | Purpose-built for exactly this (multi-track adaptive music with transitions) | `src-fmod-licensing.txt` |
| **Wwise** | Adaptive game-audio middleware + authoring tool | ✅ | Page is titled **"Wwise for Games"**. Indie: **Free**, "Production Budget: Less than $250K", "Sound Files / Media Assets: Unlimited", "All Engine Features", **"Royalty Free (0%)"**. Pro from **$8,000**, Premium **$25,000**, Platinum **$45,000**. Non-game licensing terms **not found** on this page | Same class of tool as FMOD; interactive-music hierarchy is designed for layering/crossfading | `src-wwise-pricing.txt` |
| **Tone.js / Web Audio** | JS audio framework | ⚠️ browser/WebView only | **MIT License, Copyright (c) 2014-2025 Yotam Mann** | Free and unrestricted, but you are writing the layering logic yourself; not a native iOS audio graph | `src-tonejs.txt`, `src-tonejs-license.txt` |
| **AudioKit** | "audio synthesis, processing, and analysis platform for iOS, macOS (including Catalyst), and tvOS" (Swift) | ✅ native | MIT (badge on the README) | Native Swift building blocks; again, you author the sequencing/crossfade logic | `src-audiokit-github.txt` |
| **Elementary Audio** | "A JavaScript library for digital audio signal processing… both natively and in the browser" | ⚠️ "natively" claimed; iOS support not stated on the landing page | not stated on the landing page | Declarative DSP graph; not an adaptive-music system out of the box | `src-elementary-audio.txt` |
| **RNBO (Cycling '74)** | "take Max-like patches, export them as portable code… export to C++ or Web Assembly code for your desktop, mobile, or web applications" | ⚠️ "mobile" claimed generically | Terms not fetched | Lets a non-programmer author the layering logic in Max and export it — but it is a DSP export path, not a stem-scheduling engine | `src-rnbo-cycling74.txt` |
| **Endlesss** | Consumer "online multiplayer loop station" app, "now in the care of HabLab London… founded by Imogen Heap" | app, not an SDK | n/a | **Not reusable** — it is an end-user product, not a library | `src-endlesss-site.txt` |
| **Ableton Live + Max for Live** | Desktop DAW | ❌ not embeddable in an iOS app | n/a | Production tool for *making* the stems, not for shipping playback | `src-ableton-max.txt` |
| **Bitwig** | Desktop DAW | ❌ | n/a | Same | `src-bitwig-pricing.txt` |

**What Endel itself does** (primary + on-record founder quote):

> "The sound logic and elements are pre-designed by our sound team and assigned to every soundscape.
> Driven by the core logic, with any input change the sound adapts on-the-fly." — endel.io/technology

> "The soundscapes are stem-based — professional music industry jargon for snippets of sounds, think of
> them as samples. The app has a huge library of samples and stems, and the algorithm picks the right
> stems to sequence the audio together." — TechCrunch, 2022-05-20

> "Some of the soundscapes on the app are done in collaboration with some of the biggest artists on the
> planet… **They prepare a stem pack, a sound pack. They never submit a musical composition.** They just
> are the building blocks that the algorithm then uses to assemble tracks on the fly."
> — Oleg Stavitsky, CEO & co-founder, Endel, TechCrunch, 2022-05-20

Endel's engine is proprietary and patented: "Endel Pacific is the patented technology that powers our
apps and integrations." Sources: `src-endel-technology.txt`, `src-endel-about.txt`,
`src-techcrunch-endel-stems.txt`.

**No off-the-shelf "Endel-in-a-box" engine was found.** The closest reusable pieces are FMOD and Wwise
(both built for adaptive multi-layer music, both licensed primarily for games, both with unpublished
non-game pricing), and the low-level frameworks (AudioKit, Tone.js) where the layering logic is yours to
write.

---

## Per-tool notes

### ElevenLabs Music API

- **Endpoints.** `POST https://api.elevenlabs.io/v1/music` (prompt *or* `composition_plan`),
  `/v1/music/compose-detailed`, and `POST /v1/music/stem-separation`. Models `music_v1`, `music_v2`.
  Regional endpoints exist (US / EU / India / Singapore residency).
- **Structure control is unusually deep.** A `composition_plan` takes ordered `chunks`, each with `text`,
  `duration_ms` (3 000–120 000 per chunk), `positive_styles` / `negative_styles`, and
  `context_adherence: low|medium|high`. `force_instrumental: true` "guarantees that the generated song
  will be instrumental."
- **Stems.** The stem-separation endpoint takes an uploaded file and returns "ZIP archive containing
  separated audio stems. Each stem is provided as a separate audio file in the requested output format."
  It has a `stem_variation_id` parameter. The docs do **not** say how many stems or what they are named.
  It is *separation of a mix*, not native multitrack generation.
- **The licence clause that matters most for a stem-library product:**
  > "Music Libraries & Repositories means any arrangement in which Customer creates or permits others to
  > create a library, catalogue, database, or other repository of Output with the intent of licensing it
  > or otherwise making it available to third parties."

  and in the rights table that row reads **Prohibited** on Free, Starter, Creator, Pro, Scale and
  Business — "Custom" only on the two Enterprise tiers.
- Eligibility on Free/Starter/Creator/Pro is **"For Individual Use Only"**; Scale is capped at "fewer
  than 10 employees", Business at "fewer than 50 employees".
- Media Rights on every self-serve plan: "All online and offline commercial use permitted, **except film,
  TV, radio, & Studio Games**." Streaming Rights (putting output on Spotify et al.) are **Prohibited on
  Free and Starter**, Yes from Creator.
- Prohibited inputs include "any artist's… real name or stage name", "any song title", "any music
  label's name" — i.e. reference-track prompting by artist name is contractually out.
- Optional C2PA signing on MP3 output (`sign_with_c2pa`) on both compose and stem-separation.
- **Unresolved conflict:** the API reference allows `music_length_ms` up to 600 000 ms (10 minutes); the
  capability docs FAQ and the API pricing card both say 5 minutes. Not reconciled.

### Suno

- **No official API.** MBW, 2026-07-02: "Suno does not currently offer an official public API. While
  third-party developers have built unofficial API wrappers around Suno's platform, the company has not
  released self-serve developer access or published its own API documentation." CPO Jack Brody,
  2026-07-01: "Ahead of our partner powered model, we're exploring a developer API and want to hear from
  you before we start building… We plan to start with a curated group of partners."
  `docs.sunoapi.org` (saved as `src-thirdparty-sunoapi-org.txt`) is a **third-party wrapper**, not Suno.
- **Length:** "V4.5 and V5 can generate up to 8 minutes of music in one shot!" plus Extend.
- **Stems** exist only in **Suno Studio**, and "Studio is only available with a Premier plan". Export
  options are Full Song / Selected Time Range / **Multitrack** ("downloads individual tracks/stems as
  separate files to your device"). "All audio exports from Studio are delivered as high-quality WAV
  files." MIDI extraction from a stem costs 10 credits.
- **Ownership:** paid Pro/Premier subscribers get an assignment of Suno's interest in the Output, with an
  explicit warning that copyright may not vest at all. The help centre puts it plainly: "If you make
  music with the Basic (free) plan, Suno is the owner of the songs… If you make songs while subscribed to
  the Pro or Premier plan, you own the songs. Further, you are granted a commercial use license."
- **Planned platform change that directly affects a stem pipeline** (WMG press release, 2025-11-25):
  > "In 2026, Suno will make several changes to the platform, including launching new, more advanced and
  > licensed models. When the new models launch in 2026, the current models will be deprecated. Moving
  > forward, downloading audio will require a paid account. Suno will introduce download restrictions in
  > certain scenarios… Paid tier users will have limited monthly download caps with the ability to pay
  > for more downloads."

### Udio

Post-settlement Udio is, as written, unusable as a source of shippable material. Three clauses, all from
the ToS "Last Revised on November 12, 2025":

- §1.2 "**You may not download copies of any Output** or any other output generated by the Services."
- §5.2 (restrictions) "exploit the Services, any Output, or the outputs of other users for **any
  commercial purpose**".
- §6.1 "You agree that the Company and/or its licensors **own all right, title and interest in and to the
  Services and the Output**… to the extent ownership in any Output vests with you, you hereby assign and
  agree to assign all right, title and interest in and to such Output… to the Company."
- §6.3 "you may use Output **solely for your personal and non-commercial purposes**, provided that you
  may not download any copies of your Output from the App for any purpose."

This matches UMG's press release language: "Udio's existing product will remain available to users during
the transition period with creations **controlled within a walled garden** and the service amended in
multiple ways—including fingerprinting, filtering, and other measures—before the launch of the updated
service."

### Stable Audio (cloud, 2.5 / 3.0)

- Three endpoint families: `text-to-audio`, `audio-to-audio`, `inpaint`. SA3's text-to-audio is
  **asynchronous** — "returns a generation id immediately (HTTP 202). Poll `GET
  /v2beta/audio/results/{id}`."
- SA3 `duration [1..380]` seconds, default 190; `steps [4..8]`; `output_format` mp3 or wav; 26 credits
  ($0.26) flat. SA2.5: 190 s max, 20 credits ($0.20).
- `audio-to-audio` `strength`: "A value of 0 would yield audio that is identical to the input. A value of
  1 would be as if you passed in no audio at all. Minimum value for stable-audio-2.5 is 0.01." This is
  the closest thing to a reference-track workflow in the matrix.
- `inpaint` with `mask_start` / `mask_end` lets you regenerate a time window inside an existing track.
- Training data is licensed: "Stable Audio models were exclusively trained on licensed data from the
  AudioSparx music library, honoring opt-out requests and ensuring fair compensation for creators.
  Additionally, Stable Audio 3.0 was pre-trained on licensed data from Freesound."
- "We do not allow copyrighted content to be uploaded to our platform." Rate limit 150 req / 10 s.
- **No stems.**

### Stable Audio Open 1.0 and Open Small

- 47 s and 11 s maximum respectively, 44.1 kHz stereo, 0.5B params for Small.
- Both cards say only "For commercial use, please refer to https://stability.ai/license". That resolves
  to the **Stability AI Community License**, whose operative clause is:
  > "If You are using or distributing the Stability AI Materials for a Commercial Purpose, You must
  > register with Stability AI. If at any time You or Your Affiliate(s), either individually or in
  > aggregate, generate more than USD $1,000,000 in annual revenue… any licenses granted to You under
  > this Agreement shall terminate as of such date."

  Distribution also requires "prominently display 'Powered by Stability AI'". The licence is explicitly
  **revocable**.
- Open 1.0's training data is CC-licensed material: "486492 audio recordings, where 472618 are from
  Freesound and 13874 are from the Free Music Archive (FMA)… All audio files are licensed under CC0,
  CC BY, or CC Sampling+."
- **No MLX port was found** for either model. Open Small's card points at Arm CPU optimisation guidance
  (mobile), not Apple Silicon specifically.

### Google Lyria 3 and Lyria RealTime

- The page the brief called "Lyria 2" now documents **Lyria 3**: `lyria-3-clip-preview` (30 s clip,
  $0.04) and `lyria-3-pro-preview` ("full-length songs", "A couple of minutes (controllable using
  prompt)", $0.08). 44.1 kHz stereo; MP3 default, WAV available on Pro. "All generated audio includes a
  SynthID audio watermark." Vertex still lists **Lyria 2** at $0.06 / 1 count.
- **Lyria RealTime** is the interesting one for this use case and also the least production-ready:
  - `models/lyria-realtime-exp`, WebSocket, "persistent, bidirectional, low-latency streaming connection".
  - "Output format: Raw 16-bit PCM Audio · Sample rate: 48kHz · Channels: 2 (stereo)"; "Control latency:
    Maximum 2 seconds".
  - Steering is by `WeightedPrompt` blends plus `bpm`, `temperature`, scale; you can `play()`, `pause()`,
    `stop()`, `reset_context()`. Google's own JS sample in the docs literally prompts *"Minimal techno
    with deep bass, sparse percussion, and atmospheric synths"* at bpm 90.
  - "**Instrumental only:** The model generates instrumental music only."
  - "**Watermarking:** Output audio is always watermarked for identification."
  - Status "Experimental", "Latest update: **May 2025**", and **no price appears anywhere on the Gemini
    API pricing page**.
- **No stems** from either.

### Magenta RealTime and Magenta RealTime 2

MRT2 is the strongest technical fit in this matrix for on-device, endless, steerable instrumental audio —
and the cleanest licence.

- Repo `github.com/magenta/magenta-realtime` (v1 moved to the `v1_legacy` branch). Ships: open weights,
  a Python library with **JAX and MLX backends**, a **C++ inference engine `magentart::core` "for
  efficient streaming audio generation on Apple Silicon MacBooks"**, an **AUv3 plugin** for DAWs, and a
  standalone macOS app.
- Sizes: `mrt2_small` 230M ("runs real-time on any Apple Silicon Mac, including Air models") and
  `mrt2_base` 2.4B ("higher quality; requires a Pro Max chip for real-time streaming"). The README
  publishes a per-device real-time support table (M1 Air → M5 Max).
- Audio path: SpectroStream codec, "stereo 48kHz audio into tokens", 25 Hz frames, 16 kbps.
- Control: text **and audio** style embeddings (MusicCoCa) **and MIDI** — "(MIDI) 128-dim multihot vector
  representing the state of each MIDI pitch during this frame".
- Licence: "the codebase is licensed under Apache 2.0, and the model weights under Creative Commons
  Attribution 4.0 International"; plus **"Google claims no rights in outputs you generate using Magenta
  RealTime 2. You and your users are solely responsible for outputs and their subsequent uses."**
- Training: "~71k hours of stock music from multiple sources, mostly instrumental." Google notes "With
  specific prompting, this model has been observed to generate some vocal sounds and effects, though
  those vocal sounds and effects tend to be non-lexical."
- Google's own positioning claim: "At the time of release, Magenta RealTime 2 represents the only open
  weights model supporting real-time, continuous musical audio generation with low latency control
  (~200ms)."
- **No stem output.** It emits one stereo stream.

### MusicGen / AudioCraft, musicgen-mlx, heartlib-mlx

- **MusicGen weights are CC-BY-NC-4.0.** The model card is explicit: "Code is released under MIT, model
  weights are released under CC-BY-NC 4.0." The bundled `LICENSE_weights` file is
  Creative Commons **Attribution-NonCommercial** 4.0 International. This rules MusicGen — and anything
  downstream of its weights, including `musicgen-mlx` — out of a commercial product.
- MusicGen does support melody/audio conditioning (`generate_with_chroma`, `musicgen-melody` and
  `musicgen-melody-large`) and audio continuation, at 32 kHz.
- `musicgen-mlx` (github.com/andrade0/musicgen-mlx): "A clean MLX port of Meta's MusicGen for
  **inference-only** on Mac M1/M2/M3/M4". Self-reported on M4 Max with MLX 0.21: `musicgen-small` (300M)
  8 s of audio in 6.3 s = "1.3x realtime"; `musicgen-stereo-large` (3.3B) ~24 s = "0.3x realtime". The
  README warns "**Early release** — This is a working port but still rough around the edges."
- `heartlib-mlx` (github.com/Acelogic/heartlib-mlx): MLX port of HeartMuLa. Code **Apache 2.0**, and the
  `HeartMuLa/HeartMuLa-oss-3B` Hugging Face card carries `license: apache-2.0` — i.e. commercially
  permissive, unlike MusicGen. Claims "2x faster than PyTorch MPS on Apple Silicon", "32GB+ unified
  memory recommended for full inference", ~6 GB for the 3B model. The "comparable quality to Suno" and
  "Suno-Quality Output" lines are **the repo's own marketing**, not an independent measurement.

### Mubert API

- Real API with track generation (`POST .../v3/public/tracks`) and streaming
  (`GET .../v3/public/streaming/get-link`). The docs also document a **loop mode**: "Use the
  set-loop-state url to loop the latest part of the music composition (or turn the loop mode off)."
- Duration ceiling is visible in the licence object returned by the API: `"max_track_duration": 1500`
  (25 minutes). Composition `mode` can be `track`, `loop`, `jingle`, `mix`. Formats mp3/wav,
  bitrates 32–320, `intensity` low/…/high.
- **The stems claim needs care.** mubert.com/api (marketing) describes per-part control over "drums,
  percs, hats, claps, bass, mids, leads, fx, vocals, pads, riser, and impact which can be grouped into
  stems like drums, bass, leads, and vocals." **The v3 API reference that was fetched exposes no
  stem-level output** — no endpoint returns separated layers. Treat "Mubert outputs stems" as unverified.
- Licence language is marketing-page only ("Royalty-free", "DMCA-free", "Cleared for monetization",
  "Sub-licensing options are available on paid tiers"). `mubert.com/license` returns "Sorry! The page you
  were looking for doesn't exist." and `mubert.com/api/pricing` returns Cloudflare error 1101 to curl.

### Demucs / HT-Demucs v4

- MIT licensed, Meta. "The v4 version features Hybrid Transformer Demucs, a hybrid spectrogram/waveform
  separation model using Transformers." "This model separates drums, bass and vocals and other stems for
  any song."
- Output: "four stereo wav files sampled at 44.1 kHz: `drums.wav`, `bass.wav`, …" (plus `other` and
  `vocals`). `--two-stems=vocals|drums|bass` gives a 2-way split.
- CPU-viable: "If you do not have enough memory on your GPU, simply add `-d cpu`… With Demucs, processing
  time should be roughly equal to 1.5 times the duration of the track." macOS notes live in `docs/mac.md`.
- This is the only tool in the matrix that reliably turns a finished 2-track mix into named instrument
  stems under a permissive licence. It is a **4-stem** split (drums/bass/vocals/other) — it will not give
  you "pads vs textures vs hats" separately.

---

## User-reported quality

This column is weak and it is weak for a structural reason: Reddit — the only place with volume of
genre-specific AI-music criticism — refused every fetch path available here (403 on `search.json`, domain
blocked to WebSearch). Perplexity `sonar-pro` was run twice and explicitly declined to produce Reddit
quotes rather than fabricate them (`sonar-reddit-quality-quotes.json`: "if I tried to show you 'Reddit
quotes' with URLs, they would be invented (hallucinated) rather than real comments").

What *is* directly verifiable, from Hacker News comments harvested via the Algolia API
(`src-hackernews-user-comments.txt`). None of these are techno- or ambient-specific; they are the
best-available dated public user statements:

> "it can't remix. even comfyui can remix on my desktop. I've used udio, suno, comfyui with the music
> generation models, and one other site that i can't remember the name of… **They all kinda suck, you do
> have to run generation many times unless you're very lucky.**"
> — user `genewitch`, 2026-04-25, https://news.ycombinator.com/item?id=47897394

> "Hell, I've sent people songs made in Suno, and they were surprised to learn that those were AI
> generated. If you open suno and type in '90s jazz song' then yeah, you're likely going to get a bit of
> generic AI slop. If you get into specifics, voice style, instrument types, how they're played, which
> chords, etc. You can get [better results]"
> — user `giancarlostoro`, 2026-05-28, https://news.ycombinator.com/item?id=48302503

> "suno already matches 99% of music in quality and creativity."
> — user `jatora`, 2026-01-13, https://news.ycombinator.com/item?id=46606990

> "Udio has good models to generate audio, but awful UI and organization/management tools."
> — user `brulard`, 2025-04-28, https://news.ycombinator.com/item?id=43819852

> "Without the entire music catalog, they are just not going to be able get the diversity and quality of
> outputs they once had… Udio and Suno have demonstrated that okay-quality new music can be created by
> training on vast collections of pirated music, and, as expected, the music labels shut them down."
> — user `lexandstuff`, 2025-10-31, https://news.ycombinator.com/item?id=45769734

Second-hand, **not independently verified** (surfaced by Perplexity from an aggregator page that was not
itself fetched): a 2026-07-30 Mubert review summary reporting that "users find it useful for quickly
generating royalty-free music… but the main complaints are consistency and reliability. Some say genres
miss the brief. Others say tracks feel too similar or generic." Raw response in
`sonar-mubert-endel-quality.json`.

Perplexity's open-model pass (`sonar-quality-open-models.json`) returned mostly the vendors' own papers
and metrics rather than user reports, and its inferences are flagged as such inside that file.

**Nobody's dated, first-hand verdict on 10+ minute hypnotic minimal/dub techno was found for any tool in
this matrix.**

---

## Lawsuit status

Sourced to the **companies' own press releases**, because Reuters (401), BBC and AP (blocked) could not
be fetched from this environment.

**Warner Music Group ↔ Suno — settled, announced 2025-11-25.** PRNewswire, "WARNER MUSIC GROUP AND SUNO
FORGE GROUNDBREAKING PARTNERSHIP":

> "NEW YORK, Nov. 25, 2025 /PRNewswire/ — Warner Music Group (Nasdaq: WMG)… and Suno, the leader in AI
> music, today announced a first-of-its-kind partnership… **The deal also settles previous litigation
> between the companies.**"

> "In 2026, Suno will make several changes to the platform, including launching new, more advanced and
> licensed models. When the new models launch in 2026, the current models will be deprecated. Moving
> forward, downloading audio will require a paid account."

WMG CEO Robert Kyncl: "AI becomes pro-artist when it adheres to our principles: committing to licensed
models, reflecting the value of music on and off platform, and providing artists and songwriters with an
opt-in for the use of their name, image, likeness, voice and compositions in new AI songs."
(`src-pr-wmg-suno.txt`)

**Universal Music Group ↔ Udio — settled, announced 2025-10-29.** PRNewswire, "UNIVERSAL MUSIC GROUP AND
UDIO ANNOUNCE UDIO'S FIRST STRATEGIC AGREEMENTS FOR NEW LICENSED AI MUSIC CREATION PLATFORM":

> "SANTA MONICA, Calif., Oct. 29, 2025 /PRNewswire/ — Universal Music Group (UMG)… and Udio… today
> announced industry-first strategic agreements, **under which the companies settled copyright
> infringement litigation** and will collaborate on an innovative, new commercial music creation,
> consumption and streaming experience."

> "The new platform, which will be launched in 2026, will be powered by new cutting-edge generative AI
> technology that will be trained on authorized and licensed music."

> "**Udio's existing product will remain available to users during the transition period with creations
> controlled within a walled garden** and the service amended in multiple ways—including fingerprinting,
> filtering, and other measures—before the launch of the updated service."

(`src-pr-umg-udio.txt`) This press release is the direct explanation for the 2025-11-12 Udio ToS that
bans all downloads and all commercial use of Output.

**Sony Music — status NOT VERIFIED.** Search results (`WebSearch`, 2026-09-02) consistently indicate Sony
is the remaining major label still litigating against both Suno and Udio, with claims of a second SDNY
filing against Udio on 2026-07-20 covering ~30,117 additional recordings and a trial expected late 2026.
**Every one of those sources is a secondary blog or tracker site; none of it was confirmed against a
court docket, a Sony press release, or a wire service, because Reuters/BBC/AP are unreachable here.**
Do not rely on the Sony details without re-verification.

**What is safely inferable from the verified documents alone** (stated as document facts, not as legal
advice):

1. Udio outputs cannot lawfully be shipped in a product today — its own ToS forbids downloading them and
   forbids commercial exploitation, and assigns ownership to Udio.
2. Suno's paid-tier assignment of Output rights survives the WMG settlement, but Suno has publicly
   committed to deprecating its current models in 2026 and to adding per-account monthly download caps —
   a pipeline built on bulk Suno stem downloads has an announced expiry date.
3. Stability, Google (Magenta RT2 and Lyria) and ElevenLabs all publish affirmative statements about
   licensed or opt-out-honouring training data; MusicGen's weights are non-commercial by licence
   regardless of the litigation picture.

---

## What I could not verify

Each item below is a genuine gap, not an omission.

**Blocked by the fetching environment**
1. **Any Reddit thread.** `reddit.com` returns 403 to curl and is blocked to WebSearch. This is the
   single largest gap — it removes essentially all genre-specific user quality reporting.
2. **Reuters, BBC, AP.** Reuters returns 401; BBC and AP are blocked to the fetcher. The lawsuit section
   therefore rests on corporate press releases.
3. **Sony Music's current litigation posture** against Suno and Udio — secondary sources only, not
   confirmed against a docket or a first-party statement.

**Pricing / plan facts behind logins or broken pages**
4. **Suno plan prices**, including the Premier price needed for Studio (and therefore for stems). The ToS
   points to `https://app.suno.ai/account`, which requires sign-in.
5. **Udio plan prices** — behind a login wall.
6. **Mubert's actual licence text.** `mubert.com/license` 404s; `mubert.com/api/pricing` returns
   Cloudflare error 1101. All Mubert licence language quoted here is from the marketing page.
7. **Lyria RealTime pricing.** The string `lyria-realtime` does not appear on the Gemini API pricing page
   at all, and Vertex lists only Lyria 2 / Lyria 3 / Lyria 3 Pro.
8. **FMOD's price for a non-game iOS app.** Explicitly quote-only: "contact us for custom license models".
9. **Wwise's terms for a non-game app.** The pricing page fetched is titled "Wwise for Games"; the Indie
   tier's <$250K threshold is a *production budget* threshold for games.

**Product facts the vendor does not document**
10. **How many stems ElevenLabs' `stem-separation` returns, and what they are called.** The docs say only
    "ZIP archive containing separated audio stems".
11. **How many stems Suno Studio's Multitrack export produces**, and whether they include separate
    percussion/pad/texture layers rather than a coarse drums/bass/other split.
12. **Whether Mubert's API can actually return stems.** Marketing says yes; the v3 reference documents no
    such endpoint.
13. **Udio's feature set** — stems, lengths, audio input. The ToS is the only public document that
    rendered, and it describes none of them.
14. **Stability Platform's commercial-use clause for API outputs.** The Community License covers the
    *open weights*; the cloud API's output-rights clause did not render to this fetcher.
15. **Commercial-use terms for Lyria 3 / Lyria RealTime output.** Neither model page states one; only the
    SynthID watermarking commitment is documented.
16. **Magenta RealTime v1's specs** — the v1 code and model were moved to a `v1_legacy` branch and the v1
    model card was not re-read in detail; all Magenta numbers here are MRT2's.
17. **Whether Stable Audio Open runs under MLX on Apple Silicon.** No official or community MLX port was
    found; the Open Small card references Arm CPU optimisation only.
18. **Independent quality measurement of HeartMuLa.** "Comparable quality to Suno" and "Suno-Quality
    Output" are the repo's own claims.
19. **Elementary Audio's licence and iOS support**, and **RNBO's licence terms** — neither landing page
    states them.
20. **The ElevenLabs 5-minute vs 10-minute max-length contradiction** between the API schema
    (`music_length_ms` ≤ 600 000) and the documentation/pricing card ("5 minute duration limit").

---

## Index of saved sources

**Primary pages** (`src-*.txt`, each with its URL and fetch date at the top): 65 files covering
ElevenLabs (9), Suno (7), Udio (1), Stability (4), Google (6 + Vertex pricing), Magenta (5), MusicGen /
AudioCraft / MLX ports (7), Mubert (2), Demucs (2), the playback engines (8), Endel (3), the two
settlement press releases (2), and one Hacker News comment harvest.

**Raw Perplexity responses** (`sonar-*.json`): `sonar-quality-techno-ambient.json`,
`sonar-quality-open-models.json`, `sonar-reddit-quality-quotes.json`, `sonar-mubert-endel-quality.json`.
All four were used only to look for user quality reports, as scoped. Perplexity was reached via the
OpenRouter API (`perplexity/sonar-pro`); perplexity.ai was never opened in a browser.
