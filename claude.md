# claude.md — Project Constitution
## Antigravity News Dashboard

---

## Project Identity
A beautiful, interactive web dashboard that aggregates AI news from newsletters and Reddit. Displays articles from the last 24 hours. Users can save articles (persisted via localStorage, later Supabase).

---

## Data Schema (DRAFT — pending user confirmation)

### Article Object
```json
{
  "id": "string (hash of url+title)",
  "source": "string (e.g. 'bens_bytes' | 'ai_rundown' | 'reddit')",
  "source_display": "string (e.g. 'Ben's Bytes')",
  "title": "string",
  "summary": "string (first 2-3 sentences or meta description)",
  "url": "string",
  "published_at": "ISO8601 datetime string",
  "scraped_at": "ISO8601 datetime string",
  "thumbnail": "string | null (image URL if available)",
  "tags": ["string"],
  "saved": false
}
```

### Scraper Cache Object (stored in .tmp/)
```json
{
  "last_scraped": "ISO8601 datetime",
  "articles": [Article]
}
```

### Saved Articles (localStorage key: "saved_articles")
```json
["article_id_1", "article_id_2"]
```

---

## Behavioral Rules
1. Only display articles published within the last 24 hours
2. Do not duplicate articles (deduplicate by URL)
3. Scraper runs at most once every 24 hours (cache results)
4. Saved articles persist on page refresh
5. Never crash on a single source failure — isolate errors per source
6. Design must be gorgeous, interactive, and card-based

---

## Architecture Invariants
- Python Flask server serves both the API and the static dashboard
- Each source has its own isolated scraper tool in `tools/`
- All intermediate data goes to `.tmp/`
- `.env` holds any future API keys
- Supabase will replace localStorage in a future phase

---

## Tech Stack
- **Backend:** Python (Flask), requests, BeautifulSoup4, feedparser
- **Frontend:** HTML/CSS/JS (vanilla, no framework needed)
- **Storage (Phase 1):** localStorage for saved articles, `.tmp/` JSON for cache
- **Storage (Phase 2):** Supabase

---

## Maintenance Log
*(updated after deployments or architecture changes)*
