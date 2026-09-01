#!/usr/bin/env python3
"""Complaint + praise classification for the non-Endel/Brain.fm competitors.

Reuses the category names of complaint-taxonomy.md and the method of
need-mining/classify.py: keyword/regex rules (EN+DE), ONE primary complaint per
negative (1-3 star) review, plus mention-level "share of ALL reviews" counts
that deliberately overlap.

Praise codes are mention-level over 4-5 star reviews only.

Input : parsed-<app>-<sf>.json  (produced by parse-competitors.py)
Output: stdout report + complaints-per-review.csv / praise-per-review.csv
"""
import json, re, csv, os, sys
from collections import Counter, defaultdict

D = os.path.dirname(os.path.abspath(__file__))

APPS = {
    "Focus@Will": [("focusatwill", "US"), ("focusatwill", "DE")],
    "myNoise":    [("mynoise", "US"), ("mynoise", "DE")],
    "Noisli":     [("noisli", "US"), ("noisli", "DE")],
    "Portal":     [("portal", "US"), ("portal", "DE")],
    "Mubert":     [("mubert", "US"), ("mubert", "DE")],
    "Dark Noise": [("darknoise", "US"), ("darknoise", "DE")],
    # Endel and Brain.fm are re-run here ONLY so the PRAISE codes are computed on
    # the same rule set as the newer apps (their complaint numbers stay owned by
    # complaint-taxonomy.md). Same parsed files, untouched.
    "Endel": [("endel", "US"), ("endel", "DE")],
    "Brain.fm": [("brainfm", "US"), ("brainfm", "DE")],
}

