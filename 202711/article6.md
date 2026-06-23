# 差分隱私與聯邦學習安全

## 1. 引言

AI 系統的訓練需要大量資料，但這些資料常包含敏感個人資訊。差分隱私（Differential Privacy, DP）提供嚴格的數學保證來保護個體資料，聯邦學習（Federated Learning, FL）則讓多參與方在不共享原始資料的情況下協同訓練。兩者的結合是當前資料安全的主流方案。

## 2. 差分隱私基礎

### 定義與直覺

一個演算法 M 滿足 ε-差分隱私，當對於任意兩個僅差一筆記錄的資料集 D 和 D'，任何輸出 S 都有：

```
Pr[M(D) ∈ S] ≤ e^ε * Pr[M(D') ∈ S]
```

直覺上，ε 越小，從輸出推斷單一個體資料的難度越大。

### 實作：DP-SGD

差分隱私隨機梯度下降（DP-SGD）是核心演算法：

```python
def dp_sgd_step(model, data, epsilon, delta, batch_size):
    eps = epsilon / len(data)
    sensitivity = 1.0
    model.zero_grad()
    for x, y in data:
        loss = F.cross_entropy(model(x), y)
        loss.backward()
        clip_grad_norm_(model.parameters(), max_norm=sensitivity)
        for param in model.parameters():
            noise = torch.normal(mean=0,
                std=sensitivity * eps / batch_size,
                size=param.grad.shape)
            param.grad += noise
    optimizer.step()
```

### 隱私預算管理

```python
class PrivacyBudget:
    def __init__(self, total_epsilon=1.0):
        self.remaining_eps = total_epsilon
    def query(self, cost: float) -> bool:
        if self.remaining_eps >= cost:
            self.remaining_eps -= cost; return True
        return False
```

## 3. 聯邦學習的安全挑戰

### 梯度洩漏攻擊（Gradient Leakage）

攻擊者可以從共享的梯度重建訓練資料（Deep Leakage from Gradients）：

```python
def deep_leakage_attack(shared_gradients, dummy_data):
    optimizer = torch.optim.LBFGS([dummy_data.requires_grad_()])
    for _ in range(100):
        optimizer.zero_grad()
        loss = mse_loss(shared_gradients, compute_gradients(dummy_data))
        loss.backward()
        optimizer.step()
    return dummy_data  # 重建的訓練資料
```

### 安全聚合

使用安全多方計算（MPC）或同態加密來聚合梯度：

```python
def secure_aggregate(client_updates, threshold=3):
    if len(client_updates) < threshold:
        return None  # 隱私保護不足
    return sum(client_updates) / len(client_updates)
```

## 4. 結語

差分隱私和聯邦學習為 AI 系統的資料安全提供了數學保證和架構保障。然而，每個方案都有取捨——DP 的 ε 越小，模型精確度越低；FL 的通訊開銷會隨參與者數量增加。實際部署需要在隱私、精確度與效率之間取得平衡。

---

## 延伸閱讀

- [差分隱私教科書（Dwork & Roth）](https://www.google.com/search?q=Differential+Privacy+Dwork+Roth+book)
- [DP-SGD 實作指南](https://www.google.com/search?q=DP-SGD+implementation+guide)
- [聯邦學習安全聚合論文](https://www.google.com/search?q=Federated+Learning+secure+aggregation+Bonawitz)
- [OpenMined PySyft 框架](https://www.google.com/search?q=PySyft+OpenMined+differential+privacy)
