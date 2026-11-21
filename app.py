"""ThreatGuard AI Flask application."""
from flask import Flask, jsonify, render_template, request

from detector import analyze_text, analyze_url

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    value = str(payload.get("value", "")).strip()
    scan_type = payload.get("type", "url")

    if not value:
        return jsonify({"error": "Enter a URL or message to analyze."}), 400

    if scan_type not in {"url", "text"}:
        return jsonify({"error": "Choose URL or Message analysis."}), 400

    try:
        result = analyze_text(value) if scan_type == "text" else analyze_url(value)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
