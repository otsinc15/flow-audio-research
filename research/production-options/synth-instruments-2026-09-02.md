# Code-driven synthesis for Plastikman-character focus music — cited options

**Compiled 2026-09-02.** Target sound: hypnotic minimal / dub techno in the character of Plastikman
"Deeper Focus" — 909-style drums, sub bass, filtered chord stabs, dub delay, ~115–120 BPM — produced by
**code driving real synth and drum-machine emulations**, not by prompting an AI music model.

Every claim traces to a file in this directory: `src-*.txt` (primary page, with URL + fetch date in the
header) or `sonar-*.json` (raw Perplexity response). Claims that could not be verified from a primary
source say **not found**. Nothing here is inferred.

Render box assumption: **Mac mini M4, Apple Silicon, no Homebrew, no sudo, pip/uv only.**

---

## 0. What was actually run, not just read

Seven claims in this document were verified by execution on Apple Silicon (macOS 26.6.2, arm64,
Python 3.12.13 in a `uv` venv, `~/.local/bin/uv`, **no Homebrew on the box, no sudo used**). Probe scripts
and their outputs are transcribed in `src-probe-pedalboard-surge-2026-09-02.txt`.

| Probe | Result |
|---|---|
| `uv pip install pedalboard` | ✅ `pedalboard==0.9.24` installed from a prebuilt `macosx_11_0_arm64` wheel. No compiler, no brew. |
| `uv pip install dawdreamer` | ✅ `dawdreamer==0.9.0`, arm64 wheel. Slow — **"Prepared 1 package in 3m 07s"**; a 2-minute command timeout killed a first attempt. |
| A clean box has **zero** instrument plugins | ✅ `AudioUnitPlugin.installed_plugins == []`, `VST3Plugin.installed_plugins == []`, `/Library/Audio/Plug-Ins/Components` empty, `/Library/Audio/Plug-Ins/VST3` does not exist. **pedalboard is a host with nothing to host until you supply a plugin.** |
| Surge XT VST3 loaded from an arbitrary path | ✅ `load_plugin("./surge/Surge XT.vst3")` → `VST3Plugin`, `is_instrument=True`, **599 addressable parameters**. The bundle was unzipped from the official `surge-xt-macos-1.3.4-pluginsonly.zip` into a scratch directory — **no installer, no `/Library` write, no sudo.** |
| Code plays notes offline | ✅ `p(midi_messages, duration=7.0, sample_rate=48000, num_channels=2)` returned `(2, 336000)` float32. **0.04 s wall for 7.0 s of audio = ~166× realtime.** Through DawDreamer the same plugin renders at **~142× realtime** and exposes **2,855** parameters. |
| Code changes a parameter and the audio changes | ✅ `p.global_volume = -12.0` → RMS 0.07840 → 0.01967. |
| **Drum synthesis with no plugin at all** | ✅ DawDreamer compiled a Faust string calling `sy.kick(55, 0.2, 0.01, 0.5, 6.0, gate)` from the Faust standard `synths.lib` (`compile() == True`) and rendered 4.0 s in **0.002 s = ~2,400× realtime**, peak 1.000 (drive 6 saturates into clipping — as intended for a techno kick). **This path needs no VST, no AU, no download beyond the pip wheel.** |

One gotcha found by running it: setting `a_filter_1_cutoff` changed the reported value but produced a
**byte-identical render**, because the default Surge patch has `a_filter_1_type == "Off"` — the parameter
is inert, not broken. Lesson: in a plugin host, always verify a parameter change by measuring the audio,
never by reading the parameter back.

Second gotcha: `surge-xt-macos-1.3.4-pluginsonly.zip` contains **0 `.fxp` factory patches and 0 `.wt`
wavetables** — those ship in the 417 MB `.dmg`, installed to `/Library/Application Support`. The plugin
still loads and renders on its init patch, and every voice can be built from code via the 599 parameters,
but "load a factory preset by name" is not available from the plugins-only zip.

Third finding, relevant to the whole dub-techno effects chain: the companion **Surge XT Effects** VST3
loads as an effect with `fx_type` selectable from
`['Delay', 'Reverb 1', 'Phaser', 'Rotary Speaker', 'Distortion', 'EQ', 'Frequency Shifter', 'Conditioner', 'Chorus', 'Vocoder', 'Reverb 2', 'Flanger', 'Ring Modulator', 'Airwindows', 'Neuron', 'Graphic EQ', 'Resonator', 'CHOW', 'Exciter', 'Ensemble', 'Combulator', 'Nimbus', 'Tape', 'Treemonster', 'Waveshaper', 'Mid-Side Tool', 'Spring Reverb', 'Bonsai', 'Audio Input']`
— i.e. dub delay, two reverbs, spring reverb, tape saturation and Airwindows are all one GPLv3 download.

---

## 1. The licence question that governs everything else

Almost every serious open-source synth is **GPLv3**. GPLv3 constrains distribution of *the software*, not
the *audio the software renders*. The FSF is explicit:

> "In general this is legally impossible; copyright law does not give you any say in the use of the
> output people make from their data using your program. If the user uses your program to enter or
> convert her own data, the copyright on the output belongs to her, not you."
> — GNU GPL FAQ, §"Is there some way that I can GPL the output people get from use of my program?"
> (`src-gpl-faq-output.txt`)

The practical consequence, and the single most important architectural fact in this document:

