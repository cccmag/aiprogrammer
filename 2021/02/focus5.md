# 分散式訓練

## 多 GPU 訓練策略

### 資料平行（DataParallel）

```python
model = nn.Linear(10, 1)
model = nn.DataParallel(model)
```

問題：使用單一程序，有通訊瓶頸

### 分散式資料平行（DDP）

```python
import torch.distributed as dist

dist.init_process_group(backend='nccl')
model = nn.parallel.DistributedDataParallel(model)
```

### 啟動方式

```bash
python -m torch.distributed.launch \
    --nproc_per_node=2 \
    train.py
```

## 多節點訓練

### 設定

```bash
# Node 0
python -m torch.distributed.launch \
    --nnodes=2 \
    --node_rank=0 \
    --master_addr="192.168.1.1" \
    train.py

# Node 1
python -m torch.distributed.launch \
    --nnodes=2 \
    --node_rank=1 \
    --master_addr="192.168.1.1" \
    train.py
```

## 混合精度訓練

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in dataloader:
    with autocast():
        output = model(input)
        loss = criterion(output, target)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## 實用技巧

1. **使用 `find_unused_parameters=True`**：如果網路有條件分支
2. **梯度累積**：模擬更大 batch size
3. **梯度壓縮**：減少通訊開銷

---

## 延伸閱讀

- [分散式訓練教程](https://www.google.com/search?q=PyTorch+distributed+training+tutorial)
- [DDP+vs+DataParallel](https://www.google.com/search?q=DataParallel+vs+DistributedDataParallel)
- [混合精度訓練詳解](https://www.google.com/search?q=mixed+precision+training+PyTorch)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*