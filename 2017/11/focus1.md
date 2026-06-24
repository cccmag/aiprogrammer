# 超參數調優基礎

## 前言

深度學習模型的性能很大程度上取決於超參數的選擇。超參數調優是將機器學習應用於實際問題的關鍵步驟。本篇文章將介紹主要的超參數調優方法。

## 主要超參數

### 網路架構超參數

- **層數**：網路的深度
- **每層神經元數**：網路的寬度
- **激活函數**：ReLU, Sigmoid, Tanh 等

### 訓練超參數

- **學習率 (Learning Rate)**：最重要的超參數
- **批次大小 (Batch Size)**：影響記憶體和泛化
- **訓練輪數 (Epochs)**：何時停止訓練

### 正則化超參數

- **Dropout Rate**：防止過擬合
- **Weight Decay**：L2 正則化強度
- **Gradient Clipping**：防止梯度爆炸

## 調優方法

### 1. 網格搜索 (Grid Search)

最直觀的方法，遍歷所有超參數組合：

```python
import itertools

param_grid = {
    'learning_rate': [0.001, 0.01, 0.1],
    'batch_size': [32, 64, 128],
    'dropout_rate': [0.2, 0.4, 0.6]
}

best_score = 0
best_params = None

for lr, bs, dr in itertools.product(
    param_grid['learning_rate'],
    param_grid['batch_size'],
    param_grid['dropout_rate']
):
    model = create_model(dropout_rate=dr)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    train_loader = DataLoader(dataset, batch_size=bs)

    score = train_and_evaluate(model, optimizer, train_loader)
    if score > best_score:
        best_score = score
        best_params = {'lr': lr, 'bs': bs, 'dr': dr}

print(f"Best: {best_params}, Score: {best_score}")
```

### 2. 隨機搜索 (Random Search)

比網格搜索更高效，尤其當只有部分超參數重要時：

```python
import random

param_dist = {
    'learning_rate': uniform(1e-4, 1e-1),
    'batch_size': choice([16, 32, 64, 128, 256]),
    'dropout_rate': uniform(0.1, 0.5),
    'hidden_dim': choice([64, 128, 256, 512])
}

best_score = 0
best_params = None

for _ in range(100):
    params = {k: v.rvs() for k, v in param_dist.items()}

    model = create_model(hidden_dim=int(params['hidden_dim']),
                        dropout_rate=params['dropout_rate'])
    optimizer = torch.optim.Adam(model.parameters(),
                                 lr=params['learning_rate'])

    score = train_and_evaluate(model, optimizer, batch_size=int(params['batch_size']))
    if score > best_score:
        best_score = score
        best_params = params
```

### 3. 貝氏優化 (Bayesian Optimization)

利用之前結果指導搜索，更高效：

```python
from sklearn.gaussian_process import GaussianProcessRegressor

def objective(params):
    lr, bs, dr = params
    model = create_model(dropout_rate=dr)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    score = train_and_evaluate(model, optimizer, batch_size=int(bs))
    return -score  # 最大化變為最小化

# 搜尋空間
space = [(1e-4, 1e-1), (16, 256), (0.1, 0.5)]

# 初始化
gp = GaussianProcessRegressor()

# 迭代優化
for _ in range(50):
    next_params = suggest_next(gp, space)
    result = objective(next_params)
    gp.update(next_params, result)

best_params = gp.get_best_params()
```

## 實驗設計原則

### 1. 隔離重要超參數

先確定重要超參數，優先調優：

```
┌─────────────────────────────────────────────────────────┐
│              超參數重要性排序                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Learning Rate        ★★★★★                       │
│  2. Batch Size           ★★★★                        │
│  3. Network Architecture ★★★★                        │
│  4. Learning Rate Schedule ★★★                        │
│  5. Dropout/Regularization ★★★                       │
│  6. Momentum             ★★                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2. 分階段調優

```python
# 階段 1: 粗搜索
lr_candidates = [0.1, 0.01, 0.001, 0.0001]
# 快速找到大致的範圍

# 階段 2: 細搜索
lr_candidates = [0.05, 0.075, 0.1, 0.15]
# 在找到的範圍內更精細地搜索
```

### 3. 記錄和重現

```python
import json
from datetime import datetime

class ExperimentTracker:
    def __init__(self):
        self.results = []

    def log(self, params, score):
        self.results.append({
            'timestamp': datetime.now().isoformat(),
            'params': params,
            'score': score
        })

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)

    def load(self, filename):
        with open(filename, 'r') as f:
            self.results = json.load(f)
```

## Learning Rate Finder

Leslie Smith 提出的方法可以自動找到合適的學習率：

```python
def find_learning_rate(model, train_loader, optimizer, start_lr=1e-7, end_lr=10):
    """Learning Rate Finder 實現"""

    model.train()
    optimizer.param_groups[0]['lr'] = start_lr

    lrs = []
    losses = []

    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = F.cross_entropy(output, target)
        loss.backward()
        optimizer.step()

        lrs.append(optimizer.param_groups[0]['lr'])
        losses.append(loss.item())

        # 指數增加學習率
        optimizer.param_groups[0]['lr'] *= 1.0001

        if optimizer.param_groups[0]['lr'] > end_lr:
            break

    return lrs, losses
```

## 總結

超參數調優是深度學習成功的關鍵。貝氏優化通常比網格搜索和隨機搜索更高效，但實現也更複雜。Learning Rate Finder 可以幫助快速找到合適的學習率範圍。

---

**延伸閱讀**

- [Random Search for Hyperparameter Optimization](https://www.google.com/search?q=random+search+hyperparameter+bergstra)
- [Bayesian Optimization](https://www.google.com/search?q=bayesian+optimization+hyperparameter)
- [Learning Rate Finder](https://www.google.com/search?q=learning+rate+finder+smith)