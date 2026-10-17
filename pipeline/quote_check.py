#!/usr/bin/env python3
"""Helper for writers and fact-checkers: is this quote word for word in the text at this URL?

Usage: python3 pipeline/quote_check.py URL "quote"      → prints FOUND, NOT FOUND or UNREACHABLE
       python3 pipeline/quote_check.py URL --text      → prints the normalized page text (first 20,000 chars)
Reads from the page store (pipeline/pages.py), the same text the machine check (stage 7) uses.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages  # noqa: E402

url, arg = sys.argv[1], sys.argv[2]
if arg == "--text":
    print((pages.text(url) or "UNREACHABLE")[:20000])
else:
    print(pages.find(url, arg))
