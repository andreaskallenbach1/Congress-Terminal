#!/usr/bin/env python3
"""Before checker A: one packet with everything A needs per claim, so A rarely has to open a page (saving measure).

Measured 18.10.2026: checker A spent 29 tool calls mostly reading pages to see the context around each quote. Code
cuts that context out of the page store instead. Per claim: text, status, weight, the story sentences that carry its
marker, and per evidence quote the source (name, tier) plus the surrounding text of the page (CONTEXT chars on each
side). The story's headline and dek are listed once per story, because they must be covered by the claims too.

Usage: python3 pipeline/packets.py <run-id> [--ids recheck-ids.json]   → run/<id>/packet-checkA.json
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages  # noqa: E402

CONTEXT = 200
ROOT = Path(__file__).resolve().parent.parent


def context(url: str, quote: str) -> str | None:
    t = pages.text(url)
    if not t:
        return None
    i = t.lower().find(pages.normalize(quote))
    if i < 0:
        return None
    a, b = max(0, i - CONTEXT), min(len(t), i + len(pages.normalize(quote)) + CONTEXT)
    return ("…" if a else "") + t[a:b] + ("…" if b < len(t) else "")


def sentences_with(marker: str, story: dict) -> list[str]:
    out = []
    for part in ("whatsNew", "whyItMatters", "whatsNext", "background"):
        for para in story.get(part) or []:
            for s in re.split(r"(?<=\]\])\s+", para):          # a sentence ends with its marker(s)
                if f"[[{marker}]]" in s:
                    out.append(f"{part}: {s.strip()}")
    return out


def main() -> None:
    run = ROOT / "run" / sys.argv[1]
    only = None
    if "--ids" in sys.argv:
        only = {(x["story"], x["claim"]) for x in json.loads((run / sys.argv[sys.argv.index("--ids") + 1]).read_text())}
    draft = json.loads((run / "edition-draft.json").read_text())
    sources = {s["id"]: s for s in draft["sources"]}
    packet = {"stories": [], "claims": []}
    for st in draft["stories"]:
        packet["stories"].append({"story": st["id"], "headline": st["headline"], "dek": st["dek"]})
        for c in st["claims"]:
            if only and (st["id"], c["id"]) not in only:
                continue
            packet["claims"].append({
                "story": st["id"], "claim": c["id"], "text": c["text"], "status": c["status"], "weight": c["weight"],
                "sentences": sentences_with(c["id"], st),
                "evidence": [{
                    "source": sources.get(e["sourceId"], {}).get("name"), "tier": sources.get(e["sourceId"], {}).get("tier"),
                    "url": e["url"], "quote": e["quote"], "context": context(e["url"], e["quote"]),
                } for e in c["evidence"]],
            })
    name = "packet-checkA-recheck.json" if only else "packet-checkA.json"
    (run / name).write_text(json.dumps(packet, indent=1, ensure_ascii=False))  # short lines: readable in parts
    missing = sum(e["context"] is None for c in packet["claims"] for e in c["evidence"])
    print(json.dumps({"packet": name, "claims": len(packet["claims"]), "withoutContext": missing}))


if __name__ == "__main__":
    main()
