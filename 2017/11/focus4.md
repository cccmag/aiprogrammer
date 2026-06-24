# Batch Normalization

## 前言

Batch Normalization (BatchNorm) 是深度學習中最重要的技術之一，由 Sergey Ioffe 和 Christian Szegedy 於 2015 年提出。這個技術幾乎成為訓練深度網路的必備组件。

## 內部協變量轉移問題 (Internal Covariate Shift)

### 問題描述

訓練深度神經網路時，每層的輸入分佈會隨著前面層的參數變化而變化，這稱為內部協變量轉移：

```
┌─────────────────────────────────────────────────────────┐
│          內部協變量轉移示意                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Layer 1 → Layer 2 → Layer 3 → Layer 4                 │
│     ↑         ↑         ↑                              │
│     │         │         │                              │
│   更新      更新      更新                              │
│   權重      權重      權重                              │
│     │         │         │                              │
│     ▼         ▼         ▼                              │
│   輸入      輸入      輸入                              │
│   分佈      分佈      分佈                              │
│   改變      改變      改變                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 解決方案

BatchNorm 透過對每層的輸入進行標準化來解決這個問題：

```python
# BatchNorm 公式
y = γ * (x - μ_B) / sqrt(σ²_B + ε) + β

# 其中：
# μ_B: mini-batch 均值
# σ²_B: mini-batch 方差
# γ, β: 可學習的縮放和平移參數
```

## BatchNorm 的實現

```python
class BatchNorm1d(nn.Module):
    def __init__(self, num_features, eps=1e-5, momentum=0.1):
        super().__init__()
        self.num_features = num_features
        self.eps = eps
        self.momentum = momentum

        # 可學習參數
        self.gamma = nn.Parameter(torch.ones(num_features))
        self.beta = nn.Parameter(torch.zeros(num_features))

        # 移動平均（推論時使用）
        self.running_mean = torch.zeros(num_features)
        self.running_var = torch.ones(num_features)

    def forward(self, x):
        if self.training:
            # 訓練時：使用 mini-batch 統計
            mean = x.mean(dim=0)
            var = x.var(dim=0, unbiased=False)

            # 更新移動平均
            self.running_mean = self.momentum * self.running_mean + \
                               (1 - self.momentum) * mean
            self.running_var = self.momentum * self.running_var + \
                              (1 - self.momentum) * var
        else:
            # 推論時：使用移動平均
            mean = self.running_mean
            var = self.running_var

        # 標準化
        x_norm = (x - mean) / torch.sqrt(var + self.eps)

        # 縮放和平移
        return self.gamma * x_norm + self.beta
```

## PyTorch 中的 BatchNorm

```python
# 1D BatchNorm (用於全連接層)
bn1d = nn.BatchNorm1d(num_features=128)

# 2D BatchNorm (用於卷積層)
bn2d = nn.BatchNorm2d(num_features=64)

# 3D BatchNorm (用於 3D 卷積)
bn3d = nn.BatchNorm3d(num_features=128)
```

## 使用範例

```python
class CNNWithBatchNorm(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)

        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(128)

        self.fc = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)  # BatchNorm 在 activation 之前
        x = torch.relu(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = torch.relu(x)

        x = torch.max_pool2d(x, 2)
        x = x.mean(dim=[2, 3])  # Global average pooling
        x = self.fc(x)
        return x
```

## BatchNorm 的優點

```
┌─────────────────────────────────────────────────────────┐
│              BatchNorm 的優勢                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 加速收斂                                             │
│     - 可以使用更高的學習率                               │
│     - 梯度更穩定                                         │
│                                                         │
│  2. 減少對初始化的依賴                                   │
│     - 權重初始化不再那麼關鍵                             │
│                                                         │
│  3. 正則化效果                                           │
│     - Mini-batch 統計有噪聲                             │
│     - 輕微的正則化                                       │
│                                                         │
│  4. 允許更深層的網路                                    │
│     - 緩解梯度消失問題                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## BatchNorm 的變體

### Layer Normalization

每個樣本獨立標準化，適用於 RNN：

```python
# LayerNorm: 在特徵維度上標準化
ln = nn.LayerNorm(normalized_shape=[128, 16, 16])

# 適用於 RNN 和 Transformers
```

### Instance Normalization

常用於風格遷移：

```python
# InstanceNorm: 在空間維度上標準化
in_ = nn.InstanceNorm2d(num_features=64)

# 常用於 neural style transfer
```

### Group Normalization

結合 BatchNorm 和 LayerNorm 的優點：

```python
# GroupNorm: 將通道分組後標準化
gn = nn.GroupNorm(num_groups=32, num_channels=64)
# 32 個通道分為 4 組，每組 8 個通道
```

## 比較

| 方法 | 標準化維度 | 訓練依賴 | 適用場景 |
|------|-----------|----------|---------|
| BatchNorm | Batch | 是 | CNN，大批次 |
| LayerNorm | Feature | 否 | RNN, Transformer |
| InstanceNorm | Spatial | 否 | 風格遷移 |
| GroupNorm | Group | 否 | 小批次 |

## 訓練 vs 推論

```python
model = ModelWithBatchNorm()

# 訓練模式
model.train()
for batch in dataloader:
    output = model(batch)  # BatchNorm 使用 mini-batch 統計

# 推論模式
model.eval()
with torch.no_grad():
    output = model(batch)  # BatchNorm 使用移動平均
```

## 注意事項

### 1. Batch Size 的影響

```python
# Batch Size 太小時，BatchNorm 效果變差
# 因為統計估計不准確

# 解決方案：
# - 使用 GroupNorm
# - 使用更大的 batch size
# - 累積多個 mini-batch 的統計
```

### 2. 與 Dropout 的順序

```python
# 建議的順序
nn.Conv2d(...)
nn.BatchNorm2d(...)
nn.ReLU()        # 通常在 BN 之後
nn.Dropout(0.5)  # Dropout 放在最後
```

### 3. 移動平均的更新

```python
# PyTorch 自動處理移動平均
# 但需要注意 training/eval 模式的切換
```

## 總結

BatchNorm 是深度學習中不可或缺的技術。它簡化了網路的訓練，允許使用更高的學習率，減少對初始化的依賴。對於不同的應用場景，可以選擇合適的正規化方法。

---

**延伸閱讀**

- [Batch Normalization Paper](https://www.google.com/search?q=batch+normalization+ioffe+2015)
- [BatchRenorm Paper](https://www.google.com/search?q=batch+renormalization)
- [Group Normalization Paper](https://www.google.com/search?q=group+normalization+wu+2018)