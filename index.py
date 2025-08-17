# index.py
import os
from pathlib import Path
from flask import Flask, Response, send_file

app = Flask(__name__)

APP_DIR = Path(__file__).resolve().parent
HOME = APP_DIR / "home_min.html"
SIGNUP = APP_DIR / "personal_sign_up.html"
LOGIN = APP_DIR / "log_in.html"

def serve_file(path: Path, not_found="File not found"):
    if path.exists():
        return send_file(path)
    return Response(not_found, status=404, mimetype="text/plain")

@app.get("/")
def home():
    return serve_file(HOME, "home_min.html not found")

@app.get("/personal-sign-up")
def personal_sign_up():
    return serve_file(SIGNUP, "personal_sign_up.html not found")

@app.get("/log-in")
def log_in():
    return serve_file(LOGIN, "log_in.html not found")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/favicon.ico")
@app.get("/favicon.png")
def favicon():
    return Response(status=204)

# Vercel WSGI entry
handler = app

if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
