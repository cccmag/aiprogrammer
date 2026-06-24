# 本月新知

## 2024 年 1 月程式與 AI 技術動態

### ECMAScript 2024 (ES15) 正式定案

ECMAScript 2024 於本月正式定案，這是 JavaScript 語言的第十五個版本。新版本引入了多項備受期待的功能：

**`Array.prototype.groupBy` 與 `Array.prototype.groupByToMap`**

開發者現在可以更直覺地對陣列進行分組操作：

```javascript
const items = [
  { type: 'fruit', name: 'apple' },
  { type: 'fruit', name: 'banana' },
  { type: 'vegetable', name: 'carrot' },
];

const grouped = Object.groupBy(items, item => item.type);
// { fruit: [ { type: 'fruit', name: 'apple' }, { type: 'fruit', name: 'banana' } ],
//   vegetable: [ { type: 'vegetable', name: 'carrot' } ] }
```

**`Promise.withResolvers`**

簡化 Promise 的創建流程，不再需要手動儲存 resolve 和 reject：

```javascript
const { promise, resolve, reject } = Promise.withResolvers();
setTimeout(() => resolve('done'), 1000);
await promise; // 'done'
```

**正則表達式 `/v` flag**

新增的 Unicode 屬性轉義支援，讓正則表達式處理更強大。

### TC39 最新進展

TC39 委員會在 1 月的會議中討論了多項提案：

**Stage 3 提案更新：**
- `Temporal` API 進入 Stage 3，將成為 JavaScript 新的日期時間處理標準
- `Decorators` 提案持續推進，為類別和方法提供裝飾器語法
- `Import Assertions` 改進為 `Import Attributes`，增強模組載入控制

**新晉 Stage 2 提案：**
- `Pattern Matching` 提案引入強大的模式匹配語法
- `Records & Tuples` 提供不可變資料結構
- `Type Annotations` 提案讓 JavaScript 支援可選的型別註解

### JavaScript 生態系動態

**Node.js 21 成為 LTS 版本**

Node.js 21 於本月正式進入 LTS 階段，內建對 ECMAScript Modules 的完整支援，並將預設的 JavaScript 解析器切換為 V8 的最新版本。效能方面提升了約 15%。

**Deno 重大更新**

Deno 團隊發布 1.40 版本，重點改進了與 npm 套件的相容性，並引入了新的 WebGPU API 支援。Deno 的套件管理器 now 也支援更快的依賴解析。

**Bun 突破性進展**

Bun 1.0 持續獲得社群關注，其內建的 TypeScript 和 JSX 支援讓開發者可以零配置啟動專案。Bun 團隊宣布與 Node.js 的 API 相容性已達到 90% 以上。

### AI 與其他技術動態

**GPT-4 Turbo 正式上線**

OpenAI 發布 GPT-4 Turbo，支援 128K 上下文視窗，價格比 GPT-4 降低 50% 以上。新版本在程式碼生成和邏輯推理方面有顯著提升。

**Google Gemini Pro 開放 API**

Google 的 Gemini Pro 模型正式向開發者開放 API，支援多模態輸入和最多 32K token 的上下文長度。定價策略極具競爭力。

**WebAssembly GC 正式支援**

主流瀏覽器已全面支援 WebAssembly 垃圾回收（GC）提案，使得 Java、Kotlin、Dart 等語言可以更高效地編譯到 WASM 運行。

### 業界趨勢

- **Remix 與 Next.js 競爭白熱化**：雙方紛紛推出更強的 Server Components 支援
- **React Server Components 生產就緒**：React 團隊宣布 RSC 已達到生產穩定
- **ESLint 9.0 發布**：採用全新 Flat Config 系統，效能大幅提升
- **Playwright 取代 Cypress 趨勢**：微軟的 Playwright 在 E2E 測試領域市佔率持續上升

### 標準與規範

- **ECMAScript 2024 正式定案**：新增 groupBy、Promise.withResolvers 等功能
- **W3C 發布 HTML6 草案**：引入 Declarative Shadow DOM 等新特性
- **HTTP/3 採用率突破 30%**：主要 CDN 均已支援 QUIC 協定
- **WebGPU 1.0 候選推薦版發布**：為 Web 平台帶來現代 GPU 運算能力