# ---------------------------------------------------------------------------
# COMPLAINTS - priority order, first match wins as PRIMARY.
# Names reused verbatim from complaint-taxonomy.md where they fit.
COMPLAINT_RULES = [
    # --- most specific first; first match wins as the review's PRIMARY complaint ---
    ("AI-generated music distaste (\"soulless\")",
     r"\bai[- ]?(generated|music|slop)|generated .{0,12}music|no soul|soulless|randomly generated|elevator music|computer.generated"),
    ("Audible loops / short loops / audio artifacts",
     r"loop(s|ing)? (is|are|too|noticeab|audib|short|obvious)|audible (loop|jump|seam|gap)|noticeable (gap|loop|jump)|short(er)? loops?|hear(s|d|ing)? (the )?loop|repeats itself|repeating itself|loop point|crackle|crackling|compression artifact|artifacts?\b|clicks? and pops|skips? like|scratchy|monaural|mono (sound|only)|cuts? off (abruptly|mid)|st(ö|oe)rung|h(ö|oe)rbar(er)? ((ü|ue)bergang|schnitt)|loops? sind (zu )?kurz|nahtlos"),
    ("Abandonware / not updated / no new-device support",
     r"(not|never|hasn.t|haven.t|no longer) (been )?(updated|maintained|supported)|needs? an? update|please update|still not updated|last update was|abandon|dead app|not optimi[sz]ed for|doesn.t fit (the |my )?(screen|display)|iphone x|notch|retina display|larger (screen|display)|bigger screen|larger display|nicht (mehr )?(aktualisiert|gepflegt|optimiert)|keine anpassung|keine updates|seit .{0,12}kein update|out of business|eingestellt"),
    ("Subscription model resented (was one-time / went subscription)",
     r"(went|switched|turned|moved|changed) (in)?to (a )?subscription|now (a |it.s a )?subscription|now that it.?s subscription|subscription\?!|subscription\? no|boycott subscription|refuse to pay subscription|another subscription|yet another subscription|used to be (free|paid|a one|one.?time)|bought (the app|it) (before|once|years)|lifetime (member|purchase|version).{0,40}(now|lock|forced)|legacy (user|customer)|original customer|paid (for it|for the app) (before|already|once)|abo.?modell|jetzt ein abo|abo f(ü|ue)r|kein abo mehr|zwingt.{0,20}abo|new app, new subscription"),
    ("Paywall on launch / too little free content / \"not free\"",
     r"not (a )?free( app)?\b|listed as free|says? (it.?s )?free|free (plan|version|tier) is (useless|limited|laughable|a joke|so)|only \d+ (sound|scene|track)s? (are )?(free|available without)|free (plan|version).{0,25}(useless|limited|nothing)|paywall|locked behind|forces? (you )?to (subscribe|pay)|requires? a subscription (upon|to (even|open))|can.t (even )?(try|test|preview|listen).{0,25}(without|before) (pay|subscri|trial)|trapped in a|zwingt.{0,20}(zum kauf|zahlen)|nur mit abo|alles kostet|no free option|restrict(ed)? free|free (version|plan) is not (indicat|shown)|available in the free version|subscription fees in the first|everything just need to pay|need to pay for it|just pay for it|trop ferm(é|e)|nicht kostenlos"),
    ("Free alternatives exist (YouTube / free apps)",
     r"(youtube|spotify|pandora|free apps?|other free|for free (on|elsewhere|online))\b.{0,60}(free|instead|better|same)|free on youtube|can (get|find|listen).{0,40}(for )?free|so many free|plenty of free|10x the sounds|gibt.{0,20}kostenlos|umsonst"),
    ("Billing / unauthorized charges / refund anger",
     r"charged (me|us|my|again)|charge(d|s)? my (card|account)|still charg|keeps? charging|unauthorized charg|charged for|double.?charg|unauthorized|double.?bill|refund|money back|took my money|stole|fraud|scam|betrug|abgebucht|abbuchung|geld zur(ü|ue)ck|erstattung|abzock|rip.?off|ripoff|billed|bill me"),
    ("Cancellation difficulty",
     r"can.t cancel|hard to cancel|cancel(l)?(ed|ing|ation)|k(ü|ue)ndig|unsubscrib|abo beenden|stop the subscription"),
    ("Battery / data drain",
     r"battery (life|usage|drain|power)|drain(s|ing)? my battery|kills? my battery|akku|data (usage|hungry)|(used|consumed|eats?) .{0,15}(data|megabytes|gb)|frisst"),
    ("No offline / streaming-only",
     r"\boffline\b|online only|requires? (an )?internet|without (wifi|internet|a connection)|streaming every track|no download|can.t download|use my data|ohne internet|nur online"),
    ("Missing feature: can't mix sounds / no customization",
     r"can.?t (mix|combine|layer|blend)|only (play|one) (one )?sound at a time|mix (multiple|sounds|audio) (together|with)|needs a mixer|no (mixer|mixing)|combine (the )?(different )?(sound|track)s|mix with other apps|play (music|podcast|audiobook) (at the same time|simultaneous|along)|other audio|no (option|way) to (choose|pick|customi|adjust|set|save|favorite)|no random(izer)? (button|option)|nicht (mischen|kombinieren)|keine (auswahl|einstell)|its sounds with music|along with (music|podcast)|save (things|it) in a (personal )?library|no (personal )?library|can.t search"),
    ("Confusing / hard to figure out (onboarding, navigation)",
     r"can.?t figure (it |this )?out|how (do|to) (you|i) (even )?use|no (tutorial|instructions|onboarding|explanation)|confusing|unintuitive|not intuitive|hard to (figure|navigate|understand|use)|obtuse|what am i missing|unapproachable|nichts anfangen|versteh(e|t)? nicht|unverst(ä|ae)ndlich|kompliziert"),
    ("Feature removed / update regression",
     r"(since|after) (the )?(last |latest |new )?(update|redesign|version)|update (ruined|hat|broke)|used to (be able to|have|work|love)|removed (the|a|my|from)|took away|no longer (have|works|able|available)|bring back|regress|old (app|version) (was|is) better|worse (now|since)|cut or partition|locked out of|seit dem update|nach dem update|alte version"),
    ("UX / app bugs / reliability",
     r"\bcrash|\bbugs?\b|buggy|glitch|freez|\blag(s|gy|ging)?\b|stutter|won.t (open|load|play|start|run|download|close|delete)|(doesn.?t|does not|never) (open|load|play|start|work|run|launch)|(music|audio|sound|stream|playback|it) (just )?(stops|cuts out|shuts off|quits|drops)|stops? (playing|working)|keeps? (stopping|crashing)|black screen|white screen|blank (page|screen)|splash screen|loading screen|error\b|something went wrong|broken|unreliable|unstable|force (quit|clos)|restart the app|reopen the app|absturz|st(ü|ue)rzt ab|fehler|funktioniert (nicht|gar nicht)|h(ä|ae)ngt|bricht ab|startet nicht|schrott|geht nicht|no audio|no sound\b|plays? silence|it.s silent|is silent|didn.t work|did not work|takes forever to load|not downloading|sounds are damaged|audio is (very )?bad|inconsistent|choppy|skips? in the audio|doesn.t always work|refuses to work|no audio output|interfere(s)? with|volume slider|too much storage|app size"),
    ("Account / login / restore",
     r"log ?in|sign ?in|sign ?up|password|\baccount\b|restore (my )?purchase|restore purchases|can.t access|anmeld|konto|passwort|wiederherstell|verification|verify my|gmail|family sharing|synchroni[sz]|sync(ed|ing)? (across|on|to)|familienfreigabe"),
    ("Misleading advertising",
     r"misleading|false advertis|bait|not as advertised|deceptive|dishonest|irref(ü|ue)hrend|falsche versprech|nowhere does it say|hidden (fee|cost|charge)|description says|dark pattern"),
    ("Sound quality / unpleasant sounds",
     r"sound quality|audio quality|low quality|bitrate|tinny|distort|hiss|annoying (sound|noise|music)|unpleasant|grating|grates|harsh|awful (sound|music|noise)|terrible (sound|music)|horrible music|sounds? (fake|bad|digital|damaged)|not (very )?(good|realistic)|klangqualit|schlechte qualit|unangenehm|gr(ä|ae)sslich|nervig|zu hektisch|grausam|bescheiden|geringer qualit(ä|ae)t|distracting|disruptive"),
    ("\"Doesn't work / no effect\"",
     r"(doesn.?t|didn.?t|does not) (do anything|help|make a difference)|no (noticeable )?(effect|difference)|no effect|placebo|snake oil|gimmick|hat nicht geholfen|keine wirkung|bringt nichts|waste of (time|money)|does nothing|useless"),
    ("Repetitiveness / lack of variety",
     r"repetit|same (thing|song|sound|music|loop|track|few|handful)|endless repeat|over and over|monoton|\bboring\b|langweilig|wiederhol|immer (das|die) (gleiche|selbe)|dieselben|eint(ö|oe)nig|gets old|too few (sound|option|track)|not enough (sound|variety|option|music|track)|(low|limited|small|little) (selection|variety|count|options?)|only \d+ (sound|track|option|scene)|few (sound|option|scene|track)s|wenig auswahl|zu wenig|mehr abwechslung|begrenzt|alle .{0,15}gleich|all .{0,15}sound the same|(should|could|would like to|please) add (more )?(frog|ocean|beach|forest|rain|thunder|wave|bird|sound)|add (more )?(sound|nature)|expected (a lot )?more|more sound (option|alternat)|alternativen|fehlen mir|w(ü|ue)nsche mir mehr|worthy sounds|nothing to choose"),
    ("Upsell / ads / nagging in-app",
     r"\bads?\b|advert|pop.?up|upsell|nag(g|ging)?|full.?screen ad|sales pitch|spam(my|med|ming)?|push notification|forced notification|begging for|asks? for a (rating|review)|werbung|eigenwerbung|aufdringlich|prompt(ed|s)? me to (buy|upgrade)|constantly asks"),
    ("Price / value / paywall",
     r"too expensive|so expensive|expensive|overpriced|not worth|worth (it|the money)\?|\$\d|\d+ ?(usd|dollars|euro|€)|\bprice|pricing|\bcost\b|zu teuer|teuer|preis|kosten|greedy|gouging|cash grab|money grab|afford|can.t justify"),
    ("Missing platform / device support (Mac, watch, iPad, CarPlay…)",
     r"apple watch|watchos|\bipad\b|\bmac\b|macos|macbook|carplay|android|\bwidget|apple ?tv|homepod|airplay|chromecast|shortcuts?\b|\bsiri\b|background (mode|play|usage)|lock ?screen|desktop|wallpaper|\bweb\b|browser|voiceover|landscape|querformat|headphone jack|airpods?"),
    ("Customer support",
     r"customer (support|service)|no (reply|response|answer)|never (replied|responded|heard back)|support (team|ticket|email|page)|dev(eloper)? support|kundendienst|kundenservice|keine antwort|contacted (them|support)"),
]

