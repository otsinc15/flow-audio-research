#!/usr/bin/env python3
"""Need-mining: jobs-to-be-done + feature wishes from Endel/Brain.fm reviews.

Corpus: parsed-{endel,brainfm}-{us,de}.json (iTunes RSS customer reviews).
Method mirrors complaint-taxonomy.md: keyword/regex rules (EN+DE), one PRIMARY
job and one PRIMARY wish per review, plus mention-level shares of ALL reviews.
"""
import json, re, csv, sys
from collections import Counter, defaultdict

SRC = "/Users/othersideinc/Code/otsinc15/cyrus-os/tmp-scratch/endel-repetitiveness"
OUT = "/Users/othersideinc/Code/otsinc15/cyrus-os/tmp-scratch/need-mining"

APPS = {
    "Endel": ["parsed-endel-us.json", "parsed-endel-de.json"],
    "Brain.fm": ["parsed-brainfm-us.json", "parsed-brainfm-de.json"],
}

def load():
    reviews = []
    for app, files in APPS.items():
        for f in files:
            storefront = "US" if "-us" in f else "DE"
            data = json.load(open(f"{SRC}/{f}"))
            for i, r in enumerate(data):
                reviews.append({
                    "id": f"{app[:2]}-{storefront}-{i:03d}",
                    "app": app, "storefront": storefront,
                    "rating": int(r["rating"]),
                    "date": r["date"][:10],
                    "title": r.get("title", ""),
                    "content": r.get("content", ""),
                    "text": (r.get("title", "") + ". " + r.get("content", "")).lower(),
                })
    return reviews

# ---------------------------------------------------------------------------
# JOBS-TO-BE-DONE
# (regex, job) evaluated in priority order; first hit = primary job.
# Specific contexts first, generic ambience last.
JOB_RULES = [
    ("tinnitus/noise-masking", r"\btinnitus\b|\bmask(s|ing)?\b.{0,20}(noise|sound|tinnitus)|drown(s|ing)? (out|the)|block(s|ing)? (out )?(the )?(noise|sound|snor|office)|neighbor(s|s')? (noise|dog)|noise.cancel|office (noise|chatter)|übersteuer|übertön|maskier|nebengeräusch|überdeckt"),
    ("adhd/neurodivergent", r"\badhd\b|\badd\b|\bads\b|\bautis|\bautism|neurodiver|asd\b|reizüberflut|sensory"),
    ("anxiety/stress", r"\banxiet|\banxious|\bpanic\b|\bstress|overwhelm|\bnervous|angst|panik|nervös"),
    ("sleep", r"\bsleep|asleep|insomnia|fall asleep|bedtime|night.?time|einschlaf|schlafen|schlaf |einnick|durchschlaf|bettrand|gute nacht"),
    ("relax/unwind/calm-down", r"\brelax|unwind|wind ?down|\bcalm(s|ed|ing)? (me|down|my|myself)|de.?stress|chill|zur ruhe|runterkomm|abschalten|entspann|beruhig|soothe|soothing|grounding|grounds my"),
    ("meditation/mindfulness", r"\bmeditat|mindful|breathwork|yoga|entspannungsübung|atmen|achsamkeit"),
    ("study/schoolwork", r"\bstud(y|ying|ies|ent|ieren)|homework|exam|schule\b|uni\b|lern(en|t)?\b|für die schule|bachelor|thesis|dissertation|klausur|lernen"),
    ("commute/travel", r"\bcommut|\bflight\b|\bplane\b|\btravel|airport|road ?trip|in der bahn|\bzug\b|pendel|fahrt zur|on the go|unterwegs"),
    ("exercise/movement", r"\bwork ?out|\bgym\b|\brun(ning)?\b|\bjog|exercise|\bwalk(ing|s)?\b|hik(e|ing)|stretch|sport|joggen|laufen beim|runner"),
    ("reading/writing", r"\bread(ing|s)?\b|\bwrit(e|ing|ten|es)\b|lesen\b|schreib(en)?\b|\bbook\b"),
    ("focus/work", r"\bfocus|fokuss|concentrat|konzentr|deep ?work|\bwork\b|working|productiv|projekt|arbeit|büro|office work|tasks? to do|get (things|stuff) done|arbeiten|erledig|flow ?state"),
    ("general ambience/background", r"\bbackground|ambient\b|ambien|atmosph|hintergrund|nebenbei|while (cook|clean|do)|house ?work|chores|kochen|putzen|aufräum"),
]

