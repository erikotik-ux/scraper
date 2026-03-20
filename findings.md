# Findings

## Sources — Confirmed

### 1. Ben's Bites (Ben Tossell)
- **Note:** The newsletter is called "Ben's Bites" not "Ben's Bytes"
- **RSS Feed:** `https://www.bensbites.com/feed` ✅ (Substack, RSS 2.0)
- **Strategy:** feedparser — no API key needed
- **Sample article today:** "What makes a good AGENTS.md?" (Mar 19, 2026)
- **Fields available:** title, link, pubDate, description/summary

### 2. The AI Rundown
- **Website:** `https://www.therundown.ai/`
- **RSS Feed:** `https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml` ✅ (beehiiv, RSS 2.0)
- **Strategy:** feedparser — no API key needed
- **Sample article today:** "Google bets on 'vibe design' with Stitch" (Mar 19, 2026)
- **Fields available:** title, link, pubDate, summary

### 3. Reddit
- **Strategy:** `old.reddit.com` HTML scraping with BeautifulSoup + User-Agent header
- **Subreddits:** r/artificial, r/MachineLearning, r/ChatGPT, r/OpenAI
- **Headers required:** `User-Agent: Mozilla/5.0 ...` (mimics browser)
- **Rate limiting:** 2-second delay between requests
- **Alternative:** PRAW (official API, free, requires Reddit app credentials)
- **Decision:** Use old.reddit.com for now (no API key needed); switch to PRAW if blocked

## Scraping Strategy Summary
| Source | Method | Auth Required |
|--------|--------|--------------|
| Ben's Bites | RSS via feedparser | None |
| The AI Rundown | RSS via feedparser | None |
| Reddit | old.reddit.com + BeautifulSoup | None (browser UA) |

## Tech Stack Decisions
- **Backend:** Python + Flask (serves API + static files)
- **Scraping:** feedparser, requests, BeautifulSoup4
- **Caching:** JSON file in `.tmp/` (TTL: 24 hours)
- **Frontend:** Vanilla HTML/CSS/JS (no framework — keep it fast and beautiful)
- **Persistence:** localStorage for saved articles (Supabase later)
