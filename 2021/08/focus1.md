# 主題一：CNN 的崛起與發展

## AlexNet 到 ResNet

### 1. 深度學習的起點：AlexNet

2012 年，Alex Krizhevsky、Ilya Sutskever 和 Geoffrey Hinton 設計的 AlexNet 在 ImageNet 競賽中取得突破性成果：

- Top-5 錯誤率：15.3%（第二名 26.2%）
- 8 層網路
- 使用 ReLU 激活函數
- 使用 GPU 加速訓練
- 使用 Dropout 防止過擬合

```python
class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super().__init__()
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
```

### 2. VGGNet：更深更簡單

2014 年，VGGNet 提出更簡單的網路架構：

- 使用 3x3 卷積核替代大卷積核
- 網路深度增加到 16-19 層
- 結構簡單、效能優異

```python
class VGG(nn.Module):
    def __init__(self, configs, num_classes=1000):
        super().__init__()
        layers = []
        in_channels = 3

        for config in configs:
            if config == 'M':
                layers.append(nn.MaxPool2d(2, 2))
            else:
                layers.append(nn.Conv2d(in_channels, config, 3, padding=1))
                layers.append(nn.ReLU(inplace=True))
                in_channels = config

        self.features = nn.Sequential(*layers)
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, num_classes),
        )
```

### 3. GoogLeNet：Inception 模組

2014 年，Google 提出 GoogLeNet，引入 Inception 模組：

- 多尺度特徵提取
- 1x1 卷積降維
- 全域平均池化替代全連接層
- 22 層深度

```python
class Inception(nn.Module):
    def __init__(self, in_channels, ch1x1, ch3x3red, ch3x3, ch5x5red, ch5x5, pool_proj):
        super().__init__()
        self.branch1 = nn.Sequential(
            nn.Conv2d(in_channels, ch1x1, 1),
            nn.ReLU(inplace=True)
        )
        self.branch2 = nn.Sequential(
            nn.Conv2d(in_channels, ch3x3red, 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(ch3x3red, ch3x3, 3, padding=1),
            nn.ReLU(inplace=True)
        )
        self.branch3 = nn.Sequential(
            nn.Conv2d(in_channels, ch5x5red, 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(ch5x5red, ch5x5, 5, padding=2),
            nn.ReLU(inplace=True)
        )
        self.branch4 = nn.Sequential(
            nn.MaxPool2d(3, stride=1, padding=1),
            nn.Conv2d(in_channels, pool_proj, 1),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return torch.cat([self.branch1(x), self.branch2(x),
                         self.branch3(x), self.branch4(x)], 1)
```

### 4. CNN 的核心設計原則

**卷積層設計**：
- 小卷積核（3x3）堆疊優於大卷積核
- 1x1 卷積可用於降維和增加非線性
- 適當的 padding 保持空間維度

**池化層**：
- Max Pooling 常用於特徵提取
- Average Pooling 用於整合資訊
- Global Pooling 減少參數

**訓練技巧**：
- Batch Normalization 加速收斂
- Dropout 防止過擬合
- 資料增強提高泛化能力

### 5. CNN 的局限性

隨著網路深度增加，傳統 CNN 面臨挑戰：
- 梯度消失/爆炸
- 訓練困難
- 計算成本高

這些問題催生了 ResNet 的殘差學習。

---

## 延伸閱讀

- [AlexNet 論文](https://www.google.com/search?q=AlexNet+ImageNet+classification+deep+convolutional)
- [VGGNet 論文](https://www.google.com/search?q=VGG+very+deep+convolutional+networks)
- [GoogLeNet+Inception](https://www.google.com/search?q=GoogLeNet+inception+deep+convolutional)