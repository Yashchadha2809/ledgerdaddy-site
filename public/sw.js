self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('ld-v1').then((cache) =>
      cache.addAll([
        '/',              // homepage
        '/chat.html',     // add key pages you want offline
        '/styles.css',    // your css (if any)
        '/app.js',        // your js (if any)
        '/icons/icon-192.png',
        '/icons/icon-512.png'
      ])
    )
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(caches.match(e.request).then((res) => res || fetch(e.request)));
});
