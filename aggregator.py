import json
import os
from datetime import datetime, timezone, timedelta

from tools.scrape_bensbites import scrape as scrape_bensbites
from tools.scrape_airundown import scrape as scrape_airundown
from tools.scrape_reddit import scrape as scrape_reddit

CACHE_FILE = ".tmp/articles_cache.json"
CACHE_TTL_HOURS = 24


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8", errors="replace") as f:
            cache = json.load(f)
        last_scraped = datetime.fromisoformat(cache["last_scraped"])
        if datetime.now(timezone.utc) - last_scraped > timedelta(hours=CACHE_TTL_HOURS):
            return None
        return cache
    except Exception as e:
        print(f"[Cache] Load error: {e}")
        return None


def save_cache(articles):
    os.makedirs(".tmp", exist_ok=True)
    cache = {
        "last_scraped": datetime.now(timezone.utc).isoformat(),
        "articles": articles,
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)
    return cache


def aggregate(force_refresh=False):
    if not force_refresh:
        cache = load_cache()
        if cache:
            return cache

    all_articles = []
    seen_urls = set()

    sources = [
        ("Ben's Bites", scrape_bensbites),
        ("The AI Rundown", scrape_airundown),
        ("Reddit", scrape_reddit),
    ]

    for name, scraper in sources:
        try:
            articles = scraper()
            count = 0
            for article in articles:
                if article["url"] not in seen_urls:
                    seen_urls.add(article["url"])
                    all_articles.append(article)
                    count += 1
            print(f"[{name}] {count} articles collected")
        except Exception as e:
            print(f"[{name}] Scraper error: {e}")

    all_articles.sort(
        key=lambda x: x.get("published_at") or "",
        reverse=True,
    )

    return save_cache(all_articles)
