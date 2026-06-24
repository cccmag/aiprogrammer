# 分散式訓練框架

## NCCL 通訊庫

NVIDIA Collective Communications Library（NCCL）：

```python
import torch.distributed as dist

dist.init_process_group(backend="nccl")
local_rank = dist.get_rank() % torch.cuda.device_count()
torch.cuda.set_device(local_rank)

# 所有參與者同步
dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
```

## Horovod 框架

```python
import horovod.torch as hvd

hvd.init()
optimizer = hvd.DistributedOptimizer(
    optimizer,
    named_parameters=model.named_parameters(),
    compression=hvd.Compression.fp16
)

# 廣播初始學習率
optimizer.param_groups[0]['lr'] *= hvd.size()
```

## DeepSpeed

Microsoft 的分散式訓練庫：

```python
from deepspeed import DeepSpeed ZeROOptimizer

model, optimizer, _, _ = deepspeed.initialize(
    model=model,
    config_params=ds_config
)
```

## 張量並行

```python
# Megatron-LM 風格的張量並行
class TensorParallelModel(nn.Module):
    def __init__(self):
        self.linear = ColumnParallelLinear(...)
```

---

## 延伸閱讀

- [NCCL+官方文檔](https://www.google.com/search?q=NCCL+documentation)
- [Horovod+使用說明](https://www.google.com/search?q=Horovod+distributed+training)
- [DeepSpeed+教學](https://www.google.com/search?q=DeepSpeed+tutorial)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*