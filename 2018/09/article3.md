# 學習率排程與微調技巧

## 1. 學習率的重要性

學習率控制梯度更新的幅度。太大會震盪不收斂，太小會收斂緩慢。

```python
# 學習率過大
loss: [1.2, 2.5, 1.8, 3.1, 2.0, 4.5...]  # 震盪發散

# 學習率過小
loss: [1.2, 1.15, 1.10, 1.06, 1.03, 1.01...]  # 收斂太慢

# 適當學習率
loss: [1.2, 0.8, 0.5, 0.3, 0.15, 0.08...]  # 平穩收斂
```

## 2. 常見排程策略

```python
# Step LR：每 N 個 epoch 衰減一次
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

# Multi-Step LR：在特定 epoch 衰減
scheduler = optim.lr_scheduler.MultiStepLR(
    optimizer, milestones=[60, 120, 160], gamma=0.2
)

# Cosine Annealing：餘弦函數衰減
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=150)

# ReduceLROnPlateau：監控指標停滞時衰減
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=10
)

# Exponential LR：指數衰減
scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)
```

## 3. Warmup

```python
class WarmupScheduler:
    def __init__(self, optimizer, warmup_epochs, base_lr):
        self.optimizer = optimizer
        self.warmup_epochs = warmup_epochs
        self.base_lr = base_lr
        self.current_epoch = 0

    def step(self):
        if self.current_epoch < self.warmup_epochs:
            lr = self.base_lr * (self.current_epoch + 1) / self.warmup_epochs
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = lr
        self.current_epoch += 1
```

## 4. 微調學習率設定

```python
# 預訓練層使用較小學習率
optimizer = optim.Adam([
    {'params': model.backbone.parameters(), 'lr': 1e-5},
    {'params': model.head.parameters(), 'lr': 1e-3}
])
```

## 5. 小結

合理的學習率排程能顯著提升訓練效率和最終性能。微調時使用較小的學習率是重要的技巧。

---

**參考資料**
- [Learning Rate Scheduling](https://www.google.com/search?q=learning+rate+scheduling+deep+learning)
- [Deep Learning Training Tips](https://www.google.com/search?q=deep+learning+training+lr+scheduler+tips)