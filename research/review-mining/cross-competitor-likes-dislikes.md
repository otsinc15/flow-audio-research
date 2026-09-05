# Cross-competitor likes & dislikes — iTunes customer reviews, US & DE storefronts

**Scope:** eight focus/functional-audio apps. Endel and Brain.fm were already mined
(`complaint-taxonomy.md`, `../need-mining/jobs-and-wishes-taxonomy.md`); this document adds
Focus@Will, myNoise, Noisli, Portal, Mubert and Dark Noise on the same method, and puts all
eight side by side.

**Corpus:** 3,047 reviews total — 2,020 newly pulled for the six added apps (1,755 US / 265 DE)
plus the 1,027 Endel + Brain.fm reviews already on disk. Every number below is counted from raw
iTunes RSS files in this directory. Nothing is estimated. Storefront is named on every figure.

**Method (same as the two prior docs):** each **negative (1–3★)** review gets exactly one
*primary* complaint from a priority-ordered keyword/regex rule list (EN + DE). "Share of ALL
reviews" is a separate *mention-level* count — a review can appear in several categories there,
so those shares deliberately overlap (a billing rant usually also mentions price). **Praise
codes** are mention-level over **positive (4–5★)** reviews only, so they also overlap.
Classifier: `classify-competitors.py`. Categories with fewer than 5 reviews are marked
**n<5, anecdotal**.

**Hand-check:** a stratified sample of ≥34 reviews per app (20 positive + 14–16 negative, random
seed fixed) was read in full by hand against the classifier's output, plus every single review
that the classifier could not categorise (230 on the first pass, 68 after two rule refinements).
The rules below are the post-hand-check version. Residual "Other (uncategorized)" now runs
7.8–13.5% of negatives per app. Known remaining imprecision is called out in the provenance block.

---

## 1. The one-paragraph answer

Across all 3,047 reviews, what paying users **credit when they stay** is overwhelmingly a
*functional* outcome plus a *feeling of being treated fairly* — not features. Of 1,860 positive
(4–5★) reviews, 599 (32.2%) credit an effect on focus/productivity, 363 (19.5%) credit design
and craft, 359 (19.3%) credit calming/anxiety relief and 349 (18.8%) credit sleep; by contrast
only 105 (5.6%) mention variety or catalogue size, 89 (4.8%) mention sound quality and 24 (1.3%)
mention adaptivity. 230 positive reviews (12.4%) use explicit longevity language ("for years",
"every day", "can't work without it") — and within that group the codes that appear at the
highest **lift** over their baseline are not the loud ones: variety/catalogue (10.9% of longevity
reviews vs 5.6% of all positives, 1.93×), one-time purchase / no subscription (7.4% vs 4.2%,
1.74×), science framing (4.8% vs 2.8%, 1.71×), sound quality (7.8% vs 4.8%, 1.64×) and honesty /
fair treatment (5.2% vs 3.2%, 1.62×). What **drives 1★** is money-trust and reliability, in that
order: of 635 one-star reviews across all eight apps, 114 (18.0%) are primarily billing /
unauthorised-charge / refund anger, 106 (16.7%) are app reliability, 50 (7.9%) price/value, 33
(5.2%) cancellation difficulty, 32 (5.0%) account/login/restore, 32 (5.0%) in-app upsell nagging
and 28 (4.4%) "paywall the moment I opened it / listed as free". Restricted to the six newly
mined apps (295 one-star reviews), the ranking flips: **reliability is #1 at 80 (27.1%)** and
billing is #4 at 23 (7.8%) — Endel is what makes billing the category leader overall.
Repetitiveness/lack of variety is a *minor* primary complaint everywhere (highest: Portal, 10 of
135 negatives, 2.5% of all its 612 reviews) but it is the single highest-lift praise code among
long-term users.

---

## 2. Cross-app table

Storefronts: US + DE combined per row; per-storefront splits are in the per-app sections.
Endel and Brain.fm complaint rankings are **taken from `complaint-taxonomy.md`** (its ruleset);
their praise codes were **recomputed here** on this document's praise rules so the "likes" column
is comparable across all eight. "Would miss most" = the praise code that co-occurs most often
with longevity language in that app's own positive reviews (count / longevity reviews).

| App | n (US / DE) | Date range | % negative (1–3★) | Top-3 dislikes (primary complaint, n of negatives) | Top-3 likes (mentions, % of positives) | Would miss most |
|---|---|---|---|---|---|---|
| **Endel** | 600 (300 / 300) | 2022-10-21 → 2026-08-30 | **62.8%** (377) | Billing/refund 122 · UX bugs 66 · Upsell nagging 43 | focus 30.9% · sleep 27.4% · calm 24.2% | Focus effect (17/32, 53.1%) |
| **Brain.fm** | 427 (300 / 127) | 2016-12-02 → 2026-08-28 | 34.9% (149) | UX bugs 35 · Price/value 27 · Billing 26 | focus **64.0%** · sleep 27.0% · calm 23.0% | Focus effect (23/41, 56.1%) |
| **Focus@Will** | 463 (429 / 34) | 2013-05-24 → 2026-07-02 | 47.1% (218) | **UX bugs/reliability 100** · Price/value 13 · Account/login 12 | focus **71.8%** · longevity 16.7% · price-value 11.0% | Focus effect (33/41, **80.5%**) |
| **myNoise** | 146 (127 / 19) | 2024-11-01 → 2026-08-28 | **25.3%** (37) | UX bugs 20 · Feature removed (legacy app) 3 · Price/paywall 2 (n<5, anecdotal) | sleep 27.5% · **control/customization 26.6%** · longevity 19.3% | Sleep (10/21, 47.6%); control/customization 2nd (8/21, 38.1%) |
| **Noisli** | 308 (253 / 55) | 2014-05-08 → 2026-05-23 | 33.8% (104) | UX bugs 27 · **Abandonware/no new-device support 20** · Missing platform 9 | sleep 24.0% · design 20.1% · calm 19.6% | Sleep (6/18, 33.3%) |
| **Portal** | 612 (500 / 112) | 2020-02-07 → 2026-08-23 | **22.1%** (135) | **Price/value 37** · UX bugs 17 · "It's free on YouTube" 13 | **design 32.5%** · calm 26.8% · focus 23.9% | Design/visuals (25/57, 43.9%) |
| **Mubert** | 164 (141 / 23) | 2017-10-20 → 2026-06-17 | 47.6% (78) | UX bugs 17 · Account/login 12 · Missing platform 8 | design 18.6% · **variety 12.8%** · focus 10.5% | n<5, anecdotal (3 longevity reviews) |
| **Dark Noise** | 327 (305 / 22) | 2019-08-27 → 2026-08-23 | 27.2% (89) | **Sound quality 11** · Price/value 10 · Paywall-on-launch 9 | **design 33.2%** · sleep 20.2% · control/customization 16.8% | Design (6/17, 35.3%); one-time-purchase & integration tied 2nd (5/17, 29.4%) |

