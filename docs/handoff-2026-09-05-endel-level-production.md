# Handoff — reaching Endel-level hypnotic minimal techno in Ableton Live

**Date:** 2026-09-05 (early morning CEST) · **Branch:** `eval/2026-09-01-thesis-probe` · **Owner:** Daniel (d.zubrik@me.com)
**Written by:** the outgoing Claude session. Everything below is verified against the repo, the Live set, or Daniel's own words unless marked *unverified*.

This document tells you the goal, what has been tried, what you can use, and where things are.
It deliberately does **not** tell you how to get there. Find your own way, with full research, and
show Daniel results he can hear.

---

## 1. The goal, in Daniel's terms

Daniel is building a focus-music product (the Endel / Brain.fm category; business context in
`docs/original-handoff.md` and `docs/2026-09-02-what-users-like-dislike-and-the-moat.md`). The music
side has one target right now, which he calls **Level 1**:

> Hit the exact spot of Endel's "Deeper Focus" soundscape (built on Plastikman / Richie Hawtin
> stems) with *different* tracks in the same style, at a level a professional producer would sign.

He calls the genre **hypnotic minimal techno**. Never call it "dub techno" (he corrected that
explicitly; dub is at most a later addition). Character: heavy deep bass, hypnotic repeating elements,
slow, volatile filter movement, no drops, no melody, no pads, monotone in the good sense, "Berlin".

Daniel is not a programmer and does not produce music himself. He judges **entirely by ear**, on
external headphones, with Live open on his second monitor. Every one of eleven rounds so far was decided
by a taste verdict, never by a number. He wants the agent at his side in Live, driving channel by channel
while he listens, and he wants to compare instruments as you go.

Success criterion, as stated by him across sessions: a loop that a listener would take for a real
producer's hypnotic techno track, that could run for 7 minutes and stay interesting through subtle
movement, not through events.

---

## 2. What the reference actually is (measured)

`research/ear-test/endel-deeper-focus-analysis-2026-09-05.md` is a full teardown of a 7:47 iPhone
capture of Deeper Focus (`ref02`, copyrighted study material, never in the repo, never fed to a
generator; lives under `~/Documents/AI Agent Outputs/Artifacts/flow-audio-references/`). The numbers
you will keep coming back to:

- 120.2 BPM, key C, one 2.00 s bar repeated ~234 times.
- Three layers only: a kick on every beat tuned to C2 (~66 Hz) ringing ~370 ms; a bass that see-saws
  every half bar between an E2 pedal and a partner note (D2, later C2, later G2); one quiet top layer at
  roughly 3.4 % of the energy, about −12.6 dB under the kick RMS.
- The top layer's filter cycles every ~7.66 s while its volume cycles every ~8.00 s, so the two never
  line up (the "never-identical detail" Daniel wants). Dotted-quarter echo ≈ 749 ms.
- Under 0.5 % of the energy sits above 2 kHz. Loudness range ≈ 0.9 LU. It is dark and constant.

Plots in `research/ear-test/plots/endel/`; script `research/ear-test/analyse-endel.py`.

---

## 3. What has been tried, and the verdicts

Full chronological log with Daniel's verbatim words: `research/ear-test/generation-log-2026-09-02.md`.
Short version:

| Round | Approach | Verdict |
|---|---|---|
| 1–4 (Sep 2) | ElevenLabs, Magenta RT, coded synth (numpy), Surge XT patches, bass-only layer stacks | "generic", "computer-generated", "they all sound the same" |
| 5 (Sep 2) | ACE-Step 1.5, Lyria RealTime | Lyria "quality awesome" but "paddy, spacy, not hypnotic"; ACE-Step good sound, boring arrangement, goes silent |
| 6 (Sep 2) | Lyria one-knob-per-clip, fixed seed | "worse, too unpredictable, back to the drawing board" → generators are **out** as songwriters |
| Ableton r1 (Sep 5) | Stock rebuild of the measured recipe: Operator kick, Operator+Saturator bass, Analog chord through Auto Filter/Auto Pan/Echo | **Kick and bass passed** (first bass to pass in seven rounds). Top layer "terrible, way too loud, not interesting", reads as brass |
| Ableton r2 (Sep 5) | Same kick+bass, four quiet top-layer candidates | Only the ticking pluck (D4, five off-grid hits per bar, S&H filter, 3/16 echo) "goes in the right direction". Bass now "a little bit primitive". "Definitely needs still more channels" |
| Live driving (Sep 5) | Bass filter-envelope edit; six Live Core Library bass presets (Drift, Analog, Operator, Wavetable) on separate tracks so he could A/B | Edit "absolutely terrible", reverted. All six presets: "not what I'm looking for at all, not even close" |
| Riemann loops (Sep 5) | Free Riemann Techno Starter pack, kick+bass+perc+texture loops warped to 120.2 | "way too aggressive, we don't need loops, we need instruments, synthesizers" |

