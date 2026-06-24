# EfficientNet：效率與效能的平衡

## 2019 年：複合縮放的突破

### 論文資訊

- **標題**：EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks
- **作者**：Mingxing Tan, Quoc V. Le
- **發布**：ICML 2019

---

## 一、為何需要效率？

### 模型規模的問題

| 模型 | 參數量 | FLOPs | Top-1 準確率 |
|------|--------|-------|-------------|
| ResNet-152 | 60M | 11B | 77.8% |
| ResNeXt-101 | 83M | 16B | 78.8% |
| SENet-154 | 115M | 21B | 81.2% |

更大的模型需要更多計算資源，但效益邊際遞減。

### 行動裝置的需求

在邊緣設備上部署模型需要：
- 低延遲
- 低功耗
- 小記憶體

---

## 二、複合縮放（Compound Scaling）

### 傳統方法的問題

| 方法 | 問題 |
|------|------|
| 僅增加深度 | 梯度消失 |
| 僅增加寬度 | 過擬合 |
| 僅增加解析度 | 計算量增長過快 |

### 複合縮放策略

EfficientNet 提出同時縮放三個維度：

```
深度 d: 網路層數
寬度 w: 每層的通道數
解析度 r: 輸入圖像解析度
```

約束條件：
```
d * w^2 * r^2 ≈ k
```

其中 k 是目標計算預算。

### 縮放公式

```
depth: d = α^φ
width: w = β^φ
resolution: r = γ^φ

約束: α * β^2 * γ^2 ≈ 2
α ≥ 1, β ≥ 1, γ ≥ 1
φ 控制資源使用
```

預設：α=1.2, β=1.1, γ=1.15

---

## 三、EfficientNet 架構

### MBConv 模組

```python
class MBConv(nn.Module):
    def __init__(self, in_channels, out_channels, expand_ratio=1):
        super().__init__()
        self.expand_ratio = expand_ratio
        mid_channels = in_channels * expand_ratio

        self.expand = nn.Conv2d(in_channels, mid_channels, 1) if expand_ratio > 1 else nn.Identity()
        self.depthwise_conv = nn.Conv2d(mid_channels, mid_channels, 3, padding=1, groups=mid_channels)
        self.se = SqueezeExcitation(mid_channels, int(in_channels * 0.25))
        self.project = nn.Conv2d(mid_channels, out_channels, 1)

    def forward(self, x):
        x = self.expand(x)
        x = self.depthwise_conv(x)
        x = F.silu(x)  # SiLU/Swish
        x = self.se(x)
        x = self.project(x)
        return x
```

### Squeeze-and-Excitation

```python
class SqueezeExcitation(nn.Module):
    def __init__(self, channels, reduction=4):
        super().__init__()
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channels, channels // reduction),
            nn.SiLU(),
            nn.Linear(channels // reduction, channels),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)
```

---

## 四、EfficientNet 系列

| 模型 | 參數量 | FLOPs | Top-1 |
|------|--------|-------|-------|
| B0 | 5.3M | 0.39B | 77.1% |
| B1 | 7.8M | 0.70B | 79.1% |
| B2 | 9.2M | 1.0B | 80.1% |
| B3 | 12M | 1.8B | 81.6% |
| B4 | 19M | 4.2B | 82.6% |
| B5 | 30M | 9.9B | 83.3% |
| B6 | 43M | 19B | 83.8% |
| B7 | 66M | 39B | 84.0% |

---

## 五、與其他模型比較

| 模型 | 參數量 | FLOPs | Top-1 |
|------|--------|-------|-------|
| ResNet-50 | 26M | 4B | 76.2% |
| DenseNet-169 | 14M | 3B | 77.2% |
| **EfficientNet-B3** | 12M | 1.8B | **81.6%** |

EfficientNet-B3 在更少參數和計算的情況下，達到了更好的效能。

---

## 六、使用方法

### PyTorch

```python
import torchvision.models as models

model = models.efficientnet_b3(pretrained=True)
```

### TensorFlow/Keras

```python
from tensorflow.keras import applications
model = applications.EfficientNetB3(weights='imagenet')
```

---

## 七、實際應用

### 遷移學習

```python
model = EfficientNet.from_pretrained('efficientnet-b0')
model.classifier = nn.Linear(1280, num_classes)
```

### 模型量化

```python
model = torch.quantization.quantize_dynamic(
    model,
    {nn.Linear, nn.Conv2d},
    dtype=torch.qint8
)
```

---

**下一步**：[Vision Transformer (ViT) 的興起](focus4.md)

## 延伸閱讀

- [EfficientNet+compound+scaling+ICML+2019](https://www.google.com/search?q=EfficientNet+compound+scaling+ICML+2019)
- [EfficientNet+b0+b3+accuracy+efficiency](https://www.google.com/search?q=EfficientNet+b0+b3+accuracy+efficiency)