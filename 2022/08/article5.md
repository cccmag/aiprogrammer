# PyTorch DDP 實戰

## DDP 架構概覽

`DistributedDataParallel`（DDP）是 PyTorch 官方的資料平行實作。底層使用 NCCL 進行高效梯度通訊，上層提供與單 GPU 幾乎一致的 API。

## 實戰步驟

### 第一步：初始化

```python
import torch.distributed as dist
dist.init_process_group(backend='nccl')
local_rank = int(os.environ['LOCAL_RANK'])
torch.cuda.set_device(local_rank)
```

### 第二步：包裝模型

```python
model = MyModel().to(local_rank)
model = DDP(model, device_ids=[local_rank])
```

### 第三步：調整資料載入

```python
sampler = DistributedSampler(dataset)
dataloader = DataLoader(dataset, sampler=sampler, batch_size=32)
```

### 第四步：啟動訓練

使用 torchrun 啟動：
```
torchrun --nproc_per_node=4 train.py
```

## 進階技巧

**梯度累積與 DDP**：使用 `no_sync()` 上下文管理器可暫時關閉梯度同步，實現梯度累積。

**Mixed Precision 訓練**：搭配 `torch.cuda.amp` 使用，可提升訓練速度並減少記憶體。

**動態批次**：透過 `find_unused_parameters` 參數處理動態計算圖。

## 效能陷阱

- 避免在 DDP wrapper 後修改模型架構
- 確保所有 GPU 輸入資料量一致
- 關閉不必要的 broadcast 操作

## 實戰建議

從單機多卡開始，確認 DDP 正確後再擴展到多機。監控 GPU 記憶體使用與通訊時間比例，找出效能瓶頸。

[搜尋 PyTorch DDP 教學](https://www.google.com/search?q=PyTorch+DDP+tutorial+example)
[搜尋 torchrun 分散式訓練](https://www.google.com/search?q=torchrun+distributed+data+parallel)
