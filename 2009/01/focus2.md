# 事件驅動架構：Event Loop 機制與非阻塞 I/O

## 前言

Node.js 的核心是其事件驅動架構。理解 Event Loop 的運作原理，是掌握 Node.js 的關鍵。本章將深入探討事件驅動的設計理念與實作機制。

## 什麼是事件驅動架構？

事件驅動架構是一種程式設計範式，其中程式的流程由事件（如使用者動作、訊息、或是 I/O 完成）來決定。

```
傳統的請求-回應模型：
───────────────────
Client  ──請求──▶  Server
         ◀──回應──  （等待處理完成）

事件驅動模型：
─────────────
Client  ──請求──▶  Server ──▶ 處理中...
                      ↓
                  I/O 作業
                      ↓
         事件觸發 ◀┘
                      ↓
Client  ◀──回應──  Server
```

## Event Loop 機制

### 單執行緒事件迴圈

Node.js 使用單一執行緒來處理所有請求，但透過事件迴圈來實現高併發：

```javascript
// 這個程式可以同時處理成千上萬個連線
const server = http.createServer((req, res) => {
  // 每個請求都會觸發這個回呼
  res.writeHead(200);
  res.end('Hello World');
});

server.listen(3000);
console.log('伺服器運行中...');

// 單一執行緒同時處理：
// - HTTP 請求
// - 檔案讀寫
// - 資料庫查詢
// - 網路通訊
```

### Event Loop 的工作流程

```
┌─────────────────────────────────────────────────────────┐
│                      Event Loop                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐    ┌─────────────┐    ┌───────────┐  │
│   │   Timers    │    │ Pending     │    │   Poll    │  │
│   │  setTimeout │    │ Callbacks   │    │  I/O Events│  │
│   │  setInterval│    │             │    │           │  │
│   └──────┬──────┘    └──────┬──────┘    └─────┬─────┘  │
│          │                  │                  │        │
│          └──────────────────┴──────────────────┘        │
│                           │                              │
│                    ┌──────▼──────┐                       │
│                    │  Check      │                       │
│                    │ setImmediate│                       │
│                    └──────┬──────┘                       │
│                           │                              │
│                    ┌──────▼──────┐                       │
│                    │ Close       │                       │
│                    │ Callbacks   │                       │
│                    └─────────────┘                       │
└─────────────────────────────────────────────────────────┘

執行順序：
1. Timers（計時器）：執行 setTimeout、setInterval 的回呼
2. Pending Callbacks（待處理回呼）：上一輪延遲的 I/O 回呼
3. Poll（輪詢）：獲取新的 I/O 事件
4. Check（檢查）：執行 setImmediate 的回呼
5. Close Callbacks（關閉回呼）：關閉連線的回呼
```

### 計時器階段

```javascript
console.log('1');

setTimeout(() => {
  console.log('3 - setTimeout');
}, 0);

setImmediate(() => {
  console.log('2 - setImmediate');
});

console.log('同步任務');

// 輸出：
// 1
// 同步任務
// 2 - setImmediate 或 3 - setTimeout（視情況）
// 3 - setTimeout 或 2 - setImmediate
```

## 非阻塞 I/O 原理

### 阻塞 vs 非阻塞

```javascript
// 阻塞式 I/O（傳統模式）
const data = fs.readFileSync('/path/to/file'); // 等待完成
console.log(data); // 這裡才继续执行

// 非阻塞式 I/O（Node.js 模式）
fs.readFile('/path/to/file', (err, data) => {
  console.log(data); // I/O 完成後執行
});
console.log('這行會立即執行'); // 不等待 I/O
```

### libuv 的角色

Node.js 底層使用 libuv 函式庫來處理非阻塞 I/O：

