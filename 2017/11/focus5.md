# 優化器比較

## 前言

選擇合適的優化器對深度學習訓練至關重要。本篇文章將比較常用的優化器，包括 SGD、Adam、RMSprop 等，分析它們的優缺點和適用場景。

## 梯度下降基礎

### 批量梯度下降

```python
# 完整資料集上的梯度下降
for _ in range(num_epochs):
    loss = compute_loss(model, all_data)
    grads = torch.autograd.grad(loss, model.parameters())
    params = params - learning_rate * grads
```

### 隨機梯度下降 (SGD)

```python
# 每次使用一個樣本
for batch in dataloader:
    loss = compute_loss(model, batch)
    grads = torch.autograd.grad(loss, model.parameters())
    params = params - learning_rate * grads
```

### Mini-batch SGD

```python
# 實際使用的方式
for batch in dataloader:
    loss = compute_loss(model, batch)
    grads = torch.autograd.grad(loss, model.parameters())
    optimizer.step()
```

## SGD 與 Momentum

### 標準 SGD

```python
# 梯度直接更新
w = w - lr * grad
```

### SGD with Momentum

```python
# 加入動量累積
class SGDwithMomentum:
    def __init__(self, params, lr=0.01, momentum=0.9):
        self.params = params
        self.lr = lr
        self.momentum = momentum
        self.velocities = [torch.zeros_like(p) for p in params]

    def step(self, grads):
        for i, (param, grad) in enumerate(zip(self.params, grads)):
            self.velocities[i] = self.momentum * self.velocities[i] - self.lr * grad
            param = param + self.velocities[i]
```

### Nesterov Momentum

```python
# Nesterov 先看未來
class NesterovMomentum:
    def step(self, grads):
        for i, (param, grad) in enumerate(zip(self.params, grads)):
            v = self.momentum * self.velocities[i] - self.lr * grad
            # 先更新 velocity，再更新參數
            self.velocities[i] = v
            param = param + v
```

## Adam (Adaptive Moment Estimation)

```python
class Adam:
    def __init__(self, params, lr=1e-3, beta1=0.9, beta2=0.999, eps=1e-8):
        self.params = params
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = [torch.zeros_like(p) for p in params]  # 一階矩估計
        self.v = [torch.zeros_like(p) for p in params]  # 二階矩估計
        self.t = 0  # 時間步

    def step(self, grads):
        self.t += 1
        for i, (param, grad) in enumerate(zip(self.params, grads)):
            # 更新一階和二階矩估計
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grad
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (grad ** 2)

            # 偏差校正
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)

            # 更新參數
            param = param - self.lr * m_hat / (torch.sqrt(v_hat) + self.eps)
```

## RMSprop

```python
class RMSprop:
    def __init__(self, params, lr=1e-3, alpha=0.99, eps=1e-8):
        self.params = params
        self.lr = lr
        self.alpha = alpha
        self.eps = eps
        self.avg_gram = [torch.zeros_like(p) for p in params]

    def step(self, grads):
        for i, (param, grad) in enumerate(zip(self.params, grads)):
            # 指數加權平均
            self.avg_gram[i] = self.alpha * self.avg_gram[i] + (1 - self.alpha) * (grad ** 2)

            # 更新參數
            param = param - self.lr * grad / (torch.sqrt(self.avg_gram[i]) + self.eps)
```

## Adagrad

```python
# 適合稀疏梯度
class Adagrad:
    def step(self, grads):
        for i, (param, grad) in enumerate(zip(self.params, grads)):
            self.cache[i] += grad ** 2  # 累積梯度平方
            param = param - self.lr * grad / (torch.sqrt(self.cache[i]) + self.eps)
```

## 比較實驗

