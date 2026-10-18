#!/usr/bin/env python3
"""After the collectors: merge their leads into the gated inputs for the story builder (code).

Each collector writes run/<id>/leads-<area>.json = [{"title","url","outlet","tier","why"}] (at most 8). Leads whose URL
is already among the items are merged into that item; new ones become items with "collector": <area>.
Usage: python3 pipeline/leads.py <run-id>
"""
import json
import sys
from pathlib import Path

run = Path(__file__).resolve().parent.parent / "run" / sys.argv[1]
view = json.loads((run / "inputs-gated.json").read_text())
known = {link["url"] for g in view["items"] for link in g["links"]}
n = max((g["n"] for g in view["items"]), default=0) + 1000
added = {}
for f in sorted(run.glob("leads-*.json")):
    area = f.stem.removeprefix("leads-")
    leads = json.loads(f.read_text())[:8]
    added[area] = 0
    for lead in leads:
        if not lead.get("url") or lead["url"] in known:
            continue
        view["items"].append({"n": n, "title": lead["title"], "summary": (lead.get("why") or "")[:160], "published": None,
                              "links": [{"outlet": lead.get("outlet"), "tier": lead.get("tier"), "url": lead["url"]}],
                              "collector": area})
        known.add(lead["url"])
        n += 1
        added[area] += 1
(run / "inputs-gated.json").write_text(json.dumps(view, ensure_ascii=False, separators=(",", ":")))
print(json.dumps({"added": added, "items": len(view["items"])}))
