# Agent-Driven Ableton Live 12 for Dub Techno — Tooling Survey (2026-09-03)

## Top 5, ranked by usefulness to the goal

1. **AbletonOSC** (ideoforms) — the real foundation. MIT, ~799★, active (292 commits), aims to expose the *entire* Live Object Model over OSC: tracks, clips, devices, params, MIDI mapping, scenes, view nav. It's the lowest-level, most complete control surface — everything else (MCP servers) is a thin wrapper on top of LOM/OSC. Mature, no vapourware.
2. **ahujasid/ableton-mcp** — most-used MCP wrapper (MIT, ~3.0k★, 70 commits). Solid for track/clip/device creation, MIDI note writing, transport, tempo. Cannot do audio export, stem separation, or fine-grained automation curves on its own — it's a control layer, not a mixing/mastering brain. Best paired with a skills file for actual production knowledge.
3. **glincker/ableton-skills** — the closest thing to "encoded production knowledge" for an agent. MIT, 12 skills (mixing diagnostics, arrangement coaching, sound design, sidechain setup), explicitly "co-pilot not generator," cites real references (Owsinski, Senior). Genre packs (house/trap/lofi) exist or are roadmapped; no dub-techno-specific pack yet — would need to write one, but the skill *format* and MCP pairing already work.
4. **Ableton Live 12.3 Stem Separation** (native, Suite only) — genuinely useful and agent-drivable indirectly: right-click/menu command splits any clip into vocals/bass/drums/other via local ML (Music AI-derived), no internet needed. Useful for pulling references apart to study/reuse elements. Native, well-documented, actively shipped (12.3, 2026).
5. **Mixed In Key Wingman** ($79, one-time) — listens to audio and suggests chords/bassline MIDI, does its own stem separation and audio-to-MIDI. Not agent-controllable via API (no documented automation/API surface found) — useful as a human-in-the-loop songwriting aid alongside the agent, not something Claude Code can drive directly.

## 1. Agent control of Ableton (MCP servers / OSC)