```python
#!/usr/bin/env python3
"""Optimizer comparison demo"""

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

class SimpleNet(nn.Module):
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

def demo():
    print("Optimizer Comparison")
    print("=" * 50)

    print("\n1. SGD:")
    print("   - 簡單，但收斂慢")
    print("   - 適合 fine-tuning")
    print("   - 需要 careful learning rate tuning")

    print("\n2. SGD + Momentum:")
    print("   - 加速收斂")
    print("   - 減少震盪")
    print("   - 適合視覺任務")

    print("\n3. Adam:")
    print("   - 自適應學習率")
    print("   - 收斂快")
    print("   - 適合 NLP 和快速原型")
    print("   - 泛化能力有時不如 SGD")

    print("\n4. RMSprop:")
    print("   - 自適應學習率")
    print("   - 適合 RNN")
    print("   - 適合 non-stationary 問題")

    print("\n5. Adagrad:")
    print("   - 自動調整學習率")
    print("   - 適合稀疏資料")
    print("   - 學習率會持續下降")

    # 實驗展示
    print("\n6. Simulated Comparison:")
    optimizers = {
        'SGD': optim.SGD,
        'Adam': optim.Adam,
        'RMSprop': optim.RMSprop
    }

    results = {}
    for name, OptClass in optimizers.items():
        model = SimpleNet()
        opt = OptClass(model.parameters(), lr=0.01)

        losses = []
        for epoch in range(50):
            # 模擬訓練
            x = torch.randn(32, 10)
            y = torch.randn(32, 1)

            pred = model(x)
            loss = nn.MSELoss()(pred, y)

            opt.zero_grad()
            loss.backward()
            opt.step()

            losses.append(loss.item())

        results[name] = losses

    print(f"   Final losses after 50 epochs:")
    for name, losses in results.items():
        print(f"   {name}: {losses[-1]:.4f}")

    print("\n   Observation: Adam typically converges fastest,")
    print("   but SGD+Momentum often achieves lower final loss.")

    print("\nDemo completed!")

if __name__ == "__main__":
    demo()
```

## 實用建議

### 選擇指南

```
┌─────────────────────────────────────────────────────────┐
│              優化器選擇指南                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  任務類型：                                             │
│  ├─ 影像分類/檢測     → SGD + Momentum (或 Adam)       │
│  ├─ NLP/語言模型     → Adam (或 AdamW)                  │
│  ├─ GAN             → Adam (學習率較低)                │
│  ├─ RL              → Adam (或 PPO 內建的優化器)       │
│  └─ 語音識別         → SGD + Momentum                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 學習率設置

```python
# SGD + Momentum
optimizer = optim.SGD(
    model.parameters(),
    lr=0.1,           # 典型值
    momentum=0.9,
    weight_decay=1e-4
)

# Adam
optimizer = optim.Adam(
    model.parameters(),
    lr=1e-3,          # 典型值
    betas=(0.9, 0.999),
    weight_decay=1e-4
)

# AdamW (Adam with Weight Decay Fix)
optimizer = optim.AdamW(
    model.parameters(),
    lr=1e-3,
    weight_decay=0.01
)
```

### AMSGrad

```python
# 解決 Adam 可能不收斂的問題
optimizer = optim.Adam(
    model.parameters(),
    lr=1e-3,
    betas=(0.9, 0.999),
    amsgrad=True  # 使用 AMSGrad 變體
)
```

## 總結

| 優化器 | 優點 | 缺點 | 適用場景 |
|--------|------|------|---------|
| SGD | 泛化好 | 收斂慢 | 影像任務 |
| SGD+Momentum | 加速收斂 | 需要 LR schedule | 大多數任務 |
| Adam | 收斂快 | 可能泛化差 | NLP、快速原型 |
| RMSprop | 自適應 | - | RNN、非平穩問題 |
| Adagrad | 自動調整 | 學習率下降 | 稀疏資料 |

---

**延伸閱讀**

- [Adam Paper](https://www.google.com/search?q=adam+optimizer+kingma+2014)
- [AdamW Paper](https://www.google.com/search?q=adamw+loshchilov+2019)
- [On the Difference of Optimizers](https://www.google.com/search?q=SGD+vs+Adam+generalization)