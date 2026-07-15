/* Impulso — service worker (abertura instantânea: stale-while-revalidate) */
const CACHE = 'impulso-v3';
const ASSETS = [
  '/',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/apple-touch-icon.png',
  './icons/favicon-32.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS).catch(() => {})).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const isFont = url.host.includes('fonts.googleapis.com') || url.host.includes('fonts.gstatic.com');

  // Navegação (abrir o app): serve o shell do cache NA HORA e revalida em segundo plano.
  if (req.mode === 'navigate') {
    e.respondWith((async () => {
      const cache = await caches.open(CACHE);
      const cached = await cache.match('/', { ignoreSearch: true });
      const network = fetch(req).then((res) => {
        if (res && res.status === 200) cache.put('/', res.clone());
        return res;
      }).catch(() => cached);
      return cached || network;   // cache primeiro; rede só se não houver cache
    })());
    return;
  }

  // Assets same-origin e fontes: cache-first com atualização em segundo plano.
  if (url.origin === self.location.origin || isFont) {
    e.respondWith((async () => {
      const cache = await caches.open(CACHE);
      const cached = await cache.match(req);
      const network = fetch(req).then((res) => {
        if (res && res.status === 200) cache.put(req, res.clone());
        return res;
      }).catch(() => cached);
      return cached || network;
    })());
  }
});