```
┌─────────────────────────────────────────┐
│            Node.js 應用程式              │
├─────────────────────────────────────────┤
│                                         │
│   JavaScript 代碼                       │
│   ┌─────────────────────────────────┐   │
│   │ setTimeout, fs.readFile,       │   │
│   │ http.createServer, etc.        │   │
│   └─────────────────────────────────┘   │
│                  │                      │
│                  ▼                      │
│   ┌─────────────────────────────────┐   │
│   │      Node.js C++ Bindings       │   │
│   └─────────────────────────────────┘   │
│                  │                      │
└──────────────────┼──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│              libuv                         │
├────────────────────────────────────────────┤
│                                            │
│   ┌──────────────┐    ┌──────────────────┐ │
│   │  執行緒池    │    │   事件迴圈       │ │
│   │  Thread Pool │    │   Event Loop    │ │
│   └──────────────┘    └──────────────────┘ │
│         │                      │            │
│         │ 阻塞 I/O             │ 非阻塞 I/O │
│         ▼                      ▼            │
│   ┌─────────┐          ┌───────────────┐   │
│   │ 檔案系統 │          │  網路/計時器   │   │
│   │  DNS    │          │               │   │
│   └─────────┘          └───────────────┘   │
└────────────────────────────────────────────┘
```

### 非阻塞優點

```javascript
// 模擬：假設有 3 個檔案需要處理

// 阻塞式：總時間 = 1秒 + 1秒 + 1秒 = 3秒
const a = fs.readFileSync('a.txt');
const b = fs.readFileSync('b.txt');
const c = fs.readFileSync('c.txt');

// 非阻塞式：總時間 ≈ 1秒（平行處理）
fs.readFile('a.txt', (err, a) => {});
fs.readFile('b.txt', (err, b) => {});
fs.readFile('c.txt', (err, c) => {});
```

## 常見的事件處理模式

### 回呼函式

```javascript
// 基本回呼模式
fs.readFile('data.json', (err, data) => {
  if (err) {
    console.error('讀取錯誤:', err);
    return;
  }
  console.log('成功:', data);
});

// 多層回呼（回呼地獄）
fs.readFile('a.txt', (err, a) => {
  fs.readFile('b.txt', (err, b) => {
    fs.readFile('c.txt', (err, c) => {
      console.log(a, b, c);
    });
  });
});
```

### 事件發射器

```javascript
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}

const emitter = new MyEmitter();

emitter.on('event', (data) => {
  console.log('事件觸發:', data);
});

emitter.emit('event', { message: 'Hello' });
```

### Promise 模式（2009 年還未廣泛使用）

```javascript
// 2009 年，Promise 還不是標準
// 這是未來的写法
const readFile = (path) => {
  return new Promise((resolve, reject) => {
    fs.readFile(path, (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
};

readFile('data.json')
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

## Event Loop 的實際應用

### 伺服器請求處理

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  // 這個回呼在事件迴圈中執行
  if (req.url === '/api/data') {
    // 模擬資料庫查詢（非阻塞）
    setTimeout(() => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ message: 'Hello World' }));
    }, 100);
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});

server.listen(3000, () => {
  console.log('伺服器在 3000 連接埠運行');
});
```

### 併發處理示意

```
同時 10,000 個請求到達：
────────────────────────

傳統方式：
  需要 10,000 個執行緒
  記憶體：10,000 × 8MB = 80GB

Node.js 方式：
  單一執行緒，事件迴圈
  每個請求作為一個事件處理
  記憶體：約 100MB
```

## 結語

事件驅動架構是 Node.js 的核心。透過單執行緒事件迴圈和非阻塞 I/O，Node.js 能夠用極少的資源處理大量併發連線。

理解 Event Loop 的運作機制，是成為 Node.js 專家的必經之路。

---

## 延伸閱讀

- [Node.js Event Loop 文檔](https://www.google.com/search?q=Node.js+Event+Loop+documentation)
- [libuv 設計文件](https://www.google.com/search?q=libuv+design+document)
- [非阻塞 I/O 詳解](https://www.google.com/search?q=non-blocking+I/O+nodejs)

---

*本篇文章為「AI 程式人雜誌 2009 年 1 月號」歷史回顧系列之一。*