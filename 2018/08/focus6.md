# DataLoader 與資料處理

## PyTorch 資料管線

### Dataset 抽象

```python
from torch.utils.data import Dataset

class MNISTDataset(Dataset):
    def __init__(self, data, labels, transform=None):
        self.data = data
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img = self.data[idx]
        label = self.labels[idx]

        if self.transform:
            img = self.transform(img)

        return img, label
```

### Transforms

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
```

### DataLoader

```python
from torch.utils.data import DataLoader

train_loader = DataLoader(
    dataset=MNISTDataset(train_data, train_labels, train_transform),
    batch_size=32,
    shuffle=True,
    num_workers=4,
    pin_memory=True,
    drop_last=True
)

for batch_idx, (data, target) in enumerate(train_loader):
    # data: (batch_size, channels, height, width)
    # target: (batch_size,)
    pass
```

### Sampler

```python
from torch.utils.data import Sampler

class ImbalancedDatasetSampler(Sampler):
    def __init__(self, dataset, indices=None):
        self.indices = list(range(len(dataset)))
        # 根據類別分佈給予不同權重
        # ...

    def __iter__(self):
        return (self.indices[i] for i in torch.randint(len(self.indices), (len(self),)))

# 使用
train_loader = DataLoader(dataset, sampler=ImbalancedDatasetSampler(dataset))
```

### 内建資料集

```python
from torchvision import datasets

# MNIST
datasets.MNIST(root='./data', train=True, download=True, transform=transforms.ToTensor())

# CIFAR-10
datasets.CIFAR10(root='./data', train=True, download=True)

# ImageNet
datasets.ImageFolder(root='./imagenet/train', transform=transforms)
```

### 處理大檔案

```python
# 使用 Memory-mapped 檔案處理大資料集
class LargeDataset(Dataset):
    def __init__(self, filename):
        self.data = np.memmap(filename, dtype='float32', mode='r')

    def __getitem__(self, idx):
        return self.data[idx * 784:(idx + 1) * 784]
```

### 多程序資料載入

```python
# num_workers 引數控制子程序數
train_loader = DataLoader(dataset, batch_size=32, num_workers=4)

# pin_memory 加速 CPU 到 GPU 傳輸
train_loader = DataLoader(dataset, batch_size=32, pin_memory=True)

# 建議：num_workers = CPU 核心數 - 1
```

### 小結

PyTorch 的資料載入系統提供了靈活且高效的資料處理能力。正確使用 DataLoader 對於訓練效率至關重要。

---

**下一步**：[PyTorch 預訓練模型庫](focus7.md)