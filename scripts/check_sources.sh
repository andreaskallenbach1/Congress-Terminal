#!/usr/bin/env bash
# Checks whether each candidate source is reachable from the current environment.
# Usage: ./scripts/check_sources.sh
# The Congress.gov key is attached by the environment as a network secret (X-Api-Key header),
# so no key appears in URLs here.
set -u

UA="Mozilla/5.0 (CongressTerminal source check)"

check() {
  local name="$1" url="$2"
  local result
  result=$(curl -s -o /dev/null -L -m 20 -A "$UA" \
    -w "%{http_code} %{content_type}" "$url" 2>/dev/null)
  printf "%-28s %s\n" "$name" "${result:-error}"
}

echo "== Primary sources"
check congress_api_bills      "https://api.congress.gov/v3/bill?format=json&limit=1&sort=updateDate+desc"
check congress_api_meetings   "https://api.congress.gov/v3/committee-meeting?format=json&limit=1"
check govinfo_crec_rss        "https://www.govinfo.gov/rss/crec.xml"
check senate_votes_xml        "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_119_2.xml"
check house_votes_api         "https://api.congress.gov/v3/house-vote/119/2?format=json&limit=1"
check house_clerk_floor       "https://clerk.house.gov/FloorSummary"
check house_committee_week    "https://docs.house.gov/Committee/Calendar/ByWeek.aspx"
check sfrc_hearings           "https://www.foreign.senate.gov/hearings"
check hfac_hearings           "https://foreignaffairs.house.gov/committee-activity/hearings"
check sasc_hearings           "https://www.armed-services.senate.gov/hearings"
check arms_sales_fedreg       "https://www.federalregister.gov/api/v1/documents.json?per_page=1&conditions%5Bterm%5D=%22arms+sales+notification%22&order=newest"
check federal_register        "https://www.federalregister.gov/api/v1/documents.json?per_page=1"
check fec_api                 "https://api.open.fec.gov/v1/candidates/?api_key=DEMO_KEY&per_page=1"
check legislators_json        "https://unitedstates.github.io/congress-legislators/legislators-current.json"

echo "== News"
check npr_politics_rss        "https://feeds.npr.org/1014/rss.xml"
check ap_congress_hub         "https://apnews.com/hub/congress"
check ap_via_google_news      "https://news.google.com/rss/search?q=site:apnews.com+congress&hl=en-US&gl=US&ceid=US:en"
check reuters_via_google_news "https://news.google.com/rss/search?q=site:reuters.com+congress&hl=en-US&gl=US&ceid=US:en"
check cspan_congress          "https://www.c-span.org/congress/"
check rollcall_rss            "https://rollcall.com/feed/"
check thehill_senate_rss      "https://thehill.com/homenews/senate/feed/"
check politico_congress_rss   "https://rss.politico.com/congress.xml"
check defensenews_congress    "https://www.defensenews.com/arc/outboundfeeds/rss/category/congress/?outputType=xml"
check justsecurity_rss        "https://www.justsecurity.org/feed/"
check lawfare_rss             "https://www.lawfaremedia.org/feeds/articles"

echo "== Video & elections"
check youtube_cspan_feed      "https://www.youtube.com/feeds/videos.xml?user=CSPAN"
check ballotpedia_2026        "https://ballotpedia.org/United_States_Congress_elections,_2026"