# ---------------------------------------------------------------------------
# PRAISE codes - mention-level over 4-5 star reviews.
PRAISE_RULES = {
    "effect: focus / productivity":
        r"\bfocus(ed|es|ing|sed)?\b|concentrat|konzentr|deep work|productiv|get(s|ting)? (work|things|stuff) done|in(to)? the zone|flow state|fokus",
    "effect: sleep":
        r"\bsleep|asleep|insomnia|schlaf|einschlaf|nap\b|bedtime|through the night|durchschlaf",
    "effect: ADHD / neurodivergent":
        r"\badhd\b|\ba\.d\.d\.|\bau(d)?hd\b|autis|neurodiver|\basd\b|reiz(ü|ue)berflut|executive function",
    "effect: anxiety / calm":
        r"anxiet|anxious|panic|\bcalm|relax|soothe|soothing|entspann|beruhig|stress",
    "effect: tinnitus / noise masking":
        r"tinnitus|mask(s|ing)? (the |out )?(noise|sound)|drown(s|ing)? out|block(s|ing)? out (the )?(noise|sound)|neighbou?r|noisy (office|roommate|apartment)|(ü|ue)bert(ö|oe)n|(ü|ue)berdeck|nebenger(ä|ae)usch|open office|snor",
    "sound quality / character":
        r"sound(s)? (great|amazing|beautiful|wonderful|good|incredible|rich|natural|real)|high quality (sound|audio)|audio quality|klangqualit|realistic|lifelike|not (loopy|repetitive)|seamless (loop)?|no (audible|obvious) loop|well (recorded|produced|mixed)|hi.?fi|lossless|binaural|stereo|spatial|field recording",
    "variety / catalog size":
        r"variety|varied|so many (sound|option|track|choice)|huge (selection|library|catalog)|hundreds of|endless|never (get|gets) (old|boring)|always something (new|different)|abwechslung|vielseit|riesige auswahl|gro(ß|ss)e auswahl|every (mood|situation)|for every|wide (range|selection)",
    "control / customization":
        r"customiz|customis|\bmix(ing|er)?\b|slider|\beq\b|equaliz|adjust|fine.?tune|tweak|build (your|my) own|create (your|my) own|combine (sound|different)|per.?(sound|channel|layer) volume|control over|einstell|anpass|regler|selbst (mischen|zusammen)|granular|calibrat",
    "adaptivity / personalization":
        r"adapt(s|ive|ed)?\b|personaliz|personalis|responds? to|based on (my|your) (heart|activity|time|weather|location)|passt sich|reagier|individuell|circadian|real.?time",
    "price / value for money":
        r"worth (every|it|the)|great value|good value|cheap|affordable|bargain|reasonably priced|fair price|preis.?leistung|g(ü|ue)nstig|lohnt sich|best (money|purchase)|well spent",
    "one-time purchase / no subscription":
        r"one.?time (purchase|payment|fee|price)|pay once|no subscription|without a subscription|not a subscription|lifetime|buy it once|einmal(zahlung|ig)|kein abo|ohne abo|no monthly|not subscription.?based|owning|own it",
    "offline / privacy / no account":
        r"\boffline\b|works? without (internet|wifi|a connection)|no (account|sign.?up|login|registration) (needed|required)|no (data|tracking)|privacy|airplane mode|flugmodus|ohne internet|kein konto",
    "honesty / fair treatment / respects the user":
        r"no ads|ad.?free|honest|transparent|not greedy|doesn'?t nag|no nagging|no pressure|respects? (my|the user|your)|generous|fair\b|ehrlich|fair(e|er)? (preis|umgang)|no dark pattern|indie (dev|developer)|the developer (is|responds|replied|cares)|responsive dev",
    "design / UI / aesthetics":
        r"beautiful|gorgeous|stunning|sleek|elegant|minimal(ist)?|clean (design|interface|ui)|\bdesign\b|interface|\bui\b|\bux\b|intuitive|easy to use|simple to use|well (designed|made|crafted)|(ä|ae)sthet|sch(ö|oe)n|(ü|ue)bersichtlich|polished|delightful|animation|visual",
    "science framing":
        r"\bscience|scientific|research(.| )backed|neuroscience|neurolog|\bhz\b|frequenc|brainwave|binaural|isochronic|wissenschaft|forschung|study (showed|found)|peer.?review|patent",
    "integration (watch / home / desktop / shortcuts)":
        r"apple watch|watchos|\balexa\b|\bsiri\b|homepod|shortcuts?\b|\bwidget|carplay|apple ?tv|airplay|chromecast|mac app|desktop app|menu ?bar|ipad|sync(s|ed)? across|handoff",
    "longevity / daily habit":
        r"\bfor years\b|\d+ years|years now|every ?day|daily|all day|every night|can'?t (work|sleep|live|function) without|use it constantly|use this constantly|my go.?to|since (20\d\d|it came out)|long.?time (user|customer)|seit jahren|t(ä|ae)glich|jeden tag|jeden abend|forever|never uninstall|still using",
}

