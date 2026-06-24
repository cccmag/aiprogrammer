# 梯度累積記憶體節省

## 基本概念

梯度累積允許用小批次類是大批次，節省記憶體：

```python
accumulation_steps = 4
batch_size = 8
effective_batch_size = batch_size * accumulation_steps

model.train()
optimizer.zero_grad()

for i, (data, target) in enumerate(train_loader):
    # 前向傳播
    output = model(data.cuda())
    loss = criterion(output, target.cuda())
    
    # 標準化 loss
    loss = loss / accumulation_steps
    loss.backward()
    
    # 每累積足够步數後更新
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

## 記憶體節省原理

| 配置 | 記憶體使用 |
|------|-----------|
| 批次 32 | ~16GB |
| 批次 8 + 累積 4 | ~8GB |
| 批次 8 + 累積 4 + AMP | ~4GB |

## 實用計算器

```python
def calculate_effective_batch_size(micro_batch_size, accumulation_steps):
    return micro_batch_size * accumulation_steps

def estimate_memory(batch_size, model_size_gb=1.0, hidden_size=768, layers=12):
    # 粗略估計
    parameters_gb = model_size_gb
    activations_gb = batch_size * layers * hidden_size * 8 / 1e9
    gradients_gb = model_size_gb
    optimizer_states_gb = model_size_gb * 4  # Adam 需要額外狀態
    
    return parameters_gb + activations_gb + gradients_gb + optimizer_states_gb
```

## 與 AMP 結合

```python
from torch.cuda.amp import autocast, GradScaler

accumulation_steps = 4
scaler = GradScaler()

for i, batch in enumerate(train_loader):
    with autocast():
        output = model(batch["input"].cuda())
        loss = criterion(output, batch["target"].cuda())
        loss = loss / accumulation_steps
    
    scaler.scale(loss).backward()
    
    if (i + 1) % accumulation_steps == 0:
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()
```

## 動態累積步數

根據可用記憶體動態調整：

```python
def get_optimal_accumulation_steps(batch_size, model, max_memory_gb=16):
    test_batch = batch_size
    while test_batch >= 1:
        try:
            # 嘗試配置
            torch.cuda.empty_cache()
            model.train()
            x = torch.randn(test_batch, 768).cuda()
            y = model(x)
            del x, y
            return max_memory_gb * 1024 // (batch_size * 4)  # 估算
        except RuntimeError:
            test_batch //= 2
    return 1
```

## 何時使用梯度累積

優點：
- 可訓練更大模型
- 模擬大批次訓練
- 訓練更穩定（大批次可能不穩定）

缺點：
- 訓練速度可能略慢
- 需要小心學習率調整

## 參考資源

- https://www.google.com/search?q=gradient+accumulation+memory+saving+PyTorch+tutorial+2020
- https://www.google.com/search?q=effective+batch+size+gradient+accumulation+learning+rate+adjustment
- https://www.google.com/search?q=gradient+accumulation+AMP+mixed+precision+combined+example