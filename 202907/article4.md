# 聯邦學習安全聚合

## 前言

聯邦學習（Federated Learning）讓多個客戶端在不共享原始資料的情況下協同訓練模型，在醫療、金融等隱私敏感領域廣泛應用。然而，聯邦學習的分散式架構也引入了新的攻擊面，包括梯度洩漏、模型毒化、以及惡意客戶端攻擊。

## 安全聚合演算法

安全聚合（Secure Aggregation）使用多方計算（MPC）與同態加密技術，確保伺服器無法得知個別客戶端的梯度更新：

```python
import random

def secure_aggregate(client_updates, threshold=3):
    # 使用秘密共享 (Secret Sharing) 保護個別梯度
    n = len(client_updates)
    shares = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                shares[i][j] = random.random()
                shares[j][i] = -shares[i][j]
    masked = [client_updates[i] + sum(shares[i]) for i in range(n)]
    return sum(masked) / n
```

## 毒化攻擊防禦

惡意客戶端可能發送偽造的梯度破壞全局模型。使用 **Krum** 演算法選擇可信的梯度更新：

```python
import numpy as np

def krum_select(gradients, f=1):
    n = len(gradients)
    scores = []
    for i in range(n):
        dists = sorted([np.linalg.norm(gradients[i] - g) for g in gradients])
        scores.append(sum(dists[1:n-f]))
    return gradients[np.argmin(scores)]
```

## 差分隱私整合

在客戶端上傳梯度前加入差分隱私雜訊，提供可證明的隱私保證。更多技術細節請參考 [https://www.google.com/search?q=federated+learning+secure+aggregation+2026](https://www.google.com/search?q=federated+learning+secure+aggregation+2026)。
