// /sw.js
const CACHE = 'ld-v2';

// Only list files that actually exist in production.
// Keep chat.html/styles.css/app.js if you really have them.
// You can add more later.
const URLS = [
  '/',                 // your root (routes to /home_min.html)
  '/home_min.html',    // fallback for navigations when offline
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/icon-512-maskable.png' // new maskable icon from manifest
  // '/chat.html',
  // '/styles.css',
  // '/app.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    // Robust pre-cache: try each URL; skip any that fail (prevents install from failing)
    for (const url of URLS) {
      try {
        const res = await fetch(url, { cache: 'no-store' });
        if (res.ok) await cache.put(url, res.clone());
      } catch (_) {
        // skip missing/broken assets
      }
    }
    self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)));
    self.clients.claim();
  })());
});

self.addEventListener('fetch', (event) => {
  event.respondWith((async () => {
    // Cache-first
    const cached = await caches.match(event.request);
    if (cached) return cached;

    try {
      // Network if not in cache
      return await fetch(event.request);
    } catch (_) {
      // Offline fallback for navigations
      if (event.request.mode === 'navigate') {
        return caches.match('/home_min.html') || Response.error();
      }
      return Response.error();
    }
  })());
});
