# Node.js 12 發布：V8 引擎升級與 ES2019 支援

## 前言

Node.js 12 於 2019 年 4 月發布 LTS 版本，带来 V8 引擎升級和效能優化。

## V8 引擎升級

Node.js 12 採用 V8 7.4 引擎，带来以下改進：

```javascript
// 可選鏈（Optional Chaining）支援
const city = user?.address?.city;

// 空值合併（Nullish Coalescing）
const name = user.name ?? 'Anonymous';
```

## 效能提升

### 啟動時間優化

```bash
# Node.js 12 使用「預先編譯」技術
node --experimental-default-type=module app.js
```

### 記憶體管理

```javascript
// 更高效的 WebAssembly 支援
const wasm = require('wasm-polyfill');
```

## ES2019 新特性

```javascript
// Array.prototype.flat()
[1, 2, [3, 4]].flat();  // [1, 2, 3, 4]

// Array.prototype.flatMap()
[1, 2, 3].flatMap(x => [x, x * 2]);  // [1, 2, 2, 4, 3, 6]

// Object.fromEntries()
const obj = Object.fromEntries([['a', 1], ['b', 2]]);  // {a: 1, b: 2}

// String.prototype.trimStart/trimEnd
"  hello  ".trimStart();  // "hello  "
```

## TLS 1.3 支援

```javascript
const https = require('https');

const options = {
  secureProtocol: 'TLSv1_3_method'
};
```

## 結論

Node.js 12 的效能優化和 ES2019 支援使 JavaScript 生態系更加現代化。

---

**延伸閱讀**

- [Node.js 12 發布說明](https://www.google.com/search?q=Node.js+12+release+notes)
- [ES2019 新特性](https://www.google.com/search?q=ES2019+new+features)