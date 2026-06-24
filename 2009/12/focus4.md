# JavaScript 全端：Node.js 崛起

## Node.js 的誕生

### 背景

```markdown
# Node.js 的起源

Ryan Dahl 在 2009 年創建 Node.js

核心理念：
- 事件驅動
- 非阻塞 I/O
- JavaScript 全端
- 輕量級伺服器

目標：
- 處理高並發
- 即時 Web 應用
- 簡化的網路程式
```

## 2009 年的 Node.js

### 核心功能

```javascript
// Node.js 0.1.x（2009年）

// HTTP 伺服器
var http = require('http');
http.createServer(function(req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello, World!');
}).listen(8124);

// 檔案系統
var fs = require('fs');
fs.readFile('file.txt', 'utf8', function(err, data) {
  console.log(data);
});

// 事件發射器
var EventEmitter = require('events').EventEmitter;
var emitter = new EventEmitter();
emitter.on('event', function(data) {
  console.log(data);
});
emitter.emit('event', 'test');
```

## npm 的早期發展

### 套件管理

```bash
# 2009 年 npm

# 安裝套件
npm install express

# 全域安裝
npm install -g coffee-script

# 初始化專案
npm init
```

## 應用場景

```javascript
// 2009 年 Node.js 應用

// 即時聊天
var io = require('socket.io');
io.listen(server).sockets.on('connection', function(socket) {
  socket.on('message', function(data) {
    io.sockets.emit('message', data);
  });
});

// REST API
var express = require('express');
var app = express();
app.get('/api/users', function(req, res) {
  res.json(users);
});
```

## 結語

Node.js 的崛起標誌著 JavaScript 全端時代的來臨，這種統一語言的趨勢持續影響至今。

---

*本篇文章為「AI 程式人雜誌 2009 年 12 月號」焦點系列之一。*