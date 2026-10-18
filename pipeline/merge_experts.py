#!/usr/bin/env python3
"""After the experts (procedure explainer, historian): add their background paragraphs to the edition draft (code).

Each expert writes run/<id>/expert-<role>.json =
  {"stories": {storyId: {"background": ["paragraph with [[h1]] markers", ...], "claims": [claim, ...]}},
   "sources": [source, ...]}
Claim ids must carry the expert's prefix (historian "h", procedure explainer "p") so they never collide with the
writers' "c" ids; all expert claims are minor. Paragraphs are appended to the story's `background`, claims and sources
are added (sources deduplicated by id). Run precheck.py afterwards.

Usage: python3 pipeline/merge_experts.py <run-id>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREFIX = {"historian": "h", "procedure": "p"}


def main() -> None:
    run = ROOT / "run" / sys.argv[1]
    draft_path = run / "edition-draft.json"
    draft = json.loads(draft_path.read_text())
    stories = {s["id"]: s for s in draft["stories"]}
    source_ids = {s["id"] for s in draft["sources"]}
    report = {}
    for f in sorted(run.glob("expert-*.json")):
        role = f.stem.removeprefix("expert-")
        prefix = PREFIX.get(role)
        exp = json.loads(f.read_text())
        added = 0
        for sid, part in exp.get("stories", {}).items():
            st = stories.get(sid)
            if not st or not prefix:
                continue
            claims = [c for c in part.get("claims", []) if re.fullmatch(rf"{prefix}\d+", c["id"])]
            ids = {c["id"] for c in claims}
            existing = {c["id"] for c in st["claims"]}
            # keep only paragraphs whose markers all refer to this expert's claims
            paras = [p for p in part.get("background", [])
                     if all(m in ids for m in re.findall(r"\[\[(\w+)\]\]", p)) and re.search(r"\[\[\w+\]\]", p)]
            used = {m for p in paras for m in re.findall(r"\[\[(\w+)\]\]", p)}
            new_claims = [{**c, "weight": "minor"} for c in claims if c["id"] in used and c["id"] not in existing]
            if not paras:
                continue
            st["background"] = (st.get("background") or []) + paras
            st["claims"] += new_claims
            added += len(new_claims)
        for src in exp.get("sources", []):
            if src["id"] not in source_ids:
                draft["sources"].append(src)
                source_ids.add(src["id"])
        report[role] = added
    draft_path.write_text(json.dumps(draft, indent=1, ensure_ascii=False))
    print(json.dumps({"claimsAdded": report}))


if __name__ == "__main__":
    main()
