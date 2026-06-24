# 模型萃取攻擊防護

## 概述

模型萃取攻擊（Model Extraction Attack）是指攻擊者透過反覆查詢目標模型，竊取模型參數、架構或決策邊界。這對商業機密和隱私構成嚴重威脅。

## 攻擊原理

攻擊者利用模型 API 的回應來訓練一個代理模型：

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

def extract_model(target_api, num_queries=1000):
    X_proxy = np.random.randn(num_queries, 784)
    y_proxy = []
    for x in X_proxy:
        pred = target_api.predict(x.reshape(1, -1))
        y_proxy.append(np.argmax(pred))
    proxy_model = LogisticRegression(max_iter=1000)
    proxy_model.fit(X_proxy, y_proxy)
    return proxy_model
```

進階攻擊使用 Jacobian 矩陣來加速收斂：

```python
def jacobian_extraction(target_api, proxy_model, epsilon=0.1):
    X_synthetic = np.random.randn(100, 784)
    for _ in range(100):
        grads = compute_jacobian(proxy_model, X_synthetic)
        X_new = X_synthetic + epsilon * np.sign(grads)
        y_new = [np.argmax(target_api.predict(x.reshape(1, -1)))
                 for x in X_new]
        proxy_model.partial_fit(X_new, y_new)
    return proxy_model
```

## 防禦策略

### 預測擾動（Prediction Perturbation）

在 API 回傳前加入少量雜訊：

```python
def defense_perturbation(predictions, sigma=0.01):
    noise = np.random.laplace(0, sigma, predictions.shape)
    return predictions + noise
```

### 查詢頻率限制

```python
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_queries=100, window_sec=3600):
        self.limit = max_queries
        self.window = timedelta(seconds=window_sec)
        self.records = defaultdict(list)

    def allow_query(self, user_id):
        now = datetime.now()
        self.records[user_id] = [
            t for t in self.records[user_id]
            if now - t < self.window
        ]
        if len(self.records[user_id]) >= self.limit:
            return False
        self.records[user_id].append(now)
        return True
```

### 模型蒸餾混淆（Distillation Obfuscation）

使用溫度縮放的 soft label 混淆攻擊者：

```python
def obfuscated_predict(model, x, temperature=5.0):
    logits = model(x)
    return F.softmax(logits / temperature, dim=-1).detach()
```

## 監控與偵測

分析查詢模式以識別異常行為：

```python
def detect_extraction(query_log):
    unique_inputs = len(set(q['input_hash'] for q in query_log))
    total_queries = len(query_log)
    if unique_inputs / total_queries > 0.9:
        return "high_risk"
    return "normal"
```

參考資料：https://www.google.com/search?q=model+extraction+attack+defense+2026
