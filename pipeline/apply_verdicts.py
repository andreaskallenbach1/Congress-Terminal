#!/usr/bin/env python3
"""After the fact-checkers: write checkA/checkB into the edition draft and list what needs a revision (R3).

Decision rule (CLAUDE.md 7): both confirm → keep · one rejects → one revision, then both check again ·
both reject → claim removed · a removed core claim → story dropped (FT 2).
Core claims must be at least "multiple" (Andreas' decision 18.10.2026): an unconfirmed core claim goes to R3 like a
rejected one (find a primary source or a second independent outlet).

After R3 (re-check files present) the fixed rule applies, by code: a story whose core claim is not confirmed by both
checkers, or is still unconfirmed, leaves the draft and is listed in demoted.json (the editor may give it an attributed
one-line Also Notable item); a minor claim that is still rejected is removed together with the sentence carrying it.
Usage: python3 pipeline/apply_verdicts.py <run-id>
"""
import json
import re
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

final = (run / "checkA-recheck.json").exists()
revise, remove, demoted = [], [], []
for st in list(draft["stories"]):
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
        weak_core = c["weight"] == "core" and c["status"] == "unconfirmed"
        if final:
            if c["weight"] == "core" and (rejected or None in verdicts or weak_core):
                why = f"core claim {c['id']} " + ("still unconfirmed" if weak_core else "not confirmed by both checkers")
                entry = next((d for d in demoted if d["story"] == st["id"]), None)
                if entry:
                    entry["reasons"].append(why)
                else:
                    ev = next(e for x in st["claims"] if x["weight"] == "core" for e in x["evidence"])
                    src = next((x for x in draft["sources"] if x["id"] == ev["sourceId"]), {})
                    demoted.append({"story": st["id"], "headline": st["headline"], "dek": st["dek"], "reasons": [why],
                                    "outlet": src.get("name", ""), "url": ev["url"]})
            elif rejected:
                remove.append({"story": st["id"], "claim": c["id"], "weight": c["weight"]})
        elif c["weight"] == "core" and len(rejected) == 2:
            remove.append({"story": st["id"], "claim": c["id"], "weight": c["weight"]})
        elif rejected or None in verdicts or weak_core:
            revise.append({
                "story": st["id"], "claim": c["id"], "weight": c["weight"], "text": c["text"], "status": c["status"],
                "checkA": a and {k2: a.get(k2) for k2 in ("verdict", "reason", "fix")},
                "checkB": b and {k2: b.get(k2) for k2 in ("verdict", "reason")},
                **({"rule": "core claim unconfirmed: add a primary source or a second independent outlet"} if weak_core else {}),
            })


def drop_claim(st: dict, cid: str) -> None:
    """Remove a claim and every sentence that carries its marker (a sentence ends with its marker or markers)."""
    st["claims"] = [c for c in st["claims"] if c["id"] != cid]
    for part in ("whatsNew", "whyItMatters", "whatsNext", "background"):
        if st.get(part):
            paras = [" ".join(x for x in re.split(r"(?<=\]\])\s+", p) if f"[[{cid}]]" not in x) for p in st[part]]
            st[part] = [p for p in paras if p.strip()]


if final:
    gone = {d["story"] for d in demoted}
    draft["stories"] = [st for st in draft["stories"] if st["id"] not in gone]
    for r in remove:
        for st in draft["stories"]:
            if st["id"] == r["story"]:
                drop_claim(st, r["claim"])
    (run / "demoted.json").write_text(json.dumps(demoted, indent=1, ensure_ascii=False))
(run / "edition-draft.json").write_text(json.dumps(draft, indent=1, ensure_ascii=False))
(run / "revise.json").write_text(json.dumps({"revise": revise, "removeBothRejected": remove}, indent=1, ensure_ascii=False))
print(json.dumps({"final": final, "revise": len(revise), "removed": remove, "demoted": [d["story"] for d in demoted],
                  "reviseCore": sum(r["weight"] == "core" for r in revise)}))
