# index.py
import os, sqlite3, secrets, time, re
from flask import (
    Flask, request, render_template_string, redirect,
    url_for, session, flash, make_response, Response
)

# -----------------------------------------------------------------------------
# App bootstrap
# -----------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-change-me")  # set SECRET_KEY in prod
DB_PATH = os.getenv("DB_PATH", "db.sqlite3")

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
# Your existing homepage HTML (served directly from Python)
# -----------------------------------------------------------------------------
HOME_HTML = r"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Chadaddy – Global AI Customs Platform</title>
  <meta name="description" content="Your AI trade partner — learn, calculate duties globally, and book verified brokers." />
  <meta name="theme-color" content="#1A237E" />
  <link rel="preconnect" href="https://images.unsplash.com" />
  <link rel="preload" as="image"
        href="https://images.unsplash.com/photo-1586521995568-39ef16c6934d?q=80&w=1920&auto=format&fit=crop" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors:{ indigoDeep:"#1A237E", emerald:"#2E7D32", cyanBright:"#00BCD4", accentOrange:"#FF7043" },
          boxShadow:{ lift:"0 14px 34px rgba(0,0,0,.12)" }
        }
      }
    }
  </script>
  <style>
    .card{transition:transform .12s ease, box-shadow .2s ease}
    .card:hover{transform:translateY(-2px); box-shadow:0 14px 34px rgba(0,0,0,.14)}
    .sticky-shadow{box-shadow:0 8px 18px rgba(0,0,0,.08)}
    .hero-img{background:url('https://images.unsplash.com/photo-1586521995568-39ef16c6934d?q=80&w=1920&auto=format&fit=crop') center/cover no-repeat;}
  </style>
