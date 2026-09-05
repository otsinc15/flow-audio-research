---
name: synth-study
description: Learn electronic sound design from a user-selected tutorial or reference, verify the audible and visible technique, reconstruct it in Ableton, and retain recipes with listening evidence. Use for systematic tutorial study and reference-led synth experiments.
---

# Synth study

Turn a specific passage into a reproducible experiment, not a generic synthesis summary.

## Study loop

1. Identify the exact video, timestamp, and musical layer the user likes. A bass demonstration can play over a previously built lead; distinguish them. Preserve any accepted baseline before changing the session.
2. Read the full timecoded captions to locate the build sequence and later explanation. Inspect the actual video around the relevant changes through browser playback and screenshots. Captions cannot establish knob values or the sound during music-only passages.
3. When authorized audio/video analysis is available, use the helper below on bounded public YouTube passages. Its observations are hypotheses: corroborate critical settings against frames and the instrument manual. Do not claim direct hearing from text or screenshots. A track name does not prove the instrument heard; an unseen FX tab does not prove effects are off.
4. Record a technique card: source URL/time range, intended audible effect, visible/spoken evidence, unknowns, source signal path, native Ableton adaptation, one testable change, and result. See [techniques.md](references/techniques.md) for initial cards and [live-control.md](references/live-control.md) for empirical Ableton pitfalls.
5. Reconstruct first, then adapt to the user's music. Match oscillator family, register, amplitude shape, filter shape, and processing order before adding random movement. Use existing stock instruments when they implement the mechanism. Exact recreation on another synth is not assumed.
6. Render a short dry version and processed version, then test in context. Hold MIDI/register/gain constant when testing timbre; hold the patch constant when testing rhythm. Match comparison loudness with fixed gain, inspect decoded true peak and mono compatibility, and preserve the original exports. Measurements establish differences and technical defects, not whether the music is good.
7. Keep user verdicts attached to the precise audio and patch snapshot. Status progression: observed → reconstructed → rendered → auditioned → user-kept/rejected. Only a user verdict makes a taste preference; lack of feedback is not acceptance. Keep rejected recipes searchable to avoid repeating them.

## Select lessons by the current failure

- Thin or generic source: oscillator harmonics/register, filtering, amp versus filter envelopes.
- Static phrase: velocity destinations, bounded continuous modulation, delayed repeats.
- Weak groove: note placement/gates and kick interaction before additional percussion.
- Crowded result: simplify one layer and assign distinct spectral/rhythmic roles.

Study one mechanism deeply enough to render it before expanding the viewing queue. Prefer a creator's supplied preset/project when legitimately available, then inspect and compare it; do not mistake downloading a library for learning it. Audit third-party skill recipes for ambiguous units, invented APIs, blanket style assumptions, and unsupported quality scores.

## Video analysis helper

`scripts/study-video.py` sends only a canonical public YouTube URL, a bounded time range, and the explicitly supplied prompt to Gemini. No local audio or project files are sent. It stores the request, response, text, and token usage in a new output directory. No automatic retries. Authentication uses `GEMINI_API_KEY`/`GOOGLE_API_KEY`, with the existing local `~/.claude/.env` credential as a fallback; credentials never enter artifacts.

```bash
python3 <skill-dir>/scripts/study-video.py \
  --url 'https://www.youtube.com/watch?v=p1-WmITJqBk' \
  --start 720 --end 870 --model gemini-3.1-pro-preview \
  --prompt-file /path/to/question.txt --output-dir /path/to/new-study
```

Use exact timestamps for knob transitions; reduce `--fps` only for broad, mostly static passages. Inspect usage because provider clipping/billing behavior can change. API reference: [Google video understanding](https://ai.google.dev/gemini-api/docs/generate-content/video-understanding).

This skill is a portable local workflow, not a trained audio model or a guarantee of production taste. Its repository copy is versioned; a copy installed in the personal skill directory does not automatically update or sync to another machine.
