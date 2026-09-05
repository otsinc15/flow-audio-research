# Can Riemann Kollektion (or comparable free loop sources) be used inside a shipped focus-music app?

**Compiled 2026-09-02.** Question: can loops from Riemann Kollektion's FREE ambient/techno/dub-techno
sample packs legally be used as source stems inside an app that assembles/crossfades them at runtime, or
that pre-renders sessions and streams the rendered audio to subscribers?

Every claim traces to a saved primary page (`src-riemann-*.txt`, URL + fetch date in the header) or to a
Perplexity `sonar-pro` pass (`sonar-riemann-*.json`, marked as such and never treated as a primary source).
What could not be verified from a primary page says **not found**, not a guess.

---

## 1. Riemann Kollektion — the licence, verbatim

There is **no separate `/license`, `/licence`, `/faq`, `/terms`, or `/eula` page** — all of those return
HTTP 404 (`src-riemann-terms-of-service.txt` confirms `/policies/terms-of-service` is generic Shopify
boilerplate with no product-licence content at all). The actual **"RIEMANN KOLLEKTION – SAMPLE LIBRARY
LICENSE AGREEMENT"** is embedded at the bottom of `/pages/about-us` (`src-riemann-about-us.txt`), and nowhere
else — not one of the six individual product pages checked (three free, three paid) carries its own licence
text; all inherit this one page.

> "Upon purchase, Riemann Kollektion grants you a **non-exclusive, non-transferable, perpetual license** to
> use the included sounds in your own musical compositions, audio-visual works, and productions, whether
> released commercially or non-commercially, without payment of additional royalties."

> **Permitted:** "Use the samples in production music and library music, **provided they are incorporated
> into musical compositions and not distributed as standalone sounds.**"

> **Prohibited:** "Resell, sublicense, distribute, share, transfer, or otherwise make available the samples,
> in whole or in part, **as standalone files**." … "Use the samples **in isolation, where the primary value
> of the product is the sample itself rather than a musical composition**." … "Use the samples for the
> purpose of training, fine-tuning, or developing artificial intelligence, machine learning, or generative
> audio systems without prior written consent."

**No "sampler / sample playback unit / website / computer" clause exists in this text** — that is Goldbaby's
language, not Riemann's (§3 below). Riemann's text never mentions apps, software, or runtime playback at
all, in either direction. A Perplexity cross-check (`sonar-riemann-licence-and-alt-sources.json`) reached
the same conclusion independently: "I could not verify any explicit clause in a primary source that
mentions apps, software, sample-playback units, or embedding samples inside a shipped application" — and
likewise found **no evidence that free packs carry a different licence than paid packs** (the licence page
is one page, referenced site-wide).

**Reading for a generative app:**
- ✅ **Pre-rendering sessions offline and shipping/streaming only the finished mix** — this is squarely
  "incorporated into musical compositions," the licence's own permitted use.
- ❌ / ⚠️ **Shipping the raw WAV stems inside the app bundle so the app can crossfade them at runtime** — a
  bundled, individually-addressable WAV file is hard to distinguish from "as standalone files," and a
  stem-based generative engine's entire value proposition is arguably "the sample itself rather than a
  musical composition," which is the exact case the prohibited-uses clause names. Riemann's licence is
  **less explicit** than Goldbaby's (no named "sampler/computer" clause) but **no more permissive** — it
  bans the same underlying act (standalone/isolated distribution of the samples) through different words.
  Treat the verdict as the same as §4 of `synth-instruments-2026-09-02.md`: fine pre-rendered, not fine
  embedded raw.

---

## 2. Free-pack inventory — most of "Free Sample Packs" is not actually free

`/collections/free-sample-packs` (`src-riemann-free-sample-packs.txt`) is titled **"Free Techno Sample Packs
/ On Sale"** and lists 35 products — but only **4 are priced €0.00**; the other 31 are discounted paid packs
(e.g. "Riemann Dub Techno 2" shows €29.95 struck through to €19.95, not free, despite living in this
collection). Checked directly on each product page (`src-riemann-product-*.txt`):

| Pack | Price | Format / size | Contents | BPM / key |
|---|---|---|---|---|
| **FREE Techno Starter Sample Pack 2026** | €29.95→**€0.00** | 223 × 24-bit WAV, **308MB** | Atmosphere, bass, beat, chord, clap, fx, groove, hihat, kick, percussion, ride, snare, synth, top **loops** + bass/chord/clap/hihat/kick/fx/noise/percussion/ride/snare/synth **oneshots**. Copy explicitly names "Deep Hypnotic Techno and Raw Hypnotic Techno… Deep Techno, Melodic Techno and Dub Techno" as the covered styles. | not found |
| **FREE Organic House Starter Sample Pack (ASHRAM Sounds)** | €29.95→**€0.00** | 262 × 24-bit WAV, size **not found** on page | Afro percussion, deep-house bass/chord loops, ethno pad/synth/vocal loops, **texture background loops**, deep-techno bass/beat/synth loops, oneshots | not found |
| FREE DOWNLOAD: Riemann Techno Mastering Chain 2026 | €9.95→**€0.00** | Ableton Live effect rack (not audio) | 8 mastering presets | n/a |
| FREE DOWNLOAD: Riemann House Mastering Chain 2026 | €9.95→**€0.00** | Ableton Live effect rack (not audio) | 5 mastering presets | n/a |

