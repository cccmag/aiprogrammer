# EfficientNet 背後的設計原則

## 前言

EfficientNet 通过系統性的複合縮放方法，在效率和效能之間達到了最佳平衡。本文深入分析其設計原則。

---

## 一、規模化的挑戰

### 傳統方法的問題

| 方法 | 問題 |
|------|------|
| 僅增加深度 | 梯度消失、訓練複雜度增加 |
| 僅增加寬度 | 過擬合風險增加 |
| 僅增加解析度 | 計算量平方增長 |

### 觀察

- 輸入解析度翻倍，計算量增加 4 倍
- 網路深度翻倍，計算量增加 2 倍
- 網路寬度翻倍，計算量增加 4 倍

---

## 二、複合縮放

### 核心思想

同時且協調地縮放網路的深度、寬度和解析度。

### 約束條件

```
d × w² × r² ≈ k
```

其中 $d$ 是深度放大倍數，$w$ 是寬度放大倍數，$r$ 是解析度放大倍數，$k$ 是目標計算預算。

### 預設配置

EfficientNet-B0 的配置：
- α = 1.2
- β = 1.1  
- γ = 1.15

滿足約束：α × β² × γ² ≈ 2

---

## 三、推導過程

### 步驟 1：網路深度縮放

```
d = α^φ
```

深度增加可以捕捉更豐富、更複雜的特征。

### 步驟 2：網路寬度縮放

```
w = β^φ
```

寬度增加可以捕捉更細節的特徵。

### 步驟 3：輸入解析度縮放

```
r = γ^φ
```

更高的解析度可以捕捉更細節的資訊。

### φ 的控制

- φ = 0：B0 基線
- φ = 1：B1
- φ = 2：B2
- φ = 3：B3
- ...

---

## 四、MBConv 模組

### Mobile Inverted Bottleneck

```python
class MBConv(nn.Module):
    def __init__(self, in_channels, out_channels, expand_ratio=1):
        super().__init__()

        # Expansion (如果 expand_ratio > 1)
        expanded_channels = in_channels * expand_ratio
        if expand_ratio > 1:
            self.expand = nn.Sequential(
                nn.Conv2d(in_channels, expanded_channels, 1),
                nn.BatchNorm2d(expanded_channels),
                nn.SiLU()
            )
        else:
            self.expand = nn.Identity()

        # Depthwise Convolution
        self.depthwise = nn.Sequential(
            nn.Conv2d(expanded_channels, expanded_channels, 3,
                      padding=1, groups=expanded_channels),
            nn.BatchNorm2d(expanded_channels),
            nn.SiLU()
        )

        # Squeeze and Excitation
        self.se = SEBlock(expanded_channels)

        # Projection
        self.project = nn.Sequential(
            nn.Conv2d(expanded_channels, out_channels, 1),
            nn.BatchNorm2d(out_channels)
        )

    def forward(self, x):
        x = self.expand(x)
        x = self.depthwise(x)
        x = self.se(x)
        x = self.project(x)
        return x
```

### 深度可分離卷積

```
標准卷積：3×3 卷積核
深度可分離：(1×1) 擴張 + (3×3) 深度wise + (1×1) 投影
```

節省計算：
```
節省比例 = 1/(K_h × K_w) = 1/9 ≈ 89%
```

---

## 五、Squeeze-and-Excitation

### 機制

```python
class SEBlock(nn.Module):
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
        return x * y
```

### 作用

動態調整每個通道的權重，增強有用通道，抑制無用通道。

---

## 六、效能比較

### ImageNet 結果

| 模型 | 參數量 | FLOPs | Top-1 |
|------|--------|-------|-------|
| ResNet-50 | 26M | 4.1B | 76.2% |
| EfficientNet-B0 | 5.3M | 0.39B | 77.1% |
| EfficientNet-B3 | 12M | 1.8B | 81.6% |

### 效率提升

```
EfficientNet-B0 vs ResNet-50:
- 參數減少 80%
- FLOPs 減少 91%
- 精度提升 0.9%
```

---

## 七、遷移學習效果

EfficientNet 在各種遷移學習任務上表現出色：

```python
# 使用預訓練 EfficientNet
model = torchvision.models.efficientnet_b0(pretrained=True)
model.classifier[1] = nn.Linear(1280, num_classes)
```

---

## 結語

EfficientNet 的成功來自於：
1. 系統性的複合縮放
2. 高效的 MBConv 架構
3. Squeeze-and-Excitation 機制

這提供了一種可擴展且高效的方法來構建高性能視覺模型。

---

*延伸閱讀：[EfficientNet+compound+scaling+design+principles](https://www.google.com/search?q=EfficientNet+compound+scaling+design+principles+ICML+2019)*