</head>
<body class="bg-gray-50 text-gray-900">
  <!-- ===== Topbar (day-only) ===== -->
  <header class="fixed top-0 inset-x-0 z-50 border-b border-gray-200 bg-white/90 backdrop-blur">
    <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="#home" class="flex items-center gap-2" aria-label="Chadaddy home">
        <span class="grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-tr from-cyanBright to-emerald text-white font-extrabold shadow">◆</span>
        <span class="text-xl font-bold text-indigoDeep">Chadaddy</span>
        <span class="ml-2 hidden sm:inline-flex text-[11px] px-2 py-0.5 rounded-full border border-cyanBright/40 text-cyanBright">AI Customs</span>
      </a>
      <nav class="hidden md:flex items-center gap-6 text-sm font-medium" aria-label="Main">
        <a href="#marketplace" class="hover:text-cyanBright">Marketplace</a>
        <a href="#calculator" class="hover:text-cyanBright">Calculator</a>
        <a href="#hsfinder" class="hover:text-cyanBright">HS Finder</a>
        <a href="#chat" class="hover:text-cyanBright">Chat</a>
        <a href="#news" class="hover:text-cyanBright">News</a>
        <a href="#learn" class="hover:text-cyanBright">Academy</a>
        <a href="#pricing" class="hover:text-cyanBright">Pricing</a>
      </nav>
      <!-- Changed Sign up button to point to Flask route -->
      <a href="/auth/personal-sign-up" class="bg-emerald text-white px-4 py-2 rounded-lg hover:opacity-95">Sign up</a>
    </div>
  </header>

  <!-- ===== Sticky Mobile CTA ===== -->
  <div class="md:hidden fixed bottom-0 inset-x-0 z-40 bg-white/95 border-t border-gray-200 backdrop-blur sticky-shadow">
    <div class="max-w-7xl mx-auto px-3 py-2 grid grid-cols-4 gap-2">
      <a href="#calculator" class="text-center text-xs bg-emerald text-white py-2 rounded">Estimate</a>
      <a href="#marketplace" class="text-center text-xs bg-cyanBright text-black py-2 rounded">Broker</a>
      <a href="#chat" class="text-center text-xs bg-gray-900 text-white py-2 rounded">Chat</a>
      <a href="#learn" class="text-center text-xs bg-orange-500 text-white py-2 rounded">Learn</a>
    </div>
  </div>

  <!-- ===== Hero ===== -->
  <section id="home" class="pt-28 md:pt-32 pb-12 text-white">
    <div class="hero-img">
      <div class="backdrop-brightness-90 bg-gradient-to-r from-indigoDeep/70 to-cyanBright/60">
        <div class="max-w-7xl mx-auto px-4 py-14 grid md:grid-cols-2 gap-8 items-center">
          <div>
            <h1 class="text-4xl md:text-5xl font-extrabold leading-tight">Your AI Trade Partner — Learn, Calculate, Clear.</h1>
            <p class="mt-3 text-lg text-white/95">Ask questions like ChatGPT, find HS codes, calculate duties globally, and book verified brokers.</p>
            <div class="mt-6 grid gap-3 md:flex md:flex-row">
              <a href="#calculator" class="bg-emerald text-white px-6 py-3 rounded-xl font-semibold">Get Duty Estimate</a>
              <a href="#marketplace" class="bg-gray-900 text-white px-6 py-3 rounded-xl font-semibold">Find Broker</a>
              <a href="#chat" class="bg-white text-indigoDeep px-6 py-3 rounded-xl font-semibold hover:bg-gray-100">Start Free Chat</a>
              <a href="#learn"
                 class="flex items-center justify-center gap-2 bg-gradient-to-r from-cyanBright to-emerald text-white px-6 py-3 rounded-xl font-semibold shadow-md hover:shadow-lg hover:scale-[1.02] transition">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 6v12m0-12c-1.5 0-3-.5-4.5-1.5S4.5 3 3 3v18c1.5 0 3 .5 4.5 1.5S10.5 21 12 21m0-15c1.5 0 3-.5 4.5-1.5S19.5 3 21 3v18c-1.5 0-3 .5-4.5 1.5S13.5 21 12 21" />
                </svg>
                Learn Import/Export
              </a>
            </div>
            <div class="mt-6 flex flex-wrap gap-4 text-sm text-white/95">
              <span class="px-3 py-1 rounded-full border border-white/40"><strong>★ 4.9</strong> avg</span>
              <span class="px-3 py-1 rounded-full border border-white/40">10,000+ duty estimates</span>
              <span class="px-3 py-1 rounded-full border border-white/40">2,000+ verified CHAs</span>
              <span id="ticker" class="px-3 py-1 rounded-full border border-white/40">5 shipments cleared today at JNPT</span>
            </div>
          </div>

          <!-- Calculator Teaser (lead-gated) -->
          <div class="bg-white text-gray-900 rounded-2xl p-4 shadow">
            <p class="font-semibold">Quick Duty Teaser</p>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-3">
              <select id="tzCountry" class="border rounded-lg px-3 py-2">
                <option>IN</option><option>US</option><option>EU</option><option>UK</option>
              </select>
              <input id="tzHS" class="border rounded-lg px-3 py-2" placeholder="HS e.g. 8517" />
              <input id="tzAV" type="number" class="border rounded-lg px-3 py-2" placeholder="Value e.g. 100000" />
            </div>
            <button id="tzBtn" class="mt-3 w-full bg-emerald text-white py-2 rounded-lg">Quick Estimate</button>
            <div id="tzOut" class="mt-3 text-sm"></div>
            <p class="text-xs text-gray-500 mt-1">Enter values freely; results require name & email (once).</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- (Sections omitted for brevity in this snippet — keep your full page content here) -->

  <!-- ===== Footer ===== -->
  <footer class="bg-gray-900 text-gray-300 py-12 mt-20">
    <div class="max-w-7xl mx-auto px-6 grid md:grid-cols-4 gap-6">
      <div>
        <h4 class="font-semibold text-white mb-3">Chadaddy</h4>
        <p>AI-powered customs platform to ship smarter worldwide.</p>
      </div>
      <div>
        <h4 class="font-semibold text-white mb-3">Quick Links</h4>
        <ul class="space-y-2 text-sm">
          <li><a href="#learn">Academy</a></li>
          <li><a href="#marketplace">Ports we cover</a></li>
          <li><a href="#hsfinder">HS code index</a></li>
        </ul>
      </div>
      <div>
        <h4 class="font-semibold text-white mb-3">Legal</h4>
        <ul class="space-y-2 text-sm">
          <li><a href="#">Privacy</a></li>
          <li><a href="#">Terms</a></li>
          <li><a href="#">Refunds</a></li>
        </ul>
      </div>
      <div>
        <h4 class="font-semibold text-white mb-3">Stay Updated</h4>
        <form class="flex">
          <input id="nlEmail" type="email" placeholder="Your email" class="p-2 rounded-l w-full text-gray-900" />
          <button id="nlBtn" class="bg-emerald px-4 rounded-r">→</button>
        </form>
        <a href="https://wa.me/0000000000" class="inline-block mt-3 text-sm underline">WhatsApp</a>
      </div>
    </div>
    <p class="text-center text-sm mt-8">© <span id="year"></span> Chadaddy. All rights reserved.</p>
  </footer>

  <!-- ===== Lead Gate Modal, Scripts, etc. — keep your existing JS here ===== -->
  <script>
    const $ = s=>document.querySelector(s);
    $('#year').textContent = new Date().getFullYear();
    const ports=['JNPT','Mundra','Chennai','Rotterdam','LA','Felixstowe','Dubai','Singapore']; let ti=0;
    setInterval(()=>{ const n=Math.floor(Math.random()*6)+3; const el=document.getElementById('ticker'); if(el){ el.textContent = `${n} shipments cleared today at ${ports[ti++%ports.length]}`;}}, 4500);
    // (Keep the rest of your existing JS here unchanged)
  </script>
