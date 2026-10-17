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

echo "== Official (extended)"
check house_floor_weekly      "https://docs.house.gov/floor/"
check majority_leader_sched   "https://www.majorityleader.gov/schedule/weekly-schedule.htm"
check senate_dem_floor        "https://www.democrats.senate.gov/floor"
check senate_press_gallery    "https://www.dailypress.senate.gov/feed/"
check cbo_rss                 "https://www.cbo.gov/publications/all/rss.xml"
check gao_rss                 "https://www.gao.gov/rss/reports.xml"
check everycrsreport_rss      "https://www.everycrsreport.com/rss.xml"
check state_dept_press        "https://www.state.gov/rss-feed/press-releases/feed/"

echo "== News: center / mainstream (extended)"
check nyt_politics            "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml"
check cbs_politics            "https://www.cbsnews.com/latest/rss/politics"
check nbc_politics            "https://feeds.nbcnews.com/nbcnews/public/politics"
check abc_politics            "https://abcnews.go.com/abcnews/politicsheadlines"
check pbs_politics            "https://www.pbs.org/newshour/feeds/rss/politics"
check semafor                 "https://www.semafor.com/rss.xml"
check axios_via_google_news   "https://news.google.com/rss/search?q=site:axios.com+congress&hl=en-US&gl=US&ceid=US:en"
check punchbowl_via_gnews     "https://news.google.com/rss/search?q=site:punchbowl.news&hl=en-US&gl=US&ceid=US:en"
check wsj_world               "https://feeds.a.dj.com/rss/RSSWorldNews.xml"
check realclearpolitics       "https://www.realclearpolitics.com/index.xml"

echo "== News: right-leaning"
check fox_politics            "https://moxie.foxnews.com/google-publisher/politics.xml"
check washington_examiner     "https://www.washingtonexaminer.com/section/policy/feed/"
check national_review         "https://www.nationalreview.com/feed/"
check the_dispatch            "https://thedispatch.com/feed/"
check free_beacon             "https://freebeacon.com/feed/"
check ny_post_politics        "https://nypost.com/politics/feed/"

echo "== News: left-leaning"
check the_nation              "https://www.thenation.com/feed/?post_type=article"
check mother_jones            "https://www.motherjones.com/politics/feed/"
check new_republic            "https://newrepublic.com/rss.xml"
check vox_politics            "https://www.vox.com/rss/politics/index.xml"
check talking_points_memo     "https://talkingpointsmemo.com/feed"

echo "== International perspective"
check guardian_us_politics    "https://www.theguardian.com/us-news/us-politics/rss"
check bbc_us_canada           "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml"
check dw_world                "https://rss.dw.com/rdf/rss-en-world"

echo "== Foreign & security policy"
check war_on_the_rocks        "https://warontherocks.com/feed/"
check responsible_statecraft  "https://responsiblestatecraft.org/feed/"
check atlantic_council        "https://www.atlanticcouncil.org/feed/"
check foreign_policy          "https://foreignpolicy.com/feed/"
check breaking_defense        "https://breakingdefense.com/feed/"

echo "== Elections & video (extended)"
check sabato_via_google_news  "https://news.google.com/rss/search?q=site:centerforpolitics.org+crystal+ball&hl=en-US&gl=US&ceid=US:en"
check yt_speaker              "https://www.youtube.com/feeds/videos.xml?channel_id=UC4czmSY7dsAiLFseD313tKA"
check yt_senate_democrats     "https://www.youtube.com/feeds/videos.xml?channel_id=UC-ABttxh8uQv_10qmwGaidw"
check house_live_video        "https://live.house.gov/"