Notes on the table:
- Portal is the **best-liked** app in the set (22.1% negative, mean 4.25★); Endel is the
  worst-liked (62.8% negative, mean 2.72★). Focus@Will and Mubert sit at ~47% negative.
- **Portal's "Missing platform" mention share (179 of 612 = 29.2%) is a measurement artefact**:
  Portal *is* a Mac/wallpaper product, so the words "Mac", "desktop", "wallpaper" appear
  constantly in praise. Only the 9 *primary* complaints are real platform complaints.
- Dark Noise DE is 22 reviews with 59.1% negative vs 24.9% negative on US — that DE cell is small
  and skewed by the 2023–2026 subscription switch; treat it as anecdotal.

---

## 3. Per-app findings

### 3.1 Focus@Will (US 429, 2013-05-24 → 2026-07-02, 45.7% neg, mean 3.36★ · DE 34, 2013-11-11 → 2025-08-23, 64.7% neg, mean 2.74★)

The corpus reaches back to 2013, so this is a full-lifecycle record of a subscription service
whose *content* is loved and whose *app* is not.

**Dislikes — 218 negative reviews**

| # | Category | Neg. | US | DE | Avg ★ | Share of ALL 463 |
|---|---|---:|---:|---:|---:|---:|
| 1 | **UX / app bugs / reliability** | **100** | 89 | 11 | 1.7 | **29.8%** |
| 2 | Other (uncategorized) | 17 | 14 | 3 | 1.5 | — |
| 3 | Price / value / paywall | 13 | 11 | 2 | 1.4 | 12.5% |
| 4 | Account / login / restore | 12 | 12 | 0 | 1.3 | 8.2% |
| 5 | Billing / unauthorized charges / refund | 12 | 12 | 0 | 1.2 | 2.6% |
| 6 | Cancellation difficulty | 10 | 10 | 0 | 1.3 | 3.9% |
| 7 | Feature removed / update regression | 7 | 7 | 0 | 1.9 | 2.2% |
| 8 | Abandonware / not updated for new devices | 7 | 6 | 1 | 1.9 | 1.9% |
| 9 | Repetitiveness / lack of variety | 6 | 3 | 3 | 2.5 | 3.9% |
| 10 | No offline / streaming-only | 5 | 5 | 0 | 2.2 | 2.6% |
| — | Sound quality 4 · Paywall-on-launch 4 · Misleading ads 3 · Battery/data 3 · "no effect" 3 · Subscription resented 3 · Missing platform 2 · Free alternatives 2 · Support 2 · AI distaste 1 · Loop artifacts 1 · Confusing 1 | all n<5, anecdotal | | | | |

Reliability is not just #1, it is 46% of all negative reviews and is mentioned in 29.8% of the
whole corpus. The recurring shape is "music works, app doesn't":

- [1★ US 2025-06-28] "Website great. App is garbage. No audio. … The standalone app may have worked at some point, but no longer plays audio at all. You had one job."
- [2★ US 2023-08-30] "The content in the app is great. Good sounds that do keep me focused, but the app is very glitchy, and ends up being more distracting than it should be."
- [3★ US 2022-11-09] "Works great when it works … Unfortunately, the iPad version crashes for no reason."
- [1★ DE 2018-05-25] "Die Musik ganz gut, die App ist Schrott in Anbetracht der Höhe des Abos."

Trial/cancellation friction is small in count but sharp in tone, and repeatedly names ADHD:
- [1★ US 2021-01-14] "You say you want to help the ADD/ADHD people, yet you require people to sign up for a subscription first and give them 7 days free. Considering my ADD, I would miss the time to cancel."
- [1★ US 2019-10-11] "RIP OFF $69 a year!!!!!!! … Super angry at misleading FREE."

**Likes — 245 positive reviews**

