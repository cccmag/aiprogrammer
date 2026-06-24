# JavaScript 歷史與生態

## 從 Mocha 到 JavaScript

### 1995：十天創造一個語言

1995 年，Netscape 公司正面臨一個挑戰：瀏覽器需要一種能在客戶端執行的腳本語言。Brendan Eich 被任命為設計師，他僅用了十天時間就完成了原型——最初命名為 Mocha，後改名為 LiveScript，最終在與 Sun Microsystems 合作行銷時定名為 JavaScript。

為什麼十天可以創造一個影響整個世界的語言？Eich 借鑒了多種語言的設計：
- **Scheme** 的函數式特性
- **Self** 的原型繼承
- **Java** 的 C 風格語法
- **Perl** 的正則表達式支援

```javascript
// 1995 年的 JavaScript 風貌
function validateForm() {
  var name = document.forms[0].name.value;
  if (name == "") {
    alert("請輸入姓名");
    return false;
  }
  return true;
}
```

### 瀏覽器大戰

Netscape 與 Microsoft 之間的瀏覽器大戰推動了 JavaScript 的快速演進。Microsoft 在 Internet Explorer 3.0 中推出了 JScript，本質上與 JavaScript 相容，但存在許多差異。這讓開發者陷入了跨瀏覽器相容性的噩夢。

## ECMAScript 標準化

### 標準的必要性

1996 年，Netscape 將 JavaScript 提交給 ECMA International 進行標準化。1997 年，ECMAScript 第一版（ES1）正式發布。

**ECMAScript 版本演進：**

| 版本 | 年份 | 重要特性 |
|-----|------|---------|
| ES1 | 1997 | 第一版標準 |
| ES2 | 1998 | 編輯器修正 |
| ES3 | 1999 | 正則表達式、try/catch |
| ES5 | 2009 | 嚴格模式、JSON 支援 |
| ES6 | 2015 | 箭頭函數、class、模組 |
| ES7 | 2016 | async/await 先驅 |
| ES8 | 2017 | async/await 正式 |
| ES9 | 2018 | Rest/Spread 屬性 |
| ES10 | 2019 | flat、flatMap |
| ES11 | 2020 | 可選鏈、nullish 合併 |
| ES12 | 2021 | Promise.any、邏輯賦值 |
| ES13 | 2022 | Top-level await |
| ES14 | 2023 | Array findLast |
| ES15 | 2024 | groupBy、Promise.withResolvers |

### ES6 的革命

2015 年發布的 ES6（又稱 ECMAScript 2015）是 JavaScript 史上最重要的版本更新。它引入了現代程式的核心特性：

```javascript
// ES6 帶來的新語法
const PI = 3.14159;
let count = 0;

// 箭頭函數
const add = (a, b) => a + b;

// class 語法
class Person {
  constructor(name) {
    this.name = name;
  }
  greet() {
    return `Hello, ${this.name}`;
  }
}

// 解構賦值
const [first, ...rest] = [1, 2, 3, 4];
const { name, age } = { name: 'Alice', age: 30 };
```

## Node.js 與全端 JavaScript

### 伺服器端的革命

2009 年，Ryan Dahl 創建了 Node.js，它基於 Google 的 V8 JavaScript 引擎，使 JavaScript 可以在伺服器端執行。這是一個重大突破：

```javascript
// Node.js HTTP 伺服器
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World\n');
});

server.listen(3000, () => {
  console.log('伺服器運行於 http://localhost:3000/');
});
```

Node.js 的成功帶動了整個 JavaScript 生態系的爆發：
- **npm**：套件管理器，目前擁有超過 200 萬個套件
- **Express**：最流行的 Web 框架
- **Electron**：跨平台桌面應用框架
- **React Native**：行動應用開發框架

## 現代框架生態系

### 前端三大框架

- **React**（2013）：Facebook 開發，基於 Virtual DOM 和元件化
- **Vue**（2014）：尤雨溪開發，輕量且易學
- **Angular**（2016）：Google 開發，完整的企業級框架

### 開發工具鏈

```javascript
// 使用 Vite 開發（2020 年後的現代工具）
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
```

### 新興替代方案

- **Deno**：Ryan Dahl 的新作品，原生支援 TypeScript
- **Bun**：極快的 JavaScript runtime 和打包工具
- **Svelte**：編譯時框架，無 Virtual DOM
- **Solid.js**：細粒度響應式框架

## 結語

從 1995 年十天創造的簡單腳本語言，到今天成為世界上最廣泛使用的程式語言，JavaScript 的演化史是一部技術創新的傳奇。理解這段歷史，有助於我們更好地掌握這門語言的設計哲學和使用方式。

---

**延伸閱讀**

- [JavaScript 創世記](https://www.google.com/search?q=JavaScript+history+Brendan+Eich)
- [ECMAScript 規範](https://www.google.com/search?q=ECMAScript+specification)
- [Node.js 官方文件](https://www.google.com/search?q=Node.js+documentation)
