# Evaluation — where the venture stands after two research sessions (2026-09-01)

Scope: the Claude business-case session (Rev 1–3, the "Endel Question" artifact + `docs/original-handoff.md`)
and Kimi's research (PR #1, `RESEARCH-SUMMARY.md`, everything under `research/`). Written after auditing
Kimi's headline numbers against the raw files and running two fresh probes (Google Trends 2019–2026;
Perplexity on Aimi's pivot, Moongate's acquisition, and solo-app precedents).

## 1. Audit of Kimi's numbers

| Claim | Verdict | What the raw actually says |
|---|---|---|
| "focus music" +142%, "adhd music" +538% 2019→2025, "verified via DataForSEO" | **Wrong provenance, right direction.** | The DataForSEO raw holds only 12 months (Aug 2025→Jul 2026). No 2019 data exists in the repo. Independently re-verified 2026-09-01 via Google Trends (US, web, yearly mean of the index; `research/need-research/google-trends-us-2019-2026.json`): focus music 22.8→53.8 (**+136%**), adhd music 3.4→20.9 (**+515%**); 2026 YTD higher still (76.0 / 37.1). Brand demand grew too: "endel" 1.8→7.9, "brain.fm" 0.9→2.7. |
| doomscrolling 33.1K, body doubling 33.1K, endel alternative 20 | Supported | Exact. Identical 33.1K is Google's volume bucketing, not a copy error. "deep work music 90/mo" was never queried. |
| Repetitiveness 4.5% / 4.2%; billing 21.7% | Defensible, not reproducible | Independent regex gives 3.7% / 4.0% and 23.2%. No classifier script exists for the complaint taxonomy (the jobs taxonomy has one and reproduces to the decimal). |
| Jobs-to-be-done table | Supported | Recomputed from `jobs-per-review.csv` and `classify.py`; exact. Best-evidenced work in the repo. |
| Endel ~$500K/mo | Partial | Sensor Tower estimate, US-only, one unnamed month. |
| Brain.fm ~$2.5M/yr | **Unsupported** | Raw says "$2–7M/yr rough range"; $2.5M appears nowhere in the sources. |
| Moongate $200K/mo, "zero brand searches" | Partial | Rating count exact (59,197). Revenue is an uncaptured Adapty/Sensor Tower/screensdesign estimate (other aggregators say $480K/mo). Brand volume is `null`, not 0. |
| lofi.co shut down at 26K MAU | **Unsupported** | Not in any raw file; the raw describes lofi.co in the present tense with live pricing. |
| Flow benefit fades 53% after 30 days | Partial | Real quote from PMC12024392, but the study is Mozart/classical, generalized to "background music." |
| RevenueCat 37% "insufficient usage" = "the boredom bucket" | Supported / speculation | 37.02% is real. "Boredom" is Perplexity's guess; the source names no such reason. |

Pattern: the review mining and the keyword pulls are solid. Every failure is a number that entered via
Perplexity prose or an uncaptured web page and lost its hedge on the way into a summary table.

## 2. Thesis probes

**"The demand is real and growing."** Holds, now with correct provenance (Google Trends, not DataForSEO).
Nuance the summary misses: the incumbents' own brand demand grew 3–7× over the same period. This is a
growing category whose leaders are growing with it, not a stagnant one waiting for a challenger.

**"The graveyard is the opportunity — they died of neglect and billing, not lack of demand."** Weakest
inference in the corpus. Aimi is the closest analog to this exact product (generative electronic music
from artist stems, listener sliders, $24M, Founders Fund) and it reached ~110K Android downloads in three
years before its iOS app disappeared. No founder statement blames demand (Perplexity: framed as a
strategic move to tools; the player was "just really an MVP"), but nothing shows demand either — users
rated it 4.5★ and still did not come. Mubert's users praised its endless variety and it still died as a
consumer app. The two survivors are the two that are *not* variety-first: Brain.fm (science + ritual +
ADHD ownership) and Endel (brand + label deals + paid social). The "empty slot" is indistinguishable, on
current evidence, from a slot nobody wants.

