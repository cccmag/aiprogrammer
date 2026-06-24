# 本月新知

## 2024 年 4 月前端與 AI 技術動態

### React 生態系

**React 19 正式發布**

React 團隊於本月正式發布 React 19，這是一次重大版本更新。新版本引入了 React Server Components（RSC）的穩定支援，開發者可以在伺服器端渲染元件，減少客戶端 JavaScript 體積。此外，`use()` 這個全新的 Hook 讓開發者可以在 render 階段直接讀取 Promise 和 Context，大幅簡化了資料獲取的寫法。Actions API 的加入讓表單處理變得更加直覺，配合 `useActionState` 和 `useFormStatus` 兩個新 Hook，前端表單開發進入新時代。

**Next.js 15 發布**

Vercel 在本月推出 Next.js 15，完全擁抱 React 19 的生態系。新版本強化了 App Router 的穩定性，並引入了全新的 `@next/codemod` 工具協助升級。Partial Prerendering（PPR）功能正式穩定，讓頁面可以同時包含靜態和動態內容。

**Vite 6 發布前端工具鏈升級**

Vite 6 在 4 月帶來重大更新，支援更快的冷啟動和 HMR 速度。新的環境變數系統讓開發者可以更靈活地管理不同環境的配置。

### JavaScript 與 TypeScript

**TypeScript 5.4 發布**

微軟在本月發布 TypeScript 5.4，新增 NoInfer 工具型別，讓開發者可以更精確地控制型別推論。此外，Conditional Type 的效能獲得大幅優化。

**ECMAScript 2024 規範定案**

ECMAScript 2024 正式定案，新增 `Map.groupBy`、`Promise.withResolvers` 等實用功能。`RegExp v` flag 也正式納入標準，為正則表達式提供更強大的 unicode 支援。

### 新興框架與工具

**Svelte 5 進入 RC**

Svelte 5 在本月進入 Release Candidate 階段，最大的改變是引入了「runes」系統──`$state`、`$derived` 和 `$effect` 等編譯時期語法，讓反應性系統更加透明。

**Solid.js 2.0 開發中**

Solid.js 團隊宣布 2.0 版本的開發計畫，將專注於改善開發者體驗和伺服器端渲染支援。Solid.js 1.8 也在本月發布，帶來了更好的 `Suspense` 支援。

**Astro 4.5 支援多頁面 Islands**

Astro 4.5 引入多頁面 Islands 架構，允許開發者在多個頁面間共享互動式元件，同時保持靜態輸出的優勢。

### CSS 與設計系統

**CSS 新功能支援**

Chrome 125 和 Firefox 126 在本月全面支援 CSS Anchor Positioning，讓開發者可以將浮動元素相對於特定錨點定位。這對 tooltip、popover 和下拉選單的實作有重大意義。

**Tailwind CSS v4 開發進展**

Tailwind CSS 團隊展示 v4 版本的開發進度，新版本將全面擁抱 CSS 原生特性，支援 CSS Nesting 和 Container Queries。

### 開發工具與平台

**Deno 1.43 改進相容性**

Deno 在本月更新至 1.43，大幅改進了與 Node.js 的生態相容性，現在可以執行更多原本僅限於 Node.js 的套件。

**ESLint 9.0 發布**

ESLint 9.0 是本月的另一個大新聞。新版本使用全新的扁平化配置格式（Flat Config），移除了傳統的 `.eslintrc` 配置方式，讓配置更加直觀和可組合。

### AI 輔助開發

**GitHub Copilot 推出 Workspace 模式**

GitHub Copilot 推出 Workspace 模式，可以理解整個專案的結構並提供跨檔案的建議，對於前端專案尤其有幫助。

**V0 由 Vercel 推出**

Vercel 發布 V0 工具，允許開發者用自然語言描述 UI，直接生成 React 元件程式碼，支援 shadcn/ui 和 Tailwind CSS。

### 標準與規範

- **W3C 發布 WebGPU 1.0**：為 Web 上的高效 GPU 運算開啟新紀元
- **Interop 2024 聚焦**：Anchor Positioning、CSS Nesting 和 View Transitions
- **Core Web Vitals 更新**：Google 宣布 INP（Interaction to Next Paint）正式取代 FID
