# 本月新知

## 2026 年 10 月 Linux 核心、Rust 與 AI 技術動態

### Linux 核心與驅動程式

**Linux 8.1 發布：Rust 驅動程式框架大幅擴展**

Linux 核心 8.1 於本月發布，重點是 Rust 驅動程式框架的大幅擴展。新版本引入了統一的 Rust 裝置模型抽象層（Device Model Abstraction Layer, DMAL），讓 PCI、USB、平台裝置、I2C、SPI 等所有匯流排類型都能用一致的 Rust API 撰寫驅動程式。核心中的 Rust 驅動程式數量突破 200 個，涵蓋儲存、網路、顯示、音訊等子系統。

**Rust for Linux 專案發布 bindings 自動化工具**

Rust for Linux 專案發布了 `kernel-bindgen` 工具，可以從核心標頭檔案自動生成高品質的 Rust FFI 綁定。此工具支援智慧型指標推斷（例如將 `spin_lock_t` 自動轉換為 `SpinLock<T>`）和生命週期分析，大幅降低維護綁定的工作量。詳見[官方說明](https://www.google.com/search?q=Linux+kernel+Rust+bindgen+automation)。

**NVMe 驅動程式完全以 Rust 重寫完成**

Linux 核心的 NVMe 驅動程式經過兩年多的逐步遷移，終於在本月完成完全 Rust 化。新的 Rust NVMe 驅動在基準測試中展示了與 C 版本相當的 I/O 吞吐量，同時記憶體相關的錯誤（如釋放後使用、雙重釋放）已歸零。這是目前核心中最大規模的 Rust 驅動程式遷移專案。

**Intel 發布 Rust GPU 驅動程式初始版本**

Intel 發布了基於 Rust 的 Xe GPU 驅動程式初始版本，支援最新的 Arc GPU 架構。這是首個完全以 Rust 撰寫的現代 GPU 驅動程式，利用了 Rust 的型別系統來管理複雜的 GPU 命令緩衝區和記憶體物件生命週期。

### 程式語言

**Rust 1.85 發布：核心模組開發體驗改善**

Rust 1.85 發布，多項改進直接受益於核心開發者。新的 `no_std` 編譯最佳化減少了核心模組的二進位大小約 15%。此外，編譯器新增了 `#[kernel_module]` 屬性（目前為 nightly 專屬），簡化核心模組的入口點宣告。

**C 語言 Safe C 研究小組發布初步報告**

ISO/IEC JTC1/SC22/WG14 的 Safe C 研究小組發布了初步報告，提出了一套「借用檢查器」的語法提案，靈感來自 Rust 的借用規則。雖然短時間內 C 語言不太可能大規模採用這些特性，但這反映了 Rust 對 C 語言標準社群的深遠影響。

**eBPF 開始支援 Rust**

Linux 核心的 eBPF 子系統新增了原生 Rust 支援。開發者現在可以用 Rust 撰寫 eBPF 程式，並利用 Rust 的所有權模型確保 eBPF 驗證器的安全要求。此功能由 `aya` 專案與 Rust for Linux 團隊合作實現。

### AI

**Claude 6 發布：核心驅動程式自動生成**

Anthropic 發布 Claude 6，在程式碼生成方面達到了新高度——可以從裝置規格文件自動生成完整的 Linux 核心驅動程式框架。測試顯示，Claude 6 生成的 Rust 核心模組有 92% 的機率通過核心的嚴格審查規則。

**LLM 驅動的核心程式碼審計工具**

多個開源專案發布了專門用於核心程式碼審計的 LLM 工具。這些工具能夠分析核心驅動程式的 C 和 Rust 程式碼，自動識別競爭條件、記憶體洩漏和型別混淆等漏洞。在一項針對核心 8.0 驅動程式的測試中，AI 審計工具發現了 14 個先前未知的漏洞。

**DeepMind AlphaCode 3 支援系統程式設計**

DeepMind 的 AlphaCode 3 新增了對系統程式設計語言的深度支援，包括 Rust、C 和核心特定的 API。AlphaCode 3 可以理解核心抽象（如 `file_operations`、`platform_driver`）並生成符合核心風格指南的程式碼。

### 開發工具

**cargo-kmod 正式發布**

社群開發的 `cargo-kmod` 工具發布 1.0 版本，提供類似 `cargo build` 的體驗來建構 Linux 核心模組。它自動處理核心標頭路徑、交叉編譯、模組簽名和載入測試，讓核心模組開發變得像一般 Rust 專案一樣簡單。

**KernelCI 整合 Rust 核心模組測試**

KernelCI（Linux 核心持續整合基礎設施）正式整合 Rust 核心模組的測試支援。Rust 驅動程式現在會自動在超過 100 種硬體配置上進行編譯和運行測試，確保 Rust 驅動程式在不同架構上的可靠性。

**VS Code Kernel 擴充套件**

微軟發布了 VS Code 的 Linux 核心開發擴充套件，支援 Rust 和 C 核心模組的智慧型程式碼補全、核心 API 文件檢索和一鍵載入/卸載模組。該擴充套件整合了 `cargo-kmod` 和核心偵錯工具。

### 業界動態

- **Google 貢獻 Android 核心 Rust 驅動程式層**：Google 將 Android 的通用核心驅動程式層（包括 USB、電源管理、感測器）遷移至 Rust，預計在 Android 17 中全面啟用
- **AWS 開源 Nitro 安全晶片的 Rust 驅動程式**：AWS 將其 Nitro 虛擬化加速晶片的 Linux 驅動程式以 Rust 重寫並開源
- **Samsung 發表 Rust 核心驅動程式開發指南**：Samsung 發布了企業級的 Rust 核心驅動程式開發指南與最佳實踐
- **紅帽承諾在 RHEL 10 中全面支援 Rust 核心驅動程式**：紅帽宣布 RHEL 10 將把 Rust 核心驅動程式列為一級支援功能
