# 即時模型監控

## 監控三大支柱

即時 AI 系統的監控不同於傳統軟體監控。除了系統指標（CPU、記憶體），還需要關注模型品質指標和資料漂移。本文介紹三大監控支柱：效能、資料品質、模型準確度。

## 推論延遲監控

```python
import time
import prometheus_client as prom

# Prometheus 指標定義
INFERENCE_LATENCY = prom.Histogram(
    'inference_latency_seconds',
    '模型推論延遲',
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05,
             0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
    labelnames=['model_name', 'device']
)

INFERENCE_COUNT = prom.Counter(
    'inference_total',
    '推論總次數',
    labelnames=['model_name', 'status']
)

@prom.register
def monitored_inference(model, features):
    start = time.time()
    try:
        result = model.predict(features)
        INFERENCE_COUNT.labels(
            model_name=model.name, status='success'
        ).inc()
        return result
    except Exception:
        INFERENCE_COUNT.labels(
            model_name=model.name, status='error'
        ).inc()
        raise
    finally:
        INFERENCE_LATENCY.labels(
            model_name=model.name, device=model.device
        ).observe(time.time() - start)
```

## 資料漂移偵測

模型在生產環境中的輸入分佈會隨時間改變。即時偵測資料漂移是維持推論品質的關鍵：

```python
import numpy as np
from scipy.stats import ks_2samp

class DriftDetector:
    def __init__(self, reference_dist, threshold=0.05):
        self.reference = reference_dist
        self.threshold = threshold
        self.window = []

    def update(self, sample):
        self.window.append(sample)
        if len(self.window) >= 100:
            stat, p_value = ks_2samp(
                self.reference, self.window
            )
            is_drift = p_value < self.threshold

            if is_drift:
                self.alert(p_value)

            self.window = []
            return is_drift
        return False

    def alert(self, p_value):
        prom.Gauge('data_drift_score',
                   'KS test p-value').set(p_value)
```

## 預測分佈監控

追蹤即時推論的輸出分佈，及早發現概念漂移：

```python
class PredictionMonitor:
    def __init__(self):
        self.mean = prom.Gauge(
            'prediction_mean',
            '推論輸出的平均值'
        )
        self.entropy = prom.Gauge(
            'prediction_entropy',
            '推論輸出的平均熵'
        )
        self.class_dist = prom.Counter(
            'prediction_class_total',
            '各類別預測次數',
            labelnames=['class_id']
        )

    def observe(self, logits):
        probs = softmax(logits)
        pred_class = np.argmax(probs)
        entropy = -np.sum(probs * np.log(probs + 1e-10))

        self.mean.set(np.mean(probs))
        self.entropy.set(entropy)
        self.class_dist.labels(
            class_id=str(pred_class)
        ).inc()
```

## 即時儀表板

```python
from fastapi import FastAPI
from prometheus_client import make_asgi_app

app = FastAPI()

# Prometheus 端點
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Grafana 告警規則可設定：
# 1. 延遲 P99 > 500ms → 告警
# 2. 錯誤率 > 1% → 告警
# 3. 資料漂移 p < 0.01 → 告警
```

## 自動回退機制

當監控指標觸發閾值時，自動切換到備用模型：

```python
class AutoFallback:
    def __init__(self, primary, backup, monitor):
        self.primary = primary
        self.backup = backup
        self.monitor = monitor
        self.activated = False

    def predict(self, features):
        if self.activated:
            return self.backup.predict(features)

        result = self.primary.predict(features)
        self.monitor.observe(result)

        if self.monitor.drift_detected or \
           self.monitor.error_rate > 0.05:
            self.activated = True
            self.alert_team()

        return result
```

## 延伸閱讀

- [Prometheus 監控最佳實務](https://www.google.com/search?q=Prometheus+monitoring+best+practices)
- [ML 模型漂移偵測](https://www.google.com/search?q=ML+model+drift+detection+methods)
- [Grafana 即時儀表板](https://www.google.com/search?q=Grafana+real+time+monitoring+dashboard)
