#!/usr/bin/env python3
"""Page store (saving measure 1): every source page is fetched once per day and kept as clean text.

Writers, fact-card makers, fact-checkers and the machine check all read from here instead of fetching the
same page again and again (in the first run some pages were fetched five times).

  python3 pipeline/pages.py URL            → prints the clean text (fetches and stores it if needed)
  python3 pipeline/pages.py URL --find "q" → FOUND / NOT FOUND / UNREACHABLE (same rule as the machine check)

Store: run/pages/<sha1 of URL>.json = {"url", "fetchedAt", "status", "text"}; entries older than 24 h are refetched.
"""
import datetime as dt
import hashlib
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect import get  # noqa: E402  (throttling per host, user agent)

STORE = Path(__file__).resolve().parent.parent / "run" / "pages"
MAX_AGE = dt.timedelta(hours=24)


def _chars(t: str) -> str:
    t = unicodedata.normalize("NFKC", html.unescape(t))
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = t.replace("–", "-").replace("—", "-").replace(" ", " ")
    return re.sub(r"\s+", " ", t).strip()


def clean(raw: bytes) -> str:
    t = raw.decode("utf-8", errors="ignore")
    t = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", t)
    return _chars(re.sub(r"<[^>]+>", " ", t))


def normalize(s: str) -> str:
    """Comparison form used everywhere quotes are matched (quotes are plain text: no tag stripping)."""
    return _chars(s).lower()


def text(url: str) -> str | None:
    """Clean page text with original capitalisation, or None if the page cannot be fetched."""
    STORE.mkdir(parents=True, exist_ok=True)
    f = STORE / (hashlib.sha1(url.encode()).hexdigest() + ".json")
    now = dt.datetime.now(dt.timezone.utc)
    if f.exists():
        d = json.loads(f.read_text())
        if now - dt.datetime.fromisoformat(d["fetchedAt"]) < MAX_AGE:
            return d["text"]
    raw = get(url, timeout=30)
    d = {"url": url, "fetchedAt": now.isoformat(), "status": "ok" if raw else "unreachable",
         "text": clean(raw) if raw else None}
    f.write_text(json.dumps(d, ensure_ascii=False))
    return d["text"]


def find(url: str, quote: str) -> str:
    t = text(url)
    if t is None:
        return "UNREACHABLE"
    return "FOUND" if normalize(quote) in t.lower() else "NOT FOUND"


def cased_quote(url: str, quote: str) -> str:
    """The quote as printed in the source (restores capitalisation of a lower-cased copy)."""
    t = text(url)
    if not t:
        return quote
    q = normalize(quote)
    i = t.lower().find(q)
    return t[i:i + len(q)] if i >= 0 else quote


if __name__ == "__main__":
    url = sys.argv[1]
    if len(sys.argv) > 3 and sys.argv[2] == "--find":
        print(find(url, sys.argv[3]))
    else:
        print(text(url) or "UNREACHABLE")
