import os
import requests
from flask import Flask, jsonify, render_template, send_file
from aggregator import aggregate, load_cache_any, is_cache_stale

app = Flask(__name__)

MODAL_ARTICLES = os.environ.get("MODAL_ARTICLES_URL", "")
MODAL_REFRESH  = os.environ.get("MODAL_REFRESH_URL", "")


def _modal_get(url):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


def _modal_post(url):
    r = requests.post(url, timeout=30)
    r.raise_for_status()
    return r.json()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logo")
def logo():
    return send_file("DesignGuidelines/pulse_logo.png", mimetype="image/png")


@app.route("/api/articles")
def get_articles():
    try:
        if MODAL_ARTICLES:
            return jsonify(_modal_get(MODAL_ARTICLES))
        if is_cache_stale():
            return jsonify(aggregate(force_refresh=True))
        return jsonify(load_cache_any())
    except Exception as e:
        return jsonify({"error": str(e), "articles": [], "last_scraped": None}), 500


@app.route("/api/refresh", methods=["POST"])
def refresh_articles():
    try:
        if MODAL_REFRESH:
            return jsonify(_modal_post(MODAL_REFRESH))
        return jsonify(aggregate(force_refresh=True))
    except Exception as e:
        return jsonify({"error": str(e), "articles": [], "last_scraped": None}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
