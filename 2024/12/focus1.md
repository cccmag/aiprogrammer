# Focus 1：2024 JavaScript 生態回顧

## Node.js 年度進展

2024 年 Node.js 發布了三個重要版本：22.x（四月）、23.x（十月）與 24.x（十二月，早期版本）。Node.js 22 帶來 V8 12.2、改進的 ESM 支援與新的 `node:test` runner 穩定版。

```javascript
// Node.js 22 的 ESM 改進範例
import { describe, it, mock } from 'node:test';
import assert from 'node:assert/strict';

describe('ESM 模組測試', () => {
  it('應該支援 top-level await', async () => {
    const data = await fetch('https://api.example.com/data');
    assert.ok(data.ok);
  });

  it('應該支援 mock 功能', () => {
    const fn = mock.fn(() => 42);
    assert.equal(fn(), 42);
    assert.strictEqual(fn.mock.callCount(), 1);
  });
});
```

## TypeScript 5.5

TypeScript 5.5 引入了 inferred type predicates，讓型別推斷更加精確。同時效能也有顯著改善。

## Deno 2 登場

Deno 2 RC 版在 2024 年釋出，最大亮點是與 Node.js 生態的相容性大幅提升。支援 npm 套件、package.json 和 node_modules。

## 套件管理競爭

Bun 1.x 持續發展，以驚人的效能吸引開發者。pnpm 成為 monorepo 首選。

## ESLint 9 重大改版

ESLint 9 將 flat config 設為預設格式，標誌著格式化規則的新紀元。

## 年度統計

- **npm 下載量**：每週超過 500 億次
- **Node.js 使用率**：全端開發者中 85% 使用 Node.js
- **TypeScript 採用率**：在 JavaScript 專案中佔比超過 60%

> 參考：https://www.google.com/search?q=JavaScript+ecosystem+2024+review
