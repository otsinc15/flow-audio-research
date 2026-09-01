> **Note:** Original handoff from a prior agent — partially unverified; verified findings live in README.md and research/.

# Handoff — Focus/Flow Audio Venture Evaluation (Daniel)

**Date:** 2026-09-01 · **Status:** research complete, no build started, no money spent
**Full business case (Rev 3):** https://claude.ai/code/artifact/ac34dc85-03af-4b99-8d3c-d4b64e3a00b0
**Memory record:** `~/.claude/projects/-Users-othersideinc-Code-otsinc15-cyrus-os/memory/endel-functional-audio-business-case.md`

This is NOT Cyrus OS work. No repo, no code, no branch. Nothing here touches the Cyrus OS
codebase and no session-learnings file applies.

---

## 1. What this is

Daniel is evaluating whether to build a focus/flow functional-music product — the market
Brain.fm and Endel occupy. He is not a programmer. He has ADD (takes modafinil, no
stimulants), used Endel for deep-monotone focus work, left after product changes, and wants
"consistent sonic character, never-identical detail, user holds the dial." The personal need
is real and is the origin of the idea; the research exists to test whether a business is real.

**Verdict reached:** no venture-scale entry. A narrow solo product is defensible — Brain.fm's
own ten-year ceiling is roughly $2–7M, so plan against that, not against a unicorn. Realistic
prize at 1k/5k/10k subscribers is roughly $84K/$420K/$840K net per year.

**Three gates stand between here and any build spend.** None has been run.

---

## 2. Ground rules Daniel has established (follow these)

- **Start every response with "Daniel, ..."** Default to 1–3 sentences. Completion messages
  open with a `**TLDR**` block of ≤3 lines, whole message ≤10 lines.
- **He caught real errors in this research and was right to.** He does not trust claims he
  cannot trace. Always separate *verified against a primary source* from *third-party
  estimate*, and say which is which unprompted.
- **App Store numbers are per-country storefront.** Daniel is on the **German** store;
  research agents default to US. Always name the storefront when citing a rating or price.
  This caused a trust rupture once — do not repeat it.
- Disagree with him when warranted, before implementing, not after.
- He is not watching in real time on long tasks. Do reversible work autonomously; stop only
  for spend, outbound public posts, and payment credentials.

**Corrections already made — do not re-derive or re-break:**
- Brain.fm **does** have a free trial (3-day, no card, in-app, on their own backend, length is
  a live A/B experiment). An earlier draft said it did not. Daniel proved it with a screenshot.
- Brain.fm has **both** $14.99/mo and $99.99/yr. Not annual-only.
- Endel **never removed** the 2D tune pad. Daniel's founding memory of this was refuted by
  review research; the pad shipped ~2024 and was gated behind premium in 2026. What was
  actually lost: the unlimited free tier, menu-bar controls, Mac-app quality.

---

## 3. Verified facts (primary sources, checked live 2026-08-31)

**App Store ratings** — iTunes lookup API:

| Storefront | Endel | Brain.fm |
|---|---|---|
| US | 4.64 (33,582) | 4.54 (5,397) |
| Germany | 4.46 (5,063) | 4.30 (427) |
| UK | 4.58 (3,555) | 4.40 (600) |

Endel is marginally ahead on every storefront. Reproduce with:
`curl -s "https://itunes.apple.com/lookup?id=1346247457&country=de"` (Endel id `1346247457`,
Brain.fm id `1110684238`).

**Pricing** — scraped from live App Store pages:
- Endel US: $119.99/yr list, $19.99/mo, lifetime $124.99, with discount offers at
  $79.99 / $59.99 / $34.99. Germany: €59.99/yr list with offers down to €29.99 / €23.99 /
  **€17.99** (the tier Daniel actually bought).
- Brain.fm: $14.99/mo + $99.99/yr (US), €14.99/€99.99 (DE), offers at $69.99 / $49.99.
- The steep discount ladder — Endel selling at 15–30% of list — is itself evidence of the
  churn-and-win-back squeeze.

**Google Ads CPC + volume (US)** — DataForSEO live, 2026-08-31:

| keyword | vol/mo | CPC |
|---|---|---|
| brown noise | 90,500 | $0.30 |
| music for focus | 18,100 | $0.42 |
| brain.fm (brand) | 14,800 | $0.59 |
| endel (brand) | 8,100 | $4.40 |
| adhd music | 5,400 | $3.18 |
| binaural beats for focus | 4,400 | $2.41 |
| brain.fm review | 1,300 | $6.14 |
| best focus music | 390 | $13.61 |
| flow state music | 210 | $7.84 |
| brain.fm alternative | 140 | $9.88 |
| focus music app | 70 | $9.27 |

