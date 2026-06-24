# JavaScript 2019：ES2019 與 Node.js 13

## 前言

JavaScript 在 2019 年繼續是 Web 開發的核心語言。ES2019 完成以及 Node.js 13 的發布是這一年的重要事件。

## ES2019

### 新特性

ES2019（ES10）在 2019 年完成：

```javascript
// Array.prototype.flat
const arr = [1, [2, [3]]];
arr.flat(2); // [1, 2, 3]

// Array.prototype.flatMap
[1, 2, 3].flatMap(x => [x, x * 2]); // [1, 2, 2, 4, 3, 6]

// 可選的 Catch Binding
try {
    // ...
} catch {  // 不需要 (error)
    // ...
}
```

### Object.fromEntries

```javascript
const obj = { a: 1, b: 2 };
const entries = Object.entries(obj);
const fromEntries = Object.fromEntries(entries);
```

## Node.js 13

### 重要更新

Node.js 13 在 2019 年帶來了重要變化：

```
Node.js 13：
- ES Modules 支援改進
- V8 引擎升級
- 診斷報告 API
```

### 對 ES Modules 的支援

Node.js 13 繼續改善 ES Modules 支援：

```javascript
// 在 package.json 中設置 "type": "module"
// 或使用 .mjs 擴展名
import { readFile } from 'fs';
```

## 結論

JavaScript/Node.js 生態在 2019 年繼續成熟。ES2019 的新特性和 Node.js 的持續改進，為開發者提供了更好的工具。

---

**延伸閱讀**

- [ES2019+features](https://www.google.com/search?q=ES2019+features)
- [Node.js+13+2019](https://www.google.com/search?q=Node.js+13+2019)