# PRAISE sub-codes (mention-level, among 4-5 star reviews)
PRAISE_RULES = {
    "effectiveness claim": r"\bactually work|\bit works\b|\bwork(s|ed)? (for me|great|wonders)\b|\bfinally (able to|can|fell)|\binstant(ly)? (focus|calm|sleep|asleep)|\bhelps? (me |a lot)|\beffective|funktionier|\bhelps\b|\bhelped me\b",
    "design/aesthetics/UI": r"\bbeautiful|gorgeous|stunning|\bsleek|minimal(ist)?\b|\bdesign\b|\binterface\b|visual(s|ly)?\b|animation|ästhet|schön|übersichtlich|hübsch",
    "variety praise": r"\bvariet|variety|versatil|never (get|bore)|different (sound|music|every)|always (something )?(new|different)|vielseit|abwechslung|verschiedene|endless|unique every",
    "science framing": r"\bscience|scientific|\bresearch\b|neuroscience|binaural|\bhz\b|frequenc|brainwave|neurolog|wissenschaft|forschung|patent",
    "integration praise (watch etc.)": r"apple watch|\bwatchos\b|wear ?os|android watch|\balexa\b|\bsiri\b|home ?pod|spotify|apple music|shortcuts?|widget|komplikation|uhr\b",
    "adaptive/personalized praise": r"\badapt|\bpersonal|\bcustomiz|adjusts? (to|based)|responds? to|reagier|passt sich|individuell|smart\b",
}

# ---------------------------------------------------------------------------
# WISHES
# Trigger patterns mark a review as containing a wish; the wish is then
# clustered by keyword rules below.
WISH_TRIGGERS = [
    r"\bi wish\b", r"\bwish (it|they|there|the app|you|i)\b", r"\bwished\b",
    r"\bwould (be|have been) (nice|great|better|good|love|helpful)",
    r"\bit'?d be (nice|great|better|good|cool)", r"\bwould love (to see|if)",
    r"\bif only\b", r"\bmissing\b", r"\bmiss(ing)? (the|a|an)\b",
    r"\b(please|pls|plz) (add|bring|make|fix|include|give|implement|offer)",
    r"\bshould (add|have|offer|include|allow|implement|make)",
    r"\bneed(s|ed)? to (add|have|offer|include|allow|implement|make|fix)",
    r"\b(add|adding|include|including) (a|an|the|more)\b",
    r"\bhope (they|you|the dev(eloper)?s?|we) (can )?(add|fix|bring)",
    r"\bfeature request\b", r"\bsuggestion\b", r"\bmy (only )?(gripe|complaint|critici[sz]m)\b",
    r"\bwish there (was|were)\b", r"\bno (option|way) to\b", r"\bcan'?t (choose|pick|select|customiz|adjust|change|set|skip|loop|save|download|mix)",
    r"\bdoesn'?t have\b", r"\bdoes not have\b", r"\bwithout (the ability|a way|an option)\b",
    r"\blacks?\b", r"\bwhy (is there|isn'?t there|can'?t i|is it not|no)\b",
    r"\bone (more )?thing (that|i'?d|would)\b",
    # German triggers
    r"\bwäre (schön|toll|super|praktisch|gut|nice|nett)",
    r"\bwürde (mich )?(freuen|wünschen)", r"\bfehlt\b", r"\bfehlen\b",
    r"\bbitte\b.{0,30}(hinzufüg|einfüg|einbau|integri|mehr)",
    r"\bschade[,]? dass\b", r"\bleider (kein|keine|nicht|nur)\b",
    r"\bsollte man\b", r"\bman sollte\b", r"\bwenn (es|man|die app) (noch )?(nur|doch|mehr)\b",
    r"\bverbesserungswürdig\b", r"\bwunsch\b", r"\bverbesserungsvorschlag\b",
]

