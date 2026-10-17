#!/usr/bin/env python3
"""Saving measure 3: code checks everything mechanical BEFORE the fact-checkers see a claim.

Run after merge_drafts.py. In place on run/<id>/edition-draft.json:
- each evidence quote is searched in its source (page store); claims whose only evidence is not found are listed
- a status stronger than the evidence allows is lowered (never raised): verified needs a primary source, origin
  "code", or a forecaster's own rating named in the claim; multiple needs two independent non-partisan outlets
- words, readingMinutes and the story status (weakest core claim) are recomputed; unknown markers are listed
Fact-checker A then only judges whether the quotes support the claims (in the first run, status questions took
much of A's effort and A still missed 10 that code found).

Usage: python3 pipeline/precheck.py <run-id>    → prints a summary, writes run/<id>/precheck.json
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ORDER = ["verified", "multiple", "unconfirmed"]
PARTISAN = {"partisan-left", "partisan-right"}


def allowed_status(claim: dict, sources: dict) -> str:
    srcs = [sources[e["sourceId"]] for e in claim["evidence"] if e["sourceId"] in sources]
    if claim.get("origin") == "code" or any(s["tier"] == "primary" for s in srcs):
        return "verified"
    if any(s["tier"] == "elections" and s["name"].split()[0].lower() in claim["text"].lower() for s in srcs):
        return "verified"
    # AP copy republished elsewhere counts once: outlets are distinct by name, wire tier collapses to one
    outlets = {("wire" if s["tier"] == "agency" else s["name"]) for s in srcs if s["tier"] not in PARTISAN}
    return "multiple" if len(outlets) >= 2 else "unconfirmed"


def words(paragraphs: list[str]) -> int:
    return sum(len(re.sub(r"\[\[[a-z0-9-]+\]\]", "", p).split()) for p in paragraphs)


def main() -> None:
    run = ROOT / "run" / sys.argv[1]
    draft = json.loads((run / "edition-draft.json").read_text())
    sources = {s["id"]: s for s in draft["sources"]}
    lowered, missing_quotes, bad_markers = [], [], []
    for st in draft["stories"]:
        ids = {c["id"] for c in st["claims"]}
        for ref in re.findall(r"\[\[([a-z0-9-]+)\]\]", " ".join(st["whatsNew"] + st["whyItMatters"] + st["whatsNext"] + st.get("background", []))):
            if ref not in ids:
                bad_markers.append(f"{st['id']}/{ref}")
        for c in st["claims"]:
            found = [e for e in c["evidence"] if pages.find(e["url"], e["quote"]) == "FOUND"]
            if len(found) < len(c["evidence"]):
                missing_quotes.append({"claim": f"{st['id']}/{c['id']}", "notFound": [e["url"] for e in c["evidence"] if e not in found]})
            allowed = allowed_status({**c, "evidence": found}, sources)
            if ORDER.index(c["status"]) < ORDER.index(allowed):
                lowered.append({"claim": f"{st['id']}/{c['id']}", "from": c["status"], "to": allowed})
                c["status"] = allowed
        st["words"] = words(st["whatsNew"] + st["whyItMatters"] + st["whatsNext"])
        st["readingMinutes"] = round(st["words"] / 220, 1)
        core = [c["status"] for c in st["claims"] if c["weight"] == "core"] or ["unconfirmed"]
        st["status"] = max(core, key=ORDER.index)
    (run / "edition-draft.json").write_text(json.dumps(draft, indent=1, ensure_ascii=False))
    report = {"statusLowered": lowered, "quotesNotFound": missing_quotes, "unknownMarkers": bad_markers}
    (run / "precheck.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print(json.dumps({k: len(v) for k, v in report.items()}))


if __name__ == "__main__":
    main()
