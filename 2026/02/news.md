# 本月新知

## 2026 年 2 月程式與 AI 技術動態

### 程式語言與框架

**Mojo 正式版發布**

Mojo 語言於本月發布 1.0 正式版。這是由 Chris Lattner（LLVM 與 Swift 創始人）帶領開發的語言，專為 AI 與高效能運算設計。Mojo 融合了 Python 的語法與 Rust 的記憶體安全，能在 GPU、CPU 與 TPU 上高效執行。其最大亮點是支援 Python 生態系無縫整合，開發者可直接在 Mojo 中匯入 NumPy、PyTorch 等 Python 套件。

**Kotlin 2.2 帶來多平台編譯再進化**

JetBrains 發布 Kotlin 2.2，重點強化 Kotlin Multiplatform（KMP）的編譯速度與穩定性。新版本引入了「編譯器快取」機制，重複編譯速度提升 40%。同時 KMP 正式支援 iOS 原生 UI 開發，讓開發者能用同一份程式碼基礎建構 Android、iOS 與 Web 應用程式。

**Dart 4.0 推出巨集系統**

Google 發布 Dart 4.0，最受關注的是巨集（Macros）系統的正式引入。開發者現在可以在編譯時生成程式碼，減少重複的模板代碼。此外，Dart 4.0 強化了與 JavaScript 的互操作性，讓 Flutter Web 應用能更流暢地整合現有 JavaScript 生態系。

### AI 與機器學習

**DeepSeek-R1 引發開源推理模型之爭**

中國 AI 公司 DeepSeek 發布 DeepSeek-R1，這是一個專注於推理的開源模型，在多項推理基準測試中達到 GPT-4 級別水準。其獨特的 MoE（混合專家）架構和極低的訓練成本引發業界廣泛討論，也證明高品質開源模型可以以更低成本實現。

**Google 推出 Gemma 2 開源模型系列**

Google 發布 Gemma 2 開源模型系列，包含 2B、9B 和 27B 三種規模。Gemma 2 採用新的架構設計，在相同參數量下表現優於 Llama 3。Google 同時發布了 Gemma Scope，這是一套用於理解模型內部運作的可解釋性工具。

**PyTorch 3.0 進入 Alpha 測試**

PyTorch 團隊宣布 PyTorch 3.0 Alpha 版本，帶來多項重大更新：原生支援動態形狀（dynamic shapes）編譯、全新的量化工具鏈，以及更緊密的 TPU 整合。這些改進使得 PyTorch 在部署效率和硬體適應性上大幅提升。

**Hugging Face 開源 LeRobot 機器人框架**

Hugging Face 發布 LeRobot，這是一個開源的機器人學習框架，提供標準化的資料集、模型和模擬環境。LeRobot 支援從模仿學習到強化學習的多種機器人訓練方法，並與 ROS 2 生態系深度整合。

**RAG 技術持續演進**

檢索增強生成（RAG）技術在 2 月迎來多項突破。Meta 提出 GraphRAG，將知識圖譜與向量檢索結合，顯著提升多跳推理能力。Anthropic 則發布 Contextual RAG，讓檢索系統能感知對話上下文，提供更精確的資訊檢索。

### 開發工具與雲端服務

**GitHub Copilot 支援自訂指令**

GitHub 宣布 Copilot 新增「自訂指令」（Custom Instructions）功能，開發者可以定義編碼風格指南和專案規範，讓 AI 助理產生的程式碼更符合團隊標準。這項功能支援 .github/copilot-instructions.md 配置檔，可納入版本控制。

**AWS 推出 SageMaker Studio Lab 2.0**

AWS 發布 SageMaker Studio Lab 2.0，提供免費的 GPU 開發環境。新版本支援 JupyterLab 4.0、VS Code 整合，以及一鍵部署到 SageMaker 生產環境。這讓機器學習開發者可以無痛從實驗過渡到生產。

### 業界動態

- **Apple Vision Pro 出貨突破 300 萬台**，visionOS 2.0 推出 AI 驅動的空間理解功能
- **微軟宣布 Copilot 品牌統一**：Microsoft 365、GitHub 和 Windows 的 Copilot 將共用底層模型
- **Red Hat 發布 RHEL 10 Beta**：全面採用 Wayland，終結 X11 支援
- **NVIDIA H200 正式出貨**：記憶體容量與頻寬相比 H100 翻倍

### 標準與規範

- **歐盟 AI Act 正式生效**：分級監管制度上路
- **W3C 成立 AI 與 Web 工作組**：探索 AI 在 Web 標準中的角色
- **ISO 通過 C++ 26 部分特性**：包含 Reflection 和 Pattern Matching 的初步規範
