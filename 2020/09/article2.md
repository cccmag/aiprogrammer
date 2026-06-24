# PyTorch 電腦視覺入門

## 前言

PyTorch 是目前最流行的深度學習框架之一。本文介紹如何使用 PyTorch 進行電腦視覺任務。

---

## 一、環境設定

```bash
pip install torch torchvision
```

---

## 二、資料載入

### 使用 torchvision.datasets

```python
import torch
import torchvision
from torch.utils.data import DataLoader

# 載入 MNIST
train_dataset = torchvision.datasets.MNIST(
    root='./data',
    train=True,
    transform=torchvision.transforms.ToTensor(),
    download=True
)

test_dataset = torchvision.datasets.MNIST(
    root='./data',
    train=False,
    transform=torchvision.transforms.ToTensor()
)

# DataLoader
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
```

### 自訂資料集

```python
from torch.utils.data import Dataset

class CustomImageDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx])
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label
```

---

## 三、建立模型

### 簡單 CNN

```python
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # 28 -> 14
        x = self.pool(F.relu(self.conv2(x)))  # 14 -> 7
        x = x.view(-1, 64 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x
```

### 使用預訓練模型

```python
import torchvision.models as models

# 載入預訓練 ResNet
model = models.resnet18(pretrained=True)

# 修改最後一層
model.fc = nn.Linear(model.fc.in_features, num_classes)
```

---

## 四、訓練迴圈

```python
import torch.optim as optim

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = SimpleCNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 10

for epoch in range(num_epochs):
    running_loss = 0.0
    correct = 0
    total = 0

    for i, (images, labels) in enumerate(train_loader):
        images, labels = images.to(device), labels.to(device)

        # 前向傳播
        outputs = model(images)
        loss = criterion(outputs, labels)

        # 反向傳播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    print(f'Epoch {epoch+1}: Loss={running_loss/len(train_loader):.4f}, '
          f'Accuracy={100*correct/total:.2f}%')
```

---

## 五、驗證與測試

```python
def evaluate(model, test_loader, device):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    accuracy = 100 * correct / total
    print(f'Test Accuracy: {accuracy:.2f}%')
    return accuracy

evaluate(model, test_loader, device)
```

---

## 六、模型保存與載入

```python
# 保存
torch.save(model.state_dict(), 'model.pth')

# 載入
model = SimpleCNN()
model.load_state_dict(torch.load('model.pth'))
model.eval()
```

---

## 七、使用 GPU

```python
# 檢查 GPU
print(f"GPU available: {torch.cuda.is_available()}")

# 移動到 GPU
model = model.to('cuda')

# 訓練時確保資料在同一設備
images = images.to('cuda')
labels = labels.to('cuda')
```

---

## 結語

PyTorch 提供了完整的電腦視覺工具鏈。從資料載入、模型建立、訓練到部署，都有良好的支援。建議讀者動手實踐這些範例。

---

*延伸閱讀：[PyTorch+vision+tutorial+2020](https://www.google.com/search?q=PyTorch+vision+tutorial+2020)*