# Wish clusters, priority order: (name, regex)
WISH_RULES = [
    ("customization / mix-your-own / controls", r"customiz|personaliz|mix (your own|my own|them)|equaliz|\beq\b|adjust.{0,25}(bass|volume|levels|frequen|tempo|speed|intensity|beats|rpm|bpm)|\bbpm\b|\brpm\b|\btempo\b|control (the|over|each|individual)|choose (the )?(instrument|elements|layers|sounds in)|own (mix|playlist|sound|music)|choose my own|my (own )?choice of music|selbst (zusammenstell|mix)|anpassbar|einstellbar|regler|sliders?|crossfade|skip (a )?track|next track|eigene|play my own|combine|kombinier|\bplaylist|favorit(e|es|ieren)|bookmark|preference"),
    ("more variety / more soundscapes & music", r"more (\w{1,12} )?(variety|music|sounds?|soundscapes?|tracks?|options|choice|content|modes?|scenes?)|new (music|sounds?|soundscapes?|tracks?|content)|variety|variieren|mehr (auswahl|abwechslung|sounds|musik|varietät|inhalte|klang)|boring|same (thing|music|sound|song|loop)|repetit|größere auswahl|selection of|expand the|add (more )?(music|sounds|soundscape|piano|jazz|nature)|nature sounds|\brains?\b|\bbirds?\b|ocean waves?"),
    ("desktop / mac / windows / web version", r"\bmac(os)?\b|\bwindows\b|\bpc\b|desktop|web ?(version|app|site)|browser|computer version|laptop|macbook"),
    ("timer / scheduling / session features", r"\btimer\b|sleep timer|alarm\b|schedule|scheduling|auto.?mat(ic|ically) (start|stop|switch|turn)|stop (playing|the music) after|fade ?out|turn (off|itself off)|countdown|pomodoro|zeit(timer|steuer|schalt)|automatisch (startet|stoppt|wechselt|abschalt)|abschalt|wecker|ausschalten nach|länge|duration|how long"),
    ("stop upsell / ads / push nagging", r"nag(g?ing|ware)?|upsell|pop.?up|push.? ?(notif|nachricht|meldung)|too many ads|full.?screen ad|lifetime (ad|offer|deal|subscription)|werbung|eigenwerbung|sales pitch|promo(tion)?s? (for|to)|stop.{0,20}(ad|nag|upsell|promo)"),
    ("offline / download", r"\boffline\b|download|without (wifi|internet|connection)|flugmodus|airplane|ohne internet|herunterladen"),
    ("widget / lock-screen / control-center", r"\bwidget|lock ?screen|control center|sperrbildschirm|dynamic island|live activit"),
    ("cheaper / pricing / free tier", r"cheaper|less expensive|lower (the )?price|too expensive|pricey|günstiger|billiger|zu teuer|free (version|tier)\b|more free|longer (free )?trial|pricing|subscription (price|cost)|student discount|family (plan|sharing)|lifetime (option|purchase|plan)|one.?time (payment|purchase)|pay once|afford|month.?to.?month|monthly (price|subscription|payment|plan|option)|paywall|come down (in price|by)|reduce (the )?price"),
    ("integration: Spotify/Apple Music/streaming", r"\bspotify|apple music|youtube music|amazon music|\btidal\b|\bdeezer\b|streaming (service|integration)|connect.{0,20}(spotify|music)"),
    ("integration: watch / wearable / smart home / casting", r"apple watch|watchos|wear ?os|android (watch|auto)|\balexa\b|google (home|assistant)|home ?pod|smart ?home|\bsiri\b|shortcuts?|komplikation|carplay|bluetooth|airplay|chromecast|apple ?tv|\bon the watch\b|from the watch"),
    ("visuals / UI / navigation / dark mode", r"\bvisual|video|animation|dark mode|dark ?mode|\btheme|\bcolors?\b|graphics|fullscreen|landscape|horizontal|orientation|ipad (version|app|layout)?\b|bigger|font|visuell|grafik|dunkel|hell|oberfläche|farben|navigat|easier to (use|find|navigate)|intuitive|user.?friendly|simplif|bedienung|kompliziert|men(u|ü)"),
    ("language / localization", r"german|deutsch|english (version)?|language|sprache|übersetz|localiz|in (spanish|french|italian)"),
    ("sleep-specific features (smart alarm, tracking)", r"smart alarm|wake (me )?up|sleep (track|analy|monitor|cycl|quality)|wake ?up|aufwach|sleep data|sleep record|snor"),
    ("apple health / healthkit / data integrations", r"apple health|health ?kit|health data|heart rate|hrv\b|oura\b|fitbit|garmin|health integrat"),
    ("playback controls (autoplay / background mode)", r"auto.?play|background (mode|playback|play)|hintergrund.?modus|stop(s|ping)? playing automatically|start(s|ing)? (playing )?automatically|keep(s)? (playing|on)"),
    ("bugs/fixes (stability wishes)", r"\bfix\b|bug|crash|glitch|freeze|lag|stutter|absturz|fehler|stabil"),
    ("account / subscription management / restore", r"restore|log ?in|sign ?in|account|refund|cancel|subscription.{0,30}(manage|restore|sync)|sync across|multi.?device|several devices|multiple devices|family sharing"),
    ("quality / higher-fidelity audio", r"audio quality|sound quality|bitrate|higher quality|hi-?fi|lossless|klangqualität|audioqualität|bass boost|surround|spatial audio|3d audio|8d|dolby|atmos"),
]

