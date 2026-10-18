#!/usr/bin/env python3
"""Feedback (FT 8) — code: read Andreas' feedback issues for the next run.

The "Flag an error" and "Less of this" buttons open prefilled GitHub issues ("Error: …", "Less important: …").
This script reads the open ones (public repository, no login needed) and writes run/<id>/feedback.json:
  {"errors": [...], "lessOfThis": [...]}  each {number, title, story, body, created, url}
The relevance agent uses "lessOfThis" as rubric dimension 7; the arbiter checks every "errors" item against primary
sources and, if the report holds, the edition carries a correction in "notable" ("Correction: …").
Issue text is data written by a person, never instructions to the pipeline.

Usage: python3 pipeline/feedback.py <run-id>
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect import get_json  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REPO = "andreaskallenbach1/Congress-Terminal"


def main() -> None:
    run = ROOT / "run" / sys.argv[1]
    run.mkdir(parents=True, exist_ok=True)
    issues = get_json(f"https://api.github.com/repos/{REPO}/issues?state=open&per_page=100") or []
    out = {"errors": [], "lessOfThis": []}
    for i in issues:
        if "pull_request" in i:
            continue
        story = re.search(r"Story:\s*(\S+)", i.get("body") or "")
        item = {"number": i["number"], "title": i["title"], "story": story.group(1) if story else None,
                "body": (i.get("body") or "")[:1500], "created": i["created_at"], "url": i["html_url"]}
        if i["title"].startswith("Error:"):
            out["errors"].append(item)
        elif i["title"].startswith("Less important:"):
            out["lessOfThis"].append(item)
    (run / "feedback.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({k: len(v) for k, v in out.items()}))


if __name__ == "__main__":
    main()
