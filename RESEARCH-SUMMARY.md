# Flow-Audio Venture — Consolidated Research Summary

Status: 2026-09-01. This document consolidates every research thread so far.
Raw data and per-thread reports live in `research/` — this file is the readable index + verdicts.

## 1. The idea

An iOS app that plays generative "Endel-type techno" focus music with much more variety
than existing apps — plus (hypothesis) a calm, interactive visual layer for the eyes and
fingers, aimed at the "TikTok brain" / anti-doomscrolling crowd.

## 2. Demand signals (verified via DataForSEO)

- "focus music" grew ~+142% (2019→2025), "adhd music" ~+538%. "study music": 27,100 US searches/mo.
- "deep work music" is tiny (90/mo) — the concept grew, not the keyword.
- Problem vocabulary dwarfs product vocabulary: "doomscrolling" 33.1K/mo US + 14.8K/mo DE,
  "body doubling" 33.1K/mo US, vs. "endel alternative" 20/mo.
  → Position on the problem, never as an "Endel alternative."
- Germany mirrors US at ~5–15% of volume, same shape. "doomscrolling" is DE's strongest term.

Raw: `research/need-research/keywords-*.json`

## 3. Why people actually use these apps (1,027 reviews mined)

Top jobs-to-be-done (share of all reviews):

| Job | Endel (n=600) | Brain.fm (n=427) |
|---|---|---|
| Focus/deep work (primary) | 6.8% (mentioned in 23.8%) | 22.0% (mentioned in 58.3%) |
| ADHD/neurodivergent | 11.7% | 16.4% |
| Sleep | 11.8% | 13.6% |
| Relax/unwind | 6.7% | 6.6% |

- The #1 driver is a noisy head (ADHD, anxiety), not generic productivity.
- Why they pay when free playlists exist: lyrics/hooks grab attention; picking music is itself a distraction.
- The effect must be felt immediately or users cancel within a week.
- Top wishes in both apps: more variety, and mix-your-own control.
  Verbatim (5★ Brain.fm): "my brain craves novelty above all else."
- Nobody explicitly asks for a visual component — but users already run ASMR/"satisfying"
  videos in the corner while studying (latent, unarticulated demand).

Raw: `research/need-mining/jobs-and-wishes-taxonomy.md`

## 4. The anti-doomscrolling angle (Daniel's hypothesis — supported)

- "TikTok destroyed my attention span" threads across 8+ subreddits, 2021–2026, still growing.
- Scale: r/nosurf ~300K members, #DopamineDetox ~82–88M TikTok views.
- What people adopt today: app blockers (Opal ~7.5M downloads) and dumbphones —
  focus music is rarely named as the fix. That is the positioning wedge, unproven.
- Fidget/ASMR mechanism: ADHD users self-report tactile/visual stimulation channels
  restlessness into focus ("the tactile pressure focuses me"). No controlled studies verified.

Raw: `research/need-research/q3.json`, `q4.json`, `summary.md`

## 5. Why users leave (silent churn)

- Repetitiveness complaints are rare in reviews (Endel 4.5%, Brain.fm 4.2% — rank 8).
- But the #1 subscription cancel reason is "insufficient usage" (37%, RevenueCat 2025) — the boredom bucket.
- Peer-reviewed: background-music flow benefit fades 53% after 30 days of familiarization.
- Bored users rotate to FREE (YouTube/Spotify), not to another paid app.
- Verdict: repetitiveness is a RETENTION problem, not an acquisition hook.
  "Never gets stale" is a keeping-superpower; the winning message is a proven outcome.

Raw: `research/review-mining/complaint-taxonomy.md`, `research/moat-decline/churn-q*.json`

## 6. Competitive landscape (30 players, 12 deep cards)

The field is a graveyard — most who tried this are gone or leaving:

