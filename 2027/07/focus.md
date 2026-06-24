# 本期焦點

## AI 原生開發維運 — 從 MLOps 到 LLMOps

### 引言

當 AI 模型從研究專案進入生產環境，一個新的挑戰浮現：如何像管理軟體一樣管理 AI？

MLOps（Machine Learning Operations）在過去幾年建立了模型生命週期管理的標準做法。但 LLM 的出現帶來了全新的維運挑戰——提示詞版本管理、輸出品質監控、RAG 管線的可觀測性、以及 AI Agent 的行為追蹤——這些問題超越了傳統 MLOps 的範疇，催生了 LLMOps。

這不是單純的工具問題，而是思維轉變：
- **從模型中心到資料中心**：模型的品質取決於訓練資料和檢索資料的品質
- **從準確率到輸出品質**：LLM 的評估不是一個數字能衡量的
- **從靜態部署到動態提示**：提示詞像程式碼一樣需要版本控制、測試和部署
- **從監控到可觀測性**：你需要理解 AI 系統為什麼做出某個決定

本期將從 MLOps 的基礎開始，逐步進入 LLMOps 的實戰領域，幫助你建構可靠的 AI 生產系統。

---

## 大綱

* [程式：實作 Mini MLOps 平台](focus_code.md)
   - 模型監控與漂移偵測
   - 提示詞版本管理
   - A/B 測試框架
   - 評估與儀表板

1. [從 MLOps 到 LLMOps 的演進（2015-2026）](focus1.md)
   - MLOps 的誕生與成熟
   - LLM 帶來的全新維運挑戰
   - MLOps vs LLMOps 的比較
   - 2026 年的 AI 維運全景

2. [模型監控與漂移偵測（2018-2026）](focus2.md)
   - 資料漂移（Data Drift）與概念漂移（Concept Drift）
   - 監控指標：延遲、吞吐量、錯誤率
   - 漂移偵測演算法（PSI、KS-test）
   - LLM 特有的品質監控

3. [提示詞管理與版本控制（2022-2026）](focus3.md)
   - 提示詞即程式碼的思維
   - 提示詞版本管理策略
   - A/B 測試與漸進式發布
   - 提示詞資產管理（Prompt Registry）

4. [LLM 評估框架（2020-2026）](focus4.md)
   - 自動化評估指標（BLEU、ROUGE、METEOR）
   - LLM-as-Judge 評估方法
   - 人工評估流程設計
   - 回歸測試與閘道檢查

5. [RAG 管線的可觀測性（2023-2026）](focus5.md)
   - RAG 管線的追蹤（Tracing）
   - 檢索品質監控（MRR、NDCG、Hit Rate）
   - 生成品質監控（Faithfulness、Relevance）
   - 端到端延遲分析

6. [AI Agent 的行為追蹤（2024-2026）](focus6.md)
   - Agent 執行的可觀測性
   - 工具呼叫的監控與除錯
   - 多步驟推理的軌跡記錄
   - Agent 行為的安全審計

7. [AI 應用的持續交付（2020-2026）](focus7.md)
   - CI/CD for ML：從訓練到部署
   - 模型 A/B 測試與漸進式發布
   - 提示詞的持續部署
   - 基礎設施即程式碼（IaC）for AI

---

## MLOps 技術堆疊

```
監控層 (漂移偵測、品質指標、異常警報)
      │
評估層 (離線評估、線上評估、LLM-as-Judge)
      │
部署層 (模型服務、提示詞部署、A/B 測試)
      │
管線層 (訓練管線、評估管線、部署管線)
      │
版本層 (模型版本、資料版本、提示詞版本)
```

## 濃縮回顧

### MLOps 發展里程碑

| 年份 | 事件 | 意義 |
|------|------|------|
| 2015 | Google 發表 MLOps 概念 | ML 生命週期管理的起點 |
| 2018 | TFX、Kubeflow 發布 | 開源 MLOps 工具 |
| 2020 | MLflow 1.0 | 實驗追蹤標準化 |
| 2022 | ChatGPT API 發布 | LLMOps 需求爆發 |
| 2023 | LangSmith、Weights & Biases 支援 LLM | LLM 可觀測性 |
| 2025 | 提示詞管理成為標準實踐 | Prompt as Code |
| 2026 | AI Agent 監控框架成熟 | Agent Observability |

### MLOps vs LLMOps

| 面向 | MLOps | LLMOps |
|------|-------|--------|
| 部署單元 | 模型檔案 | 模型 + 提示詞 + RAG 管線 |
| 評估指標 | 準確率、F1、AUC | 相關性、忠實度、安全性 |
| 監控重點 | 資料漂移、模型衰退 | 輸出品質、提示詞注入、偏見 |
| 版本控制 | 模型 + 資料 | 模型 + 提示詞 + 文檔 |
| 測試策略 | 資料驗證 + 模型評估 | 提示詞測試 + 對抗性測試 |

### 提示詞版本管理的核心模式

```python
# prompt_manager.py — 提示詞即程式碼
class PromptTemplate:
    def __init__(self, name, version, template, params):
        self.name = name
        self.version = version
        self.template = template  # 使用 Jinja2 或 f-string
        self.params = params

    def render(self, **kwargs):
        return self.template.format(**kwargs)

# A/B 測試配置
ab_config = {
    "variant_a": PromptTemplate("summarize", "1.0", "摘要：{text}", ...),
    "variant_b": PromptTemplate("summarize", "2.0", "用三句話總結：{text}", ...),
}
```

### 漂移偵測

```python
def detect_drift(reference_stats, current_stats, method="psi"):
    """Population Stability Index (PSI) 漂移偵測"""
    psi = sum((p_i - q_i) * log(p_i / q_i) for p_i, q_i in zip(reference, current))
    return psi > threshold  # PSI > 0.2 表示顯著漂移
```

---

**下一步**：[程式實作](focus_code.md) → [從 MLOps 到 LLMOps](focus1.md)

## 延伸閱讀

- [MLOps 最佳實踐](https://www.google.com/search?q=MLOps+best+practices+2026)
- [LLMOps 指南](https://www.google.com/search?q=LLMOps+guide)
- [提示詞工程與管理](https://www.google.com/search?q=prompt+engineering+management)
- [AI 可觀測性工具](https://www.google.com/search?q=AI+observability+tools)
