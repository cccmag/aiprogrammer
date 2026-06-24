# 學習率排程與 Warmup

## 為什麼需要 Warmup

訓練初期模型權重隨機初始化，大的學習率可能導致不穩定。Warmup 在初期使用小學習率，逐漸增加到目標值。

## 常見排程器

### Step LR

```python
scheduler = torch.optim.lr_scheduler.StepLR(
    optimizer,
    step_size=30,  # 每 30 個 epoch 衰減
    gamma=0.1  # 學習率乘以此值
)
```

### Cosine Annealing

```python
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=100,  # 最大迭代次數
    eta_min=1e-6  # 最小學習率
)
```

### Warmup + Cosine

```python
class WarmupCosineScheduler:
    def __init__(self, optimizer, warmup_epochs, total_epochs, min_lr=1e-6):
        self.optimizer = optimizer
        self.warmup_steps = warmup_epochs
        self.total_steps = total_epochs
        self.min_lr = min_lr
        self.base_lrs = [pg["lr"] for pg in optimizer.param_groups]
    
    def step(self, epoch):
        if epoch < self.warmup_steps:
            # Warmup：線性增加
            factor = epoch / self.warmup_steps
        else:
            # Cosine 衰減
            progress = (epoch - self.warmup_steps) / (self.total_steps - self.warmup_steps)
            factor = 0.5 * (1 + np.cos(np.pi * progress))
        
        for param_group, base_lr in zip(self.optimizer.param_groups, self.base_lrs):
            param_group["lr"] = max(base_lr * factor, self.min_lr)
```

## PyTorch 內建 Warmup

```python
# 使用 SequentialLR 組合 warmup 和衰減
scheduler = torch.optim.lr_scheduler.SequentialLR(
    optimizer,
    schedulers=[
        # Warmup 階段（線性）
        torch.optim.lr_scheduler.LinearLR(
            optimizer, start_factor=0.1, end_factor=1.0, total_iters=5
        ),
        # 主階段（cosine）
        torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=95
        )
    ],
    milestones=[5]  # warmup 結束的 epoch
)
```

## OneCycleLR

自動調整 warmup 和衰減：

```python
scheduler = torch.optim.lr_scheduler.OneCycleLR(
    optimizer,
    max_lr=1e-3,
    epochs=100,
    steps_per_epoch=len(train_loader),
    pct_start=0.1  # 前 10% 為 warmup
)
```

## 訓練循環中的使用

```python
model.train()
scheduler = torch.optim.lr_scheduler.OneCycleLR(
    optimizer, max_lr=1e-3, epochs=10, steps_per_epoch=len(train_loader)
)

for epoch in range(10):
    for batch in train_loader:
        optimizer.zero_grad()
        output = model(batch["input"])
        loss = criterion(output, batch["target"])
        loss.backward()
        optimizer.step()
        scheduler.step()  # 每個 step 更新
```

## 學習率檢測

```python
import matplotlib.pyplot as plt

lrs = []
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=100, eta_min=1e-6
)

for epoch in range(100):
    lrs.append(optimizer.param_groups[0]["lr"])
    scheduler.step()

plt.plot(lrs)
plt.xlabel("Epoch")
plt.ylabel("Learning Rate")
plt.title("Cosine Annealing LR Schedule")
plt.savefig("lr_schedule.png")
```

## 參考資源

- https://www.google.com/search?q=learning+rate+scheduler+PyTorch+warmup+tutorial+2020
- https://www.google.com/search?q=warmup+cosine+annealing+OneCycleLR+training+schedule
- https://www.google.com/search?q=learning+rate+decay+strategy+deep+learning+optimal+schedule