# 本月新知

## 2026 年 9 月程式與 AI 技術動態

### Rust 系統程式設計

**Rust for Linux 8.0 生態持續擴展**

Linux 核心 8.0 的 Rust 支援在上月穩定後，本月持續擴展。新的 Rust 網路驅動程式框架（Net-Rust）發布，支援 eBPF 風格的網路過濾器完全用 Rust 撰寫。核心中的 Rust 程式碼已超過 50 萬行，涵蓋網路、儲存、GPU 和 USB 子系統。

**Tock OS 3.0 發布**

Tock OS——用 Rust 寫的安全嵌入式作業系統——發布 3.0 版本。新版本引入了基於 Rust 型別系統的「權限沙箱」（Capability Sandbox），讓每個應用程式只能存取明確授予的硬體資源。Tock OS 3.0 支援 Cortex-M、RISC-V 和 x86 平台。

**RTIC v3 正式穩定**

RTIC（Real-Time Interrupt-driven Concurrency）框架發布 v3 穩定版。RTIC v3 引入了基於 Rust 型別系統的「靜態優先級分析」——所有任務的調度可行性在編譯時就被驗證。RTIC 已成為 Rust 嵌入式即時系統的標準框架。

**Rust 編譯器支援 Cortex-M85**

LLVM 19 發布後，Rust 編譯器新增了對 Arm Cortex-M85 處理器的完整支援。Cortex-M85 是 Arm 最高效能的微控制器核心，Rust 的支援讓開發者可以在 MCU 上使用 Rust 的所有安全保證。

### 程式語言與框架

**C 語言標準委員會借鑑 Rust 所有權模型**

C 語言標準委員會（ISO/IEC JTC1/SC22/WG14）正式成立了「Safe C」研究小組，探索在 C 語言中引入類似 Rust 所有權模型的語法。雖然這仍處於研究階段，但標誌著 C 社群對 Rust 記憶體安全理念的認可。

**Zig 0.15 發布：強調與 Rust 的互操作性**

Zig 0.15 發布，新增了自動生成 Rust FFI 綁定的功能。Zig 的 comptime 元程式設計能力使其成為 Rust 與 C 之間的理想橋樑——Zig 可以編譯為 C ABI 相容的靜態庫，然後由 Rust 透過 FFI 呼叫。

**WebAssembly GC 穩定**

W3C 宣布 WebAssembly GC（垃圾回收）提案正式穩定。Rust 的 Wasm 生態藉此可以更高效地與 JavaScript 互通——wasm-bindgen 現在可以自動處理 GC 物件的生命週期。

### AI 與機器學習

**Claude 5 的程式碼分析能力達到新高度**

Anthropic 的 Claude 5 在程式碼分析方面達到新里程碑——可以自動發現 Rust 程式碼中的記憶體安全漏洞，包括複雜的 unsafe 程式碼模式。在一項基準測試中，Claude 5 發現了 87% 的已知 Rust 安全漏洞，超越了專用靜態分析工具。

**AI 輔助 FFI 生成達到生產就緒**

多款 AI 工具新增了從 C 頭文件自動生成 Rust FFI 綁定的功能。這些工具不僅生成 bindgen 風格的綁定程式碼，還能自動包裹 unsafe 函式為安全的 Rust API——包括所有權語義的自動推斷。

**形式化驗證工具的 AI 整合**

形式化驗證工具（如 Kani、Creusot）整合了 AI 輔助功能——AI 可以自動生成驗證條件和契約（contract），大幅降低了形式化驗證的門檻。

### 開發工具

**VS Code 嵌入式開發套件**

微軟發布了 VS Code 的嵌入式 Rust 開發套件，整合了 Cortex-M 除錯器、即時變數監視和 RTOS 感知的任務可視化。

**cargo-embed 5.0**

cargo-embed 5.0 發布，支援一鍵編譯+燒錄+除錯的流程。新版本支援 JTAG/SWD 協議的自動偵測，以及與 VS Code 的除錯器整合。

### 業界動態

- **NASA 宣布使用 Rust 開發下一代太空船軟體**：基於 Rust 的記憶體安全保證和 RTIC 框架的即時能力
- **特斯拉採用 Rust 開發車載控制器**：替換部分 C 程式碼，重點是安全關鍵系統
- **Arm 發布官方的 Rust 嵌入式 HAL**：基於 embedded-hal 標準，支援所有 Cortex-M 系列
- **Rust 在航空電子領域達到 DO-178C Level A**：經過認證的 Rust 編譯器子集可用於安全關鍵航空軟體
