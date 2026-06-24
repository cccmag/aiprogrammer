# 文章集錦

本期共 10 篇精選文章，深入探討用 Rust 撰寫 Linux 驅動程式的各個面向，從歷史發展到實戰教學，從底層機制到 AI 輔助開發。

## 程式相關文章

### [1. Linux 核心 Rust 支援發展史 — 從 2020 年 RFC 到 2026 年正式穩定](article1.md)

完整回顧 Rust 進入 Linux 核心的六年歷程。從 Miguel Ojeda 在 2020 年發布的初始 RFC，到 2021 年 Google 和 ISRG 宣布支援，2022 年初步合入 Linux 6.1，再到 2026 年 Linux 8.0 宣布正式穩定。本文記錄了這段改變 Linux 生態的歷史。

### [2. 字元設備驅動程式實戰 — 完整的 Rust 字元設備範例](article2.md)

字元設備是最基礎也最常見的 Linux 驅動程式類型。本文從 `module_init` 到 `file_operations`，展示如何用 Rust 撰寫一個完整的字元設備驅動程式，包含 read、write、ioctl、mmap 等操作的實作細節。

### [3. PCI 驅動程式開發指南 — PCI 列舉、BAR 空間、DMA](article3.md)

深入探討如何用 Rust 撰寫 PCI 驅動程式。涵蓋 PCI 裝置列舉、BAR（Base Address Register）空間的映射與存取、中斷處理、以及 DMA（Direct Memory Access）操作的安全抽象。

### [4. 網路驅動程式與 XDP — net_device_ops、NAPI、XDP hooks](article4.md)

探討 Rust 在網路子系統中的應用。從 `net_device_ops` 的註冊、NAPI 輪詢機制的實現，到新興的 XDP（eXpress Data Path）技術，展示如何用 Rust 的安全保證簡化網路驅動程式的開發。

### [5. GPU/DRM 驅動程式入門 — Direct Rendering Manager、GEM 緩衝區](article5.md)

GPU 驅動程式是核心中最複雜的驅動類型之一。本文介紹 Linux 核心的 Direct Rendering Manager（DRM）子系統架構，以及如何用 Rust 管理 GEM（Graphics Execution Manager）緩衝區物件，實現基本的顯示輸出。

## AI 相關文章

### [6. AI 輔助核心驅動程式開發 — LLM 生成驅動框架、自動化 bindings](article6.md)

探討大型語言模型如何在核心驅動程式開發中發揮作用。從 LLM 生成驅動框架模板、自動化 C 到 Rust 的 FFI 綁定生成，到智慧型核心 API 建議系統，LLM 正在重塑驅動程式的開發流程。

### [7. LLM 在核心安全審計中的應用 — 用 AI 發現驅動程式漏洞](article7.md)

安全審計是核心開發中最耗費人力的環節之一。本文探討如何利用 LLM 自動分析核心驅動程式程式碼，識別緩衝區溢位、競爭條件、權限提昇等漏洞，並與傳統靜態分析工具進行比較。

### [8. Rust for Linux 專案深度解析 — 專案架構、維護模式、社群治理](article8.md)

深入分析 Rust for Linux 專案的內部運作機制。包括核心抽象層（`kernel` crate）的架構設計、與上游 Linux 核心的整合策略、維護者模式、以及社群治理模型。

### [9. Linux 核心記憶體管理與 Rust — 核心記憶體配置器、Slab、頁面管理](article9.md)

核心記憶體管理是驅動程式開發的核心主題。本文探討 Rust 如何與 Linux 核心的記憶體管理子系統互動，包括核心記憶體配置器（kmalloc/vmalloc）、Slab 快取、頁面分配回收以及 IOMMU/IOVA 的管理。

### [10. 從 C 到 Rust：驅動程式遷移實戰 — 漸進式遷移策略、混合驅動](article10.md)

真實世界的驅動程式遷移不是非黑即白的選擇。本文分享從 C 到 Rust 的漸進式遷移策略，包括包裹式遷移、混合驅動架構、ABI 相容性處理、以及效能對比資料。

---

**回到**：[本期目錄](README.md)
