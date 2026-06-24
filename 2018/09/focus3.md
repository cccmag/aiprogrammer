# 經典架構：VGG、GoogLeNet、ResNet

## 1. VGGNet（2014）

### 設計理念

VGG 的核心思想是使用小卷積核（3x3）堆疊多層，取代大卷積核。

```python
# VGG-16 完整結構
def vgg16():
    model = Sequential([
        # Block 1
        Conv2D(64, (3, 3), padding='same', activation='relu', input_shape=(224, 224, 3)),
        Conv2D(64, (3, 3), padding='same', activation='relu'),
        MaxPooling2D((2, 2)),

        # Block 2
        Conv2D(128, (3, 3), padding='same', activation='relu'),
        Conv2D(128, (3, 3), padding='same', activation='relu'),
        MaxPooling2D((2, 2)),

        # Block 3
        Conv2D(256, (3, 3), padding='same', activation='relu'),
        Conv2D(256, (3, 3), padding='same', activation='relu'),
        Conv2D(256, (3, 3), padding='same', activation='relu'),
        MaxPooling2D((2, 2)),

        # Block 4
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        MaxPooling2D((2, 2)),

        # Block 5
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        Conv2D(512, (3, 3), padding='same', activation='relu'),
        MaxPooling2D((2, 2)),

        # 全連接層
        Flatten(),
        Dense(4096, activation='relu'),
        Dropout(0.5),
        Dense(4096, activation='relu'),
        Dropout(0.5),
        Dense(1000, activation='softmax')
    ])
    return model
```

### 小卷積核的優勢

| 設定 | 3 層 3x3 vs 1 層 7x7 |
|------|-----------------------|
| 感受野 | 相同（7x7） |
| 參數（假設 C） | 3 × (3×3×C×C) = 27C² |
| 參數（單層 7x7） | 7×7×C×C = 49C² |
| 非線性激活 | 3 層 ReLU vs 1 層 |

## 2. GoogLeNet / Inception（2014）

### Inception 模組

```python
from keras.layers import Conv2D, MaxPooling2D, Concatenate

def inception_module(x, filters_1x1, filters_3x3_reduce,
                     filters_3x3, filters_5x5_reduce, filters_5x5,
                     pool_proj):
    # 分支 1：1x1 卷積
    branch1 = Conv2D(filters_1x1, (1, 1), padding='same', activation='relu')(x)

    # 分支 2：1x1 -> 3x3
    branch2 = Conv2D(filters_3x3_reduce, (1, 1), padding='same', activation='relu')(x)
    branch2 = Conv2D(filters_3x3, (3, 3), padding='same', activation='relu')(branch2)

    # 分支 3：1x1 -> 5x5
    branch3 = Conv2D(filters_5x5_reduce, (1, 1), padding='same', activation='relu')(x)
    branch3 = Conv2D(filters_5x5, (5, 5), padding='same', activation='relu')(branch3)

    # 分支 4：3x3 pool -> 1x1
    branch4 = MaxPooling2D((3, 3), strides=(1, 1), padding='same')(x)
    branch4 = Conv2D(pool_proj, (1, 1), padding='same', activation='relu')(branch4)

    # 拼接所有分支
    output = Concatenate()([branch1, branch2, branch3, branch4])
    return output
```

### GoogLeNet 結構

```python
# 22 層網路，包含多個 Inception 模組
# 開始：Stem 網路
# 主體：多個 Inception 模組堆疊
# 結束：Average Pooling + FC
```

## 3. ResNet（2015）

### 殘差學習

```python
import torch
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels,
                               kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels,
                               kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        # 捷徑連接
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels,
                         kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = torch.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)  # 殘差連接
        out = torch.relu(out)
        return out
```

### ResNet 變體

| 版本 | 層數 | 參數量 | Top-1 錯誤率 |
|------|------|--------|--------------|
| ResNet-18 | 18 | 11.7M | 30.43% |
| ResNet-34 | 34 | 21.8M | 26.49% |
| ResNet-50 | 50 | 25.6M | 24.01% |
| ResNet-101 | 101 | 44.5M | 22.44% |
| ResNet-152 | 152 | 60.2M | 21.86% |

## 4. 架構比較

| 架構 | 創新年份 | 創新點 | 參數量 |
|------|----------|--------|--------|
| VGG-16 | 2014 | 小卷積核、深網路 | 138M |
| GoogLeNet | 2014 | Inception、并行多尺度 | 5M |
| ResNet-50 | 2015 | 殘差連接 | 25.6M |

## 5. 小結

VGG 的簡單深網路、GoogLeNet 的多尺度並行、ResNet 的殘差連接，都是 CNN 發展史上的重要里程碑，至今仍是研究的基礎。

---

**下一步**：[遷移學習與微調策略](focus4.md)