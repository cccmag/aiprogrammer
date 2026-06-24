# 回顧與結語

## 本月主題總結

2026 年 10 月號的 AI 程式人雜誌深入探討了「用 Rust 寫 Linux 驅動程式」這個主題。從 2020 年的初始 RFC 到 2026 年的今天，Rust 在 Linux 核心中的旅程見證了系統程式設計的典範轉移。

### 我們學到了什麼？

**核心模組的基礎**展示了一個 Rust 核心模組從初始化到卸載的完整生命週期，以及 `kernel` crate 如何將核心 API 包裹在型別安全的 Rust 抽象中。

**字元設備驅動程式**是 Rust 安全保證最直觀的展示——`FileOperations` trait 和 `Mutex` 這樣的同步原語，在編譯期就消滅了 C 語言驅動程式中常見的緩衝區溢位和競爭條件。

**平台驅動程式與裝置樹**展示了 Rust 如何與 Linux 的裝置模型無縫整合——透過 `PlatformDriver` trait 和 Device Tree 匹配，開發者可以用更少、更安全的程式碼完成同樣的工作。

**PCI 與 USB 驅動程式**則暴露了驅動開發中最棘手的部分——DMA 緩衝區管理、BAR 空間映射、中斷處理——而這些恰好是 Rust 所有權模型的最大勝利場。

**網路驅動程式與 XDP**說明了在要求極致效能的場景中，Rust 的零成本抽象不會成為瓶頸——NAPI、XDP、硬體卸載——這些複雜機制在 Rust 中運作良好。

**GPU/DRM 驅動程式**作為核心中最複雜的驅動類型，展示了 Rust 在管理複雜狀態機和記憶體層級方面的獨特價值。

**AI 輔助驅動程式開發**則展望了未來——LLM 正在從框架生成、bindings 自動化到安全審計等多個維度改變驅動程式的開發方式。

### 本期程式實作：mini-kmod

我們的 mini-kmod 專案雖然只是使用者空間的模擬，但它精確地捕捉了核心驅動程式的核心模式——模組生命週期、MMIO 暫存器操作、字元設備操作、ioctl 命令分派、中斷處理和平台裝置模型。透過這個專案，即使沒有核心開發經驗的讀者也能理解驅動程式的基本架構。

### 驅動程式開發的未來

隨著 Linux 8.0 將 Rust 支援標記為穩定，以及 Linux 8.1 引入統一的裝置模型抽象層，Rust 在核心中的地位已不可逆轉。我們正處於一個過渡期：

- **2024-2025**：實驗階段，早期採用者建立信心
- **2026-2027**：主流採用階段，新驅動程式優先考慮 Rust
- **2028+**：常態化階段，Rust 成為核心驅動程式開發的預設語言

對於想要開始學習 Rust 核心驅動程式開發的讀者，建議如下：

1. **先從使用者空間開始**：理解 Rust 語言本身和標準 crate 生態
2. **學習 mini-kmod**：理解驅動程式的核心模式
3. **閱讀真實 Rust 驅動程式碼**：核心 `samples/rust/` 目錄下有多個範例
4. **從簡單的字元設備起步**：不要直接挑戰 GPU 驅動
5. **善用 AI 工具**：LLM 可以大幅加速框架生成和程式碼理解

### 未來展望

下個月（2026 年 11 月號），我們將探討 **AI 代理系統與自動化程式設計**——從 AutoGPT 到 Claude Agent，從 ReAct 模式到工具使用——一個正在重新定義軟體開發本身的領域。

感謝閱讀本期的 AI 程式人雜誌。如果你有任何問題或建議，歡迎在我們的 [GitHub 專案](https://github.com/ccckmit/aiprogrammer) 上提出。

---

**編輯**：陳鍾誠 (ccckmit)

**生成**：OpenCode + Big Pickle 模型

**回到**：[本期目錄](README.md)

## 參考資源

- [Rust for Linux 專案](https://www.google.com/search?q=Rust+for+Linux+kernel)
- [Linux 核心 8.0 發布公告](https://www.google.com/search?q=Linux+8.0+release)
- [Linux 核心 Rust 程式碼範例](https://www.google.com/search?q=Linux+kernel+Rust+samples)
- [Linux 裝置驅動程式（第三版）](https://www.google.com/search?q=Linux+device+drivers+third+edition)
- [Writing Linux Kernel Modules in Rust](https://www.google.com/search?q=Writing+Linux+kernel+modules+in+Rust)
