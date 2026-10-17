#!/usr/bin/env python3
"""After the gatekeeper: keep only the headlines it let through (saving measure 5 / stage 0 gatekeeper).

The gatekeeper (small model) reads run/<id>/headlines.txt and writes run/<id>/gate.json = {"keep": [n, ...]}.
This script writes run/<id>/inputs-gated.json: the compact inputs with only the kept items. The story builder
reads that file. Primary data (votes, bills, meetings, arms sales) is never filtered here.

Usage: python3 pipeline/gate.py <run-id>
"""
import json
import sys
from pathlib import Path

run = Path(__file__).resolve().parent.parent / "run" / sys.argv[1]
view = json.loads((run / "inputs-compact.json").read_text())
keep = set(json.loads((run / "gate.json").read_text())["keep"])
before = len(view["items"])
view["items"] = [g for g in view["items"] if g["n"] in keep]
(run / "inputs-gated.json").write_text(json.dumps(view, ensure_ascii=False, separators=(",", ":")))
print(json.dumps({"items": before, "kept": len(view["items"])}))