| Praise code | n | % of 245 pos | US | DE |
|---|---:|---:|---:|---:|
| **effect: focus / productivity** | **176** | **71.8%** | 170 | 6 |
| longevity / daily habit | 41 | 16.7% | 40 | 1 |
| price / value for money | 27 | 11.0% | 26 | 1 |
| effect: ADHD / neurodivergent | 22 | 9.0% | 22 | 0 |
| effect: anxiety / calm | 21 | 8.6% | 20 | 1 |
| design / UI / aesthetics | 18 | 7.3% | 17 | 1 |
| variety / catalog size | 17 | 6.9% | 16 | 1 |
| science framing | 16 | 6.5% | 16 | 0 |
| one-time purchase / lifetime | 11 | 4.5% | 11 | 0 |
| control / customization | 9 | 3.7% | 9 | 0 |
| integration | 7 | 2.9% | 7 | 0 |
| offline / privacy | 6 | 2.4% | 5 | 1 |
| sleep 4 · sound quality 4 · tinnitus 4 · honesty 2 | all n<5, anecdotal | | | |

Focus@Will has the most concentrated "like" profile in the set: nearly three quarters of its
positive reviews are a single functional claim.

- [5★ US 2017-08-03] "Focus at Will works! It helps my mind focus and stay active. I love it because my production has increased. I can't live without it." [longevity]
- [5★ US 2019-04-07] "GETS ME IN THE ZONE — I have been using F@W for over a year now and I use it all the time on all my devices."
- [4★ US 2017-11-01] "I measured my productivity with focus@will vs playing other music in background. F@W is hands down winner… the music is geared toward work and constantly changing so it does not become familiar."
- [5★ US 2017-02-25] "I have used this app every day since adding it to my device. Is now my 'go to' music source while working. Upgraded to lifetime membership because I use it so heavily."

**Wishes (keyword-triggered, NOT hand-checked):** 44 reviews (9.5% of 463) contain a wish
trigger. Clusters: bug fixes 7, more variety 7, offline/download 6, customization 4, integrations
2, desktop 2, pricing 2.

---

### 3.2 myNoise (US 127, 2024-11-01 → 2026-08-28, 26.8% neg, mean 4.13★ · DE 19, 2024-11-09 → 2026-08-24, 15.8% neg, mean 4.32★)

The RSS feed only reaches back to Nov 2024 — this is the **new, rewritten** myNoise app, not the
legacy one. That matters: a visible share of the corpus is legacy users judging the rewrite.

**Dislikes — 37 negative reviews** (small corpus; every category below except reliability is n<5)

| # | Category | Neg. | US | DE | Avg ★ | Share of ALL 146 |
|---|---|---:|---:|---:|---:|---:|
| 1 | UX / app bugs / reliability | 20 | 19 | 1 | 2.2 | 23.3% |
| 2 | Other (uncategorized) | 5 | 5 | 0 | 2.6 | — |
| 3 | Feature removed / update regression (legacy app) | 3 | 3 | 0 | 1.7 | 5.5% |
| — | Price/paywall 2 · Paywall-on-launch 2 · Billing 1 · Confusing 1 · Repetitiveness 1 · Misleading ads 1 · Subscription resented 1 | all n<5, anecdotal | | | | |

The reliability bucket is dominated by playback faults (a channel drops, a downloaded soundscape
plays silent) and by the loss of the old app's multi-layer generator:

- [2★ US 2025-11-08] "Left channel stops — I'd give it 5 stars but for some reason the left channel just stops working and only comes through the right."
- [1★ US 2026-02-25] "Latest Update Broke the App — Sounds aren't loading, weird download behavior. Why fix what isn't broken?"
- [1★ US 2024-11-19] "Favorite factory sounds are no longer available — Old app was better by far. They've cut or partitioned my favorite sounds!"
- [1★ US 2025-05-29] "Have to love the false advertising. Pictures of the product clearly claim 'no ads. No subscription' and the very first thing I'm greeted with when I open the app is to start a subscription."

**Likes — 109 positive reviews**

| Praise code | n | % of 109 pos | US | DE |
|---|---:|---:|---:|---:|
| effect: sleep | 30 | 27.5% | 29 | 1 |
| **control / customization** | **29** | **26.6%** | 26 | 3 |
| longevity / daily habit | 21 | 19.3% | 19 | 2 |
| effect: anxiety / calm | 19 | 17.4% | 11 | 8 |
| design / UI / aesthetics | 16 | 14.7% | 14 | 2 |
| effect: focus / productivity | 13 | 11.9% | 11 | 2 |
| effect: tinnitus / noise masking | 12 | 11.0% | 12 | 0 |
| one-time purchase / no subscription | 11 | 10.1% | 10 | 1 |
| variety / catalog size | 10 | 9.2% | 10 | 0 |
| price / value 8 · sound quality 8 · honesty 7 · integration 6 · science 5 | | | | |
| ADHD 2 · adaptivity 2 · offline 1 | all n<5, anecdotal | | | |

myNoise has by far the highest **control/customization** praise share of any app in the set
(26.6% vs a 7.9% all-app baseline) — the per-channel slider mixer is what people name.

- [5★ US 2025-11-08] "I have been using my noise for several years and love it! The background sounds help me concentrate at work, sleep and effectively mask tinnitus. I appreciate the easy interface whereby I can mix sounds and toggle up/down the sound tracks to get just the right combo."
- [5★ US 2026-05-27] "I use this app in every aspect of my life every day. I am always in awe of the variety of sounds, and the customization is incredible."
- [5★ US 2025-05-31] "Amazing variety and huge collection! — What really sells it is the highly customizable soundscapes."
- [5★ US 2025-08-05] "This is How Apps Should Be — This app is built by someone who clearly is in love with what he is making — the dedication and integrity is tangible."

**Wishes (not hand-checked):** 22 reviews (15.1% of 146). Dominant cluster: customization /
mix-your-own 9 (6.2% of all) — mostly "bring back the multi-generator layering".

---

