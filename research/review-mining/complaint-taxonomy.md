# Complaint Taxonomy — Endel vs Brain.fm (iTunes US & DE storefront reviews)

**Source (verified):** raw iTunes RSS customer-review pulls in this directory (`parsed-endel-us.json`, `parsed-endel-de.json`, `parsed-brainfm-us.json`, `parsed-brainfm-de.json`). Every finding below is derived directly from review text — no external data.

**Corpus:**
- Endel: 600 reviews (300 US, 2026-03-18 → 2026-08-29; 300 DE, 2022-10-21 → 2026-08-30). 377 negative (1–3★) = 63% of all.
- Brain.fm: 427 reviews (300 US, 2024-06-21 → 2026-08-28; 127 DE — all the DE storefront returned, 2016-12-02 → 2026-08-02, so DE skews older). 149 negative = 35% of all.

**Method:** each negative review assigned one primary category (keyword rules, EN+DE, manually iterated until "other" was ~5% residual). "Share of ALL reviews" counts any review (positive included) that *mentions* the complaint — a review can count in several categories there, so those shares overlap (e.g. billing reviews usually also mention price).

---

## Endel — ranked complaints (377 negative reviews)

| # | Category | Neg. reviews | US | DE | Avg ★ | Share of ALL 600 reviews |
|---|----------|---:|---:|---:|---:|---:|
| 1 | Billing / unauthorized charges / refund anger | 122 | 93 | 29 | 1.1 | 21.7% |
| 2 | UX / app bugs / reliability | 66 | 20 | 46 | 1.9 | 21.7% |
| 3 | Upsell / ads / nagging in-app (lifetime-offer pop-ups for paying users) | 43 | 22 | 21 | 1.6 | 11.0% |
| 4 | Price / value / paywall | 30 | 12 | 18 | 1.5 | 30.8%* |
| 5 | Cancellation difficulty | 29 | 14 | 15 | 1.6 | 13.7% |
| 6 | Misleading advertising (song in ad not in app, "8D" claims) | 26 | 21 | 5 | 1.2 | 7.8% |
| 7 | Sound quality / unpleasant sounds | 10 | 5 | 5 | 2.5 | 2.8% |
| 8 | **Repetitiveness / lack of variety** | 10 | 4 | 6 | 1.2 | **4.5%** |
| 9 | "Doesn't work / no effect" | 9 | 5 | 4 | 1.2 | 5.3% |
| 10 | Feature removed / update regression | 8 | 3 | 5 | 1.4 | 3.8% |
| 11 | Account / login / restore | 5 | 1 | 4 | 2.0 | 0.8% |
| 12 | Customer support | 4 | 2 | 2 | 2.0 | 3.3% |
| 13 | Other (misc: app icon, language, vague rants) | 15 | 4 | 11 | 2.3 | — |

\* Price share is inflated by co-mentions: nearly all billing/cancellation reviews also mention money. As a *primary* complaint it ranks 4th.

**Plain-English read:** Endel's negative reviews are dominated by *money-trust* issues — being charged after cancelling, refused refunds, "scam/fraud" language (avg 1.1★, heavily US) — and by a large DE cluster complaining the apps (especially macOS) are buggy, overloaded, or regressed after redesigns. The in-app upsell nagging (full-screen lifetime ads shown to paying subscribers) is a distinct, unusually specific complaint on both storefronts. **Repetitiveness/lack of variety is real but small: 10 of 377 negative reviews, mentioned in only 4.5% of all reviews.**

### Quotes

**Billing / charges / refunds:**
- [1★ US 2026-08-29] "Beware they will still charge you even if you cancel the trial membership days before it ends! … I verified I canceled because they have [confirmation]."
- [1★ US 2026-08-23] "These individuals are deceivers. I installed the application and terminated it in under a minute, yet I was billed 79.99. I have notified American Express about them."
- [1★ US 2026-08-24] "I cancelled my subscription during the trial period but was still charged the annual rate. Tried to seek refund through customer service and told they can't."

**UX / app bugs:**
- [1★ US 2026-05-25] "Immediately crashes — I paid for the year and now every time I open it, it immediately crashes after two seconds!"
- [1★ US 2026-06-11] "The music is good. The UX is like a puzzle… using the app for a long time BUT still have to realize how to navigate every time."
- [1★ DE 2026-06] (typical DE macOS complaint) "Apps leave a lot to be desired… Desktop app seems half-baked and not Mac-native."

**Upsell / ads nagging:**
- [1★ US 2026-07-31] "I pay for Premium, yet every time I open the app I'm greeted with a full-screen ad that blocks me from doing anything until I close it."
- [1★ US 2026-07-25] "Every single time I want to use the app, there's a sales pitch I need to go through, and I already pay yearly. Come on!!"
- [1★ DE] "Nervt mit Eigenwerbung und noch teureren Abos — Selten eine App erlebt, die Nutzer so aggressiv und ausdauernd mit weiteren Abos … nervt."

**Price / value:**
- [1★ US 2026-05-03] "…it told me it was $120 a year or $70 a month for 3 months as the subscription options. That's absolutely insane for an app."
- [1★ US 2026-06-16] "It costs $119/yr … Shameful app that takes advantage of ADHD people."

**Repetitiveness / variety:**
- [1★ DE 2026-08-30] "Always the same — You can choose between 3 or 4 different soundscapes, that after a while get really annoying and repetitive and cause exactly the opposite."
- [1★ DE 2025-11-22] "Das Repertoire an Klängen ist so gering, dass man gezwungen ist, immer wieder das Gleiche zu hören."
- [1★ US 2026-06-22] "Bought a subscription but there's just not enough on here to keep it interesting if I were to use it every day."

