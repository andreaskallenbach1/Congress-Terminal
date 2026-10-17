#!/usr/bin/env python3
"""Stage 7: machine check of an edition before it is published (code, no AI).

Checks
  1. Votes equal the primary data collected in stage 0 (chamber, roll call, date, result, counts by party).
  2. Every evidence quote is found word for word in the text of its source (FT 3).
  3. Every core claim was confirmed by both fact-checkers (FT 2); a story whose core claim fails is invalid.
  4. Status rules: "verified" needs a primary source, "multiple reports" needs two independent outlets.
  5. Links answer, the edition is not marked as sample, word counts match the text.
The full structure is checked again by the site build (app/src/content.config.ts).

Usage: python3 pipeline/check_edition.py briefings/<id>.json run/<run-id>/inputs.json
Exit code 0 = publishable; 1 = problems (listed in run/<run-id>/check.json).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages  # noqa: E402  (page store: one fetch per source and day)

# Outlets that block direct fetches (CLAUDE.md): their quotes cannot be machine-checked, so their claims
# can at most be "multiple reports" backed by other outlets, never the only evidence.
UNFETCHABLE = ("apnews.com", "reuters.com", "c-span.org", "axios.com", "news.google.com", "punchbowl.news", "congress.gov/bill", "www.congress.gov")


def normalize(s: str) -> str:
    return pages.normalize(s)


def page_text(url: str) -> str | None:
    """Normalized page text from the page store (fetched once per day, shared by all stages)."""
    t = pages.text(url)
    return t.lower() if t is not None else None


def words(paragraphs: list[str]) -> int:
    return sum(len(re.sub(r"\[\[[a-z0-9-]+\]\]", "", p).split()) for p in paragraphs)


def main() -> int:
    edition_path, inputs_path = Path(sys.argv[1]), Path(sys.argv[2])
    ed = json.loads(edition_path.read_text())
    inputs = json.loads(inputs_path.read_text())
    problems: list[dict] = []
    warnings: list[str] = []

    def problem(where: str, msg: str, **extra):
        problems.append({"where": where, "problem": msg, **extra})

    if ed.get("sample"):
        problem("edition", "marked as sample")

    # 1. votes = primary data
    primary = {(v["chamber"], v["rollCall"]): v for v in inputs.get("senateVotes", []) + inputs.get("houseVotes", [])}
    for v in ed.get("floor", {}).get("votes", []):
        p = primary.get((v["chamber"], v["rollCall"]))
        if not p:
            problem(f"vote {v['chamber']} {v['rollCall']}", "not in the primary roll-call data of this run")
            continue
        for k in ("date", "result", "byParty"):
            if v.get(k) != p.get(k):
                problem(f"vote {v['chamber']} {v['rollCall']}", f"{k} differs from primary data", expected=p.get(k), found=v.get(k))

    sources = {s["id"]: s for s in ed.get("sources", [])}
    for st in ed.get("stories", []):
        sid = st["id"]
        claim_ids = {c["id"] for c in st["claims"]}
        text = st["whatsNew"] + st["whyItMatters"] + st["whatsNext"] + st.get("background", [])
        for ref in re.findall(r"\[\[([a-z0-9-]+)\]\]", " ".join(text), re.I):
            if ref not in claim_ids:
                problem(sid, f"marker [[{ref}]] has no claim")

        counted = words(st["whatsNew"] + st["whyItMatters"] + st["whatsNext"])
        if abs(counted - st["words"]) > max(40, 0.15 * counted):
            problem(sid, "word count does not match the text", stated=st["words"], counted=counted)

        weakest = "verified"
        for c in st["claims"]:
            cid = f"{sid}/{c['id']}"
            # 3. both checkers on core claims
            if c["weight"] == "core" and not (c.get("checkA") == "confirmed" and c.get("checkB") == "confirmed"):
                problem(cid, "core claim not confirmed by both fact-checkers: the story must be dropped or fixed")
            # 2. quotes found in source
            outlets = set()
            for e in c["evidence"]:
                src = sources.get(e["sourceId"])
                if not src:
                    problem(cid, f"unknown source id {e['sourceId']}")
                    continue
                outlets.add(src["name"])
                if any(u in e["url"] for u in UNFETCHABLE):
                    warnings.append(f"{cid}: quote not machine-checkable ({src['name']} blocks direct fetches)")
                    continue
                txt = page_text(e["url"])
                if txt is None:
                    problem(cid, "source could not be fetched to check the quote", url=e["url"])
                elif normalize(e["quote"]) not in txt:
                    problem(cid, "quote not found in source text", url=e["url"], quote=e["quote"][:160])
            # 4. status rules
            tiers = {sources[e["sourceId"]]["tier"] for e in c["evidence"] if e["sourceId"] in sources}
            # A forecaster's own page is the primary source for its own rating, if the claim names it ("Cook rates …").
            own_rating = any(
                sources[e["sourceId"]]["tier"] == "elections"
                and sources[e["sourceId"]]["name"].split()[0].lower() in c["text"].lower()
                for e in c["evidence"] if e["sourceId"] in sources
            )
            if c["status"] == "verified" and "primary" not in tiers and c["origin"] != "code" and not own_rating:
                problem(cid, "'verified' requires a primary source")
            if c["status"] == "multiple" and len(outlets - {s["name"] for s in sources.values() if s["tier"].startswith("partisan")}) < 2:
                problem(cid, "'multiple reports' requires two independent non-partisan outlets")
            if tiers and tiers <= {"partisan-left", "partisan-right"} and c["weight"] == "core":
                problem(cid, "partisan outlets may not establish facts")
            if c["weight"] == "core":
                order = ["verified", "multiple", "unconfirmed"]
                weakest = max(weakest, c["status"], key=order.index)
        if st["status"] != weakest:
            problem(sid, f"story status should be '{weakest}' (weakest core claim)", found=st["status"])

    # 5. links answer
    for s in ed.get("sources", []):
        if any(u in s["url"] for u in UNFETCHABLE):
            continue
        if page_text(s["url"]) is None:
            problem(f"source {s['id']}", "link does not answer", url=s["url"])

    report = {"edition": ed.get("id"), "publishable": not problems, "problems": problems, "warnings": warnings}
    out = inputs_path.parent / "check.json"
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print(json.dumps({"publishable": report["publishable"], "problems": len(problems), "warnings": len(warnings), "report": str(out)}))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
