import feedparser
import hashlib
import re
from datetime import datetime, timezone, timedelta

FEED_URL = "https://www.bensbites.com/feed"


def scrape():
    articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    try:
        feed = feedparser.parse(FEED_URL)
    except Exception as e:
        print(f"[Ben's Bites] Feed parse error: {e}")
        return articles

    for entry in feed.entries:
        published = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            except Exception:
                pass

        if published and published < cutoff:
            continue

        url = entry.get("link", "")
        if not url:
            continue

        title = entry.get("title", "").strip()
        article_id = hashlib.md5(url.encode()).hexdigest()[:12]

        raw_summary = entry.get("summary", entry.get("description", ""))
        summary = re.sub(r"<[^>]+>", " ", raw_summary).strip()
        summary = re.sub(r"\s+", " ", summary)[:300]

        # Extract image from enclosure
        thumbnail = None
        enclosures = entry.get("enclosures", [])
        for enc in enclosures:
            href = enc.get("href", "")
            if href and enc.get("type", "").startswith("image"):
                thumbnail = href
                break

        articles.append({
            "id": article_id,
            "source": "bens_bites",
            "source_display": "Ben's Bites",
            "title": title,
            "summary": summary,
            "url": url,
            "published_at": published.isoformat() if published else None,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "thumbnail": thumbnail,
            "tags": [],
        })

    return articles
