# 可觀測性工具生態

## 從開源到 SaaS 的選擇（2022-2028）

### 前言

AI 可觀測性的工具生態在過去六年快速擴張。從基礎的 Prometheus + Grafana 組合，到專門的 MLObs 平台，再到整合式的 AI 可觀測性方案——選擇合適的工具是建置可觀測性系統的第一步。

### 工具分類

**開源工具**

| 工具 | 用途 | 語言 |
|------|------|------|
| Prometheus + Grafana | 指標收集與視覺化 | Go / TypeScript |
| OpenTelemetry | 追蹤與日誌標準 | Multi-language |
| Evidently | 漂移檢測與報告 | Python |
| Alibi Detect | 進階漂移檢測 | Python |
| MLflow | 實驗追蹤與模型登錄 | Python |
| Langfuse (開源版) | LLM 可觀測性 | TypeScript |

**商業 SaaS**

| 平台 | 特色 | 開始支援 AI |
|------|------|------------|
| Datadog | APM + AI Monitor | 2022 |
| New Relic | AI Monitoring 插件 | 2023 |
| Arize AI | 專注模型可觀測性 | 2021 |
| WhyLabs | 模型漂移監控 | 2021 |
| Helicone | LLM 代理監控 | 2023 |
| LangSmith | LLM 應用除錯 | 2024 |

### 工具選擇決策樹

```
模型類型？
├── 傳統 ML（分類/迴歸）
│   └── Evidently + Prometheus
├── LLM（API 呼叫）
│   └── Helicone 或 LangSmith
└── 自訂深度學習
    └── Arize AI 或 WhyLabs
```

### OpenTelemetry 成為核心標準

2024 年後，OpenTelemetry 的 AI 語意慣例（Semantic Conventions）逐漸成熟。所有主要工具都支援 OTel 協定，讓可觀測性資料可以自由在不同工具間流動：

```
Application → OTel SDK → OTel Collector
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
           Prometheus      Jaeger         Loki
           (Metrics)      (Traces)       (Logs)
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                          Grafana
```

### 整合範例

以下展示如何使用 Evidently 串接 Prometheus：

```python
from evidently.metrics import DataDriftTable
from evidently.test_suite import TestSuite
from evidently.test_preset import DataStabilityTestPreset

suite = TestSuite(tests=[DataStabilityTestPreset()])
suite.run(reference_data=ref, current_data=cur)
# 結果可匯出為 JSON 供 Prometheus 抓取
suite.json()
```

### 2028 年的趨勢

1. **收斂到 OTel**：所有工具以 OpenTelemetry 為核心標準
2. **AI 驅動的分析**：可觀測性工具本身使用 LLM 進行根因分析
3. **邊緣監控**：模型在邊緣裝置上的可觀測性
4. **成本可觀測性**：追蹤每個推論請求的成本（API 費用、GPU 時間）

### 小結

沒有單一工具能解決所有可觀測性問題。最好的策略是：使用 OpenTelemetry 作為統一標準，搭配專注於特定問題的專業工具。從簡單開始（Prometheus + 結構化日誌），需要時再加入專用平台。

---

**下一步**：[程式實作：AI 監控系統](focus_code.md)

## 延伸閱讀

- [OpenTelemetry AI Standard](https://www.google.com/search?q=OpenTelemetry+AI+semantic+conventions+2025)
- [Arize AI Platform](https://www.google.com/search?q=Arize+AI+observability+platform)
- [Langfuse LLM Observability](https://www.google.com/search?q=Langfuse+LLM+observability)
- [Evidently Open Source](https://www.google.com/search?q=Evidently+open+source+ML+monitoring)
