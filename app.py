from flask import Flask, jsonify, render_template, send_file
from aggregator import aggregate

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logo")
def logo():
    return send_file("DesignGuidelines/Neatly_Logo.png", mimetype="image/png")


@app.route("/api/articles")
def get_articles():
    try:
        cache = aggregate(force_refresh=False)
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
