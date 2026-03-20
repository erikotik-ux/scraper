import json
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta

from tools.scrape_bensbites import scrape as scrape_bensbites
from tools.scrape_airundown import scrape as scrape_airundown
from tools.scrape_reddit import scrape as scrape_reddit

# Use system temp dir — writable on Vercel (/tmp), Render, and local Windows
CACHE_FILE = os.path.join(tempfile.gettempdir(), "articles_cache.json")
CACHE_TTL_HOURS = 24

# In-memory cache — survives across requests on warm serverless instances
_mem = {"data": None, "ts": None}


def _mem_fresh():
    if not _mem["data"] or not _mem["ts"]:
        return False
    return datetime.now(timezone.utc) - _mem["ts"] < timedelta(hours=CACHE_TTL_HOURS)


def load_cache_any():
    """Return cache from memory or disk, regardless of age."""
    if _mem["data"]:
        return _mem["data"]
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Cache] Load error: {e}")
        return None


def is_cache_stale():
    """True if cache is missing or older than TTL."""
    if _mem_fresh():
        return False
    cache = load_cache_any()
    if not cache:
        return True
    try:
        last = datetime.fromisoformat(cache["last_scraped"])
        return datetime.now(timezone.utc) - last > timedelta(hours=CACHE_TTL_HOURS)
    except Exception:
        return True


def save_cache(articles):
    cache = {
        "last_scraped": datetime.now(timezone.utc).isoformat(),
        "articles": articles,
    }
    _mem["data"] = cache
    _mem["ts"] = datetime.now(timezone.utc)
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Cache] Write error: {e}")
    return cache


def aggregate(force_refresh=False):
    if not force_refresh and _mem_fresh():
        return _mem["data"]

    if not force_refresh:
        cache = load_cache_any()
        if cache and not is_cache_stale():
            return cache

    all_articles = []
    seen_urls = set()

    sources = [
        ("Ben's Bites", scrape_bensbites),
        ("The AI Rundown", scrape_airundown),
        ("Reddit", scrape_reddit),
    ]

    # Parallel scraping — all 3 sources run simultaneously
    # keeps total time ~3-4s instead of ~12s sequential
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(fn): name for name, fn in sources}
        for future in as_completed(futures, timeout=9):
            name = futures[future]
            try:
                articles = future.result()
                count = 0
                for article in articles:
                    if article["url"] not in seen_urls:
                        seen_urls.add(article["url"])
                        all_articles.append(article)
                        count += 1
                print(f"[{name}] {count} articles collected")
            except Exception as e:
                print(f"[{name}] Scraper error: {e}")

    all_articles.sort(key=lambda x: x.get("published_at") or "", reverse=True)
    return save_cache(all_articles)
