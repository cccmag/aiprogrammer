# 本月新知

## 2019 年 10 月程式與 AI 技術動態

### 程式語言與框架

**Python 3.8 穩定版發布**

Python 3.8 於 2019 年 10 月正式發布，這是 Python 語言的又一重要里程碑。本次版本帶來了多項實用特性：

- **賦值表達式（Assignment Expressions）**：新增 `:=` 運算子，允許在表達式中直接賦值，例如 `if (n := len(a)) > 10`
- **位置-only 參數（Positional-Only Parameters）**：支援在函式定義中使用 `/` 標記位置參數
- **改進的語法提示**：typing 模組新增 TypedDict、Literal 等類型
- **效能提升**： pickle 模組序列化速度提升約 10%

**TypeScript 3.7 正式發布**

微軟於 2019 年 10 月發布 TypeScript 3.7，引入了多項開發者期待已久的功能：

- **可選鏈（Optional Chaining）**：支援 `obj?.prop?.method()` 語法
- **空值合併（Nullish Coalescing）**：新增 `??` 運算子
- **Assertion Functions**：更嚴格的類型斷言
- **Smart Selections**：用於包圍和取消包圍程式碼的編輯功能

**WebAssembly 持續獲得瀏覽器支援**

2019 年 10 月，主流瀏覽器對 WebAssembly 的支援持續強化。Chrome 和 Firefox 已完整支援 WebAssembly 的記憶體報告和參考類型。WebAssembly 正在從 Web 瀏覽器擴展到更多場景，包括伺服器端運算和區塊鏈智慧合約。

**Rust 2019 年度發展回顧**

Rust 語言在 2019 年持續穩定發展。Rust 2018 Edition 的各項功能已完全穩定，async/await 語法也更加成熟。生態系統持續擴展，crates.io 上的套件數量已突破 10,000 大關。

### AI 與機器學習

**Google 發布 ALBERT**

Google 研究團隊於 2019 年 9 月發布了 ALBERT（A Lite BERT），這是 BERT 的一個輕量級版本。ALBERT 使用了兩項核心技術：

- **引數共享（Parameter Sharing）**：跨層共享注意力權重，大幅減少參數量
- **句子順序預測（SOP）**：替代 Next Sentence Prediction（NSP）

ALBERT BASE 版本僅有 12M 參數（相比 BERT BASE 的 110M），但效能幾乎相當。

**預訓練模型成為 NLP 主流**

2019 年 10 月，預訓練語言模型已成為 NLP 領域的主流方法。Google 的 BERT、OpenAI 的 GPT-2、Facebook 的 RoBERTa 等模型相繼出現，推動了 NLP 任務的全面進步。

**T5 模型發布**

Google 於 2019 年 10 月發布了 T5（Text-to-Text Transfer Transformer）模型。T5 將所有 NLP 任務統一為文字對文字的格式，提供了一個通用的框架來處理翻譯、分類、摘要等任務。

**NLP 基準測試持續刷新**

基於 BERT 和類似模型的優化，NLP 各大基準測試的成績不斷提升。問答、情感分析、文字分類等任務的準確率已達到或超越人類水準。

### 開發工具與雲端服務

**GitHub 推出 Actions 正式版**

GitHub Actions 於 2019 年 10 月正式脫離 Beta 階段，成為 GitHub 的核心功能之一。開發者可以使用 Actions 自動化軟體開發工作流程，包括 CI/CD、程式碼品質檢查和部署。

**Visual Studio Online 發布**

微軟於 2019 年 11 月發布了 Visual Studio Online，這是一個基於雲端的開發環境。支援多人即時協作、Git 整合和 AI 輔助程式設計功能。

### 業界動態

- **蘋果發布 Swift 5.2**：改進了編譯器性能和錯誤訊息
- **Flutter 1.9 發布**：支援 macOS Catalina 和 iOS 13
- **Deno 1.0 預覽版發布**：Ryan Dahl 的新專案受到廣泛關注
- **TypeScript 支援突破 10 億下載**：成為最受歡迎的 JavaScript 超集

### 標準與規範

- **ES2019 定案**：正式納入 Array.prototype.flat、Optional Catch Binding 等特性
- **WebGPU 規範草案**：為 Web 上的 GPU 運算奠定基礎
- **HTTP/2 普及率超過 40%**：成為主流 Web 協定

### 延伸閱讀

- [Python 3.8 新特性](https://www.google.com/search?q=Python+3.8+release+October+2019)
- [TypeScript 3.7 Optional Chaining](https://www.google.com/search?q=TypeScript+3.7+optional+chaining+2019)
- [ALBERT Google 2019](https://www.google.com/search?q=ALBERT+Google+2019)