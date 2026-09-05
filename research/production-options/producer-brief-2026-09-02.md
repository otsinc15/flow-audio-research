# Producer brief — hypnotic techno stem library for a focus-music app

Date: 2026-09-02. Status: draft for Daniel's review before any outreach. Nothing has been sent.

Why this exists: six ear-test rounds (`../ear-test/generation-log-2026-09-02.md`) showed that
sound quality is solved by the engines (Lyria, ACE-Step, sample packs) but taste, balance and
arrangement are not. Every clip Daniel rejected was rejected for "too paddy", "too lively",
"generic", "not hypnotic" — decisions a producer makes with ears, not a knob. So we buy a
producer's taste once, as loopable stems, and let our engine do the endless recombination.

---

## 1. One-paragraph pitch (what the producer reads first)

We are building a focus-music app in the lane of Endel's *Deeper Focus*: hypnotic, minimal,
dub-tinged techno that runs for hours without drops, vocals, builds or breakdowns — music you
work to, not music you listen to. The app assembles the music live from a library of loopable
stems, so we are not commissioning tracks. We are commissioning **building blocks in one key and
one tempo**, produced by someone who lives in this sound, under a clean buyout so they can be
embedded in software. We pay a fixed fee, no royalties, and we start with a small paid sample so
neither side commits blind.

## 2. The sound, in the words we use internally

- **Hypnotic, monotone, Berlin.** A locked groove that repeats for minutes with only slow
  movement. Plastikman *Consumed*, Basic Channel / Maurizio, Deepchord, Donato Dozzy, the
  quieter end of Ostgut. Endel *Deeper Focus* is the commercial reference.
- **The bass is the star.** Deep, wide, fat. A sub that you feel plus a body you can hear on
  earbuds. Two rejected rounds sounded "computer-generated", "not part of a library" — we want
  the opposite: analogue-feeling, saturated, alive.
- **Almost no pads.** Three rounds in a row were rejected for sustained washy chords. If there
  is a chord element it is a **short, dry stab** through a tempo-synced delay, not a wash.
- **No melody, no lead, no vocal, no risers, no drops.** Nothing that asks for attention.
- **Dark up top.** Both references keep almost nothing above 2 kHz. Hats are quiet, filtered,
  behind the kick.
- **Movement without events.** Filter and delay feedback drift slowly; nothing "happens".

## 3. Technical spec (hard requirements)

| Item | Requirement | Why |
|---|---|---|
| Tempo | **118 BPM**, one tempo per pack (a second pack at 122 later) | Engine matches tempo exactly, no time-stretching |
| Key | **A minor**, all pitched material | Engine matches key exactly, no transposition |
| Format | WAV, 24-bit, 48 kHz, stereo (sub and kick may be mono) | Lossless into the engine; we convert down |
| Loop length | 16 bars per stem (32 bars for slow-moving textures), **sample-accurate loop points**, no tails crossing the loop boundary | Engine loops and crossfades on bar boundaries |
| One element per stem | kick / sub / bass / hats+perc / stab / texture, never premixed | Engine layers them; premixed stems cannot be recombined |
| Level | Peaks at or below **−6 dBFS**, no limiter, no master bus compression | We mix and master; baked-in loudness cannot be undone |
| Low end | Mono below 120 Hz; no sidechain ducking baked in (deliver a ducked *and* an unducked bass if you use it) | Layer combinations change which kick plays |
| Naming | `<role>_<variant>_118_Am.wav`, e.g. `bass_03_118_Am.wav` | Engine parses tempo and key from the filename |
| Sources | Your own synthesis, hardware, or CC0 samples only. **No Splice, Loopcloud or other licensed loop libraries**, no uncleared samples, no AI-generated audio | Those licences forbid redistributing loops inside a product |

## 4. Deliverables per pack (roughly 25 stems)

