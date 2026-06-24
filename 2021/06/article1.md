# Article 1：從單卡到多卡 — 分散式訓練入門

## 何時需要分散式訓練

當單卡的記憶體無法容納模型、訓練時間過長、或需要處理大量資料時，就需要分散式訓練。簡單的判斷標準：如果你需要在單卡上使用很小的 batch size 才能運行，或者訓練一個 epoch 需要數小時，分散式訓練可能是解決方案。

## 基本的分散式設定

分散式訓練需要多個計算節點和高速網路互連。每個節點運行一個或多個程序實例，通過網路同步梯度。環境變數如 `WORLD_SIZE`、`RANK`、`LOCAL_RANK` 控制程式的運行方式。

## 簡單的 DDP 範例

```python
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

# 初始化
dist.init_process_group(backend='nccl')
local_rank = int(os.environ['LOCAL_RANK'])
torch.cuda.set_device(local_rank)

# 模型和資料
model = MyModel().cuda()
model = DDP(model, device_ids=[local_rank])
dataset = MyDataset()
sampler = DistributedSampler(dataset)
loader = DataLoader(dataset, sampler=sampler)

# 訓練迴圈
for data, target in loader:
    data, target = data.cuda(), target.cuda()
    output = model(data)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()
```

## 關鍵概念

DistributedSampler 確保每個 GPU 處理不同的資料。DDP 自動處理梯度同步。訓練結束後需要呼叫 `dist.destroy_process_group()`。

## 硬體需求

至少需要多 GPU 系統或叢集環境。對網路頻寬敏感——高速互連（如 NVLink、InfiniBand）能顯著提升效能。

## 參考資源

- PyTorch DDP Tutorial：https://www.google.com/search?q=pytorch+distributed+dataparallel+tutorial
- Multi-GPU Training：https://www.google.com/search?q=multi+GPU+training+pytorch+beginner