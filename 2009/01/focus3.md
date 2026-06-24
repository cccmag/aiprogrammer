# CommonJS 模組系統：require() 與模組化設計

## 前言

在 Node.js 中，模組化是核心概念。CommonJS 規範定義了 JavaScript 如何在不同環境中共享程式碼，這使得 Node.js 的套件生態系得以蓬勃發展。

## 什麼是 CommonJS？

CommonJS 是一個志願者組織，旨在為 JavaScript 之外的環境指定通用的 API 規範。Node.js 採用了 CommonJS 模組規範作為其模組系統的基礎。

```
CommonJS 規範的目標：
─────────────────────
1. 提供一個標準的方式來組織和分享程式碼
2. 讓同一套程式碼能在不同環境中執行
3. 定義模組的導入和導出機制
```

## 基本模組語法

### 導出模組

```javascript
// math.js
// 導出單一函式
module.exports = function add(a, b) {
  return a + b;
};

// 或導出多個函式
module.exports = {
  add: function(a, b) { return a + b; },
  subtract: function(a, b) { return a - b; },
  multiply: function(a, b) { return a * b; }
};

// 或使用 exports 簡寫
exports.add = function(a, b) { return a + b; };
exports.subtract = function(a, b) { return a - b; };
```

### 導入模組

```javascript
// main.js
const math = require('./math');

console.log(math.add(1, 2));      // 3
console.log(math.subtract(5, 3)); // 2
```

## 模組解析機制

### 路徑解析順序

```javascript
// 1. 相對路徑
const utils = require('./utils');        // 同目錄
const helpers = require('../helpers');   // 上層目錄

// 2. 絕對路徑
const config = require('/etc/app/config'); // 很少使用

// 3. 內建模組（核心模組）
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

// 4. node_modules 套件
const express = require('express');
const lodash = require('lodash');
```

### node_modules 查找順序

```
require('express') 的查找順序：
───────────────────────────────
1. ./node_modules/express
2. ../node_modules/express
3. ../../node_modules/express
4. ... 持續向上查詢直到根目錄
```

## 內建模組

Node.js 提供了豐富的內建模組：

```javascript
// HTTP 模組
const http = require('http');
const server = http.createServer((req, res) => {
  res.end('Hello');
});

// 檔案系統模組
const fs = require('fs');
fs.readFile('data.txt', (err, data) => {
  console.log(data);
});

// 路徑模組
const path = require('path');
const fullPath = path.join(__dirname, 'views', 'index.html');

// 作業系統模組
const os = require('os');
console.log('平台：', os.platform());
console.log('CPU 核心數：', os.cpus().length);

// URL 解析
const url = require('url');
const parsed = url.parse('http://example.com/path?query=1');
```

## 建立自己的模組

### 簡單模組

```javascript
// greet.js
function greet(name) {
  return `Hello, ${name}!`;
}

function farewell(name) {
  return `Goodbye, ${name}!`;
}

module.exports = { greet, farewell };
```

```javascript
// 使用
const { greet, farewell } = require('./greet');
console.log(greet('World'));     // Hello, World!
console.log(farewell('World'));   // Goodbye, World!
```

### 工廠模式模組

```javascript
// counter.js
module.exports = function Counter() {
  let count = 0;

  return {
    increment: function() { count++; },
    decrement: function() { count--; },
    getCount: function() { return count; }
  };
};

// 使用
const Counter = require('./counter');
const c = Counter();
c.increment();
c.increment();
console.log(c.getCount()); // 2
```

## 模組作用域

```javascript
// 每個模組都有獨立的作用域
// a.js
const privateVariable = '這是私有的';

function privateFunction() {
  return '私有函式';
}

module.exports = {
  publicFunction: function() {
    return privateFunction(); // 可以訪問私有函式
  }
};
```

```javascript
// b.js
const a = require('./a');
console.log(a.publicFunction()); // 私有函式
// console.log(a.privateVariable); // undefined - 無法訪問
```

## 模組快取

```javascript
// Node.js 會快取每個模組
// 同一個 require 只會執行一次

// 第一次 require
const utils = require('./utils'); // 執行一次
const utils2 = require('./utils'); // 使用快取

// utils === utils2 為 true
```

## 環形依賴

```javascript
// a.js
console.log('a 开始加载');
const b = require('./b');
console.log('a 加载完成，b =', b);

module.exports = { name: 'a' };

// b.js
console.log('b 开始加载');
const a = require('./a');
console.log('b 加载完成，a =', a);

module.exports = { name: 'b' };

// 執行 node a.js
// 輸出順序可能會讓人驚訝
```

## 2009 年的模組生態

在 2009 年，Node.js 的模組生態才刚刚起步：

```
2009 年可用的模組：
───────────────────
- connect：HTTP 中介軟體框架
- express：Web 框架（還未發布，2010 年才出现）
- socket.io：WebSocket 封裝
- mongojs：MongoDB 驅動程式
- redis：Redis 客戶端

2009 年的限制：
────────────────
- 沒有 npm（2010 年 10 月才發布）
- 必須手動下載和安裝模組
- 模組数量不多
- 文件和社群还在发展中
```

## 結語

CommonJS 模組系統為 Node.js 提供了標準化的程式碼組織方式。透過 `require()` 和 `module.exports`，開發者可以輕鬆地分割、共享和重用程式碼。

雖然 2009 年 npm 還不存在，但 CommonJS 規範已經為未來的套件生態系奠定了基礎。

---

## 延伸閱讀

- [CommonJS 規範](https://www.google.com/search?q=CommonJS+specification)
- [Node.js 模組系統文檔](https://www.google.com/search?q=Node.js+module+system)
- [require() 原始碼解析](https://www.google.com/search?q=Node.js+require+source+code)

---

*本篇文章為「AI 程式人雜誌 2009 年 1 月號」歷史回顧系列之一。*