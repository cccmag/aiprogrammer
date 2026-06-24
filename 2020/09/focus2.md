# ResNet 與深度網路的突破

## 2015 年：解決深度網路訓練難題

### 歷史背景

2015 年，He 等人提出了 ResNet（Residual Network），解決了深層網路訓練的梯度消失問題，並在 ImageNet 比賽中獲得冠軍。

### 核心問題：為何深度網路難以訓練？

隨著網路加深，出現了：

1. **梯度消失/爆炸**：反向傳播時梯度趨近於 0 或無窮大
2. **退化問題**：更深層的網路反而具有更高的訓練誤差

### 解決方案：殘差連接

```
輸出 = F(x) + x

其中 F(x) 是學習的殘差映射
```

---

## 一、殘差區塊

### 結構

```
輸入 x
  │
  ├──→ 主分支：卷積 -> BN -> ReLU -> 卷積 -> BN ──┐
  │                                               │
  └─→ 捷徑連接：identity ──────────────────────────┤
                                                 │
                                                 ↓
                                               輸出
```

### 公式

```
y = F(x, {W_i}) + x

如果 F 的維度與 x 不同：
y = F(x, {W_i}) + W_s * x
```

---

## 二、為何殘差連接有效？

### 1. 梯度流動

在反向傳播時：
```
∂L/∂x = ∂L/∂y * ∂y/∂x
       = ∂L/∂y * (1 + ∂F/∂x)
```

即使 ∂F/∂x 很小，1 + ∂F/∂x 也能確保梯度流動。

### 2. 緩解退化

- 淺層網路可以視為深層網路的一部分
- 額外的層可以學習 identity mapping
- 深層網路至少不應比淺層差

### 3. 特徵重複使用

殘差連接允許淺層特徵直接傳遞到深層，促進特徵重複使用。

---

## 三、ResNet 架構

### 不同深度的配置

| 配置 | 層數 | 50層 | 101層 | 152層 |
|------|------|------|-------|-------|
| Conv1 | 1 | 64 | 64 | 64 |
| Conv2 | 3 | 64, 64, 256 | 64, 64, 256 | 64, 64, 256 |
| Conv3 | 4 | 128, 128, 512 | 128, 128, 512 | 128, 128, 512 |
| Conv4 | 6 | 256, 256, 1024 | 256, 256, 1024 | 256, 256, 1024 |
| Conv5 | 3 | 512, 512, 2048 | 512, 512, 2048 | 512, 512, 2048 |

### Bottleneck 設計

為了解決計算複雜度，ResNet 使用 bottleneck 設計：

```
1x1 conv (reduce) -> 3x3 conv -> 1x1 conv (restore)
```

---

## 四、PyTorch 實作

```python
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out
```

---

## 五、訓練技巧

### 1. 預熱（Warmup）

```python
for epoch in range(warmup_epochs):
    lr = base_lr * (epoch + 1) / warmup_epochs
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr
```

### 2. Label Smoothing

```python
class LabelSmoothingLoss(nn.Module):
    def __init__(self, classes, smoothing=0.1):
        self.smoothing = smoothing
        self.cls = classes

    def forward(self, pred, target):
        confidence = 1.0 - self.smoothing
        smooth_value = self.smoothing / (self.cls - 1)
        one_hot = torch.full_like(pred, smooth_value)
        one_hot.scatter_(1, target.unsqueeze(1), confidence)
        return torch.mean(torch.sum(-one_hot * F.log_softmax(pred, dim=-1), dim=-1))
```

---

## 六、影響與後續發展

### 開啟了更深網路的時代

ResNet 的成功證明了「更深」在適當結構下確實「更好」。

### 衍生變體

| 變體 | 改進 |
|------|------|
| Pre-activation ResNet | BN-ReLU-Conv 順序 |
| SE-ResNet | 加入 SE 模組 |
| ResNeXt | 分組卷積 |
| DenseNet | 密集連接 |

---

**下一步**：[EfficientNet：效率與效能的平衡](focus3.md)

## 延伸閱讀

- [ResNet+deep+residual+learning+2015](https://www.google.com/search?q=ResNet+deep+residual+learning+2015)
- [residual+connection+training+deep+network](https://www.google.com/search?q=residual+connection+training+deep+neural+network)