### 3.3 Noisli (US 253, 2014-05-08 → 2026-05-23, 31.6% neg, mean 3.95★ · DE 55, 2014-05-11 → 2025-08-05, 43.6% neg, mean 3.47★)

**Dislikes — 104 negative reviews**

| # | Category | Neg. | US | DE | Avg ★ | Share of ALL 308 |
|---|---|---:|---:|---:|---:|---:|
| 1 | UX / app bugs / reliability | 27 | 25 | 2 | 2.1 | 16.2% |
| 2 | **Abandonware / not updated / no new-device support** | **20** | 12 | 8 | 2.2 | 8.1% |
| 3 | Other (uncategorized) | 13 | 11 | 2 | 2.6 | — |
| 4 | Missing platform / device support | 9 | 7 | 2 | 2.3 | 13.0% |
| 5 | Price / value / paywall | 6 | 3 | 3 | 2.7 | 5.2% |
| 6 | Repetitiveness / lack of variety | 5 | 3 | 2 | 2.4 | 4.5% |
| 7 | Missing feature: can't mix with other audio | 5 | 5 | 0 | 2.4 | 2.9% |
| 8 | **Audible loops / short loops / artifacts** | 5 | 5 | 0 | 2.8 | 2.9% |
| — | Sound quality 4 · Billing 3 · "no effect" 2 · Free alternatives 2 · Feature removed 1 · Misleading 1 · Account 1 | all n<5, anecdotal | | | | |

Noisli is the clearest case of a **paid one-off app dying of neglect**: 20 of 104 negatives are
explicitly "you stopped updating this". Its average negative rating is unusually mild (2.2–2.8★)
— these are disappointed fans, not angry ones. Two categories here do not exist in the
Endel/Brain.fm taxonomy and are real: abandonware, and **audible loop seams**.

- [2★ US 2020-11-08] "Crashes with iOS 14.2 — App hasn't been updated in three years and now it's crashing on launch 100% of the time… I don't expect it to be fixed."
- [3★ US 2019-09-26] "Is this app still supported? App works as intended, but is still not updated for the new screen format of the iPhone X and beyond. The last update was years ago."
- [3★ US 2016-10-07] "There is a noticeable gap in the brown noise loop. Please fix in the update."
- [2★ US 2016-07-22] "The loops are quite short. So you hear the loud female cackle in the coffee shop a lot. Stays with you."
- [2★ US 2017-05-12] "Will not allow other audio to play simultaneously — I was looking for white noise to play along with podcasts to block out noisy neighbors. When you open this app it turns off other audio."

**Likes — 204 positive reviews**

| Praise code | n | % of 204 pos | US | DE |
|---|---:|---:|---:|---:|
| effect: sleep | 49 | 24.0% | 45 | 4 |
| design / UI / aesthetics | 41 | 20.1% | 35 | 6 |
| effect: anxiety / calm | 40 | 19.6% | 32 | 8 |
| control / customization (the mixer) | 32 | 15.7% | 30 | 2 |
| longevity / daily habit | 18 | 8.8% | 17 | 1 |
| effect: focus / productivity | 18 | 8.8% | 17 | 1 |
| effect: tinnitus / noise masking | 14 | 6.9% | 13 | 1 |
| integration 11 · sound quality 9 · price/value 7 | | | | |
| variety 4 · offline 4 · honesty 3 · adaptivity 1 | all n<5, anecdotal | | | |

- [5★ US 2017-04-16] "I'm a software developer and need to concentrate. My coworkers are very loud and noisy. This app has been a life saver for me. I love how you can mix different ambient sounds with white noise and control how loud each one plays."
- [5★ US 2014-05-23] "Just wanted to say thanks for real sounds and adjustable volume for each sound… other apps sub in the pink noise for a fan or short loops."
- [4★ DE 2016-06-02] "The sounds are perfect. Good quality, appropriate variety and no discernible beginning/end of the loops."
- [5★ US 2015-10-15] "My favorite napping app — I take at least one timed [nap] every day and this app is the best white noise app that I have found. There's no nonsense of buying this or that."

**Wishes (not hand-checked):** 69 reviews (22.4% of 308) — the highest wish rate in the set.
Clusters: customization 12, more variety 10, desktop/web parity 6, UI 5, bug fixes 4.

---

### 3.4 Portal (US 500, 2021-12-13 → 2026-08-23, 20.0% neg, mean 4.33★ · DE 112, 2020-02-07 → 2026-07-24, 31.2% neg, mean 3.89★)

**The US pull is truncated:** the RSS feed caps at 10 pages and all 10 returned a full 50, so 500
is a ceiling, not the total. The US date range therefore only reaches back to 2021-12-13.

**Dislikes — 135 negative reviews**

| # | Category | Neg. | US | DE | Avg ★ | Share of ALL 612 |
|---|---|---:|---:|---:|---:|---:|
| 1 | **Price / value / paywall** | **37** | 26 | 11 | 2.2 | **19.4%** |
| 2 | UX / app bugs / reliability | 17 | 13 | 4 | 2.0 | 5.2% |
| 3 | **Free alternatives exist (YouTube / free apps)** | **13** | 12 | 1 | 2.0 | 2.6% |
| 4 | Other (uncategorized) | 13 | 8 | 5 | 1.8 | — |
| 5 | Repetitiveness / lack of variety | 10 | 4 | 6 | 2.3 | 2.5% |
| 6 | Missing platform / device support | 9 | 8 | 1 | 2.0 | 29.2%* |
| 7 | Billing / unauthorized charges | 5 | 5 | 0 | 1.4 | 1.3% |
| 8 | Abandonware / not updated | 5 | 4 | 1 | 2.0 | 2.0% |
| 9 | Account / login / restore | 5 | 3 | 2 | 1.8 | 2.8% |
| 10 | Paywall on launch / too little free content | 5 | 5 | 0 | 1.2 | 1.3% |
| — | Sound quality 4 · Feature removed 3 · Confusing 2 · Subscription resented 2 · can't-mix 1 · Upsell 1 · Battery 1 · Cancellation 1 · Misleading 1 | all n<5, anecdotal | | | | |

