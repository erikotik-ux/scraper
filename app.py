import threading
from flask import Flask, jsonify, render_template, send_file
from aggregator import aggregate, load_cache_any, is_cache_stale

app = Flask(__name__)

_refresh_lock = threading.Lock()
_refreshing = False


def _background_refresh():
    global _refreshing
    with _refresh_lock:
        if _refreshing:
            return
        _refreshing = True
    try:
        aggregate(force_refresh=True)
        print("[BG] Cache refreshed successfully")
    except Exception as e:
        print(f"[BG] Refresh error: {e}")
    finally:
        _refreshing = False


# Pre-warm cache on startup so first visitor never waits
threading.Thread(target=_background_refresh, daemon=True).start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logo")
def logo():
    return send_file("DesignGuidelines/Neatly_Logo.png", mimetype="image/png")


@app.route("/api/articles")
def get_articles():
    try:
        cache = load_cache_any()
        if cache is None:
            # No cache at all — scrape synchronously (first ever cold start)
            cache = aggregate(force_refresh=True)
        elif is_cache_stale():
            # Stale — return existing data immediately, refresh in background
            threading.Thread(target=_background_refresh, daemon=True).start()
        return jsonify(cache)
    except Exception as e:
        return jsonify({"error": str(e), "articles": [], "last_scraped": None}), 500


@app.route("/api/refresh", methods=["POST"])
def refresh_articles():
    try:
        cache = aggregate(force_refresh=True)
        return jsonify(cache)
    except Exception as e:
        return jsonify({"error": str(e), "articles": [], "last_scraped": None}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
