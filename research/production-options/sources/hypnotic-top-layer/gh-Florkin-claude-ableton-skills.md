# claude-ableton-skills

A panel of **20 advanced [Claude Code](https://claude.com/claude-code) skills** for electronic-music
production in **Ableton Live 12**, driven by the **[LivePilot](https://github.com/dreamrec/LivePilot)** MCP
copilot. Focused on **techno, house, and electro**. English, advanced level, native-device-first
(Operator, Wavetable, Drift, Meld, Simpler, Drum Rack, EQ Eight, Glue, Saturator, Roar, Echo, Hybrid Reverb,
Auto Filter, Utility, Limiter…), with Max for Live and third-party (Serum/Diva) notes where useful.

Each skill is a `SKILL.md` (YAML frontmatter + body) that Claude can auto-invoke from its `description:`, or you
can call explicitly with `/<skill-name>`. Two skills ship a `references/` cookbook (arrangement maps, effect-rack
recipes). Every skill has a **LivePilot playbook** section mapping the workflow to concrete `mcp__livepilot__*` tools.

## Requirements

- [Claude Code](https://claude.com/claude-code) (or any client that loads `.claude/skills/`).
- **Ableton Live 12** (Suite for the Max for Live analyzer).
- **[LivePilot](https://github.com/dreamrec/LivePilot)** connected as an MCP server (the skills reference its tools).
- Optional but assumed by some recipes: Splice, Max for Live, third-party synths (Serum, Diva…).

## Install

**Global** (available in every project):

```bash
git clone https://github.com/Florkin/claude-ableton-skills.git
cp -R claude-ableton-skills/skills/* ~/.claude/skills/
```

**Per-project** (only when working from that project):

```bash
cp -R claude-ableton-skills/skills/* /path/to/your-project/.claude/skills/
```

Skills are auto-discovered on the next session. They trigger from their `description:` keywords, or invoke one
directly, e.g. `/arrangement-structure` or `/effect-racks`.

## The panel

See [`skills/README.md`](skills/README.md) for the full index and how the skills compose. Summary:

| Group | Skills |
|---|---|
| **Piloting** | `livepilot-operation` (hub) · `production-workflow` |
| **Genres** | `genre-techno` · `genre-house` · `genre-electro` |
| **Arrangement** | `arrangement-structure` (+ bar-by-bar maps) · `transitions-and-fx` · `automation-and-movement` |
| **Harmony** | `harmony-and-melody` |
| **Racks** | `effect-racks` (+ 10-rack cookbook) · `instrument-racks-and-layering` |
| **Sound design** | `bass-design` · `synth-leads-stabs-plucks` · `pads-atmospheres-textures` |
| **Rhythm** | `drums-and-groove` |
| **Mix / master** | `mixing-club` · `low-end-and-sidechain` · `mastering-loudness` |
| **Sampling / finishing** | `sampling-and-sound-sourcing` · `finishing-tracks` |

Skill file anatomy: `When to use` / `TL;DR` / domain sections / **`LivePilot playbook`** / `Common mistakes` / `See also`.

## Notes

- **Unofficial / community.** Not affiliated with Ableton or with the LivePilot project. LivePilot is a separate,
  fast-moving pre-1.0 tool — pin a version; some tool names/behaviors may drift between releases.
- All device settings and numbers are **starting points** — dial by ear against a reference.
- Authored with Claude Code.

## License

[MIT](LICENSE).
