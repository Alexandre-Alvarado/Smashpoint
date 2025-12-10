self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('smashpoint-v1').then(cache => {
      return cache.addAll([
        '/public/scoreboard/',
        '/offline/'
      ]);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(resp => {
      return resp || fetch(event.request).catch(() => caches.match('/offline/'));
    })
  );
});