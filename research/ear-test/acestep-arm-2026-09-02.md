# ACE-Step 1.5 arm — 2026-09-02

Date: 2026-09-02. Machine: Mac mini (`cyruss-mac-mini-1`), Apple Silicon, macOS 26.3.1, 24 GB
unified memory shared with production jobs.

**The agent that wrote this file cannot hear.** Every characterisation below is either an `ffmpeg`
(EBU R128) or `librosa` 0.11.0 measurement, a fact read out of the model's own logs, or arithmetic
on those numbers. The listening notes at the end are labelled as inference from measurement, not as
listening. The ear test is still the real test.

No reference audio, loop, stem or sample was uploaded to or referenced by the model at any point.
Text prompts only.

---

## 1. What was run, and what was not

| | |
|---|---|
| **DiT model used** | `acestep-v15-turbo` — the **2B** model, 8 steps, `shift=3.0` |
| **DiT model NOT used** | `acestep-v15-xl-turbo` (4B) — ruled out, see below |
| **LM used** | `acestep-5Hz-lm-0.6B`, MLX backend |
| **DiT backend** | native MLX (`use_mlx_dit=True`), confirmed in log: `[MLX-DiT] Native MLX DiT decoder initialized successfully` |
| **Device** | `mps` |

### Why XL was not used

The brief preferred `acestep-v15-xl-turbo`. It was rejected on two independent grounds, both
measured before anything was downloaded:

1. **Size.** The Hugging Face repo `ACE-Step/acestep-v15-xl-turbo` is **19.95 GB** of weights
   (4 × ~4.99 GB shards). The project's own README puts XL at "≥12 GB VRAM (with offload +
   quantization) or ≥20 GB (without offload)". The mini had **~2.3 GB free and ~7.9 GB inactive**
   (i.e. ~9 GB genuinely reclaimable) out of 24 GB, with production jobs holding the rest, against
   a task budget of ~12 GB resident.
2. **Time.** Sustained Hugging Face throughput from the mini measured **6–7.7 MB/s**. XL alone
   would have been ~50 minutes of download *on top of* the 10 GB main repo.

ACE-Step's own hardware detector independently agreed with the downgrade. On startup it logged:

> `macOS MPS detected (17.8 GB unified memory, tier=tier6a). Applying Apple Silicon optimizations:
> no compile, no quantization, mlx backend, no CPU offload.`

`tier6a` is the 16–20 GB tier, for which the README recommends "2B sft or XL turbo — *XL requires
CPU offload below 20 GB*". The 2B turbo sits comfortably inside that tier; XL did not.

`acestep-v15-sft` (the 2B, 50-step, higher-quality variant) was **also not run**. It is a separate
~5 GB download and 50 steps instead of 8, i.e. roughly 6× the inference cost per clip. There was no
time budget left for it after the download problems below. **This is the single most obvious
follow-up.**

---

## 2. Install recipe — the exact commands that worked

No Homebrew, no sudo, user-space only. `uv` (0.12.1), `python3.11`, and `ffmpeg` were already
present on the mini at `~/.local/bin` and `/opt/homebrew/bin`.

```bash
ssh cyrus@cyruss-mac-mini-1.tail976740.ts.net
export PATH=$HOME/.local/bin:/opt/homebrew/bin:$PATH

mkdir -p ~/flow-acestep && cd ~/flow-acestep
git clone --depth 1 https://github.com/ACE-Step/ACE-Step-1.5.git
cd ACE-Step-1.5

# Dependency install. Resolves to CPython 3.12.13, torch 2.10.0, mlx, mlx-lm.
# ~6 min. Do NOT use the start_*_macos.sh launchers - they are interactive
# (update prompt, uv-install prompt) and will hang a non-interactive session.
uv sync

# Model weights. See the xet note below - this flag is load-bearing.
export HF_HUB_DISABLE_XET=1
export HF_HUB_DISABLE_PROGRESS_BARS=1

# Main repo: 2B turbo DiT + VAE + Qwen3-Embedding-0.6B text encoder (+ the 1.7B LM,
# excluded here). 10.09 GB unfiltered; ~6.4 GB with the exclude.
uvx --from "huggingface_hub[cli]" hf download ACE-Step/Ace-Step1.5 \
    --local-dir ./checkpoints --exclude "acestep-5Hz-lm-1.7B/*"

# The smaller LM, chosen over the bundled 1.7B to save ~2.4 GB resident.
uvx --from "huggingface_hub[cli]" hf download ACE-Step/acestep-5Hz-lm-0.6B \
    --local-dir ./checkpoints/acestep-5Hz-lm-0.6B
```

Final on-disk footprint of `checkpoints/`: **12.2 GB** (includes ~4.9 GB of abandoned `.incomplete`
files from the restarts described below; a clean run is ~7.8 GB).

