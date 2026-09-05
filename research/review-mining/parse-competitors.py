#!/usr/bin/env python3
"""Parse raw iTunes RSS customer-review pulls into the same schema as
parsed-endel-us.json etc: [{date, rating, title, content}, ...].

Input : reviews-<app>-<sf>-p<N>.json  (raw, untouched)
Output: parsed-<app>-<sf>.json
"""
import json, glob, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
APPS = ["focusatwill", "mynoise", "noisli", "portal", "mubert", "darknoise"]

def entries(path):
    try:
        d = json.load(open(path))
    except Exception:
        return []
    e = d.get("feed", {}).get("entry", [])
    if isinstance(e, dict):
        e = [e]
    return [x for x in e if "im:rating" in x]

def main():
    summary = []
    for app in APPS:
        for sf in ("us", "de"):
            rows, seen = [], set()
            pages = sorted(glob.glob(f"{D}/reviews-{app}-{sf}-p*.json"),
                           key=lambda p: int(re.search(r"-p(\d+)\.json$", p).group(1)))
            for p in pages:
                for e in entries(p):
                    r = {
                        "date": e["updated"]["label"],
                        "rating": e["im:rating"]["label"],
                        "title": e["title"]["label"],
                        "content": e["content"]["label"],
                    }
                    k = (r["date"], r["title"], r["content"])
                    if k in seen:
                        continue
                    seen.add(k)
                    rows.append(r)
            out = f"{D}/parsed-{app}-{sf}.json"
            json.dump(rows, open(out, "w"), ensure_ascii=False, indent=1)
            dates = sorted(r["date"][:10] for r in rows)
            summary.append((app, sf, len(rows), dates[0] if dates else "-", dates[-1] if dates else "-"))
    for s in summary:
        print(f"{s[0]:12s} {s[1]} n={s[2]:4d}  {s[3]} -> {s[4]}")

if __name__ == "__main__":
    main()
