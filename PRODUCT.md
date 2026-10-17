# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Delegated: Astro, static output hosted on GitHub Pages from the public repository `andreaskallenbach1/Congress-Terminal`, installable as a PWA (Windows first, Edge/Chrome). Chosen because the product is many dated, read-mostly pages (daily briefing, archive, watchlist, calendar) that a scheduled job regenerates as files.

## Users

One primary user: Andreas Kallenbach, a political science student focused on the US Congress. He reads the briefing once a day, mostly on a Windows laptop, for about 40 minutes, and picks what he reads in depth. He reads English fluently; the interface and all content are in English.

## Product Purpose

A daily, verified briefing on the US Congress that keeps a serious student current without the noise of general news sites. It covers only significant developments: legislation with real consequences, power shifts, oversight, Senate confirmations and treaties, the 2026 midterms, and Congress as a foreign-policy actor (sanctions, war powers, arms sales, foreign aid, hearings, CODELs, letters, joint statements). Success: after one session he knows what moved in Congress and why it matters, and can trust every statement.

## Positioning

Each statement carries its verification status and a link to its source; facts come from primary sources (Congress.gov, roll-call records, committee sites, CRS, CBO, Federal Register) and agencies, while partisan outlets are used only to show how each side frames a story. A pipeline of agents and counter-agents selects and checks the content every morning, and disagreements between them are visible to the reader. Foreign policy is a first-class section, not an afterthought.

## Operating Context

- A scheduled Claude session runs every morning, writes the briefing as data files into the repository, and the site rebuilds from them; a Sunday run adds a weekly review and one deep dive.
- Fixed sections: Top Stories, Foreign Policy Desk, Midterms 2026, Floor & Committees, Watch (video clips with timestamps), Also Notable. Persistent tools: Watchlist (bills tracked through intro, committee, floor, other chamber, president), What's Next calendar (7 days), Archive, Glossary of procedural terms.
- Stories are long-form: every story is a full article of roughly 500–800 words in a fixed structure (What's new, Why it matters, What's next, Background, Sources), not a short summary.
- Feedback buttons on each story ("not important", "flag an error") open a prefilled GitHub issue that the next run reads.

## Capabilities and Constraints

- Static site; no server, no login. The repository is public, so nothing private goes into it.
- Verification statuses: `verified` (primary source), `multiple reports` (two or more independent outlets), `unconfirmed`.
- Content from AP, Reuters, C-SPAN, Axios, Punchbowl and other paywalled or blocking sites appears only as headline plus link; no full text of third-party articles.
- Imagery: public-domain official portraits of members (unitedstates images, Congress.gov member images with attribution), public-domain photos of the Capitol and Congress (Architect of the Capitol, Library of Congress, Wikimedia Commons), free Unsplash photos via its connector once connected. No news-agency photos.
- An own logo/emblem for Congress Terminal; never the official seal of Congress, the House or the Senate.
- Undecided: exact time of the morning run; how much one run costs in subscription usage.

## Brand Commitments

Name: Congress Terminal. Voice: precise, neutral, explanatory; quotes and facts instead of judgments; contested interpretations attributed to their side.

## Evidence on Hand

- 66 tested sources (`scripts/check_sources.sh`); the Congress.gov API key is supplied by the environment.
- No real briefing exists yet. Any mockup content must be labelled as sample and must not present invented facts as real.

## Product Principles

1. Substance over volume: nothing ceremonial or local unless it has institutional consequences.
2. Every statement is traceable to a source and shows how well it is verified.
3. Congress acts abroad as well as at home; foreign policy gets equal weight.
4. Neutral and fair to both parties; partisan framing is shown as framing.
5. Built for deep reading: long-form text must be comfortable to read for 40 minutes.

## Accessibility & Inclusion

WCAG 2.2 AA contrast and keyboard access; comfortable long-form reading on a laptop screen.