</body>
</html>
"""

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.get("/")
def home():
    # Serve your full homepage from Python
    return Response(HOME_HTML, mimetype="text/html; charset=utf-8")

# --- Personal Sign Up (DB + CSRF) -------------------------------------------

SIGNUP_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Personal Sign Up – Chadaddy</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-gray-50 text-gray-900 flex items-center justify-center py-10">
  <div class="w-full max-w-md bg-white border border-gray-200 rounded-2xl shadow p-6">
    <a href="/" class="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700">
      ← Back to home
    </a>
    <h1 class="mt-2 text-2xl font-bold">Create your account</h1>
    <p class="text-sm text-gray-600">Unlock calculators, chat, and HS finder.</p>

    {% with msgs = get_flashed_messages(with_categories=True) %}
      {% if msgs %}
        <div class="mt-3 space-y-2">
          {% for cat, msg in msgs %}
            <div class="text-sm px-3 py-2 rounded border
                 {% if cat == 'error' %} border-red-300 text-red-700 bg-red-50
                 {% else %} border-emerald-300 text-emerald-800 bg-emerald-50 {% endif %}">
              {{ msg }}
            </div>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}

    <form class="mt-4 grid gap-3" method="post" action="{{ url_for('personal_sign_up_post') }}">
      <input type="hidden" name="csrf" value="{{ csrf }}">
      <input type="hidden" name="next" value="{{ next }}">

      <div class="grid gap-1">
        <label class="text-sm font-medium">Full name</label>
        <input name="name" required class="border rounded-lg px-3 py-2" placeholder="e.g., Alex Kumar">
      </div>

      <div class="grid gap-1">
        <label class="text-sm font-medium">Email</label>
        <input name="email" type="email" required class="border rounded-lg px-3 py-2" placeholder="you@company.com">
      </div>

      <div class="grid gap-1">
        <label class="text-sm font-medium">Phone / WhatsApp (optional)</label>
        <input name="phone" class="border rounded-lg px-3 py-2" placeholder="+91 98xxxxxxx">
      </div>

      <button class="mt-2 bg-emerald text-white py-2 rounded-lg">Create account</button>
    </form>
    <p class="mt-3 text-xs text-gray-500">By continuing, you agree to our Terms and Privacy Policy.</p>
  </div>
</body>
</html>
"""

WELCOME_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Welcome – Chadaddy</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-gray-50 text-gray-900 flex items-center justify-center py-10">
  <div class="w-full max-w-lg bg-white border border-gray-200 rounded-2xl shadow p-6 text-center">
    <h1 class="text-2xl font-bold">Welcome, {{ name }} 🎉</h1>
    <p class="mt-2 text-gray-700">We’ve created your account with <strong>{{ email }}</strong>.</p>
    <div class="mt-6 grid gap-3">
      <a class="bg-emerald text-white py-2 rounded-lg" href="/">Go to Homepage</a>
      <a class="border py-2 rounded-lg" href="/#calculator">Open Calculator</a>
      <a class="border py-2 rounded-lg" href="/#chat">Start Chat</a>
    </div>
  </div>
</body>
</html>
"""

@app.get("/auth/personal-sign-up")
def personal_sign_up():
    return render_template_string(
        SIGNUP_HTML,
        csrf=new_csrf(),
        next=request.args.get("next", url_for("welcome"))
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
    return make_response(render_template_string(WELCOME_HTML, name=name, email=email))

# -----------------------------------------------------------------------------
# Health & Vercel WSGI entry
# -----------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"ok": True}

# For Vercel:
handler = app

if __name__ == "__main__":
    # pip install flask
    app.run(host="127.0.0.1", port=5000, debug=True)
