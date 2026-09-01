# Flow Audio Research

Research for a possible side venture: an iOS app that plays generative "Endel-type" techno focus music with far more variety than existing apps. Endel and Brain.fm occupy this market today; the working hypothesis was that users leave these apps because the sound gets repetitive, and that a generative engine with real variety could win them. This repo collects the research done to test that hypothesis before any build spend.

## Repo layout

- `research/review-mining/` — corpus of 1,027 App Store reviews (Endel and Brain.fm, US and DE storefronts) fetched via the iTunes RSS customer-reviews API, plus `complaint-taxonomy.md` ranking every complaint category.
- `research/moat-decline/` — Perplexity sonar-pro research on the moat question (`q1`–`q3`) and on silent churn (`churn-q1`–`churn-q4`), with raw JSON responses and write-ups.
- `research/landscape-factcheck/` — fact-check research on Brain.fm funding, headcount, and revenue (questions `q1`–`q5`, answers `r1`–`r5`).
- `docs/original-handoff.md` — the original handoff document from a prior agent (partially unverified; the verified findings are summarized below).

## Verified findings

**Keyword demand (verified via DataForSEO live API).** Demand for focus music is real and growing: "focus music" grew roughly +142% in US search volume from 2019 to 2025, and "adhd music" grew +538% over the same period. "Study music" alone gets 27,100 US searches per month. But "deep work music" is tiny — about 90 searches per month. Note: the original handoff cites slightly different growth figures (+136% / +567%); treat the exact percentages as approximate, the direction as solid.

**Review mining (verified — computed directly from 1,027 pulled reviews).** The top Endel complaints are billing/refund anger (21.7% of all reviews) and app bugs (21.7%). Repetitiveness ranks only 8th, mentioned in 4.5% of all reviews. Brain.fm shows the same pattern (repetitiveness 4.2%). Brain.fm is praised for variety; Endel ships 15+ soundscapes but users perceive one sound — "variety in count, not character." Full taxonomy with quotes: `research/review-mining/complaint-taxonomy.md`.

**Moat research (third-party/AI research, sources cited in the JSONs).** Variety alone is not a moat. Calm and Headspace had huge catalogs, celebrity voices, and published studies — and still declined. Variety-seekers are already served for free: Lofi Girl has 15.8M YouTube subscribers, Spotify's Deep Focus playlist has roughly 5M followers, and Mubert streams generative music free.

**Silent-churn research (mixed: one verified industry stat, one peer-reviewed study, plus AI research).** The #1 cancellation reason for subscription apps is "insufficient usage" at 37% (RevenueCat State of Subscription Apps 2025). A peer-reviewed study found the flow-enhancing benefit of background music attenuates 53% after 30 days of familiarization. Bored users rotate to free alternatives, not to another paid app. Conclusion: repetitiveness is a retention problem, not an acquisition hook.

**Patents (verified — public patent records).** Relevant patents exist: US 7,674,224 (Brain.fm, amplitude modulation), US 11,275,350 and US 12,248,289 (Endel, sensor-driven and continuous composition). A freedom-to-operate review would be needed before any build.

**Landscape (third-party estimates unless noted).** Brain.fm raised only about 225–325K USD total (estimate), with roughly 13–14 staff — a small, capital-disciplined company, not a venture rocket. Endel's Universal Music Group deal (May 2023) produced a handful of albums and then went quiet.

## Open questions

- **The ear test:** can AI actually generate techno worth 2 hours of listening? Nothing in this repo answers that — it is the first gate before any build spend.
- **Brain.fm first-hand trial:** use the category leader for real before building against it.
- **Acquisition strategy (if the gates pass):** content-first, since ADHD-marketed products cannot be performance-marketed — YouTube long-form, TikTok/Shorts, Spotify-as-artist, SEO.
- **The "scatterbrain / anti-doomscrolling / fidget" angle:** positioning as a fidget/anti-doomscroll tool rather than a productivity app; unexplored.

---

*Personal research repo. Not affiliated with Endel, Brain.fm, or any company mentioned. Raw API responses are included as fetched; some JSON files contain third-party API response metadata.*
