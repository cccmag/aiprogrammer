# ResNet 詳解

## 殘差連接與極深網路

ResNet（Residual Network）由何愷明等人於 2015 年提出，是深度學習領域的里程碑。

---

## 問題：深度網路的退化

### 退化現象

```
訓練誤差不隨網路深度增加而減少，反而增加
- 不是過擬合（訓練和測試誤差都變差）
- 也不是梯度消失（梯度在某些層正常流動）
- 而是網路變得更難訓練
```

### 原因分析

```
網路變深後：
1. 恒等映射（identity mapping）難以學習
2. 每一層都要學習一個新的映射，而不是保留上一層的輸出
```

---

## 解決方案：殘差學習

### 核心思想

```
不要讓每一層直接學習 H(x)，而是學習 F(x) = H(x) - x
x → [F(x)] → (+) → H(x) = F(x) + x
          ↑
      跳躍連接（Shortcut）
```

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

        # 跳躍連接
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels,
                         kernel_size=1, stride=stride),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)  # 殘差連接
        out = F.relu(out)
        return out
```

### 視覺化

```
輸入 x
    │
    ├──→ [Conv → BN → ReLU → Conv → BN] ──→ (+) ──→ ReLU ──→ 輸出
    │                                              ↑
    └──────────────────────────────────────────────┘
                       跳躍連接
```

---

## 為什麼殘差學習有效？

### 1. 簡化優化

```
如果 H(x) = x（恒等映射）
那麼 F(x) = 0 更容易學習

因為網路可以輕鬆地將 F(x) 設置為 0
然後透過跳躍連接輸出 x
```

### 2. 梯度流動

```python
# 梯度可以直接流過跳躍連接
# ∂L/∂x = ∂L/∂H · (1 + ∂F/∂x)
# 解決了梯度消失問題
```

### 3. 特徵重用

```python
# 後面的層可以 reuse 前面的特徵
# 而不是從頭開始學習
```

---

## ResNet 架構

### ResNet-18/34

```python
# 基本殘差區塊（BasicBlock）
class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels,
                               kernel_size=3, stride=stride, padding=1)
        self.conv2 = nn.Conv2d(out_channels, out_channels,
                               kernel_size=3, stride=1, padding=1)

        # 跳躍連接
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride)
            )
        else:
            self.shortcut = nn.Sequential()
```

### ResNet-50/101/152

```python
# 瓶頸殘差區塊（Bottleneck）
class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        # 1x1 減少維度
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1)
        # 3x3 卷積
        self.conv2 = nn.Conv2d(out_channels, out_channels,
                               kernel_size=3, stride=stride, padding=1)
        # 1x1 恢復維度
        self.conv3 = nn.Conv2d(out_channels, out_channels * self.expansion,
                               kernel_size=1)
```

---

## ResNet 配置

| 層 | 輸出尺寸 | ResNet-50 |
|----|---------|----------|
| conv1 | 112x112 | 7x7, 64, stride=2 |
| conv2_x | 56x56 | 3x3 max pool, stride=2 |
| | | [1x1, 64]×3 |
| | | [3x3, 64]×3 |
| | | [1x1, 256]×3 |
| conv3_x | 28x28 | [1x1, 128]×4 |
| | | [3x3, 128]×4 |
| | | [1x1, 512]×4 |
| conv4_x | 14x14 | [1x1, 256]×6 |
| | | [3x3, 256]×6 |
| | | [1x1, 1024]×6 |
| conv5_x | 7x7 | [1x1, 512]×3 |
| | | [3x3, 512]×3 |
| | | [1x1, 2048]×3 |
| | | avg pool, 1000-d fc |

---

## 效能對比

| 模型 | Top-5 錯誤率 | 層數 | 參數 |
|-----|------------|-----|------|
| VGG-19 | 7.4% | 19 | 144M |
| GoogLeNet | 6.7% | 22 | 7M |
| ResNet-34 | 3.6% | 34 | 22M |
| ResNet-50 | 3.1% | 50 | 26M |
| ResNet-101 | 3.0% | 101 | 45M |
| ResNet-152 | 2.7% | 152 | 60M |

---

## 變體

### Pre-activation ResNet

```python
# 將 BN-ReLU 放在 Conv 之前
def forward(self, x):
    out = F.relu(self.bn1(self.conv1(x)))
    out = F.relu(self.bn2(self.conv2(out)))
    out += self.shortcut(x)
    return out
```

### DenseNet 連接

每層都與所有後續層連接：

```python
# DenseNet: H(x) = Conv([x, H1(x), H2(H1(x)), ...])
```

---

## 延伸閱讀

- [ResNet 原始論文](https://www.google.com/search?q=ResNet+He+2015+paper)
- [Deep Residual Learning](https://www.google.com/search?q=deep+residual+learning+for+image+recognition)
- [殘差網路詳解](https://www.google.com/search?q=residual+networks+explained)

---

*本篇文章為「AI 程式人雜誌 2019 年 5 月號」系列文章之一。*