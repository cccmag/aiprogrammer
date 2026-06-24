# Batch Normalization 原理與實作

## 1. Internal Covariate Shift

深度神經網路層數多時，每層輸入的分佈會隨著前層參數更新而改變，稱為 Internal Covariate Shift。這導致訓練困難，需要較小的學習率和仔細的初始化。

## 2. Batch Normalization 解決方案

```python
def batch_norm(x, gamma, beta, moving_mean, moving_var, epsilon=1e-5, training=True):
    if training:
        # 使用當前 batch 的統計量
        mean = x.mean(dim=0)
        var = x.var(dim=0)
    else:
        # 使用移動平均的統計量
        mean = moving_mean
        var = moving_var

    # 標準化
    x_norm = (x - mean) / np.sqrt(var + epsilon)

    # 縮放和平移
    return gamma * x_norm + beta
```

## 3. Keras 實現

```python
from keras.layers import BatchNormalization, Dense

model = Sequential([
    Dense(256, use_bias=False),
    BatchNormalization(),
    Activation('relu'),
    Dense(256, use_bias=False),
    BatchNormalization(),
    Activation('relu'),
    Dense(10)
])
```

## 4. PyTorch 實現

```python
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.conv2 = nn.Conv2d(64, 64, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.fc = nn.Linear(64, 10)

    def forward(self, x):
        x = self.bn1(self.conv1(x))
        x = F.relu(x)
        x = F.max_pool2d(self.bn2(self.conv2(x)), 2)
        x = x.view(-1, 64)
        x = self.fc(x)
        return x
```

## 5. 訓練與推論

```python
# 訓練模式：使用 batch 統計量
model.train()
bn.running_mean  # 更新移動平均
bn.running_var

# 推論模式：使用移動平均統計量
model.eval()
output = model(input)
```

## 6. 小結

Batch Normalization 大幅加速深度網路訓練，讓網路對初始化不那么敏感，是現代深度學習的標準元件。

---

**參考資料**
- [Batch Normalization Paper](https://www.google.com/search?q=batch+normalization+paper+2015)
- [BatchNorm in PyTorch](https://www.google.com/search?q=BatchNorm+PyTorch+tutorial)