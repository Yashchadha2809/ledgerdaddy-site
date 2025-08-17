from flask import Flask, render_template_string

app = Flask(__name__)

homepage_html = r"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Chadaddy – Global AI Customs Platform</title>
  <meta name="description" content="Your AI trade partner — learn, calculate duties globally, and book verified brokers." />
  <meta name="theme-color" content="#1A237E" />
  <link rel="preconnect" href="https://images.unsplash.com" />
  <!-- Preload NEW hero photo -->
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
    /* NEW hero image */
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
      <a href="#signup" class="bg-emerald text-white px-4 py-2 rounded-lg hover:opacity-95">Sign up</a>
    </div>
  </header>

  <!-- ===== Sticky Mobile CTA (added Learn) ===== -->
  <div class="md:hidden fixed bottom-0 inset-x-0 z-40 bg-white/95 border-t border-gray-200 backdrop-blur sticky-shadow">
    <div class="max-w-7xl mx-auto px-3 py-2 grid grid-cols-4 gap-2">
      <a href="#calculator" class="text-center text-xs bg-emerald text-white py-2 rounded">Estimate</a>
      <a href="#marketplace" class="text-center text-xs bg-cyanBright text-black py-2 rounded">Broker</a>
      <a href="#chat" class="text-center text-xs bg-gray-900 text-white py-2 rounded">Chat</a>
      <a href="#learn" class="text-center text-xs bg-orange-500 text-white py-2 rounded">Learn</a>
    </div>
  </div>

  <!-- ===== Hero (NEW photo + extra CTA: Learn Import/Export) ===== -->
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
              <!-- Learn CTA (refined design) -->
              <a href="#learn" class="group relative inline-flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-white
                 bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-500 hover:opacity-95 transition">
                <!-- icon -->
                <svg class="h-5 w-5 opacity-90 group-hover:scale-110 transition-transform" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
                  <path d="M4 19.5V7.8a1 1 0 0 1 .6-.9l6-2.6a1 1 0 0 1 .8 0l6 2.6a1 1 0 0 1 .6.9v11.7" />
                  <path d="M12 6v13" />
                  <path d="M6 10l-2 1m16-1l-2 1" />
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

  <!-- ===== How it works ===== -->
  <section class="py-14 bg-white">
    <div class="max-w-7xl mx-auto px-6">
      <h2 class="text-3xl font-bold text-center">How It Works</h2>
      <div class="mt-8 grid md:grid-cols-3 gap-6">
        <div class="card p-6 bg-white rounded-xl border border-gray-200">
          <h3 class="font-semibold text-lg">1) Chat</h3>
          <p class="text-gray-600 mt-1">Ask anything about HS, duties, docs, Incoterms.</p>
          <a href="#chat" class="mt-4 inline-block text-cyanBright">Chat with Chadaddy →</a>
        </div>
        <div class="card p-6 bg-white rounded-xl border border-gray-200">
          <h3 class="font-semibold text-lg">2) Calculate</h3>
          <p class="text-gray-600 mt-1">Enter HS & value to see line-by-line duties.</p>
          <a href="#calculator" class="mt-4 inline-block text-cyanBright">Try Calculator →</a>
        </div>
        <div class="card p-6 bg-white rounded-xl border border-gray-200">
          <h3 class="font-semibold text-lg">3) Connect</h3>
          <p class="text-gray-600 mt-1">Book verified brokers & clear faster.</p>
          <a href="#marketplace" class="mt-4 inline-block text-cyanBright">Find a Broker →</a>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== Marketplace (sample grid) ===== -->
  <section id="marketplace" class="py-16 bg-gray-50">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex items-end justify-between gap-3">
        <h2 class="text-3xl font-bold">Find Your Broker</h2>
        <div class="hidden md:flex items-center gap-2">
          <input id="fSearch" class="border rounded-lg px-3 py-2" placeholder="Search broker or HS…" />
          <select id="fSort" class="border rounded-lg px-3 py-2">
            <option value="featured">Featured</option>
            <option value="rating">Rating</option>
            <option value="price">Price from</option>
            <option value="response">Response time</option>
          </select>
          <button id="openFilters" class="border rounded-lg px-3 py-2">Filters</button>
        </div>
      </div>

      <div id="brokGrid" class="mt-6 grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- two sample cards -->
        <article class="bg-white border border-gray-200 rounded-xl overflow-hidden">
          <img class="h-36 w-full object-cover" src="https://images.unsplash.com/photo-1556761175-4b46a572b786?q=80&w=800&auto=format&fit=crop" alt="Pacific Global">
          <div class="p-3">
            <div class="flex items-center justify-between">
              <div class="font-semibold">Pacific Global</div>
              <div class="text-xs px-2 py-0.5 rounded-full border border-emerald text-emerald">Verified</div>
            </div>
            <div class="text-xs text-gray-500 mt-1">IN • JNPT • Mundra</div>
            <div class="text-xs mt-1">Electronics, Chemicals</div>
            <div class="flex items-center justify-between mt-2">
              <div class="text-sm">★ 4.9 <span class="text-gray-500">(312)</span></div>
              <div class="text-sm">From <strong>₹ 6,500</strong></div>
            </div>
            <div class="mt-3 grid grid-cols-2 gap-2">
              <button class="border rounded-lg px-2 py-1">Get Quote</button>
              <button class="bg-cyanBright text-black rounded-lg px-2 py-1">Compare</button>
            </div>
          </div>
        </article>

        <article class="bg-white border border-gray-200 rounded-xl overflow-hidden">
          <img class="h-36 w-full object-cover" src="https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=800&auto=format&fit=crop" alt="Astra Customs">
          <div class="p-3">
            <div class="flex items-center justify-between">
              <div class="font-semibold">Astra Customs</div>
              <div class="text-xs px-2 py-0.5 rounded-full border border-emerald text-emerald">Verified</div>
            </div>
            <div class="text-xs text-gray-500 mt-1">IN • Mundra • Chennai</div>
            <div class="text-xs mt-1">Apparel, Furniture</div>
            <div class="flex items-center justify-between mt-2">
              <div class="text-sm">★ 4.7 <span class="text-gray-500">(201)</span></div>
              <div class="text-sm">From <strong>₹ 5,500</strong></div>
            </div>
            <div class="mt-3 grid grid-cols-2 gap-2">
              <button class="border rounded-lg px-2 py-1">Get Quote</button>
              <button class="bg-cyanBright text-black rounded-lg px-2 py-1">Compare</button>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- ===== Calculator (lead-gated) ===== -->
  <section id="calculator" class="py-16 bg-white">
    <div class="max-w-7xl mx-auto px-6">
      <h2 class="text-3xl font-bold">Global Duty & Landed Cost</h2>
      <div class="mt-6 grid md:grid-cols-2 gap-6">
        <form id="calcForm" class="bg-gray-50 border border-gray-200 rounded-xl p-4 grid gap-3">
          <div class="grid grid-cols-2 gap-3">
            <select id="cCountry" class="border rounded-lg px-3 py-2"><option>IN</option><option>US</option><option>EU</option><option>UK</option></select>
            <select id="cIncoterm" class="border rounded-lg px-3 py-2"><option value="CIF">CIF</option><option value="FOB">FOB</option><option value="EXW">EXW</option></select>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <input id="cHS" class="border rounded-lg px-3 py-2" placeholder="HS code e.g. 851713" required />
            <input id="cGoods" type="number" class="border rounded-lg px-3 py-2" placeholder="Goods Value" required />
          </div>
          <div class="grid grid-cols-3 gap-3">
            <input id="cFreight" type="number" class="border rounded-lg px-3 py-2" placeholder="Freight" />
            <input id="cIns" type="number" class="border rounded-lg px-3 py-2" placeholder="Insurance" />
            <input id="cOther" type="number" class="border rounded-lg px-3 py-2" placeholder="Other includable" />
          </div>
          <details class="p-3 border rounded-lg">
            <summary class="cursor-pointer font-medium">Advanced (optional)</summary>
            <div class="grid grid-cols-3 gap-3 mt-3">
              <input id="cDuty" type="number" class="border rounded-lg px-3 py-2" placeholder="Override duty %">
              <input id="cVat" type="number" class="border rounded-lg px-3 py-2" placeholder="VAT/IGST %">
              <input id="cAidc" type="number" class="border rounded-lg px-3 py-2" placeholder="AIDC/Cess %">
            </div>
          </details>
          <div class="flex items-center gap-3">
            <button class="bg-emerald text-white py-2 px-4 rounded-lg" type="submit">Calculate</button>
            <label class="text-sm flex items-center gap-2"><input id="ftaToggle" type="checkbox"> Apply FTA savings (demo)</label>
          </div>
          <p class="text-xs text-gray-600">Results show after a quick name & email check (one-time).</p>
        </form>

        <div>
          <h3 class="font-semibold mb-2">Breakdown</h3>
          <div class="overflow-hidden rounded-xl border border-gray-200">
            <table class="w-full text-sm">
              <tbody id="cTable" class="divide-y divide-gray-200">
                <tr><td class="px-3 py-3 text-center text-gray-500">No results yet — run a calculation.</td></tr>
              </tbody>
            </table>
          </div>
          <div id="hsSuggestBox" class="hidden mt-3 p-3 border rounded-lg">
            <strong>HS suggestions</strong>
            <ul id="hsSuggestList" class="list-disc ml-5 text-sm"></ul>
            <p class="text-xs text-gray-500 mt-1">Customs makes the final decision.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== HS Finder (lead-gated) ===== -->
  <section id="hsfinder" class="py-16 bg-gray-50">
    <div class="max-w-7xl mx-auto px-6">
      <h2 class="text-3xl font-bold">HS / HSN Finder</h2>
      <div class="mt-6 grid md:grid-cols-2 gap-6">
        <div class="bg-white border border-gray-200 rounded-xl p-4">
          <div class="grid gap-3">
            <select id="hsCountry" class="border rounded-lg px-3 py-2"><option>IN</option><option>US</option><option>EU</option><option>UK</option><option>AE</option><option>SG</option><option>AU</option><option>CA</option><option>MX</option><option>CN</option></select>
            <textarea id="hsDesc" rows="5" class="border rounded-lg px-3 py-2" placeholder="Describe your product (materials, function, use)…"></textarea>
            <div class="flex gap-3">
              <button id="hsRun" class="bg-emerald text-white px-4 py-2 rounded-lg">Find HS codes</button>
              <button id="hsReset" class="border px-4 py-2 rounded-lg">Reset</button>
            </div>
          </div>
        </div>
        <div id="hsResults" class="grid gap-3" aria-live="polite"></div>
      </div>
    </div>
  </section>

  <!-- ===== Learn (NEW simple section) ===== -->
  <section id="learn" class="py-16 bg-white">
    <div class="max-w-7xl mx-auto px-6">
      <h2 class="text-3xl font-bold">Learn Import/Export</h2>
      <p class="text-gray-600 mt-2 max-w-3xl">Step-by-step guides and micro-courses for students and businesses. Earn a free certificate and apply your HS knowledge directly in the calculator.</p>
      <div class="mt-6 grid md:grid-cols-3 gap-6">
        <div class="p-5 rounded-xl border bg-gray-50">
          <h3 class="font-semibold">HS Basics (30 min)</h3>
          <p class="text-sm text-gray-600">Chapters, headings, rules.</p>
          <a href="#hsfinder" class="mt-3 inline-block text-cyanBright">Use HS Finder →</a>
        </div>
        <div class="p-5 rounded-xl border bg-gray-50">
          <h3 class="font-semibold">Incoterms 2020 (20 min)</h3>
          <p class="text-sm text-gray-600">FOB vs CIF vs EXW.</p>
          <a href="#calculator" class="mt-3 inline-block text-cyanBright">Try Calculator →</a>
        </div>
        <div class="p-5 rounded-xl border bg-gray-50">
          <h3 class="font-semibold">Valuation (25 min)</h3>
          <p class="text-sm text-gray-600">What goes into customs value?</p>
          <a href="#chat" class="mt-3 inline-block text-cyanBright">Ask in Chat →</a>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== Chat (lead-gated responses) ===== -->
  <section id="chat" class="py-16 bg-gray-50">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex items-center justify-between">
        <h2 class="text-3xl font-bold">Chat with Chadaddy</h2>
        <span class="text-xs text-gray-500 hidden md:inline">Type “/hsfinder …” • Responses unlock after quick access form</span>
      </div>
      <div class="mt-6 grid lg:grid-cols-[260px,1fr,280px] gap-6">
        <aside class="bg-white border border-gray-200 rounded-xl p-3">
          <div class="flex items-center justify-between"><strong>History</strong><button id="newThread" class="text-xs border rounded px-2 py-1">New</button></div>
          <ul id="threads" class="mt-3 grid gap-2 text-sm"></ul>
        </aside>

        <section class="bg-white border border-gray-200 rounded-xl p-3">
          <div class="flex flex-wrap gap-2 text-xs">
            <button class="quick border rounded px-2 py-1" data-q="/hsfinder AirPods in IN">/hsfinder</button>
            <button class="quick border rounded px-2 py-1" data-q="/duty IN 8517 CIF 100000">/duty</button>
            <button class="quick border rounded px-2 py-1" data-q="/marketplace IN JNPT electronics">/marketplace</button>
            <button class="quick border rounded px-2 py-1" data-q="/news IN ports">/news</button>
            <button class="quick border rounded px-2 py-1" data-q="/products trending electronics">/products</button>
          </div>
          <div id="thread" class="mt-3 h-[52vh] overflow-auto grid gap-2 pr-1" aria-live="polite"></div>
          <form id="chatForm" class="mt-3 flex gap-2" autocomplete="off">
            <input id="chatInput" class="flex-1 border rounded-lg px-3 py-2" placeholder="Ask anything… (try: 'HS for LED bulbs in EU')" />
            <button class="bg-emerald text-white px-4 py-2 rounded-lg">Send</button>
          </form>
          <p class="text-xs text-gray-500 mt-2">We keep the last 30 messages per chat in your browser.</p>
        </section>

        <aside class="bg-white border border-gray-200 rounded-xl p-3">
          <strong>Saved calcs & docs</strong>
          <ul id="rightRail" class="mt-3 grid gap-2 text-sm"></ul>
        </aside>
      </div>
    </div>
  </section>

  <!-- ===== News ===== -->
  <section id="news" class="py-16 bg-white">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 class="text-3xl font-bold">News & Alerts</h2>
          <span class="text-xs px-2 py-1 rounded-full border border-cyanBright text-cyanBright">AI summaries</span>
        </div>
        <div class="flex gap-2">
          <select id="newsCountry" class="border rounded-lg px-3 py-2"><option>ALL</option><option>IN</option><option>US</option><option>EU</option></select>
          <select id="newsTopic" class="border rounded-lg px-3 py-2"><option>All topics</option><option>Ports</option><option>Tariff</option><option>Compliance</option></select>
          <button id="newsSub" class="bg-cyanBright text-black px-4 py-2 rounded-lg">Subscribe</button>
        </div>
      </div>
      <div id="newsList" class="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 gap-6"></div>
    </div>
  </section>

  <!-- ===== Pricing (stub) ===== -->
  <section id="pricing" class="py-16 bg-gray-50">
    <div class="max-w-7xl mx-auto px-6">
      <h2 class="text-3xl font-bold">Pricing</h2>
      <div class="mt-6 grid md:grid-cols-3 gap-6">
        <div class="p-6 rounded-2xl border bg-white">
          <h3 class="font-semibold">Free</h3>
          <p class="text-sm text-gray-600">Chat + HS finder (limited)</p>
          <p class="text-3xl font-extrabold mt-2">$0</p>
          <a href="#signup" class="mt-4 inline-block bg-emerald text-white px-4 py-2 rounded-lg">Start</a>
        </div>
        <div class="p-6 rounded-2xl border bg-white ring-2 ring-cyanBright">
          <h3 class="font-semibold">Pro</h3>
          <p class="text-sm text-gray-600">Calculator PDFs, alerts, priority</p>
          <p class="text-3xl font-extrabold mt-2">$9<span class="text-base">/mo</span></p>
          <a href="#signup" class="mt-4 inline-block bg-cyanBright text-black px-4 py-2 rounded-lg">Upgrade</a>
        </div>
        <div class="p-6 rounded-2xl border bg-white">
          <h3 class="font-semibold">Team</h3>
          <p class="text-sm text-gray-600">Brokers, RFP, escrow</p>
          <p class="text-3xl font-extrabold mt-2">$49<span class="text-base">/mo</span></p>
          <a href="#signup" class="mt-4 inline-block border px-4 py-2 rounded-lg">Contact sales</a>
        </div>
      </div>
    </div>
  </section>

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

  <!-- ===== Lead Gate Modal ===== -->
  <div id="leadModal" class="hidden fixed inset-0 z-50 items-center justify-center bg-black/50 p-3">
    <div class="max-w-lg w-full bg-white border border-gray-200 rounded-xl p-4">
      <div class="flex items-center justify-between">
        <h3 class="font-semibold">Access your free result</h3>
        <button id="leadClose" class="border rounded px-2 py-1">✕</button>
      </div>
      <p class="text-sm text-gray-600">Enter your details once to unlock results across the site.</p>
      <form id="leadForm" class="grid sm:grid-cols-2 gap-3 mt-3">
        <input id="leadName" class="border rounded-lg px-3 py-2 sm:col-span-2" placeholder="Your name" required />
        <input id="leadEmail" type="email" class="border rounded-lg px-3 py-2 sm:col-span-2" placeholder="Email" required />
        <input id="leadWA" class="border rounded-lg px-3 py-2 sm:col-span-2" placeholder="Phone / WhatsApp (optional)" />
        <button class="sm:col-span-2 bg-emerald text-white py-2 rounded-lg">Unlock Results</button>
      </form>
      <p class="text-xs text-gray-500 mt-2">By continuing you agree to receive your results via email.</p>
    </div>
  </div>

  <!-- ===== App JS (lead gating + stubs) ===== -->
  <script>
    const $ = s=>document.querySelector(s); const $$=s=>Array.from(document.querySelectorAll(s));
    $('#year').textContent = new Date().getFullYear();

    // Activity ticker
    const ports=['JNPT','Mundra','Chennai','Rotterdam','LA','Felixstowe','Dubai','Singapore']; let ti=0;
    setInterval(()=>{ const n=Math.floor(Math.random()*6)+3; $('#ticker').textContent = `${n} shipments cleared today at ${ports[ti++%ports.length]}`; }, 4500);

    // Lead gate
    const GATE_KEY='chadaddy_lead';
    const hasLead = () => !!localStorage.getItem(GATE_KEY);
    function openGate(){ $('#leadModal').classList.remove('hidden'); $('#leadModal').classList.add('flex'); }
    function closeGate(){ $('#leadModal').classList.add('hidden'); $('#leadModal').classList.remove('flex'); }
    $('#leadClose').addEventListener('click', closeGate);
    $('#leadForm').addEventListener('submit', (e)=>{
      e.preventDefault();
      const name=$('#leadName').value.trim(); const email=$('#leadEmail').value.trim(); const wa=$('#leadWA').value.trim();
      if(!name || !email) return;
      localStorage.setItem(GATE_KEY, JSON.stringify({name,email,wa,ts:Date.now()}));
      closeGate();
      const t=document.createElement('div'); t.textContent='Access granted'; t.className='fixed bottom-24 right-4 bg-gray-900 text-white text-sm px-3 py-2 rounded-lg shadow'; document.body.appendChild(t); setTimeout(()=>t.remove(),1400);
      if(window.__afterGate){ const cb=window.__afterGate; window.__afterGate=null; cb(); }
    });
    function requireLead(cb){ if(hasLead()) cb(); else { window.__afterGate=cb; openGate(); } }

    // Hero teaser
    const ccy = {IN:'₹', US:'$', EU:'€', UK:'£'};
    function runQuickTeaser(){
      const av=Number($('#tzAV').value||0), country=$('#tzCountry').value;
      if(!av){ $('#tzOut').innerHTML='<span class="text-red-600">Enter a value</span>'; return; }
      const dutyMap={IN:0.10,US:0.03,EU:0.05,UK:0.05}; const igstMap={IN:0.18,US:0.009,EU:0.20,UK:0.20};
      const bcd=av*(dutyMap[country]||0.1); const sws=(country==='IN')?bcd*0.10:0; const sub=av+bcd+sws; const vat=sub*(igstMap[country]||0.18); const total=sub+vat;
      $('#tzOut').innerHTML = `<span class="inline-block mr-2 px-2 py-1 rounded bg-gray-100">Est. duties: ${ccy[country]||'₹'} ${(bcd+sws+vat).toFixed(0)}</span>
      <span class="inline-block px-2 py-1 rounded bg-green-50 text-emerald">Total: ${ccy[country]||'₹'} ${Math.round(total).toLocaleString()}</span>`;
    }
    $('#tzBtn').addEventListener('click', ()=> requireLead(runQuickTeaser));

    // Calculator
    function addRow(label,basis,rate,amount){ return `<tr><td class="px-3 py-2">${label}</td><td class="px-3 py-2 text-right">${basis?.toLocaleString?.()||'-'}</td><td class="px-3 py-2 text-right">${rate?rate+'%':'—'}</td><td class="px-3 py-2 text-right font-semibold">${Math.round(amount).toLocaleString()}</td></tr>`; }
    function runCalc(){
      const country=$('#cCountry').value, hs=$('#cHS').value.trim(), goods=+($('#cGoods').value||0), freight=+($('#cFreight').value||0), ins=+($('#cIns').value||0), other=+($('#cOther').value||0);
      const override=+($('#cDuty').value||NaN), vatIn=+($('#cVat').value||NaN), aidcIn=+($('#cAidc').value||NaN), fta=$('#ftaToggle').checked;
      let AV=goods+freight+ins+other;
      let baseDuty=isNaN(override)?({IN:10,US:3,EU:5,UK:5}[country]||10):override;
      if(fta) baseDuty=Math.max(0, baseDuty-5);
      const vatRate=isNaN(vatIn)?({IN:18,US:0.9,EU:20,UK:20}[country]||18):vatIn;
      const aidcRate=isNaN(aidcIn)?({IN:0,US:0,EU:0,UK:0}[country]||0):aidcIn;

      const BCD=AV*baseDuty/100, SWS=country==='IN'?BCD*0.10:0, AIDC=AV*aidcRate/100;
      const sub=AV+BCD+SWS+AIDC, VAT=sub*(vatRate/100), total=sub+VAT;

      const tb=$('#cTable'); tb.innerHTML = addRow('Assessable Value (AV)', AV, null, AV)
        + addRow('BCD', AV, baseDuty, BCD)
        + (SWS? addRow('SWS (10% of BCD)', BCD, 10, SWS):'')
        + (AIDC? addRow('AIDC/Cess', AV, aidcRate, AIDC):'')
        + addRow(country==='IN'?'IGST':'VAT', sub, vatRate, VAT)
        + `<tr class="bg-gray-50 font-semibold"><td class="px-3 py-2" colspan="3">Total Landed Cost</td><td class="px-3 py-2 text-right">${Math.round(total).toLocaleString()}</td></tr>`;
      if(hs.length<6){ $('#hsSuggestBox').classList.remove('hidden'); $('#hsSuggestList').innerHTML=['851713 – Phones','851762 – Comm. equip','850760 – Li-ion cells'].map((s,i)=>`<li>${s} <span class="text-xs text-gray-500">confidence ${(85-i*10)}%</span></li>`).join(''); } else { $('#hsSuggestBox').classList.add('hidden'); }
    }
    $('#calcForm').addEventListener('submit',(e)=>{ e.preventDefault(); requireLead(runCalc); });

    // HS Finder
    function runHsFinder(){
      const desc=$('#hsDesc').value.trim(); if(!desc) return alert('Please describe your product');
      const res=[{code:'851713',title:'Smartphones',conf:0.88,examples:['Android phone','iPhone']},{code:'851762',title:'Comm. equipment',conf:0.72,examples:['Wi-Fi router','LTE module']},{code:'851830',title:'Headphones/earbuds',conf:0.64,examples:['TWS earbuds','Headset']}];
      $('#hsResults').innerHTML = res.map(r=>`
        <div class="p-3 border rounded-lg bg-white">
          <div class="flex items-center justify-between">
            <div class="font-semibold">${r.code} — ${r.title}</div>
            <div class="text-xs px-2 py-0.5 rounded-full border">${Math.round(r.conf*100)}%</div>
          </div>
          <div class="text-xs text-gray-500">Examples: ${r.examples.join(', ')}</div>
          <a href="#calculator" class="mt-2 inline-block text-cyanBright text-sm">Open in calculator →</a>
        </div>`).join('');
    }
    $('#hsRun').addEventListener('click', ()=> requireLead(runHsFinder));
    $('#hsReset').addEventListener('click',()=>{ $('#hsDesc').value=''; $('#hsResults').innerHTML=''; });

    // Chat (lead-gated responses)
    const threadEl=$('#thread'); const savedKey='chadaddy_thread_v2';
    let messages=JSON.parse(localStorage.getItem(savedKey)||'[]');
    function renderChat(){ threadEl.innerHTML = messages.map(m=>`<div class="${m.role==='user'?'ml-auto bg-cyanBright text-black':'mr-auto bg-gray-100 text-gray-900'} px-3 py-2 rounded-xl max-w-[85%]">${m.text}</div>`).join(''); threadEl.scrollTop = threadEl.scrollHeight; }
    function addMsg(role,text){ messages.push({role,text,t:Date.now()}); if(messages.length>30) messages=messages.slice(-30); localStorage.setItem(savedKey,JSON.stringify(messages)); renderChat(); }
    renderChat();
    $('#chatForm').addEventListener('submit',(e)=>{ e.preventDefault(); const val=$('#chatInput').value.trim(); if(!val) return; addMsg('user',val);
      requireLead(()=>{ let reply="I'm a demo assistant. Connect API for live answers.";
        if(val.startsWith('/hsfinder')) reply="HS finder: 851713 (88%), 851762 (72%), 851830 (64%).";
        if(val.startsWith('/duty')) reply="Duty (demo): BCD 10%, IGST/VAT 18–20% depending on country.";
        if(val.startsWith('/marketplace')) reply="Try brokers: Pacific Global, Astra Customs, Metro ACI.";
        if(val.startsWith('/news')) reply="Latest: JNPT advisory; EU CET update; US FDA pilot.";
        if(val.startsWith('/products')) reply="Trending: Smartphones, LEDs, Sneakers, Coffee.";
        setTimeout(()=>addMsg('assistant',reply),250);
      });
      $('#chatInput').value='';
    });

    // News
    const NEWS=[
      {id:1,country:'IN',topic:'Ports',title:'JNPT issues advisory on weekend cut-off',sev:'Medium'},
      {id:2,country:'EU',topic:'Tariff',title:'EU updates CET for electronics',sev:'High'},
      {id:3,country:'US',topic:'Compliance',title:'New FDA prior-notice pilot',sev:'Low'}
    ];
    function sevBadge(sev){ const map={High:'border-accentOrange text-accentOrange',Medium:'border-yellow-500 text-yellow-600',Low:'border-emerald text-emerald'}; return map[sev]||'border'; }
    function renderNews(list=NEWS){ $('#newsList').innerHTML = list.map(n=>`
      <article class="bg-white border border-gray-200 rounded-xl p-4">
        <div class="text-xs mb-2 flex items-center gap-2">
          <span class="px-2 py-0.5 rounded-full border">${n.country}</span>
          <span class="px-2 py-0.5 rounded-full border">${n.topic}</span>
          <span class="px-2 py-0.5 rounded-full ${sevBadge(n.sev)} border">${n.sev}</span>
        </div>
        <div class="font-semibold">${n.title}</div>
        <a class="text-cyanBright text-sm mt-2 inline-block" href="#news">Subscribe for alerts →</a>
      </article>`).join(''); }
    renderNews();
    $('#newsCountry')?.addEventListener('change',e=>{ const v=e.target.value; renderNews(v==='ALL'?NEWS:NEWS.filter(n=>n.country===v)); });
    $('#newsTopic')?.addEventListener('change',e=>{ const v=e.target.value; renderNews(v==='All topics'?NEWS:NEWS.filter(n=>n.topic===v)); });

    // Newsletter toast
    $('#nlBtn').addEventListener('click',(e)=>{ e.preventDefault(); const t=document.createElement('div'); t.textContent='Subscribed'; t.className='fixed bottom-24 right-4 bg-gray-900 text-white text-sm px-3 py-2 rounded-lg shadow'; document.body.appendChild(t); setTimeout(()=>t.remove(),1400); });
  </script>
</body>
</html>"""

@app.route("/")
def home():
    return render_template_string(homepage_html)

# Optional lightweight health check
@app.route("/api/health")
def health():
    return {"ok": True}

# Local run (Vercel ignores this, but handy for dev)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
