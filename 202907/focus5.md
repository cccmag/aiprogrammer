# 聯邦學習安全

## 分散式訓練的隱私難題（2021-2029）

### 聯邦學習的承諾與現實

聯邦學習（Federated Learning, FL）的承諾很美好：資料不出本地端，只交換模型更新，從而保護使用者隱私。但 2021 年以來的安全研究逐步揭示了這個承諾的裂縫。

```python
import torch
import numpy as np

class FederatedClient:
    """聯邦學習中的客戶端（可能被攻擊者控制）"""

    def __init__(self, data, model):
        self.data = data
        self.model = model

    def train_local_epoch(self):
        """在本地資料上訓練一個 epoch"""
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.01)
        for x, y in self.data:
            optimizer.zero_grad()
            pred = self.model(x)
            loss = torch.nn.functional.cross_entropy(pred, y)
            loss.backward()
            optimizer.step()
        return self.get_model_update()

    def get_model_update(self):
        """回傳模型更新（聯邦學習的核心交換內容）"""
        return {name: param.data.clone()
                for name, param in self.model.named_parameters()}
```

### 2021-2023：梯度洩漏攻擊

最令人震驚的發現是：**從梯度可以重建原始資料**。Zhu 等人 2019 年的論文展示了可以從共享的梯度完美重建訓練資料：

```python
def deep_leakage_from_gradients(real_gradients, model, input_shape):
    """從梯度重建訓練資料（Deep Leakage from Gradients）"""
    # 隨機初始化虛擬資料和標籤
    dummy_data = torch.randn(input_shape, requires_grad=True)
    dummy_label = torch.randn(1, 10, requires_grad=True)

    optimizer = torch.optim.LBFGS([dummy_data, dummy_label])

    def closure():
        optimizer.zero_grad()
        dummy_pred = model(dummy_data)
        dummy_loss = torch.nn.functional.cross_entropy(dummy_pred, dummy_label)
        dummy_gradients = torch.autograd.grad(
            dummy_loss, model.parameters(), create_graph=True
        )

        # 最小化虛擬梯度與真實梯度的距離
        grad_diff = sum(
            torch.norm(dg - rg) ** 2
            for dg, rg in zip(dummy_gradients, real_gradients)
        )
        grad_diff.backward()
        return grad_diff

    for _ in range(100):
        optimizer.step(closure)

    return dummy_data.detach(), dummy_label.detach()
```

### 2023-2025：惡意伺服器攻擊

如果聯邦學習的中央伺服器被攻陷（或本身就是惡意的），它可以操控整個訓練過程：

```python
class MaliciousServer:
    """惡意的聯邦學習伺服器"""

    def __init__(self, global_model):
        self.global_model = global_model
        self.client_updates = []

    def receive_update(self, client_update):
        """收集客戶端更新"""
        self.client_updates.append(client_update)

    def detect_poisoned_update(self, client_update, threshold=5.0):
        """使用統計方法檢測中毒的更新"""
        # 計算所有更新的平均值
        avg_update = {
            k: torch.mean(torch.stack([u[k] for u in self.client_updates]), dim=0)
            for k in self.client_updates[0]
        }

        # 計算每個更新與平均值的距離
        distances = []
        for update in self.client_updates:
            dist = sum(
                torch.norm(update[k] - avg_update[k]) ** 2
                for k in update
            ).item()
            distances.append(dist)

        # Z-score 異常檢測
        mean_dist = np.mean(distances)
        std_dist = np.std(distances) + 1e-8
        z_scores = [(d - mean_dist) / std_dist for d in distances]
        return [z > threshold for z in z_scores]
```

### 2025-2027：模型中毒攻擊

模型中毒（Model Poisoning）是資料中毒在聯邦學習中的變體。攻擊者控制的客戶端提交惡意的模型更新，在全球模型中植入後門：

```python
def model_poisoning_attack(global_model, malicious_update, scaling_factor=100):
    """模型中毒攻擊 — 放大惡意更新以繞過聚合"""
    # 正常聯邦學習中，伺服器會平均所有更新
    # 攻擊者放大惡意更新的幅度，使其主導平均值
    poisoned_update = {
        k: v * scaling_factor for k, v in malicious_update.items()
    }
    return poisoned_update

# 後門觸發函數
def evaluate_backdoor(model, backdoor_trigger, target_label, test_data):
    """評估後門攻擊的成功率"""
    correct = 0
    total = 0
    model.eval()

    for x, y in test_data:
        # 在測試樣本上添加後門觸發器
        x_triggered = add_trigger(x, backdoor_trigger)
        with torch.no_grad():
            pred = model(x_triggered)
            predicted = pred.argmax(dim=1)

        # 攻擊目標：所有帶觸發器的樣本都被分類為 target_label
        correct += (predicted == target_label).sum().item()
        total += y.size(0)

    return correct / total
```

### 2027-2029：穩健聚合與防禦

對抗這些攻擊需要設計穩健的聚合演算法：

```python
def robust_aggregation(client_updates, strategy="trimmed_mean", trim_ratio=0.1):
    """穩健的聯邦學習聚合器"""
    n_clients = len(client_updates)
    aggregated = {}

    for key in client_updates[0]:
        # 收集所有客戶端在該參數上的值
        values = torch.stack([u[key] for u in client_updates])

        if strategy == "average":
            aggregated[key] = values.mean(dim=0)

        elif strategy == "trimmed_mean":
            # 移除最高和最低的 trim_ratio%
            k = int(n_clients * trim_ratio)
            sorted_vals, _ = torch.sort(values, dim=0)
            aggregated[key] = sorted_vals[k:n_clients-k].mean(dim=0)

        elif strategy == "median":
            aggregated[key] = values.median(dim=0).values

        elif strategy == "krum":
            # Krum: 選擇與多數更新最接近的更新
            distances = torch.zeros(n_clients)
            for i in range(n_clients):
                for j in range(n_clients):
                    if i != j:
                        distances[i] += torch.norm(values[i] - values[j])
            best_idx = distances.argmin().item()
            aggregated[key] = values[best_idx]

    return aggregated
```

### 聯邦學習的隱私-安全權衡

聯邦學習面臨一個根本性矛盾：合作的層級越細，攻擊面越大。更新頻率越高、參數共享越多，梯度洩漏的風險越大；差分隱私加入噪音越多，模型效用下降。

到 2029 年，實務共識是：**聯邦學習不是隱私的萬靈丹**，它需要與差分隱私、安全多方計算（SMPC）、可信執行環境（TEE）等技術組合使用，才能達到真正的安全保障。

---

**下一步**：[紅隊自動化](focus6.md)

## 延伸閱讀

- [Deep Leakage from Gradients](https://www.google.com/search?q=deep+leakage+from+gradients+federated+learning)
- [Model Poisoning in Federated Learning](https://www.google.com/search?q=model+poisoning+federated+learning)
- [Robust Aggregation for Federated Learning](https://www.google.com/search?q=robust+aggregation+federated+learning+attacks)
