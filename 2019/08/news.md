# 本月新知

## 2019 年 8 月程式與 AI 技術動態

### 程式語言與框架

**Go 1.13 正式發布**

Go 語言團隊於本月正式發布 Go 1.13，這是自 Go Module 引入以來最重要的版本。Module 功能正式穩定，成為 Go 依賴管理的默認方式。新版還帶來了 `go.mod` 和 `go.sum` 的正式支援，以及改進的 `go vet` 工具。錯誤處理方面，新增了 `errors.Is` 和 `errors.As` 函數，提供了更標準化的錯誤檢查方式。

此外，Go 1.13 提升了浮點數精度，增強了位移運算，並修復了多個長期困擾開發者的問題。編譯器優化也帶來了約 2-3% 的性能提升。

**Deno 1.0 預發布**

Ryan Dahl（Node.js 創始人）在本月宣佈 Deno 1.0 將於 2020 年 5 月正式發布。Deno 是一個基於 V8 的 JavaScript/TypeScript 運行時，採用 Rust 編寫，旨在解決 Node.js 的一些設計問題。

Deno 的主要特點包括：原生支援 TypeScript、默認安全的沙箱執行、去中心化依賴管理、以及內建的 HTTP/2 伺服器支援。雖然正式版尚未發布，但社群已經表現出濃厚的興趣。

**React 16.9 正式發布**

Facebook 發布了 React 16.9，這個版本標誌著 Concurrent Mode 接近完成。`useEffect` 的 cleanup 函數現在支持非同步操作，而 `React.StrictMode` 也增強了開發時的檢查。新的 `unstable_ConcurrentMode` API 被標記為即將棄用，為未來的 17.0 版本做準備。

### AI 與機器學習

**BERT 應用爆發**

2019 年 8 月，BERT 發布即將滿一年。這一年裡，BERT 催生了大量應用：

- Google Search 全面整合 BERT，提升搜尋理解能力
- 中文 NLP 任務全面採用 BERT 架構
- 醫療、金融、法律等領域的專業 BERT 模型相繼問世

預訓練 + 微調已成為 NLP 領域的新標準。

**GPT-2 安全性討論持續**

OpenAI 關於 GPT-2 安全性的討論仍在繼續。研究者提出多种检测 AI 生成文字的方法，同時也開發了更強大的語言模型。

**聯邦學習普及**

聯邦學習（Federated Learning）在本月獲得更多關注。Google 將其應用於 Gboard 鍵盤的改進，而蘋果也在 CoreML 中加入聯邦學習支援。這種保護隱私的機器學習範式正在從學術界走向工業應用。

### 雲端與開發工具

**Kubernetes 1.15 正式發布**

CNCF 發布 Kubernetes 1.15，這個版本的重點是 StatefulSet 和 Local PV 的 GA（正式可用）：

- Local PV 穩定化，用於本地儲存
- 增強的 Custom Resources
- 更好的 Windows 節點支援

**WebAssembly 走出瀏覽器**

WebAssembly 的應用場景正在擴展到瀏覽器之外：

- Fastly 推出 WASM 邊緣計算平台
- Cloudflare Workers 支援 WASM
- WASM 成為 serverless 的新標準

### 業界動態

- **華為發布鴻蒙 OS 開發者版本**：為物聯網裝置設計的作業系統
- **Stripe 開源 Fermi**：分布式的 HTTP 客戶端
- **GitHub 推出Actions 正式版**：CI/CD 功能全面可用
- **AWS 發布 Aurora Serverless v2**：自動擴展的無服務器數據庫

### 標準與規範

- **HTTP/3 草案發布**：QUIC 協議成為互聯網標準候選
- **TLS 1.3 全面普及**：更安全的加密標準
- **W3C 發布 WebGPU 初步規範**：為 Web 圖形運算打開新的大門

---

*本頁內容依照 [Google 新聞搜尋](https://www.google.com/search?q=2019+August+tech+news+programming+AI) 整理，相關連結僅供參考。*