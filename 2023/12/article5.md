# Rust 生態系統成長

## Rust 語言在 2023 年的生態發展與應用擴張

2023 年是 Rust 語言的關鍵之年。這一年，Rust 正式進入 Linux 核心，生態系統持續繁榮，應用領域從系統程式設計擴展到 WebAssembly、嵌入式開發和 CLI 工具。作為連續 8 年 Stack Overflow 最受喜愛的程式語言，Rust 正在從「有前景的語言」變成「真正重要的語言」。

---

## Linux 核心中的 Rust

### 歷史背景

Rust for Linux 專案始於 2021 年，目標是讓 Rust 成為繼 C 之後第二個可以編寫 Linux 核心驅動程式的語言。2023 年，這個目標開始實現。

### 2023 年的關鍵裡程碑

**6.1 核心**（2022 年 12 月）：最初的 Rust 基礎設施合併，包含 Rust 編譯器支援和核心 Rust 抽象。

**6.6 核心**（2023 年 10 月）：第一組 Rust 核心抽象（Rust abstractions）被合併。包括：
- `Arc`：原子引用計數
- `RefCount`：核心引用計數
- 異步基礎設施

**6.7 核心**（2023 年 12 月）：
- 第一個 Rust 網路驅動程式範例（NIC 驅動）
- Rust NVMe 驅動的初始工作
- 更多的核心抽象

### 為什麼用 Rust？

Linux 核心長期面臨一個問題：約 70% 的 CVE 漏洞是記憶體安全問題。Rust 的所有權系統可以在編譯時消除這些問題：

- **空指標解引用**：Option 類型防止
- **緩衝區溢出**：邊界檢查
- **釋放後使用**：借用檢查器防止
- **雙重釋放**：所有權系統防止

### 挑戰

Rust 進入核心面臨的挑戰：
- **學習曲線**：核心開發者需要學習新語言
- **工具鏈整合**：Rust 編譯器需要與核心建置系統整合
- **FFI 邊界**：Rust 與 C 介面之間的複雜性

---

## 生態系統成長

### crates.io 數據

2023 年底的 crates.io 統計：
- **套件總數**：超過 145,000 個
- **下載總量**：超過 500 億次
- **增長率**：全年增長約 21%

### 重要套件發布

- **Tokio 1.34**：異步執行器的持續改進
- **Serde 1.0.189**：序列化框架的穩定
- **Rocket 0.5**：Web 框架的重大更新
- **Axum 0.7**：Tokio 生態 Web 框架的成長
- **Bevy 0.12**：遊戲引擎的快速迭代
- **Tauri 2.0 Beta**：跨平台桌面應用框架

### Web 開發

Rust 在 Web 開發中的應用持續增長：

**前端**：
- **Leptos** 和 **Dioxus**：基於 WebAssembly 的前端框架
- **Yew**：React 風格的 WebAssembly 框架

**後端**：
- **Axum**：基於 Tower 和 Tokio 的 Web 框架
- **Actix-web**：高效能 Web 框架
- **Salvo**：新興的 Web 框架

---

## WebAssembly 生態

### Rust 與 WASM

Rust 是 WebAssembly 的主要開發語言。2023 年的進展包括：

- **wasm-pack 0.12**：更好的除錯和效能
- **wasm-bindgen**：與 JavaScript 的無縫互操作
- **WebAssembly System Interface（WASI）**：在伺服器端執行 WASM

### 應用案例

**邊緣運算**：
- **Cloudflare Workers**：支援 Rust 編寫的邊緣函數
- **Fastly Compute@Edge**：Rust 原生支援

**瀏覽器應用**：
- **Figma**：核心引擎使用 Rust/WASM
- **Visual Studio Code**：終端模擬器使用 Rust/WASM

---

## 嵌入式與 IoT

Rust 在嵌入式領域的優勢明顯：
- 零成本抽象
- 無 GC 的記憶體安全
- 優秀的交叉編譯支援

**2023 年發布的關鍵套件**：
- **embedded-hal 1.0**：硬體抽象層的穩定版本
- **RTIC v2**：即時中斷驅動並發框架
- **Embassy**：嵌入式異步執行器

---

## 採用情況

### 企業採用

2023 年採用 Rust 的主要組織：
- **Microsoft**：Windows 核心元件用 Rust 重寫
- **Google**：Android 中的 Rust 使用量持續增加
- **Meta**：原始碼控制（Sapling）、AI 框架（PyTorch 中 Rust 元件）
- **Amazon**：AWS Nitro 系統使用 Rust
- **Cloudflare**：Pingora（替代 Nginx 的 Rust 代理）

### 社群調查

Stack Overflow 2023 開發者調查：
- **最喜愛的語言**：Rust 第 8 年蟬聯第一（85%）
- **高薪語言**：Rust 開發者薪水中位數排名前 5
- **使用增長**：Rust 在專業開發者中的使用率持續增長

---

## 2024 年展望

- **Rust 2024 Edition**：新的語言版本，可能包含新的 trait 解析規則
- **更多的 Linux 核心 Rust 程式碼**：預計更多驅動程式將用 Rust 撰寫
- **Async Rust 改進**：非同步生態系統的持續完善
- **更好的 IDE 支援**：rust-analyzer 的持續改進
- **嵌入式生態成熟**：更多 HAL 和 BSP 支援

---

## 延伸閱讀

- [Rust for Linux 進展](https://www.google.com/search?q=Rust+for+Linux+2023+progress)
- [Rust 2023 年度報告](https://www.google.com/search?q=Rust+2023+annual+survey+results)
- [Rust 生態系統統計](https://www.google.com/search?q=Rust+crates.io+2023+statistics)

---

*本篇文章為「AI 程式人雜誌 2023 年 12 月號」文章系列之五。*
