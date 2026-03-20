# SOP: Article Scraper

## Goal
Collect articles published within the last 24 hours from Ben's Bites, The AI Rundown, and Reddit. Return a unified list of Article objects.

## Inputs
- None (sources are hardcoded)
- `force_refresh: bool` — bypass cache

## Output
```json
{
  "last_scraped": "ISO8601",
  "articles": [Article]
}
```

## Article Schema
```json
{
  "id": "md5 hash of URL (12 chars)",
  "source": "bens_bites | ai_rundown | reddit",
  "source_display": "Ben's Bites | The AI Rundown | r/subreddit",
  "title": "string",
  "summary": "string (max 300 chars, HTML stripped)",
  "url": "string",
  "published_at": "ISO8601 or null",
  "scraped_at": "ISO8601",
  "thumbnail": "URL string or null",
  "tags": ["string"]
}
```

## Sources
| Source | Method | URL |
|--------|--------|-----|
| Ben's Bites | RSS feedparser | https://www.bensbites.com/feed |
| The AI Rundown | RSS feedparser | https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml |
| Reddit | JSON API | https://www.reddit.com/r/{sub}/new.json |

## Cache Rules
- Cache file: `.tmp/articles_cache.json`
- TTL: 24 hours
- If cache is stale or missing → run all scrapers
- If cache is fresh → return cached data directly

## Error Handling
- Each scraper is isolated in a try/except
- A single source failure MUST NOT crash the aggregator
- Log the error and continue to next source

## Deduplication
- Deduplicate articles by URL across all sources
- First occurrence wins

## Rate Limiting
- Reddit: 2-second delay between subreddit requests
- RSS feeds: no rate limiting required