| Player | Status | Key numbers |
|---|---|---|
| Endel | Active, angry users | 4.64★ / 33.6K US ratings; ~$22.5M raised; est. ~$500K rev/mo; billing-rage reviews |
| Brain.fm | Active, small | 4.54★ / 5.4K US ratings; team ~14; est. ~$2.5M/yr; loved by ADHD users, hated billing |
| Aimi | DEAD (consumer) | $24M raised incl. Founders Fund; consumer app delisted, pivoted B2B |
| Mubert | Abandoned app | No iOS update since Dec 2023; pivoted B2B/Web3 |
| Focus@Will | Abandoned → relaunched | Old app dead since 2022; "focus.music" relaunch Apr 2026 has 4 ratings |
| Loóna | Abandoned | 4.56★ / 26.7K ratings; team laid off 2023; users beg for content |
| Mesmerize | Active | 4.73★ / 56.6K US ratings; ~2/3 of recent reviews are 1★ billing-scam complaints |
| Portal | Active, stale | 4.78★ / 10.2K ratings; bootstrapped 4-person team; price-revolt in reviews |
| myNoise | Solo founder | 4.73★; one-time $19.99; the trust benchmark ("no AI, no data sale") |
| Noisli | Fossil | iOS untouched since 2017; still ~$80K/yr for a 2-person team |
| Calm / Headspace | Adjacent giants | Static music tabs, no generative audio, declining downloads |
| Moongate (discovery) | Paid-UA machine | 59K ratings, est. ~$200K/mo with ZERO brand searches |
| TeraMuse (discovery) | Closest concept rival | Music adapts to typing rhythm; desktop-only, not generative |
| lofi.co (discovery) | SHUT DOWN | Died at ~26K MAU — beautiful free web focus apps don't survive |

The empty slot: **generative techno + reactive interactive visuals on iOS.** Nobody occupies it.
The graveyard pattern: they died of neglect, billing dark patterns, or B2B pivots — not lack of demand.

Raw: `research/competitor-sweep/*/card.md`

## 7. Moat analysis

- Variety alone is NOT a moat: Calm/Headspace had catalog + celebrities + studies and still declined.
- AI-generated music is not copyrightable in the US — the moat can never be the raw tracks.
- Patents exist (US 7,674,224 Brain.fm; US 11,275,350 + US 12,248,289 Endel).
  Freedom-to-operate review (~3–10K USD) needed only if other gates pass.
- Realistic solo-founder moats: measurable focus outcome, narrow audience (ADHD/TikTok-brain),
  a small real study, workflow integration, honest billing as a trust brand.

Raw: `research/moat-decline/q1..q3.json`

## 8. Economics sketch

- One-person business frame: 1,000 subscribers ≈ ~84K USD/yr.
- Total initial capital ~700 USD (Apple dev account, ear test, small App Store ads probe).
- Apple 15–30% cut: a non-issue for validation (15% Small Business Program).
- Mobile-first iOS from day one (Daniel's call; ASA measurement needs a live app anyway).
- Acquisition: content-first (YouTube long-form, Shorts, Spotify-as-artist, SEO) —
  content is a byproduct of making the audio. One exception: a 300–500 USD Apple Search Ads
  probe at launch as a measuring instrument only.

## 9. Open gates (in order)

1. **Ear test** (~50 USD, one afternoon): can AI generate techno worth 2 hours of real work?
   Approved models for commercial use: Stable Audio, Lyria, ACE-Step. MusicGen/Udio disqualified.
2. **Daniel's Brain.fm trial** (started ~2026-08-31): first-hand flow session = primary evidence.
3. Visual-layer deep dive: is the fidget/ASMR screen a feature, a gimmick, or the product?
4. Patent FTO review — only if 1–3 pass.

## 10. Research index

- `research/review-mining/` — 1,027-review corpus + complaint taxonomy
- `research/need-mining/` — jobs-to-be-done + feature-wishes taxonomy
- `research/need-research/` — doomscroll/fidget trends + keyword volumes
- `research/moat-decline/` — moat probes + silent-churn probes
- `research/landscape-factcheck/` — Brain.fm/Endel funding & traction fact-checks
- `research/competitor-sweep/` — 12 competitor cards + discovery sweep
- `docs/original-handoff.md` — the prior agent's handoff (partially unverified)
