# Focus 2：前端框架年度報告

## React 19：漫長等待的終點

2024 年七月，React 19 正式版終於發布。這是自 2013 年開源以來的第四個大版本。

### 重點功能

- **Actions**：表單處理的全新方式
- **use()**：直接在 render 中讀取 Promise 與 Context
- **Server Components**：正式穩定，Next.js 深度整合
- **ref as prop**：不再需要 forwardRef

```javascript
// React 19 Actions 範例
function UserForm() {
  const [error, formAction, isPending] = useActionState(
    async (prevState, formData) => {
      const name = formData.get('name');
      const res = await fetch('/api/users', {
        method: 'POST',
        body: JSON.stringify({ name })
      });
      if (!res.ok) return { error: '新增失敗' };
      return { success: true };
    },
    { error: null }
  );

  return (
    <form action={formAction}>
      <input name="name" required />
      <button type="submit" disabled={isPending}>
        {isPending ? '處理中...' : '送出'}
      </button>
      {error && <p>{error}</p>}
    </form>
  );
}
```

## Next.js 15 穩定版

Next.js 15 於十月發布，全面支援 React 19、Turbopack 正式可用、快取策略重新設計。

## Vue 3.5

Vue 3.5 在 2024 年推出，專注於效能優化與開發體驗改進。響應式系統重寫帶來更快的更新速度。

## Svelte 5 里程碑

Svelte 5 引入 runes 響應式系統，改變了元件撰寫方式。

## 前端框架趨勢

| 框架 | 2024 關鍵動向 |
|------|--------------|
| React | 19 大版本、Server Components 穩定 |
| Next.js | 15 穩定、Turbopack 正式版 |
| Vue | 3.5 效能優化、Vapor Mode 預覽 |
| Svelte | 5 runes、效能提升 |
| Solid | 持續成長、精簡高效 |

> 參考：https://www.google.com/search?q=frontend+frameworks+2024+review
