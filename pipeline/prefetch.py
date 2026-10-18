#!/usr/bin/env python3
"""Before the fact cards: fetch every source of the selected stories once into the page store (saving measure 1).

Reads run/<id>/selection.json (sourcesToUse per story) and run/<id>/candidates.json (item URLs of the chosen
candidates). Writes run/<id>/sources-<story>.json = [{"url", "outlet", "tier", "chars"|"unreachable"}] for the
fact-card makers. AP/Reuters (headline-only via Google News) and other blocked outlets are listed but not fetched.

Usage: python3 pipeline/prefetch.py <run-id>
       python3 pipeline/prefetch.py <run-id> --candidates   (before the arbiter: fetch every candidate's links once and
       write run/<id>/reach.json = {url: "ok" | "unreachable" | "blocked"}, so the arbiter only plans with sources that
       answer; in run 2 four of the arbiter's chosen sources returned 403 to the writers)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages  # noqa: E402

BLOCKED = ("news.google.com", "apnews.com", "reuters.com", "axios.com", "c-span.org", "punchbowl.news", "www.congress.gov")
run = Path(__file__).resolve().parent.parent / "run" / sys.argv[1]
candidates = {c["id"]: c for c in json.loads((run / "candidates.json").read_text())}
if "--candidates" in sys.argv:
    reach = {}
    for c in candidates.values():
        for it in c.get("items", []):
            u = it["url"]
            if u and u not in reach:
                reach[u] = "blocked" if any(b in u for b in BLOCKED) else ("ok" if pages.text(u) else "unreachable")
    (run / "reach.json").write_text(json.dumps(reach, indent=1))
    print(json.dumps({k: sum(v == k for v in reach.values()) for k in ("ok", "unreachable", "blocked")}))
    sys.exit(0)
selection = json.loads((run / "selection.json").read_text())
summary = {}
for st in selection["stories"]:
    urls: dict[str, dict] = {}
    for c_id in [st["id"], *st.get("mergedFrom", [])]:
        for it in candidates.get(c_id, {}).get("items", []):
            urls.setdefault(it["url"], {"outlet": it.get("outlet"), "tier": it.get("tier")})
    for u in st.get("sourcesToUse", []):
        urls.setdefault(u, {"outlet": None, "tier": None})
    out = []
    for u, meta in urls.items():
        if any(b in u for b in BLOCKED):
            out.append({"url": u, **meta, "status": "blocked (headline only)"})
            continue
        t = pages.text(u)
        out.append({"url": u, **meta, "status": "ok" if t else "unreachable", "chars": len(t or "")})
    (run / f"sources-{st['id']}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    summary[st["id"]] = sum(1 for o in out if o["status"] == "ok")
print(json.dumps(summary))
