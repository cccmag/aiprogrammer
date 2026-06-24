# 前端建置工具：Vite

## 什麼是 Vite

Vite（法語「快速」之意）是由 Evan You（Vue.js 作者）開發的現代前端建置工具。與傳統的 webpack 不同，Vite 利用瀏覽器原生 ESM（ES Module）支援來提供極速的開發體驗。

### Vite 的核心優勢

1. **極速冷啟動**：不需要打包，直接提供原始碼
2. **即時 HMR**：模組級別的熱更新
3. **最佳化建置**：使用 Rollup 進行生產建置
4. **框架無關**：支援 React、Vue、Svelte 等

---

## 建立 Vite 專案

### 使用 create-vite

```bash
npm create vite@latest my-app -- --template react
# 或
npm create vite@latest my-app -- --template vue
# 或
npm create vite@latest my-app -- --template vanilla
```

### 專案結構

```
my-app/
├── index.html          # 入口 HTML
├── package.json
├── vite.config.js      # Vite 設定
├── public/             # 靜態資源
└── src/
    ├── main.js         # 入口 JS
    ├── App.jsx
    ├── style.css
    └── components/
```

### 常用指令

```bash
npm run dev      # 啟動開發伺服器
npm run build    # 生產建置
npm run preview  # 預覽生產建置
```

---

## Vite 核心概念

### 原生 ESM

Vite 開發伺服器直接以原生 ESM 提供原始碼，瀏覽器負責模組載入：

```html
<!-- index.html -->
<script type="module" src="/src/main.js"></script>
```

```javascript
// main.js
import { createApp } from "vue";   // 直接引入 npm 套件
import App from "./App.vue";       // 引入本地模組
```

### HMR（Hot Module Replacement）

當修改原始碼時，Vite 只更新被修改的模組，無需重新載入整個頁面：

```javascript
// main.js
if (import.meta.hot) {
  import.meta.hot.accept();
}
```

---

## vite.config.js

Vite 設定檔使用 ESM 語法：

```javascript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir: "dist",
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
        },
      },
    },
  },
  resolve: {
    alias: {
      "@": "/src",
    },
  },
});
```

---

## Vite 外掛系統

Vite 使用 Rollup 相容的外掛系統。常見外掛：

```javascript
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import react from "@vitejs/plugin-react";
import svelte from "@sveltejs/vite-plugin-svelte";
import legacy from "@vitejs/plugin-legacy";  // 舊瀏覽器支援

export default defineConfig({
  plugins: [
    react(),
    legacy({
      targets: ["defaults", "not IE 11"],
    }),
  ],
});
```

---

## Vite vs Webpack

| 特性 | Vite | Webpack |
|------|------|---------|
| 開發伺服器 | 原生 ESM，無需打包 | 需要打包全部檔案 |
| HMR 速度 | 即時，模組層級 | 較慢，需重新編譯 |
| 冷啟動 | 極快（< 1s） | 較慢（5-30s） |
| 設定複雜度 | 簡潔，合理預設 | 複雜，需大量設定 |
| 外掛生態 | Rollup 相容 | 成熟但複雜 |
| 生產建置 | Rollup | Webpack |

### 遷移至 Vite

從 webpack 遷移至 Vite 通常很直接：

1. 安裝 Vite 和對應的外掛
2. 建立 vite.config.js
3. 將 index.html 移到專案根目錄
4. 調整路徑別名
5. 測試 HMR 和建置

---

## Vite 進階功能

### CSS 處理

Vite 內建支援 CSS、PostCSS、CSS Modules 和預處理器：

```css
/* styles.module.css */
.card {
  padding: 16px;
  background: white;
}
```

```javascript
import styles from "./styles.module.css";
function Card() {
  return <div className={styles.card}>內容</div>;
}
```

### 靜態資源

自動處理圖片、字型等靜態資源：

```javascript
import logo from "./logo.svg";  // 回傳 URL
import imgUrl from "./image.png?url";  // 強制回傳 URL
```

### TypeScript 支援

Vite 內建 TypeScript 支援，無需額外設定：

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
});
```

---

## Vite 在 2024 年的生態

2024 年，Vite 已成為前端建置工具的事實標準：

- **React**：Create React App 官方推薦遷移至 Vite
- **Vue**：預設使用 Vite
- **Svelte**：官方範本使用 Vite
- **Solid**：推薦使用 Vite
- **Astro**：基於 Vite 構建
- **Nuxt 3**：底層使用 Vite
- **Vitest**：Vite 生態的測試框架

---

## 延伸閱讀

- [Vite 官方文件](https://www.google.com/search?q=Vite+official+documentation)
- [Vite vs Webpack 比較](https://www.google.com/search?q=Vite+vs+Webpack+comparison)
- [從 Webpack 遷移至 Vite](https://www.google.com/search?q=migrate+from+Webpack+to+Vite)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」精選文章之一。*
