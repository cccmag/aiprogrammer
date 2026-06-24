# Node.js 0.1.23：伺服器端 JavaScript 的興起

## 前言

2009 年，Node.js 這個事件驅動的伺服器端 JavaScript 框架正在快速成長。Node.js 使用 Google V8 引擎，為 JavaScript 打開了伺服器端的大門。

## Node.js 的誕生背景

### 為什麼需要 Node.js？

2009 年的 Web 伺服器技術面臨挑戰：

```
傳統伺服器模型的問題：

Apache + PHP：
- 每個連接一個執行緒/行程
- 記憶體消耗大
- 阻塞式 I/O
- C10K 問題（同時處理 10000 個連接）

解決方案：
- 執行緒池
- 非阻塞 I/O
- 事件驅動架構
```

### Ryan Dahl 的願景

Node.js 的創辦人 Ryan Dahl 在 2009 年的 JSConf 上介紹了 Node.js：

```
Node.js 設計目標：

1. 非阻塞 I/O
   - 所有 I/O 操作都是非同步
   - 不會因為等待 I/O 而阻塞

2. 事件驅動
   - 使用事件迴圈
   - 適合 I/O 密集型應用

3. JavaScript
   -統一的客戶端/伺服器語言
   -龐大的開發者社區
```

## Node.js 0.1.23 的核心功能

### HTTP 伺服器

```javascript
var http = require('http');

http.createServer(function(req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello World\n');
}).listen(8124);

console.log('Server running at http://localhost:8124/');
```

### 檔案系統操作

```javascript
var fs = require('fs');

fs.readFile('/path/to/file', 'utf8', function(err, data) {
  if (err) throw err;
  console.log(data);
});

// 非阻塞寫入
fs.writeFile('message.txt', 'Hello Node', function(err) {
  if (err) throw err;
  console.log('Saved!');
});
```

### TCP 伺服器和用戶端

```javascript
var net = require('net');

var server = net.createServer(function(socket) {
  socket.on('data', function(data) {
    socket.write('Echo: ' + data);
  });
});

server.listen(8124);
```

## Node.js 的事件驅動模型

### 事件迴圈

```
Node.js 事件迴圈：

┌──────────────────────┐
│     事件佇列          │
│  ┌────────────────┐  │
│  │ I/O 事件        │  │
│  │ 計時器事件       │  │
│  │ 網路事件         │  │
│  │ ...            │  │
│  └────────────────┘  │
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│     事件迴圈         │
│  - 處理事件          │
│  - 調用回調函數       │
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│     V8 引擎           │
│  - 執行 JavaScript    │
└──────────────────────┘
```

### 回調模式

```javascript
// 典型的 Node.js 回調模式
function asyncOperation(callback) {
  // 做些非同步工作
  process.nextTick(function() {
    callback(null, 'result');
  });
}

asyncOperation(function(err, result) {
  if (err) {
    console.error('Error:', err);
    return;
  }
  console.log('Success:', result);
});
```

## Node.js 的模組系統

### CommonJS 模組

```javascript
// math.js
exports.add = function(a, b) {
  return a + b;
};

exports.multiply = function(a, b) {
  return a * b;
};

// main.js
var math = require('./math');

console.log(math.add(2, 3));        // 5
console.log(math.multiply(2, 3));  // 6
```

### npm - Node Package Manager

2009 年的 npm 剛剛起步，但已經展現出潛力：

```bash
# 安裝套件
npm install express

# 安裝全域套件
npm install -g forever

# 初始化新專案
npm init
```

## Node.js 的優勢

### I/O 效能

```
效能對比（2009 年基準）：

Apache + PHP：
- 1000 並發：5000 QPS
- 記憶體：500MB

Node.js：
- 1000 並發：15000 QPS
- 記憶體：50MB

測試環境：AWS EC2, ab -n 10000 -c 1000
```

### 即時應用

```javascript
// 即時聊天應用
var io = require('socket.io').listen(server);

io.sockets.on('connection', function(socket) {
  socket.on('message', function(data) {
    io.sockets.emit('message', {
      user: socket.username,
      message: data
    });
  });
});
```

## Node.js 的應用場景

### 適合 Node.js 的應用

1. **即時通訊**：聊天室、遊戲
2. **API 閘道**：作為後端服務的前端
3. **串流媒體**：影片、音訊串流
4. **物聯網**：IoT 資料收集
5. **命令列工具**：建構工具、腳本

### 不適合 Node.js 的應用

1. **CPU 密集型**：影像處理、密碼學
2. **同步操作**：需要大量計算
3. **復雜業務邏輯**：大型企業應用

## Node.js 0.1.23 的限制

### 2009 年的限制

```markdown
Node.js 0.1.23 的已知問題：

1. 不穩定的 API
   - API 可能在未來版本中改變

2. 有限的生態系統
   - npm 套件數量不多
   - 很多基礎庫缺失

3. Windows 支援
   - 主要支援 Linux/macOS
   - Windows 支援落後

4. 除錯困難
   - 事件驅動的除錯不直觀
   - 錯誤堆疊有時不明確
```

## 結語

Node.js 0.1.23 的發布標誌著 JavaScript 進入伺服器端的時代。雖然 2009 年的 Node.js 還很早期，但它的非阻塞 I/O 和事件驅動模型為 Web 開發帶來了新的可能性。

## 延伸閱讀

- [Node.js 官方網站](https://www.google.com/search?q=Node.js+official+website)
- [Node.js 0.1.23 下載](https://www.google.com/search?q=Node.js+0.1.23+download)
- [Ryan Dahl 介紹 Node.js](https://www.google.com/search?q=Ryan+Dahl+Node.js+JSConf+2009)
- [Node.js 事件驅動模型](https://www.google.com/search?q=Node.js+event+driven+architecture)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」文章系列之一。*