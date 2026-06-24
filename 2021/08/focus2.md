# 主題二：ResNet 與深度殘差學習

## 解決深度網路訓練問題

### 1. 深度網路的挑戰

隨著網路深度增加，傳統 CNN 面臨嚴重的訓練問題：

**梯度消失/爆炸**：
- 反向傳播時梯度不斷衰減或膨脹
- 底部層难以獲得有效更新

**網路退化**：
- 增加深度後，訓練誤差反而增加
- 並非過擬合，而是優化困難

### 2. 殘差學習的思想

ResNet 的核心創新是殘差連接（Residual Connection）：

```python
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, 1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, 1, 1)
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out
```

**關鍵洞察**：
- 學習殘差 F(x) = H(x) - x 比學習完整映射 H(x) 更容易
- 殘差連接讓梯度直接流向較低層

### 3. ResNet 架構

```python
class ResNet(nn.Module):
    def __init__(self, ResidualBlock, num_blocks, num_classes=1000):
        super().__init__()
        self.in_channels = 64

        self.conv1 = nn.Conv2d(3, 64, 7, 2, 3)
        self.bn1 = nn.BatchNorm2d(64)
        self.maxpool = nn.MaxPool2d(3, 2, 1)

        self.layer1 = self._make_layer(64, 1, num_blocks[0])
        self.layer2 = self._make_layer(128, 2, num_blocks[1])
        self.layer3 = self._make_layer(256, 2, num_blocks[2])
        self.layer4 = self._make_layer(512, 2, num_blocks[3])

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)

    def _make_layer(self, out_channels, stride, num_blocks):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(ResidualBlock(self.in_channels, out_channels, stride))
            self.in_channels = out_channels
        return nn.Sequential(*layers)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x
```

**經典配置**：
- ResNet-18：2 + 2 + 2 + 2 blocks
- ResNet-34：3 + 4 + 6 + 3 blocks
- ResNet-50/101/152：使用 Bottleneck 區塊

### 4. Bottleneck 設計

ResNet-50 及更深的網路使用 Bottleneck 區塊：

```python
class Bottleneck(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels//4, 1)
        self.bn1 = nn.BatchNorm2d(out_channels//4)
        self.conv2 = nn.Conv2d(out_channels//4, out_channels//4, 3, stride, 1)
        self.bn2 = nn.BatchNorm2d(out_channels//4)
        self.conv3 = nn.Conv2d(out_channels//4, out_channels, 1)
        self.bn3 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out
```

### 5. ResNet 的影響

ResNet 的設計思想影響深遠：

**電腦視覺**：
- 成為幾乎所有視覺任務的骨幹網路
- 各種下游任務的標準基礎

**深度學習理論**：
- 殘差連接成為現代網路的標配
- 催生了 DenseNet、SENet 等變體

**跨領域應用**：
- NLP、語音等領域也開始使用殘差連接

### 6. ResNet 的變體

| 模型 | 創新 |
|------|------|
| Pre-act ResNet | 激活函數放在殘差之前 |
| ResNeXt | 引入cardinality 維度 |
| SE-ResNet | 加入通道注意力 |
| EfficientNet | 複合縮放 + ResNet |

---

## 延伸閱讀

- [ResNet 論文](https://www.google.com/search?q=ResNet+deep+residual+learning+image+recognition)
- [Batch Normalization 論文](https://www.google.com/search?q=batch+normalization+going+deeper+networks)
- [殘差網路詳解](https://www.google.com/search?q=residual+networks+tutorial+pytorch)