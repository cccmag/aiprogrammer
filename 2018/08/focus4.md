# nn.Module 神經網路模組化

## PyTorch 模型的核心類別

### 什麼是 nn.Module？

`nn.Module` 是 PyTorch 中所有神經網路模型的基類，提供了參數管理、層註冊、GPU 迁移等功能。

```python
import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = SimpleNet()
print(model)
```

### 常用層

```python
# 線性層
nn.Linear(in_features, out_features)

# 卷積層
nn.Conv2d(in_channels, out_channels, kernel_size, stride=1)
nn.Conv1d, nn.Conv3d

# 池化層
nn.MaxPool2d(kernel_size, stride=2)
nn.AvgPool2d(kernel_size)

# Dropout
nn.Dropout(p=0.5)
nn.Dropout2d, nn.Dropout3d

# 正規化層
nn.BatchNorm2d(num_features)
nn.LayerNorm(normalized_shape)
```

### Sequential 容器

```python
# 簡單序列模型
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(256, 128),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(128, 10)
)
```

### ModuleList 和 ModuleDict

```python
# 多層堆疊
class MultiLayerNet(nn.Module):
    def __init__(self, num_layers):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.Linear(128, 128) for _ in range(num_layers)
        ])

    def forward(self, x):
        for layer in self.layers:
            x = torch.relu(layer(x))
        return x

# 條件層
class ConditionalNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoders = nn.ModuleDict({
            'conv': nn.Conv2d(3, 64, 3),
            'linear': nn.Linear(784, 128)
        })

    def forward(self, x, use_conv=False):
        key = 'conv' if use_conv else 'linear'
        return self.encoders[key](x)
```

### 參數管理

```python
# 遍歷所有參數
for name, param in model.named_parameters():
    print(f"{name}: {param.shape}")

# 某層的參數
fc1_weight = model.fc1.weight
fc1_bias = model.fc1.bias

# 凍結參數
for param in model.parameters():
    param.requires_grad = False

# 只訓練特定層
for param in model.fc2.parameters():
    param.requires_grad = True
```

### GPU 支援

```python
# 移動到 GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# 移動輸入
x = x.to(device)

# 檢查設備
print(next(model.parameters()).device)
```

### 模型共享

```python
# 共享權重的範例
class SharedWeightNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(128, 128)
        self.fc1 = self.fc  # 共享權重
        self.fc2 = self.fc

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return x
```

### 小結

`nn.Module` 提供了 PyTorch 模型的核心抽象，熟練掌握其用法是建構複雜模型的基礎。

---

**下一步**：[Optimizer 與學習率排程](focus5.md)