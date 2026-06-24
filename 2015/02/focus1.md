# Node.js 基礎與核心模組：事件驅動、檔案系統、HTTP

## 前言

Node.js 是基於 Chrome V8 引擎的 JavaScript 執行環境，專為建立快速、可擴展的網路應用程式而設計。

## 事件驅動架構

### EventEmitter

```javascript
const EventEmitter = require('events').EventEmitter;

// 建立事件發射器
class MyEmitter extends EventEmitter {}

const emitter = new MyEmitter();

// 監聽事件
emitter.on('event', function(arg1, arg2) {
  console.log('事件觸發:', arg1, arg2);
});

// 發射事件
emitter.emit('event', '參數1', '參數2');

// 只監聽一次
emitter.once('single-event', function() {
  console.log('只會觸發一次');
});
```

### HTTP 伺服器範例

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  console.log(`${req.method} ${req.url}`);

  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World\n');
});

server.listen(3000, () => {
  console.log('伺服器執行於 http://localhost:3000');
});

// 事件監聽
server.on('request', (req, res) => {
  console.log('收到請求');
});

server.on('close', () => {
  console.log('伺服器關閉');
});
```

## 檔案系統操作

### 同步 vs 非同步

```javascript
const fs = require('fs');

// 非同步（回調）
fs.readFile('file.txt', 'utf8', (err, data) => {
  if (err) throw err;
  console.log(data);
});

// 同步（阻塞）
const data = fs.readFileSync('file.txt', 'utf8');
console.log(data);

// Promise 風格（Node.js 10+）
const fsPromises = require('fs').promises;
async function read() {
  const data = await fsPromises.readFile('file.txt', 'utf8');
  console.log(data);
}
```

### 常見檔案操作

```javascript
const fs = require('fs');
const path = require('path');

// 讀取目錄
fs.readdir('./src', (err, files) => {
  files.forEach(file => {
    console.log(file);
  });
});

// 建立目錄
fs.mkdir('./new-dir', { recursive: true }, (err) => {
  if (err) throw err;
});

// 寫入檔案
fs.writeFile('message.txt', 'Hello', (err) => {
  if (err) throw err;
});

// 附加到檔案
fs.appendFile('message.txt', ' World', (err) => {
  if (err) throw err;
});

// 刪除檔案
fs.unlink('temp.txt', (err) => {
  if (err) throw err;
});

// 檢查存在
fs.access('file.txt', fs.constants.F_OK, (err) => {
  console.log(err ? '不存在' : '存在');
});
```

### 路徑處理

```javascript
const path = require('path');

// 路徑組合
path.join('/foo', 'bar', 'baz');  // '/foo/bar/baz'

// 解析為絕對路徑
path.resolve('index.html');  // '/current/dir/index.html'

// 取得副檔名
path.extname('file.txt');  // '.txt'

// 取得檔案名
path.basename('/foo/bar/file.txt');  // 'file.txt'
path.basename('/foo/bar/file.txt', '.txt');  // 'file'

// 目錄名
path.dirname('/foo/bar/file.txt');  // '/foo/bar'
```

## HTTP 模組

### 發送 HTTP 請求

```javascript
const http = require('http');

// GET 請求
const options = {
  hostname: 'api.example.com',
  port: 80,
  path: '/users',
  method: 'GET'
};

const req = http.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  res.on('end', () => {
    console.log(JSON.parse(data));
  });
});

req.on('error', (e) => {
  console.error(e);
});

req.end();

// 簡化版 GET
http.get('http://api.example.com/users', (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => console.log(JSON.parse(data)));
});
```

### 建立 HTTP API

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  // CORS 標頭
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // 路由
  const url = req.url.split('?')[0];
  const method = req.method;

  if (url === '/api/users' && method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ users: [] }));
  } else if (url === '/api/users' && method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      const user = JSON.parse(body);
      res.writeHead(201, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ created: true, user }));
    });
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not Found' }));
  }
});

server.listen(3000);
```

## 實用範例：靜態檔案伺服器

```javascript
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const STATIC_DIR = './public';

const mimeTypes = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml'
};

const server = http.createServer((req, res) => {
  let filePath = path.join(STATIC_DIR, req.url === '/' ? 'index.html' : req.url);

  const ext = path.extname(filePath);
  const contentType = mimeTypes[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404);
        res.end('File Not Found');
      } else {
        res.writeHead(500);
        res.end('Server Error');
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    }
  });
});

server.listen(PORT, () => {
  console.log(`靜態伺服器執行於 http://localhost:${PORT}`);
});
```

## 結論

Node.js 的核心模組提供了建立網路應用所需的全部工具。事件驅動的架構讓處理大量併發連線成為可能，非阻塞 I/O 確保了高效能。

---

## 延伸閱讀

- [Node.js 官方文檔](https://www.google.com/search?q=Node.js+documentation+events+fs+http)
- [Node.js 核心模組詳解](https://www.google.com/search?q=Node.js+core+modules+tutorial)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」歷史回顧系列之一。*