| Tool | URL | Last update | License | Assessment |
|---|---|---|---|---|
| AbletonOSC | [github.com/ideoforms/AbletonOSC](https://github.com/ideoforms/AbletonOSC) | active, 292 commits | MIT | Most complete LOM coverage; the substrate most MCP servers build on. No native audio export/stem separation (that's Live's job, not OSC's). |
| ableton-mcp (ahujasid) | [github.com/ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp) | active, 70 commits, 3.0k★ | MIT | The de-facto standard Claude/Cursor MCP. Track/clip/device create, MIDI notes, transport, tempo. No automation-curve writing, no audio bounce/export, no stem separation exposed. |
| Producer Pal (adamjmurray) | [github.com/adamjmurray/producer-pal](https://github.com/adamjmurray/producer-pal) | active, 271★ | GPL-3.0 | Multi-provider (Claude/Gemini/ChatGPT/Ollama), text-based music notation instead of raw MIDI, also exposes a plain REST API (agent optional). Explicitly a "co-pilot," self-limits autonomous composition. |
| Forks (itsuzef, jpoindexter "200+ tools", chaudepark, sharray2918) | GitHub search | mixed activity | mostly MIT | Community forks adding return-track/FX/mixing control or multi-LLM support beyond the original. Quality/maintenance varies — vet before use; not independently verified here. |
| ableton-osc-mcp (nozomi-koborinai) | [github.com/nozomi-koborinai/ableton-osc-mcp](https://github.com/nozomi-koborinai/ableton-osc-mcp) | unknown | unknown | Thin MCP-over-AbletonOSC bridge; smaller project, not vetted for maturity. |

**Common gap across all of them:** none write automation *curves* natively, none export/bounce audio via the protocol, none do stem separation themselves (that's Live 12.3's native feature, separate from MCP/OSC). Agent + MCP gets you composition/arrangement/device-loading; mixing/export still needs either manual steps or Live's own automation recording.

## 2. Claude Code skills for music production

- **glincker/ableton-skills** — [github.com/glincker/ableton-skills](https://github.com/glincker/ableton-skills), MIT, SKILL.md format, pairs with any Ableton MCP. 12 skills covering mixing diagnostics, MIDI humanization, arrangement, sound design, vocal processing, sidechain/tempo guidance, focused on stock instruments (Operator, Wavetable, Analog, Drift). No dub-techno-specific skill yet — genre packs are partly roadmap.
- **bitwize-music-studio/claude-ai-music-skills** — Suno-focused, not Ableton; not directly applicable.
- **Ronvaknins/ableton-extensions-skill** — teaches agents to build Ableton Extensions SDK (TypeScript) devices, i.e. for building new M4L-style extensions, not for producing tracks.
- No official Anthropic skill for music/Ableton in anthropics/skills as of this search.

## 3. Ableton-native resources

- **Live 12.3 Stem Separation** (Suite only) — local ML split into vocals/bass/drums/other, high-quality and high-speed modes, works offline. [ableton.com/stem-separation-in-ableton-live](https://www.ableton.com/stem-separation-in-ableton-live/)
- **Live Object Model / Control Surface Python scripts / Max for Live** — the official scripting layer AbletonOSC and MCP servers sit on; well documented, stable, been production-grade for years.
- **Learning Music / Learning Synths** (learningmusic.ableton.com, learningsynths.ableton.com) — good for a non-producer to build ear/theory intuition alongside agent-driven work; not agent-drivable, browser-based lessons.

## 4. AI mixing/mastering plugins

| Tool | Price | Agent-drivable? | Note |
|---|---|---|---|
| iZotope Neutron 5 | Elements $49, full higher | No known API/automation hook | Plugin-only, manual mixing assistant inside a channel strip. |
| iZotope Ozone 11 | Standard $249 / Advanced $499 | No | Mastering assistant, analyzes mix, sets EQ/dynamics/limiting chain. |
| Sonible smart:bundle | $599 (plugins from $129) | No | AI EQ/dynamics suite, no agent API found. |
| Mixed In Key Wingman | $79 one-time | No | Chord/bass suggestion + its own stem separation + audio-to-MIDI; human-driven, no documented API. |

None of these expose an API an agent can call — they're all manual-use VSTs. The agent's role is limited to instructing the human where/how to apply them, not operating them directly.

## 5. Dub techno / hypnotic minimal reference material

- Attack Magazine "Basic Channel-Style Dub Techno" — beat/technique breakdown, foldable into a skill file. [attackmagazine.com](https://www.attackmagazine.com/technique/beat-dissected/basic-channel-style-dub-techno/)
- Pheek's Guide To Making Dub Techno — production workflow. [audioservices.studio](https://audioservices.studio/production/pheeks-dub-techno-making-guide)
- Studio Brootle "Dub Techno Tutorial: 4 Ingredients" and Ableton-specific tutorial — practical, DAW-specific. [studiobrootle.com](https://www.studiobrootle.com/dub-techno-tutorial-4-ingredients/)
- Audiotent "Dub Techno Chord Sound Design" — three-oscillator (square sub + two saw) chord-stab patch design, directly encodable as synth-preset instructions. [audiotent.com](https://www.audiotent.com/blogs/production-tips/dub-techno-chord-sound-design)
- ADSR Massive dub-techno stab tutorial — device-specific patch recipe. [adsrsounds.com](https://www.adsrsounds.com/ni-massive-tutorials/dub-techno-synth-stab-tutorial/)
- No dedicated Plastikman-acid-bass writeup surfaced in this search; would need a follow-up pass (likely found in Attack Magazine's TB-303/acid-bass series or YouTube teardown channels).

These five sources give enough concrete parameter-level detail (oscillator config, filter-delay chains, sidechain approach, minor-chord stab voicing) to write directly into a `SKILL.md` for dub techno / hypnotic minimal.
