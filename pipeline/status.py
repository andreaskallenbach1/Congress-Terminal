#!/usr/bin/env python3
"""Run status for the "Update now" progress display (code, no AI).

Writes run/<id>/status.json and publishes the same file as the only file on the branch `run-status`, which the web
app polls through the GitHub API. The branch is written with git plumbing (no checkout, the working tree stays as it
is) and does not trigger the Pages build. A failed push only prints a warning: the run itself must never fail because
the progress display could not be updated.

Stages (CLAUDE.md 3, "Automatik"): 0 Requested · 1 Collect · 2 Bundle · 3 Select · 4 Write and check · 5 Edit · 6 Publish
States: running · done (edition published) · failed (nothing published, last edition stays)

Usage: python3 pipeline/status.py <run-id> <stage 0-6> [--state running|done|failed] [--kind daily|weekly] [--note "..."]
"""
import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABELS = {0: "Requested", 1: "Collect", 2: "Bundle", 3: "Select", 4: "Write and check", 5: "Edit", 6: "Publish"}
BRANCH = "run-status"


def git(*args: str, data: str | None = None) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, input=data, capture_output=True, text=True, check=True).stdout.strip()


def publish(body: str, message: str) -> None:
    blob = git("hash-object", "-w", "--stdin", data=body)
    tree = git("mktree", data=f"100644 blob {blob}\tstatus.json\n")
    parent = []
    try:
        git("fetch", "-q", "origin", BRANCH)
        parent = ["-p", git("rev-parse", "FETCH_HEAD")]
    except subprocess.CalledProcessError:
        pass                                              # first status ever: the branch is created
    commit = git("commit-tree", tree, *parent, "-m", message)
    git("push", "-q", "origin", f"{commit}:refs/heads/{BRANCH}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_id")
    ap.add_argument("stage", type=int, choices=range(0, 7))
    ap.add_argument("--state", default="running", choices=["running", "done", "failed"])
    ap.add_argument("--kind", choices=["daily", "weekly"])
    ap.add_argument("--note", default="")
    a = ap.parse_args()

    run = ROOT / "run" / a.run_id
    run.mkdir(parents=True, exist_ok=True)
    f = run / "status.json"
    prev = json.loads(f.read_text()) if f.exists() else {}
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    status = {
        "runId": a.run_id,
        "kind": a.kind or prev.get("kind") or ("weekly" if a.run_id.endswith("-weekly") else "daily"),
        "stage": a.stage,
        "label": LABELS[a.stage],
        "state": a.state,
        "note": a.note,                                   # short, public: never secrets, never session links
        "startedAt": prev.get("startedAt", now),
        "updatedAt": now,
    }
    body = json.dumps(status, indent=1)
    f.write_text(body)
    try:
        publish(body, f"Run {a.run_id}: stage {a.stage} {LABELS[a.stage]} ({a.state})")
        print(json.dumps({"published": True, **status}))
    except subprocess.CalledProcessError as e:
        print(f"warning: status not published ({e.stderr.strip()[:200]})", file=sys.stderr)
        print(json.dumps({"published": False, **status}))


if __name__ == "__main__":
    main()
