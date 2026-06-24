# 本月新知

## 2023 年 1 月程式與 AI 技術動態

### 處理器架構

**Intel 發布第 13 代 Raptor Lake 行動處理器**

Intel 在 CES 2023 上正式發布第 13 代 Core 行動處理器系列，代號 Raptor Lake。新系列採用 Intel 7 製程，最高 24 核心（8 P-core + 16 E-core）配置，並支援 DDR5-5600 與 DDR4-3200 記憶體。效能核心（P-core）的單執行緒效能提升約 15%，多執行緒效能因 E-core 數量增加而提升達 40%。

**AMD Ryzen 7000 系列 3D V-Cache 處理器登場**

AMD 在 CES 2023 上推出了 Ryzen 7 7800X3D，採用 3D V-Cache 技術，將額外的 64MB L3 快取堆疊在 CCD 之上，總 L3 快取達到 96MB。在遊戲場景中，7800X3D 相比非 3D V-Cache 版本平均提升約 15-20% 效能。

**RISC-V 生態系統快速成長**

RISC-V International 宣布 2022 年 RISC-V 核心出貨量突破 100 億顆，主要在物聯網和嵌入式市場。SiFive 發布了 Performance P670 處理器，支援 RISC-V 向量擴展（RVV 1.0），目標應用包括 AI 推理和邊緣運算。

### 程式語言與框架

**Python 3.12 發布第一個 alpha 版本**

Python 3.12 的 alpha 1 版本在 2023 年 1 月發布。新特性包括更佳的錯誤訊息、`Perf` 監控支援、`typing` 模組強化以及 `f-string` 的語法改進。PEP 695 引入的 Type Parameter 語法讓泛型型別定義更加簡潔。

**Rust 1.66 與 1.67 穩定發布**

Rust 1.66 引入了 `#[deprecated_safe]` 屬性和 `black_box` 函式的穩定化。Rust 1.67 則穩定了 `const` 泛型中的整數型別參數，讓泛型程式碼更加靈活。

**WebAssembly 在伺服器端持續擴展**

Wasmer 發布 3.0 版本，支援 WASI 預覽 2 和更快的編譯速度。Cloudflare Workers 宣布支援 Python（透過 Pyodide 編譯為 Wasm），標誌著 Wasm 在邊緣運算領域的進一步普及。

### AI 與機器學習

**ChatGPT 突破 1 億使用者**

OpenAI 的 ChatGPT 在 2023 年 1 月達到 1 億活躍使用者，成為史上成長最快的消費級應用。其基於 GPT-3.5 架構的對話能力引發了全球對大型語言模型的關注。

**微軟宣布對 OpenAI 的數十億美元投資**

微軟在 2023 年 1 月宣布追加對 OpenAI 的投資，總額達數十億美元。同時宣布將 ChatGPT 整合進 Azure 雲端服務、Bing 搜尋引擎和 Office 產品線。

**Stable Diffusion 2.1 與 ControlNet 發布**

Stability AI 發布 Stable Diffusion 2.1，改善了人體比例和文字生成品質。同時，ControlNet 架構的發布讓使用者可以透過邊緣圖、深度圖等條件精確控制影像生成結果。

**Meta 發布 LLaMA 語言模型**

Meta AI 在 2023 年初發表了 LLaMA（Large Language Model Meta AI），參數規模從 7B 到 65B 不等。LLaMA 展示了較小模型透過更多訓練資料可以達到超越大型模型的效能。

### 開發工具

**VS Code 2023 年 1 月更新**

VS Code 發布 2023 年 1 月更新（1.75 版），新增了更好的 Markdown 編輯體驗、終端機增強功能和 Git 圖形化操作改進。

**GitHub Copilot 商業版正式上線**

GitHub Copilot 的商業版（Copilot for Business）在 2023 年 1 月正式開放。與個人版相比，商業版提供了組織層級的管理功能、安全漏洞過濾和客製化政策設定。

### 業界動態

- **Apple 推出 M2 Pro 與 M2 Max 晶片**：採用第二代 5nm 製程，最高 12 核心 CPU + 38 核心 GPU，統一記憶體架構支援最高 96GB
- **NVIDIA RTX 4070 Ti 發布**：基於 Ada Lovelace 架構，支援 DLSS 3 和光線追蹤，起售價 799 美元
- **Linux 核心 6.2 rc 版本發布**：新增 Rust 基礎架構支援，為後續 Rust 驅動程式開發奠定基礎
- **Google 宣布 Pathways 語言模型 PaLM 2 開發中**：下一代大型語言模型，專注於多語言和多模態能力
