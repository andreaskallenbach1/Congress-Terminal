#!/usr/bin/env python3
"""Helper for writers and fact-checkers: is this quote word for word in the text at this URL?

Usage: python3 pipeline/quote_check.py URL "quote"      → prints FOUND, NOT FOUND or UNREACHABLE
       python3 pipeline/quote_check.py URL --text      → prints the normalized page text (first 20,000 chars)
Uses the same normalization as the machine check (stage 7), so a FOUND here will pass there.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_edition import normalize, page_text  # noqa: E402

url, arg = sys.argv[1], sys.argv[2]
text = page_text(url)
if text is None:
    print("UNREACHABLE")
elif arg == "--text":
    print(text[:20000])
else:
    print("FOUND" if normalize(arg) in text else "NOT FOUND")
