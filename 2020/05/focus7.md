# 7. 分散式訓練入門

## 分散式訓練策略

- **資料平行（Data Parallel）**：多 GPU 處理不同批次
- **模型平行（Model Parallel）**：模型分布在多 GPU
- **流水線平行（Pipeline Parallel）**：將模型分階段處理

## 資料平行 (DataParallel)

最簡單的多 GPU 訓練方式：

```python
model = MyModel()
if torch.cuda.device_count() > 1:
    model = nn.DataParallel(model)

model = model.cuda()
```

但 DataParallel 有瓶頸——梯度在 GPU 0 彙總。

## 分散式資料平行 (DDP)

更高效的實現：

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

# 初始化程序組
dist.init_process_group(backend="nccl")
local_rank = dist.get_rank()
torch.cuda.set_device(local_rank)

model = MyModel().cuda(local_rank)
model = DDP(model, device_ids=[local_rank])

# 訓練迴圈
for batch in train_loader:
    inputs = batch.cuda(local_rank)
    outputs = model(inputs)
    loss = criterion(outputs, targets.cuda(local_rank))
    loss.backward()
    optimizer.step()
```

## 啟動 DDP 訓練

```bash
python -m torch.distributed.launch \
    --nproc_per_node=4 \
    train.py
```

## 環境變數設定

```python
import os

os.environ["MASTER_ADDR"] = "localhost"
os.environ["MASTER_PORT"] = "29500"
os.environ["RANK"] = "0"
os.environ["WORLD_SIZE"] = "1"
```

## 同步 BatchNorm

多 GPU 訓練時 BatchNorm 統計需要同步：

```python
model = nn.SyncBatchNorm.convert_sync_batchnorm(model)
```

## Horovod 分散式訓練

另一個流行的分散式訓練框架：

```python
import horovod.torch as hvd

hvd.init()
rank = hvd.rank()

model = model.cuda(rank)
optimizer = hvd.DistributedOptimizer(
    optimizer, named_parameters=model.named_parameters()
)
hvd.broadcast_parameters(model.state_dict(), root_rank=0)
```

## 何時使用分散式訓練

| 模型大小 | GPU 需求 | 建議方法 |
|---------|---------|---------|
| < 1B 參數 | 1-2 GPU | 單機單卡 / DP |
| 1-10B 參數 | 4-8 GPU | DDP |
| > 10B 參數 | 8+ GPU | 模型平行 + DDP |

## 參考資源

- https://www.google.com/search?q=distributed+training+PyTorch+DDP+DataParallel+multi+GPU+tutorial+2020
- https://www.google.com/search?q=DistributedDataParallel+NVLink+GPU+communication+performance
- https://www.google.com/search?q=Horovod+distributed+training+TensorFlow+PyTorch+setup