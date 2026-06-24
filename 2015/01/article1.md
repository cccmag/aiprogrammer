# Node.js 0.12 發布：效能大幅提升

## 前言

2015 年 1 月，Node.js 0.12 正式發布，這是自 2014 年 io.js 分支以來的一次重要更新。這次版本帶來了顯著的效能提升和功能增強。

## V8 引擎升級

Node.js 0.12 整合了 V8 3.28 版本，帶來了 ES6 更好的支援：

```javascript
// Arrow Function（ES6）
const sum = (a, b) => a + b;

// Block scoping（ES6）
let x = 10;
const PI = 3.14159;

// Class（ES6）
class Rectangle {
  constructor(width, height) {
    this.width = width;
    this.height = height;
  }
  area() {
    return this.width * this.height;
  }
}
```

## 原生 Promise 支援

```javascript
// 無需 polyfill 即可使用 Promise
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve('完成！');
  }, 1000);
});

promise
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

## cluster 模組改進

```javascript
// 更好的負載平衡
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
  });
} else {
  // 改進的排程策略
  const server = require('http').createServer((req, res) => {
    res.writeHead(200);
    res.end('Hello World\n');
  });
  server.listen(8000);
}
```

## 效能提升數據

```
Node.js 0.10 vs 0.12 效能對比：
───────────────────────────────
HTTP 請求/秒：  +40%
記憶體使用：    -15%
啟動時間：      -25%
```

---

## 延伸閱讀

- [Node.js 0.12 發布公告](https://www.google.com/search?q=Node.js+0.12+released+January+2015)
- [Node.js 效能優化指南](https://www.google.com/search?q=Node.js+performance+tuning)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」文章之一。*