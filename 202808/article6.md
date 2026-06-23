# 自動回復策略

## 前言

自動回復（Auto-Recovery）可將平均修復時間（MTTR）從數小時縮短至數分鐘。本文探討四層自動回復策略的設計與實作。

---

## 一、回復策略層級

| 層級 | 動作 | 時間尺度 |
|------|------|---------|
| L1 | 重試 / 降級 | 秒級 |
| L2 | 模型回滾 | 分鐘級 |
| L3 | 自動重新訓練 | 小時級 |
| L4 | 人工介入 | 依需求 |

---

## 二、L1：重試與降級

```python
import time

def predict_with_retry(input_data, max_retries=3):
    for attempt in range(max_retries):
        try:
            return model.predict(input_data)
        except Exception:
            if attempt == max_retries - 1:
                return {"prediction": None, "fallback": True}
            time.sleep(0.5 * (2 ** attempt))
```

降級模式可根據延遲調整服務品質：

```python
class DegradationManager:
    def __init__(self):
        self.mode = "full"

    def check_degradation(self, latency_ms):
        if latency_ms > 2000:
            self.mode = "lite"
        elif latency_ms > 5000:
            self.mode = "cache_only"

    def predict(self, data):
        if self.mode == "cache_only":
            return cache.get(data.hash)
        if self.mode == "lite":
            data = data.drop_columns(["complex_feature"])
        return model.predict(data)
```

---

## 三、L2：自動回滾

```python
class AutoRollback:
    def __init__(self, registry_client):
        self.registry = registry_client

    def monitor_and_rollback(self, value, threshold):
        if value < threshold:
            previous = self.registry.get_previous_version()
            if previous and previous.health_score > 0.9:
                self.registry.promote_model(previous, stage="Production")
                return True
        return False
```

---

## 四、L3：自動重新訓練

```python
class AutoRetrainTrigger:
    def check_retrain_needed(self, drift_score, accuracy):
        if drift_score > 0.25 or accuracy < 0.75:
            self.pipeline.start_run(params={"trigger": "auto_retrain"})
            return True
        return False
```

---

## 五、Canary 部署

```python
class CanaryDeploy:
    def promote(self):
        weight = 0.05
        while weight < 1.0:
            metrics = self._get_canary_metrics()
            if metrics["error_rate"] > 0.02:
                return False
            weight = min(weight + 0.05, 1.0)
        return True
```

---

## 結語

從 L1 重試開始逐步建置，每次 incident 都是改善自動回復邏輯的契機。

---

## 參考資料

- https://www.google.com/search?q=auto+recovery+ML+model+production
- https://www.google.com/search?q=canary+deploy+model+rollback
- https://www.google.com/search?q=MTTR+ML+system+reliability