### Three traps worth writing down

1. **`hf-xet` downloads bytes and writes nothing.** The default transfer backend pulled 655 MB over
   the wire while every `.incomplete` file on disk stayed at **0 bytes** and `~/.cache/huggingface/xet`
   stayed at 1.8 MB. Five minutes of apparent progress produced no file. `HF_HUB_DISABLE_XET=1`
   fixed it immediately and permanently. **Diagnose this by `stat`-ing the `.incomplete` files, not
   by watching the progress bar** — the bar looks healthy either way.
2. **`hf download` does not resume across restarts.** Each invocation creates a *new* `.incomplete`
   file with a different trailing token and starts from zero. Killing and restarting the download to
   change flags cost 2.5 GB of completed transfer. Decide the flags before you start.
3. **Unauthenticated Hugging Face requests get rate-limited.** Two parallel downloads shared ~7 MB/s
   and then dropped to ~1.1 MB/s combined. Killing one restored the other to 7.3 MB/s. There is no
   `HF_TOKEN` on the mini or the laptop; setting one would likely remove the ceiling.

### One code patch was required

`check_main_model_exists()` treats `acestep-5Hz-lm-1.7B` as a mandatory component of the main model.
Running the 0.6B LM instead therefore re-triggers a 3.7 GB download on every launch. The renderer
drops it from the required list before importing the handlers:

```python
from acestep import model_downloader as _md
_md.MAIN_MODEL_COMPONENTS[:] = [
    c for c in _md.MAIN_MODEL_COMPONENTS if c != "acestep-5Hz-lm-1.7B"
]
```

---

## 3. Prompt fields used

Driven through the Python API (`acestep.inference.generate_music`), not the Gradio UI or the
wizard CLI. The wizard is interactive and unsuitable for batch work.

| Field | Value | Why |
|---|---|---|
| `task_type` | `text2music` | |
| `caption` | the style prompt, verbatim | genre words and BPM number substituted per clip |
| `lyrics` | `"[Instrumental]"` | the value the source treats as the instrumental sentinel |
| `instrumental` | `True` | |
| `bpm` | 118 or 122 | |
| `duration` | `90.0` | **not honoured — see defects** |
| `seed` | 1001 or 2002 | |
| `inference_steps` | `8` | turbo default |
| `shift` | `3.0` | the README's recommended value for turbo models |
| `infer_method` | `"ode"` | |
| `thinking` | `True` | LM chain-of-thought planning of the audio semantic codes |
| `lm_negative_prompt` | see below | **the only negative/exclude field the API exposes** |
| `use_cot_metas` | `False` | otherwise the LM overwrites the requested BPM and duration |
| `use_cot_caption` | `False` | otherwise the LM rewrites the prompt |
| `use_cot_language` | `False` | irrelevant for instrumental |
| `GenerationConfig.audio_format` | `"wav"` | 48 kHz stereo 16-bit |
| `GenerationConfig.use_random_seed` | `False`, with explicit `seeds=[...]` | reproducibility |

**Negative prompt.** ACE-Step 1.5 has no per-stem or DiT-level exclusion field. The only one is
`lm_negative_prompt`, which steers the language model's planning stage. It was set to:

> `vocals, singing, voice, choir, melody, lead synth, solo, drop, build-up, breakdown, riser,
> white noise sweep, EDM, psytrance, trance`

The prompt text itself also carries the exclusions ("no melody, no lead, no vocals, no risers…"),
so the negation is expressed twice.

### The design of the eight

A clean 2×2×2 grid — one factor moves at a time:

| | seed 1001 | seed 2002 |
|---|---|---|
| dub techno, 118 | 01 | 05 |
| dub techno, 122 | 02 | 06 |
| minimal techno, 118 | 03 | 07 |
| minimal techno, 122 | 04 | 08 |

---

## 4. Time and memory

| | |
|---|---|
| Model load (cold, both handlers) | **45.8 s** first run, 35.8 s second |
| 30 s smoke render | **78.0 s** |
| 90 s renders | **51–100 s each** (first is slowest; 8 clips in **8.5 min** wall clock, load included) |
| Peak RSS of the render process | **14.44 GB** smoke / **14.83 GB** batch |
| Swaps attributed to the render process | **0** (`/usr/bin/time -l`) |

The peak RSS number needs a caveat: on macOS `ru_maxrss` counts memory-mapped file pages, and the
checkpoints are mmap'd safetensors, so 14.8 GB overstates the true anonymous footprint. The honest
signal is that the process itself recorded **zero swaps**. The machine as a whole was already under
pressure before this arm started (21 GB of 24 GB in use, 12.5 GB of swap in use) and that did not
measurably worsen. Nothing was killed.

