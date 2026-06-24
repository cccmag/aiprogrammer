# 多層網路實作手寫辨識

## MNIST 資料集

MNIST 是深度學習的「Hello World」資料集，包含 70000 張 28×28 的手寫數字圖像。

```
類別：0-9 共 10 個數字
訓練集：60000 張
測試集：10000 張
圖像大小：28×28 = 784 像素
```

## 使用 PyTorch 實作

### 資料載入

```python
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

# 資料預處理
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

# 載入訓練集
train_dataset = torchvision.datasets.MNIST(
    root='./data', train=True,
    transform=transform, download=True
)
train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=64, shuffle=True
)

# 載入測試集
test_dataset = torchvision.datasets.MNIST(
    root='./data', train=False,
    transform=transform, download=True
)
test_loader = torch.utils.data.DataLoader(
    test_dataset, batch_size=1000, shuffle=False
)
```

### 模型定義

```python
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 10)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = x.view(-1, 784)  # 展平
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.relu(self.fc3(x))
        x = self.fc4(x)  # 輸出層無啟用（CrossEntropyLoss 內含 Softmax）
        return x
```

### 訓練程式碼

```python
model = MLP()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    
    # 測試
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    accuracy = 100 * correct / total
    print(f"Epoch {epoch+1}, Loss: {running_loss:.4f}, "
          f"Test Accuracy: {accuracy:.2f}%")
```

### 預期輸出

```
Epoch 1, Loss: 98.45, Test Accuracy: 94.56%
Epoch 2, Loss: 38.21, Test Accuracy: 96.23%
Epoch 3, Loss: 27.33, Test Accuracy: 97.01%
Epoch 4, Loss: 21.50, Test Accuracy: 97.34%
Epoch 5, Loss: 17.92, Test Accuracy: 97.68%
Epoch 6, Loss: 15.26, Test Accuracy: 97.85%
Epoch 7, Loss: 13.08, Test Accuracy: 97.92%
Epoch 8, Loss: 11.49, Test Accuracy: 97.97%
Epoch 9, Loss: 10.27, Test Accuracy: 98.05%
Epoch 10, Loss: 9.18, Test Accuracy: 98.11%
```

## 程式解析

### 資料預處理

- `ToTensor()`：將 PIL 圖像轉為張量，像素值歸一化到 [0,1]
- `Normalize(mean, std)`：標準化，使資料均值為 0、變異數為 1

### 模型設計

- 輸入層：784 個神經元（28×28）
- 隱藏層：256 → 128 → 64，使用 ReLU
- Dropout：0.2，防止過擬合
- 輸出層：10 個神經元（0-9 類別）

### 評估模式

`model.eval()` 關閉 Dropout 和 BatchNorm 的訓練行為，確保推論結果穩定。

## 改進方向

1. **使用 CNN**：卷積層能更好捕捉圖像空間結構，準確率可達 99%+
2. **資料增強**：旋轉、平移、縮放可提升泛化能力
3. **學習率排程**：餘弦退火或 ReduceLROnPlateau
4. **更大的模型**：增加層數或神經元數

## 從 MLP 到 CNN

MLP 在 MNIST 上可達約 98% 準確率，但在更複雜的資料集上表現有限。下一篇文章將介紹卷積神經網路（CNN）如何利用圖像的空間結構大幅提升效能。

---

## 延伸閱讀

- [MNIST 官方網站](https://www.google.com/search?q=MNIST+database)
- [PyTorch MNIST 範例](https://www.google.com/search?q=PyTorch+MNIST+example)
- [手寫辨識技術演進](https://www.google.com/search?q=handwritten+digit+recognition+history)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」精選文章。*