**Read this carefully — it is the single most decision-relevant table in the handoff.** The
high-intent terms are expensive *and* nearly empty. The cheap volume is cheap because it is
free-YouTube-stream intent. "Flow state music" gets 210 searches/month, so *flow* is
positioning language, not search language — people type "focus music" and "brown noise."

Ten-market comparison (US/UK/CA/AU/DE/NL/IE/IN/PH/ZA) showed **geo arbitrage does not work**:
the expensive terms are not cheaper abroad, they are non-existent (10–50 searches/mo). The
genuinely cheap geos (India, Philippines, South Africa) are cheap because nobody bids there,
which is the same reason a $99/yr test there would tell us nothing. Legitimate move: bundle
UK+CA+AU with the US for the mid-intent lane (~35% more volume, same willingness to pay).
Side note: "endel" gets 8,100 searches/mo in **Germany**, equal to the US — they are
Berlin-based.

---

## 4. Why Brain.fm wins (the benchmark, not Endel)

Daniel reframed the target mid-research: the market is **focus/flow/ADHD, not sleep**, and the
benchmark is **Brain.fm, not Endel**. Sleep is shrinking (Sleep Cycle audited −21.5% YoY,
taken private, whole paid sleep-app market <$200M); focus is growing (US 2019→25 "focus music"
+136%, "deep work" +165%, "ADHD music" +567%).

Five causal factors behind Brain.fm's success:
1. Catalog + amplitude-modulation post-processing — a format that *enables* their peer-reviewed
   Communications Biology paper, the category's only non-replicable asset.
2. A ritual machine: activity → timer commitment → streaks. Users report the ritual matters as
   much as the audio.
3. 74% of power users have ADHD, a segment owned via published evidence since Jan 2025.
4. Account-level no-card trial on their own backend, decoupled from app-store payment rails.
5. ~15 people on ~$1M ever raised — capital discipline *forced* the D2C, high-margin, niche model.

