# 學習率調整

## 前言

學習率是深度學習中最重要的超參數之一。合適的學習率可以加速收斂，過高或過低都會影響訓練效果。本篇文章將探討各種學習率調整策略。

## 學習率的重要性

```
┌─────────────────────────────────────────────────────────┐
│              學習率對訓練的影響                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  學習率過高：                                            │
│  - 震盪不收斂                                           │
│  - 可能越過最優點                                        │
│                                                         │
│  學習率過低：                                            │
│  - 收斂緩慢                                             │
│  - 可能陷入局部最優                                      │
│                                                         │
│  合適的學習率：                                          │
│  - 平穩收斂                                             │
│  - 到達全域或接近全域最優                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 學習率 Schedule

### 1. Step Decay

```python
def step_decay(epoch):
    """每 N 個 epoch 衰減學習率"""
    n_epochs_drop = 30
    drop_rate = 0.1
    lr = initial_lr * (drop_rate ** (epoch // n_epochs_drop))
    return lr

# 使用
for epoch in range(num_epochs):
    lr = step_decay(epoch)
    optimizer.param_groups[0]['lr'] = lr
```

### 2. Cosine Annealing

```python
import math

def cosine_annealing(epoch, T_max, eta_min=0):
    """Cosine annealing schedule"""
    return eta_min + (initial_lr - eta_min) * \
           (1 + math.cos(math.pi * epoch / T_max)) / 2

# 使用
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=num_epochs)
```

### 3. Warmup

在訓練初期逐漸增加學習率：

```python
def warmup_lr(epoch, warmup_epochs=5, initial_lr=1e-7, target_lr=0.1):
    """Warmup learning rate"""
    if epoch < warmup_epochs:
        return initial_lr + (target_lr - initial_lr) * epoch / warmup_epochs
    else:
        # Warmup 後使用正常 schedule
        return step_decay(epoch - warmup_epochs)

# PyTorch 內建 warmup
scheduler = torch.optim.lr_scheduler.LambdaLR(
    optimizer,
    lr_lambda=lambda epoch: warmup_lr(epoch)
)
```

### 4. Cyclical Learning Rate

週期性的學習率變化：

```python
# CyclicLR
scheduler = torch.optim.lr_scheduler.CyclicLR(
    optimizer,
    base_lr=0.001,
    max_lr=0.1,
    step_size_up=2000,
    step_size_down=None,
    mode='triangular'
)

# 學習率變化圖：
# lr
#  ^     /\      /\      /\
#  |    /  \    /  \    /  \
#  |   /    \  /    \  /    \
#  |  /      \/      \/      \
#  └────────────────────────────> step
```

## 比較不同的 Schedule

```python
#!/usr/bin/env python3
"""Learning rate schedule comparison"""

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import math

def demo():
    print("Learning Rate Schedule Comparison")
    print("=" * 50)

    initial_lr = 0.1
    num_epochs = 100

    # 1. Step Decay
    step_lrs = []
    lr = initial_lr
    for epoch in range(num_epochs):
        step_lrs.append(lr)
        if (epoch + 1) % 30 == 0:
            lr *= 0.1

    # 2. Cosine Annealing
    cosine_lrs = [
        0.1 + (initial_lr - 0.1) * (1 + math.cos(math.pi * e / num_epochs)) / 2
        for e in range(num_epochs)
    ]

    # 3. Exponential Decay
    exp_lrs = [initial_lr * (0.95 ** e) for e in range(num_epochs)]

    # 4. Warmup + Cosine
    warmup_epochs = 10
    warmup_lrs = []
    for epoch in range(num_epochs):
        if epoch < warmup_epochs:
            lr = 1e-6 + (initial_lr - 1e-6) * epoch / warmup_epochs
        else:
            adjusted_epoch = epoch - warmup_epochs
            adjusted_max = num_epochs - warmup_epochs
            lr = 0.1 + (initial_lr - 0.1) * (1 + math.cos(math.pi * adjusted_epoch / adjusted_max)) / 2
        warmup_lrs.append(lr)

    print("Schedule | Initial LR | Final LR | Avg LR")
    print("-" * 50)
    print(f"Step      | {step_lrs[0]:.6f}    | {step_lrs[-1]:.6f} | {sum(step_lrs)/len(step_lrs):.6f}")
    print(f"Cosine    | {cosine_lrs[0]:.6f}    | {cosine_lrs[-1]:.6f} | {sum(cosine_lrs)/len(cosine_lrs):.6f}")
    print(f"Exponential| {exp_lrs[0]:.6f}    | {exp_lrs[-1]:.8f} | {sum(exp_lrs)/len(exp_lrs):.6f}")
    print(f"Warmup    | {warmup_lrs[0]:.8f} | {warmup_lrs[-1]:.6f} | {sum(warmup_lrs)/len(warmup_lrs):.6f}")

    print("\nKey Observations:")
    print("- Step: Abrupt changes, simple but effective")
    print("- Cosine: Smooth decay, often better convergence")
    print("- Exponential: Smooth but aggressive decay")
    print("- Warmup: Helps early training stability")

    print("\nDemo completed!")

if __name__ == "__main__":
    demo()
```

## One Cycle Policy

由 Leslie Smith 提出，效果優秀：

```python
def one_cycle(epoch, max_lr, pct_warmup=0.3, pct_max=0.9):
    """One Cycle Learning Rate Policy"""
    if epoch < num_epochs * pct_warmup:
        # Warmup 階段
        return max_lr * epoch / (num_epochs * pct_warmup)
    elif epoch < num_epochs * pct_max:
        # 衰減階段
        progress = (epoch - num_epochs * pct_warmup) / (num_epochs * (pct_max - pct_warmup))
        return max_lr * (1 - 0.5 * (1 + math.cos(math.pi * progress)))
    else:
        # 最終衰減
        progress = (epoch - num_epochs * pct_max) / (num_epochs * (1 - pct_max))
        return max_lr * 0.01 * (1 + math.cos(math.pi * progress))
```

## 實用建議

### 1. 從較高的學習率開始

```python
# 先用少量資料測試最大穩定學習率
model = create_model()
optimizer = torch.optim.Adam(model.parameters(), lr=1.0)

# 如果 loss 爆炸，說明學習率太高
# 如果 loss 下降緩慢，可以提高學習率
```

### 2. 監控學習率

```python
# 使用 TensorBoard 監控
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter()
for epoch in range(num_epochs):
    writer.add_scalar('Learning Rate',
                     optimizer.param_groups[0]['lr'],
                     epoch)
```

### 3. 不同層使用不同學習率

```python
# 較低層使用較小的學習率
optimizer = torch.optim.Adam([
    {'params': model.base.parameters(), 'lr': 1e-4},
    {'params': model.head.parameters(), 'lr': 1e-3}
], lr=1e-4)  # 這個 lr 會被當作預設值
```

## 總結

學習率調整是訓練成功的關鍵。One Cycle Policy 通常效果很好，但需要仔細設置最大學習率。Warmup 可以提高訓練穩定性。

---

**延伸閱讀**

- [Smith, 2017: Cyclical Learning Rates](https://www.google.com/search?q=cyclical+learning+rates+smith+2017)
- [One Cycle Policy](https://www.google.com/search?q=one+cycle+policy+smith)
- [Learning Rate Schedules](https://www.google.com/search?q=learning+rate+schedule+pytorch)