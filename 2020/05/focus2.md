# 2. GPU 記憶體管理

## 記憶體階層

GPU 擁有多層記憶體：
- **全域記憶體（Global Memory）**：最大但速度較慢，約 500-1000 GB/s
- **共享記憶體（Shared Memory）**：每個區塊共用，速度極快
- **暫存器（Registers）**：每個線程私有
- **L2 快取**：所有區塊共享

最佳化記憶體使用可大幅提升效能。

## 記憶體不足處理

當遇到 CUDA out of memory 錯誤時：

```python
# 1. 減少批次大小
batch_size = 8  # 嘗試更小的值

# 2. 梯度累積（見 focus4）

# 3. 啟用混合精度
from torch.cuda.amp import autocast, GradScaler

# 4. 清理未使用的張量
del intermediate_tensor  # 刪除不需要的張量
torch.cuda.empty_cache()  # 清理快取
```

## 記憶體分配策略

```python
# 預分配記憶體
torch.cuda.empty_cache()

# 使用 pin_memory 加速 CPU-GPU 傳輸
train_loader = torch.utils.data.DataLoader(
    dataset,
    batch_size=batch_size,
    num_workers=4,
    pin_memory=True  # 加速傳輸
)
```

## 記憶體追蹤

```python
import torch

class MemoryTracker:
    def __init__(self):
        self.start = None
    
    def start_tracking(self):
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
            self.start = torch.cuda.memory_allocated()
    
    def report(self, label=""):
        if torch.cuda.is_available():
            current = torch.cuda.memory_allocated() / 1024**3
            peak = torch.cuda.max_memory_allocated() / 1024**3
            print(f"{label}: 目前 {current:.2f} GB, 峰值 {peak:.2f} GB")

tracker = MemoryTracker()
tracker.start_tracking()
```

## 記憶體碎片整理

長時間訓練可能導致記憶體碎片：

```python
# 定期呼叫
torch.cuda.empty_cache()

# 使用 contiguous 確保張量記憶體連續
x = x.contiguous()
```

## 混合精度與記憶體

使用 FP16 可將記憶體使用減半：
- FP32：4 位元組/參數
- FP16：2 位元組/參數
- INT8：1 位元組/參數

這使得可以在相同 GPU 上訓練更大的模型。

## 參考資源

- https://www.google.com/search?q= GPU+memory+management+CUDA+out+of+memory+solutions+2020
- https://www.google.com/search?q=PyTorch+memory+optimization+empty+cache+gradient+checkpointing
- https://www.google.com/search?q=CUDA+memory+hierarchy+global+shared+register+performance