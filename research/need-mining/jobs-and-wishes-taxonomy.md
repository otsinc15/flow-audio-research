# Jobs-to-be-Done & Feature Wishes — Endel vs Brain.fm (iTunes US & DE storefront reviews)

**Companion to `complaint-taxonomy.md`.** Same corpus, same rigor, opposite lens: not what people complain about, but **why they use these apps** and **what they wish existed**.

**Source (verified):** raw iTunes RSS customer-review pulls in `../endel-repetitiveness/` (`parsed-endel-us.json`, `parsed-endel-de.json`, `parsed-brainfm-us.json`, `parsed-brainfm-de.json`). Originals untouched. Classifier: `classify.py` (keyword/regex rules, EN+DE); hand-check layer: `handcheck.py`.

**Corpus:**
- Endel: 600 reviews (300 US + 300 DE). 223 positive (4–5★).
- Brain.fm: 427 reviews (300 US + 127 DE). 278 positive.

**Method:**
- **Jobs:** each review assigned at most one PRIMARY use context (first match in a specificity-ordered rule list: tinnitus/noise-masking > ADHD > anxiety > sleep > relax > meditation > study > commute > exercise > reading/writing > focus/work > ambience). "Share of ALL" mention counts allow a review to hit several contexts (they overlap), like the complaint taxonomy.
- **Praise:** mention-level codes over 4–5★ reviews only (effectiveness claims, design, variety, science framing, integrations, adaptivity).
- **Wishes:** reviews flagged by explicit wish-phrasing triggers ("i wish", "would be great/nice if", "please add", "missing", "no option to", "if only", "wäre schön", "fehlt", "schade dass", …), then clustered. **Every one of the 111 wish-triggered reviews was read by hand**; 7 trigger false-positives (rhetorical "wish I discovered it sooner") were dropped and ~30 misassignments corrected (`handcheck.py` overrides). The counts below are the hand-checked numbers — clusters that survive on keywords but evaporate under reading (offline mode, widgets, timers) are called out honestly.

---

## Part 1 — Jobs-to-be-done

### Endel (600 reviews) — primary job, one per review

| # | Primary use context | Reviews | Share of ALL 600 | Mentioned in (overlapping) |
|---|----------------------|---:|---:|---:|
| — | no use context stated (billing rants, vague praise) | 328 | 54.7% | — |
| 1 | Sleep | 71 | 11.8% | 14.7% |
| 2 | ADHD / neurodivergent self-regulation | 70 | 11.7% | 11.8% |
| 3 | Focus / deep work | 41 | 6.8% | 23.8% |
| 4 | Relax / unwind / calm-down | 40 | 6.7% | 12.7% |
| 5 | Anxiety / stress regulation | 19 | 3.2% | 5.0% |
| 6 | Study / schoolwork | 11 | 1.8% | 4.3% |
| 7 | Reading / writing | 6 | 1.0% | 3.5% |
| 8 | Tinnitus / noise masking | 5 | 0.8% | 0.8% |
| 9 | General background ambience | 5 | 0.8% | 3.0% |
| 10 | Exercise / movement | 2 | 0.3% | 1.2% |
| 11 | Meditation / mindfulness | 2 | 0.3% | 1.3% |

**Read:** Endel is used as a *whole-day state machine* — sleep and ADHD lead as primary jobs, but "focus/work" is *mentioned* in nearly a quarter of all reviews. The 55% "none stated" is mostly billing/cancellation rants that never describe usage.

**Sleep:**
- [5★ US 2026-08-12] "I've been struggling with insomnia for two decades. I don't understand what the science is behind this, but this is not a gimmick. I've tried everything…the combo of sounds is different than other sound apps..this actually works! First time I've dreamed since…"
- [5★ US 2026-06-29] "First night was amazing I was asleep in minutes!"
- [5★ US 2026-06-25] "I've tried them all. Sleep and focus sound apps, calming this, relaxing that. Endel stands out as a game-changer. It genuinely works. I used to struggle with napping… I use the smart alarms and they wake me up at th[e right moment]"
- [5★ US 2026-08-29] "I can now sleep" (entire review)

