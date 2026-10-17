#!/usr/bin/env python3
"""Between stage 4 and the fact-checkers: merge the writers' drafts into one edition draft (code, no AI).

- Joins run/<id>/draft-*.json (stories, sources, agenda, today) into run/<id>/edition-draft.json.
- Restores the original capitalisation of every evidence quote from the source page, so readers see the quote
  as published (writers may have copied it from lower-cased, normalised text).
- Copies votes from inputs.json unchanged (hard facts from primary data).

Usage: python3 pipeline/merge_drafts.py <run-id>
"""
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect import get  # noqa: E402
from check_edition import normalize  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
_raw: dict[str, str | None] = {}


def readable(url: str) -> str | None:
    """Page text with the same cleaning as normalize(), but keeping case."""
    if url not in _raw:
        data = get(url, timeout=30)
        if data is None:
            _raw[url] = None
        else:
            t = data.decode("utf-8", errors="ignore")
            t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
            t = unicodedata.normalize("NFKC", html.unescape(re.sub(r"<[^>]+>", " ", t)))
            t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
            t = t.replace("–", "-").replace("—", "-").replace(" ", " ")
            _raw[url] = re.sub(r"\s+", " ", t).strip()
    return _raw[url]


def restore_case(quote: str, url: str) -> str:
    text = readable(url)
    if not text:
        return quote
    i = text.lower().find(normalize(quote))
    return text[i:i + len(normalize(quote))] if i >= 0 else quote


def main() -> None:
    run_id = sys.argv[1]
    run = ROOT / "run" / run_id
    stories, sources, agenda, today, dropped = [], {}, [], [], []
    for f in sorted(run.glob("draft-*.json")):
        d = json.loads(f.read_text())
        stories += d.get("stories", [])
        for s in d.get("sources", []):
            sources[s["id"]] = s
        agenda += d.get("agenda", [])
        today += d.get("today", [])
        dropped += d.get("dropped", [])
    restored = 0
    for st in stories:
        for c in st["claims"]:
            for e in c["evidence"]:
                if e["quote"] == e["quote"].lower():
                    new = restore_case(e["quote"], e["url"])
                    restored += new != e["quote"]
                    e["quote"] = new
    inputs = json.loads((run / "inputs.json").read_text())
    draft = {
        "stories": stories,
        "sources": list(sources.values()),
        "agenda": sorted(agenda, key=lambda a: a["date"]),
        "today": today,
        "floorVotes": inputs.get("senateVotes", []) + inputs.get("houseVotes", []),
        "dropped": dropped,
    }
    (run / "edition-draft.json").write_text(json.dumps(draft, indent=1, ensure_ascii=False))
    claims = sum(len(s["claims"]) for s in stories)
    core = sum(1 for s in stories for c in s["claims"] if c["weight"] == "core")
    print(json.dumps({"stories": len(stories), "claims": claims, "coreClaims": core, "sources": len(sources), "quotesRecased": restored}))


if __name__ == "__main__":
    main()
