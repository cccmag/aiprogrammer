# 內建模組：fs、path、http

## 前言

Node.js 提供了一組豐富的內建模組（Built-in Modules），讓開發者無需安裝任何第三方套件即可完成常見的後端開發任務。其中最常用的三個模組是 `fs`（檔案系統）、`path`（路徑處理）和 `http`（HTTP 伺服器）。

## fs — 檔案系統模組

`fs` 模組提供了與檔案系統互動的 API，所有操作都有同步和非同步兩種版本。

### 讀取檔案

```javascript
const fs = require('fs');

// 非同步讀取
fs.readFile('./data.txt', 'utf8', (err, data) => {
  if (err) throw err;
  console.log(data);
});

// 同步讀取
const data = fs.readFileSync('./data.txt', 'utf8');
console.log(data);

// Promise 版本
const fsp = require('fs/promises');
async function read() {
  const data = await fsp.readFile('./data.txt', 'utf8');
  console.log(data);
}
```

### 寫入與附加

```javascript
// 寫入檔案（覆蓋）
fs.writeFileSync('./output.txt', 'Hello World');

// 附加到檔案
fs.appendFileSync('./log.txt', new Date().toISOString() + '\n');
```

### 目錄操作

```javascript
const fs = require('fs');

// 建立目錄
fs.mkdirSync('./uploads', { recursive: true });

// 讀取目錄內容
const files = fs.readdirSync('./uploads');
console.log(files);

// 檢查檔案是否存在
if (fs.existsSync('./data.txt')) {
  console.log('檔案存在');
}
```

## path — 路徑處理模組

`path` 模組提供跨平台的路徑處理功能，避免手動拼接路徑字串時出現錯誤。

```javascript
const path = require('path');

// 路徑拼接（自動處理分隔符）
const fullPath = path.join('user', 'docs', 'file.txt');
// Linux: 'user/docs/file.txt'
// Windows: 'user\\docs\\file.txt'

// 取得檔案資訊
const info = path.parse('/user/docs/file.txt');
console.log(info);
// {
//   root: '/',
//   dir: '/user/docs',
//   base: 'file.txt',
//   ext: '.txt',
//   name: 'file'
// }

// 常用方法
path.basename('/foo/bar/baz.txt');  // 'baz.txt'
path.dirname('/foo/bar/baz.txt');   // '/foo/bar'
path.extname('/foo/bar/baz.txt');   // '.txt'
path.resolve('docs', '..', 'file.txt'); // 解析為絕對路徑
```

### 跨平台注意事項

```javascript
// 不要這樣做（Windows 上會失敗）
const badPath = __dirname + '/data/' + 'file.txt';

// 請使用 path.join
const goodPath = path.join(__dirname, 'data', 'file.txt');

// 取得當前目錄路徑
console.log(__dirname);  // 當前檔案所在目錄
console.log(__filename); // 當前檔案完整路徑
```

## http — HTTP 伺服器模組

`http` 模組讓開發者可以用純 Node.js 建立 HTTP 伺服器和客戶端。

### 建立 HTTP 伺服器

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  // 設定回應標頭
  res.writeHead(200, {
    'Content-Type': 'application/json',
  });

  // 根據路由回應
  if (req.url === '/api/hello') {
    res.end(JSON.stringify({ message: 'Hello World' }));
  } else if (req.url === '/api/time') {
    res.end(JSON.stringify({ time: new Date().toISOString() }));
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not Found' }));
  }
});

server.listen(3000, () => {
  console.log('Server running at http://localhost:3000/');
});
```

### 處理請求主體

```javascript
const server = http.createServer((req, res) => {
  if (req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      const data = JSON.parse(body);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ received: data }));
    });
  }
});
```

### 綜合範例：簡單的靜態檔案伺服器

```javascript
const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
  const filePath = path.join(__dirname, 'public', req.url === '/' ? 'index.html' : req.url);
  
  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(404);
      res.end('File not found');
    } else {
      res.writeHead(200);
      res.end(content);
    }
  });
});

server.listen(3000);
```

## 總結

`fs`、`path`、`http` 這三個內建模組構成 Node.js 後端開發的基礎。熟練它們之後，即使不使用任何第三方框架，也能建立功能完整的伺服器應用。

## 延伸閱讀

- [Node.js fs 官方文件](https://www.google.com/search?q=Node.js+fs+module)
- [Node.js path 官方文件](https://www.google.com/search?q=Node.js+path+module)
- [Node.js http 官方文件](https://www.google.com/search?q=Node.js+http+module)