**"Honest billing alone is a weapon."** It prevents 1★ reviews; it does not acquire anyone. myNoise, Portal,
Pzizz, Dark Noise and Not Boring Vibes all bill honestly and all sit at modest scale. Endel's scam-review
wall coexists with 33.6K US ratings, rising brand searches, and 20 searches/month for "endel alternative."
The anger is not measurably leaking users to alternatives.

**"Position on the problem: doomscrolling 33K searches."** Informational intent ($1.29 CPC, low competition
= nobody monetizes it). People searching "doomscrolling" want to stop scrolling; the adopted cures are
blockers and dumbphones, and Kimi's own research says focus music is "rarely named as the fix." "Body
doubling" is Focusmate-shaped intent, not music. This is a content/SEO angle at best. It also quietly
changes the product: the Claude session researched a Brain.fm-shaped flow-audio product with a pinned
sonic character and a user dial; the Kimi session researched a generative-techno + interactive-visual
fidget app for "TikTok brain." Those are two products. The visual layer has zero articulated demand in
1,027 reviews and no verified request thread; it is a hypothesis, not a finding.

**"Repetitiveness is a retention problem, not an acquisition hook."** Both sessions agree and the reviews
support it. Consequence Kimi's summary does not draw: the venture's headline differentiator (variety)
therefore cannot be the reason anyone downloads it. What acquires is a felt effect in the first session
and, for Brain.fm, the peer-reviewed claim behind it. Neither is something a solo generative engine
brings by default.

**"~$700 gets you to a real yes/no."** No. The $50 ear test answers "can AI make techno Daniel would work
to" — necessary, not sufficient. The $300–500 Apple Search Ads probe needs a shipped app, so "yes/no"
actually means "build first"; and the Claude session's adversarial review already showed that
small-budget paid probes at this N are noise. The real yes/no is acquisition, and both sessions left it
open: Kimi says "content-first (YouTube, Shorts, Spotify-as-artist, SEO)" with no evidence; the Claude
Rev 1 lanes called YouTube/Spotify/Reddit dead ends, also thinly evidenced. Perplexity could not find a
single solo or 1–3 person focus/generative-audio app that reached 1,000 paying subscribers organically
between 2022 and 2026. The one thing that verifiably acquires in this category is Moongate's playbook:
Meta ads at 1,000+ creatives, a web-to-app quiz funnel, aggressive paywalls, a professional growth
operator. That is the opposite of the product Daniel wants to build, and it is the only working
precedent found.

**"1,000 subscribers ≈ $84K/yr."** Arithmetic is fine. Holding 1,000 subscribers steady means replacing
churned ones every year; at the category's 2–3% download-to-paid rate that is on the order of 20K+
downloads a year, every year. Without a channel, the number is not a business plan.

## 3. Verdict

- **As a business:** the evidence has moved *against* since the last session. Demand is real and
  growing, but everything specific to this venture's differentiation — variety, a visual layer, honest
  billing — is shown not to acquire; the closest analog with $24M got no traction; and no acquisition
  channel a solo founder can use has been evidenced. Brain.fm's ~$2–7M ten-year ceiling remains the
  upside case, and Brain.fm holds it with an asset (a peer-reviewed effect) that cannot be copied.
- **As a capped personal product:** still defensible, if the goal is "a tool I want, that a few thousand
  people like me will pay for," with acquisition accepted as an unsolved problem rather than a gate that
  is assumed to pass.
- **The ear test ($50) is worth running** because it is cheap and answers Daniel's own question. It is
  not "the gate for everything else." The business gate is a demand/acquisition test that nobody has
  designed yet; do not spend the $300–500 ASA probe.

## 4. Decisions Daniel has to make before more research is useful

1. Which product: flow-audio with a pinned character (Claude session) or generative techno + interactive
   visual for TikTok-brain (Kimi session). The research does not decide this; the visual layer has no
   demand evidence and doubles build scope.
2. Whether "a few thousand subscribers with no proven channel" is an acceptable ceiling.
3. Whether his Brain.fm trial (started ~Aug 31) produced flow sessions — that is primary evidence for
   whether the incumbent already solves his need.
