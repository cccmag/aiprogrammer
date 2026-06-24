# FairScale 與 FSDP

## FairScale 簡介

FairScale 是 Facebook AI Research（現 Meta）開發的分散式訓練函式庫，作為 PyTorch 的擴充套件。它實作了多種大規模訓練技術，包括 FSDP、Gradient Checkpointing、Sharded Optimizer 等。

## FSDP 核心概念

Fully Sharded Data Parallel（FSDP）將模型參數、梯度和最佳化器狀態全部進行分片。每個 GPU 只儲存一部分參數，需要時透過 all-gather 獲取完整參數進行計算。

## FSDP vs ZeRO

FSDP 實作了 DeepSpeed ZeRO Stage 3 的概念，但整合在 PyTorch 生態中。主要差異：

- FSDP 原生支援 PyTorch 的 autograd 系統
- FSDP 提供更靈活的 sharding strategy 設定
- FSDP 的 wrapping 策略可精細控制哪些層被分片

## 使用方式

```python
from fairscale.nn.data_parallel import FullyShardedDataParallel as FSDP
model = FSDP(model)
```

PyTorch 2.0 後 FSDP 已移至 `torch.distributed.fsdp`。

## Sharding Strategy

**NO_SHARD**：等同於 DDP，不分片。

**SHARD_GRAD_OP**：僅分片梯度（ZeRO Stage 2）。

**FULL_SHARD**：參數、梯度、狀態全部分片（ZeRO Stage 3）。

**HYBRID_SHARD**：節點內 FULL_SHARD，節點間 NO_SHARD。

## 實戰建議

FSDP 適合單機多卡與多機多卡場景。建議從 FULL_SHARD 開始，若通訊成為瓶頸則嘗試 HYBRID_SHARD。開啟 CPU offloading 可進一步減少 GPU 記憶體使用。

## FairScale 其他功能

- 支援管線平行的 `Pipe` 模組
- 提供 `optim.OSS`（Optimizer State Sharding）
- 包含 `nn.checkpoint` 梯度檢查點實作

[搜尋 FairScale FSDP](https://www.google.com/search?q=FairScale+FSDP+distributed+training)
[搜尋 PyTorch FSDP 教學](https://www.google.com/search?q=PyTorch+FSDP+tutorial)
