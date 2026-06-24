# 聯邦學習與隱私保護：隱私優先的 AI

## 前言

隨著 AI 應用的普及，隱私保護成為越來越重要的話題。聯邦學習允許在不集中資料的情況下訓練模型，保護使用者隱私。

## 聯邦學習原理

```
聯邦學習：
────────────────────────────────

傳統方法：
用戶端 ────▶ 中央伺服器
   │                    │
   └────── 資料移動 ────┘
   
問題：隱私風險、網路頻寬

聯邦學習：
用戶端訓練 ──▶ 只傳送模型更新 ──▶ 中央伺服器聚合
   │                                      │
   └──────── 本地資料從不離開 ────────────┘

優勢：
- 資料隱私保護
- 降低網路傳輸
- 個性化模型
```

## 聯邦學習實現

```python
# 聯邦學習示例

class FederatedClient:
    def __init__(self, model, data, client_id):
        self.model = model
        self.data = data
        self.client_id = client_id
    
    def train_local(self, epochs=5):
        """本地訓練"""
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.01)
        
        for epoch in range(epochs):
            for batch in self.data:
                self.model.train()
                optimizer.zero_grad()
                output = self.model(batch)
                loss = F.cross_entropy(output, batch['labels'])
                loss.backward()
                optimizer.step()
        
        # 返回模型更新，而非資料
        return self.model.state_dict()
    
    def receive_model(self, global_weights):
        """接收聚合後的全局模型"""
        self.model.load_state_dict(global_weights)

class FederatedServer:
    def __init__(self, model, clients):
        self.model = model
        self.clients = clients
    
    def aggregate(self):
        """聚合客戶端更新"""
        updates = []
        for client in self.clients:
            update = client.train_local()
            updates.append(update)
        
        # 聯邦平均 (FedAvg)
        avg_update = {}
        for key in updates[0].keys():
            avg_update[key] = sum(u[key] for u in updates) / len(updates)
        
        self.model.load_state_dict(avg_update)
        return self.model.state_dict()
```

## 差分隱私

```python
# 差分隱私

class DifferentialPrivacy:
    """在梯度上添加噪音以保護隱私"""
    
    def __init__(self, noise_multiplier=1.0):
        self.noise_multiplier = noise_multiplier
    
    def add_noise(self, gradient):
        # 拉普拉斯噪音
        noise = torch.randn_like(gradient) * self.noise_multiplier
        return gradient + noise
    
    def clip_gradient(self, gradient, max_norm):
        # 梯度裁剪
        total_norm = torch.norm(gradient)
        clip_coef = max_norm / (total_norm + 1e-6)
        return gradient * clip_coef
```

## Google 的聯邦學習應用

```
Gboard 聯邦學習：
────────────────────────────────

- 鍵盤預測
- 下一詞建議
- 表情符號預測

特點：
- 保護用戶輸入隱私
- 利用全球數據提升模型
- 即時學習新詞彙
```

## 延伸閱讀

- [聯邦學習](https://www.google.com/search?q=federated+learning+privacy+Google)
- [差分隱私](https://www.google.com/search?q=differential+privacy+machine+learning)
- [聯邦平均演算法](https://www.google.com/search?q=FedAvg+federated+averaging)

---

*本篇文章為「AI 程式人雜誌 2020 年 12 月號」年度回顧系列之一。*