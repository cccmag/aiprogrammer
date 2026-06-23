# 多模型監控架構

## 前言

大型 AI 系統中，單一模型越來越少見。推薦系統可能包含數十個模型，LLM 應用則涉及 RAG、Guardrails 等多個元件。本文探討多模型監控的架構設計。

---

## 一、挑戰

| 挑戰 | 說明 |
|------|------|
| 異質性 | 不同框架（PyTorch/TF/ONNX） |
| 相依性 | 模型 A 輸出是模型 B 輸入 |
| 規模 | 數十到數百個模型 |
| 資源競爭 | GPU 記憶體、CPU 執行緒 |

---

## 二、統一監控抽象層

```python
from prometheus_client import Histogram, Gauge, Counter

class ModelMonitor:
    def __init__(self):
        self.latency = Histogram("inference_latency", "延遲",
            ["model"], buckets=[10, 50, 100, 200, 500])
        self.count = Counter("inference_total", "次數", ["model", "status"])
        self.drift = Gauge("feature_drift", "漂移", ["model", "feature"])

    def log(self, model, latency, status, drifts):
        self.latency.labels(model=model).observe(latency)
        self.count.labels(model=model, status=status).inc()
        for f, s in drifts.items():
            self.drift.labels(model=model, feature=f).set(s)
```

---

## 三、相依模型追蹤

```python
class PipelineTracker:
    def __init__(self):
        self.pipelines = {}

    def trace_pipeline(self, pipeline_id, models):
        self.pipelines[pipeline_id] = models

    def get_downstream_impact(self, upstream_model):
        impacted = set()
        for mid, models in self.pipelines.items():
            if upstream_model in models:
                idx = models.index(upstream_model)
                impacted.update(models[idx + 1:])
        return impacted
```

---

## 四、資源監控

| 資源 | 監控方式 | 常見瓶頸 |
|------|---------|---------|
| GPU 利用率 | nvidia-smi / DCGM | 記憶體不足 |
| CPU 使用率 | Node Exporter | 預處理瓶頸 |
| 記憶體用量 | cAdvisor | 模型載入過多 |

---

## 五、架構

```
Grafana ← Prometheus ← OTel Collector ← 各模型 Monitor
```

---

## 結語

關鍵在於統一抽象層與標準化指標命名。Prometheus + Grafana 可大幅降低大規模模型監控的維運成本。

---

## 參考資料

- https://www.google.com/search?q=multi+model+monitoring+architecture
- https://www.google.com/search?q=Prometheus+ML+model+metrics
- https://www.google.com/search?q=distributed+model+tracing+pipeline