\* Artefact: "Mac", "desktop" and "wallpaper" are part of Portal's product description and appear
throughout its *praise*. Only the 9 primary complaints are genuine platform complaints.

Portal is the only app in the set where **price is the #1 primary complaint** and where a
distinct "you can get this free on YouTube" category is large enough to stand on its own. It is
also, simultaneously, the best-rated app here — the price anger comes from people who like it.

- [1★ US 2025-08-14] "I think some people might accidentally purchase this expensive $300 app. On top of that, if you subscribe, it costs $7–13 per month. But you can simply go to YouTube and search for 'nature sounds' [and] you'll find countless free videos."
- [3★ US 2023-03-27] "It's a beautiful and effective app — but a subscription for some noise I could find on YouTube?? … I'd happily pay a fair one time."
- [2★ US 2024-03-09] "The promise of a $30 one time lifetime fee as mentioned in reviews … seemed reasonable. Well at some point the one time fee jumped from a modest $30 to $250."
- [3★ US 2024-10-22] "I was surprised at the fairly limited selection of soundscapes from a limited number of geographic locations… Plus some of the soundscapes seem like they loop after just a few minutes."
- [2★ DE 2026-07-17] "It's nice but repeating itself after 1 or 2 minutes — I'm a premium member… I wish the sequences were longer."

**Likes — 477 positive reviews**

| Praise code | n | % of 477 pos | US | DE |
|---|---:|---:|---:|---:|
| **design / UI / aesthetics** | **155** | **32.5%** | 124 | 31 |
| effect: anxiety / calm | 128 | 26.8% | 99 | 29 |
| effect: focus / productivity | 114 | 23.9% | 97 | 17 |
| integration (Mac / HomeKit / AirPods) | 79 | 16.6% | 63 | 16 |
| effect: sleep | 78 | 16.4% | 73 | 5 |
| longevity / daily habit | 57 | 11.9% | 49 | 8 |
| sound quality / character | 48 | 10.1% | 42 | 6 |
| price / value for money | 34 | 7.1% | 31 | 3 |
| one-time purchase / lifetime | 31 | 6.5% | 23 | 8 |
| variety / catalog size | 20 | 4.2% | 17 | 3 |
| honesty / fair treatment | 20 | 4.2% | 19 | 1 |
| control / customization | 14 | 2.9% | 11 | 3 |
| ADHD 8 · adaptivity 7 · offline 5 | | | | |
| tinnitus 3 · science 2 | n<5, anecdotal | | | |

Portal is the only app whose #1 like is **craft, not effect** — and its sound-quality praise share
(10.1%) is double any other app's.

- [5★ US 2025-08-25] "Portal is an app that should be studied. It carefully and thoughtfully builds a captivating experience in the name of wellbeing."
- [5★ US 2025-02-16] "Crazy Effective for Focus! — I play this with my headphones on and it increases my productivity 100%… It's saved me hours of distracted time waste."
- [5★ DE 2020-05-08] "The soundscapes are amazing and have a stunning quality. If you listen to them with headphones, it seems like you are at another place."
- [4★ US 2026-06-21] "I love this app and have been using it for years. I don't think I've ever found any other app with comparable audio quality." [longevity]
- [4★ US 2022-05-28] "One of my favorite apps. I use it every day. I wish there was a greater variety of environments… This app is too expensive at $50/year." [likes and dislikes in one review]

**Wishes (not hand-checked):** 79 reviews (12.9% of 612). Clusters: more variety 13, desktop/web
12, customization 9, watch/casting integration 9, cheaper 6, timers 5.

---

### 3.5 Mubert (US 141, 2017-10-20 → 2026-06-17, 48.2% neg, mean 3.36★ · DE 23, 2018-08-31 → 2024-05-17, 43.5% neg, mean 3.48★)

The only pure generative-AI music app in the set, and the only one where "confusing / can't
figure out how to use it" is a real category.

**Dislikes — 78 negative reviews**

| # | Category | Neg. | US | DE | Avg ★ | Share of ALL 164 |
|---|---|---:|---:|---:|---:|---:|
| 1 | UX / app bugs / reliability | 17 | 13 | 4 | 2.3 | 18.9% |
| 2 | Account / login / restore | 12 | 11 | 1 | 1.8 | 11.0% |
| 3 | Other (uncategorized) | 10 | 10 | 0 | 1.8 | — |
| 4 | Missing platform / device support (iPad landscape) | 8 | 5 | 3 | 2.6 | 13.4% |
| 5 | **Confusing / hard to figure out** | 4 | 4 | 0 | 1.5 | 3.0% |
| 6 | Billing / unauthorized charges | 4 | 3 | 1 | 1.2 | 3.0% |
| — | Feature removed 3 · Repetitiveness 3 · No offline 2 · Price 2 · Upsell 2 · **AI distaste 2** · Cancellation 2 · Subscription resented 2 · Paywall-on-launch 2 · Free alternatives 1 · Misleading 1 · Battery 1 | all n<5, anecdotal | | | | |

Mubert's negatives are unusually *operational* — accounts that won't create, streams that stall,
an interface people cannot navigate — and its money complaints are small. "AI music is soulless"
exists but is tiny (2 primary, 6 mentions = 3.7% of all 164).

