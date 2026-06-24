# 主題三：EfficientNet 與模型效率

## 複合縮放的智慧

### 1. 模型效率的重要性

深度神經網路在各種任務上取得了巨大成功，但代價是巨大的計算成本。EfficientNet 提出的複合縮放策略，在效率和效能之間找到了更好的平衡。

### 2. 複合縮放策略

傳統方法通常只縮放網路的一個維度（深度、寬度或解析度）。EfficientNet 提出同時縮放三個維度：

```python
def get_efficientnet_config(scale_coef):
    """EfficientNet-B0 基於複合係數的配置"""
    base_config = {
        'width_coef': 1.0,
        'depth_coef': 1.0,
        'resolution': 224
    }

    scale_coefs = {
        'b0': (1.0, 1.0, 224),
        'b1': (1.0, 1.1, 240),
        'b2': (1.1, 1.2, 260),
        'b3': (1.2, 1.4, 300),
        'b4': (1.4, 1.8, 380),
        'b5': (1.6, 2.2, 456),
        'b6': (1.8, 2.6, 528),
        'b7': (2.0, 3.1, 600),
    }

    return scale_coefs.get(scale_coef, scale_coefs['b0'])
```

**維度解釋**：
- **深度（d）**：層數增加
- **寬度（w）**：通道數增加
- **解析度（r）**：輸入圖像解析度增加

### 3. 複合縮放的原則

EfficientNet 使用以下公式來複合縮放：

```
depth: d^α
width: w^β
resolution: r^γ

subject to: α × β × γ ≈ 1
α = β = γ = 1.2
```

### 4. MobileNet 的深度可分離卷積

MobileNet 是另一個重要的效率優化方向：

```python
class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.depthwise = nn.Conv2d(
            in_channels, in_channels, 3, stride, 1,
            groups=in_channels
        )
        self.pointwise = nn.Conv2d(in_channels, out_channels, 1)

    def forward(self, x):
        x = self.depthwise(x)
        x = self.pointwise(x)
        return x
```

**計算節省**：
- 標準卷積：DK × DK × M × N
- 深度可分離卷積：DK × DK × M + M × N
- 約減少 8-9 倍計算量

### 5. EfficientNet-B0 架構

```python
class EfficientNetB0(nn.Module):
    def __init__(self, num_classes=1000):
        super().__init__()
        self.stem = nn.Sequential(
            nn.Conv2d(3, 32, 3, 2, 1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True)
        )

        self.blocks = nn.Sequential(
            MBConvBlock(32, 16, 1, 1),
            MBConvBlock(16, 24, 6, 2),
            MBConvBlock(24, 40, 6, 2),
            MBConvBlock(40, 80, 6, 2),
            MBConvBlock(80, 112, 6, 1),
            MBConvBlock(112, 192, 6, 2),
            MBConvBlock(192, 320, 6, 1),
        )

        self.head = nn.Sequential(
            nn.Conv2d(320, 1280, 1),
            nn.BatchNorm2d(1280),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(1280, num_classes)
        )

    def forward(self, x):
        x = self.stem(x)
        x = self.blocks(x)
        x = self.head(x)
        return x
```

### 6. EfficientNet 系列

| 模型 | Top-1 準確率 | 參數量 | FLOPS |
|------|-------------|--------|-------|
| B0 | 77.1% | 5.3M | 390M |
| B1 | 79.1% | 7.8M | 700M |
| B3 | 81.6% | 12M | 1.8B |
| B5 | 83.3% | 30M | 9.9B |
| B7 | 84.4% | 66M | 37B |

### 7. 效率優化的影響

EfficientNet 的思想影響深遠：
- 催生了更多高效架構
- 推動了行動裝置上的深度學習
- 為大型模型的效率優化提供方向

---

## 延伸閱讀

- [EfficientNet 論文](https://www.google.com/search?q=EfficientNet+convolutional+neural+networks+compound+scaling)
- [MobileNet 論文](https://www.google.com/search?q=MobileNets+efficient+convolutional+neural+networks)
- [神經架構搜尋](https://www.google.com/search?q=neural+architecture+search+NAS)