**ADHD / neurodivergent:**
- [5★ US 2026-06-16] "For someone neurodivergent, this has become a serious boon for my cognitive functions, specifically focus. I focus better during work, creativity, and exercise."
- [5★ US 2026-06-20] "Have bad ADHD this helps"
- [5★ US 2026-03-23] "I love this app. It grounds my ADHD in a way that nothing else has ever been able to do."
- [5★ US 2026-04-29] "As an AuDHD person, I struggle with reading due to distractions. Endel's focus, dynamic focus, study, and deeper focus modes help me stay on task and make reading easier."

**Focus / work:**
- [5★ US 2026-05-19] "This app has seriously improved my ability to remain focused in a high stakes technical environment. My results thank you."
- [4★ DE 2023-07-11] "The deep work on the Endel works wonders on me. I could finish so many writing tasks including my thesis by listening to the deep work on the headphones. 👌"
- [5★ DE 2026-05-21] "In meinem Bürojob hilft mir der Fokus-Modus bei der Konzentration wie kaum etwas anderes. Der Study-Modus ist perfekt, um auch nach Feierabend noch konzentriert Texte zu lesen."

**Relax / calm-down / anxiety:**
- [5★ US 2026-07-20] "I literally wept the first time I calmed my mind down… I think it saved my life."
- [5★ US 2026-03-19] "I have been a firefighter and a paramedic for a very long time and I needed something to break up my day to relax because like others we can't turn off."
- [5★ US 2026-05-03] "I had a brain injury 10 [years] ago and I use this app every day since… It also helps me when I'm in crowded spaces or feeling anxious."
- [5★ US 2026-05-12] "Whenever I have anxiety or a panic attack this is this app I go to calm down and feel better."

**Tinnitus / masking (small but passionate):**
- [5★ DE 2024-06-12] "Die App hilft mir nicht nur beim Fokus auf der Arbeit sondern auch wenn der Tinnitus unerträglich wird… Bitte belasst die Funktion in Endel drin und entfernt diese nicht!"
- [4★ DE 2022-12-25] "Mit der Sleep-Funktion schlafe ich wirklich besser. Kleinere Geräusche, die mich sonst wecken, werden überdeckt."

### Brain.fm (427 reviews) — primary job, one per review

| # | Primary use context | Reviews | Share of ALL 427 | Mentioned in (overlapping) |
|---|----------------------|---:|---:|---:|
| — | no use context stated | 119 | 27.9% | — |
| 1 | Focus / deep work | 94 | 22.0% | 58.3% |
| 2 | ADHD / neurodivergent self-regulation | 70 | 16.4% | 16.4% |
| 3 | Sleep | 58 | 13.6% | 19.0% |
| 4 | Relax / unwind / calm-down | 28 | 6.6% | 15.2% |
| 5 | Study / schoolwork | 21 | 4.9% | 9.8% |
| 6 | Anxiety / stress regulation | 11 | 2.6% | 4.4% |
| 7 | Reading / writing | 10 | 2.3% | 7.0% |
| 8 | Meditation / mindfulness | 6 | 1.4% | 7.3% |
| 9 | Tinnitus / noise masking | 4 | 0.9% | 0.9% |
| 10 | Exercise / movement | 3 | 0.7% | 2.3% |

**Read:** Brain.fm is *the focus tool* — focus/work is the primary job for 22% of ALL its reviews and is mentioned in 58% of them. ADHD self-regulation is remarkably large for both apps (Endel 11.7%, Brain.fm 16.4% as primary job): these apps are functioning as unmedicated ADHD infrastructure.

**Focus / deep work:**
- [5★ US 2026-07-22] "If you have a neurodivergent brain, this app is a lifesaver! For work, I listen to 'Deep Focus' on my desktop computer every single day when I have to lock in… In total silence, my brain goes off on tangents."
- [5★ US 2026-08-09] "The UI is absolutely gorgeous… And the focus music/audio? I'm left completely speechless. It works so well."
- [5★ US 2026-06-07] "I've tried different focus playlists in all the music apps and this is the only app the actually consistently helps."
- [5★ US 2026-08-01] "It's the next best thing to hyper[focus]… I get really sharp and focused right away. And then I can stay there in the zone for a long, long time."

