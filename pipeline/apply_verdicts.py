#!/usr/bin/env python3
"""After the fact-checkers: write checkA/checkB into the edition draft and list what needs a revision (R3).

Decision rule (CLAUDE.md 7): both confirm → keep · one rejects → one revision, then both check again ·
both reject → claim removed · a removed core claim → story dropped (FT 2).
Usage: python3 pipeline/apply_verdicts.py <run-id>
"""
import json
import sys
from pathlib import Path

run = Path(__file__).resolve().parent.parent / "run" / sys.argv[1]
draft = json.loads((run / "edition-draft.json").read_text())
verdicts_a, verdicts_b = {}, {}
# After R3, checkA-recheck.json / checkB-recheck.json hold the second verdicts on revised claims; they are read last
# and replace the first verdicts.
for f in sorted(run.glob("checkA-*.json"), key=lambda f: f.name == "checkA-recheck.json"):
    for v in json.loads(f.read_text()):
        verdicts_a[(v["story"], v["claim"])] = v
for f in [run / "checkB.json", run / "checkB-recheck.json"]:
    for v in json.loads(f.read_text()) if f.exists() else []:
        verdicts_b[(v["story"], v["claim"])] = v

revise, remove = [], []
for st in draft["stories"]:
    for c in st["claims"]:
        k = (st["id"], c["id"])
        a, b = verdicts_a.get(k), verdicts_b.get(k)
        c["checkA"] = a["verdict"] if a else None
        # B checks core claims only (lean run); minor claims rest on A plus the machine check, so they carry no checkB.
        c.pop("checkB", None)
        if c["weight"] == "core":
            c["checkB"] = b["verdict"] if b else None
        verdicts = [c["checkA"]] + ([c["checkB"]] if c["weight"] == "core" else [])
        rejected = [x for x in verdicts if x == "rejected"]
        if c["weight"] == "core" and len(rejected) == 2:
            remove.append({"story": st["id"], "claim": c["id"], "weight": c["weight"]})
        elif rejected or None in verdicts:
            revise.append({
                "story": st["id"], "claim": c["id"], "weight": c["weight"], "text": c["text"], "status": c["status"],
                "checkA": a and {k2: a.get(k2) for k2 in ("verdict", "reason", "fix")},
                "checkB": b and {k2: b.get(k2) for k2 in ("verdict", "reason")},
            })
(run / "edition-draft.json").write_text(json.dumps(draft, indent=1, ensure_ascii=False))
(run / "revise.json").write_text(json.dumps({"revise": revise, "removeBothRejected": remove}, indent=1, ensure_ascii=False))
print(json.dumps({"revise": len(revise), "removeBothRejected": remove, "reviseCore": sum(r["weight"] == "core" for r in revise)}))
