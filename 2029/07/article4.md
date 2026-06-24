# 聯邦學習安全聚合

## 概述

聯邦學習（Federated Learning）允許多方協同訓練模型而不共享原始資料。但惡意客戶端可能透過模型更新注入後門或破壞全局模型。

## 安全聚合框架

### 基礎 FedAvg 實現

```python
import numpy as np

def fed_avg(global_model, client_updates):
    new_weights = []
    for layer_idx in range(len(global_model)):
        layer_sum = sum(
            update[layer_idx] for update in client_updates
        )
        new_weights.append(layer_sum / len(client_updates))
    return new_weights
```

## 拜占庭容錯聚合

### Krum 聚合

選擇與多數更新最接近的更新：

```python
def krum_aggregation(updates, f=1):
    n = len(updates)
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distances[i][j] = np.linalg.norm(
                np.concatenate(updates[i]) -
                np.concatenate(updates[j])
            )
    scores = np.sort(distances, axis=1)[:, :n-f-1].sum(axis=1)
    best_idx = np.argmin(scores)
    return updates[best_idx]
```

### Trimmed Mean

去除極值後取平均：

```python
def trimmed_mean(updates, trim_ratio=0.1):
    n = len(updates)
    k = int(n * trim_ratio)
    aggregated = []
    for layer_idx in range(len(updates[0])):
        layer_vals = np.array([u[layer_idx] for u in updates])
        sorted_vals = np.sort(layer_vals, axis=0)
        trimmed = sorted_vals[k:n-k]
        aggregated.append(np.mean(trimmed, axis=0))
    return aggregated
```

## 差分隱私聯邦學習

在客戶端上傳前加入雜訊：

```python
def dp_client_update(model_update, epsilon=1.0, delta=1e-5):
    sensitivity = 1.0
    scale = sensitivity * np.sqrt(2 * np.log(1.25 / delta)) / epsilon
    dp_update = []
    for layer in model_update:
        noise = np.random.laplace(0, scale, layer.shape)
        dp_update.append(layer + noise)
    return dp_update
```

## 安全聚合加密

使用安全多方計算（Secure Aggregation）：

```python
def secure_aggregate(encrypted_updates, server_key):
    """簡化的安全聚合示意"""
    aggregated = encrypted_updates[0]
    for update in encrypted_updates[1:]:
        aggregated = (aggregated + update) % server_key
    return aggregated
```

## 異常客戶端檢測

```python
def detect_malicious_clients(updates, threshold=3.0):
    flat = [np.concatenate(u) for u in updates]
    mean = np.mean(flat, axis=0)
    std = np.std(flat, axis=0) + 1e-8
    z_scores = [(f - mean) / std for f in flat]
    anomalies = [i for i, z in enumerate(z_scores)
                 if np.max(np.abs(z)) > threshold]
    return anomalies
```

參考資料：https://www.google.com/search?q=federated+learning+security+aggregation+2026
