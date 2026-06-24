# Node.js 年度報告

## 版本回顧

2024 年 Node.js 的版本發布時程：

| 版本 | 發布日期 | 主要亮點 |
|------|---------|---------|
| 21.x (LTS) | 2023 Q4 | V8 11.8、ESM 改進 |
| **22.x (LTS)** | **2024-04** | **V8 12.2、node:test 穩定** |
| 23.x | 2024-10 | 效能優化、API 改進 |
| 24.x (Early) | 2024-12 | 前瞻功能預覽 |

## node:test 穩定化

Node.js 22 將 `node:test` 模組標記為穩定，讓開發者無需外部套件即可撰寫測試。

```javascript
import { test, describe, it, mock } from 'node:test';
import assert from 'node:assert';
import { sum, divide } from './math.js';

describe('數學函式庫', () => {
  it('應該正確計算加法', () => {
    assert.strictEqual(sum(1, 2), 3);
    assert.strictEqual(sum(-1, 1), 0);
  });

  it('應該處理除零錯誤', () => {
    assert.throws(() => divide(1, 0), /Cannot divide by zero/);
  });

  it('應該支援 mock', () => {
    const fn = mock.fn((a, b) => a * b);
    assert.strictEqual(fn(3, 4), 12);
    assert.strictEqual(fn.mock.callCount(), 1);
    assert.deepStrictEqual(fn.mock.calls[0].arguments, [3, 4]);
  });
});
```

## ESM 採用率

2024 年 ESM 在 npm 生態系統中的採用率突破 50%。

## 套件管理

npm、pnpm、yarn、bun 四強競爭。pnpm 在 monorepo 場景持續佔優。

## 效能改善

Node.js 22 的 V8 12.2 帶來顯著的效能提升，JSON 解析速度提升約 30%。

## 社群統計

- npm 總套件數：超過 250 萬
- 每週下載量：500 億次以上
- Node.js 貢獻者：超過 4000 人
- 下載量最大的套件：lodash、chalk、react

## 重要事件

2024 年 Express.js 的維護問題引發了對「過度依賴關鍵開源專案」的討論。

> 參考：https://www.google.com/search?q=Node.js+2024+annual+report
