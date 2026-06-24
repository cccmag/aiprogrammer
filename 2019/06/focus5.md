# 資料處理

## Dataset、DataLoader、transforms

PyTorch 提供完整的資料處理工具鏈。

---

## Dataset

### 自定義 Dataset

```python
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

dataset = MyDataset(data, labels)
sample = dataset[0]  # (data[0], labels[0])
```

### 常用內建 Dataset

```python
from torchvision import datasets

# 影像 dataset
mnist = datasets.MNIST(root='./data', train=True, download=True)
cifar10 = datasets.CIFAR10(root='./data', train=False, download=True)
imagenet = datasets.ImageNet(root='./data', split='train')
```

---

## DataLoader

```python
from torch.utils.data import DataLoader

dataloader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,         # 隨機打亂
    num_workers=4,       # 多程序載入
    pin_memory=True,     # 加速 GPU 傳輸
    drop_last=True       # 舍棄最後一個不完整 batch
)

for batch_data, batch_labels in dataloader:
    # batch_data: (32, ...) 批次大小
    # batch_labels: (32,)
    pass
```

---

## transforms

```python
from torchvision import transforms

# 影像 transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# 套用 transform
dataset = datasets.CIFAR10(root='./data', transform=transform)
```

### 常見 transforms

```python
# 影像處理
transforms.Resize((224, 224))      # 調整大小
transforms.RandomCrop(224)        # 隨機裁剪
transforms.RandomHorizontalFlip()  # 水平翻轉
transforms.RandomRotation(10)      # 隨機旋轉

# 張量轉換
transforms.ToTensor()              # 轉為張量
transforms.Normalize(mean, std)    # 正規化

# 資料增強
transforms.ColorJitter(brightness=0.2)  # 亮度
transforms.RandomGrayscale()           # 隨機灰階
```

---

## 實用範例

```python
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 準備訓練資料
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

train_dataset = datasets.ImageFolder(
    root='./data/train',
    transform=train_transform
)

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4
)

# 訓練迴圈中使用
for images, labels in train_loader:
    images = images.to(device)
    labels = labels.to(device)
    # 訓練...
```

---

## 延伸閱讀

- [PyTorch DataLoader 文檔](https://www.google.com/search?q=pytorch+dataloader+tutorial)
- [torchvision transforms](https://www.google.com/search?q=torchvision+transforms+tutorial)

---

*本篇文章為「AI 程式人雜誌 2019 年 6 月號」系列文章之一。*