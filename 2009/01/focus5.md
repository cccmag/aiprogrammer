# HTTP 伺服器開發：使用 Node.js 建立 Web 服務

## 前言

Node.js 最初就是為了解決 Web 伺服器開發的問題而創造的。內建的 `http` 模組讓建立 HTTP 伺服器變得簡單而強大。

## 建立基本的 HTTP 伺服器

### 最簡單的範例

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World');
});

server.listen(3000, () => {
  console.log('伺服器運行在 http://localhost:3000');
});
```

### 處理不同的 HTTP 方法

```javascript
const http = require('http');
const server = http.createServer((req, res) => {
  const method = req.method;
  const url = req.url;

  console.log(`${method} ${url}`);

  if (method === 'GET') {
    if (url === '/') {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end('<h1>首頁</h1>');
    } else if (url === '/about') {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end('<h1>關於我們</h1>');
    } else {
      res.writeHead(404, { 'Content-Type': 'text/html' });
      res.end('<h1>404 Not Found</h1>');
    }
  } else if (method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
    });
    req.on('end', () => {
      console.log('POST 資料：', body);
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end('收到 POST 請求');
    });
  }
});

server.listen(3000);
```

## 請求物件

```javascript
const server = http.createServer((req, res) => {
  // URL 物件
  const parsedUrl = require('url').parse(req.url, true);

  console.log('主機名：', req.headers.host);
  console.log('URL 路徑：', parsedUrl.pathname);
  console.log('查詢參數：', parsedUrl.query);

  // HTTP 方法
  console.log('方法：', req.method);

  // 使用者代理
  console.log('使用者代理：', req.headers['user-agent']);

  res.writeHead(200);
  res.end();
});
```

## 回應物件

```javascript
const server = http.createServer((req, res) => {
  // 發送 HTTP 狀態碼
  res.writeHead(200); // 成功
  res.writeHead(404); // 找不到
  res.writeHead(500); // 伺服器錯誤

  // 發送表頭
  res.writeHead(200, {
    'Content-Type': 'text/html',
    'X-Custom-Header': '自訂表頭'
  });

  // 發送 JSON 回應
  const data = { name: '王小明', age: 25 };
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(data));

  // 發送 HTML
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end('<html><body><h1>你好</h1></body></html>');
});
```

## 路由處理

### 簡單的路由實作

```javascript
const http = require('http');
const url = require('url');

const routes = {
  'GET': {
    '/': (req, res) => {
      res.writeHead(200);
      res.end('首頁');
    },
    '/about': (req, res) => {
      res.writeHead(200);
      res.end('關於頁面');
    },
    '/api/users': (req, res) => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify([
        { id: 1, name: '王小明' },
        { id: 2, name: '李小華' }
      ]));
    }
  },
  'POST': {
    '/api/users': (req, res) => {
      let body = '';
      req.on('data', chunk => { body += chunk; });
      req.on('end', () => {
        res.writeHead(201, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ message: '使用者已建立' }));
      });
    }
  }
};

http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  const method = req.method;

  const handler = routes[method] && routes[method][pathname];

  if (handler) {
    handler(req, res);
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
}).listen(3000);
```

## 靜態檔案服務

```javascript
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const mimeTypes = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg'
};

http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url);
  let pathname = '.' + parsedUrl.pathname;

  if (pathname === './') {
    pathname = './index.html';
  }

  const extname = path.extname(pathname);
  const contentType = mimeTypes[extname] || 'application/octet-stream';

  fs.readFile(pathname, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404);
        res.end('File not found');
      } else {
        res.writeHead(500);
        res.end('Server error');
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    }
  });
}).listen(3000);
```

## request 事件

```javascript
const server = http.createServer();

// request 事件：每當有請求到達時觸發
server.on('request', (req, res) => {
  console.log('收到請求：', req.url);
});

// connection 事件：客戶端連線時觸發
server.on('connection', (socket) => {
  console.log('新的 TCP 連線');
});

// close 事件：伺服器關閉時觸發
server.on('close', () => {
  console.log('伺服器已關閉');
});

server.listen(3000);
```

## 發送 HTTP 請求

```javascript
const http = require('http');

// GET 請求
const req = http.request('http://example.com/api/data', (res) => {
  let data = '';
  res.on('data', chunk => { data += chunk; });
  res.on('end', () => {
    console.log('回應：', data);
  });
});
req.end();

// POST 請求
const postData = JSON.stringify({ name: 'test' });
const postReq = http.request({
  hostname: 'example.com',
  port: 80,
  path: '/api/users',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
}, (res) => {
  console.log('狀態碼：', res.statusCode);
});
postReq.write(postData);
postReq.end();
```

## 結語

Node.js 的 `http` 模組提供了建立 HTTP 伺服器和用戶端所需的所有基礎功能。雖然在 2009 年 Express 框架還不存在，但原生 HTTP 模組已經足夠強大，能夠建立完整的 Web 應用。

從基本的 request 回應，到複雜的路由系統和靜態檔案服務，Node.js 提供了建設現代 Web 應用所需的所有工具。

---

## 延伸閱讀

- [Node.js HTTP 模組文檔](https://www.google.com/search?q=Node.js+http+module+documentation)
- [HTTP 協定詳解](https://www.google.com/search?q=HTTP+protocol+tutorial)
- [RESTful API 設計](https://www.google.com/search?q=RESTful+API+design)

---

*本篇文章為「AI 程式人雜誌 2009 年 1 月號」歷史回顧系列之一。*