NEG = {1, 2, 3}

def load(app_key, storefront):
    p = f"{D}/parsed-{app_key}-{storefront.lower()}.json"
    if not os.path.exists(p):
        return []
    return json.load(open(p))

def build():
    rows = []
    for app, srcs in APPS.items():
        for key, sf in srcs:
            for i, r in enumerate(load(key, sf)):
                rows.append({
                    "app": app, "storefront": sf,
                    "id": f"{key}-{sf}-{i:03d}",
                    "rating": int(r["rating"]),
                    "date": r["date"][:10],
                    "title": r.get("title", ""),
                    "content": r.get("content", ""),
                    "raw": r.get("title", "") + ". " + r.get("content", ""),
                    "text": (r.get("title", "") + ". " + r.get("content", "")).lower(),
                })
    return rows

C_RES = [(n, re.compile(rx)) for n, rx in COMPLAINT_RULES]
P_RES = {n: re.compile(rx) for n, rx in PRAISE_RULES.items()}
ADD_CASED = re.compile(r"\bADD\b")
ADHD_CODE = "effect: ADHD / neurodivergent"


def praise_codes(r):
    """Praise codes for one review. 'ADD' is only counted when written in caps
    in the original text, so the English verb 'add' does not create false ADHD
    hits (Focus@Will's own subtitle is 'Control Your ADD', so this matters)."""
    codes = [n for n, rx in P_RES.items() if rx.search(r["text"])]
    if ADHD_CODE not in codes and ADD_CASED.search(r["raw"]):
        codes.append(ADHD_CODE)
    return codes

