# 資料集與 DataLoader

## Dataset 介面

```python
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, data_path):
        self.data = self.load_data(data_path)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
```

## 自定義 Dataset

```python
class TextDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        return {
            'text': text,
            'label': label
        }
```

## DataLoader

```python
from torch.utils.data import DataLoader

train_loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,
    pin_memory=True
)

for batch in train_loader:
    inputs = batch['text']
    targets = batch['label']
```

## 實用技巧

### 處理不平衡數據

```python
WeightedRandomSampler
```

### 記憶體效率

```python
# IterableDataset（大型數據）
class StreamingDataset(torch.utils.data.IterableDataset):
    def __iter__(self):
        for line in open('large_file.txt'):
            yield preprocess(line)
```

---

## 延伸閱讀

- [Dataset 官方文檔](https://www.google.com/search?q=PyTorch+Dataset+DataLoader)
- [自定義Dataset教學](https://www.google.com/search?q=custom+dataset+PyTorch+tutorial)
- [DataLoader+效能優化](https://www.google.com/search?q=DataLoader+num_workers+optimization)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*