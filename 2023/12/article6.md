# WebAssembly 進展

## WASM 在 2023 年的技術演進與應用場景

2023 年是 WebAssembly 從「瀏覽器技術」向「通用運算平台」轉變的關鍵之年。Component Model 的標準化、WASI 的成熟、邊緣運算的普及，以及 AI 領域的應用探索，讓 WebAssembly 的影響力持續擴大。

---

## WASM 在瀏覽器中的進展

### 瀏覽器支援

2023 年，所有主流瀏覽器（Chrome、Firefox、Safari、Edge）都全面支援 WebAssembly MVP（Minimum Viable Product）。新功能也在加速落地：

**WebAssembly GC**：
- 2023 年底，Chrome 和 Firefox 穩定支援 WASM GC
- 允許垃圾回收語言的代碼直接編譯成 WASM
- Kotlin、Dart、Java 等語言可以在瀏覽器中更高效地運行

**Fixed-Width SIMD**：
- 所有瀏覽器都支援 128-bit SIMD
- 在音頻/視頻處理、遊戲和科學計算中帶來顯著效能提升

**Multi-Memory**：
- 允許多個線性記憶體實例
- 對模組化和安全隔離有重要意義

### 效能提升

瀏覽器廠商在 2023 年持續優化 WASM 執行效能：

- **Liftoff 編譯器**：V8 的基礎編譯器，編譯速度提升 2 倍
- **Wasmtime**：優化了 aka 呼叫開銷
- **SpiderMonkey**：改進了 WASM 的 inline caching

---

## Component Model 與標準化

### 什麼是 Component Model？

WebAssembly Component Model 是 WASM 生態中的重要標準，它解決了 WASM 模組之間的互操作問題：

- **語言無關**：用不同語言（Rust、C、Go、Python）編譯的 WASM 模組可以互通
- **類型安全**：在模組邊界提供強類型檢查
- **資源管理**：自動處理跨語言記憶體管理

### 2023 年進展

W3C WebAssembly 工作組在 2023 年取得了重要進展：

**Component Model Phase 3**：
- 規範進入 Phase 3（候選推薦）
- 多個實作（wasm-tools、Jco、Wasmtime）支援 Component Model
- `wit`（WebAssembly Interface Types）語言成為標準

**WIT 範例**：

```wit
// 一個簡單的 WASM 元件介面
package example:counter;

interface counter {
  record count {
    value: u32,
    label: string,
  }

  increment: func() -> count;
  get-count: func() -> u32;
  reset: func();
}
```

---

## WASI：WASM 的系統介面

### WASI 0.2 發布

2023 年，WASI 0.2 成為重大里程碑。WASI（WebAssembly System Interface）定義了 WASM 與作業系統互動的標準介面。

**WASI 0.2 的新功能**：
- **檔案系統 I/O**：標準化的檔案讀寫介面
- **網路 socket**：TCP/UDP 支援
- **時鐘和隨機數**：時間和隨機數生成
- **標準 I/O**：stdin/stdout/stderr

### WASI 與容器化

WASI 的成熟讓 WASM 在伺服器端成為容器的輕量級替代方案：

- **啟動時間**：微秒級（對比容器的毫秒級）
- **記憶體佔用**：KB 級（對比容器的 MB 級）
- **安全性**：基於能力的權限模型（Capability-based Security）

---

## 邊緣運算與 WASM

### 主要平台

2023 年，WASM 成為邊緣運算的主要技術選擇：

**Cloudflare Workers**：
- 支援 WASM 原生運行
- Workers AI 可以運行 ONNX 格式的 AI 模型
- D1 資料庫與 WASM Workers 整合

**Fastly Compute@Edge**：
- 基於 Lucet/Wasmtime 的執行環境
- 支援 Rust、AssemblyScript、TinyGo

**Fermyon Technologies**：
- Spin：用於建構 WASM 微服務的框架
- Nomad（HashiCorp）中 WASM workload 支援

### 優勢

WASM 在邊緣運算中的優勢明顯：
- **冷啟動極快**：完全沒有容器啟動延遲
- **資源效率高**：可以在資源受限的邊緣裝置上運行
- **安全隔離**：沙箱模型比容器更安全
- **可移植性**：一次編譯，到處執行

---

## WASM 在 AI 中的應用

### 瀏覽器中的 AI 推論

2023 年，WASM 被用於在瀏覽器中執行 AI 模型：

**ONNX Runtime Web**：基於 WASM 的 ONNX 推理引擎，可以在瀏覽器中執行機器學習模型。

**Transformers.js**：在瀏覽器中使用 Hugging Face 的 Transformer 模型。支援：
- 文本分類
- 問答系統
- 文本生成
- 圖像分類

**MediaPipe**：Google 的 ML 解決方案支援 WASM 部署。

### 邊緣 AI

WASM 的輕量級特性使其成為邊緣 AI 推論的理想平台：
- 模型在雲端訓練，在邊緣以 WASM 格式部署
- 支援 GPU 加速（透過 WebGPU）
- 與容器相比，更適合資源受限的 IoT 裝置

---

## 工具鏈與開發體驗

### 編譯器支援

- **LLVM 17**：對 WASM 目標的持續優化
- **rustc**：WASM 是一級目標
- **Emscripten 3.1.50**：C/C++ 到 WASM 編譯
- **TinyGo**：Go 到 WASM 編譯

### 除錯工具

- **Chrome DevTools**：WASM debugging 改進（來源映射、步進除錯）
- **wasm-tools**：WASM 工具鏈（反組譯、驗證、最佳化）

---

## 2024 年展望

- **Component Model 正式標準**：預計 2024 年達到正式推薦標準
- **WASI 1.0**：穩定的系統介面標準
- **WASM 在 AI 中的更深入應用**
- **更多的程式語言支援 WASM 作為一級目標**
- **WASM 在 IoT 和嵌入式領域的擴展**

---

## 延伸閱讀

- [WebAssembly 2023 年度報告](https://www.google.com/search?q=WebAssembly+2023+year+in+review)
- [WASI 0.2 發布說明](https://www.google.com/search?q=WASI+0.2+release+notes+2023)
- [Component Model 規範](https://www.google.com/search?q=WebAssembly+component+model+specification)

---

*本篇文章為「AI 程式人雜誌 2023 年 12 月號」文章系列之六。*
