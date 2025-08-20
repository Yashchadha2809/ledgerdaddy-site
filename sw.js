const CACHE = 'ld-v1';
const URLS = [
  '/',               // ensure this resolves to your main page
  '/home_min.html',  // include the page you route "/" to
  // Add only files that actually exist in production:
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
      } catch (e) {
        // Skip missing/broken assets to avoid failing the whole install
        // console.warn('SW skip caching', url, e);
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
      const res = await fetch(event.request);
      return res;
    } catch (e) {
      // Optional: return fallback page for navigations
      if (event.request.mode === 'navigate') {
        return caches.match('/home_min.html') || Response.error();
      }
      return Response.error();
    }
  })());
});