After warm-up, generation runs at roughly **1.5–1.8× faster than real time** for 90 s of audio.
That is the one unambiguously good number in this document.

---

## 5. Per-clip measurements

All measured on the **trimmed** clips (the surviving musical stretch — see defects). Reproduced
with `research/ear-test/measure-clips.py`, `librosa==0.11.0`, `ffmpeg` EBU R128.

| clip | variant | seed | BPM asked | **BPM measured** | beat CV | LUFS | **LRA** | <60 Hz | 60–150 | **150–500** | sub-150 | onsets/min | centroid | usable s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | dub | 1001 | 118 | **117.5** | 0.012 | −17.1 | 1.0 | 47.6 % | 40.0 % | **5.3 %** | 87.6 % | 372 | 3951 Hz | 38.7 |
| 02 | dub | 1001 | 122 | **123.0** | 0.011 | −13.3 | 1.2 | 38.8 % | 46.8 % | **9.6 %** | 85.6 % | 488 | 3499 Hz | 44.9 |
| 03 | minimal | 1001 | 118 | **117.5** | 0.009 | −14.9 | 2.8 | 31.5 % | 52.2 % | **9.4 %** | 83.7 % | 396 | 2650 Hz | 47.0 |
| 04 | minimal | 1001 | 122 | **97.5** ⚠ | 0.033 | −15.8 | 0.5 | 24.6 % | 56.2 % | **9.0 %** | 80.8 % | 490 | 3722 Hz | 20.1 |
| 05 | dub | 2002 | 118 | **117.5** | 0.009 | −14.1 | 1.8 | 64.3 % | 28.4 % | **4.4 %** | 92.7 % | 472 | 4582 Hz | 30.9 |
| 06 | dub | 2002 | 122 | **123.0** | 0.016 | −16.0 | 0.6 | 39.5 % | 49.6 % | **4.4 %** | 89.1 % | 490 | 4818 Hz | 20.7 |
| 07 | minimal | 2002 | 118 | **117.5** | 0.009 | −14.5 | 1.7 | 44.9 % | 40.2 % | **10.6 %** | 85.1 % | 470 | 3957 Hz | 31.0 |
| 08 | minimal | 2002 | 122 | **123.0** | 0.035 | −14.7 | 0.3 | 54.6 % | 37.0 % | **3.5 %** | 91.5 % | 488 | 5365 Hz | 22.0 |
| | | | | | | | | | | | | | | |
| ref01 | "Late Autumn" | | | 114.8 | 0.027 | −20.4 | **4.1** | 27.6 % | 21.2 % | **46.5 %** | 48.8 % | 393 | 1797 Hz | — |
| ref02 | Endel Deeper Focus | | | 120.2 | 0.019 | −14.9 | **4.1** | 4.5 % | 76.7 % | **14.8 %** | 81.2 % | 346 | 788 Hz | — |
| **target** | | | | 114–122 | | −16…−14 | **≤ 4** | | | **15–45 %** | **40–55 %** | | | |

### What the table says

**Tempo control works, and works well.** Every clip asked for 118 came back at 117.5 BPM. Three of
the four asked for 122 came back at 123.0. Beat-interval CV of 0.009–0.016 on six of eight clips is
*steadier than either reference* (0.027 and 0.019). Clip 04 is the exception and it is a real miss:
97.5 BPM against 122 requested, with the loosest grid in the set (CV 0.033).

**Loudness flatness is achieved, arguably overachieved.** LRA of 0.3–2.8 LU against a target of
≤ 4 LU and references that both landed on 4.1. Nothing here has dynamics. Whether 0.3 LU reads as
"hypnotic" or as "dead" is exactly the question the ear test has to answer.

**The spectral balance is the failure.** This is the finding of the round. The 150–500 Hz band —
where a filtered chord, the body of a stab, and the warmth of a room live — measures **3.5 % to
10.6 %** across all eight clips, against a target of 15–45 % and a ref01 value of 46.5 %. Energy
below 150 Hz is **80.8 % to 92.7 %**, against a target of 40–55 %. Every single clip is outside the
target on both counts, in the same direction, with no overlap.

The prompt explicitly asked for "dark dubby chord stabs fed through dotted-eighth delay and long
spring reverb". In energy terms those stabs are close to absent. What the measurements describe is
a sub, a kick, and a thin bright top, with a hole where the middle of the record should be. The high
spectral centroids (2650–5365 Hz against ref01's 1797 Hz and ref02's 788 Hz) point the same way: the
centroid is being dragged up by low-energy high-frequency content sitting above an empty midrange.

---

## 6. Defects

**1. The model will not fill the requested duration.** This is the serious one. Every render was
asked for 90 seconds. Every render produced music for a while and then went silent for the
remainder:

