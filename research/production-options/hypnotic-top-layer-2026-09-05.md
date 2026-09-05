# Hypnotic top layers — why rounds 1–2 sounded primitive, and what to do in round 3

Compiled 2026-09-05. Genre label: **hypnotic minimal techno** (Endel "Deeper Focus" / Plastikman lane).
Method: Perplexity `sonar-pro` via OpenRouter for discovery (raw JSON in
`sources/hypnotic-top-layer/q*-*.json`), then every kept claim re-fetched from its primary page
(`sources/hypnotic-top-layer/src-*.txt`, URL + fetch date at top of each) and cited below. Anything not
re-verified is tagged **[unverified]**; anything that is my reasoning rather than a source is tagged
**[agent inference]**. Live's installed device/pack list was read back over the ableton MCP (read-only).

Not repeated here: `techno-pattern-book-2026-09-02.md` §§3–8 (delay/feedback numbers) and
`plastikman-endel-sound-2026-09-05.md` (Hawtin gear and the Endel engine). Both are cited instead.

---

## 1. Plain-language summary

1. Round 2's top layers were **one synth + one synced LFO on a cutoff**. That is the textbook
   beginner patch, and every source on evolving textures says the same thing: one modulator on one
   parameter is heard, learned and dismissed by the ear within a few cycles.
2. Worse, the LFO was **tempo-synced**, so it repeats *exactly* every 4 bars forever. The reference does
   not do that: our own measurement found the pad's **filter cycle at 7.66 s and its volume cycle at
   8.00 s** — deliberately not the same number. Two nearly-equal but unequal periods drift against each
   other and only realign every ~90 bars. That drift *is* the hypnosis.
3. "Way too loud" was probably really **"too bright."** The reference pad puts 45 % of its energy in
   150–500 Hz, 48 % in 500 Hz–2 kHz and **0.43 % above 2 kHz**. Round 1 had nine times the reference's
   2–8 kHz share. A layer placed above 2 kHz sticks out at any fader level, because there is nothing
   else up there.
4. Wrong instrument class as well. Hawtin's actual *Consumed* top layer was a **tom/conga opened and
   closed through a resonant filter**, not a saw pad. Live 12 ships **DS Tom, DS FM, DS Clang, Corpus,
   Resonators and Collision** — a whole family of resonant/physical-model percussion voices this project
   has not touched. All confirmed installed on this Mac.
5. And a tooling limit was doing real damage: the MCP in use has **no automation and no clip-envelope
   API** (verified — see §6), so round 2 had to fake a 22 dB swell with a tremolo device. Forks that can
   write automation now exist.

**Three highest-leverage changes for round 3**

- **Detune the modulation.** Run the filter cycle and the amplitude cycle at *free-running* rates a few
  percent apart (e.g. 0.1305 Hz and 0.1250 Hz), not one synced LFO doing both. Add a third, much slower
  free source. Nothing realigns; the loop stops sounding like a loop.
- **Band-limit hard and modulate timbre, not just cutoff.** HP ~150 Hz / LP ~2 kHz on the top bus, then
  put the movement into FM amount, resonance, delay time and stereo, not only the filter frequency.
- **Change the instrument.** Try a resonant/percussive voice (DS Tom or Operator FM ping into
  Corpus/Resonators) as at least one of the three candidates, instead of a third saw pad.

---

## 2. Findings per angle

### 2.1 Cross-modulation with stock tools

**What ships.** Live 12's Max for Live devices are documented in manual ch. 32
(`src-ableton-m4l-devices-manual.txt`, https://www.ableton.com/en/live-manual/12/max-for-live-devices/).
Instruments: **DS Clang, DS Clap, DS Cymbal, DS FM, DS HH, DS Kick, DS Snare, DS Tom**. Audio effects:
**Align Delay, Envelope Follower, LFO, Shaper**. MIDI effects: **Expression Control, MIDI Monitor, MPE
Control, Note Echo, Shaper MIDI**. Every one of those is present in this Mac's browser (read back over
MCP, 2026-09-05), plus the *Sequencers* pack (**Melodic Steps, Rhythmic Steps, SQ Sequencer, Step Arp,
CC Control**) and *Creative Extensions* (**Pitch Hack, Re-Enveloper, Gated Delay, Spectral Blur, Color
Limiter, Convolution Reverb**).

