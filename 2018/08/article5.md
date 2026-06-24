# 影像分類實作：ResNet

## 1. ResNet 核心概念

ResNet（Residual Network）在 2015 年提出，通過殘差連接解決深層網路的梯度消失問題。

### 殘差區塊

```python
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels,
                               kernel_size=3, stride=stride, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels,
                               kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)

        # 捷徑（Shortcut）
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels,
                         kernel_size=1, stride=stride),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = torch.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)  # 殘差連接
        out = torch.relu(out)
        return out
```

### 完整 ResNet

```python
class ResNet(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.in_channels = 64

        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.layer1 = self._make_layer(64, 2, stride=1)
        self.layer2 = self._make_layer(128, 2, stride=2)
        self.layer3 = self._make_layer(256, 2, stride=2)
        self.layer4 = self._make_layer(512, 2, stride=2)
        self.fc = nn.Linear(512, num_classes)

    def _make_layer(self, out_channels, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(ResidualBlock(self.in_channels, out_channels, stride))
            self.in_channels = out_channels
        return nn.Sequential(*layers)

    def forward(self, x):
        out = torch.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = nn.functional.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out
```

## 2. 使用預訓練模型

```python
from torchvision import models

# 載入預訓練 ResNet-18
resnet = models.resnet18(pretrained=True)

# 修改最後分類層（10 類）
num_features = resnet.fc.in_features
resnet.fc = nn.Linear(num_features, 10)
```

## 3. 訓練流程

```python
import torchvision.transforms as transforms
from torch.optim import lr_scheduler

# 資料增強
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# 損失函數和優化器
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(resnet.parameters(), lr=0.001)

# 學習率排程
exp_lr_scheduler = lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

# 訓練
for epoch in range(50):
    train_one_epoch()
    exp_lr_scheduler.step()
    validate()
```

## 4. 小結

ResNet 的殘差連接是深度學習的重大突破，使得訓練數百層的網路成為可能，在 2018 年已成為影像分類的標準骨幹架構。

---

**參考資料**
- [ResNet Paper](https://www.google.com/search?q=ResNet+deep+residual+learning+paper)
- [ResNet in PyTorch](https://www.google.com/search?q=ResNet+PyTorch+implementation+tutorial)