| Architecture | GPLv3 status |
|---|---|
| **Render offline on the mini**, ship only the resulting audio files in the app | ✅ Clean. The GPL software never leaves your machine; the audio is yours. |
| **Embed the synth in the shipped iOS/Android app** and synthesise at runtime | ❌ Blocked for GPLv3 components unless you GPL the whole app. Distributing the app distributes the GPL binary, which propagates the licence. (The further claim that GPLv3 conflicts specifically with Apple's App Store terms is widely repeated but **was not verified from a primary source here** — treat it as a reason to get counsel, not as a finding.) |

So the stack splits in two. Anything GPLv3 (Surge XT, pedalboard, DawDreamer, Dexed, Vital, Dragonfly,
Cardinal, SuperCollider — all confirmed `GPL-3.0` on the GitHub API, `src-github-repo-licences.txt`) is
fine for an **offline render farm** and unusable for **on-device runtime synthesis**. Only the permissive
components (Faust with its LGPL exception, Open303 MIT, Mutable Instruments STM32 MIT, Airwindows MIT,
Pure Data BSD) can cross into a shipped binary. Odin 2's licence is unresolved — see §3.3.

---

## 2. Headless, scriptable synth rendering on macOS / Apple Silicon

Legend: ✅ yes · ❌ no · ⚠️ conditional · **?** not found.

| | **Spotify pedalboard** | **DawDreamer** | **Surge XT `surgepy`** | **Csound** | **SuperCollider NRT** | **Faust** | **Pure Data / libpd** | **Vital / Vitalium** | **pyo** |
|---|---|---|---|---|---|---|---|---|---|
| **Can code play notes offline?** | ✅ verified by execution — `plugin(midi_messages, duration, sample_rate, num_channels)` renders MIDI → numpy audio (`src-probe-pedalboard-surge-2026-09-02.txt`) | ✅ **verified by execution** — `add_midi_note()` + `render()` on a plugin processor, and `make_faust_processor().set_dsp_string()` for plugin-free synthesis. Documented: "MIDI playback in absolute time and PPQN time", "Parameter automation at audio-rate and at pulses-per-quarter-note", "VST instruments and effects (with UI editing and state loading/saving)" (`src-dawdreamer-readme.txt`) | ✅ "Surge XT uses `pybind` to expose the innards of the synth to Python code for direct native access to all its features" (`src-surge-readme.txt`) | ✅ (score/API driven; offline `-o file` render is the classic Csound mode) — **`ctcsound` is bindings only, it needs a `libcsound` you must supply** | ✅ NRT ("non-realtime") mode is a documented scsynth mode; `supriya` is "A Python API for SuperCollider" (`src-pypi-supriya.txt`) | ✅ DSP is *written* in code and compiled; DawDreamer compiles Faust strings at runtime (`src-dawdreamer-readme.txt`) | ✅ Pd patches driven by messages via libpd | ⚠️ it is a plugin, so only through a host such as pedalboard/DawDreamer | ✅ "Python module to build digital signal processing program" (`src-pypi-pyo.txt`) |
| **Sets parameters from code?** | ✅ verified — 599 named params on Surge XT; `load_plugin(..., parameter_values={...})` and attribute assignment | ✅ documented parameter automation | ✅ full native access | ✅ | ✅ | ✅ | ✅ | via host | ✅ |
| **Apple Silicon** | ✅ verified running on arm64; PyPI ships `macosx_11_0_arm64` wheels cp310–cp314 (`src-pypi-pedalboard.txt`) | ✅ **verified running on arm64**; PyPI ships `macosx_11_0_arm64` wheels cp311–cp314 for 0.9.0 (2026-08-12) (`src-pypi-dawdreamer.txt`); README: "Apple Silicon (arm64) or Intel (x86_64), macOS 11.0 or higher" | ✅ (Surge XT itself is universal) | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ last release 1.0.5 (2023-03-26) ships `macosx_13_0_arm64` wheels only for cp310/cp311 — **no cp312+ arm64 wheel** (`src-pypi-pyo.txt`) |
| **Licence** | **GPLv3** — `LICENSE` is the GPLv3 text; PyPI classifier `License :: OSI Approved :: GNU General Public License v3 (GPLv3)`; GitHub API `spdx_id: GPL-3.0` (`src-pedalboard-license.txt`, `src-pypi-pedalboard.txt`) | **GPLv3** (`src-dawdreamer-license.txt`, GitHub `GPL-3.0`) | **GPLv3** (`src-surge-license.txt`) | **LGPL-2.1** — `COPYING` is "GNU LESSER GENERAL PUBLIC LICENSE Version 2.1" (`src-csound-license.txt`) | **GPLv3** (`src-supercollider-license.txt`); `supriya` itself is **MIT** per GitHub API | **Compiler LGPL-2.1**; the *libraries* carry an explicit exception — see §2.1 | **BSD-3-ish** — Pd's `LICENSE.txt` is the "Standard Improved BSD License" (`src-puredata-license.txt`); libpd repo licence is `NOASSERTION` on the GitHub API | **GPLv3** (`src-vital-license.txt`) | **LGPLv3+** (`src-pypi-pyo.txt`) |
| **Install without brew/sudo (pip/uv only)** | ✅ **verified** — `uv pip install pedalboard`, prebuilt wheel, nothing else | ✅ **verified** — `uv pip install dawdreamer`, wheel-only, but slow ("Prepared 1 package in 3m 07s") (`src-dawdreamer-readme.txt`, `src-probe-pedalboard-surge-2026-09-02.txt`) | ❌ **No.** Not on PyPI (pypi.org/pypi/surgepy/json → HTTP 404, `src-pypi-surgepy.txt`). Requires `cmake -Bignore/bpy -DSURGE_BUILD_PYTHON_BINDINGS=ON` then `cmake --build ... --target surgepy` (`src-surge-readme.txt`) — a C++ toolchain build |
| | | | | ❌ `ctcsound` PyPI has **sdist only, no macOS wheels, last upload 2022-02-25**, and is only "Python bindings to the Csound API using ctypes" — libcsound must exist on the box (`src-pypi-ctcsound.txt`) | ❌ `supriya` PyPI has **sdist only, no wheels** and is an API to `scsynth`, which is a separate binary you must obtain (`src-pypi-supriya.txt`) | ✅ **verified, via DawDreamer** — DawDreamer's wheel embeds the Faust compiler (`make_faust_processor()`, `set_dsp_string()`, `compile() == True` on this box) so no C++ toolchain is needed. Installing standalone `faust` *would* be a compiler install. | ❌ no `libpd` on PyPI (HTTP 404, `src-pypi-libpd.txt`) | ⚠️ plugin binary, not pip — but the Vital binary is a plain `.vst3`/`.component` that can be dropped anywhere and loaded by path | ⚠️ wheel exists but not for cp312+ arm64 |

### 2.1 Faust's licence exception is the one that matters

The Faust standard libraries carry an explicit carve-out that most open-source audio code does not:

> "EXCEPTION TO THE LGPL LICENSE : As a special exception, you may create a larger FAUST program which
> directly or indirectly imports this library file and still distribute the compiled code generated by
> the FAUST compiler, or a modified version of this compiled code, **under your own copyright and
> license**. This EXCEPTION TO THE LGPL LICENSE explicitly grants you the right to freely choose the
> license for the resulting compiled code. In particular the resulting compiled code has no obligation
> to be LGPL or GPL. For example you are free to choose a commercial or closed source license or any
> other license if you decide so."
> — header of `synths.lib`, Faust standard libraries (`src-faust-synths-lib.txt`)

The Faust compiler itself is LGPL-2.1 ("FAUST compiler, Version 2.83.1 … GNU Lesser General Public
License … version 2.1", `src-faust-license.txt`).

This is the **only route in this document that is clean for on-device runtime synthesis in a closed-source
commercial app.**

---

## 3. Emulations of the Plastikman-era instruments

### 3.1 Drum machines (TR-909 / TR-808)

| Source | Licence | Verified quote / evidence | Fit |
|---|---|---|---|
| **Faust `synths.lib` drum functions** — `sy.kick(pitch, click, attack, decay, drive, gate)`, `sy.clap(tone, attack, decay, gate)`, `sy.hat(...)` | **LGPL-2.1 + the output exception above** | `synths.lib` header: "This library provides synthesizer and drum building blocks"; `sy.kick` docs: "Kick drum synthesis via a pitched sine sweep", parameters include **`drive`: a gain multiplier going into the saturator. Tuned for [1, 10]**; `sy.clap`: "Clap synthesis via filtered white noise". Reference given: `github.com/nick-thompson/drumsynth` (`src-faust-synths-lib.txt`) | **Best licence fit, and verified running.** `sy.kick(55, 0.2, 0.01, 0.5, 6.0, gate)` compiled and rendered on this box through DawDreamer at ~2,400× realtime with no plugin installed at all (`src-probe-pedalboard-surge-2026-09-02.txt`). Analytic 909/808-style voices, not samples, driven entirely by numbers from code. `drive` is exactly the saturation stage §5 says the sound needs. Upstream `nick-thompson/drumsynth` is "A small drum synthesis library for Elementary Audio" — its own `LICENSE` file 404s, so **its licence is not found**; only the Faust reimplementation's licence is verified. |
| **Mutable Instruments (Émilie Gillet) — Plaits, Peaks, Rings, Elements, Marbles, Tides, Stages, Clouds** | **MIT for the STM32F projects**, GPL3 for the AVR ones, cc-by-sa-3.0 hardware | Repo README: "Code (AVR projects): GPL3.0. / Code (STM32F projects): MIT license. / Hardware: cc-by-sa-3.0" (`src-mutable-eurorack-readme.txt`). Repo has directories for `plaits`, `peaks`, `braids`, `rings`, `elements`, `marbles`, `stages`, `tides2` etc. (`src-mutable-tree.txt`) | Plaits and Peaks contain 808/909-flavoured analogue bass-drum, snare and hi-hat models in **MIT C++** — portable into a closed app. Note the trademark condition: "The name 'Mutable Instruments' should not be used on any of the derivative works you create from these files." |
| **Surge XT** (as a hosted VST3) | GPLv3 | verified loading and rendering, §0 | Offline render only. |
| **Cardinal** (DISTRHO — VCV Rack modules as a plugin) | **GPL-3.0** (GitHub API, `src-cardinal-license-note.txt`) | Latest release 26.02 (2026-02-28) ships **only** `Cardinal-macOS-universal-26.02.pkg`, 974 MB (`src-cardinal-releases.txt`) | Offline only, and a `.pkg` rather than a drop-in bundle — heavier install path than Surge's zip. |
| **Bespoke Synth** | **?** licence not fetched | `src-bespoke-readme.txt` fetched but licence line not verified | **not found** |
| **Roland Cloud TR-909/TR-808 (official)** | **not found** | Every attempt to retrieve Roland's EULA / Roland Cloud terms failed: `roland.com/global/support/by_support/eula/` → 404, `roland.com/us/legal/terms/` → 404, `roland.com/global/legal/terms/` → 404, `rolandcloud.com/legal` and `/legal/eula` → the site returns its own "Not Found - 404" page (`src-roland-cloud-eula.txt`, `src-roland-cloud-terms.txt`, `src-roland-cloud-terms-of-use.txt`, `src-rolandcloud-legal.txt`, `src-rolandcloud-eula2.txt`) | **Do not assume anything about Roland Cloud output rights.** Unverified. |

### 3.2 TB-303 / SH-101 style monosynths

| Source | Licence | Verified quote | Fit |
|---|---|---|---|
| **Open303** (Robin Schmidt) | **MIT** | "The Open303 source code is released under the terms of the MIT license: … Copyright (c) 2009 Robin Schmidt (www.rs-met.com) … without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies" (`src-open303-license.txt`). GitHub API reports `spdx_id: NOASSERTION` (no `LICENSE` at the path GitHub scans) — the real grant is in `License.txt`; 88 stars, last push 2024-03-29 (`src-open303-repo.txt`, `src-open303-files.txt`) | **MIT, so shippable on-device.** C++ source, no prebuilt Python binding — you would compile it into your own engine. |
| **Faust `sy.dubDub`** | LGPL-2.1 + output exception | "A simple synth based on a sawtooth wave filtered by a resonant lowpass" (`src-faust-synths-lib.txt`) | Exactly the SH-101 / 303 topology: saw → resonant LP. Available from code with no plugin at all. |
| **Surge XT** | GPLv3 | verified — 599 params incl. `a_filter_1_cutoff`, `a_osc_1_pitch` (`src-probe-pedalboard-surge-2026-09-02.txt`) | Offline only. |
| **TAL-BassLine-101 / TAL-Bassline / TAL-NoiseMaker** | **not found** | `tal-software.com`, `tal-software.com/products`, `www.tal-software.com/products`, `tal-software.com/products/tal-bassline-101` and `/tal-noisemaker` all returned **HTTP 404 to this fetcher** (`src-tal-products.txt`, `src-tal-bassline101.txt`, `src-tal-www.txt`, `src-talsoftware-root.txt`, `src-tal-plugins.txt`) — the site appears to refuse this client, not to be missing. **TAL terms are unverified.** |

### 3.3 Poly / chord stabs

| Source | Licence | Evidence |
|---|---|---|
| **Surge XT** | GPLv3 (`src-surge-license.txt`); GitHub `GPL-3.0`, 3,989 stars, last push 2026-08-31 (`src-surge-repo-api.txt`) | Verified rendering, §0. |
| **Dexed** (DX7 emulation) | **GPLv3**, with a caveat: "Dexed is licensed on the GPL v3. The msfa component (acronym for music synthesizer for android, see msfa in the source folder) stays on the Apache 2.0 license" (`src-dexed-readme.txt`); GitHub `GPL-3.0`, 3,484 stars | FM, not the analogue-stab character, but licence-documented. |
| **Odin 2** | GitHub API `NOASSERTION` — SPDX **not resolved**; 808 stars, last push 2025-09-07 (`src-github-repo-licences.txt`) | Licence text not verified: **not found**. Do not count Odin 2 as GPLv3 without reading its licence file. |
| **Vital** | **GPLv3** (`src-vital-license.txt`); GitHub `GPL-3.0`, last push **2023-05-25** — the open-source repo has been dormant for over three years | vital.audio sells "Basic — Free … Vital: The full synth with all features" plus paid preset tiers (`src-vital-site.txt`, `src-vital-faq.txt`). **Vitalium** (the DISTRHO GPL build) was not independently fetched: **not found**. |

### 3.4 Dub delay, tape delay, reverb, saturation

| Source | Licence | Evidence |
|---|---|---|
| **Surge XT Effects** (Delay, Reverb 1, Reverb 2, Spring Reverb, Tape, Bonsai, Distortion, Waveshaper, Airwindows, Nimbus, Combulator, Ensemble, Frequency Shifter…) | GPLv3 | **Verified by execution** — the fx type list is quoted in §0 from the loaded plugin, not from a web page. |
| **Airwindows** (Chris Johnson) | **MIT** — "MIT License / Copyright (c) 2018 Chris Johnson … including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies" (`src-airwindows-license.txt`); GitHub `MIT`, 1,215 stars, last push 2026-08-29 | **The permissive saturation/console/tape option.** MIT means it can also ship inside a closed app. Surge XT exposes an "Airwindows" fx type, so the same DSP is reachable both ways. |
| **LSP Plugins** | **LGPL-3.0** — "Licensed under the terms of GNU Lesser Public License v3 (LGPLv3)" (`src-lsp-readme.txt`); GitHub `LGPL-3.0`, last push 2026-09-01 | LGPL: dynamic linking is permissible; still awkward for a static iOS binary. |
| **Dragonfly Reverb** | **GPL-3.0** (GitHub API; 1,143 stars, last push 2026-05-21) | Offline only. |

**Restriction on output: none of the above imposes one.** No licence in §3 places any condition on the
audio rendered — per the FSF quote in §1, and confirmed by reading each licence text. The only
output-side restrictions found in this whole study are in the *sample* licences (§4).

---

## 4. Sample-based route — and why it is the *worse* licence story, not the better one

This is the counter-intuitive result. Sample-pack licences restrict the **output** in ways that synth
licences do not, and the specific thing they restrict is *exactly* what a generative app does.

| Source | Quoted licence | Verdict for a generative app |
|---|---|---|
| **Goldbaby** | "Yes, Goldbaby sounds are 100% royalty-free… you can use our sounds in commercially released compositions without paying any additional royalties or fees." **But:** "You may not re-distribute these sounds, either in native format **or reformatted for use as samples, multi-samples, programs, or patches in a sampler, sample playback unit, website, or computer.**" (`src-goldbaby-faq.txt`) | ✅ for **pre-rendered tracks** shipped as finished audio. ❌ for **shipping the samples inside an app that triggers them at runtime** — that is a "sample playback unit… in a computer" in the licence's own words. |
| **Samples From Mars** | "The Audio Products are licensed, not sold, to you to be used for and reproduced **within your new musical compositions and productions only**. All copying, lending, duplicating, re-selling or trading of any Audio Product … is strictly prohibited, save as used for or incorporated into your original created works… This license is granted for a **single user only**… any use by you that frustrates the purpose of this Agreement or circumvents the revenue model of the Company (including without limitation selling, renting, or otherwise using or **distributing un-integrated Content**) would likely cause irreparable loss" (`src-samplesfrommars-terms.txt`) | ✅ for pre-rendered tracks. ⚠️/❌ for runtime triggering — a shipped one-shot in an app bundle is arguably "un-integrated Content". |
| **Freesound CC0** | Freesound's own FAQ: "freesound lets the user select one of three licenses… zero (cc0) … attribution (by) … attribution noncommercial (by-nc)… for the 'zero' license you can do pretty much what you want with the sound. **You could even sell the sound**, ... but you can't claim you are the author!" (`src-freesound-license-page.txt`). A CC0-filtered search for `TR-909` returns **712 sounds** (`src-freesound-909-cc0.txt`) | ✅ **The only sample source verified clean for both pre-rendered *and* runtime use.** Caveats: per-sound licence must be checked individually (by-nc is a trap — "you can't earn any money with the piece of work you create"), provenance and quality are user-uploaded and uneven, and the retired "Sampling+" licence still exists on old files. |
| **Roland Cloud sample terms** | **not found** — see §3.1; every Roland legal URL 404'd. | Unverified. Do not use on assumption. |
| **MusicRadar SampleRadar 909 packs** | **not found** — `musicradar.com/news/drums/sampleradar-1000-free-drum-machine-samples-61838` returned **HTTP 404** (`src-musicradar-909.txt`). | Unverified. |

**Nothing here is "for personal use only" outright**, but Goldbaby and Samples From Mars both restrict
redistribution in a form the app could replay, and Samples From Mars restricts to a single user.

---

## 5. What producers say makes 909/808 sound "fat, thick, warm" — and how to do it in code

Sources: Sound On Sound (Hugh Robjohns, *Analogue Warmth*, **published February 2010**,
`src-sos-analogue-warmth.txt`), Attack Magazine *Thumping Techno* beat-dissected
(`src-attack-thumping-techno.txt`), a KVR Audio forum thread on mid-90s kick design
(`src-kvr-mid90s-kick.txt`), Hacker News comments harvested via the Algolia API
(`src-hn-synth-comments.txt`), and one Perplexity `sonar-pro` pass (`sonar-fat-909-techno.json`).

**Note on the Perplexity pass:** 4 of its 15 citations were Reddit URLs, which are unreachable from this
environment and therefore unverified; the quotes reproduced below are only the ones I re-fetched from the
primary page myself.

### 5.1 Saturation and drive — the largest single factor

Attack Magazine, on building a techno beat, describes the chain in one sentence:

> "we're mainly going to use analogue drum samples as our sound sources, **processing them with filters
> and saturation** to create a distinctive in-­your­-face techno sound… we've run it through **heavy
> compression and analogue overdrive to add character and harmonics**. Finally, we've boosted the low end
> and removed made a small cut around **250 Hz**."
> — Attack Magazine, *Beat Dissected: Thumping Techno* (audio assets dated 2015-07)

And on the tuned percussion: *"we've added heavy overdrive then filtered with a 24dB/octave high-pass
filter."* And on the drum bus: *"saturation… can be added to achieve a more aggressive character."*

A KVR poster reverse-engineering a mid-90s hardcore kick describes the extreme version, and — importantly
for this project — says the plugins don't get there:

> "kick+clap on a mixer track or buss, lowshelf filter with high Q and or peak/bell filter round about the
> stopband of the lowshelf (before the clipping), murder through **transistor based clipping (hard
> clipping essentially)**, eq again … with some **dip around 180-200hz and 800-2000hz** … perhaps record
> it, rinse it through the same chain, repeat till happy."
> "**I've not found many (read none) distortion plugins that go to these lengths of clipping though and
> not sound just plain horrible, plastic, thin** etc etc, so good luck with that part"
> — KVR Audio forum thread 494912

Sound On Sound explains *why* saturation reads as warmth, and names the mechanism you have to implement:

> "some aspects of analogue technology introduce artifacts and distortions that are perceived as pleasant,
> and are often musically enhancing — and this is something that lies at the heart of the idea of
> 'analogue warmth'." … "often **significant third-harmonic distortion on loud low-frequency components**
> of the recorded sound." … "Harmonic distortion in transformers is caused by two effects: **hysteresis
> for low-level signals and saturation for high-level signals**. The effect is **always greatest for low
> frequencies**, and results mainly in third-harmonic distortion."
> — Hugh Robjohns, *Analogue Warmth*, Sound On Sound, February 2010

Robjohns also warns against the shortcut this project would be tempted by:

> "Although frequency response is an important element of the impression of warmth… **the overall tonality
> is not, in itself, enough to introduce warmth.** If it were, all we'd have to do is modify the frequency
> response of our digital systems appropriately… While frequency response clearly plays a role, the effect
> that analogue recording has on **signal transients** is — in my view — far more important."

**Implementation:** an EQ curve will not buy warmth. You need a real non-linearity that produces
odd-harmonic content concentrated at low frequencies, and transient softening. In the stack above that is
`sy.kick`'s own `drive` parameter (into its saturator), Surge XT Effects' `Tape` / `Bonsai` / `Distortion`
/ `Waveshaper`, or an Airwindows MIT saturator.

### 5.2 Analogue drift and per-hit variation

The strongest primary evidence is a Hacker News commenter who has owned three 808s:

> "I've owned 3 tr-808s in my life. I currently own one. **I can confirm that each one sounds different.**
> I've samples from each one… There are 2 distinct revisions of tr-808s. The early models had a shorter
> higher pitched snare sound and later models were a lower pitch deeper snare. My current 808 has the
> weakest clap of the three I've owned."
> — HN user S_A_P, 2018-07-29 (`news.ycombinator.com/item?id=17636066`)

and, directly on the Plastikman lineage:

> "Little did Roland realize that to residents of South Florida there is no such thing as too much bass.
> When producers wanted more out of the machine, they took to opening it up and fiddling around with the
> factory default settings (**Richie Hawtin did this once and the result was Spastik**). Those who were
> more electronically inclined took a soldering gun to the circuit board to tune the kick circuit and
> increase the decay time to the point of **self-oscillation**."
> — HN user adam_ellsworth quoting Ishkur's Guide, 2022-05-18 (`item?id=31428027`)

Attack Magazine gives the software equivalent for humanising a pattern: *"Velocity play a fundamental role
here, making the pattern feel more humanised and adding a subtle groove."*

**Implementation:** this is the argument *for* the synthesis route and *against* the sample route. A single
909 sample is one fixed unit on one fixed day; a `sy.kick(pitch, click, attack, decay, drive, gate)` call
lets you jitter pitch, click and decay per hit. Sampled kits need round-robin layers to fake what
parameterised synthesis gets for free.

### 5.3 Layering, sidechain, and the 150–500 Hz band

Attack's beat is built from layered elements with deliberately different roles: two closed hi-hats, one
*"treated with some saturation and subtle plate reverb"* and one *"without the use of saturation and
reverb… layered with some white noise to create a subtle crispy decay tail"* and *"high-pass filtered…
to make it thinner"*; two copies of a tuned TR-909 rimshot, *"one tuned low and one high"*; and a 909
ride *"that plays the same pattern as the kick drum, to make the groove more incisive… processed with a
small amount of plate reverb and a high-pass filter to ensure it sits in the top of the mix **without
taking up too much mid-range space**."*

On the 150–500 Hz band specifically, two independent primary sources converge on **cutting**, not
boosting: Attack cuts *"around 250 Hz"* on the kick after overdrive; the KVR poster dips *"around
180-200hz"* after clipping. The Perplexity pass reports further figures (a 240–350 Hz cut, saturating
100–300 Hz at 40–50% drive while keeping sub below 80 Hz clean) attributed to third-party tutorial blogs —
those are recorded in `sonar-fat-909-techno.json` but were **not re-verified from the primary page** and
should be treated as unconfirmed.

Sidechain compression figures (4:1, 1–3 ms attack, 80–150 ms release, 6–10 dB gain reduction) appear only
in the Perplexity pass, sourced partly to Reddit: **not verified.**

**Note on the earlier ear-test finding.** This repo's own `research/ear-test` work already recorded a
measured **150–500 Hz body deficit** against the reference tracks (commit `e24ec4d`, "log 'fat/thick'
feedback vs measured body deficit"). The primary sources above say that band is filled by *saturation
harmonics and layered mid-range elements*, and is then **selectively carved** at 180–350 Hz — not by an
EQ boost. That is a testable prediction for the next render.

---

## 6. Precedent: apps that generate electronic music at runtime by rules + synthesis

Verified from primary sources:

| Product | What it is | Runtime synthesis? | Commercial? | Source |
|---|---|---|---|---|
| **Intermorphic Wotja** (lineage: SSEYO Koan → Noatikl → Mixtikl → Wotja) | Self-described "Live Generative Music & MIDI", explicitly **"'AI-free', on-device"**; the company describes "a 35+ year passion for developing powerful & 'AI-free' generative music apps" | On-device, per its own page title | ✅ shipping commercial product across iOS/macOS/Windows/Android | `src-wotja-ai-free.txt`, `src-intermorphic-wotja.txt` |
| **Sonic Pi** | "The Live Coding Music Synth for Everyone"; "Sonic Pi is your free code-based music creation and performance tool"; "Powerful for professional musicians and DJs"; genres listed include "Hip hop & EDM" | ✅ real-time software synthesis (it is a SuperCollider front end) | Free/open, not a consumer product | `src-sonicpi-about.txt` |
| **Bitwig The Grid** | Modular sound-design environment inside a commercial DAW | ✅ | ✅ | `src-bitwig-grid.txt` |
| **Amper Music** | Reported by a friend of the builder on HN: "They use a lot of custom acoustic instrument samples and **some sound synthesis driven by Haskell and SuperCollider. No neural nets or machine learning involved** … it's mostly rules based, with a large and byzantine rule set" | Server-side rules + synthesis, not neural | ✅ was a commercial product | HN user Somniloquist, 2019-07-25, `item?id=20525330` (`src-hn-synth-comments.txt`) — **second-hand, not a company statement** |
| **Spore / Maxis procedural music (Brian Eno + Kent Jolly + Aaron McLeran)** | HN: Aaron McLeran "collaborated with Brian Eno on the procedural music in Will Wright's 'Spore' … using Pure Data (PD)" and had written "computer music in CSound" | ✅ procedural, in-game | ✅ shipped game | HN user DonHopkins, 2020-04-06, `item?id=22790854` (`src-hn-synth-comments.txt`) — second-hand |
| **Bronze** | Site fetched, 36 KB | **?** the Perplexity pass reports a TechCrunch piece saying Bronze packages music as a "generative, interactive, or personalized experience", tested with Arca and Jai Paul, but **whether Bronze synthesises or assembles pre-rendered assets is not documented in any source retrieved** | apparently commercial | `src-bronze-site.txt`, `sonar-generative-synth-precedent.json` |
| **Eno & Chilvers — Bloom, Trope, Scape, Reflection** | Generative music apps; the Perplexity pass quotes Peter Chilvers' site and the App Store listing | **?** neither source describes a synthesis engine | ✅ commercial App Store products | `sonar-generative-synth-precedent.json` — **primary pages not fetched directly: unverified** |
| **Endel** | endel.io/technology fetched (256 KB) | **?** | ✅ | `src-endel-tech.txt`. Also relevant: this repo's own 2026-09-02 correction that **Endel is stem assembly, not generative synthesis**. |
| **No Man's Sky / Paul Weir** | | **?** — `gamesindustry.biz` article 404'd (`src-paulweir-nms.txt`) | | **not found** |
| **Nodal** | | **?** | | **not found** — no primary source retrieved |

**The honest summary of Q5:** there is a real, long-running commercial precedent for **rule-driven,
on-device, non-AI generative music** (Wotja, 35+ years of lineage, explicitly "AI-free"), and a real
precedent for **rules + synthesis at commercial scale** (Amper, second-hand). There is **no verified
precedent found for an app that generates *techno specifically* from drum-machine emulations by rules at
runtime.** That is a gap in the evidence, not proof it doesn't exist — Reddit, where such apps would be
discussed, is unreachable from here.

One HN comment is worth carrying into the design, from a working generative-music practitioner:

> "**Embrace determinism, especially at first.** It can be tempting to lean-in to the essence of
> generative music and have randomness reign supreme ('it goes on forever and never repeats, different
> every time'), but that makes it very difficult to track the consequences of your decisions as you're
> composing the system… **Pick a genre, reverse-engineer it, write down its rules**"
> — HN user spiralganglion, 2019-03-17 (`item?id=19412606`)

and one that captures why techno is the right genre to attempt this in:

> "Making interesting music of other genres is a lot more difficult to do algorithmically. One of the big
> perks of **acid techno** (a pair of TB-303s and a TR-808 or TR-909 drum machine, and some simple effects
> processors) is **how easy it is to get really interesting sounding stuff out of random patterns and
> simple filter sweeps.**"
> — HN user sneak, 2021-04-20 (`item?id=26871049`)

---

## 7. Ranking: the most practical licence-clean stack for the synthesis arm

The ranking depends entirely on one question the product has not yet answered: **does the app ship
pre-rendered audio, or synthesise on the device?** They have different winners.

### Track A — offline render on the mini, ship audio files (what the app does today)

**1. `pedalboard` (pip) + Surge XT VST3 (unzipped, no installer) + Surge XT Effects.** ★ recommended

- **Verified working end-to-end on Apple Silicon with no brew and no sudo, at ~166× realtime.**
- One `uv pip install`, one 187 MB zip. Nothing touches `/Library`. 599 parameters, all addressable.
- Delay, two reverbs, spring reverb, tape, Bonsai and Airwindows saturation in the same package —
  the entire dub-techno effects chain, GPLv3, from one download.
- GPLv3 is a non-issue because only rendered audio ships (§1, FSF quote).
- **Trade-offs:** the plugins-only zip has no factory patches — every voice must be built from parameters
  in code (arguably an advantage for reproducibility, definitely more up-front work). Parameters that
  belong to a disabled module read back as "set" while doing nothing, so every patch needs an audio-level
  assertion. `pedalboard` has no transport/PPQN concept — you hand it a flat list of MIDI messages and a
  duration, so tempo, swing and automation curves are your code's problem.

**2. DawDreamer (pip) — the same thing plus a mixing graph, PPQN MIDI, and built-in Faust.** ★ also verified

- `uv pip install dawdreamer`, arm64 wheel for cp311–cp314, released 2026-08-12 (`src-pypi-dawdreamer.txt`).
  **Verified on this box:** loaded the same Surge XT VST3 (2,855 parameters, ~142× realtime) *and*
  compiled a Faust `sy.kick` with no plugin at all (~2,400× realtime).
- Adds what pedalboard lacks: "Composing graphs of multi-channel audio processors", "Parameter automation
  at audio-rate and at pulses-per-quarter-note", "Rendering and saving multiple processors simultaneously"
  (i.e. stems in one pass), and a Faust processor that compiles DSP from a string.
- **Trade-offs:** much bigger install than pedalboard — "Prepared 1 package in 3m 07s", and a 2-minute
  command timeout killed the first attempt, so budget for it in any CI/provisioning script. Newer, smaller
  user base; requires Python ≥3.11. Also GPLv3 — same offline-only rule.

**3. Csound / SuperCollider NRT — rejected for this box.** Both are excellent renderers, but neither is
pip-installable without a system binary: `ctcsound` is sdist-only ctypes bindings last uploaded
**2022-02-25** and needs a `libcsound` you cannot brew-install; `supriya` is sdist-only and needs
`scsynth`. On a no-brew mini these are a source build, not a `pip install`.

**4. pyo — rejected.** Last release 1.0.5 (2023-03-26); arm64 wheels only for cp310/cp311.

### Track B — synthesis inside the shipped app, at runtime on the user's device

**1. Faust, compiled to C++/Wasm, using `sy.kick` / `sy.clap` / `sy.hat` / `sy.dubDub`.** ★ the only clean answer

- The **only** option in this study with an explicit, written grant to ship the compiled result under a
  commercial closed licence (§2.1).
- Ships the exact 909/808/303 topologies you need as parameterised functions, with a `drive` saturator
  already in the kick.
- You can prototype it today **inside DawDreamer** on the mini (same Faust source, offline — already
  proven working, §0), then compile the identical DSP for the device. That is a real de-risking path: the
  render farm and the app run the same code.
- **Trade-offs:** you are writing DSP, not loading a finished synth. Nothing sounds like Surge XT on day
  one. Faust is a real language to learn.

**2. Open303 (MIT) + Mutable Instruments STM32 sources (MIT) + Airwindows (MIT)**, compiled into your own
engine. Permissive, battle-tested, but three separate C++ codebases with no shared host, and Mutable's
trademark condition forbids using the "Mutable Instruments" name on derivatives.

**3. CC0 Freesound 909 samples as a fallback layer** — the only sample source verified safe to embed in a
shipped app (§4). Requires per-sound licence checking and quality triage.

**4. Everything GPLv3 — Surge XT, Vital, Dexed, Cardinal, Dragonfly, pedalboard, DawDreamer — is
disqualified for Track B.** So are Goldbaby and Samples From Mars sample packs, by their own explicit
"sample playback unit" / "un-integrated Content" clauses.

### The one-line recommendation

**Build Track A now on `pedalboard` + Surge XT (proven working, fastest to a first listenable render), and
write every drum voice in Faust from the start so the same DSP can move to Track B later without a
rewrite.** Adopt DawDreamer when you need per-stem rendering or audio-rate automation.

---

## 8. Everything marked "not found"

| Item | Why |
|---|---|
| Roland Cloud EULA / output rights for TR-909, TR-808, SH-101, and Roland Cloud sample terms | 5 distinct Roland/Roland Cloud legal URLs all returned 404 |
| TAL-BassLine-101, TAL-Bassline, TAL-NoiseMaker licence terms | `tal-software.com` returned HTTP 404 to this fetcher on 5 different paths — the site refuses this client |
| Odin 2 licence | GitHub API reports `NOASSERTION`; licence file not fetched |
| Bespoke Synth licence | README fetched, licence line not verified |
| Vitalium (DISTRHO build of Vital) | not fetched independently |
| `nick-thompson/drumsynth` licence (upstream of the Faust drum functions) | repo `LICENSE` returns 404 |
| MusicRadar SampleRadar free 909 packs | article URL 404 |
| No Man's Sky / Paul Weir procedural audio architecture | article URL 404 |
| Nodal | no primary source retrieved |
| Eno/Chilvers Bloom / Scape / Reflection engine architecture | only reachable second-hand via Perplexity |
| Bronze — synthesis vs pre-rendered assembly | not documented in any retrievable source |
| Endel's own synthesis architecture | page fetched but no engine description verified |
| Sidechain compression settings for techno (ratio/attack/release/GR) | only in the Perplexity pass, partly Reddit-sourced |
| Reddit corroboration of any producer claim | Reddit is unreachable from this environment |

---

## 9. Fetch limitations

- **Reddit, Reuters and BBC are unreachable from this environment** (per the standing constraint) and were
  not attempted. Where Perplexity returned Reddit citations they are flagged as unverified above.
- `tal-software.com`, `roland.com`/`rolandcloud.com` legal paths, `musicradar.com` and `gamesindustry.biz`
  all returned 404 to this fetcher.
- `soundonsound.com/reviews/roland-tr-909` returned **HTTP 410 Gone**; the *Analogue Warmth* article
  fetched cleanly and is the SOS source used.
- GitHub's code-search API requires authentication and was not used; repository metadata came from the
  unauthenticated `/repos/{owner}/{repo}` endpoint.
- The Perplexity call is recorded raw in `sonar-fat-909-techno.json` and
  `sonar-generative-synth-precedent.json`, including all citation URLs, so its unverified claims can be
  audited separately.

---

## 10. Additional sources fetched but not quoted above

Kept for audit; each carries its own URL + fetch-date header. Nothing in this document rests on them.

`src-attack-rumbling-bass.txt` (Attack Magazine, rumbling techno bass in Operator) ·
`src-cardinal-readme.txt` · `src-cc0-legalcode.txt` (CC0 1.0 deed) · `src-csound-readme.txt` ·
`src-distrho-ports-readme.txt` · `src-dragonfly-readme.txt` ·
`src-drumsynth-readme.txt` and `src-drumsynth-license.txt` (HTTP 404 — the evidence that the upstream
drum-synth licence is unavailable) · `src-faust-demos-lib.txt` · `src-faust-readme.txt` ·
`src-freesound-licenses.txt` · `src-goldbaby-terms.txt` · `src-libpd-readme.txt` ·
`src-odin2-readme.txt` · `src-pedalboard-readme.txt` · `src-roland-eula.txt` (HTTP 404) ·
`src-sos-909.txt` (soundonsound.com TR-909 review, **HTTP 410 Gone**) · `src-vcvrack-license.txt` ·
`src-vital-readme.txt` · `src-wotja-about.txt`.

---

## Decision (2026-09-02, Fable orchestrator)

**Track A.** The product plan since the moat pass is Endel-style stem assembly inside our own playback engine, i.e. audio rendered offline on the mini and shipped as files. That makes GPLv3 tooling a non-issue and picks stack #1 (`pedalboard` + Surge XT + Surge XT Effects) for the coded arm's real-synth rebuild, with drum voices written in Faust per the recommendation so an on-device move later needs no rewrite. Track B is not being pursued. Sample packs with "no sampler / no un-integrated content" clauses are out; CC0 Freesound hits remain allowed.
