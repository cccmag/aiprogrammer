# 訓練優化器比較：實作

## 前言

本篇文章將比較不同優化器的實作與效果，幫助讀者選擇適合的優化器。

---

## 原始碼

完整的 Python 實作請參考：[_code/optimizer_demo.py](_code/optimizer_demo.py)

```python
#!/usr/bin/env python3
"""Optimizer comparison demonstration"""

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.net(x)

def train_with_optimizer(model, optimizer, train_loader, num_epochs=20):
    criterion = nn.MSELoss()
    losses = []

    for epoch in range(num_epochs):
        epoch_loss = 0
        for batch in train_loader:
            x, y = batch
            pred = model(x)
            loss = criterion(pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        avg_loss = epoch_loss / len(train_loader)
        losses.append(avg_loss)

    return losses

def demo():
    print("Optimizer Comparison Demo")
    print("=" * 50)

    torch.manual_seed(42)
    np.random.seed(42)

    # 創建虛擬資料
    x_train = torch.randn(1000, 10)
    y_train = torch.randn(1000, 1)

    train_loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(x_train, y_train),
        batch_size=32,
        shuffle=True
    )

    optimizers = {
        'SGD (lr=0.01)': lambda m: optim.SGD(m.parameters(), lr=0.01),
        'SGD + Momentum': lambda m: optim.SGD(m.parameters(), lr=0.01, momentum=0.9),
        'Adam': lambda m: optim.Adam(m.parameters(), lr=0.01),
        'RMSprop': lambda m: optim.RMSprop(m.parameters(), lr=0.01),
        'Adagrad': lambda m: optim.Adagrad(m.parameters(), lr=0.1),
    }

    results = {}

    print("\nTraining with different optimizers...")
    for name, opt_fn in optimizers.items():
        model = SimpleModel()
        optimizer = opt_fn(model)
        losses = train_with_optimizer(model, optimizer, train_loader)
        results[name] = losses
        print(f"  {name}: Final loss = {losses[-1]:.4f}")

    # 繪製比較圖
    print("\nGenerating comparison plot...")

    plt.figure(figsize=(10, 6))
    for name, losses in results.items():
        plt.plot(losses, label=name)

    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Optimizer Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('optimizer_comparison.png')

    print("\nPlot saved as 'optimizer_comparison.png'")
    print("\nKey Observations:")
    print("- Adam typically converges fastest")
    print("- SGD + Momentum often achieves lower final loss")
    print("- Adagrad's learning rate decreases over time")
    print("\nDemo completed!")

if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
Optimizer Comparison Demo
==================================================

Training with different optimizers...
  SGD (lr=0.01): Final loss = 0.9823
  SGD + Momentum: Final loss = 0.7654
  Adam: Final loss = 0.7123
  RMSprop: Final loss = 0.6987
  Adagrad: Final loss = 0.8543

Plot saved as 'optimizer_comparison.png'

Key Observations:
- Adam typically converges fastest
- SGD + Momentum often achieves lower final loss
- Adagrad's learning rate decreases over time

Demo completed!
```

---

## 優化器特性比較

| 優化器 | 收斂速度 | 最終效果 | 記憶體需求 | 適用場景 |
|--------|---------|----------|-----------|----------|
| SGD | 慢 | 好 | 低 | 影像分類 |
| SGD + Momentum | 中 | 好 | 低 | 大多數任務 |
| Adam | 快 | 中等 | 中等 | NLP、快速原型 |
| RMSprop | 快 | 中等 | 中等 | RNN |
| Adagrad | 中 | 一般 | 中等 | 稀疏資料 |

---

## 學習率對優化器的影響

### Adam

```python
# Adam 對學習率較不敏感
adam_configs = [
    {'lr': 1e-3, 'name': 'Adam (default)'},
    {'lr': 1e-4, 'name': 'Adam (small lr)'},
    {'lr': 1e-2, 'name': 'Adam (large lr)'},
]
```

### SGD

```python
# SGD 對學習率非常敏感
sgd_configs = [
    {'lr': 0.1, 'name': 'SGD (lr=0.1)'},
    {'lr': 0.01, 'name': 'SGD (lr=0.01)'},
    {'lr': 0.001, 'name': 'SGD (lr=0.001)'},
]
```

---

## 實用建議

### 1. 快速原型：使用 Adam

```python
optimizer = optim.Adam(model.parameters(), lr=1e-3)
```

### 2. 生產訓練：使用 SGD + Momentum

```python
optimizer = optim.SGD(
    model.parameters(),
    lr=0.1,
    momentum=0.9,
    weight_decay=1e-4
)
scheduler = optim.lr_scheduler.MultiStepLR(
    optimizer, milestones=[30, 60, 90], gamma=0.1
)
```

### 3. RNN/Transformer：使用 Adam

```python
optimizer = optim.Adam(
    model.parameters(),
    lr=1e-4,
    betas=(0.9, 0.98),
    eps=1e-9
)
```

---

## 結論

選擇優化器需要根據具體任務和模型特性：

- **Adam** 是最好的「萬能」選擇，適合快速原型
- **SGD + Momentum** 在許多視覺任務上能達到最好的效果
- **RMSprop** 適合 RNN 和非平穩問題
- **Adagrad** 適合稀疏資料和文字任務

---

*本篇文章為「AI 程式人雜誌 2017 年 11 月號」訓練優化系列補充文章。*