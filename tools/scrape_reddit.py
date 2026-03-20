import hashlib
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

SUBREDDITS = ["artificial", "MachineLearning", "ChatGPT", "OpenAI"]


def _parse_entry(entry, subreddit, cutoff, seen_urls):
    try:
        pub = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            pub = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            if pub < cutoff:
                return None

        url = entry.get("link", "")
        if not url or url in seen_urls:
            return None
        seen_urls.add(url)

        # Extract thumbnail and clean summary from HTML content
        thumbnail = None
        summary = ""
        raw_html = ""
        if hasattr(entry, "content") and entry.content:
            raw_html = entry.content[0].get("value", "")
        elif hasattr(entry, "summary"):
            raw_html = entry.summary

        if raw_html:
            soup = BeautifulSoup(raw_html, "html.parser")
            img = soup.find("img")
            if img and img.get("src") and "redditstatic" not in img["src"]:
                thumbnail = img["src"]
            summary = soup.get_text(separator=" ").strip()[:300]

        article_id = hashlib.md5(url.encode()).hexdigest()[:12]

        return {
            "id": article_id,
            "source": "reddit",
            "source_display": f"r/{subreddit}",
            "title": entry.get("title", "").strip(),
            "summary": summary or f"r/{subreddit}",
            "url": url,
            "published_at": pub.isoformat() if pub else datetime.now(timezone.utc).isoformat(),
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "thumbnail": thumbnail,
            "tags": [f"r/{subreddit}"],
        }
    except Exception:
        return None


def scrape():
    articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    seen_urls = set()

    for subreddit in SUBREDDITS:
        try:
            feed = feedparser.parse(
                f"https://www.reddit.com/r/{subreddit}/new.rss?limit=25",
                agent="Mozilla/5.0 (compatible; news-aggregator/1.0)",
            )
            for entry in feed.entries:
                article = _parse_entry(entry, subreddit, cutoff, seen_urls)
                if article:
                    articles.append(article)
        except Exception as e:
            print(f"[Reddit] Error scraping r/{subreddit}: {e}")
            continue

    return articles
