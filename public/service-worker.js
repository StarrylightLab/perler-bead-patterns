// 缓存名称和版本
const CACHE_NAME = 'pixel-art-tool-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/vite.svg',
  '/manifest.json'
];

// 安装事件 - 缓存基本资源
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('打开缓存并添加资源');
        return cache.addAll(ASSETS_TO_CACHE);
      })
  );
  self.skipWaiting();
});

// 激活事件 - 删除旧缓存
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME) {
            console.log('删除旧缓存:', name);
            return caches.delete(name);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// 获取事件 - 实现缓存优先策略
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // 如果缓存中有匹配的响应，返回缓存的响应
        if (response) {
          return response;
        }

        // 否则，发起网络请求
        return fetch(event.request)
          .then((networkResponse) => {
            // 如果响应有效，将其克隆并添加到缓存中
            if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
              return networkResponse;
            }

            const responseToCache = networkResponse.clone();

            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });

            return networkResponse;
          })
          .catch(() => {
            // 网络请求失败时的回退方案
            return new Response('网络不可用，请检查您的网络连接', {
              status: 503,
              headers: { 'Content-Type': 'text/plain' }
            });
          });
      })
  );
});

// 推送事件处理
self.addEventListener('push', (event) => {
  const data = event.data?.json() || {};
  const title = data.title || '像素画工具';
  const options = {
    body: data.body || '有新的更新可用',
    icon: '/vite.svg',
    badge: '/vite.svg'
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

// 通知点击事件处理
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    self.clients.matchAll({ type: 'window' }).then((clientList) => {
      if (clientList.length > 0) {
        return clientList[0].focus();
      }
      return self.clients.openWindow('/');
    })
  );
});