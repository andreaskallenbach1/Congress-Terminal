#!/usr/bin/env python3
"""Calendar and "today" notes when no floor story is written (code, no AI).

The floor writer normally adds `agenda` and `today`. On recess days the arbiter may choose no floor story; then this
step carries the previous edition's agenda items that are still ahead (within 7 days), adds committee meetings from
inputs.json, and writes plain factual notes: no roll-call votes since the last edition, and primary sources that
failed during collection. Writes run/<id>/draft-agenda.json (merged by merge_drafts.py like a writer's draft).

Usage: python3 pipeline/agenda.py <run-id>
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILED_PRIMARY = {
    "federalregister.gov": "The Federal Register API refused requests this morning, so new arms-sales notices could not be checked.",
}


def main() -> None:
    run_id = sys.argv[1]
    run = ROOT / "run" / run_id
    inputs = json.loads((run / "inputs.json").read_text())
    start = date.fromisoformat(run_id[:10])
    end = start + timedelta(days=7)

    agenda: dict[tuple, dict] = {}
    prev = ROOT / "briefings" / f"{inputs.get('previousEdition')}.json"
    if prev.exists():
        for a in json.loads(prev.read_text()).get("agenda", []):
            if start <= date.fromisoformat(a["date"][:10]) <= end:
                agenda[(a["date"][:10], a.get("url"), a["title"])] = a
    for m in inputs.get("committeeMeetings", []):
        d = m["date"][:10]
        if not start <= date.fromisoformat(d) <= end or any(k[1] == m["url"] for k in agenda):
            continue
        agenda[(d, m["url"], m["title"])] = {
            "date": d, "chamber": m["chamber"].lower(), "kind": "markup" if m["type"] == "Markup" else "hearing",
            "title": m["title"], "committee": ", ".join(m.get("committees", [])), "url": m["url"],
        }

    today = []
    if not inputs.get("senateVotes") and not inputs.get("houseVotes"):
        today.append("Neither chamber held a roll-call vote since the last edition.")
    failed = [line for line in inputs.get("log", []) if line.startswith(("HTTP 4", "HTTP 5", "ERR"))]
    today += [note for host, note in FAILED_PRIMARY.items() if any(host in line for line in failed)]

    out = {"stories": [], "sources": [], "dropped": [], "agenda": sorted(agenda.values(), key=lambda a: a["date"]), "today": today}
    (run / "draft-agenda.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({"agenda": len(out["agenda"]), "today": len(today)}))


if __name__ == "__main__":
    main()
