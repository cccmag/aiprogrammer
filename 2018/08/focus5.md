# Optimizer 與學習率排程

## PyTorch 的優化系統

### 基本用法

```python
import torch
import torch.nn as nn
import torch.optim as optim

model = nn.Linear(10, 2)
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 訓練迴圈
for epoch in range(100):
    optimizer.zero_grad()  # 清除梯度
    loss = criterion(model(x), y)
    loss.backward()
    optimizer.step()  # 更新參數
```

### 常用優化器

```python
# SGD（隨機梯度下降）
optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Adam（自適應矩估計）
optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))

# AdamW（Adam with Weight Decay）
optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

# RMSprop
optim.RMSprop(model.parameters(), lr=0.01, alpha=0.99)

# Adagrad
optim.Adagrad(model.parameters(), lr=0.01)

# Adadelta
optim.Adadelta(model.parameters(), lr=1.0)
```

### Learning Rate Scheduler

```python
# Step LR
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

# Multi-Step LR
scheduler = optim.lr_scheduler.MultiStepLR(
    optimizer, milestones=[30, 60, 90], gamma=0.1
)

# Exponential LR
scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)

# ReduceLROnPlateau
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=5
)

# Cosine Annealing
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)

# 訓練迴圈中使用
for epoch in range(100):
    scheduler.step()
    print(f"Epoch {epoch}, LR: {optimizer.param_groups[0]['lr']}")
```

### 自訂 Scheduler

```python
class WarmupScheduler(torch.optim.lr_scheduler._LRScheduler):
    def __init__(self, optimizer, warmup_epochs, base_lr, last_epoch=-1):
        self.warmup_epochs = warmup_epochs
        self.base_lr = base_lr
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        if self.last_epoch < self.warmup_epochs:
            return [self.base_lr * (self.last_epoch + 1) / self.warmup_epochs
                    for _ in self.base_lrs]
        return self.base_lrs
```

### 不同參數群組

```python
# 不同層使用不同學習率
optimizer = optim.Adam([
    {'params': model.backbone.parameters(), 'lr': 1e-4},
    {'params': model.head.parameters(), 'lr': 1e-3}
], lr=1e-2)  # 預設學習率（未指定的參數使用）

# 或使用引數
optimizer = optim.Adam(model.parameters(), lr=1e-3)
# 但個別調整
for param_group in optimizer.param_groups:
    param_group['lr'] = param_group['lr'] * 0.95
```

### 梯度裁剪

```python
# 防止梯度爆炸
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# 或
torch.nn.utils.clip_grad_value_(model.parameters(), clip_value=1.0)

loss.backward()
optimizer.step()
```

### 小結

PyTorch 的優化系統提供了豐富的選擇。Adam 是良好的首選，但對於特定任務可能需要嘗試其他優化器。學習率排程對於收斂速度和最終性能都有重要影響。

---

**下一步**：[DataLoader 與資料處理](focus6.md)