**ADHD:**
- [5★ US 2026-06-15] "Personally I find regular music too distracting and silence makes my brain too loud. Brain.fm is a great equal[izer]."
- [5★ US 2026-05-07] "16 week streak — and I'm not a streaker! Doing anything consistently is a Herculean effort because my brain craves novelty above all else. I love how the variety of stations meets me in all my 'modes' of life."
- [5★ US 2026-07-15] "If u have trouble focusing or ADHD THIS HELPS SO MUCH!!!!"

**Sleep:**
- [5★ US 2026-07-19] "I depend on it to get me to sleep quickly every evening. It's worth whatever I pay for it. I figure I am saving the money I spent on melatonin gummies."
- [5★ US 2026-01-08] "With Brain.fm Deep Sleep mode timed for 3 hrs, my body actually recovered overnight. HRV increased! … sleep graph show deep restorative sleep during the Brain.fm window." (user ran his own alcohol/HRV experiment)

**Study:**
- [5★ US 2026-07-09] "I am a grad student. This works way better than any drug."
- [5★ US 2026-01-27] "I'm a registered nurse and I used Brain.fm to study for a professional exam… I really appreciated the experience of putting on headphones and being absorbed."
- [5★ US 2025-11-21] "I'm a pre grad school student and live in a chaotic noisy home. Studying is difficult… it genuinely works. I've been using it now consistently for months and my studying is so much more focused now."

### What users PRAISE (share of 4–5★ reviews)

| Praise theme | Endel (of 223 pos.) | Brain.fm (of 278 pos.) |
|---|---:|---:|
| Effectiveness claims ("it actually works", "finally") | 17.5% | 36.3% |
| Design / aesthetics / UI | 7.6% | 2.5% |
| Integration praise (Apple Watch, HomePod, Alexa…) | 5.8% | 4.0% |
| Variety praise | 5.4% | 4.3% |
| Adaptive / personalized praise | 3.6% | 3.2% |
| Science framing ("research-backed", "neuroscience") | 2.7% | 7.6% |

- Brain.fm's love is *functional*: a third of its positive reviews contain an explicit effectiveness claim, and science framing is 3× Endel's ("data driven with numerous samples showing their product is effective", [5★ US 2025-10-27]; "real music developed by both scientists and a[rtists]", [5★ US 2026-08-09]).
- Endel's love is *sensory + ecosystem*: design praise ("the design is crazy good. Lot of work went into it. You can see and feel it", [3★ DE 2024-11-29]) and device adaptivity ("Die App verbindet die physischen Daten des Nutzers (wenn eine Smartwatch benutzt wird) mit den kosmischen (zirkardianrhythmisch)…", [5★ DE 2024-10-19]).

---

## Part 2 — Feature wishes / unmet needs (hand-checked)

Wish volume is modest: **70 Endel reviews (11.7%)** and **35 Brain.fm reviews (8.2%)** contain an explicit wish. Wishers skew positive — these are fans asking for more, not detractors.

### Endel — 70 wish reviews (share of ALL 600)

| # | Wish cluster | Reviews | Share of ALL |
|---|-------------|---:|---:|
| 1 | Account / cancellation / restore (complaint-adjacent: cancel via Apple, restore purchase) | 13 | 2.2% |
| 2 | Desktop / Mac feature parity | 9 | 1.5% |
| 3 | Customization / mix-your-own / controls | 7 | 1.2% |
| 4 | More variety / more soundscapes & music | 7 | 1.2% |
| 5 | Stop upsell / ads / push nagging | 6 | 1.0% |
| 6 | Cheaper / pricing / free tier / monthly option | 6 | 1.0% |
| 7 | UI / navigation / simplicity | 6 | 1.0% |
| 8 | Playback controls (autoplay, background mode) | 4 | 0.7% |
| 9 | Bug fixes | 4 | 0.7% |
| 10 | Watch / smart-home / casting integration | 3 | 0.5% |
| 11 | Audio quality / alternative sound variants | 2 | 0.3% |
| 12 | Sleep features (smart alarm, wake-up scenario) | 2 | 0.3% |
| 13 | Calendar / session-stats sync | 1 | 0.2% |

