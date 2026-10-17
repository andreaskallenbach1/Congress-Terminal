#!/usr/bin/env python3
"""After the fact-card makers: keep only cards whose quote is really in the source (FT 3, code).

Reads run/<id>/cards-<story>.json = [{"id","statement","quote","url","outlet","tier"}], drops cards whose quote is not
found in the page store, restores the quote's capitalisation, and writes run/<id>/cards-<story>.checked.json.
Usage: python3 pipeline/cards_check.py <run-id>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages  # noqa: E402

run = Path(__file__).resolve().parent.parent / "run" / sys.argv[1]
report = {}
for f in sorted(run.glob("cards-*.json")):
    if f.name.endswith(".checked.json"):
        continue
    cards = json.loads(f.read_text())
    kept = []
    for c in cards:
        if pages.find(c["url"], c["quote"]) == "FOUND":
            kept.append({**c, "quote": pages.cased_quote(c["url"], c["quote"])})
    f.with_name(f.stem + ".checked.json").write_text(json.dumps(kept, indent=1, ensure_ascii=False))
    report[f.stem] = f"{len(kept)}/{len(cards)}"
print(json.dumps(report))
