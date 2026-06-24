# 本月新知

## 2025 年 1 月程式與 AI 技術動態

### Python 生態系

**Python 3.13 穩定版持續推進**

Python 3.13 自 2024 年 10 月發布以來，社群持續為其生態系進行適配。3.13 版本引入了 JIT 編譯器（實驗性）、改良的直譯器、以及全新的 `__replace__` 協定。Python 3.13 在效能上有顯著提升，特別是在 CPU 密集型任務上。建議新專案直接使用 Python 3.12 或 3.13。

**PyPI 惡意套件檢測強化**

Python 軟體基金會宣布加強 PyPI 套件倉庫的安全審查機制。新的自動化掃描系統可檢測已知的惡意模式，並在可疑套件上線前進行人工審查。2024 年全年共攔截了超過 5000 個惡意套件上傳。

**FastAPI 成為最受歡迎的 Python Web 框架**

根據 JetBrains 的開發者調查，FastAPI 首次超越 Django 成為 Python 開發者最常使用的新 Web 框架。FastAPI 的非同步支援、自動 OpenAPI 文件生成、以及 Pydantic v2 整合是其受歡迎的主因。

### AI 與機器學習

**Google Gemini 2.0 正式上線**

Google 於 2025 年 1 月正式發布 Gemini 2.0 系列模型，在推理、編碼和多模態理解方面有顯著提升。新模型支援直接生成圖像和音訊，並強化了 Agent 能力，能夠自主完成多步驟任務。

**OpenAI o3 推理模型發布**

OpenAI 在 2024 年底發布了 o3 推理模型，其在前沿數學和程式設計基準測試上表現卓越。o3 在 ARC 視覺推理挑戰賽中取得了突破性成績，被認為是邁向通用人工智慧的重要一步。

**Llama 4 訓練細節公開**

Meta 公開了 Llama 4 系列模型的訓練細節。Llama 4 採用專家混合（MoE）架構，在多語言任務上的表現大幅優於前代。Meta 同時發表了新的對齊技術，在保持模型效能的同時降低了偏見。

**PyTorch 2.5 發布**

PyTorch 團隊於 2025 年 1 月發布 2.5 版本，重點包括：更快的 torch.compile 編譯速度、增強的非同步執行支援、以及新的量化 API。新版本還改善了對 Apple Silicon GPU 的支援。

**向量資料庫生態成熟**

2025 年初，向量資料庫市場迅速成熟。Chroma、Weaviate、Milvus 和 Pinecone 等產品都推出了重大更新。Chroma 發布 v1.0，支援多模態向量搜尋；Weaviate 整合了混合搜尋和生成式 AI 功能。

### 開發工具

**VS Code Python 擴充重大更新**

微軟於 1 月發布了 VS Code Python 擴充的重大更新，引入基於 AI 的程式碼建議、增強的除錯體驗、以及整合的 Jupyter Notebook 編輯器。新版本加快了擴充的啟動速度並減少了記憶體使用。

**GitHub Copilot 支援更多語言**

GitHub 宣布 Copilot 現在支援超過 50 種程式語言，並強化了對 Rust、Go 和 Kotlin 的程式碼生成能力。付費方案現在包含更長上下文的審查功能。

### 業界動態

- **Samsung 推出 AI 手機 Galaxy S25 系列**：內建 Gemini Nano 2，支援裝置端 AI 處理
- **Nvidia 發布 RTX 5090**：全新 Blackwell 架構，AI 推理效能提升 2 倍
- **Apple Vision Pro 銷量未達預期**：售價過高是主因，傳聞平價版將於 2025 年底推出
- **Hugging Face 與 AWS 深化合作**：提供企業級模型部署方案

### 標準與規範

- **歐盟 AI Act 正式生效**：全球首部全面性 AI 法規，影響深遠
- **Python 4.0 討論啟動**：Python 指導委員會開始討論 4.0 的可能方向
- **PEP 703 (no-GIL) 進入最終階段**：Python 將逐步移除全域直譯器鎖定

### 值得關注的開源專案

- **uv**：更快的 Python 套件管理器，由 Ruff 團隊開發
- **Ollama**：本地 LLM 執行工具，支援 Llama 4 和 Mistral
- **CrewAI**：多 AI Agent 協作框架
- **LiteLLM**：統一的 LLM API 呼叫介面
