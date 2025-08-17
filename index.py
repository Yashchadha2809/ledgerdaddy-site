# index.py
from flask import Flask, Response
from pathlib import Path

app = Flask(__name__)
APP_DIR = Path(__file__).resolve().parent
HOME_FILE = APP_DIR / "home_min.html"

@app.get("/")
def home():
    if HOME_FILE.exists():
        return Response(HOME_FILE.read_text(encoding="utf-8"), mimetype="text/html")
    return Response("<h1>home_min.html not found</h1>", mimetype="text/html", status=404)

@app.get("/health")
def health():
    return {"ok": True}

# Vercel entrypoint
handler = app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