Explicitly **rejected** as explanations: price (Endel's US annual is *higher* than Brain.fm's;
in the EU Endel is far *cheaper*, which rejects "Brain.fm wins on cheapness" even harder) and
paywall hardness (Endel's free tier is more generous).

Cautionary tale: Focus@Will marketed science without peer review, died, relaunched 2026 from zero.

**The wedge, such as it is:** 58% of Endel's critical reviews are billing/cancellation anger —
ADHD-marketed products built on ADHD-hostile mechanics. "Pin a consistent sonic character" is a
real but thin need (~6 independent voices found). Repetitiveness complaints are only 3% of
critical reviews and Brain.fm gets them at the same rate, so variety alone is not a wedge.

**Hard constraint:** ADHD products **cannot be performance-marketed.** Meta, Google, and TikTok
policy throttles the word "ADHD" even on landing pages; the Lumosity and Cerebral FTC actions
set the precedent. Public positioning must be flow-first; ADHD self-identification happens
inside the product only.

---

## 5. The gates

### Gate 1 — Ear test (~$50) · NOT STARTED, awaiting Daniel's go
Can AI-generated stems hit the quality bar over 60+ minute focus sessions? Batch-generate from
Stable Audio Open, ElevenLabs, Lyria, ACE-Step; blind-compare against Brain.fm as the bar.
Needs API keys — `ELEVENLABS_API_KEY` and `GEMINI_API_KEY` are already in `~/.claude/.env`;
others need Daniel walked through signup. Licensing already screened: Stable Audio Open (<$1M
rev), ACE-Step and YuE (Apache-2.0), ElevenLabs, Lyria are all commercially usable; MusicGen
(CC-BY-NC) and Udio (walled garden) are disqualified. Note AI output is not copyrightable
(USCO Part 2) — the moat cannot be the audio files themselves.

**Time-sensitive:** Daniel started a Brain.fm 3-day trial ~2026-08-31 (expired ~09-03 — check
whether he used it). His own first-hand flow-session experience is primary Gate-1 evidence.

### Gate 2 — Acquisition validation · **NEEDS TO BE RESEARCHED**
### Gate 3 — Paid-acquisition viability · **NEEDS TO BE RESEARCHED**

**These two are open research questions, not agreed plans.** Everything below is prior work
that failed review — carry it as evidence about what *not* to propose, never as a settled design.

What was proposed and why it fell over:

- **v1 — landing page + email capture + $500 split across Google/Meta/Reddit + A/B, pass at 8%
  email signup.** Killed by the CPC data above: at ~$9/click the high-intent terms buy ~45
  visitors for $400, which is statistically worthless, while the cheap terms buy the wrong
  intent entirely.
- **v2 — same, but $150 switcher-term conquesting + $250 Meta/Reddit + organic, across
  US/UK/CA/AU.** Sent to Perplexity (sonar-pro) for adversarial review and it took four
  substantive hits:
  1. **Email capture is the wrong metric.** A free "founding access" email measures curiosity.
     Swapping to a real $1 refundable pre-charge drops conversion 3–5×. Waitlist→paid runs
     ~13–20% median and decays hard if launch is >1 month out. The 8% gate overestimated
     demand by roughly 5×.
  2. **$500 across 3 channels × 2 variants guarantees noise** — dozens of visitors per arm.
     Practitioners want one channel, one variant, 200–300+ visitors before judging.
  3. **Bot/invalid traffic on Meta Audience Network and Reddit ads** can move a small-N result
     across the pass/fail line on its own.
  4. **The truest signal in this category is free** — transparent posts in productivity/ADHD
     communities plus a hand-run concierge beta produce qualified people you can interview.
- **v3 — sketched but never validated:** Phase A ($0, community validation + 10–20 interviews)
  then Phase B (~$800, real $99/yr price with a $1 refundable Stripe pre-charge, single
  channel = high-intent Google search, pass at ≥1% visitor→pre-charge and ≥20% of committers
  answering follow-ups). **This is a sketch. It has had no adversarial review and no
  practitioner validation. Do not execute it as written.**

**What the next agent actually needs to answer:**
- What is the highest-signal, lowest-cost way to test willingness to pay ~$99/yr for this
  product, given that high-intent search is ~140 searches/mo at ~$10 CPC and paid social is
  bot-contaminated at small N?
- Is a paid-acquisition channel viable *at all* here at a sane CAC, or is the honest answer
  organic-only (content, community, SEO, app-store surface)? Prior work found paid UA
  structurally underwater — CAC $69–172 against year-one net revenue per user of $25–38 — but
  that was benchmark math, not a measurement. It needs to be either confirmed or overturned
  with evidence.
- If organic-only: what does the first 12 months actually look like, and what is the realistic
  time-to-first-1,000-subscribers? Prior research found YouTube, Spotify, and Reddit ads to be
  verified dead ends, and found podcast sponsorship (~$500/slot), Apple featuring nominations,
  and brown-noise SEO to be the live lanes — verify this.
- What does a $1 pre-charge test actually cost to stand up, and does its signal justify it
  versus simply shipping a thin real product behind a paywall?

Budget conversation is unresolved. Daniel has asked twice whether the spend is justified, and
was right both times. Bring him a number with evidence behind it, not a range.

### Gate 3 (original) — Patent FTO ($3–10K) · only if 1 and 2 pass
Covers **both** portfolios: Endel's US 11,275,350 (sensor-driven) and US 12,248,289
(continuous composition), plus Brain.fm's US 7,674,224 (amplitude modulation — delta 0.25–1Hz
for sleep, 12–20Hz beta for focus). The design-around for Endel is a user-controlled,
no-sensor dial. Note Endel is a stems+rules content business, not neural generation — its web
player streams pre-rendered 24-hour files.

---

## 6. Tools and credentials available

All in `~/.claude/.env` (source it; values are quoted):
- `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` — live Google Ads CPC and volume.
  `POST https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live`,
  basic auth, body `[{"keywords":[...],"location_code":2840,"language_code":"en"}]`.
  Location codes used: US 2840, UK 2826, CA 2124, AU 2036, DE 2276, NL 2528, IE 2372,
  IN 2356, PH 2608, ZA 2710.
- `OPENROUTER_API_KEY` — Perplexity via OpenRouter, model `perplexity/sonar-pro`. **Never open
  perplexity.ai in a browser; Daniel rejected that.** Citations come back in
  `choices[0].message.annotations`. Set `max_tokens` generously (~6000).
- `ELEVENLABS_API_KEY`, `GEMINI_API_KEY` — Gate 1 audio generation.
- iTunes lookup/search API — no key needed, storefront-aware.

---

## 7. Immediate next step

Daniel's go/no-go is the blocker on Gate 1. Gates 2 and 3 (acquisition) need the research
above before any plan is put in front of him — do not bring him another landing-page proposal
without evidence that the channel can work.

Do not spend money, publish public posts, create accounts, or handle payment credentials
without his explicit per-action approval.
