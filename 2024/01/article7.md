# ES6 模組系統

## 歷史背景

在 ES6 之前，JavaScript 沒有原生的模組系統。開發者使用各種變通方案：

```javascript
// 1. IIFE 模式（立即調用函數表達式）
var MyModule = (function() {
  var privateVar = '私有';
  function privateMethod() { /* ... */ }

  return {
    publicMethod: function() { /* ... */ }
  };
})();

// 2. CommonJS（Node.js）
const fs = require('fs');
module.exports = { myFunction };

// 3. AMD（瀏覽器非同步）
define(['dependency'], function(dep) {
  return { myFunction: function() {} };
});
```

ES6 終於引入了統一的模組語法，同時支援瀏覽器和伺服器端。

## 基本語法

### 匯出（export）

```javascript
// 命名匯出（Named Exports）
// utils.js
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export class Calculator { /* ... */ }

// 分批匯出
const E = 2.71828;
function multiply(a, b) { return a * b; }
export { E, multiply };

// 重新命名匯出
export { add as sum, PI as pi };

// 預設匯出（Default Export）
// math.js
export default class MathUtils {
  static square(x) { return x * x; }
}

// 同時使用命名和預設匯出
export const version = '1.0';
export default function helper() { /* ... */ }
```

### 匯入（import）

```javascript
// 匯入命名匯出
import { PI, add } from './utils.js';
import { PI as pi, add as sum } from './utils.js';
import * as Utils from './utils.js';

// 匯入預設匯出
import MathUtils from './math.js';

// 同時匯入命名和預設
import helper, { version } from './combined.js';

// 僅執行副作用（不匯入任何東西）
import './polyfills.js';

// 動態匯入（Dynamic Import）
async function loadModule() {
  const module = await import('./heavy.js');
  module.doSomething();
}
```

## 模組特性

### 嚴格模式

所有 ES6 模組預設啟用嚴格模式：

```javascript
// module.js
// 以下在嚴格模式下會報錯
// x = 10; // ReferenceError
// delete x; // SyntaxError
// with (obj) { ... } // SyntaxError
```

### 靜態分析

ES6 模組的 import/export 必須在頂層作用域，不允許動態條件匯入：

```javascript
// 正確
import { add } from './math.js';

// 錯誤：不能在條件語句中使用
// if (condition) {
//   import { add } from './math.js';
// }

// 正確：動態匯入使用 import() 函數
if (condition) {
  const module = await import('./math.js');
}
```

### 單例模式

模組只會被執行一次，後續的 import 都會取得同一個實例：

```javascript
// counter.js
let count = 0;
export function increment() { count++; }
export function getCount() { return count; }

// a.js
import { increment, getCount } from './counter.js';
increment();
console.log(getCount()); // 1

// b.js
import { getCount } from './counter.js';
console.log(getCount()); // 1（共享同一個 count）
```

## 模組解析規則

### 路徑解析

```javascript
// 相對路徑
import { foo } from './utils.js';  // 同一目錄
import { foo } from '../lib/utils.js'; // 上層目錄

// 絕對路徑（Node.js、Vite）
import { foo } from '/utils.js';

// 裸指定（bare specifier）— 由打包工具解析
import React from 'react';
import { useState } from 'react';
```

### 檔案副檔名

```javascript
// 瀏覽器 ES Modules 需要明確副檔名
import { foo } from './utils.js'; // 正確
// import { foo } from './utils'; // 錯誤（瀏覽器）

// Node.js 支援 CommonJS
// package.json 需設定 "type": "module"
// 或使用 .mjs 副檔名
```

## 實戰範例

### 建立工具庫

```javascript
// src/math.js
export const add = (a, b) => a + b;
export const subtract = (a, b) => a - b;
export const multiply = (a, b) => a * b;
export const divide = (a, b) => {
  if (b === 0) throw new Error('除數不能為零');
  return a / b;
};

// src/string.js
export function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function truncate(str, length = 100) {
  return str.length > length ? str.slice(0, length) + '...' : str;
}

// src/index.js（統一再匯出）
export { add, subtract, multiply, divide } from './math.js';
export { capitalize, truncate } from './string.js';
```

### 應用程式主入口

```javascript
// app.js
import { add, capitalize } from './src/index.js';

console.log(add(5, 3));        // 8
console.log(capitalize('hello')); // 'Hello'
```

## 與 CommonJS 的差異

```javascript
// CommonJS（Node.js 預設）
const fs = require('fs');
module.exports = { myFunc };
exports.helper = function() {};

// ES Module
import fs from 'fs';
export const myFunc = () => {};
export function helper() {}
```

**主要差異：**
- **CommonJS** 是動態載入，require 可以在條件語句中使用
- **ES Module** 是靜態載入，import 必須在頂層
- **CommonJS** 複製值，**ES Module** 是動態綁定（輸出的是引用）

## 打包工具

現代開發通常使用打包工具來處理模組：

```javascript
// Vite 設定（vite.config.js）
import { defineConfig } from 'vite';
export default defineConfig({
  build: {
    target: 'es2020',
    rollupOptions: {
      output: {
        format: 'es'
      }
    }
  }
});
```

## 結語

ES6 模組系統為 JavaScript 帶來了標準化的程式碼組織方式。模組化不僅讓程式碼更易於維護和測試，也為大型專案的開發奠定了基礎。

---

**延伸閱讀**

- [MDN JavaScript 模組](https://www.google.com/search?q=MDN+JavaScript+modules)
- [ES6 模組完整指南](https://www.google.com/search?q=ES6+modules+guide)
- [CommonJS vs ES Modules](https://www.google.com/search?q=CommonJS+vs+ES+Modules)
