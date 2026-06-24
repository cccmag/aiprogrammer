# React 生態回顧

## React 19：里程碑版本

2024 年七月 25 日，React 19 正式發布。這是自 React 16（2017）以來最大的一次更新。

### 新功能解析

**Actions**：將非同步操作與表單處理整合到 React 的資料流中。

**use() Hook**：直接在元件內部讀取 Promise，簡化資料獲取。

```javascript
function Comments() {
  const comments = use(fetchComments());
  return (
    <ul>
      {comments.map(c => <li key={c.id}>{c.text}</li>)}
    </ul>
  );
}
```

**Server Components**：RSC 成為官方推薦的資料獲取模式。

## Next.js 15

與 React 19 深度整合的 Next.js 15 在十月登場。Turbopack 已預設啟用。

## React Native

React Native 在 2024 年持續改進，新架構 (Fabric + TurboModules) 已成為預設選項。

## 狀態管理生態

| 函式庫 | 2024 狀態 | 趨勢 |
|--------|-----------|------|
| Zustand | 持續成長 | ↑ |
| Jotai | 原子化狀態管理 | ↑ |
| Redux Toolkit | 成熟穩定 | → |
| TanStack Query | 伺服器狀態標準 | ↑ |

## 測試工具

React Testing Library + Vitest 成為 React 測試的主流組合。

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import Counter from './Counter';

describe('Counter 元件', () => {
  it('應該正確遞增計數', async () => {
    const user = userEvent.setup();
    render(<Counter initial={0} />);
    
    await user.click(screen.getByText('+'));
    expect(screen.getByText('1')).toBeDefined();
    
    await user.click(screen.getByText('+'));
    expect(screen.getByText('2')).toBeDefined();
  });
});
```

## React 開發者調查

根據 State of React 2024，React 開發者滿意度達到歷史新高，主要來自 Server Components 與 Actions。

> 參考：https://www.google.com/search?q=React+ecosystem+2024+review