**Customization:**
- [5★ US 2026-03-23] "Can we please add a feature that allows the ability to adjust beats RPMs for certain playlist? That or create playlist with various RPMs for runners."
- [3★ US 2026-03-22] "I truly don't understand why there's no option to favorite certain soundscapes."
- [4★ US 2026-06-07] "I expected the music to be playlist based with the option to choose songs."
- [5★ US 2026-08-12] "I do wish I could play more than one solfeggio tone at once, or have the option to disable the added music that comes in."
- [4★ DE 2023-09-30] "Es fehlt mir nur eine Option oder die Möglichkeit binaurale Klänge einzuschalten."

**More variety / soundscapes:**
- [4★ US 2026-04-30] "But I wish there was more variety and options; even the sounds in the custom option feel like repeats of the same sounds."
- [4★ US 2026-04-28] "My one qualm is that the 8D audio seems super limited. I think it's just playing the one track? Surely there can be so much more variety."
- [4★ DE 2025-06-15] "Adding more natural sounds like rain, wind, or birds alongside the beats would make the experience more calming and immersive."
- [5★ DE 2024-10-19] "Es gibt im Internet eine Variante mit Gesang. Die sollte in die App integriert werden."

**Desktop / Mac parity:**
- [3★ DE 2025-10-20] "The more features are released on Endel for iPhone, the more frustrating is the Mac app… when I'm working it's a shame that I have to change to my ph[one]."
- [4★ DE 2025-03-25] "Ich weiß jedoch nicht, warum die Version für den Mac nicht alle Features der App bekommt… Mir fehlt vor Allem die Focus-Timer Fun[ktion]."
- [2★ DE 2026-01-07] "Missing many of the features of the iPhone app… Why not just enable us to install the fully featured iPhone/iPad app?"

**Pricing:**
- [3★ US 2026-08-03] "Great product but way too expensive given the free content now available elsewhere. Would love to see them come down by half…"
- [5★ US 2026-04-14] "I wish you had a month to month price because I would buy it in a heartbeat."
- [5★ US 2026-05-27] "It's expensive and I wish it was more accessible for lower income people."

**Stop upsell:** (all 6 are paying users begging to stop lifetime-offer pop-ups)
- [1★ US 2026-08-10] "Already purchased an annual subscription yet the app gives me a pop up for getting a lifetime subscription every time I enter the app, with seemingly no way to turn it off."
- [2★ DE 2026-06-11] "Please remove this or at least give the option to deactivate it."

**Playback controls:**
- [4★ DE 2022-12-25] "Nervig finde ich allerdings, dass ich den 'Hintergrundmodus' jeden Abend wieder neu aktivieren muss, um nicht auf mein Hörbuch zu verzichten."
- [4★ DE 2023-07-21] "…fehlt eigentlich nur noch Autoplay."

### Brain.fm — 35 wish reviews (share of ALL 427)

| # | Wish cluster | Reviews | Share of ALL |
|---|-------------|---:|---:|
| 1 | More variety / more soundscapes & music | 7 | 1.6% |
| 2 | Customization / mix-your-own / controls | 6 | 1.4% |
| 3 | Bug fixes | 6 | 1.4% |
| 4 | Cheaper / pricing / free tier | 5 | 1.2% |
| 5 | Watch / wearable / casting integration | 4 | 0.9% |
| 6 | Desktop / web version issues | 3 | 0.7% |
| 7 | Feature removed (bring back workout mode) | 1 | 0.2% |
| 8 | Account / cancellation | 1 | 0.2% |
| 9 | Audio quality | 1 | 0.2% |
| 10 | UI (iPad landscape) | 1 | 0.2% |

