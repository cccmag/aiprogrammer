# 結語

## 理解 LLM，駕馭 LLM

從 2017 年的 Attention Is All You Need 到 2027 年的多模態 Agent，Transformer 架構的影響力橫跨了整整十年。本期我們從注意力機制的數學原理出發，一路探索到 RAG 系統的工程實踐。

### 關鍵學習

1. **注意力機制是核心** — 無論模型多大、架構多複雜，Scaled Dot-Product Attention 始終是 Transformer 的靈魂。理解它，你就理解了 LLM 的一半。

2. **RAG 是實戰首選架構** — 在大多數企業場景中，RAG 比單純微調更實用、更可控、更容易更新。檢索品質往往比模型大小更重要。

3. **從理解到實作** — 本期的迷你 Transformer 實作雖然簡單，但涵蓋了所有核心概念。動手寫一次注意力機制，比看一百篇文章更有幫助。

### 下一步

- 在本期 [Transformer 實作](focus_code.md) 的基礎上，嘗試用更大的資料集訓練
- 使用 LlamaIndex 或 LangChain 建構你的第一個 RAG 系統
- 探索 Hugging Face Transformers 和 PEFT 函式庫進行微調
- 參與 Chatbot Arena，了解當前最佳模型的實際表現

### 下期預告

2027 年 7 月號（202707）將探討 **AI 原生開發維運 — 從 MLOps 到 LLMOps**，涵蓋模型監控、A/B 測試、提示詞管理、以及 AI 應用的持續交付。

---

*AI 程式人雜誌 — 由 AI 撰寫，為程式人而作*
*本期編輯：陳鍾誠 | 生成引擎：OpenCode + Big Pickle*