The 31 non-free items in that collection (e.g. Dub Techno 2, Raw Hypnotic Techno 2, Minimal Techno 3, Fast
Minimal Grooves 4 — all €19.95–€29.95) are **not free** despite being listed under "Free Sample Packs";
several of them do carry stated BPM (Raw Hypnotic Techno 2 = 135bpm/1.14GB, Minimal Techno 3 = 126bpm/451MB,
Fast Minimal Grooves 4 = 145bpm/243MB) but they cost money and are out of scope for a "free" comparison.

**No dedicated ambient collection or pack exists anywhere on the site** — checked the full nav link list;
every genre link is techno/house/psytrance/hardgroove — mark **not found**.

**Signup/account:** No account or newsletter email is required to view prices or add a €0.00 item to cart.
Whether Shopify's checkout then demands an email address to complete a €0 order was **not tested** — the
task excludes downloads/purchases, and this session did not click through checkout. Treat as **not
verified** rather than "no signup needed."

---

## 3. Same check, briefly, on alternative free/CC0 loop sources

| Source | Accessible? | What the primary page literally says |
|---|---|---|
| **Freesound (CC0)** | ✅ (already verified in `synth-instruments-2026-09-02.md` §4, reused here) | Freesound's own FAQ: "for the 'zero' license you can do pretty much what you want with the sound. You could even sell the sound... but you can't claim you are the author!" (`src-freesound-license-page.txt`). A CC0-filtered `TR-909` search returns 712 sounds. **Only source confirmed clean for both pre-rendered and runtime/embedded use** — but per-sound licence must be checked individually (by-nc sounds are mixed into the same site) and quality/provenance is user-uploaded and uneven. |
| **Legowelt free samples** (`legowelt.org/samples/`) | ✅ fetched directly, 200 OK (`src-riemann-legowelt-samples.txt`) | No formal EULA at all. Verbatim: **"The samples are free to download and use in your productions."** Packs are direct-download ZIPs (Prophet 600 — 386 samples, 198MB; Oberheim Matrix 1000 — 181 samples; Jupiter 8 — 500 samples; "Drumnibus Electrodrums" — 230 samples, 30MB), all **16-bit WAV** (not 24-bit), no account/signup. Content is dreamy analog pads/basses/FX from named vintage synths — sonically close to the ambient/dub-techno character wanted, but there is **no licence text to point to either permitting or forbidding embedding in a shipped app** — it's an artist donationware page, not a commercial EULA, so the legal footing is informal rather than clean. |
| **Loopmasters free taster packs** | ❌ blocked | `loopmasters.com/legal`, `/faq`, and every `help.loopmasters.com` licence article returned **HTTP 403 with a Cloudflare "Just a moment…" interstitial** (`src-riemann-loopmasters-legal-blocked.txt`, `src-riemann-loopmasters-license-agreement.txt`) — could not be fetched without solving a CAPTCHA, which is out of scope. A Perplexity pass (`sonar-riemann-licence-and-alt-sources.json`, **secondary source, not independently verified**) reports their commercial-use FAQ says: *"You cannot use the sounds in isolation (i.e. when not within musical compositions)... unless as part of a composition with other sounds."* — if accurate, this is the same not-standalone pattern as Riemann/Goldbaby/SFM, but treat this one line as **unverified** until someone fetches it directly (logged-in browser, not curl). Loopmasters' free-samples genre page itself did load (`src-riemann-loopmasters-free-genre.txt`) — 24-bit packs, several 100–1200MB, exist. |
| **MusicRadar SampleRadar** | ❌ dead | Already confirmed HTTP 404 in `synth-instruments-2026-09-02.md` §4 (`src-musicradar-909.txt`) — page no longer exists. |

---

## 4. Recommendation

**(a) Ear test only (internal, never distributed):** use the two genuinely-free Riemann packs — **FREE
Techno Starter (308MB, hypnotic/dub/melodic techno character, 24-bit)** and **FREE Organic House Starter
(size not stated)**. Redistribution restrictions don't bind an internal listening test that ships nothing
to anyone; this is the fastest way to hear the character. Total confirmed download: **308MB + an unstated
amount** (Organic House Starter page never states its size — budget ~300–400MB by analogy to the Techno
Starter pack, but that is an estimate, not a quoted figure).

**(b) Shipped app:** none of Riemann Kollektion, Goldbaby, Samples From Mars, or Legowelt gives a clean
contractual green light to embed raw stems for runtime crossfading — Riemann's "not distributed as
standalone files" / "primary value... the sample itself" clauses reach the same result as Goldbaby's
explicit "sampler/computer" ban, just via different wording. The only source verified clean for **both**
pre-rendered and runtime/embedded use is **Freesound CC0** (checked per-sound). Practical path: **pre-render
finished sessions offline from any of these packs** (permitted everywhere here as "incorporated into a
musical composition") and ship only the rendered audio to subscribers; if runtime stem-assembly inside the
app is a hard requirement, restrict embedded stems to CC0-verified Freesound sounds (or commission/licence
stems under an explicit "software/app" grant) rather than any Riemann, Goldbaby, SFM, or Legowelt file.
