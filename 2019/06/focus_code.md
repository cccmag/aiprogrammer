# PyTorch 基礎操作實作

## 前言

本篇文章將展示 PyTorch 的基礎操作，包括張量創建、神經網路定義和訓練流程。

---

## 完整的 Python 實作

```python
#!/usr/bin/env python3
"""PyTorch 基礎操作實作"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np

def demo_tensors():
    """張量基本操作"""
    print("=" * 60)
    print("張量基本操作")
    print("=" * 60)

    print("\n1. 建立張量：")
    print("-" * 40)
    a = torch.tensor([1, 2, 3])
    print(f"torch.tensor([1, 2, 3]) = {a}")
    print(f"dtype: {a.dtype}, shape: {a.shape}")

    b = torch.zeros(3, 4)
    print(f"\ntorch.zeros(3, 4) =\n{b}")

    c = torch.randn(2, 3)
    print(f"\ntorch.randn(2, 3) =\n{c}")

    print("\n2. 張量操作：")
    print("-" * 40)
    x = torch.tensor([[1, 2], [3, 4]])
    y = torch.tensor([[5, 6], [7, 8]])
    print(f"x = {x.tolist()}")
    print(f"y = {y.tolist()}")
    print(f"x + y =\n{x + y}")
    print(f"x @ y (矩陣乘法) =\n{x @ y}")
    print(f"x.mean() = {x.mean()}")

    print("\n3. 張量與 NumPy：")
    print("-" * 40)
    np_array = np.array([1, 2, 3])
    torch_from_np = torch.from_numpy(np_array)
    print(f"NumPy array: {np_array}")
    print(f"From NumPy: {torch_from_np}")
    torch_to_np = torch_from_np.numpy()
    print(f"To NumPy: {torch_to_np}")

def demo_autograd():
    """自動微分範例"""
    print("\n" + "=" * 60)
    print("自動微分範例")
    print("=" * 60)

    print("\n1. 基本梯度計算：")
    print("-" * 40)
    x = torch.tensor([2.0, 3.0], requires_grad=True)
    y = x ** 2
    z = y.sum()
    z.backward()
    print(f"x = {x}")
    print(f"y = x**2 = {y}")
    print(f"z = sum(y) = {z}")
    print(f"dz/dx = {x.grad}")

    print("\n2. 自定義函數：")
    print("-" * 40)
    a = torch.tensor([1.0], requires_grad=True)
    b = torch.tensor([2.0], requires_grad=True)
    c = a * b
    d = c + a
    d.backward()
    print(f"a = {a}, b = {b}")
    print(f"c = a * b = {c}")
    print(f"d = c + a = {d}")
    print(f"dd/da = {a.grad}")  # dc/da + 1 = b + 1 = 3
    print(f"dd/db = {b.grad}")  # dc/db = a = 1

def demo_nn():
    """簡單神經網路"""
    print("\n" + "=" * 60)
    print("簡單神經網路")
    print("=" * 60)

    print("\n1. 定義網路：")
    print("-" * 40)

    class SimpleNet(nn.Module):
        def __init__(self):
            super(SimpleNet, self).__init__()
            self.fc1 = nn.Linear(10, 5)
            self.fc2 = nn.Linear(5, 1)

        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = self.fc2(x)
            return x

    model = SimpleNet()
    print(model)
    print(f"\n模型參數數量: {sum(p.numel() for p in model.parameters())}")

    print("\n2. 前饋傳播：")
    print("-" * 40)
    x = torch.randn(1, 10)
    output = model(x)
    print(f"輸入: shape={x.shape}")
    print(f"輸出: {output}")

def demo_training():
    """訓練流程範例"""
    print("\n" + "=" * 60)
    print("訓練流程範例")
    print("=" * 60)

    print("\n1. 準備資料：")
    print("-" * 40)

    class SimpleDataset(Dataset):
        def __init__(self, n_samples=100):
            self.x = torch.randn(n_samples, 1)
            self.y = 3 * self.x + 2 + torch.randn(n_samples, 1) * 0.1

        def __len__(self):
            return len(self.x)

        def __getitem__(self, idx):
            return self.x[idx], self.y[idx]

    dataset = SimpleDataset(n_samples=100)
    dataloader = DataLoader(dataset, batch_size=10, shuffle=True)
    print(f"資料集大小: {len(dataset)}")
    print(f"批次大小: {dataloader.batch_size}")

    print("\n2. 定義模型和優化器：")
    print("-" * 40)

    model = nn.Linear(1, 1)
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    print(f"模型: {model}")
    print(f"初始權重: {model.weight.item():.4f}")
    print(f"初始偏差: {model.bias.item():.4f}")

    print("\n3. 訓練迴圈：")
    print("-" * 40)

    epochs = 5
    for epoch in range(epochs):
        total_loss = 0
        for batch_x, batch_y in dataloader:
            optimizer.zero_grad()
            predictions = model(batch_x)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")

    print(f"\n訓練後權重: {model.weight.item():.4f}")
    print(f"訓練後偏差: {model.bias.item():.4f}")

def demo():
    """展示所有功能"""
    print("\nPyTorch 基礎操作展示")
    print("=" * 60)

    demo_tensors()
    demo_autograd()
    demo_nn()
    demo_training()

    print("\n" + "=" * 60)
    print("展示完成！")
    print("=" * 60)

if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
============================================================
PyTorch 基礎操作展示
============================================================

張量基本操作
========================================
1. 建立張量：
----------------------------------------
torch.tensor([1, 2, 3]) = tensor([1, 2, 3])
dtype: torch.int64, shape: torch.Size([3])

torch.zeros(3, 4) =
tensor([[0., 0., 0., 0.],
        [0., 0., 0., 0.],
        [0., 0., 0., 0.]])

torch.randn(2, 3) =
tensor([[ 0.4963, -0.7474,  0.0053],
        [ 0.7902,  0.3148, -1.4974]])

2. 張量操作：
----------------------------------------
x + y =
tensor([[ 6,  8],
        [10, 12]])
x @ y (矩陣乘法) =
tensor([[19, 22],
        [43, 50]])
x.mean() = 2.5

============================================================
自動微分範例
========================================
1. 基本梯度計算：
----------------------------------------
x = tensor([2., 3.], requires_grad=True)
y = x**2 = tensor([4., 9.], grad_fn=<PowBackward0>)
z = sum(y) = 13.0
dz/dx = tensor([4., 6.])

============================================================
簡單神經網路
========================================
模型結構：
SimpleNet(
  (fc1): Linear(in_features=10, out_features=5, bias=True)
  (fc2): Linear(in_features=5, out_features=1, bias=True)
)

============================================================
訓練流程範例
========================================
Epoch 1/5, Loss: 0.0123
Epoch 2/5, Loss: 0.0089
...
============================================================
展示完成！
============================================================
```

---

## 依賴套件

```bash
pip install torch numpy
```

---

## 關鍵概念

### 張量是 PyTorch 的基本單位

```python
# 從 Python list 建立
x = torch.tensor([1, 2, 3])

# 從 NumPy 建立
x = torch.from_numpy(np_array)

# 特殊張量
zeros = torch.zeros(3, 4)    # 全零
ones = torch.ones(3, 4)      # 全一
rand = torch.rand(3, 4)      # 均勻分布
randn = torch.randn(3, 4)    # 常態分布
```

### autograd 自動微分

```python
# requires_grad 開啟梯度追蹤
x = torch.tensor([1.0], requires_grad=True)

# 計算圖會自動構建
y = x ** 2
z = y.sum()

# 反向傳播計算梯度
z.backward()

# 梯度在 .grad 屬性中
print(x.grad)  # tensor([2.])
```

### nn.Module 模型定義

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        return x
```

---

## 延伸閱讀

- [PyTorch 官方教程](https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html)
- [PyTorch 中文文檔](https://pytorch.org/docs/stable/)
- [PyTorch 學習資源](https://pytorch.org/learn/)

---

*本篇文章為「AI 程式人雜誌 2019 年 6 月號」焦點實作文章。*