# 警報閾值設計

## 前言

閾值設得過緊導致警報疲勞（Alert Fatigue），設得過鬆則錯過關鍵問題。本文探討 AI 系統中監控指標的閾值設計方法。

---

## 一、閾值類型

| 類型 | 說明 | 適用指標 |
|------|------|---------|
| 固定閾值 | 靜態數值 | 延遲 < 500ms |
| 動態閾值 | 基於歷史統計 | 準確率 ±3σ |
| 比率閾值 | 相對變化百分比 | QPS 突降 > 20% |

---

## 二、固定閾值

```python
class FixedThresholdAlert:
    def __init__(self, thresholds: dict):
        self.thresholds = thresholds

    def evaluate(self, metrics: dict) -> list:
        alerts = []
        for name, value in metrics.items():
            if name in self.thresholds:
                limit = self.thresholds[name]
                if value > limit.get("max", float("inf")):
                    alerts.append(f"{name} 超過上限 {limit['max']}：{value}")
                if value < limit.get("min", float("-inf")):
                    alerts.append(f"{name} 低於下限 {limit['min']}：{value}")
        return alerts

alert_engine = FixedThresholdAlert({
    "p99_latency_ms": {"max": 1000},
    "accuracy": {"min": 0.85},
    "error_rate": {"max": 0.01}
})
```

---

## 三、動態閾值

使用移動平均與標準差自動調整：

```python
import numpy as np
from collections import deque

class DynamicThreshold:
    def __init__(self, window_size=100, sigma=3):
        self.window = deque(maxlen=window_size)
        self.sigma = sigma

    def update(self, value):
        self.window.append(value)
        if len(self.window) < 30:
            return None
        mean = np.mean(self.window)
        std = np.std(self.window)
        if value > mean + self.sigma * std or value < mean - self.sigma * std:
            return {"value": value, "mean": mean, "std": std}
        return None
```

---

## 四、複合規則

單一指標容易誤報，建議設計加權評分：

```python
def composite_alert(metrics: dict) -> str | None:
    score = 0
    if metrics.get("accuracy", 1) < 0.8:
        score += 0.4
    if metrics.get("p99_latency_ms", 0) > 1000:
        score += 0.3
    if metrics.get("error_rate", 0) > 0.05:
        score += 0.3
    return f"健康分數 {score:.2f} 低於警戒線" if score > 0.5 else None
```

---

## 五、閾值最佳化流程

收集 2 週基準資料 → 計算統計分布 → 設定初始閾值 → 觀察誤報率 → 迭代修正。

---

## 結語

從固定閾值開始，逐步導入動態與複合規則，在「不漏報」與「不擾人」之間取得平衡。

---

## 參考資料

- https://www.google.com/search?q=alert+threshold+design+ML+monitoring
- https://www.google.com/search?q=dynamic+threshold+anomaly+detection
- https://www.google.com/search?q=alert+fatigue+reduction+strategies
