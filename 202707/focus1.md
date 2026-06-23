# 從 MLOps 到 LLMOps 的演進（2015-2026）

## MLOps 的誕生：當機器學習遇到維運

2015 年，Google 在 NeurIPS 上發表了第一篇關於 MLOps 的論文，標誌著這個領域的正式誕生。在此之前，機器學習模型只是 Jupyter Notebook 中的原型——研究人員訓練完模型就交付，部署和維運是另一個團隊的事。

MLOps 的核心問題很簡單：**如何讓機器學習模型像軟體一樣可靠地部署和維運？**

第一個重大突破來自 Google 的 TFX（TensorFlow Extended），它在 2018 年開源，提供了從資料驗證到模型部署的完整管線。同年，Kubeflow 在 KubeCon 上發布，將 ML 工作負載帶入 Kubernetes 生態系。

2020 年，MLflow 1.0 發布，由 Databricks 主導開發，解決了實驗追蹤、模型註冊和部署的標準化問題。MLflow 的 `mlflow.log_param()` 和 `mlflow.log_metric()` 成為記錄實驗結果的事實標準。

```python
# MLflow 實驗追蹤範例
import mlflow

mlflow.set_experiment("model_training_v2")
with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("model_type", "xgboost")
    mlflow.log_metric("accuracy", 0.947)
    mlflow.log_metric("f1_score", 0.932)
    mlflow.sklearn.log_model(model, "model")
```

## LLM 帶來的全新維運挑戰

2022 年底 ChatGPT API 的發布徹底改變了遊戲規則。LLM 不是傳統的 ML 模型——它們不是用「準確率」就能衡量的，它們的輸出隨提示詞而變，它們需要的外部知識來自 RAG 管線。

這些差異帶來了全新的維運挑戰：

- **提示詞管理**：提示詞就是程式碼，需要版本控制、測試和部署
- **輸出品質監控**：LLM 的輸出沒有「正確答案」，只能衡量相關性、忠實度
- **RAG 管線可觀測性**：檢索 + 生成的兩階段管線需要端到端追蹤
- **AI Agent 行為追蹤**：多步驟推理 + 工具呼叫產生了難以除錯的行為軌跡

## MLOps vs LLMOps 對比表

| 面向 | MLOps | LLMOps |
|------|-------|--------|
| 部署單元 | 模型檔案（.pkl/.h5） | 模型 + 提示詞 + RAG 管線 |
| 評估指標 | 準確率、F1、AUC、RMSE | 相關性、忠實度、安全性、一致性 |
| 監控重點 | 資料漂移、模型衰退 | 輸出品質、提示詞注入、幻覺 |
| 版本控制 | 模型 + 資料集 | 模型 + 提示詞 + 文件 + 工具定義 |
| 測試策略 | 資料驗證 + 模型評估 | 提示詞測試 + 對抗性測試 + 紅隊測試 |
| 回滾機制 | 模型版本回退 | 提示詞回退 + 模型回退 + RAG 回退 |
| A/B 測試 | 模型版本比較 | 提示詞變體比較 + 檢索策略比較 |
| 可觀測性 | 模型效能指標 | 軌跡追蹤 + 輸出審計 + 成本分析 |

## LLMOps 的架構層次

```python
# 一個整合式 LLMOps 平台的架構示意
class LLMOpsPlatform:
    def __init__(self):
        self.prompt_registry = PromptRegistry()
        self.model_gateway = ModelGateway()       # 模型路由與負載均衡
        self.rag_pipeline = RAGPipeline()          # RAG 管線
        self.monitor = LLMMonitor()               # 即時監控
        self.evaluator = LLMEvaluator()           # 離線評估
        self.tracer = AgentTracer()               # Agent 軌跡
```

## 2026 年 AI 維運全景

到了 2026 年，AI 維運已經形成了一個成熟的三層結構：

1. **基礎設施層**：Kubernetes + GPU 叢集 + 模型服務框架（vLLM、TGI）
2. **平台層**：提示詞管理（Prompt Registry）、評估系統、監控儀表板
3. **應用層**：RAG 管線、AI Agent、對話系統

值得注意的趨勢是 **Prompt as Code** 的普及——提示詞不再是一個文字檔，而是像軟體一樣經歷開發、測試、審查、部署的生命週期。以及 **Observability-Driven Development**——在開發階段就嵌入可觀測性，而不是事後補救。

---

**下一步**：[模型監控與漂移偵測](focus2.md)

## 延伸閱讀

- [MLOps 發展歷史](https://www.google.com/search?q=MLOps+history+2015+2026)
- [LLMOps 指南與最佳實踐](https://www.google.com/search?q=LLMOps+guide+best+practices)
- [MLflow 官方文件](https://www.google.com/search?q=MLflow+documentation)
- [Kubeflow 與 LLM 部署](https://www.google.com/search?q=Kubeflow+LLM+deployment)