def primary_complaint(text):
    for n, rx in C_RES:
        if rx.search(text):
            return n
    return "Other (uncategorized)"

def main():
    rows = build()
    if not rows:
        print("no parsed files"); return
    by_app = defaultdict(list)
    for r in rows:
        by_app[r["app"]].append(r)

    cw = csv.writer(open(f"{D}/complaints-per-review.csv", "w", newline=""))
    cw.writerow(["app", "storefront", "id", "date", "rating", "primary_complaint", "title"])
    pw = csv.writer(open(f"{D}/praise-per-review.csv", "w", newline=""))
    pw.writerow(["app", "storefront", "id", "date", "rating", "praise_codes", "title"])

    for app, rs in by_app.items():
        n = len(rs)
        neg = [r for r in rs if r["rating"] in NEG]
        pos = [r for r in rs if r["rating"] >= 4]
        dates = sorted(r["date"] for r in rs)
        print(f"\n{'='*72}\n{app}: n={n}  ({sum(1 for r in rs if r['storefront']=='US')} US / "
              f"{sum(1 for r in rs if r['storefront']=='DE')} DE)  {dates[0]} -> {dates[-1]}")
        print(f"  negative(1-3*)={len(neg)} ({len(neg)/n*100:.1f}%)  positive(4-5*)={len(pos)} ({len(pos)/n*100:.1f}%)")
        for sf in ("US", "DE"):
            sub = [r for r in rs if r["storefront"] == sf]
            if not sub:
                print(f"    {sf}: EMPTY FEED (0 reviews returned)")
                continue
            d = sorted(r["date"] for r in sub)
            sneg = sum(1 for r in sub if r["rating"] in NEG)
            print(f"    {sf}: n={len(sub):4d}  {d[0]} -> {d[-1]}  neg={sneg} ({sneg/len(sub)*100:.1f}%)  mean {sum(r['rating'] for r in sub)/len(sub):.2f}*")
        print(f"  mean rating = {sum(r['rating'] for r in rs)/n:.2f}")

        prim = Counter(); prim_sf = defaultdict(Counter); stars = defaultdict(list)
        for r in neg:
            c = primary_complaint(r["text"])
            r["primary_complaint"] = c
            prim[c] += 1; prim_sf[c][r["storefront"]] += 1; stars[c].append(r["rating"])
            cw.writerow([app, r["storefront"], r["id"], r["date"], r["rating"], c, r["title"][:70]])
        mention = defaultdict(set)
        for r in rs:
            for cname, rx in C_RES:
                if rx.search(r["text"]):
                    mention[cname].add(r["id"])
        print("  -- COMPLAINTS (primary, among negatives) --")
        for c, k in prim.most_common():
            avg = sum(stars[c]) / len(stars[c])
            m = len(mention.get(c, ()))
            print(f"    {c:62s} {k:4d}  US {prim_sf[c]['US']:3d} DE {prim_sf[c]['DE']:3d}  "
                  f"avg {avg:.1f}*  mentionAll {m:4d} ({m/n*100:4.1f}%)")

        pm = defaultdict(set); pm_sf = defaultdict(Counter)
        for r in pos:
            codes = praise_codes(r)
            for nm in codes:
                pm[nm].add(r["id"]); pm_sf[nm][r["storefront"]] += 1
            pw.writerow([app, r["storefront"], r["id"], r["date"], r["rating"], "|".join(codes), r["title"][:70]])
        print(f"  -- PRAISE (mention-level among {len(pos)} positives) --")
        for nm, ids in sorted(pm.items(), key=lambda x: -len(x[1])):
            k = len(ids)
            print(f"    {nm:48s} {k:4d}  {k/len(pos)*100:5.1f}% of pos   US {pm_sf[nm]['US']:3d} DE {pm_sf[nm]['DE']:3d}")

        # longevity correlation
        lon = P_RES["longevity / daily habit"]
        lon_pos = [r for r in pos if lon.search(r["text"])]
        print(f"  -- LONGEVITY co-occurrence ({len(lon_pos)} positive reviews use longevity language) --")
        for nm, rx in sorted(P_RES.items()):
            if nm == "longevity / daily habit":
                continue
            k = sum(1 for r in lon_pos if nm in praise_codes(r))
            if k:
                print(f"    {nm:48s} {k:4d}  {k/len(lon_pos)*100:5.1f}% of longevity reviews")

if __name__ == "__main__":
    main()
