"""
modal_scraper.py — Antigravity News Scraper on Modal

Runs every 24 hours, scrapes all sources in parallel, and stores
results in a Modal Dict. Exposes two web endpoints:
  GET  /api_articles  → return cached articles (used by Vercel)
  POST /api_refresh   → force a fresh scrape immediately

Deploy:   modal deploy modal_scraper.py
Run now:  modal run modal_scraper.py::scheduled_scrape
"""

import modal

app = modal.App("antigravity-scraper")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "feedparser>=6.0.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "fastapi[standard]",
    )
    .add_local_dir("tools", remote_path="/root/tools")
)

# Persistent key-value store — survives across runs
articles_store = modal.Dict.from_name("articles-cache", create_if_missing=True)


def _run_scrapers() -> dict:
    """Core scraping logic — runs inside a Modal container."""
    import sys
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from datetime import datetime, timezone

    sys.path.insert(0, "/root")
    from tools.scrape_bensbites import scrape as scrape_bensbites
    from tools.scrape_airundown import scrape as scrape_airundown
    from tools.scrape_reddit import scrape as scrape_reddit

    sources = [
        ("Ben's Bites", scrape_bensbites),
        ("The AI Rundown", scrape_airundown),
        ("Reddit", scrape_reddit),
    ]

    all_articles, seen_urls = [], set()

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(fn): name for name, fn in sources}
        for future in as_completed(futures, timeout=60):
            name = futures[future]
            try:
                for article in future.result():
                    if article["url"] not in seen_urls:
                        seen_urls.add(article["url"])
                        all_articles.append(article)
                print(f"[{name}] OK — {sum(1 for a in all_articles if a['source_display'] in name)} articles")
            except Exception as e:
                print(f"[{name}] Error: {e}")

    all_articles.sort(key=lambda x: x.get("published_at") or "", reverse=True)

    cache = {
        "last_scraped": datetime.now(timezone.utc).isoformat(),
        "articles": all_articles,
    }
    articles_store["cache"] = cache
    print(f"[Modal] Cached {len(all_articles)} articles total")
    return cache


@app.function(image=image, schedule=modal.Period(hours=24))
def scheduled_scrape():
    """Runs automatically every 24 hours."""
    _run_scrapers()


@app.function(image=image)
@modal.fastapi_endpoint(method="GET")
def api_articles():
    """Returns cached articles. Called by Vercel on every page load."""
    from datetime import datetime, timezone, timedelta

    cache = articles_store.get("cache", None)

    if cache is None:
        # First ever run — scrape now (cold start, ~4s)
        print("[Modal] No cache found, scraping now...")
        cache = _run_scrapers()
        return cache

    # Refresh if stale
    try:
        last = datetime.fromisoformat(cache["last_scraped"])
        if datetime.now(timezone.utc) - last > timedelta(hours=24):
            print("[Modal] Cache stale, refreshing...")
            cache = _run_scrapers()
    except Exception:
        pass

    return cache


@app.function(image=image)
@modal.fastapi_endpoint(method="POST")
def api_refresh():
    """Force a fresh scrape. Called by the Refresh button on the dashboard."""
    return _run_scrapers()
