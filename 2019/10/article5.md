# Node.js 13 發布：ES Modules 全面支持

## 前言

Node.js 13 於 2019 年 10 月發布，帶來了多項重要更新。本篇文章將重點探討 ES Modules 的支援情況以及 Node.js 13 的其他重要變化。

## ES Modules 在 Node.js 中的歷程

### CommonJS 的長期主導

多年來，Node.js 一直使用 CommonJS（CJS）作為預設的模組系統：

```javascript
// CommonJS 模組
const express = require('express');
const fs = require('fs');

module.exports = { foo, bar };
```

### ES Modules 的挑戰

ES Modules（ESM）在瀏覽器中是標準，但在 Node.js 中的支援面臨諸多挑戰：

- **靜態 vs 動態**：ESM 是靜態的，require 是動態的
- **延遲執行**：ESM 不允許根據條件延遲加載模組
- **檔案擴展名**：需要明確區分 .mjs 和 .js

## Node.js 13 的 ES Modules 支援

### 基本用法

Node.js 13 增強了 ES Modules 的支援：

```javascript
// my-module.mjs
export const foo = 'hello';
export function bar() { return 'world'; }

// main.mjs
import { foo, bar } from './my-module.mjs';
console.log(`${foo} ${bar()}`);
```

### package.json 中的 type 欄位

```json
{
    "name": "my-package",
    "type": "module",
    "main": "index.js"
}
```

### 與 CommonJS 的互操作

Node.js 13 支援 ESM 和 CJS 的混合使用：

```javascript
// ESM 中使用 CJS
import fs from 'fs';
// 或者
import { readFileSync } from 'fs';

// CJS 中使用 ESM（受限）
const myModule = await import('./my-module.mjs');
```

## Node.js 13 的其他重要更新

### 更新的 V8 引擎

Node.js 13 包含了更新的 V8 JavaScript 引擎：

```
V8 更新帶來的新特性：
- 可選鏈（Optional Chaining）實驗性支援
- 空值合併（Nullish Coalescing）實驗性支援
- 更快的陣列操作
```

### 診斷報告

Node.js 13 支援生成診斷報告：

```javascript
// 觸發診斷報告
process.report.writeReport('./diagnostic报告.json');

console.log(process.report.reportPath);
```

### 預設使用 ICU 資料

Node.js 13 預設啟用完整 ICU 資料：

```javascript
// 更好的國際化支援
const formatter = new Intl.DateTimeFormat('zh-TW', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
});
console.log(formatter.format(new Date()));
```

## 從 Node.js 12 到 13

### Node.js 12 LTS

Node.js 12（2019 年 10 月進入 LTS）帶來了：

| 特性 | 說明 |
|------|------|
| V8 7.6 | 更快的字串操作 |
| 預設啟用 TLS 1.3 | 更好的安全性 |
| Worker Threads | 實驗性但可用的多執行緒 |
| 診斷報告 | 增強的除錯能力 |

### Node.js 13 的新變化

| 變化 | Node.js 12 | Node.js 13 |
|------|------------|------------|
| ESM 支援 | 實驗性 | 繼續改進 |
| 預設 Node 版本 | 12.x | 13.x |
| V8 版本 | 7.6 | 7.8 |

## 開發者體驗的改善

### 更好的錯誤訊息

Node.js 13 繼續改善錯誤訊息的可讀性：

```javascript
// 錯誤訊息更加清晰
Error [ERR_REQUIRE_ESM]: Must use import to load ES Module
```

### 更好的預設安全設定

Node.js 13 加強了安全相關的預設設定：

```javascript
// 更好的安全預設值
process.env.NODE_OPTIONS = '--enable-source-maps';
```

## 過渡到 ES Modules 的建議

### 遷移策略

建議開發者逐步遷移到 ESM：

```javascript
// 步驟 1：在 package.json 中添加 "type": "module"
{
    "type": "module"
}

// 步驟 2：將所有 .js 改為 .mjs 或修改副檔名

// 步驟 3：將 require 改為 import

// 步驟 4：處理動態 require 的替代方案
const modulePath = `./${env}-config.js`;
const config = await import(modulePath);
```

### 雙模式封裝

許多函式庫開始支援雙模式：

```javascript
// 同時支援 ESM 和 CJS
export const foo = 'hello';

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { foo };
}
```

## 結論

Node.js 13 標誌著 Node.js 在 ES Modules 支援方面的重要進展。雖然完全的 ES Modules 支援仍需要一些時間，但開發者現在可以開始嘗試和使用這一新標準。建議開發者開始熟悉 ES Modules 的語法和模式，為未來的遷移做好準備。

---

**延伸閱讀**

- [Node.js 13 Release Notes](https://www.google.com/search?q=Node.js+13+release+notes)
- [ES+Modules+Node.js](https://www.google.com/search?q=ES+modules+Node.js+13)
- [Node.js+ESM+Migration+Guide](https://www.google.com/search?q=Node.js+ESM+migration+guide)