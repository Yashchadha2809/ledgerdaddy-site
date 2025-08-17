# index.py
import os
from pathlib import Path
from flask import Flask, Response, send_file

APP_DIR = Path(__file__).resolve().parent
HOME_PATH = APP_DIR / "home_min.html"
SIGNUP_PATH = APP_DIR / "personal_sign_up.html"

app = Flask(__name__)

@app.get("/")
def home():
    if not HOME_PATH.exists():
        return Response("home_min.html not found next to index.py", 500, mimetype="text/plain")
    return send_file(HOME_PATH, mimetype="text/html")

@app.get("/personal-sign-up")
def personal_sign_up():
    if not SIGNUP_PATH.exists():
        return Response("personal_sign_up.html not found next to index.py", 500, mimetype="text/plain")
    return send_file(SIGNUP_PATH, mimetype="text/html")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/favicon.ico")
@app.get("/favicon.png")
def favicon():
    return Response(status=204)

# Do NOT export `handler`; Vercel finds `app` automatically.

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
