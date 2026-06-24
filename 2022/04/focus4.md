# DataLoader 與資料管線

## Dataset 抽象

PyTorch 的 `torch.utils.data.Dataset` 是一個抽象類別，定義了資料集的基本介面。任何自訂資料集只要實作 `__len__` 與 `__getitem__` 兩個方法即可使用 DataLoader。

```python
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, data, targets):
        self.data = data
        self.targets = targets

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.targets[idx]
```

## TensorDataset 與 DataLoader

對於已經存在記憶體中的資料，`TensorDataset` 提供了最簡單的包裝方式：

```python
from torch.utils.data import TensorDataset, DataLoader

dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=32, shuffle=True)
```

## DataLoader 的關鍵參數

- **batch_size**：每個 batch 的樣本數
- **shuffle**：是否在每個 epoch 開始時打亂資料
- **num_workers**：資料載入的子程序數量（加速 I/O）
- **pin_memory**：啟用頁面鎖定記憶體，加速 CPU→GPU 傳輸
- **drop_last**：若最後一個 batch 不足，是否捨棄

## Map-Style vs Iterable-Style

- **Map-Style Dataset**：透過索引隨機存取（最常用）
- **Iterable-Style Dataset**：繼承 `IterableDataset`，適合串流資料或無法隨機存取的情況

## 資料轉換與擴增

透過 `torchvision.transforms` 可以將資料預處理整合到 Dataset 中：

```python
from torchvision import transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,)),
])
```

## 批次取樣器

`Sampler` 類別控制了 batch 的組成方式：
- **RandomSampler**：隨機取樣（shuffle=True 時的預設值）
- **SequentialSampler**：順序取樣
- **WeightedRandomSampler**：加權隨機取樣，處理類別不平衡

## 參考資料

- DataLoader 文件：https://pytorch.org/docs/stable/data.html
- TorchData 函式庫：https://github.com/pytorch/data
- torchvision.transforms：https://pytorch.org/vision/stable/transforms.html
