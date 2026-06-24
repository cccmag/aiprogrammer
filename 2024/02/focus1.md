# Node.js 執行期與事件循環

## Node.js 的誕生

2009 年，Ryan Dahl 在 JSConf 上首次展示了 Node.js，這個基於 Google V8 引擎的伺服器端 JavaScript 執行期立即引起了廣泛關注。Dahl 的目標是建立一個能夠處理大量併發連接的輕量級伺服器，而傳統的 Apache HTTP 伺服器每收到一個連接就建立一個執行緒，在高併發時消耗大量記憶體。

Node.js 的核心創新在於：它使用非阻塞 I/O 加上事件驅動的模型，讓單一執行緒就能處理成千上萬的併發連接。

## V8 引擎與架構

Node.js 由以下核心元件組成：

```
┌──────────────────────────────┐
│         JavaScript            │
├──────────────────────────────┤
│ Node.js Bindings (Node API)   │
├──────────────────────────────┤
│           V8 Engine           │
├──────────────────────────────┤
│  libuv (Event Loop + I/O)    │
└──────────────────────────────┘
```

- **V8 引擎**：Google 開發的高效 JavaScript 引擎，負責將 JS 編譯為機器碼
- **libuv**：跨平台的非同步 I/O 函式庫，提供 Event Loop 和執行緒池
- **Node.js Bindings**：將 V8 與 libuv 橋接起來的 C++ 層

## 事件循環（Event Loop）

Event Loop 是 Node.js 最核心的機制。它本質上是一個無限循環，不斷檢查是否有任務需要處理：

```
   ┌──────────────────────────┐
┌─>│          timers          │
│  └─────────────┬────────────┘
│  ┌─────────────┴────────────┐
│  │     pending callbacks    │
│  └─────────────┬────────────┘
│  ┌─────────────┴────────────┐
│  │       idle, prepare      │
│  └─────────────┬────────────┘
│  ┌─────────────┴────────────┐
│  │           poll           │
│  └─────────────┬────────────┘
│  ┌─────────────┴────────────┐
│  │           check          │
│  └─────────────┬────────────┘
│  ┌─────────────┴────────────┐
│  │      close callbacks     │
│  └──────────────────────────┘
└──────────────────────────────┘
```

Event Loop 的各個階段：

1. **timers**：執行 `setTimeout()` 和 `setInterval()` 的回呼
2. **pending callbacks**：執行延遲到下一輪的 I/O 回呼
3. **idle, prepare**：內部使用
4. **poll**：取得新的 I/O 事件，執行 I/O 相關回呼
5. **check**：執行 `setImmediate()` 回呼
6. **close callbacks**：執行關閉事件的回呼（如 socket.on('close')）

## 非阻塞 I/O 模型

傳統的阻塞 I/O 模型在讀取檔案或網路請求時會卡住執行緒：

```javascript
const fs = require('fs');

// 阻塞方式
const data = fs.readFileSync('/bigfile.txt', 'utf8');
console.log(data); // 等檔案讀完才會執行
console.log('這行要等上面執行完');
```

Node.js 的非阻塞版本：

```javascript
const fs = require('fs');

// 非阻塞方式
fs.readFile('/bigfile.txt', 'utf8', (err, data) => {
  console.log(data);
});
console.log('這行先執行，檔案還在背景讀取');
```

### 執行緒池

Node.js 的 Event Loop 是單執行緒的，但 libuv 內部維護了一個執行緒池（預設 4 個執行緒），用於處理那些無法在系統層級實現非阻塞的操作（如檔案 I/O、DNS 查詢）。

## process.nextTick 與 Promise

`process.nextTick()` 和 Promise 的回呼雖然不在 Event Loop 的六個階段中，但它們擁有更高的優先級：

```javascript
setTimeout(() => console.log('timeout'), 0);
setImmediate(() => console.log('immediate'));
process.nextTick(() => console.log('nextTick'));
Promise.resolve().then(() => console.log('promise'));
```

輸出順序為：`nextTick` → `promise` → `timeout` (或 `immediate`，取決於階段)

## 總結

理解 Event Loop 是掌握 Node.js 的關鍵。它不僅決定了程式的執行順序，也影響著效能和可預測性。非同步 I/O 讓 Node.js 在處理大量併發請求時表現出色，但開發者需要特別注意不要在同步操作上花費太多時間，否則會阻塞 Event Loop。

## 延伸閱讀

- [Node.js Event Loop 官方文件](https://www.google.com/search?q=Node.js+event+loop+documentation)
- [libuv 設計文件](https://www.google.com/search?q=libuv+design+document)
- [Philip Roberts: What the heck is the event loop?](https://www.google.com/search?q=Philip+Roberts+event+loop+talk)