| Role | Count | Notes |
|---|---|---|
| Kick | 4 | Dry analogue-style, varying weight; one with a longer sub tail |
| Sub | 3 | Mono sine/triangle lines, root-fifth movement at most |
| Bass | 5 | The showcase. Saturated, moving, filtered; at least two that work *without* a sub |
| Hats & percussion | 4 | Filtered, quiet, off-grid swing welcome; one shaker/noise-based |
| Stab / chord | 4 | Short and dry, plus the same stab with the dub delay printed |
| Texture | 3 | Room, tape hiss, vinyl crackle, slow filtered noise; 32 bars |
| Dub throws | 2 | One-bar delay/reverb throws to sprinkle every 16–32 bars |
| **Reference mix** | 1 | A 3-minute mix of the stems, exactly as you would play them. This is the taste we are buying and our ear test uses it first |

Two packs planned: **Pack A "hypnotic minimal"** (this brief) and **Pack B "dub"** (same spec,
more delay, chords allowed to breathe a little; brief follows if Pack A passes).

## 5. Process and money

1. **Paid sample, before anything else.** Kick + bass + hats, 16 bars each, plus a 60-second
   mix. **€100–150**, 5-day turnaround, delivered under the same licence terms as the full pack.
   We run it through our engine and Daniel's ear test. Three producers get this sample brief
   in parallel; at most two continue.
2. **Full Pack A.** **€600–1,200** depending on the producer, 2–3 weeks. Half on start, half on
   acceptance. One revision round on stems that fail the technical spec; taste is not revised,
   that is what the sample round is for.
3. **Pack B** on the same terms if A passes.

Estimated spend to reach a shippable first library: €1,500–3,000 across the sample round and
two packs from the best producer.

## 6. Licence terms (the part that makes this usable in an app)

Keep it short and plain; a lawyer can dress it up before signature.

- **Exclusive, perpetual, worldwide buyout** of the delivered stems and the reference mix:
  we own the recordings and may edit, loop, layer, re-process, and distribute them **embedded
  in software, apps, streams and downloads**, without limit on users, plays or territories.
- **No royalties, no revenue share, no PRO registration** of the stems by the producer.
  The one-time fee is the entire consideration.
- **Warranty of originality**: the producer created the material, used no third-party licensed
  loops or uncleared samples, and used no generative-AI audio.
- **Credit**: optional and at the producer's choice (many prefer anonymity for library work).
- **The producer keeps** the right to say they worked with us and to reuse their own
  *techniques* and presets; they may not resell or re-release the delivered stems.

## 7. Where to find them

- **SoundBetter**: search "dub techno", "minimal techno", "hypnotic"; use a custom job, not a
  Tracks-marketplace licence (those cap streams and forbid this use).
- **Bandcamp**: producers selling dub/minimal techno stem or sample packs directly; treat the
  public pack as the portfolio and negotiate the stem library privately.
- **Direct**: artists on labels in this sound (Giegling-adjacent, Delsin, Echocord, Ostgut's
  quieter roster). A modest-following artist is the target; the big names will not do library work.
- Fiverr is the fallback for the sample round only; expect thinner sound design.

## 8. Outreach message (paste-ready, Daniel sends it)

> Subject: Paid sample — hypnotic dub techno stems for a focus-music app
>
> Hi <name>, I found your <release/pack> and it sits exactly in the sound I am building a
> product around: a focus-music app (think Endel's Deeper Focus, but proper Berlin-leaning
> hypnotic techno) that assembles music live from loopable stems. I am looking for a producer
> to build a small stem library — 118 BPM, A minor, about 25 loop-clean stems plus a
> 3-minute reference mix — under a clean one-time buyout (no royalties, embedded in the app).
>
> Before any big commitment I would like to pay you €<100–150> for a short sample: kick,
> bass and hats, 16 bars each, plus a 60-second mix, within about five days. If it passes our
> listening test the full pack is €<600–1,200>. Full brief attached. Interested?
>
> Daniel

## 9. What happens when stems arrive

Drop the folder into the engine (`./synth/run-packs.sh <PACK_DIR> <PACK_NAME>`) — it selects,
layers and crossfades without processing — and put the audition set in the Listening Room. The
reference mix goes first, then the engine's combinations. The pass criterion is the same as
every round so far: Daniel's ear.
