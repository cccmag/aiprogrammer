# 4. 梯度累積技術

## 原理

梯度累積讓我們用較小的批次大小模擬更大的批次：

```
實際批次大小 = 微型批次大小 × 累積步數
```

每個微型批次獨立前向/後向傳播，梯度暫存，最後平均後更新參數。

## 基本實作

```python
accumulation_steps = 4
effective_batch_size = batch_size * accumulation_steps

model.train()
optimizer.zero_grad()

for i, batch in enumerate(train_loader):
    inputs, targets = batch
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    
    # 標準化 loss
    loss = loss / accumulation_steps
    loss.backward()
    
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

## 與混合精度結合

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
accumulation_steps = 4

for i, batch in enumerate(train_loader):
    with autocast():
        outputs = model(batch["input"])
        loss = criterion(outputs, batch["target"])
        loss = loss / accumulation_steps
    
    scaler.scale(loss).backward()
    
    if (i + 1) % accumulation_steps == 0:
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()
```

## 學習率調整

使用梯度累積時，有效批次變大，通常需要相應調整學習率：

```python
# 線性縮放規則
# 如果批次擴大 4 倍，學習率通常也增加 4 倍（需謹慎）
adjusted_lr = base_lr * accumulation_steps
optimizer = torch.optim.Adam(model.parameters(), lr=adjusted_lr)
```

## 批次正規化處理

使用梯度累積時，需要注意 BatchNorm 的統計：

```python
# 建議使用 GroupNorm 或 LayerNorm
# 它們不依賴批次統計
model = nn.Sequential(
    nn.Linear(768, 256),
    nn.GroupNorm(num_groups=8, num_channels=256),
    nn.ReLU()
)
```

## 記憶體節省效果

| 配置 | 微型批次 | 累積 | 總批次 | 記憶體 |
|------|---------|------|--------|--------|
| 無 | - | - | 32 | 16GB |
| 梯度累積 | 8 | 4 | 32 | ~8GB |
| AMP + 累積 | 8 | 4 | 32 | ~4GB |

## 參考資源

- https://www.google.com/search?q=gradient+accumulation+PyTorch+batch+size+memory+efficiency+tutorial
- https://www.google.com/search?q=accumulation+steps+effective+batch+size+learning+rate+scaling
- https://www.google.com/search?q=gradient+accumulation+AMP+mixed+precision+combined+training+example