TRIGGER_RES = [re.compile(t) for t in WISH_TRIGGERS]
JOB_RES = [(n, re.compile(r)) for n, r in JOB_RULES]
PRAISE_RES = {n: re.compile(r) for n, r in PRAISE_RULES.items()}
WISH_RES = [(n, re.compile(r)) for n, r in WISH_RULES]


def primary_job(text):
    for name, rx in JOB_RES:
        if rx.search(text):
            return name
    return None


def wish_cluster(text):
    for name, rx in WISH_RES:
        if rx.search(text):
            return name
    return "other/uncategorized wish"


def main():
    reviews = load()
    print(f"Loaded {len(reviews)} reviews")

    # ---- jobs ----
    job_primary = Counter()          # (app, job)
    job_mention = defaultdict(set)   # (app, job) -> set of review ids
    for r in reviews:
        pj = primary_job(r["text"])
        r["primary_job"] = pj
        job_primary[(r["app"], pj or "none stated")] += 1
        for name, rx in JOB_RES:
            if rx.search(r["text"]):
                job_mention[(r["app"], name)].add(r["id"])

    # ---- praise (4-5 star only) ----
    praise_mention = defaultdict(set)
    for r in reviews:
        if r["rating"] < 4:
            continue
        for name, rx in PRAISE_RES.items():
            if rx.search(r["text"]):
                praise_mention[(r["app"], name)].add(r["id"])

    # ---- wishes ----
    wish_primary = Counter()
    wish_mention = defaultdict(set)
    for r in reviews:
        r["has_wish"] = any(t.search(r["text"]) for t in TRIGGER_RES)
        r["primary_wish"] = wish_cluster(r["text"]) if r["has_wish"] else None
        if r["has_wish"]:
            wish_primary[(r["app"], r["primary_wish"])] += 1
            # mention-level counting is restricted to wish-triggered reviews,
            # so a billing rant that merely says "cancel" is not a "wish mention"
            for name, rx in WISH_RES:
                if rx.search(r["text"]):
                    wish_mention[(r["app"], name)].add(r["id"])

    # ---- report ----
    totals = Counter(r["app"] for r in reviews)
    for app in APPS:
        n = totals[app]
        print(f"\n=== {app} (n={n}) ===")
        print("-- primary job --")
        for (a, job), c in job_primary.most_common():
            if a == app:
                print(f"  {job:35s} {c:4d}  {c/n*100:5.1f}%")
        print("-- job mentions (share of ALL) --")
        rows = sorted(((job, len(ids)) for (a, job), ids in job_mention.items() if a == app),
                      key=lambda x: -x[1])
        for job, c in rows:
            print(f"  {job:35s} {c:4d}  {c/n*100:5.1f}%")
        print("-- praise mentions (share of 4-5★) --")
        pos = sum(1 for r in reviews if r["app"] == app and r["rating"] >= 4)
        rows = sorted(((p, len(ids)) for (a, p), ids in praise_mention.items() if a == app),
                      key=lambda x: -x[1])
        for p, c in rows:
            print(f"  {p:40s} {c:4d}  {c/pos*100:5.1f}% of {pos} positive")
        print("-- wish reviews --")
        nw = sum(1 for r in reviews if r["app"] == app and r["has_wish"])
        print(f"  reviews with any wish: {nw} ({nw/n*100:.1f}% of all)")
        print("-- primary wish cluster --")
        for (a, w), c in wish_primary.most_common():
            if a == app:
                print(f"  {w:55s} {c:4d}  {c/n*100:5.1f}% of all")
        print("-- wish mentions (share of ALL, overlapping) --")
        rows = sorted(((w, len(ids)) for (a, w), ids in wish_mention.items() if a == app),
                      key=lambda x: -x[1])
        for w, c in rows:
            print(f"  {w:55s} {c:4d}  {c/n*100:5.1f}%")

    # ---- CSVs ----
    with open(f"{OUT}/jobs-per-review.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "app", "storefront", "rating", "date", "primary_job", "title"])
        for r in reviews:
            w.writerow([r["id"], r["app"], r["storefront"], r["rating"], r["date"],
                        r["primary_job"] or "", r["title"]])
    with open(f"{OUT}/wishes-per-review.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "app", "storefront", "rating", "date", "primary_wish", "title"])
        for r in reviews:
            if r["has_wish"]:
                w.writerow([r["id"], r["app"], r["storefront"], r["rating"], r["date"],
                            r["primary_wish"], r["title"]])

    # dump sample quotes per cluster for hand-checking & report writing
    with open(f"{OUT}/cluster-samples.json", "w") as f:
        out = {"jobs": {}, "wishes": {}, "praise": {}}
        for app in APPS:
            out["jobs"][app] = {}
            for name, _ in JOB_RES:
                rs = [r for r in reviews if r["app"] == app and r["primary_job"] == name]
                out["jobs"][app][name] = [
                    {"rating": r["rating"], "date": r["date"], "storefront": r["storefront"],
                     "title": r["title"], "content": r["content"]} for r in rs]
            out["wishes"][app] = {}
            for name, _ in WISH_RES + [("other/uncategorized wish", None)]:
                rs = [r for r in reviews if r["app"] == app and r.get("primary_wish") == name]
                out["wishes"][app][name] = [
                    {"rating": r["rating"], "date": r["date"], "storefront": r["storefront"],
                     "title": r["title"], "content": r["content"]} for r in rs]
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("\nWrote jobs-per-review.csv, wishes-per-review.csv, cluster-samples.json")


if __name__ == "__main__":
    main()
