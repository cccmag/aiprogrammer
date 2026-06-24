# 深度學習的函式式框架：PyTorch

## PyTorch 的設計理念

PyTorch 是 Facebook 於 2016 年發布的深度學習框架，其核心設計深受函式式程式設計影響：

- **動態計算圖（Define-by-Run）**：計算圖在執行時動態構建
- **張量是不可變的**：資料以張量形式存在於函式變換中
- **模組化設計**：神經網路由可組合的模組構建

## 動態計算圖

PyTorch 的動態計算圖是其與 TensorFlow 等框架的主要區別：

```python
import torch

# 動態建立計算圖
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.tensor([4.0, 5.0, 6.0])

# 每次執行都可能不同的計算圖
z = x + y
print(z)  # tensor([5., 7., 9.])

# 支援 Python 控制流
if x.sum() > 5:
    result = x * 2
else:
    result = x / 2
```

## 自動微分

PyTorch 的 autograd 系統自動計算梯度，體現了函式式微分的精神：

```python
# 需要梯度的張量
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)

# 構建計算圖
y = x ** 2
z = y.sum()  # z = 1 + 4 + 9 = 14

# 自動微分
z.backward()

# 梯度 dz/dx = 2x
print(x.grad)  # tensor([2., 4., 6.])
```

## 模組化神經網路

`torch.nn.Module` 提供了宣告式定義網路的方式：

```python
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 784)  # 展平
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 使用
net = Net()
output = net(input_tensor)
```

## 資料處理管線

使用 `torch.utils.data` 的函式式資料處理：

```python
from torch.utils.data import DataLoader, Dataset

class MyDataset(Dataset):
    def __init__(self, data, transform=None):
        self.data = data
        self.transform = transform

    def __getitem__(self, idx):
        x, y = self.data[idx]
        if self.transform:
            x = self.transform(x)
        return x, y

    def __len__(self):
        return len(self.data)

# 資料增強（函式式轉換）
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
```

## 訓練循環

PyTorch 的訓練循環體現了函式式風格：

```python
# 純函式式的訓練步驟
def train_step(model, optimizer, inputs, targets):
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    return loss.item()

# 執行多個 epoch
for epoch in range(num_epochs):
    for batch in dataloader:
        loss = train_step(model, optimizer, *batch)
```

## 與 NumPy 的無縫轉換

PyTorch 張量與 NumPy 陣列可以互相轉換：

```python
import numpy as np

# NumPy to Tensor
np_array = np.array([1, 2, 3])
tensor = torch.from_numpy(np_array)

# Tensor to NumPy
back_to_np = tensor.numpy()
```

## 發展趨勢

2016 年的 PyTorch 還處於早期階段，但已經展現出強大的潛力。其動態圖設計和 Python 優先的理念深刻影響了後來的深度學習框架。

延伸閱讀：
- [Google 搜尋：PyTorch tutorial](https://www.google.com/search?q=PyTorch+tutorial)
- [Google 搜尋：dynamic computation graph deep learning](https://www.google.com/search?q=dynamic+computation+graph+deep+learning)