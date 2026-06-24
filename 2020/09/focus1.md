# CNN 的基礎與經典架構

## 前言

卷積神經網路（CNN）是電腦視覺的基石。自 1998 年 LeNet 起，CNN 經歷了多次突破性進展。

---

## 一、卷積操作

### 什麼是卷積？

卷積是一種用於提取圖像特徵的運算：

```
輸入圖像 (H x W x C)
     +
卷積核 (K x K x C)
     ↓
輸出特徵圖
```

### 卷積的幾何意義

| 運算 | 作用 |
|------|------|
| 邊緣檢測 | 提取物體邊界 |
| 模糊 | 平滑圖像 |
| 銳化 | 增強細節 |

### 關鍵參數

| 參數 | 說明 |
|------|------|
| Kernel size | 卷積核大小（如 3x3） |
| Stride | 移動步長 |
| Padding | 邊緣填充 |
| Dilation | 空隙採樣 |

---

## 二、經典架構

### LeNet (1998)

LeCun 等人設計，是首個成功的 CNN：

```
輸入(32x32) -> C1(6, 5x5) -> S2 -> C3(16, 5x5) -> S4 -> C5(120) -> F6(84) -> 輸出
```

### AlexNet (2012)

Krizhevsky 等人在 ImageNet 競賽中獲勝，深度學習開始蓬勃：

| 創新 | 說明 |
|------|------|
| ReLU 激活 | 更快的訓練 |
| Dropout | 防止過擬合 |
| GPU 訓練 | 加速計算 |
| 資料增強 | 增加訓練樣本 |

### VGGNet (2014)

Simonyan 和 Zisserman 展示了「更深更好」：

```
VGG-16:
輸入 -> 2xConv(64) -> Pool -> 2xConv(128) -> Pool ->
       3xConv(256) -> Pool -> 3xConv(512) -> Pool ->
       3xConv(512) -> Pool -> FC(4096) -> FC(4096) -> FC(1000)
```

### 經典架構比較

| 模型 | 年份 | 層數 | Top-5 錯誤率 |
|------|------|------|-------------|
| AlexNet | 2012 | 8 | 16.4% |
| VGG-16 | 2014 | 16 | 7.3% |
| GoogLeNet | 2014 | 22 | 6.7% |
| VGG-19 | 2014 | 19 | 7.3% |

---

## 三、核心組件

### 1. 卷積層

```python
# PyTorch 語法
conv = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, stride=1, padding=1)
```

### 2. 池化層

```python
# 最大池化
pool = nn.MaxPool2d(kernel_size=2, stride=2)

# 平均池化
pool = nn.AvgPool2d(kernel_size=2, stride=2)
```

### 3. 激活函數

```python
# ReLU
x = F.relu(x)

# Leaky ReLU
x = F.leaky_relu(x, negative_slope=0.01)
```

### 4. 全連接層

```python
# 將特徵圖展平
x = x.view(x.size(0), -1)
# 全連接
x = F.linear(x, weight, bias)
```

---

## 四、PyTorch 實作經典 CNN

```python
import torch.nn as nn

class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
```

---

## 五、訓練技巧

### 資料增強

```python
transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ColorJitter(brightness=0.2),
    transforms.ToTensor(),
])
```

### 學習率調整

```python
# Step decay
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

# Cosine annealing
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)
```

---

**下一步**：[ResNet 與深度網路的突破](focus2.md)

## 延伸閱讀

- [LeNet+AlexNet+VGG+CNN+history](https://www.google.com/search?q=LeNet+AlexNet+VGG+CNN+history+deep+learning)
- [convolutional+neural+network+tutorial+vision](https://www.google.com/search?q=convolutional+neural+network+tutorial+computer+vision)