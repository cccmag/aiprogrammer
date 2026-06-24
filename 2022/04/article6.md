# 學習率熱身與餘弦衰減

## 學習率熱身的必要性

在訓練初期，模型參數是隨機初始化的，此時的梯度方向可能不穩定。如果直接使用較大的學習率，可能導致模型震盪甚至發散。學習率熱身（Learning Rate Warmup）在訓練初期逐步增加學習率，讓模型平穩度過初始階段。

## 線性熱身實作

```python
def linear_warmup(optimizer, current_step, warmup_steps):
    if current_step < warmup_steps:
        lr_scale = min(1.0, (current_step + 1) / warmup_steps)
        for pg in optimizer.param_groups:
            pg['lr'] = lr_scale * pg['lr']
```

使用 LambdaLR 可以更優雅地實現：

```python
warmup_epochs = 5
lambda_lr = lambda e: min(1.0, (e + 1) / warmup_epochs)
scheduler = optim.lr_scheduler.LambdaLR(optimizer, lambda_lr)
```

## 餘弦退火衰減

餘弦退火（Cosine Annealing）是一種流行的學習率衰減策略，學習率按照餘弦曲線從初始值下降到最小值：

```
lr_t = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(t / T * π))
```

```python
scheduler = optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=100, eta_min=1e-6
)
```

## Warmup + Cosine Decay 完整策略

結合熱身與餘弦衰減是當前訓練大型模型的主流策略：

```python
class WarmupCosineScheduler:
    def __init__(self, optimizer, warmup_epochs, total_epochs):
        self.optimizer = optimizer
        self.warmup_epochs = warmup_epochs
        self.total_epochs = total_epochs

    def step(self, epoch):
        if epoch < self.warmup_epochs:
            lr_scale = (epoch + 1) / self.warmup_epochs
        else:
            progress = (epoch - self.warmup_epochs) / (self.total_epochs - self.warmup_epochs)
            lr_scale = 0.5 * (1 + math.cos(math.pi * progress))
        for pg in self.optimizer.param_groups:
            pg['lr'] = pg['initial_lr'] * lr_scale
```

## Cosine Annealing with Warm Restarts

`CosineAnnealingWarmRestarts` 定期重啟學習率，有助於逃離局部最小值：

```python
scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(
    optimizer, T_0=20, T_mult=2
)
```

## 參考資料

- Cosine Annealing 論文：https://arxiv.org/abs/1608.03983
- SGDR (Warm Restarts) 論文：https://arxiv.org/abs/1608.03983
- PyTorch 排程器文件：https://pytorch.org/docs/stable/optim.html