- [1★ US 2023-03-03] "Unapproachable, obtuse, and just plain stuck up. No tutorial or instructions."
- [1★ US 2018-08-25] "? — How do you even use this"
- [2★ US 2021-01-14] "Glitchy — I love the idea and when it works it works. Unfortunately, it doesn't work more often than it does. I liked it enough at first to pay for a subscription but after these experiences will not be renewing."
- [1★ US 2019-11-13] "Why would I want to listen to some randomly generated 'music' with no soul in it?"
- [3★ US 2020-07-29] "Why is there not a sleep timer… I've switched to a different app called Endel because this feature is missing."

**Likes — 86 positive reviews**

| Praise code | n | % of 86 pos | US | DE |
|---|---:|---:|---:|---:|
| design / UI / aesthetics | 16 | 18.6% | 12 | 4 |
| **variety / catalog size** | 11 | 12.8% | 10 | 1 |
| effect: focus / productivity | 9 | 10.5% | 9 | 0 |
| integration | 8 | 9.3% | 6 | 2 |
| effect: anxiety / calm | 7 | 8.1% | 5 | 2 |
| control / customization | 5 | 5.8% | 5 | 0 |
| sleep 4 · longevity 3 · honesty 2 · sound quality 2 · adaptivity 2 · offline 2 · price 1 · tinnitus 1 | all n<5, anecdotal | | | |

Mubert is the only app where **variety is a top-2 like** (12.8% vs a 5.6% all-app baseline) — the
endlessness is the product, and reviewers name it directly.

- [5★ US 2020-07-02] "I've used Pandora, Spotify and Apple Music but Mubert has very quickly become my go to music app when I want an endless evolving music stream. It's never boring."
- [5★ DE 2019-08-08] "Amazing concept… Music is playing continuously - smoothly - no songs. The hearer can set intensity and mood."
- [5★ US 2020-03-26] "At first, the entire concept of AI generated music seemed silly. But I stuck with Mubert… It's really cool to see the sounds change over time."
- [5★ US 2019-02-24] "Passes the Turing Hearing Test (if one existed) — Dynamic noises and never any sloppy transitions through the music."

**Wishes (not hand-checked):** 26 reviews (15.9% of 164). Clusters: visuals/UI 6, more variety 3,
customization 2, timers 2, bug fixes 2, offline 2.

---

### 3.6 Dark Noise (US 305, 2019-08-27 → 2026-08-23, 24.9% neg, mean 4.10★ · DE 22, 2019-09-05 → 2026-04-28, 59.1% neg, mean 2.95★)

An indie one-time-purchase app that switched to subscription. The corpus splits cleanly into
before and after.

**Dislikes — 89 negative reviews**

| # | Category | Neg. | US | DE | Avg ★ | Share of ALL 327 |
|---|---|---:|---:|---:|---:|---:|
| 1 | **Sound quality / unpleasant sounds** | 11 | 8 | 3 | 2.1 | 8.3% |
| 2 | Other (uncategorized) | 11 | 10 | 1 | 1.5 | — |
| 3 | Price / value / paywall | 10 | 8 | 2 | 1.6 | 11.0% |
| 4 | **Paywall on launch / "listed as free"** | 9 | 8 | 1 | **1.0** | 2.8% |
| 5 | UX / app bugs / reliability | 8 | 8 | 0 | 1.5 | 5.8% |
| 6 | Billing / unauthorized charges | 5 | 4 | 1 | 1.8 | 2.1% |
| 7 | Repetitiveness / lack of variety | 5 | 5 | 0 | 1.6 | 4.0% |
| — | Upsell 4 · **Subscription resented 4 (avg 1.0★)** · Audible loops 4 · can't-mix 4 · Missing platform 3 · "no effect" 3 · Account 2 · Free alternatives 2 · Support 1 · Cancellation 1 · Feature removed 1 · Misleading 1 | all n<5, anecdotal | | | | |

Two things are distinctive. First, **sound quality is the #1 primary complaint** — no other app
in the set has that; the specific fault is loop seams and artifacts in the recordings. Second,
the paywall-on-launch category carries a perfect 1.0★ average: the launch-time subscription wall
generates the purest anger in the whole eight-app corpus.

- [3★ US 2025-01-06] "Brown noise has audible 'jump' when it loops. I don't know how to explain it. It's very subtle but disruptive. Only brown is affected and that's the one I downloaded the app for."
- [2★ US 2024-02-19] "The sounds are not high quality, they have crackles and skip like scratched cd's."
- [1★ US 2026-06-30] "Not a free app — This app is listed as free when you filter in the App Store for free apps. It is not. Upon opening the app, you are immediately trapped in a 'choose your paid plan' step."
- [1★ DE 2026-04-28] "Dark Noise? Dark Patterns! Die App zwingt gleich beim Start zum Kauf von Abos - wer nicht zahlt, kann sie nicht nutzen."
- [1★ US 2026-05-22] "Bought this app back in 2020 only to realize that 99% of the noise is locked behind a paywall."
- [1★ US 2023-04-03] "Gone subscription. My favorite ambient noise app, it's a shame it went 'free' and now cost double the amount I originally paid."

**Likes — 238 positive reviews**

