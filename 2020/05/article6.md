# 資料載入優化

## 多進程資料載入

```python
from torch.utils.data import DataLoader

train_loader = DataLoader(
    dataset,
    batch_size=32,
    num_workers=4,  # CPU 核心數
    pin_memory=True,
    persistent_workers=True,  # PyTorch 1.7+
    prefetch_factor=2  # 每個 worker 預取多少批次
)
```

## pin_memory 加速傳輸

```python
# 將資料固定在頁鎖定記憶體，加速 CPU-GPU 傳輸
train_loader = DataLoader(
    dataset,
    batch_size=32,
    pin_memory=True,
    pin_memory_device="cuda:0"  # PyTorch 1.9+
)
```

## 自定義 collate 函數

```python
def custom_collate(batch):
    # 自定義如何將多個樣本組合成批次
    inputs = torch.stack([item[0] for item in batch])
    labels = torch.tensor([item[1] for item in batch])
    return inputs, labels

train_loader = DataLoader(
    dataset,
    batch_size=32,
    collate_fn=custom_collate
)
```

## 記憶體映射

對於大型資料集，使用記憶體映射：

```python
import numpy as np

# NumPy 記憶體映射
data = np.load("dataset.npy", mmap_mode="r")

class MemoryMappedDataset(torch.utils.data.TensorDataset):
    def __init__(self, mmap_data, transform=None):
        self.data = mmap_data
        self.transform = transform
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        x = torch.from_numpy(self.data[idx])
        if self.transform:
            x = self.transform(x)
        return x
```

## 漸進式載入

```python
class StreamingDataset(torch.utils.data.Dataset):
    def __init__(self, file_list):
        self.file_list = file_list
    
    def __len__(self):
        return len(self.file_list)
    
    def __getitem__(self, idx):
        # 每次只載入一個檔案
        data = np.load(self.file_list[idx])
        return torch.from_numpy(data)
```

## 非同步資料載入

```python
from torch.utils.data import DataLoader

# 使用非同步迭代
for batch in DataLoader(dataset, batch_size=32, num_workers=4):
    # 處理批次時，下一個批次已在背景載入
    train_step(batch)
```

## 緩存常用資料

```python
class CachedDataset(torch.utils.data.Dataset):
    def __init__(self, base_dataset, cache_size=1000):
        self.base_dataset = base_dataset
        self.cache = {}
        self.cache_size = cache_size
    
    def __getitem__(self, idx):
        if idx not in self.cache:
            self.cache[idx] = self.base_dataset[idx]
            if len(self.cache) > self.cache_size:
                # 簡單的 FIFO 緩存策略
                self.cache.pop(next(iter(self.cache)))
        return self.cache[idx]
```

## 資料增強優化

```python
# 在 GPU 上執行資料增強
class GPUAugmentation:
    def __call__(self, x):
        # 假設 x 已在 GPU 上
        x = x + torch.randn_like(x) * 0.1  # 添加雜訊
        x = torch.clamp(x, 0, 1)
        return x
```

## 參考資源

- https://www.google.com/search?q=PyTorch+DataLoader+num_workers+pin_memory+performance+tutorial+2020
- https://www.google.com/search?q=dataset+loading+optimization+memory+mapping+caching+streaming
- https://www.google.com/search?q=data+prefetching+GPU+training+DataLoader+async+loading