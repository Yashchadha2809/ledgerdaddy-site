// /sw.js
const CACHE = 'ld-v3'; // bump when you change this file

// Only list files that truly exist in production.
const URLS = [
  '/',                 // resolves to /home_min.html via your rewrite
  '/home_min.html',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/icon-512-maskable.png'
];

// Optional: speed up navigations while SW boots
self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    // Clean old caches
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)));

    // Enable navigation preload where supported
    if ('navigationPreload' in self.registration) {
      try { await self.registration.navigationPreload.enable(); } catch (_) {}
    }
    self.clients.claim();
  })());
});

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);

    // Precache each URL; ignore failures so install never bombs
    for (const url of URLS) {
      try {
        const req = new Request(url, { cache: 'no-store', credentials: 'same-origin' });
        const res = await fetch(req);
        // cache only good, same-origin, non-redirect responses
        if (res && res.ok && res.type === 'basic') {
          await cache.put(url, res.clone());
        }
      } catch (_) { /* skip missing/broken assets */ }
    }
    self.skipWaiting();
  })());
});

self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Only handle same-origin requests; let cross-origin pass through.
  const isSameOrigin = new URL(request.url).origin === self.location.origin;
  if (!isSameOrigin) return;

  event.respondWith((async () => {
    // 1) Cache-first for static assets we precached
    const cached = await caches.match(request);
    if (cached) return cached;

    // 2) Try network (use navigation preload if available for navigations)
    try {
      if (request.mode === 'navigate' && 'navigationPreload' in self.registration) {
        const preload = await event.preloadResponse;
        if (preload) return preload;
      }
      const fresh = await fetch(request);
      // Optionally cache successful GETs for later (basic only)
      if (request.method === 'GET' && fresh.ok && fresh.type === 'basic') {
        const cache = await caches.open(CACHE);
        cache.put(request, fresh.clone());
      }
      return fresh;
    } catch (_) {
      // 3) Offline fallback for navigations
      if (request.mode === 'navigate') {
        return (await caches.match('/home_min.html')) || Response.error();
      }
      return Response.error();
    }
  })());
});
