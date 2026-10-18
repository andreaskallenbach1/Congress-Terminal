#!/usr/bin/env python3
"""After the procedure explainer: add new glossary terms only if their definition is quoted verbatim from an
official source (FT 7: fixed and checked). Code writes the glossary; the agent only proposes.

Reads run/<id>/glossary-add.json = [{"term","definition","source","url"}]; keeps proposals whose definition is found in
the page (page store) and whose URL is on an official domain; appends them to app/src/data/glossary.json.
Usage: python3 pipeline/glossary_add.py <run-id>
"""
import datetime as dt
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OFFICIAL = (".senate.gov", ".house.gov", "congress.gov", "govinfo.gov", "crsreports.congress.gov", "everycrsreport.com", "gao.gov", "cbo.gov")
run = ROOT / "run" / sys.argv[1]
src = run / "glossary-add.json"
if not src.exists():
    sys.exit(print(json.dumps({"added": 0})))
glossary_file = ROOT / "app" / "src" / "data" / "glossary.json"
glossary = json.loads(glossary_file.read_text())
have = {g["term"].lower() for g in glossary}
added, rejected = [], []
for p in json.loads(src.read_text()):
    host = urlparse(p["url"]).netloc
    ok_host = any(host == d.lstrip(".") or host.endswith(d) for d in OFFICIAL)
    if p["term"].lower() in have or not ok_host or pages.find(p["url"], p["definition"]) != "FOUND":
        rejected.append(p["term"])
        continue
    glossary.append({"term": p["term"].lower(), "definition": pages.cased_quote(p["url"], p["definition"]),
                     "source": p["source"], "url": p["url"], "retrieved": dt.date.today().isoformat()})
    have.add(p["term"].lower())
    added.append(p["term"])
glossary_file.write_text(json.dumps(glossary, indent=1, ensure_ascii=False))
print(json.dumps({"added": added, "rejected": rejected}))
