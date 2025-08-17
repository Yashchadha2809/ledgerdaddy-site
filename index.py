import os, sqlite3, secrets, time, re
from flask import (
    Flask, request, render_template, redirect,
    url_for, session, flash, make_response
)
from vercel_serverless_wsgi import serverless_wsgi

# -----------------------------------------------------------------------------
# App bootstrap
#   - template_folder=".." so we can keep HTML files in the repo root.
# -----------------------------------------------------------------------------
app = Flask(__name__, template_folder="..")
app.secret_key = os.getenv("SECRET_KEY", "dev-change-me")
DB_PATH = os.getenv("DB_PATH", "db.sqlite3")

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
# Routes (expecting HTML files in the repo root):
#   - home_min.html
#   - personal_sign_up.html
#   - welcome.html
# -----------------------------------------------------------------------------
@app.get("/")
def home():
    # If your main file is named differently, change here:
    return render_template("home_min.html")

@app.get("/auth/personal-sign-up")
def personal_sign_up():
    return render_template(
        "personal_sign_up.html",
        csrf=new_csrf(),
        next=request.args.get("next", "/auth/welcome")
    )

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
        flash("This email is already registered.", "error")
        return redirect(url_for("personal_sign_up"))

    session["uid_email"] = email
    session["uid_name"] = name

    nxt = form.get("next") or url_for("welcome")
    return redirect(nxt)

@app.get("/auth/welcome")
def welcome():
    name = session.get("uid_name", "there")
    email = session.get("uid_email", "")
    return make_response(render_template("welcome.html", name=name, email=email))

@app.get("/health")
def health():
    return {"ok": True}

# -----------------------------------------------------------------------------
# Vercel serverless function entry
# -----------------------------------------------------------------------------
def handler(event, context):
    # Wrap the Flask WSGI app for Vercel
    return serverless_wsgi.handle_request(app, event, context)

# For local dev: `python api/index.py`
if __name__ == "__main__":
    app.run(port=5000, debug=True)
