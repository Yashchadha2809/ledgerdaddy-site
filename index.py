# index.py
import os
from datetime import timedelta
from flask import Flask, send_file, Response

app = Flask(__name__)

# Absolute path to your HTML next to this file
HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(HERE, "home_min.html")

@app.after_request
def set_security_headers(resp):
    # Light security headers (safe for static pages)
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    resp.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
    return resp

@app.get("/")
def home():
    if not os.path.exists(HTML_PATH):
        return Response("home_min.html not found next to index.py", 500, mimetype="text/plain")
    # Cache the HTML for a short time (can be 0 if you want instant updates)
    resp = send_file(HTML_PATH, mimetype="text/html; charset=utf-8", max_age=timedelta(minutes=5))
    return resp

@app.get("/health")
def health():
    return {"ok": True}

# Handle noisy requests gracefully
@app.get("/favicon.ico")
def favicon():
    return Response(status=204)

@app.get("/robots.txt")
def robots():
    return Response("User-agent: *\nAllow: /\n", mimetype="text/plain")

# Vercel WSGI entry
handler = app

if __name__ == "__main__":
    # Local dev (optional): python index.py
    app.run(host="127.0.0.1", port=5000, debug=True)