**More variety (Brain.fm's #1 wish):**
- [5★ US 2025-09-30] "PLEASE add a randomizer. The same song sequence plays from the beginning every time I start using the app. This is a basic feature for music apps."
- [3★ US 2026-03-25] "Could you add more piano and jazz music."
- [4★ US 2024-10-16] "My only issue is that I wish there was a greater selection of electronic music."
- [5★ US 2025-07-25] "It would be great to have a category for exercise."
- [5★ US 2025-03-17] "I can't wait for them to add more songs and genres."

**Customization:**
- [5★ US 2025-11-24] "I wish though they'd come up with an AI mode that would automatically harmonize isochronic tones w my choice of music."
- [5★ US 2026-03-26] "I do wish there was a way to have playlists in addition to the favorites library though…"
- [3★ DE 2022-08-28] "I use it only in the browser version, since there is no volume control in the app."
- [1★ US 2025-01-23] "I answered the questions for preferences and the music it played grates on my nerves. No way to change preferences. Deleted 10 minutes in."

**Watch / casting:**
- [5★ US 2026-01-26] "One thing I miss is being able to use it without my phone. It would be great if Brain.fm had a watch app like Endel does 🙏"
- [4★ US 2025-06-09] "Please make it available on the watch too! I like to leave my phone at home or hide it to stay productive."
- [4★ US 2025-09-23] "My only criticism is that it doesn't have Bluetooth. So you can't play it louder on a better speaker."

**Pricing:**
- [1★ US 2026-01-19] "I've paid the annual subscription ($50) for about 3 years now. A few days ago they doubled that price, and now EVERY day when I open the app, it says my sub is 'expired'…"
- [5★ DE 2025-11-02] "I wish they would make it for free because university students can't afford to pay f[or it]."
- [4★ DE 2024-04-12] "Ich würde auch gern nur ein Teil Paket (zum Beispiel Deep work) nehme[n]."

**Hypothesized clusters that did NOT materialize (hand-checked):** offline mode wishes ≈ 0 in both apps (the offline mentions are bug reports, not feature requests), widget wishes = 1, timer/scheduling wishes ≈ 1 (Endel's keyword "timer" hits were Mac-parity or UI complaints), Apple Health integration wishes ≈ 0.

---

## Cross-app takeaways for a "more variety" venture

1. **The job market is focus + ADHD + sleep, in that order.** Brain.fm: focus 22%/ADHD 16%/sleep 14% primary. Endel: sleep 12%/ADHD 12%/focus 7% primary. ADHD self-regulation is a huge, vocal, loyal segment in both — and both apps get accused of exploiting it with pricing ("Shameful app that takes advantage of ADHD people").
2. **Variety is wished for more than it's complained about.** Repetitiveness was a top-8 complaint (~4.5% of all reviews), but "more variety / more content" is a top-4 *wish* in both apps (Endel 7, Brain.fm 7 — Brain.fm's #1 wish cluster). The Brain.fm 16-week-streak quote is the venture thesis in one sentence: *"my brain craves novelty above all else… I love how the variety of stations meets me in all my 'modes' of life."* Users who habituate want a randomizer and fresh sequences, not just more static packs.
3. **Customization is the second door in.** Favorite/playlist/skip controls, per-layer mixing, BPM adjustment, exclude-tags — both apps' fans ask for compositional control. A generative app with real variety + user control answers both top wish clusters at once.
4. **Trust and pricing are the real moat to dig, not features.** The #1 Endel "wish" cluster is cancellation/billing (2.2% of ALL reviews) and #5/#6 are "stop upselling me" and "cheaper/monthly". Users explicitly say "equally good stuff on YouTube for free" — a new entrant needs a credible answer to that (generative novelty is one) plus clean Apple-native billing and no nagging.
5. **Don't over-invest in offline/widgets/timers** — barely anyone asks. Do invest in a watch/companion surface eventually (Brain.fm users literally benchmark against Endel: "a watch app like Endel does 🙏") and in sleep features (smart alarm/wake-up wishes exist but are rare).

**Files:** `classify.py` (rules), `handcheck.py` (overrides), `jobs-per-review.csv`, `wishes-per-review.csv` (auto), `wishes-final.csv` (hand-checked, authoritative), `cluster-samples.json`, `wishes-final-samples.json`.
