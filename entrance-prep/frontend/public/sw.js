// Only an offline landing page is cached. Never cache authenticated API data,
// answer keys, questions, attempts, or teacher reference metadata.
const CACHE = 'rupp-offline-v1';
self.addEventListener('install', event => { event.waitUntil(caches.open(CACHE).then(c => c.add('/offline.html'))); self.skipWaiting(); });
self.addEventListener('activate', event => { event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))); self.clients.claim(); });
self.addEventListener('fetch', event => { if(event.request.mode === 'navigate') event.respondWith(fetch(event.request).catch(() => caches.match('/offline.html'))); });
