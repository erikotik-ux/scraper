import html
import requests
import hashlib
import time
from datetime import datetime, timezone, timedelta

SUBREDDITS = ["artificial", "MachineLearning", "ChatGPT", "OpenAI"]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def scrape():
    articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    seen_urls = set()

    for subreddit in SUBREDDITS:
        try:
            url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=25"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            for post in data["data"]["children"]:
                p = post["data"]

                created = datetime.fromtimestamp(p["created_utc"], tz=timezone.utc)
                if created < cutoff:
                    continue

                post_url = f"https://www.reddit.com{p['permalink']}"
                if post_url in seen_urls:
                    continue
                seen_urls.add(post_url)

                article_id = hashlib.md5(post_url.encode()).hexdigest()[:12]

                # Prefer high-res preview image over small thumbnail
                thumbnail = None
                preview = p.get("preview", {})
                preview_images = preview.get("images", [])
                if preview_images:
                    resolutions = preview_images[0].get("resolutions", [])
                    source = preview_images[0].get("source", {})
                    # Pick a medium resolution (~640px) if available, else use source
                    mid = next((r for r in resolutions if r.get("width", 0) >= 640), source)
                    raw_url = mid.get("url", "")
                    if raw_url:
                        thumbnail = html.unescape(raw_url)

                # Fallback to thumbnail field
                if not thumbnail:
                    raw_thumb = p.get("thumbnail", "")
                    if raw_thumb and raw_thumb not in ("self", "default", "nsfw", "spoiler", "image") and raw_thumb.startswith("http"):
                        thumbnail = html.unescape(raw_thumb)

                selftext = p.get("selftext", "").strip()
                summary = selftext[:300] if selftext else f"{p.get('score', 0)} upvotes · r/{subreddit}"

                articles.append({
                    "id": article_id,
                    "source": "reddit",
                    "source_display": f"r/{subreddit}",
                    "title": p.get("title", "").strip(),
                    "summary": summary,
                    "url": p.get("url", post_url),
                    "published_at": created.isoformat(),
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                    "thumbnail": thumbnail,
                    "tags": [f"r/{subreddit}"],
                })

            time.sleep(0.5)

        except Exception as e:
            print(f"[Reddit] Error scraping r/{subreddit}: {e}")
            continue

    return articles
