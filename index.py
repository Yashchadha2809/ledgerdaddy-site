# index.py
import os, sqlite3, secrets, time, re
from flask import (
    Flask, request, render_template, redirect,
    url_for, session, flash, make_response
)

# -----------------------------------------------------------------------------
# App bootstrap (load templates from current directory)
# -----------------------------------------------------------------------------
app = Flask(__name__, template_folder=".")
app.secret_key = os.getenv("SECRET_KEY", "dev-change-me")  # set SECRET_KEY in prod
DB_PATH = os.getenv("DB_PATH", "db.sqlite3")

# Optional production-leaning cookie settings (tweak as needed)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

# -----------------------------------------------------------------------------
# DB helpers
# -----------------------------------------------------------------------------
def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
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

# Home page — this expects a file named "home_min.html" in the repo root.
# (If your file is named differently, change the template name below.)
@app.get("/")
def home():
    return render_template("home_min.html")

# ----- Personal Sign Up -----
# GET: render sign-up page (expects "personal_sign_up.html" in repo root)
@app.get("/auth/personal-sign-up")
def personal_sign_up():
    return render_template(
        "personal_sign_up.html",
        csrf=new_csrf(),
        next=request.args.get("next", "/auth/welcome")
    )

# POST: process sign-up
@app.post("/auth/personal-sign-up")
def personal_sign_up_post():
    form = request.form
    if not check_csrf(form.get("csrf")):
        flash("Your session expired. Please try again.", "error")
        return redirect(url_for("personal_sign_up"))

    name  = (form.get("name") or "").strip()
    email = (form.get("email") or "").strip().lower()
    phone = (form.get("phone") or "").strip()

    # Required fields
    if not name or not email:
        flash("Name and Email are required.", "error")
        return redirect(url_for("personal_sign_up"))

    # Basic email format check
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("personal_sign_up"))

    # Insert user
    try:
        with db() as con:
            con.execute(
                "INSERT INTO users (name, email, phone, created_at) VALUES (?,?,?,?)",
                (name, email, phone, int(time.time()))
            )
    except sqlite3.IntegrityError:
        flash("This email is already registered.", "error")
        return redirect(url_for("personal_sign_up"))

    # Save minimal session
    session["uid_email"] = email
    session["uid_name"] = name

    # Redirect
    nxt = form.get("next") or url_for("welcome")
    return redirect(nxt)

# Welcome page — expects "welcome.html" in the repo root
@app.get("/auth/welcome")
def welcome():
    name = session.get("uid_name", "there")
    email = session.get("uid_email", "")
    return make_response(render_template("welcome.html", name=name, email=email))

# Health check
@app.get("/health")
def health():
    return {"ok": True}

# WSGI entry for Vercel
handler = app

if __name__ == "__main__":
    # pip install flask
    app.run(host="127.0.0.1", port=5000, debug=True)
