# index.py
import os, sqlite3, secrets, time, re
from pathlib import Path
from flask import (
    Flask, request, redirect, url_for, session, flash, make_response, Response
)

# -----------------------------------------------------------------------------
# App bootstrap
# -----------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
HOME_FILE = APP_DIR / "home_min.html"

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-change-me")

# On Vercel, only /tmp is writable. Elsewhere, use DB_PATH or local file.
if os.getenv("VERCEL"):
    os.makedirs("/tmp", exist_ok=True)
    DB_PATH = "/tmp/db.sqlite3"
else:
    DB_PATH = os.getenv("DB_PATH", str(APP_DIR / "db.sqlite3"))

# -----------------------------------------------------------------------------
# DB helpers
# -----------------------------------------------------------------------------
def db():
    # check_same_thread=False helps under multi-threaded servers
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    # Create DB file if missing (especially important on cold starts in /tmp)
    with db() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE,
          phone TEXT,
          role TEXT DEFAULT 'personal',
          created_at INTEGER
        )
        """)
init_db()

# -----------------------------------------------------------------------------
# CSRF helpers
# -----------------------------------------------------------------------------
def new_csrf():
    token = secrets.token_urlsafe(20)
    session["csrf"] = token
    return token

def check_csrf(token):
    s = session.get("csrf")
    return bool(token and s and secrets.compare_digest(token, s))

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.get("/")
def home():
    if HOME_FILE.exists():
        return Response(HOME_FILE.read_text(encoding="utf-8"), mimetype="text/html")
    return Response("<h1>home_min.html not found</h1>", mimetype="text/html", status=404)

@app.get("/auth/personal-sign-up")
def personal_sign_up():
    csrf = new_csrf()
    next_url = request.args.get("next", url_for("welcome"))
    html = f"""<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sign up • Chadaddy</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900">
  <div class="max-w-md mx-auto mt-16 bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
    <h1 class="text-2xl font-bold">Create your account</h1>
    <p class="text-sm text-gray-600 mt-1">One-time sign up to unlock results across the site.</p>
    <form method="post" action="{url_for('personal_sign_up_post')}" class="grid gap-3 mt-5">
      <input type="hidden" name="csrf" value="{csrf}" />
      <input type="hidden" name="next" value="{next_url}" />
      <label class="grid gap-1 text-sm">
        <span>Name</span>
        <input name="name" class="border rounded-lg px-3 py-2" placeholder="Your name" required>
      </label>
      <label class="grid gap-1 text-sm">
        <span>Email</span>
        <input name="email" type="email" class="border rounded-lg px-3 py-2" placeholder="you@example.com" required>
      </label>
      <label class="grid gap-1 text-sm">
        <span>Phone / WhatsApp (optional)</span>
        <input name="phone" class="border rounded-lg px-3 py-2" placeholder="+91 9xxxx xxxxx">
      </label>
      <button class="bg-emerald-600 text-white py-2 rounded-lg mt-2">Create account</button>
      <a href="/" class="text-center text-sm text-cyan-700">← Back to home</a>
    </form>
  </div>
</body></html>"""
    return Response(html, mimetype="text/html")

@app.post("/auth/personal-sign-up")
def personal_sign_up_post():
    form = request.form
    if not check_csrf(form.get("csrf")):
        flash("Your session expired. Please try again.", "error")
        return redirect(url_for("personal_sign_up"))

    name  = (form.get("name") or "").strip()
    email = (form.get("email") or "").strip().lower()
    phone = (form.get("phone") or "").strip()

    if not name or not email:
        flash("Name and Email are required.", "error")
        return redirect(url_for("personal_sign_up"))

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("personal_sign_up"))

    try:
        with db() as con:
            con.execute(
                "INSERT INTO users (name, email, phone, created_at) VALUES (?,?,?,?)",
                (name, email, phone, int(time.time()))
            )
    except sqlite3.IntegrityError:
        # already exists — proceed as login
        pass

    session["uid_email"] = email
    session["uid_name"] = name

    nxt = form.get("next") or url_for("welcome")
    return redirect(nxt)

@app.get("/auth/welcome")
def welcome():
    name = session.get("uid_name", "there")
    email = session.get("uid_email", "")
    html = f"""<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Welcome • Chadaddy</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900">
  <div class="max-w-lg mx-auto mt-20 bg-white border border-gray-200 rounded-2xl p-6 text-center">
    <h1 class="text-3xl font-extrabold">Welcome, {name} 🎉</h1>
    <p class="mt-2 text-gray-600">Your account (<strong>{email}</strong>) is set. You can now access calculator, HS Finder, and chat results.</p>
    <div class="mt-6 grid gap-3">
      <a class="bg-emerald-600 text-white px-4 py-2 rounded-lg" href="/">Go to Home</a>
      <a class="border px-4 py-2 rounded-lg" href="/auth/personal-sign-up">Create another account</a>
    </div>
  </div>
</body></html>"""
    return Response(html, mimetype="text/html")

@app.get("/health")
def health():
    return {"ok": True, "db_path": DB_PATH, "vercel": bool(os.getenv("VERCEL"))}

# Vercel entry
handler = app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
