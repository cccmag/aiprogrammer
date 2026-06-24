# 殘差網路 ResNet

## 深層網路的退化問題

直觀上，網路越深應該表現越好——更多層意味著更強的表示能力。但在實踐中，研究者發現深層網路的訓練誤差反而比淺層網路更高。

```
測試誤差
│
│         淺層網路 ──── 誤差較低
│         深層網路 ──── 誤差較高（退化）
│
│   ╱╲              ╱╲
│  ╱  ╲    ╱╲     ╱  ╲
│ ╱    ╲  ╱  ╲   ╱    ╲
│╱      ╲╱    ╲ ╱      ╲
└─────────────────────────── 訓練輪數
```

這不是過擬合（訓練誤差也更高），而是優化困難——深層網路的梯度難以有效傳播。

## 殘差學習

ResNet（Residual Network）由 Kaiming He 等人在 2015 年提出。核心思想是引入捷徑連接（Skip Connection）：

```
傳統網路：y = F(x)           # 直接學習目標映射
殘差網路：y = F(x) + x       # 學習殘差映射
```

### 為什麼有效？

如果恆等映射（y = x）是最優解，傳統網路需要學習 F(x) = x，而殘差網路只需要學習 F(x) = 0。

學習 F(x) = 0 遠比學習 F(x) = x 容易——只需要將權重推向零即可。

```
傳統網路：學習從 x 到 y 的映射
   x → [Conv] → [BN] → [ReLU] → [Conv] → [BN] → y

殘差網路：學習從 x 到 (y - x) 的映射，再加回 x
   x ──→ [Conv] → [BN] → [ReLU] → [Conv] → [BN] → ──→ ReLU → y
       ↑                                            ↑
       └──────────────── 捷徑連接 ──────────────────┘
```

## ResNet 架構

### 基本單元

```python
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3,
                               stride=stride, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3,
                               padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        
        # 捷徑連接（如果維度不匹配）
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride=stride),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)  # 殘差連接
        out = self.relu(out)
        return out
```

### ResNet-18 結構

```
層名      輸出大小    結構
───────────────────────────
Conv1     112×112    7×7, 64, stride=2
          ─────────────────
Conv2_x   56×56      [3×3, 64] × 2
                     [3×3, 64]
          ─────────────────
Conv3_x   28×28      [3×3, 128] × 2
                     [3×3, 128]
          ─────────────────
Conv4_x   14×14      [3×3, 256] × 2
                     [3×3, 256]
          ─────────────────
Conv5_x   7×7        [3×3, 512] × 2
                     [3×3, 512]
          ─────────────────
FC        1×1        Average Pool, 1000-d fc
```

### 瓶頸結構（ResNet-50/101/152）

對於更深的網路，使用瓶頸（Bottleneck）結構減少計算量：

```
256-d 輸入
    ↓
1×1, 64 conv  （降維）
    ↓
3×3, 64 conv  （卷積）
    ↓
1×1, 256 conv （升維）
    ↓
    + → ReLU
    ↑
捷徑連接
```

## 梯度路徑分析

殘差網路的梯度可以直接通過捷徑連接流回：

```
傳統網路：
dL/dx = dL/dy · dy/dx = dL/dy · F'(x)

殘差網路：
dL/dx = dL/dy · (F'(x) + 1)
      = dL/dy · F'(x) + dL/dy
```

關鍵：梯度 dL/dy 可以直接流回（通過 +1 項），不會被連乘削弱。

## 影響與演進

ResNet 的影響遠超圖像分類：

1. **極深網路成為可能**：ResNet-152（152 層）可以穩定訓練
2. **通用設計模式**：殘差連接被用於所有現代神經網路
3. **推動了多個領域**：檢測、分割、影片理解

### 後續演進

```
ResNet (2015)         — 原始殘差連接
ResNeXt (2017)        — 分組卷積
DenseNet (2017)       — 密集連接
SE-Net (2018)         — 通道注意力
ResNeSt (2020)        — 分組注意力
ConvNeXt (2022)       — 現代化 CNN 設計
```

---

## 延伸閱讀

- [ResNet 論文 2015](https://www.google.com/search?q=Deep+Residual+Learning+for+Image+Recognition)
- [ResNet 原始碼](https://www.google.com/search?q=ResNet+PyTorch+source+code)
- [殘差連接的可視化理解](https://www.google.com/search?q=residual+connection+visualization+gradient+flow)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」精選文章。*
