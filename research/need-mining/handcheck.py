#!/usr/bin/env python3
"""Apply hand-checked overrides to the wish classification and emit final counts.

Every wish-triggered review in both apps was read by hand; reviews whose
auto-cluster was wrong (or whose "wish" was rhetorical/praise) are overridden
here by content fragment. Each fragment must match exactly one review.
"""
import json, csv
from collections import Counter, defaultdict
import classify

# fragment -> corrected cluster ("DROP" = trigger false positive, not a wish)
OVERRIDES = {
    # ---------------- Endel ----------------
    "don't want to be on the hook for another 100+": "account / cancellation / restore",
    "music was very different from the ad that drew me in": "more variety / more soundscapes & music",
    "extorts you into paying if you want to use it any longer": "cheaper / pricing / free tier",
    "overly complicated timer for the pomodoro": "visuals / UI / navigation / simplicity",
    "create custom shortcuts to start scenarios": "customization / mix-your-own / controls",
    "menge an funktionen und den aufbau generell mit vielen symbolen": "visuals / UI / navigation / simplicity",
    "variante mit gesang. die sollte in die app integriert werden": "more variety / more soundscapes & music",
    "using this app exclusively for smart alarm": "sleep-specific features (smart alarm, wake-up)",
    "make it horizontal compatible too so it can be used like": "visuals / UI / navigation / simplicity",
    "möglichkeit binaurale klänge einzuschalten": "customization / mix-your-own / controls",
    "app für die apple watch sollte besser ausgebaut werden": "integration: watch / wearable / smart home / casting",
    "play more than one solfeggio tone at once": "customization / mix-your-own / controls",
    "i recommend it if u want a amazing soundscape app": "DROP",
    "one of my favorite features was the menu bar": "desktop / mac / windows / web version",
    "uplift feature doesn’t collect my health and location data": "bugs/fixes (stability wishes)",
    "still get prompted to upgrade to the life time subscription at least once a day": "stop upsell / ads / push nagging",
    "extrem schlechten ki stimme gesprochen": "quality / higher-fidelity audio",
    "8d thing that isn’t even available in the premium": "more variety / more soundscapes & music",
    "sounds don’t stop even when you exit out": "playback controls (autoplay / background mode)",
    "wish it was more accessible for lower income people": "cheaper / pricing / free tier",
    "no way to make it stop playing automatically when i put my headphones on": "playback controls (autoplay / background mode)",
    "anti  tinitus szenario nicht mehr": "bugs/fixes (stability wishes)",
    "wish it was a monty subscription": "cheaper / pricing / free tier",
    "being charged, despite there being no indication or record of a subscription": "account / cancellation / restore",
    "should have done better connecting to apple pay": "account / cancellation / restore",
    "get an advertisement for the „upgrade to endel lifetime“": "stop upsell / ads / push nagging",
    "add the session to my google calendar": "integration: calendar / session stats",
    # ---------------- Brain.fm ----------------
    "replace my normal exercise playlist": "more variety / more soundscapes & music",
    "can’t wait for them to add more songs and genres": "more variety / more soundscapes & music",
    "this gets rid of my ocd": "DROP",
    "no option to provide fe": "more variety / more soundscapes & music",
    "app needs a bit of tweaking": "bugs/fixes (stability wishes)",
    "not knowing that i’d have to do a purchase option": "cheaper / pricing / free tier",
    "highly recommended it !": "DROP",
    "wish i discovered this years ago": "DROP",
    "only wish i had discovered it sooner": "DROP",
    "fluttery sound that is on almost every track": "quality / higher-fidelity audio",
    "wished for a superpower to tune out distractions": "DROP",
    "every time i try to log in, the app crashes": "bugs/fixes (stability wishes)",
    "no volume control in the app": "customization / mix-your-own / controls",
    "make it clear that it requires a subscription before you download": "cheaper / pricing / free tier",
    "playback error problem when i have a song saved in offline": "bugs/fixes (stability wishes)",
    "clicked wrong option on 1st screen": "customization / mix-your-own / controls",
    "loads and quits. i have been using my ipad instead": "bugs/fixes (stability wishes)",
    "developers decided to remove workout mode": "feature removed (bring back workout mode)",
    "hrv increased! physiologically balanced": "DROP",
    "way to have playlists in addition to the favorites library": "customization / mix-your-own / controls",
}

CLUSTER_CANON = {
    "account / subscription management / restore": "account / cancellation / restore",
    "visuals / UI / navigation / dark mode": "visuals / UI / navigation / simplicity",
    "sleep-specific features (smart alarm, tracking)": "sleep-specific features (smart alarm, wake-up)",
}

def main():
    reviews = classify.load()
    by_frag = {}
    used = set()
    for frag in OVERRIDES:
        hits = [r for r in reviews if frag in r["text"]]
        assert len(hits) == 1, f"fragment {frag!r} matched {len(hits)} reviews"
        by_frag[id(hits[0])] = OVERRIDES[frag]
        used.add(id(hits[0]))

    totals = Counter(r["app"] for r in reviews)
    final = defaultdict(Counter)
    n_wish = Counter()
    rows = []
    for r in reviews:
        has = any(t.search(r["text"]) for t in classify.TRIGGER_RES)
        if not has:
            continue
        c = by_frag.get(id(r), classify.wish_cluster(r["text"]))
        c = CLUSTER_CANON.get(c, c)
        if c == "DROP":
            continue
        if c == "other/uncategorized wish":
            c = "other/uncategorized"
        n_wish[r["app"]] += 1
        final[r["app"]][c] += 1
        rows.append({**r, "final_wish": c})

    for app in ["Endel", "Brain.fm"]:
        n = totals[app]
        print(f"\n=== {app} (n={n}; wish reviews after hand-check: {n_wish[app]}, {n_wish[app]/n*100:.1f}%) ===")
        for c, k in final[app].most_common():
            print(f"  {c:55s} {k:3d}  {k/n*100:4.1f}% of all")

    with open("wishes-final.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","app","storefront","rating","date","final_wish","title","content"])
        for r in rows:
            w.writerow([r["id"],r["app"],r["storefront"],r["rating"],r["date"],r["final_wish"],r["title"],r["content"]])
    print("\nWrote wishes-final.csv")

    # also dump final per-cluster quotes for the report
    out = defaultdict(lambda: defaultdict(list))
    for r in rows:
        out[r["app"]][r["final_wish"]].append(
            {"rating": r["rating"], "date": r["date"], "storefront": r["storefront"],
             "title": r["title"], "content": r["content"]})
    json.dump(out, open("wishes-final-samples.json","w"), indent=1, ensure_ascii=False)
    print("Wrote wishes-final-samples.json")

if __name__ == "__main__":
    main()
