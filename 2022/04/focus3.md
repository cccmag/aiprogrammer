# nn.Module 與模型建置

## 模組化設計哲學

PyTorch 的 `nn.Module` 是所有神經網路模型的基底類別，它提供了一個優雅的模組化機制來組織網路層。透過繼承 `nn.Module`，我們可以將網路定義為 nested 的模組結構。

```python
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)
```

## 核心特性

### 參數管理
`nn.Module` 會自動追蹤所有子模組的參數，透過 `parameters()` 或 `named_parameters()` 可以取得模型中所有可訓練的張量。

### train/eval 模式
透過 `.train()` 與 `.eval()` 切換，影響 BatchNorm、Dropout 等層的行為。

### 裝置移動
一行程式碼即可將整個模型搬到 GPU 或 CPU：`model.to(device)`

## Sequential vs ModuleList vs ModuleDict

- **nn.Sequential**：依序執行的層序列，適合簡單的 feed-forward 網路
- **nn.ModuleList**：類似 Python list，但註冊為子模組，適合需要迭代的層集合
- **nn.ModuleDict**：類似 Python dict，依名稱存取子模組

## 自訂 forward 方法

`forward` 方法定義了資料在前向傳播時的流向，這裡可以使用任何 Python 控制流：

```python
def forward(self, x):
    for layer in self.layers:
        x = layer(x)
        if x.abs().mean() > 10:
            x = torch.clamp(x, -10, 10)
    return x
```

## 權重初始化

PyTorch 提供多種初始化方法：
- `nn.init.kaiming_uniform_`（He 初始化）
- `nn.init.xavier_normal_`（Xavier/Glorot 初始化）
- `nn.init.orthogonal_`

## 參考資料

- nn.Module 文件：https://pytorch.org/docs/stable/generated/torch.nn.Module.html
- 自訂層教學：https://pytorch.org/docs/stable/notes/extending.html
- 權重初始化：https://pytorch.org/docs/stable/nn.init.html