---

## Brain.fm — ranked complaints (149 negative reviews)

| # | Category | Neg. reviews | US | DE | Avg ★ | Share of ALL 427 reviews |
|---|----------|---:|---:|---:|---:|---:|
| 1 | UX / app bugs / reliability (offline mode, playback errors, sub-not-recognized) | 35 | 22 | 13 | 2.0 | 15.9% |
| 2 | Price / value / paywall ("$99/yr for AI music") | 27 | 16 | 11 | 1.6 | 20.8% |
| 3 | Billing / charged-after-cancel / paid-but-can't-use | 26 | 21 | 5 | 1.2 | 7.3% |
| 4 | Cancellation difficulty | 13 | 7 | 6 | 1.5 | 5.9% |
| 5 | Sound quality / unpleasant sounds (low bitrate, "grates on nerves") | 10 | 4 | 6 | 1.6 | 3.3% |
| 6 | "Doesn't work / no effect" | 10 | 7 | 3 | 1.2 | 6.3% |
| 7 | **Repetitiveness / lack of variety** | 7 | 6 | 1 | 2.7 | **4.2%** |
| 8 | Account / login / can't restore purchase | 7 | 6 | 1 | 1.3 | 2.3% |
| 9 | Misleading advertising | 2 | 1 | 1 | 1.0 | 0.7% |
| 10 | Customer support | 2 | 2 | 0 | 1.0 | 2.6% |
| 11 | Upsell / ads / nagging | 1 | 1 | 0 | 1.0 | 1.4% |
| 12 | Feature removed (workout mode) | 1 | 1 | 0 | 3.0 | 1.2% |
| 13 | Other (misc: AI-generated-music distaste, language) | 8 | 5 | 3 | 2.1 | — |

**Plain-English read:** Brain.fm is much better liked overall (only 35% negative vs Endel's 63%). Its negatives are led by *app reliability* — offline mode broken, playback errors, "paid but app asks me to subscribe again" (a reliability bug that bleeds into billing) — and by *sticker shock*: recurring "$100/yr is ridiculous" and "paid app pretending to be free" complaints, on both storefronts. A notable DE-specific sub-theme is sounds being actively unpleasant ("grässliche Geräusche"). **Repetitiveness is again a minor complaint: 7 of 149 negative reviews, 4.2% of all reviews.**

### Quotes

**UX / app bugs:**
- [1★ US 2026-01-12] "Music great, app terrible — Please please fix the playback error problem when I have a song saved in offline and I try to access it from another device…"
- [1★ US 2025-06-23] "The app is unreliable. Often, I will click on it, and it will not fully open before it closes down… the bugs are crazy glitchy."
- [1★ DE] "Tolle Idee es funktioniert auch, aber… der Offline Modus funktioniert leider überhaupt nicht. Somit kann man das System nicht in der Bahn nutzen."

**Price / value:**
- [1★ US 2026-04-06] "AI generated elevator music — They want $99/year though 😂😂😂😂"
- [1★ US 2026-05-23] "This app is ridiculously priced for AI generated music. Reduce prices by 75% or make it free."
- [1★ DE] "Coole App but way too expensive… 100€ per year for some EDM based learning music is pretty overpriced."

**Billing / paid-but-can't-use:**
- [1★ US 2026-08-04] "I have paid 99$ for one year. And NOTHING. Your app still proposing to me to buy subscription again 😡"
- [1★ US 2026-02-19] "I pay a monthly subscription but anytime I want to use the app it tells me i need a subscription even though I already have one and signed in."
- [1★ US 2026-03-17] "Tried to cancel and did it on the web browser (as instructed by the app). The app still charged me today for a year long subscription… Feels like a scam."

**Cancellation:**
- [1★ US 2026-07-13] "Subscription — Nightmare to end subscription"
- [1★ US 2026-08-17] "Now I'm constantly hit with spam mail from Brain.com that won't honor any unsubscribe requests."

**Sound quality:**
- [1★ DE 2023-03-30] "Ich habe es keine 5 Minuten ausgehalten. Grässliche Geräusche die jemanden mit ADS wie mich nur aggressiv machen."
- [1★ DE 2025-06-09] "The audio has low quality and the 'Deep Work' soundscape is really annoying all together."

**"Doesn't work / no effect":**
- [1★ US 2026-06-05] "Didn't work at all. … I tried over 50 different tracks and none boasted results."
- [1★ US 2025-05-12] "blah — doesn't do anything 👎👎 also paying for sounds??? rlly"

---

## Cross-app takeaways

1. **Billing/trust is the loudest complaint for both apps** (Endel #1 at 21.7% of *all* reviews mentioning it; Brain.fm #3 but combined with cancellation and the "paid-but-can't-use" reliability bug it's the same trust wound). Endel's billing anger is far more intense (122 reviews, avg 1.1★, mostly US).
2. **Repetitiveness/lack of variety is a *minor* complaint for both apps** — ~4.5% of all reviews mention it for either app; it ranks #8 of 13 for Endel and #7 of 13 for Brain.fm. It exists (DE Endel reviews voice it most sharply) but is dwarfed by money/trust and reliability complaints.
3. **Storefront split matters:** Endel DE skews toward app-quality/redesign regressions and upsell nagging; Endel US skews toward billing/refund and misleading-ad anger. Brain.fm DE uniquely adds "sounds are actively unpleasant"; DE data is thin (127 reviews, back to 2016), so treat those percentages cautiously.
4. Endel has a complaint category Brain.fm essentially doesn't: **in-app upsell nagging of paying subscribers** (43 negative reviews, 11% of all Endel reviews).
