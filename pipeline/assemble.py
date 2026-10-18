#!/usr/bin/env python3
"""Saving measure 4: code assembles the edition; the editor-in-chief only supplies judgements.

Inputs in run/<id>/:
  edition-draft.json  fact-checked stories, sources, agenda, today (after precheck and the checkers)
  editor.json         the editor's choices: {"ranks": {storyId: rank}, "votes": ["senate:256", ...],
                      "floorSummary": str|null, "overnight": [...], "notable": [...], "watch": [...], "hero": {...}}
  inputs.json         primary data: roll calls and arms-sales notices are copied from here unchanged
  process-facts.json  counts of this run (optional)
Output: briefings/<id>.json (schema in app/src/content.config.ts). Unknown keys are dropped, reading time is computed.

Usage: python3 pipeline/assemble.py <run-id> [--kind weekly]
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORY_KEYS = {"id", "pillar", "continuing", "headline", "dek", "whatsNew", "whyItMatters", "whatsNext", "background",
              "words", "readingMinutes", "status", "claims", "image", "members", "bill", "race", "countries", "relevance"}
CLAIM_KEYS = {"id", "text", "weight", "status", "origin", "evidence", "checkA", "checkB"}
SOURCE_KEYS = {"id", "name", "tier", "url", "retrievedAt"}
AGENDA_KEYS = {"date", "time", "chamber", "kind", "title", "committee", "url"}
VALUE = re.compile(r"\$\s?([\d.,]+)\s*(billion|million)", re.I)


def usd(text: str | None) -> float | None:
    m = VALUE.search(text or "")
    if not m:
        return None
    return float(m.group(1).replace(",", "")) * (1e9 if m.group(2).lower() == "billion" else 1e6)


def main() -> None:
    run_id = sys.argv[1]
    kind = "weekly" if "--kind" in sys.argv and sys.argv[sys.argv.index("--kind") + 1] == "weekly" else "daily"
    run = ROOT / "run" / run_id
    draft = json.loads((run / "edition-draft.json").read_text())
    editor = json.loads((run / "editor.json").read_text())
    inputs = json.loads((run / "inputs.json").read_text())
    facts = json.loads((run / "process-facts.json").read_text()) if (run / "process-facts.json").exists() else {}

    stories = []
    for st in draft["stories"]:
        st = {k: v for k, v in st.items() if k in STORY_KEYS}
        st["claims"] = [{k: v for k, v in c.items() if k in CLAIM_KEYS and v is not None} for c in st["claims"]]
        if st["id"] in editor.get("ranks", {}):
            st["relevance"]["rank"] = editor["ranks"][st["id"]]
        stories.append(st)

    used = {e["sourceId"] for s in stories for c in s["claims"] for e in c["evidence"]}
    sources = [{k: v for k, v in s.items() if k in SOURCE_KEYS} for s in draft["sources"] if s["id"] in used]

    primary = {f"{v['chamber']}:{v['rollCall']}": v for v in inputs.get("senateVotes", []) + inputs.get("houseVotes", [])}
    votes = [{k: primary[key][k] for k in ("chamber", "rollCall", "date", "question", "description", "result", "byParty", "sourceUrl")}
             for key in editor.get("votes", []) if key in primary]

    arms = [{"purchaser": a["purchaser"].replace("Government of ", ""), "system": a.get("system") or a.get("title") or "See notice",
             "valueUSD": usd(a.get("value")), "date": a["date"], "url": a["textUrl"]}
            for a in inputs.get("armsSales", []) if a.get("purchaser") and usd(a.get("value"))]

    watch_minutes = sum(c.get("minutes", 2) for c in editor.get("watch", []))
    clips = [{k: v for k, v in c.items() if k != "minutes"} for c in editor.get("watch", [])]
    notable = editor.get("notable", [])
    reading = round(sum(s["readingMinutes"] for s in stories) + watch_minutes + (2 if notable else 0), 1)

    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=2)))
    edition = {
        "schemaVersion": 1,
        "id": run_id,
        "kind": kind,
        "date": run_id[:10],
        "compiledAt": now.isoformat(timespec="seconds"),
        "readingMinutes": reading,
        # the app labels symbolic images itself, so a label in the editor's caption would appear twice
        **({"hero": {**editor["hero"], "caption": re.sub(r"\s*\(symbolic image\)\.?\s*$", "", editor["hero"]["caption"], flags=re.I)}}
           if editor.get("hero") else {}),
        "stories": stories,
        "floor": {"votes": votes, **({"summary": editor["floorSummary"]} if editor.get("floorSummary") else {})},
        "agenda": [{k: v for k, v in a.items() if k in AGENDA_KEYS} for a in draft.get("agenda", [])],
        "overnight": editor.get("overnight", []),
        "today": draft.get("today", []),
        "armsSales": arms,
        "watch": clips,
        "notable": notable,
        "sources": sources,
        "process": {
            "sourcesChecked": facts.get("sourcesChecked", len(sources)),
            "claimsChecked": sum(1 for s in stories for c in s["claims"] if c["weight"] == "core"),
            "objections": facts.get("objections", 0),
            "objectionsAccepted": facts.get("objectionsAccepted", 0),
        },
    }
    out = ROOT / "briefings" / f"{run_id}.json"
    out.write_text(json.dumps(edition, indent=1, ensure_ascii=False))
    print(json.dumps({"edition": str(out.relative_to(ROOT)), "stories": len(stories), "votes": len(votes),
                      "armsSales": len(arms), "readingMinutes": reading}))


if __name__ == "__main__":
    main()
