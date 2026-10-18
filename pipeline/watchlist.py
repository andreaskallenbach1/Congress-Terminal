#!/usr/bin/env python3
"""Watchlist (FT 5) — code, no AI: every bill the briefing has covered, refreshed from Congress.gov on every run.

Stages come from the Library of Congress action codes in the bill's actions (introduced, reported, passed each
chamber, presented, signed or vetoed), so they are hard facts. Steps outside Congress that a story reported (an
executive waiver, marked `setback` with key "waived") are carried over from the latest story.

Writes data/watchlist.json. Usage: python3 pipeline/watchlist.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect import BILL_PATH, get_json  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CODES = {  # LoC action code → (stage key, label)
    "Intro-H": ("introduced", "Introduced in House"), "Intro-S": ("introduced", "Introduced in Senate"),
    "1000": ("introduced", "Introduced in House"), "10000": ("introduced", "Introduced in Senate"),
    "5000": ("committee", "Reported by House committee"), "14000": ("committee", "Reported by Senate committee"),
    "8000": ("passed-house", "Passed House"), "17000": ("passed-senate", "Passed Senate"),
    "28000": ("to-president", "Presented to President"), "36000": ("signed", "Became law"),
    "31000": ("vetoed", "Vetoed"),
}
ORDER = ["introduced", "committee", "passed-house", "passed-senate", "to-president", "signed", "vetoed"]


def parse(number: str):
    m = re.match(r"^\s*(H\.?\s?R|S|H\.?\s?Res|S\.?\s?Res|H\.?\s?J\.?\s?Res|S\.?\s?J\.?\s?Res|H\.?\s?Con\.?\s?Res|S\.?\s?Con\.?\s?Res)\.?\s*(\d+)\s*$", number, re.I)
    if not m:
        return None
    t = re.sub(r"[^a-z]", "", m.group(1).lower())
    return t, m.group(2)


def stages_for(congress: int, t: str, n: str) -> tuple[list, dict | None, str | None]:
    data = get_json(f"https://api.congress.gov/v3/bill/{congress}/{t}/{n}/actions?format=json&limit=250")
    if not data:
        return [], None, None
    seen: dict[str, dict] = {}
    for a in sorted(data.get("actions", []), key=lambda a: a["actionDate"]):
        code = str(a.get("actionCode") or "")
        if code in CODES and CODES[code][0] not in seen:
            key, label = CODES[code]
            seen[key] = {"key": key, "label": label, "date": a["actionDate"], "done": True, "setback": key == "vetoed"}
        elif "introduced" not in seen and a.get("type") == "IntroReferral":
            seen["introduced"] = {"key": "introduced", "label": "Introduced", "date": a["actionDate"], "done": True, "setback": False}
        failed = re.match(r"Failed (?:of passage )?in (Senate|House)", a.get("text", ""))
        if failed and "failed" not in seen:
            seen["failed"] = {"key": "other", "label": f"Failed in {failed.group(1)}", "date": a["actionDate"], "done": True, "setback": True}
    acts = data.get("actions", [])
    latest = max(acts, key=lambda a: a["actionDate"]) if acts else None
    title = get_json(f"https://api.congress.gov/v3/bill/{congress}/{t}/{n}?format=json")
    return sorted(seen.values(), key=lambda s: (s["date"], ORDER.index(s["key"]) if s["key"] in ORDER else 99)), latest, (title or {}).get("bill", {}).get("title")


def main() -> None:
    editions = sorted((json.loads(p.read_text()) for p in (ROOT / "briefings").glob("*.json")), key=lambda e: e["compiledAt"])
    tracked: dict[str, dict] = {}
    for e in editions:                                   # oldest first, so the latest story wins
        for st in e["stories"]:
            if st.get("bill"):
                tracked[st["bill"]["number"]] = {"story": st["id"], "edition": e["id"], "bill": st["bill"]}
    out = []
    for number, ref in tracked.items():
        parsed = parse(number)
        if not parsed:
            continue
        t, n = parsed
        stages, latest, title = stages_for(119, t, n)
        # Only executive steps outside Congress are carried over from the story (e.g. a waiver); everything else is API data.
        extra = [s for s in ref["bill"]["stages"] if s.get("setback") and s["key"] == "waived"]
        out.append({
            "number": number,
            "title": title or ref["bill"]["title"],
            "congressGovUrl": f"https://www.congress.gov/bill/119th-congress/{BILL_PATH.get(t.upper(), 'bill')}/{n}",
            "stages": stages + extra,
            "latestAction": {"date": latest["actionDate"], "text": latest["text"]} if latest else None,
            "story": ref["story"],
            "edition": ref["edition"],
        })
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "watchlist.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({"bills": len(out)}))


if __name__ == "__main__":
    main()
