# 瀏覽器 APIs：Fetch API、WebSocket、Service Worker

## 前言

現代瀏覽器提供了強大的 APIs，讓網頁應用能夠做到以前只有原生應用才能做到的事情。本篇介紹三個最重要的瀏覽器 APIs。

## Fetch API 網路請求

### 基本用法

```javascript
// GET 請求
fetch('/api/users')
  .then(response => response.json())
  .then(users => console.log(users))
  .catch(error => console.error('Error:', error));

// 等待 response（async/await）
async function loadUsers() {
  try {
    const response = await fetch('/api/users');
    const users = await response.json();
    console.log(users);
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### 請求配置

```javascript
// POST 請求
fetch('/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token123'
  },
  body: JSON.stringify({
    name: 'John',
    email: 'john@example.com'
  })
})
  .then(response => response.json())
  .then(data => console.log('Success:', data))
  .catch(error => console.error('Error:', error));
```

### Response 物件

```javascript
fetch('/api/data')
  .then(response => {
    // 檢查狀態
    console.log('Status:', response.status);
    console.log('OK:', response.ok);

    // 讀取不同格式
    response.json();    // JSON
    response.text();    // 文字
    response.blob();    // 二進位
    response.arrayBuffer(); // 陣列緩衝區

    // 讀取 headers
    console.log(response.headers.get('Content-Type'));
    console.log(response.headers.get('Date'));
  });
```

### 錯誤處理

```javascript
async function fetchWithErrorHandling(url) {
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;

  } catch (error) {
    if (error.name === 'TypeError') {
      console.error('網路錯誤或 CORS 問題');
    } else {
      console.error('伺服器錯誤:', error.message);
    }
    throw error;
  }
}
```

## WebSocket 即時通訊

### 基本概念

```
HTTP vs WebSocket：
───────────────────
HTTP:  請求-回應模式，客戶端發起
       每次請求都需要建立連線
       額外標頭開銷大

WebSocket:
       雙向通訊，伺服器可主動推送
       建立一次連線持續使用
       低延遲，即時性強
```

### 建立連線

```javascript
// 建立 WebSocket 連線
const ws = new WebSocket('wss://example.com/ws');

// 連線打開
ws.onopen = () => {
  console.log('WebSocket 連線已打開');
  ws.send('Hello, Server!');
};

// 收到訊息
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('收到訊息:', data);
};

// 發生錯誤
ws.onerror = (error) => {
  console.error('WebSocket 錯誤:', error);
};

// 連線關閉
ws.onclose = (event) => {
  console.log('WebSocket 連線已關閉', event.code, event.reason);
};
```

### 客戶端/伺服器範例

```javascript
// 客戶端
class ChatClient {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.setupHandlers();
  }

  setupHandlers() {
    this.ws.onopen = () => {
      console.log('已連接到聊天伺服器');
      this.send({ type: 'join', room: 'general' });
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };

    this.ws.onclose = () => {
      console.log('連線中斷，3 秒後重新連線...');
      setTimeout(() => this.reconnect(), 3000);
    };
  }

  send(data) {
    this.ws.send(JSON.stringify(data));
  }

  handleMessage(message) {
    console.log(`${message.user}: ${message.text}`);
  }

  reconnect() {
    this.ws = new WebSocket(this.ws.url);
    this.setupHandlers();
  }

  sendMessage(text) {
    this.send({ type: 'message', text, timestamp: Date.now() });
  }

  close() {
    this.ws.close();
  }
}

// 使用
const client = new ChatClient('wss://chat.example.com');
client.sendMessage('大家好！');
```

## Service Worker 離線應用

### 生命週期

```
Service Worker 生命週期：
─────────────────────────

1. Register（註冊）
   navigator.serviceWorker.register('/sw.js')

2. Install（安裝）
   - 快取靜態資源
   - 失敗則放棄

3. Activate（啟動）
   - 清理舊快取
   - 成為有效的 SW

4. Fetch（攔截請求）
   - 攔截網路請求
   - 快取優先/網路優先策略

5. Sync（後台同步）
   - 網路恢復後同步資料

6. Push（推播通知）
   - 接收伺服器推播
```

### 基本設定

```javascript
// sw.js - Service Worker 檔案

const CACHE_NAME = 'my-site-cache-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/styles.css',
  '/app.js',
  '/images/logo.png'
];

// Install 事件：快取資源
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('快取資源');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate 事件：清理舊快取
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('刪除舊快取:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch 事件：攔截請求
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(event.request)
          .then((response) => {
            // 不快取非成功回應
            if (!response || response.status !== 200) {
              return response;
            }
            // 快取新資源
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });
            return response;
          });
      })
  );
});
```

### 註冊 Service Worker

```html
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('ServiceWorker 註冊成功:', registration.scope);
      })
      .catch((error) => {
        console.log('ServiceWorker 註冊失敗:', error);
      });
  });
}
</script>
```

### 離線優先策略

```javascript
// 更智能的快取策略
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          // 快取命中，回傳快取
          return cachedResponse;
        }

        // 快取未命中，請求網路
        return fetch(event.request)
          .then((response) => {
            // 非成功狀態不快取
            if (!response || response.status !== 200) {
              return response;
            }

            // 動態快取
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });

            return response;
          })
          .catch(() => {
            // 網路失敗且無快取，回傳離線頁面
            return caches.match('/offline.html');
          });
      })
  );
});
```

## IndexedDB 客戶端資料庫

### 基本操作

```javascript
// 開啟資料庫
const request = indexedDB.open('MyDatabase', 1);

request.onerror = (event) => {
  console.error('資料庫錯誤:', event.target.error);
};

request.onupgradeneeded = (event) => {
  const db = event.target.result;

  // 建立物件儲存區
  if (!db.objectStoreNames.contains('users')) {
    const store = db.createObjectStore('users', { keyPath: 'id' });
    store.createIndex('name', 'name', { unique: false });
    store.createIndex('email', 'email', { unique: true });
  }
};

request.onsuccess = (event) => {
  const db = event.target.result;
  console.log('資料庫已開啟');
};

// CRUD 操作
function addUser(db, user) {
  const transaction = db.transaction(['users'], 'readwrite');
  const store = transaction.objectStore('users');
  return store.add(user);
}

function getUser(db, id) {
  const transaction = db.transaction(['users'], 'readonly');
  const store = transaction.objectStore('users');
  return store.get(id);
}

function updateUser(db, user) {
  const transaction = db.transaction(['users'], 'readwrite');
  const store = transaction.objectStore('users');
  return store.put(user);
}

function deleteUser(db, id) {
  const transaction = db.transaction(['users'], 'readwrite');
  const store = transaction.objectStore('users');
  return store.delete(id);
}
```

## 結語

現代瀏覽器 APIs 讓 Web 應用擁有了接近原生應用的能力。Fetch API 簡化了網路請求、WebSocket 實現了即時通訊、Service Worker 讓離線應用成為可能、IndexedDB 提供了客戶端儲存能力。

---

## 延伸閱讀

- [Fetch API 教程](https://www.google.com/search?q=Fetch+API+JavaScript+tutorial)
- [WebSocket 即時通訊](https://www.google.com/search?q=WebSocket+tutorial+real-time)
- [Service Worker 完全指南](https://www.google.com/search?q=Service+Worker+tutorial+PWA)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」歷史回顧系列之一。*