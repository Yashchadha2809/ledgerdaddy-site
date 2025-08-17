# index.py
import os
from flask import Flask, send_file, Response

app = Flask(__name__)

# absolute path to your HTML beside this file
HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(HERE, "home_min.html")

@app.get("/")
def home():
    if not os.path.exists(HTML_PATH):
        # helpful error if file missing
        return Response("home_min.html not found next to index.py", 500, mimetype="text/plain")
    return send_file(HTML_PATH)

@app.get("/health")
def health():
    return {"ok": True}

# handle noisy favicon requests gracefully
@app.get("/favicon.ico")
def favicon():
    return Response(status=204)

# vercel looks for this WSGI handler
handler = app

if __name__ == "__main__":
    # local dev (optional): python index.py
    app.run(host="127.0.0.1", port=5000, debug=True)