| Praise code | n | % of 238 pos | US | DE |
|---|---:|---:|---:|---:|
| **design / UI / aesthetics** | **79** | **33.2%** | 76 | 3 |
| effect: sleep | 48 | 20.2% | 47 | 1 |
| control / customization (mixing) | 40 | 16.8% | 40 | 0 |
| integration (widgets / Shortcuts / Watch) | 30 | 12.6% | 30 | 0 |
| effect: anxiety / calm | 26 | 10.9% | 23 | 3 |
| effect: focus / productivity | 22 | 9.2% | 21 | 1 |
| longevity / daily habit | 17 | 7.1% | 16 | 1 |
| variety / catalog size | 17 | 7.1% | 16 | 1 |
| price / value for money | 14 | 5.9% | 13 | 1 |
| one-time purchase / no subscription | 12 | 5.0% | 12 | 0 |
| honesty / fair treatment | 11 | 4.6% | 11 | 0 |
| tinnitus 9 · sound quality 8 | | | | |
| adaptivity 3 · offline 2 · science 2 · ADHD 1 | all n<5, anecdotal | | | |

- [5★ US 2019-08-27] "So good it should be built in — Dark Noise is so easy to use and such a good citizen of iOS that it makes you feel like the iPhone should *come with* a Noise app, and this should be it."
- [5★ US 2024-08-15] "A rare gem — I've used this app for years… It's easy to use. Its interface is simple, but elegant. It has a lot of high quality sound options." [longevity + one-time purchase]
- [5★ US 2022-11-02] "Best single purchase app for soundscapes — I hate subscription services so I try and avoid anything that is based on that platform."
- [5★ US 2020-07-20] "Excellent, and no subscription! I love the variety of sounds, and I am thrilled that there is no subs[cription] fee!"
- [5★ US 2019-08-27] "Support indie developers, especially this one. You'll be glad you did." [honesty]

**Wishes (not hand-checked):** 47 reviews (14.4% of 327). Clusters: customization/mixing 10,
more variety 8, offline 3, timers 3.

---

## 4. What retains — praise codes vs longevity language

Longevity language = the review says "for years", "X years", "every day", "daily", "all day",
"every night", "can't work/sleep/live without", "my go-to", "since [year]", "long-time user",
"still using", "never uninstall", or the German equivalents (`seit Jahren`, `täglich`, `jeden
Tag`, `jeden Abend`). **230 of 1,860 positive reviews across all eight apps (12.4%) use it.**

The table below counts, inside those 230 reviews, how many also carry each other praise code, and
compares that with the code's share of all 1,860 positives. Lift > 1 means the code is
over-represented among people describing a durable habit.

| Praise code | in longevity reviews | % of the 230 | % of all 1,860 positives | **lift** |
|---|---:|---:|---:|---:|
| offline / privacy / no account | 6 | 2.6% | 1.3% | **2.02** *(n<5 baseline is thin — anecdotal)* |
| **variety / catalog size** | 25 | 10.9% | 5.6% | **1.93** |
| **one-time purchase / no subscription** | 17 | 7.4% | 4.2% | **1.74** |
| science framing | 11 | 4.8% | 2.8% | 1.71 |
| **sound quality / character** | 18 | 7.8% | 4.8% | **1.64** |
| **honesty / fair treatment / respects the user** | 12 | 5.2% | 3.2% | **1.62** |
| effect: sleep | 69 | 30.0% | 18.8% | 1.60 |
| effect: tinnitus / noise masking | 9 | 3.9% | 2.6% | 1.52 |
| effect: focus / productivity | 101 | 43.9% | 32.2% | 1.36 |
| adaptivity / personalization | 4 | 1.7% | 1.3% | 1.35 *(n<5, anecdotal)* |
| price / value for money | 19 | 8.3% | 6.6% | 1.26 |
| integration (watch / home / desktop) | 26 | 11.3% | 9.1% | 1.24 |
| effect: ADHD / neurodivergent | 14 | 6.1% | 5.2% | 1.18 |
| effect: anxiety / calm | 51 | 22.2% | 19.3% | 1.15 |
| control / customization | 20 | 8.7% | 7.9% | 1.10 |
| design / UI / aesthetics | 48 | 20.9% | 19.5% | 1.07 |

Read literally: **by raw volume**, long-term users talk about focus (43.9%), sleep (30.0%),
calm (22.2%) and design (20.9%). **By lift** — i.e. what distinguishes a long-term user's review
from any other positive review — the separators are variety/catalogue (1.93×), one-time purchase
(1.74×), science framing (1.71×), sound quality (1.64×) and honesty (1.62×), while design (1.07×)
and control/customization (1.10×) are essentially *flat* — they show up just as often in a
first-week rave as in a five-year one.

Per app, the code that co-occurs most with longevity language:

| App | longevity reviews | top co-occurring code |
|---|---:|---|
| Focus@Will | 41 of 245 pos (16.7%) | focus/productivity 33 (80.5%) |
| Brain.fm | 41 of 278 pos (14.7%) | focus/productivity 23 (56.1%) |
| Endel | 32 of 223 pos (14.3%) | focus/productivity 17 (53.1%), sleep 15 (46.9%) |
| myNoise | 21 of 109 pos (19.3%) | sleep 10 (47.6%), control/customization 8 (38.1%) |
| Noisli | 18 of 204 pos (8.8%) | sleep 6 (33.3%), tinnitus 3 (16.7%) |
| Portal | 57 of 477 pos (11.9%) | design 25 (43.9%), focus 21 (36.8%), sleep 17 (29.8%) |
| Dark Noise | 17 of 238 pos (7.1%) | design 6 (35.3%); anxiety, integration and one-time-purchase 5 each (29.4%) |
| Mubert | 3 of 86 pos (3.5%) | **n<5, anecdotal** |

---

## 5. Provenance

Every number in this document comes from raw files in
`research/review-mining/`. Nothing was fetched from a third-party analytics service, and nothing
is estimated.