Patterns worth knowing before you start:

- Every failure was a **sound-character** failure, not a structure failure. Tempo, key, note patterns
  and the kick/bass idea are settled and passed by ear.
- Measurement-driven design does not converge (four rounds proved that; see the Sep 2 07:45 entry).
  Measure to screen, never to decide.
- Subagents running long Live sessions stalled twice; sound design rounds belong in the main session
  with Daniel listening.
- Daniel's last stated belief: the stock instruments and presets are the bottleneck and a real
  synthesizer is needed. The outgoing session disagreed (professionally made Core Library presets also
  failed, which points at what the sounds *do* rather than oscillator quality) and recommended he install
  the u-he Diva demo, with Vital as the free alternative. He has not installed anything yet. Treat both
  views as hypotheses, not conclusions.

---

## 4. Research already on disk (read before searching the web again)

All under `research/`, each with saved primary sources next to it (`src-*.txt`, `sources/`, `sonar-*.json`).

- `production-options/plastikman-endel-sound-2026-09-05.md` — how Hawtin made these sounds (hardware,
  tom/conga through resonant filters, tape/BBD delays) and what Endel's stem layering does.
- `production-options/hypnotic-top-layer-2026-09-05.md` — why r1/r2 top layers read as primitive (one
  tempo-synced LFO on one cutoff; too bright, not too loud; wrong instrument class), a round-3 brief with
  three untried recipes (resonant percussion via DS Tom → Auto Filter → Resonators; stacked band-limited
  pad; Corpus/Collision ping), a buy/no-buy section on non-stock plugins (only Surreal Machines Dub
  Machines had a documented fit; Diva/Serum/Soundtoys/Valhalla are scene folklore, not evidence).
- `production-options/hypnotic-craft-2026-09-05.md` — general craft, artist-agnostic: Eno-style
  decorrelated loops, Attack Magazine LFO and sparse-placement techniques, Note Chance / Velocity
  Deviation (never yet used), Rod Modell long-render-then-edit.
- `production-options/youtube-tutorials-hypnotic-techno-2026-09-05.md` — digest of six tutorial
  transcripts: consensus channel template, five-minute bar map, Operator rumble/sub recipes, hook recipes,
  what transfers to 120 BPM and what is club-only.
- `production-options/ableton-agent-tooling-2026-09-03.md` — survey of Live agent tooling and skills.
- `production-options/deep-research-tool-path-2026-09-02.md`, `loop-sources-licence-2026-09-02.md`,
  `producer-brief-2026-09-02.md` (draft brief for commissioning a producer, not sent).
- `production-options/synth-instruments-2026-09-02.md`, `ear-test/surge-arm-…`, `ear-test/synth-arm-…` — free/open synth survey
  (Surge XT, Vital, Open303, Airwindows, Cardinal) and the failed coded-synth rounds.
- `ear-test/ableton-r1-2026-09-05.md`, `ableton-r2-2026-09-05.md` — exact device settings and
  measurements of the two Live rounds.
- `ear-test/spec-from-references.md`, `palettes.md`, `reference-manifest.md` — earlier spec work.
- `.claude/skills/hypnotic-techno-sound-design/SKILL.md` — a project skill distilled from the above:
  target table, recipes, an anti-primitive modulation checklist, level/band placement, 4/8/16/32-bar
  variation rules, and a 12-point pre-export self-review. Read it, then decide for yourself whether it is
  right. The other skills in `.claude/skills/` came from the Florkin `claude-ableton-skills` set and are
  unproven.

---

## 5. Capabilities you have

**Ableton Live 12.4.5 Suite** is installed, authorised and running on Daniel's MacBook Pro. All ten
factory packs are in. Setup record: `~/Code/otsinc15/ableton-tools/SETUP.md`.

**ableton-mcp** (remote script 1.7.0, control surface slot 1) is wired through `.mcp.json` with telemetry
disabled. It can: read session/track/device info, create MIDI and audio tracks, create clips, add/read/
clear notes, load any browser item by URI (`query:Synths#Operator:Bass:FileId_N` style; folders under
`instruments/`, `Drift/Bass`, `Analog/Bass`, `Operator/Bass`, `Wavetable/Bass` were listed), set any device
parameter, fire/stop clips, start/stop playback, set tempo, name tracks/clips, create audio clips from a
WAV path. It **cannot** write automation or clip envelopes, mute/solo tracks, or open dialogs. A raw
socket helper (`send(type, params)` to 127.0.0.1:9877) lives in the previous session's scratchpad and is
trivial to recreate. Forks that claim automation support (dreamrec/LivePilot, freekmurze/ableton-ai,
uisato/ableton-mcp-extended) are catalogued in the tooling doc, none verified. Daniel has an open
question whether to add automation-writing to our own remote script before more rounds; it is his call.

**AbletonOSC** is installed in control surface slot 2 (`~/Code/otsinc15/ableton-tools/AbletonOSC`), not yet
used in anger.

