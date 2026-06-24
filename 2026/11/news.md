# 本月新知

## 2026 年 11 月嵌入式 Rust 與技術動態

### 嵌入式 Rust

**ESP32-C6 Rust 支援達到生產就緒**

樂鑫科技在本月宣布 ESP32-C6 (RISC-V) 的 Rust 支援已達到生產就緒等級。官方 `esp-hal` 現在支援 WiFi 6、Bluetooth 5.3 LE，以及全部的周邊中斷模式。ESP32-C6 是首款支援 Rust 原生 WiFi 驅動的主流 RISC-V MCU。

**embassy 0.20 發布：非同步嵌入式執行器重大更新**

embassy 是 Rust 嵌入式世界最重要的非同步執行器。0.20 版本引入了新的 time driver API、更有效率的 executor 排程演算法，以及對 Cortex-M85 的完整支援。embassy-usb 子 crate 也在本次發布中穩定。

**cortex-m-rt 0.9 支援多核心啟動**

cortex-m-rt 0.9 發布，新增對 ARM Cortex-M 多核心處理器的啟動支援。新的 `multi_core` 特性允許開發者定義輔助核心的入口點和中斷向量表，這對雙核心 MCU（如 STM32H7 系列）特別重要。

**嵌入式 Rust 工作小組宣布 2027 路線圖**

Rust 嵌入式工作小組發布了 2027 年路線圖草案，重點包括：async embedded-hal 正式穩定、統一的中斷模型、RISC-V 向量擴展支援，以及對 Armv8.1-M M-profile 的完整支援。

**Rust 在汽車嵌入式領域取得突破**

多家 Tier-1 汽車供應商聯合宣布成立「Rust in Automotive」聯盟，目標是在 2028 年前將 Rust 用於量產車型的 ADAS 控制單元。ISO 26262 ASIL-D 認證的 Rust 編譯器正在進行最終審查。

### 程式語言

**C++26 標準正式通過：引入 borrow checker 實驗性提案**

ISO C++ 標準委員會於本月正式通過 C++26 標準。最引人注目的是 borrow checker 的實驗性提案——這是 C++ 首次嘗試引入類似 Rust 所有權模型的靜態分析。該提案目前標記為「Experiential」，預計在 C++29 中正式納入。

**Zig 0.15 發布：編譯期記憶體安全分析**

Zig 0.15 引入了實驗性的編譯期記憶體安全分析器，可以檢測 use-after-free 和緩衝區溢位。Zig 團隊表示這項功能受到了 Rust 的啟發，但採用了不同的實現策略——在編譯期模擬所有執行路徑。

**TIOBE 指數：Rust 首次進入前五**

TIOBE 程式語言排行榜 11 月數據顯示，Rust 以 6.8% 的佔比首次進入前五名，超越了 Go（5.9%）和 JavaScript（5.7%）。C 語言仍以 14.2% 位居第一。

### AI

**Claude 6 發布：深度推理與程式碼生成大幅提升**

Anthropic 於 11 月初發布 Claude 6，在程式碼生成、深度推理和多模態理解方面有顯著提升。在 SWE-bench 3.0 上達到 86.4% 的解決率。在嵌入式 Rust 程式碼生成測試中，Claude 6 生成的 unsafe 區塊比 GPT-6 少了 35%。

**GitHub Copilot 推出「嵌入式模式」**

GitHub 宣布 Copilot 推出針對嵌入式開發的專用模式：能夠理解 MCU datasheet PDF、暫存器映射表、中斷向量表，並自動生成 PAC 層綁定程式碼。初步支援 STM32、ESP32、RP2040 三大平台。

**Google 發布 Rust 專用 AI 程式碼審查工具**

Google 的內部工具團隊開源了 `rusty-review`——一個專門針對 Rust 程式碼的 AI 審查工具。它能夠檢測 unsafe 程式碼的正確性、Send/Sync 實作的安全性，以及 embedded-hal 實作是否遵循規範。

### 開發工具

**probe-rs 0.28 發布：支援 500+ MCU**

Rust 原生除錯工具 probe-rs 發布 0.28 版本，新增對 80 款新 MCU 的支援，總支援數量突破 500 款。新版本還引入了即時變數監看（live watch）和 SWO 追蹤輸出。

**Rust Analyzer 2026-11 新增嵌入式感知**

Rust Analyzer 的最新更新加入了嵌入式開發感知功能：自動偵測 `#![no_std]` 目標、嵌入式 target triple 的建議、cortex-m-rt 中斷向量的自動補全。

**OpenOCD-RS 開源專案啟動**

社群開源了純 Rust 實作的 OpenOCD 替代方案 `openocd-rs`。初期支援 CMSIS-DAP 和 ST-Link 協定，目標是完全取代傳統 OpenOCD 的 Rust 除錯工作流程。

### 標準與規範

- **IEC 62304 醫療軟體標準納入 Rust**：國際電工委員會正式將 Rust 納入醫療設備軟體開發的推薦語言列表
- **NIST 發布嵌入式 Rust 安全指南**：針對物聯網裝置的 Rust 安全編碼實務，特別強調 `unsafe` 程式碼的審查流程
