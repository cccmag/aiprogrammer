# ResNet 發布一年：殘差連接的影響

## 前言

ResNet（Deep Residual Learning for Image Recognition）於 2015 年發表，在 2017 年已經成為電腦視覺的標準骨幹架構。本篇文章回顧 ResNet 的影響。

## ResNet 的核心思想

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

        # 捷徑連接
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

## 為什麼殘差連接有效？

```
┌─────────────────────────────────────────────────────────┐
│              殘差學習 vs 直接學習                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  傳統網路:                                             │
│  輸入 ──→ 層1 ──→ 層2 ──→ ... ──→ 輸出                 │
│            │         │                    │            │
│            │         │                    ▼            │
│            │         │              要學習 H(x)         │
│                                                         │
│  殘差網路:                                             │
│  輸入 ──┬──→ 層1 ──→ 層2 ──→ ... ──→ 輸出              │
│         │                                    │          │
│         └────────────────────────────────────┘         │
│                                              │          │
│         捷徑連接 ────────────────────────────┘          │
│                                              │          │
│            要學習 F(x) = H(x) - x (殘差)                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## ResNet 的深遠影響

### 1. 更深的網路

ResNet 讓訓練超過 1000 層的網路成為可能。

### 2. 預訓練模型

幾乎所有現代視覺模型都使用 ResNet 作為骨幹：

- Faster R-CNN
- YOLO (Darknet 是類似的設計)
- SSD

### 3. 遷移學習

ResNet 預訓練模型成為轉移學習的標準起點。

## 後續發展

```
ResNet 變體:
├── ResNeXt (增加 Cardinality)
├── DenseNet (密集連接)
├── Wide ResNet (增加寬度)
└── EfficientNet (複合縮放)
```

## 程式碼示例

```python
# PyTorch 使用 ResNet
import torchvision.models as models

# 載入預訓練 ResNet
resnet = models.resnet50(pretrained=True)

# 修改最後一層
resnet.fc = nn.Linear(2048, num_classes)

# 訓練
for epoch in range(num_epochs):
    for batch in dataloader:
        output = resnet(batch)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
```

---

**延伸閱讀**

- [ResNet Paper (He et al., 2015)](https://www.google.com/search?q=ResNet+He+2015+paper)
- [Deeper Deep Learning](https://www.google.com/search?q=deeper+residual+networks+resnet)

---

*本篇文章為「AI 程式人雜誌 2017 年 11 月號」AI 相關文章之一。*