**Raw pulls (untouched API responses), 80 files.** Endpoint:
`https://itunes.apple.com/{us|de}/rss/customerreviews/page={N}/id={APPID}/sortby=mostrecent/json?cc={us|de}`.
Naming follows the convention already in this directory (`reviews-<app>-<storefront>-p<N>.json`),
not the `<app>-<sf>-p<N>.json` form in the brief, so the new files sit alongside the existing
Endel/Brain.fm pulls.

| App | iTunes ID | US pages kept | DE pages kept |
|---|---|---|---|
| Focus@Will (`focusatwill`) | 638810714 | p1–p9 (+p10 empty, kept as end-of-feed evidence) | p1 (+p2 empty) |
| myNoise (`mynoise`) | 1523675125 | p1–p3 (+p4 empty) | p1 (+p2 empty) |
| Noisli (`noisli`) | 862773459 | p1–p6 | p1–p2 (+p3 empty) |
| Portal (`portal`) | 1436994560 | p1–p10 (**capped**) | p1–p3 (+p4 empty) |
| Mubert (`mubert`) | 1154429580 | p1–p3 | p1 (+p2 empty) |
| Dark Noise (`darknoise`) | 1465439395 | p1–p7 (+p8 empty) | p1 (+p2 empty) |

**Parsed corpora (same schema as the existing `parsed-endel-us.json`: `{date, rating, title,
content}`):** `parsed-focusatwill-{us,de}.json`, `parsed-mynoise-{us,de}.json`,
`parsed-noisli-{us,de}.json`, `parsed-portal-{us,de}.json`, `parsed-mubert-{us,de}.json`,
`parsed-darknoise-{us,de}.json`. Produced by `parse-competitors.py` (de-duplicates identical
date+title+content across pages).

**Analysis code and output:**
- `classify-competitors.py` — complaint + praise rules, EN + DE.
- `competitor-classification-report.txt` — the full stdout this document is transcribed from,
  including every category for every app and both storefronts.
- `complaints-per-review.csv`, `praise-per-review.csv` — per-review assignments.

**Reused, not re-derived:** `complaint-taxonomy.md` (Endel + Brain.fm complaint rankings),
`../need-mining/jobs-and-wishes-taxonomy.md` (jobs, wishes), `../need-mining/classify.py` (its
`WISH_TRIGGERS` / `WISH_RULES` were reused to count wishes for the six new apps),
`parsed-{endel,brainfm}-{us,de}.json` (unmodified; re-read only to recompute praise codes on this
document's rule set).

### What could NOT be obtained

- **Google Play / Android reviews:** not available through any free, key-less endpoint. Zero
  Android data in this document. All findings are iOS/macOS App Store only.
- **Storefronts beyond US and DE:** not pulled.
- **Portal US is truncated at 500 reviews.** The RSS feed hard-caps at 10 pages × 50 and all ten
  returned full pages, so Portal's true US review count is higher and its US history goes back
  further than 2021-12-13. Portal's US percentages describe the most recent 500 reviews only.
- **myNoise history before 2024-11-01** is not in the feed. The current listing (ID 1523675125)
  only returns reviews from Nov 2024 onward, i.e. the rewritten app. Legacy-app sentiment is
  present only where a reviewer mentions it.
- **No app in this set was delisted.** All six returned live feeds on both storefronts. Two feeds
  are genuinely thin rather than absent: Focus@Will DE (34 reviews) and Dark Noise DE (22),
  Mubert DE (23), myNoise DE (19) — all flagged as small in the per-app sections.
- **Feed flakiness:** `page=N` without a `?cc=` query parameter intermittently returns an empty
  feed for apps that demonstrably have reviews (Noisli US and Mubert US both returned 0 on three
  separate attempts, then 50 with the query parameter present). The final fetcher retries up to
  nine times across three URL forms per page and never accepts a zero until all retries fail; page
  files that never returned a real HTTP body were deleted rather than kept as `{}` placeholders.
  A zero-entry file that *is* a real API response was kept as end-of-feed evidence.
- **Wish counts for the six new apps are keyword-triggered only and were NOT hand-checked.** The
  Endel/Brain.fm wish numbers in `jobs-and-wishes-taxonomy.md` were hand-corrected review by
  review; these are not, and the prior work showed hand-checking moves those numbers materially.
  Treat section-level wish figures as indicative.
- **Residual "Other (uncategorized)" among negatives:** Focus@Will 17/218 (7.8%), myNoise 5/37
  (13.5%), Noisli 13/104 (12.5%), Portal 13/135 (9.6%), Mubert 10/78 (12.8%), Dark Noise 11/89
  (12.4%). Hand-reading the residual found it is genuine long tail (one-off gripes: app size,
  spelling errors, VoiceOver support, nudity in an animation), not a missed cluster.
- **Known classifier imprecision found during hand-check and left in place:** a small number of
  reviews land one category off — e.g. one Noisli 1★ ("Need updates … it's boring!!!") lands in
  Billing, and one Mubert 3★ about navigation lands in AI-distaste. Spot-check rate was roughly
  1–2 misassignments per 34-review sample. Category counts at n<5 should be read as anecdotal for
  this reason as well as for sample size.
- **Endel/Brain.fm complaint counts were not recomputed for publication.** Running this
  document's (wider) rule set over their corpora produces a different split — e.g. Endel's
  billing primary count comes out at 86 rather than the 122 in `complaint-taxonomy.md`, because
  new categories such as cancellation-difficulty and paywall-on-launch now absorb reviews that
  the older ruleset assigned to billing. `complaint-taxonomy.md` remains the authority for those
  two apps and its numbers are the ones used in the cross-app table.
