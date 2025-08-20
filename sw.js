// /sw.js
const CACHE = 'ld-v1';
const URLS = [
  '/',               // root
  '/home_min.html',  // your "/" routes here
  // Add more ONLY after confirming they load in prod:
  // '/chat.html',
  // '/styles.css',
  // '/app.js',
  // '/icons/icon-192.png',
  // '/icons/icon-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    for (const url of URLS) {
      try {
        const res = await fetch(url, { cache: 'no-store' });
        if (res.ok) await cache.put(url, res.clone());
      } catch (_) {
        // Skip missing/broken assets to avoid failing install
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
    const cached = await caches.match(event.request);
    if (cached) return cached;
    try {
      return await fetch(event.request);
    } catch (_) {
      // Fallback for navigations when offline
      if (event.request.mode === 'navigate') {
        return caches.match('/home_min.html') || Response.error();
      }
      return Response.error();
    }
  })());
});
