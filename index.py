# index.py
import os
from pathlib import Path
from flask import Flask, Response, send_file

APP_DIR = Path(__file__).resolve().parent
HTML_PATH = APP_DIR / "home_min.html"

app = Flask(__name__)

@app.get("/")
def home():
    if not HTML_PATH.exists():
        return Response("home_min.html not found next to index.py", 500, mimetype="text/plain")
    return send_file(HTML_PATH, mimetype="text/html")

@app.get("/health")
def health():
    return {"ok": True}

# Quietly swallow common favicon requests so they don't error your logs
@app.get("/favicon.ico")
@app.get("/favicon.png")
def favicon():
    # 204 No Content – nothing to serve
    return Response(status=204)

# IMPORTANT: Do NOT assign `handler = app` here.
# Vercel detects the WSGI app by the name `app` automatically.

if __name__ == "__main__":
    # Local dev: python index.py
    app.run(host="127.0.0.1", port=5000, debug=True)