**Computer use** works on Live for what MCP cannot reach: real click on a dropdown then `AXPress` on the
menu item via System Events; export via File > Export Audio/Video; the Track Activator checkboxes are
AX elements 71, 85, 99, … (step 14) for tracks 0–9 in the current window layout. Screenshots do not show
Live's popup menus.

**Analysis pipeline**: `research/ear-test/measure-clips.py` (LUFS, LRA, band shares, onsets, centroid),
`analyse-endel.py`, `master.py`. Demucs (htdemucs) stem separation is available and was used on Lyria
output and on the reference. Python 3 with numpy/librosa on the laptop.

**Listening pages**: private claude.ai artifacts ("Flow Audio Listening Room", "Ableton round 2") with
base64 AAC clips, built by a small script; Daniel uses them on his phone when not at Live. A per-round
JSON of measurements sits next to each export.

**Web research**: WebSearch/WebFetch, an OpenRouter key in `~/.claude/.env` (never print it) used for
Perplexity Sonar deep-research passes, YouTube transcripts via `uvx --from youtube-transcript-api`.
Never open perplexity.ai in a browser.

**Compute**: this laptop plus an always-on Mac mini over Tailscale (`ssh cyrus@cyruss-mac-mini-1.tail976740.ts.net`)
that ran ACE-Step; anything that must run unattended goes there.

---

## 6. Resources and their locations

- Live sets: `~/Music/Ableton/flow-audio/endel-rebuild-r2 Project/endel-rebuild-r2.als` (last saved
  before the live-driving edits). The currently open, unsaved set has 29 tracks: 0 KICK and 1 BASS from r1
  (bass reverted to the approved chain: Operator algorithm 10, sine A 1.0, B 0.4, C 0.24, glide 0.15,
  Saturator drive 0.54; notes E2/D2 alternating every 2 beats), 2–7 the six rejected bass presets, 8–14
  leftovers of round 2 (PAD-C on 13 is the ticking pluck that "goes in the right direction"), 15–28 the
  rejected Riemann loops. Save it under a new name before doing anything, or start clean; Daniel will not
  mind either.
- Exports: `~/Documents/AI Agent Outputs/Artifacts/flow-audio-candidates/ableton-r1/`, `ableton-r2/`
  (16-bar WAVs plus `measurements-r2.json`), earlier rounds alongside.
- Reference audio and stems: `~/Documents/AI Agent Outputs/Artifacts/flow-audio-references/` (study only).
- Samples: `~/Music/Ableton/flow-audio/samples/` (Riemann free pack, 223 WAV, licence in
  `loop-sources-licence-2026-09-02.md`: fine for internal tests and pre-rendered output, not for
  embedding raw in an app).
- Templates identified but **not bought** (Daniel's purchase if wanted): Shed Skin "Raw Hypnotic Techno
  Live 12 project" (€18, native + some Max for Live, Operator main sound, all rights reserved),
  Audioreakt "Hypnotic Techno template" (€29.90, stock only, walkthrough videos), Riemann/Sinee template
  (€29.95). Synths identified: u-he Diva (demo free), Vital (free), Surge XT (free), TAL and Roland Cloud
  emulations of the 303/101/909/Juno, none installed.
- Memory for this project: `~/.claude/projects/-Users-othersideinc-Code-otsinc15-flow-audio-research/memory/`
  (engine verdicts, Live setup, the genre-label correction).

---

## 7. Ground rules Daniel has set (non-negotiable)

- Start every reply with "Daniel, …", be brief, no process narration between tool calls; completion
  messages open with a three-line TLDR. Estimate effort in agent hours.
- He listens live; drive Live channel by channel and let him toggle. When he rejects something, revert
  exactly, then log his words in `generation-log-2026-09-02.md`.
- Purchases, account creation, plugin installs, downloads and outbound messages are his actions. Ask,
  then wait.
- Never feed Endel or any copyrighted reference into a generator, never copy it into the repo, never
  commit audio or secrets. Never commit to `main`; stage files by name on the feature branch and open the PR.
- Do not propose more generator rounds (ElevenLabs, Lyria, ACE-Step, Suno as songwriter); that door is closed.
- Never call the MCP's `set_dataset_consent`, `submit_intent`, `prefer_candidate`, `rate_last_action`,
  `reject_last_action`.

---

## 8. Open decisions that are Daniel's

1. Install a synthesizer (Diva demo recommended by the outgoing session; Vital free) — or not.
2. Buy a project template to study (Shed Skin €18 was the outgoing pick) — or not.
3. Add automation writing to our own Live remote script before further rounds — or work around it.
4. Commission a producer for sound design only (brief drafted in `producer-brief-2026-09-02.md`) — the
   fallback he agreed to on Sep 2 if in-house rounds keep failing.

Everything else is yours to decide. Research as deeply as you need, then put sound in his headphones.