| clip | music span | silent frames in the 90 s render |
|---|---|---|
| 01 | 0.0 – 40.2 s | 47.3 % |
| 02 | 0.0 – 46.4 s | 30.6 % |
| 03 | 0.0 – 48.5 s | 38.2 % |
| 04 | 0.0 – 21.6 s | 50.5 % |
| 05 | 0.0 – 32.4 s | 54.5 % |
| 06 | 0.0 – 22.2 s | 75.3 % |
| 07 | 0.0 – 32.5 s | 55.0 % |
| 08 | **23.6 – 47.0 s** | 41.4 % |

Between **21.6 and 48.5 seconds** of actual music per 90-second request. Clip 08 does not even start
at zero — it opens with 23 seconds of silence. The 30 s smoke render showed the same shape (19 %
silent, a −49.9 dB tail).

The most likely cause is that `use_cot_metas=False` disables the LM's duration planning, so the
5 Hz language model emits a shorter token sequence than the 90 s canvas and the DiT fills the
remainder with the model's own `silence_latent`. **The obvious next experiment is to re-run with
`use_cot_metas=True`** and accept LM-chosen BPM, or to find the field that pins sequence length
without surrendering tempo control. Until that is resolved, this arm cannot produce a long-form
track at all, which is disqualifying for the actual product.

**2. Clips are delivered trimmed, not as rendered.** Because of defect 1, each delivered clip is the
longest contiguous musical stretch, minus a 1.5 s safety cut at the end to remove the fade. The
untrimmed 90 s originals are in the same directory as `NN.wav`.

**3. Tempo failure on clip 04.** 97.5 BPM measured against 122 requested, tempogram candidates split
across 246.1 / 161.5 / 97.5. One in eight.

**4. Fade-outs inside the musical region.** Clip 03's trimmed tail still sits 25.4 dB below its body,
so the fade begins before the silence does. The prompt asked for "no ending" and did not get it.

**5. Possible voice-band content on 03 and 04.** The harmonic-component energy share in the
300–3400 Hz formant band measures 0.239 and 0.255 on clips 03 and 04, against 0.02–0.09 on the other
six. This is a **flag to listen for, not a detection** — the probe cannot distinguish a vocal from a
filtered pad. Both are minimal-techno, seed 1001. Worth an explicit listen.

**6. No section changes, which is the one thing that went right.** The novelty probe found 1–3
one-second timbre outliers per clip and no sustained section structure. No intro, no build, no drop,
no breakdown were detected in any clip. The prompt's structural instructions were followed.

---

## 7. Honest notes

**I cannot hear these clips.** What follows is inference from the measurements above, and it is
worth exactly as much as inference from measurements is worth — which is to say it can be wrong in
the direction that matters most.

The measurements describe something that is **not a produced record**. A produced dub techno record
puts a large share of its energy in the 150–500 Hz region, because that is where the chord stabs,
the tape saturation and the room live; ref01, the track Daniel calls perfect, puts 46.5 % there.
These eight put 3.5–10.6 % there. The thing that has been generated has a convincing bottom end and
a convincing pulse and then a hole in the middle. My expectation is that it will read as **thin,
hollow, and unfinished** — kick and sub arriving reliably, with the record that should be sitting on
top of them mostly missing.

Against the synth rounds, the honest comparison is split. ACE-Step is **better at the grid** — 117.5
BPM on demand with a beat CV steadier than either reference is a real result, and 1.5× real-time
generation on a Mac mini with no GPU is a real result. But the synth rounds were built from actual
oscillators and actual samples, so their midrange exists by construction; this model's midrange has
to be *summoned by a sentence*, and the sentence did not summon it. I would expect these to sound
more like a plausible sketch of the right genre than the synth rounds did, and simultaneously less
like something you would ship, because a sketch that will not run past 48 seconds and goes silent
cannot become a product.

The strongest caveat on all of the above: this is the **2B turbo at 8 steps**, the cheapest
configuration in the family. `acestep-v15-sft` at 50 steps is the obvious next run and could move
the midrange finding substantially. Nothing here should be read as a verdict on ACE-Step 1.5 as a
whole — only on its fastest model at its fastest setting.

---

## 8. Where things are

| | |
|---|---|
| Install | mini: `~/flow-acestep/ACE-Step-1.5` (venv, checkpoints), `~/flow-acestep/render.py` |
| Renders (mini) | `~/flow-acestep/out-batch/`, `~/flow-acestep/out-smoke/` |
| Delivered clips | laptop: `~/Documents/AI Agent Outputs/Artifacts/flow-audio-candidates/round5-acestep/` |
| Player manifest | `…/round5-acestep/manifest.json` — 8 × m4a, **5.81 MB** total |
| Raw measurements | `…/round5-acestep/measurements.json`, `structure.json`, `spans.json`, `render-report.json` |

Audio is never committed to this repo.