**The mapping problem, and the way around it.** The LFO / Shaper / Envelope Follower devices map targets
through a **Map button plus a Multimap panel, up to eight targets** — a UI action, not an API call
(Ableton manual ch. 32; Perplexity q1 corroborates the eight-slot figure, **[unverified]** as to the exact
count since the fetched manual text does not restate the number). Confirmed independently by the
`freekmurze/ableton-ai` README, which tells its users to say so out loud: *"Some things in Live are
dropdowns you can't set through the API: the LFO Map button, a Compressor's sidechain source, Drift's mod
matrix routing"* (https://github.com/freekmurze/ableton-ai).

**But several stock devices carry their own modulators internally, and those are plain device parameters
— fully scriptable, zero UI clicks.** This is the key practical finding of this round. From the Live 12
Audio Effect Reference (`src-ableton-audio-fx-reference.txt`,
https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/):

| Device | Internal modulation available without any Map button |
|---|---|
| **Auto Filter** | An LFO with waves **Sine, Triangle, Saw, Square, Ramp Up, Ramp Down, Wander, S&H**; rate in **Hz, seconds, or synced divisions**; **Phase** (0–180°) *or* **Spin** (% rate detune) to decorrelate L/R; **Quantization** modes Steps and S&H; **plus a separate envelope follower** that can run alongside the LFO. Two independent movement sources in one device. |
| **Echo** | A **Modulation tab** LFO (sine/tri/saw up/saw down/square/**noise**), free-Hz or synced, with **Mod Delay** (modulates *delay time*), **Modulation x4**, **Mod Filter**, L/R **Phase**, and **Env Mix** to blend the LFO with an envelope follower. Character tab adds **Wobble** (irregular delay-time drift), **Noise**, and **Ducking** with its own threshold/release. |
| **Roar** | A four-source **Modulation Matrix**: **LFO 1, LFO 2, Env** (envelope follower with attack/release/threshold/frequency/width) and **Noise** with types **Simplex, Wander, S&H, Brown**. LFOs have five waves, Free/Synced/Triplet/Dotted/Sixteenth modes, plus **Morph** and **Smooth**. |
| **Spectral Resonator** | Modulation modes **Chorus / Wander / Granular** with **Mod Rate** and **Pch. Mod**. |
| **Auto Pan-Tremolo, Phaser-Flanger, Shifter, Chorus-Ensemble, Corpus** | Each has its own LFO with rate/amount/phase parameters. |

Caveat on Roar: the manual says *"Clicking a parameter while the Matrix tab is open will set it as a
modulation target"* — the **routing** is a UI click. Whether the matrix *cells* are exposed as named
device parameters (so an agent could set amounts on already-routed cells, or on a saved preset's
routing) **[to verify in-session]** by loading Roar on a scratch track and calling
`get_device_parameters`. If they are, Roar alone gives four cross-modulating sources with no UI at all.

**Cross-modulation as the aesthetic target.** Hawtin on *Consumed*: *"Consumed is an album of feedback.
Everything was cross-modulating everything else"* (Sound On Sound, Classic Tracks,
https://www.soundonsound.com/techniques/classic-tracks-plastikman-consumed — already fetched in the
parent directory, see `plastikman-endel-sound-2026-09-05.md` §Q2).

### 2.2 What producers actually reach for, and what is installed here

**Sourced technique.** The single most useful teardown found is Attack Magazine's *Crafting Ambient
Techno Pads* (`src-attack-ambient-techno-pads.txt`,
https://www.attackmagazine.com/technique/synth-secrets/crafting-ambient-techno-pads/). It is built in
FabFilter Twin 3, not stock, but its *structure* is exactly what round 2 was missing:

- **Four oscillators at −1 / 0 / +1 / +2 octaves** at −INF / −11 / −8 / −12 dB — a stacked, register-spread
  body rather than one saw.
- Amp envelope **Attack 5 s, Decay 1.5 s, Sustain −3 dB, Release 1 s**; a later layer gets a **15 s attack**.
- **Three filters, not one**: LP 720 Hz 24 dB, **HP 280 Hz** 24 dB, and a low shelf at 280 Hz — the pad is
  band-limited to roughly 280 Hz–720 Hz before anything else happens.
- **Two LFOs, and one of them is modulated by an envelope.** XLFO 1 at 13 Hz routed to **oscillator sync**
  (not cutoff) on two oscillators and to filter pan; a 12-second-attack envelope then modulates **XLFO 1's
  own rate**, so the modulation slows down over time. XLFO 2 at 0.5 Hz to more osc sync and to filter
  frequency offset **at an amount of 0.045** — deliberately tiny.
- Delay at 50 % with **70 % feedback**, ping-pong.
- Sidechain via **Ableton's stock Auto Filter**, sidechain on, keyed from the kick pre-FX, filter envelope
  at 127.

Meta-modulation is corroborated by a second, independent source: Mojulate's *Creating An Evolving Pad*
(`src-mojulate-evolving-pad.txt`, https://mojulate.com/blogs/news/creating-an-evolving-pad) patches
**LFO 3 → LFO 1's rate**, LFO 1 → oscillator volumes, LFO 2 → oscillator pans, with tempo sync switched
off so the periods drift. Same idea in MusicRadar's oscillator-stacking piece
(`src-musicradar-oscillator-stacking.txt`,
https://www.musicradar.com/how-to/how-to-create-evolving-ambient-pads-with-oscillator-stacking).

**Filter-ping percussion.** The generic recipe — short impulse into a high-resonance band-pass, cutoff as
pitch — is well attested but mostly on hardware: *Octatrack Synthesis: Filter Ping Percussion*
(https://www.elektronauts.com/t/octatrack-synthesis-filter-ping-percussion-video/86508) and the Erica
Synths Graphic Resonant Filterbank demo (https://www.youtube.com/watch?v=8nS5cuuSKS4), which notes the
filterbank can self-oscillate for drones and be pinged with pulses for organic percussion. Perplexity's
Ableton-specific mapping of that idea onto Auto Filter / Operator / Resonators / Corpus / Collision is
**[unverified]** — no stock-Ableton filter-ping tutorial was found (see Not found).

**Confirmed installed on this Mac** (ableton MCP browser read, 2026-09-05):

- *Instruments*: Analog, Collision, Drift, Drum Rack, Drum Sampler, **DS Clang / Clap / Cymbal / FM / HH /
  Kick / Snare / Tom**, Electric, Granulator III, Impulse, Meld, Operator, **Poli**, Sampler, Simpler,
  Tension, Wavetable.
- *Audio effects*: Auto Filter, Auto Pan-Tremolo, Auto Shift, Corpus, Echo, **Envelope Follower**, **LFO**,
  **Shaper**, Resonators, **Roar**, **Spectral Resonator**, Spectral Time, Spectral Blur, Shifter,
  Grain Delay, Filter Delay, Gated Delay, Pitch Hack, Re-Enveloper, PitchLoop89, Hybrid Reverb,
  Convolution Reverb (+ Pro), Drum Buss, Saturator, Vinyl Distortion, Redux, Erosion.
- *Packs installed*: Core Library, Drum Essentials, Synth Essentials, Creative Extensions, Convolution
  Reverb, Drive and Glow, Granulator III, Lost and Found, PitchLoop89, Punch and Tilt, **Sequencers**.
- **Not installed here**: Skitter and Step, Inspired by Nature, Beat Tools, Drum Machines, Build and Drop,
  Chop and Swing. These are factory Live 12 Packs per Perplexity q2 **[unverified — help.ableton.com's
  "Updated Packs in Live 12" page is behind a Cloudflare interstitial and could not be re-fetched]**, so
  they are free to download but are **not on disk**; do not write a recipe that depends on them without
  downloading first. Note this rules out the exact samples used by the Attack *Spastik* tutorial.
- **Surreal Machines Dub Machines (Diffuse / Magnetic) is a paid add-on, not Suite-included** —
  re-fetched product page shows a price and "Requirements: Live 11 Standard & Max for Live"
  (`src-ableton-dub-machines.txt`, https://www.ableton.com/en/packs/dub-machines/). Not installed.
- "Bark of Dog" is a third-party plugin, not an Ableton pack (Perplexity q2).

### 2.3 Named tutorials and teardowns

| Source | URL | What it actually teaches | Status |
|---|---|---|---|
| Attack, *Spastik-Style Percussive Techno* (Beat Dissected) | https://www.attackmagazine.com/technique/beat-dissected/spastik-style-percussive-techno/ | Explicit Plastikman emulation at **127 BPM**, manual swing. 909 closed hat + **Velocity MIDI device with Random** for velocity variation, **EQ Eight cutting lows to ~1.8 kHz**, hat **panned 50R**; a **reversed 707 open hat at −36 dB** hitting just before each half-bar; 808 long ride at **−24 dB** doubling the kick; Glue Compressor at **2–3 dB GR** on the drum bus. | re-fetched, `src-attack-spastik.txt` |
| Attack, *Crafting Ambient Techno Pads* | https://www.attackmagazine.com/technique/synth-secrets/crafting-ambient-techno-pads/ | See §2.2 — 4-osc stack, 5 s/15 s attacks, three filters, two XLFOs, envelope modulating an LFO's rate, stock Auto Filter sidechain from kick. | re-fetched, `src-attack-ambient-techno-pads.txt` |
| Attack, *Thumping Techno* | https://www.attackmagazine.com/technique/beat-dissected/thumping-techno/ | 808 tom into a large-but-short reverb then bitcrushed; **909 rimshot duplicated, tuned high and low to the track key, heavily overdriven and 24 dB/oct high-passed** into a pitched percussive ping; 909 ride through plate reverb + HPF. | re-fetched, `src-attack-thumping-techno-2.txt` |
| SOS, *Classic Tracks: Plastikman 'Consumed'* | https://www.soundonsound.com/techniques/classic-tracks-plastikman-consumed | The title track's top layer is a **tom/conga slowly opened and closed through a Serge filter with a lot of effects**; 909 used as a one-note sequencer; "everything was cross-modulating everything else". | already fetched in parent dir (see `plastikman-endel-sound-2026-09-05.md`) |
| Mojulate, *Creating An Evolving Pad* | https://mojulate.com/blogs/news/creating-an-evolving-pad | LFO 3 → LFO 1 rate; LFO 1 → osc volumes; LFO 2 → osc pans; sync off so periods drift. | re-fetched, `src-mojulate-evolving-pad.txt` |
| MusicRadar, *evolving ambient pads with oscillator stacking* | https://www.musicradar.com/how-to/how-to-create-evolving-ambient-pads-with-oscillator-stacking | Multiple wavetable oscillators each with its own free-running LFO on index and level. | re-fetched, `src-musicradar-oscillator-stacking.txt` |
| Elektronauts, *Octatrack Synthesis: Filter Ping Percussion* | https://www.elektronauts.com/t/octatrack-synthesis-filter-ping-percussion-video/86508 | Excite a resonant filter with a near-silent impulse to make pitched percussion. | not re-fetched **[unverified]** |
| Erica Synths Graphic Resonant Filterbank demo | https://www.youtube.com/watch?v=8nS5cuuSKS4 | Self-oscillation for drones; pinging with pulses for organic percussion. Hardware. | not re-fetched **[unverified]** |
| Attack, *Minimal Techno Sound Design Using Soundtoys* | https://www.attackmagazine.com/technique/tutorials/minimal-techno-sound-design-using-soundtoys/ | Short plate reverbs (~0.5 s decay, low-cut ~140 Hz) with modulation for evolving percussion tails. Third-party plugins. | not re-fetched **[unverified]** |
| Bougaieff PhD thesis (Plastikman method) | https://eprints.hud.ac.uk/id/eprint/18067/1/nbougaiefffinalthesis.pdf | Long improvised takes later edited into tracks. | not re-fetched **[unverified]** |

### 2.4 Level and density

**The measurement we already own is better than anything found online.** From
`endel-deeper-focus-analysis-2026-09-05.md`: the pad stem is **−30.6 dBFS / 3.4 % of mix energy** against
the drums stem's **−18.0 dBFS / 61.2 %** — i.e. **12.6 dB below the kick stem**, with **45.1 % of its own
energy in 150–500 Hz, 48.3 % in 500 Hz–2 kHz, and 0.43 % in 2–8 kHz**. Whole-mix 2–8 kHz is **0.07 %**.
There are **three layers total** (kick, bass, one pad), plus a barely-there HF tick.

Corroborating sourced numbers, all from the re-fetched Attack *Spastik* piece: reversed open hat at
**−36 dB**, long ride at **−24 dB**, drum-bus glue at **2–3 dB gain reduction**. These are the only
hard dB figures for top-layer placement found in a primary source this round.

**Perplexity's own level answer is not usable.** For q4 the model disclosed it could not fetch and was
extrapolating: its "8–15 dB below the kick peak" and "3–4 dB GR at 3:1, 1–5 ms attack, 80–120 ms release"
for a pad sidechain are **[unverified]**. They happen to bracket our measured 12.6 dB, which is mildly
reassuring and nothing more.

**Sidechain, and whether it is scriptable.** The Attack ambient-pads tutorial's method is the one to copy
and it is *not* a Compressor: **Auto Filter with Sidechain switched on, keyed from the kick pre-FX, filter
envelope at 127**, so the kick opens the filter rather than dropping the level. Either way, **selecting
the sidechain audio source is a dropdown = UI click** (freekmurze README, cited above). Everything else —
threshold, ratio, attack, release, envelope amount, mix — is a device parameter and is scriptable.
Consistency check against the reference: drums↔bass envelope cross-correlation is only 0.404 and the bass
AM depth is 3.7 dB, so whatever ducking exists in the reference is **mild**; do not pump.

### 2.5 Agent skills and MCP forks — **this is the headline**

**The MCP currently connected cannot write automation.** Verified directly this session via
`get_remote_script_info`: script version 1.7.0, capabilities are exactly
`get_session_info, get_track_info, get_script_info, get_clip_notes, get_device_parameters,
get_session_snapshot, set_device_parameter, drain_passive_events, create_midi_track, create_audio_track,
create_clip, create_audio_clip, add_notes_to_clip, load_instrument_or_effect, get_arrangement_clips,
duplicate_session_clip_to_arrangement, create_locator, delete_clip, clear_notes_from_clip`.
**No automation, no clip envelopes, no track mute, no browser-preset loading beyond
`load_instrument_or_effect`.** That is exactly the constraint round 2 hit.

GitHub search (API, stars as of 2026-09-05) found several projects that lift it:

| Repo | ★ | What it adds that matters here |
|---|---|---|
| [ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp) | 2968 | The original. Same surface class as ours. |
| [ideoforms/AbletonOSC](https://github.com/ideoforms/AbletonOSC) | 799 | OSC control surface, not MCP. Generic access to the Live Object Model; good for streaming continuous parameter changes from a script. |
| [Simon-Kansara/ableton-live-mcp-server](https://github.com/Simon-Kansara/ableton-live-mcp-server) | 394 | MCP over OSC. |
| [uisato/ableton-mcp-extended](https://github.com/uisato/ableton-mcp-extended) | 257 | README explicitly: *"Automation and Envelopes: Add and clear automation points for any device parameter within a clip. **[This feature isn't working perfectly yet.]** Get information about existing clip envelopes."* — honest about being flaky. |
| [bschoepke/ableton-live-mcp](https://github.com/bschoepke/ableton-live-mcp) | 214 | General-purpose bridge. |
| [xiaolaa2/ableton-copilot-mcp](https://github.com/xiaolaa2/ableton-copilot-mcp) | 91 | Built on ableton-js; Arrangement View operations; README claims *"Support automatic envelope adjustment"*. |
| **[dreamrec/LivePilot](https://github.com/dreamrec/LivePilot)** | 66 | **474 tools.** README's tool table lists an **Automation** category of 8 tools — *"16 curve types, 15 recipes (filter sweep, sidechain pump, dub throw...), spectral suggestions"* — plus Arrangement (21 tools incl. automation and native arrangement clips), Perception (offline LUFS/LRA and reference comparison), Generative (Euclidean/Bjorklund, Steve Reich phase shift, Philip Glass additive), and a 5264-device atlas. |
| [freekmurze/ableton-ai](https://github.com/freekmurze/ableton-ai) | 8 | 150+ commands, a dedicated `automation` tool module; README example: *"Draw a twelve minute filter sweep with 200 automation points."* Also the clearest published statement of exactly which things stay UI-only (LFO Map, Compressor sidechain source, Drift mod matrix). |
| [Florkin/claude-ableton-skills](https://github.com/Florkin/claude-ableton-skills) | 0 | 20 Claude Code skills specifically for **techno/house/electro in Live 12**, including an `automation-and-movement` skill and bar-by-bar arrangement maps. Driven by LivePilot. Brand new / unproven. |
| [Korben00/ableton-producer-skills](https://github.com/Korben00/ableton-producer-skills) | 14 | Producer skills incl. sound design; runs a Node process beside Live. |
| [mikecfisher/ableton-lom-skill](https://github.com/mikecfisher/ableton-lom-skill) | 18 | Live Object Model API reference skill for Live 12.3 Remote Script development — useful if we end up extending our own script. |

**Verdict on tooling.** Nothing found can click the LFO device's Map button or a sidechain-source
dropdown; that limit is real and universal. But **writing clip envelopes and arrangement automation is a
solved problem in at least three projects**, which removes the round-2 hack of substituting a tremolo for
a 22 dB swell. `dreamrec/LivePilot` is the most capable on paper (**[unverified]** — README claims only,
not installed or tested) and `freekmurze/ableton-ai` is the most legible. **[agent inference]** The
cheapest real fix, though, is to add three or four commands to *our own* remote script (it is our code;
`clip.automation_envelope(parameter)` plus `insert_step` is the whole job), rather than swapping MCPs
mid-project. glincker's 12 skills are prompt-level workflow wrappers with no techno depth — nothing in
them addresses this problem, and no newer pack with genuine hypnotic-techno sound-design depth was found.

### 2.6 Non-stock plugins — buy/no-buy

Honest answer: **no evidence found to justify a purchase.** Perplexity q6 came back explicitly unable to
cite any interview in which Donato Dozzy, Rødhåd, Oscar Mulero, Shifted, Efdemin, Vril or Kangding Ray
names a specific plugin; the only artist with substantive gear commentary in the results is Rod Modell
(Deepchord), who repeatedly says the opposite — that software is for processing, mixing and sequencing,
and that he had not generated a synth sound on a record in software (Vice / XLR8R / Quietus interviews,
**[unverified]**, not re-fetched). The named suspects (u-he Diva/Zebra, Serum, Soundtoys EchoBoy and
Crystallizer, Valhalla VintageVerb/Delay/Shimmer, FabFilter, TAL, Audio Damage) are real scene norms but
that is folk knowledge, not a citation. The one paid item with a *documented* fit is **Surreal Machines
Dub Machines** (USD 39, Ableton's own store, re-fetched) for tape/BBD-style delay character. Given that
Live's Echo already has Wobble, Noise, Repitch and a modulation LFO on delay time, **recommend no purchase
until a stock round has been judged on its own.**

---

## 3. Round-3 build brief

Common to all three candidates. Everything below is a device parameter or a MIDI note unless marked ⚠️.

- **Track**: new MIDI track, kick and bass untouched from round 1.
- **Level**: aim the top bus at **−12.6 dB relative to the kick stem's RMS** — matching the reference's
  3.4 % energy share — not the 20–25 dB of round 2, which was under-level for a layer that then poked out
  spectrally. `[measured, endel analysis]`
- **Band-limit before anything else**: EQ Eight HP at **150 Hz** (48 dB) and LP at **2.0 kHz**. Target
  ~45 % of the layer's energy in 150–500 Hz and ~48 % in 500 Hz–2 kHz, **under 0.5 % above 2 kHz**.
  `[measured]` This is the single change most likely to fix "too loud".
- **The decorrelation rule**: any two modulators that shape the same layer must run at **free-running Hz
  rates a few percent apart**, never on the same synced division. Reference targets: filter cycle
  **7.66 s = 0.1305 Hz**, amplitude cycle **8.00 s = 0.1250 Hz** — a 4.4 % offset that realigns only every
  ~180 s. Add a third source at **0.042 Hz (24 s = 12 bars)** and a fourth at **0.031 Hz (32 s = 16 bars)**
  to reproduce the measured 8-, 12- and 16-bar secondary arcs. `[measured periods; free-running
  implementation is agent inference]`
- **Delay**: Echo, **dotted quarter (3/8, 749 ms)**, feedback high enough to survive two bars, feedback
  path HP ~200 Hz / LP ~5 kHz. `[measured lag; filter figures sourced, techno-pattern-book §7]`
- Verify every write by reading `get_device_parameters` back. Nobody in this loop can hear.

### Candidate A — **Resonant percussion, the Consumed lane** (ranked 1)

The only candidate with a direct, sourced link to how the actual artist made the actual sound.

- **Instrument**: **DS Tom** (installed), or Operator ping if DS Tom's parameter surface proves thin.
  Rationale: Hawtin's *Consumed* top layer was a tom/conga through a resonant filter (SOS). `[sourced]`
- **Chain**: DS Tom → **Auto Filter** (Band-pass, Resonance ~70 %, Freq ≈ 600 Hz) → **Resonators**
  (tuned to C/E/G, Decay long, Dry/Wet ~35 %) → EQ Eight (HP 150 / LP 2 k) → **Echo** → Utility.
- **Modulation, all scriptable**: Auto Filter LFO **Wander**, Free mode **0.1305 Hz**, Amt ~35 %,
  **Spin 12 %** so L and R drift apart; Auto Filter envelope-follower amount low, running alongside.
  Echo Modulation LFO free at **0.081 Hz**, **Mod Delay ~8 %** (delay time wobbles — this is the
  "everything cross-modulating" move), Mod Filter ~20 %, Phase 140°. Echo Character **Wobble ~10 %**.
- **MIDI**: one or two notes, ~6–10 hits per 4 bars on an off-grid subdivision (a 5-of-16 or 7-of-16
  polymeter so it does not read as a loop), velocities 30–55 varied bar to bar. Round 2's candidate C
  already established this pattern shape works mechanically.
- **Over 4/8/16 bars**: the Wander LFO never repeats; the Echo mod at 0.081 Hz beats against it at a
  ~12.3 s period; the 16-bar arc comes from a slow Auto Pan-Tremolo (Amount ~25 %, free 0.031 Hz) at the
  end of the chain.
- ⚠️ **UI steps**: none, if we accept no sidechain. Optional Auto Filter sidechain-source dropdown.

### Candidate B — **Stacked, band-limited breathing pad, the Attack ambient-techno structure** (ranked 2)

Closest to the reference's actual measured content (one sustained mid-register layer), but the same
instrument class Daniel already rejected twice — so it must be built structurally differently.

- **Instrument**: **Wavetable** or **Poli**, **four oscillator voices spread −1 / 0 / +1 / +2 octaves** at
  descending levels, mapped from Attack's −INF / −11 / −8 / −12 dB. Amp env **Attack 5 s, Decay 1.5 s,
  Sustain ~−3 dB, Release 1 s**; a duplicate layer with a **15 s attack** underneath. `[sourced, Attack]`
- **Chain**: instrument → Auto Filter (LP 24 dB, ~720 Hz) → EQ Eight (**HP 280 Hz** per Attack, then LP
  2 kHz per our measurement) → **Roar** (Drive low, used purely as a modulation host) → Echo → Utility.
- **Modulation**: Auto Filter LFO Sine, Free **0.1305 Hz**, Amt sized so the cutoff travels **1.65 octaves,
  ~1000 Hz → 3150 Hz** `[measured]` — but note the LP at 2 kHz clips the top of that sweep; sweep
  **700 → 2000 Hz** instead and let the EQ define the ceiling `[agent inference]`. Auto Pan-Tremolo in
  Tremolo mode, Free **0.1250 Hz**, Amount sized for a **22 dB swell** `[measured]`. Roar's matrix:
  **LFO 2 → Drive** and **Noise (Simplex, very low rate) → Tone**, tiny amounts — the Attack tutorial's
  "0.045" lesson: subtlety is the point. ⚠️ Roar matrix routing is a UI click; amounts may or may not be
  scriptable **[to verify]**.
- **Pitch**: C3, E3, C4, **D4 loudest**, C5, D5 — the measured added-9th voicing, no third in the low
  octaves. `[measured]`
- **Over 4/8/16 bars**: 7.66 s filter against 8.00 s amplitude gives the 4-bar breath plus a slow beat;
  Roar's Simplex noise supplies non-repeating grain; a 32 s Shifter or Spectral Resonator Mod Rate change
  is the 16-bar arc.

### Candidate C — **Corpus/Collision ping into a dub delay, the filter-ping lane** (ranked 3)

Highest risk, most different from anything tried, and the least sourced — but it is the class of sound
"a producer working a synthesizer with really hypnotic sounds" most often means.

- **Instrument**: **Operator**, single sine, Amp env A 0 / D ~80 ms / S 0 / R short — an impulse, not a
  note. Or **Collision** with a Mallet excitator and a Membrane resonator. `[unverified technique; the
  filter-ping principle is sourced only from hardware demos]`
- **Chain**: Operator → **Corpus** (Resonance type **Tube** or **Plate**, tuned to C, Decay long, Material
  mid, Dry/Wet 60 %) → Auto Filter (BP, high Resonance) → EQ Eight (HP 150 / LP 2 k) → **Spectral
  Resonator** (Mode **Wander**, Mod Rate very low, Pch. Mod ~0.3 st, Dry/Wet 20 %) → Echo → Utility.
- **Modulation**: Corpus's own LFO on transposition at a free low rate; Auto Filter LFO **S&H** with
  **Quantization = Steps**, free ~0.09 Hz, so the ping's pitch/colour steps to new values irregularly;
  Spectral Resonator Mod Rate as a third, unrelated period.
- **MIDI**: extremely sparse — 3–5 impulses per 4 bars, low velocity, plus a **Velocity MIDI device with
  Random raised** for per-hit variation (exactly the trick the Attack *Spastik* tutorial uses on its 909
  hat) `[sourced]`, and optionally **Note Echo** for hardware-style repeats.
- **Over 4/8/16 bars**: the S&H steps guarantee non-repetition; the 8-bar arc is Corpus Decay under a slow
  LFO; the 16-bar arc is Echo feedback drifting.

**Scriptability summary.** Every parameter above is settable via `set_device_parameter`; every device is
loadable via `load_instrument_or_effect`; all MIDI is writable via `add_notes_to_clip`. The only ⚠️ UI
clicks are: Roar's matrix routing (B), any sidechain-source dropdown, and — if we want the measured 22 dB
swell as a real long-form gesture rather than a periodic tremolo — writing an automation lane, which our
script cannot do at all. **Recommend adding automation-point support to our own remote script before
round 3 starts; it is a small change and it removes the one thing that forced round 2 to fake a gesture.**

---

## 4. Honest assessment

An agent driving stock Ableton can plausibly get **closer** than rounds 1 and 2, because the two failures
so far were not subtle taste failures — they were structural, and this round names both: a single synced
LFO where the reference has at least four decorrelated periods, and a layer sitting above 2 kHz where the
reference has 0.07 % of its energy. Those are fixable by parameter values, and the parameters are all
scriptable. What an agent still cannot do is the part that actually distinguishes a producer: **hear the
result and iterate on it.** Every round so far has been open-loop — the agent writes numbers, exports,
and waits for Daniel's ear, which is a one-bit feedback channel with a multi-hour latency. Three
candidates times one verdict per round is not enough resolution to converge on "sophisticated." My honest
read is that round 3 has a real chance of producing something Daniel calls *acceptable* and a low chance
of producing something he calls *on point*, and that the deciding variable is not the recipe but the
feedback loop. If round 3 lands short, the right move is **not** a round 4 of the same shape: it is to
commission a producer for sound design only — one afternoon of someone building three or four top-layer
patches against this measured spec — and keep the agent for what it demonstrably does well, which is
the kick, the bass, the arithmetic, and the endless patient assembly around a patch it did not have to
invent.

---

## Not found

- **No stock-Ableton hypnotic/minimal-techno top-layer tutorial exists.** Confirmed again this round
  (the same negative as `plastikman-endel-sound-2026-09-05.md` §Q3). The closest is Attack's *Crafting
  Ambient Techno Pads*, which is a FabFilter Twin 3 patch with one stock Auto Filter step at the end.
- **No Ableton-specific filter-ping tutorial.** All filter-ping sources found are hardware (Octatrack,
  Erica Synths). The Ableton mapping in §2.2 is Perplexity's inference, **[unverified]**.
- **No teardown of Endel "Deeper Focus" itself**, and none for Donato Dozzy, Oscar Mulero, Rødhåd,
  Peter Van Hoesen or Function specifically. Searched; nothing citable.
- **No plugin-level gear citation** for any of the named hypnotic-techno producers (§2.6).
- **help.ableton.com "Updated Packs in Live 12"** could not be re-fetched (Cloudflare interstitial), so
  the factory-pack list in §2.2 rests on Perplexity alone. The *installed* list is first-hand and reliable.
- **Whether Roar's Modulation Matrix cells are exposed as named device parameters** — needs a live
  `get_device_parameters` call on a loaded Roar, which was not done because another agent was exporting
  audio from Live during this research.
- **Whether the Live 12 LFO device's Multimap really has exactly 8 slots** — Perplexity says 8 across
  several sources; the fetched manual text does not restate the number.
