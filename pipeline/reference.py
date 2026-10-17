#!/usr/bin/env python3
"""Member profiles and committees (phase 4, role "member profiles") — code, no AI.

Builds data/members.json and data/committees.json from open, citable data:
- @unitedstates/congress-legislators (public domain): current members, committees, committee membership
- Voteview (UCLA): DW-NOMINATE first dimension for the 119th Congress (liberal −1 … conservative +1)
Run at the start of every run (cheap, two small downloads); the web app reads both files at build time.

Usage: python3 pipeline/reference.py
"""
import csv
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect import get  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LEG = "https://unitedstates.github.io/congress-legislators/"
VOTEVIEW = "https://voteview.com/static/data/out/members/HS119_members.csv"


def load_json(url: str):
    raw = get(url, timeout=60)
    if raw is None:
        sys.exit(f"could not fetch {url}")
    return json.loads(raw)


def main() -> None:
    legislators = load_json(LEG + "legislators-current.json")
    committees = load_json(LEG + "committees-current.json")
    membership = load_json(LEG + "committee-membership-current.json")
    raw = get(VOTEVIEW, timeout=60)
    nominate = {}
    if raw:
        for row in csv.DictReader(io.StringIO(raw.decode("utf-8"))):
            if row.get("bioguide_id") and row.get("nominate_dim1"):
                nominate[row["bioguide_id"]] = float(row["nominate_dim1"])

    by_id = {c["thomas_id"]: c for c in committees}
    member_committees: dict[str, list] = {}
    committee_rows = []
    for cid, roster in membership.items():
        if cid not in by_id:          # subcommittees (e.g. SSFR09) are skipped; the page lists full committees
            continue
        c = by_id[cid]
        for m in roster:
            member_committees.setdefault(m["bioguide"], []).append({"committee": c["name"], "id": cid, "title": m.get("title")})
        lead = lambda t: next(({"bioguide": m["bioguide"], "name": m["name"]} for m in roster if (m.get("title") or "") == t), None)  # noqa: E731
        committee_rows.append({
            "id": cid,
            "name": c["name"],
            "chamber": c["type"],          # house | senate | joint
            "url": c.get("url"),
            "jurisdiction": c.get("jurisdiction"),
            "chair": lead("Chairman") or lead("Chair"),
            "ranking": lead("Ranking Member"),
            "members": len(roster),
        })

    members = []
    for p in legislators:
        term = p["terms"][-1]
        bid = p["id"]["bioguide"]
        members.append({
            "bioguideId": bid,
            "name": p["name"].get("official_full") or f"{p['name']['first']} {p['name']['last']}",
            "party": {"Republican": "R", "Democrat": "D"}.get(term.get("party"), "I"),
            "state": term["state"],
            "chamber": "senate" if term["type"] == "sen" else "house",
            "district": term.get("district"),
            "since": p["terms"][0]["start"][:4],
            "website": term.get("url"),
            "committees": member_committees.get(bid, []),
            "nominate": nominate.get(bid),
        })
    out = ROOT / "data"
    out.mkdir(exist_ok=True)
    (out / "members.json").write_text(json.dumps(members, ensure_ascii=False, separators=(",", ":")))
    (out / "committees.json").write_text(json.dumps(sorted(committee_rows, key=lambda c: (c["chamber"], c["name"])), indent=1, ensure_ascii=False))
    print(json.dumps({"members": len(members), "withNominate": sum(m["nominate"] is not None for m in members), "committees": len(committee_rows)}))


if __name__ == "__main__":
    main()
