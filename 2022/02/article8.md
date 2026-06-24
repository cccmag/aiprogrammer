# 分散式資料平行 DDP

## PyTorch DistributedDataParallel 深度解析

### 從 DP 到 DDP

PyTorch 提供了兩種資料平行封裝：DataParallel（DP）和 DistributedDataParallel（DDP）。

DP 是較早的實作，工作原理簡單：每次 forward 時將 batch 分割到各 GPU，收集結果後再計算 loss 和 gradient。但 DP 有嚴重的效能問題：主 GPU（GPU 0）需要負責所有通訊和計算，容易成為瓶頸；且 DP 使用 Python GIL 限制的多執行緒模型。

DDP 是 2019 年後推薦的資料平行實作。每個 GPU 擁有獨立的 Python 程序，完全避免 GIL；使用 NCCL 進行非同步梯度通訊；沒有主 GPU 瓶頸，可擴展到數百個 GPU。

### DDP 的基本用法

```python
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP

def train(rank, world_size):
    # 初始化程序組
    dist.init_process_group(
        backend="nccl",
        init_method="tcp://localhost:23456",
        world_size=world_size,
        rank=rank
    )

    # 每個 GPU 一個程序
    torch.cuda.set_device(rank)
    model = MyModel().cuda(rank)
    ddp_model = DDP(model, device_ids=[rank])

    # 每個 GPU 處理不同的資料分片
    sampler = torch.utils.data.distributed.DistributedSampler(
        dataset, num_replicas=world_size, rank=rank
    )
    dataloader = DataLoader(dataset, batch_size=32, sampler=sampler)

    ddp_model.train()
    for epoch in range(num_epochs):
        sampler.set_epoch(epoch)
        for data, target in dataloader:
            data, target = data.cuda(rank), target.cuda(rank)
            output = ddp_model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

    dist.destroy_process_group()

if __name__ == "__main__":
    world_size = torch.cuda.device_count()
    mp.spawn(train, args=(world_size,), nprocs=world_size)
```

### torchrun：更簡單的啟動方式

PyTorch 1.10+ 推薦使用 torchrun（取代 multiprocessing.spawn）：

```bash
torchrun --nproc_per_node=4 train.py
```

```python
# train.py
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def main():
    dist.init_process_group("nccl")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)

    model = MyModel().cuda(local_rank)
    ddp_model = DDP(model, device_ids=[local_rank])

    sampler = DistributedSampler(dataset)
    dataloader = DataLoader(dataset, batch_size=32, sampler=sampler)

    for epoch in range(num_epochs):
        sampler.set_epoch(epoch)
        for data, target in dataloader:
            # ... 訓練循環 ...
```

### DDP 的核心機制

DDP 在 backward 階段自動同步梯度。其工作流程：

1. **初始化**：每個程序建立模型副本
2. **Forward**：每個程序獨立執行 forward，計算 loss
3. **Backward**：計算梯度時，DDP 使用 hook 攔截梯度
4. **All-Reduce**：DDP 對每個參數執行 all-reduce（NCCL），平均所有程序的梯度
5. **更新**：每個程序用平均後的梯度更新自己的參數

關鍵優化：DDP 將 all-reduce 與 backward 重疊執行。當第 i 層的梯度計算完成時，立即開始 all-reduce，同時繼續計算第 i-1 層的梯度。這種「梯度桶（Gradient Bucket）」機制極大減少了通訊延遲。

### 進階配置

```python
# bucket 配置（影響通訊效率）
ddp_model = DDP(model, device_ids=[rank],
                bucket_cap_mb=25)  # 預設 25 MB

# 尋找未使用的參數
ddp_model = DDP(model, device_ids=[rank],
                find_unused_parameters=True)  # 如果模型有條件執行分支

# 非同步梯度 reduction
with ddp_model.no_sync():
    # 在這個 context 中不進行梯度同步
    # 用於梯度累積
    loss.backward()
```

### 多節點訓練

```bash
# 節點 1
torchrun --nnodes=2 --nproc_per_node=8 \
    --node_rank=0 --master_addr="192.168.1.100" --master_port=12345 \
    train.py

# 節點 2
torchrun --nnodes=2 --nproc_per_node=8 \
    --node_rank=1 --master_addr="192.168.1.100" --master_port=12345 \
    train.py
```

### 延伸閱讀

- [PyTorch Distributed Tutorial](https://www.google.com/search?q=PyTorch+distributed+data+parallel+tutorial)
- [DDP Design Note](https://www.google.com/search?q=PyTorch+DDP+design+note)
