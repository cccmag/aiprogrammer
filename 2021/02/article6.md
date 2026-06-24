# 卷積神經網路實務

## CNN 基礎架構

```
輸入 → 卷積 → 池化 → 卷積 → 池化 → 全連接 → 輸出
```

## 設計要點

### 1. 卷積層設計

```python
nn.Conv2d(
    in_channels=3,      # RGB=3
    out_channels=32,    # 特徵圖數量
    kernel_size=3,      # 或 (3, 3)
    stride=1,           # 步長
    padding=1           # 保持尺寸
)
```

### 2. 殘差連接

```python
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, padding=1)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1)

    def forward(self, x):
        residual = x
        out = F.relu(self.conv1(x))
        out = self.conv2(out)
        out += residual  # 殘差連接
        return F.relu(out)
```

## 經典架構比較

| 架構 | 年份 | 創新 |
|------|------|------|
| AlexNet | 2012 | 深度 CNN、ReLU |
| VGG | 2014 | 3×3 卷積堆疊 |
| ResNet | 2015 | 殘差連接 |

## 實用技巧

- **使用 1×1 卷積降維**
- **BatchNorm 加速收斂**
- **預訓練模型遷移學習**

---

## 延伸閱讀

- [CNN 設計原則](https://www.google.com/search?q=CNN+design+principles+PyTorch)
- [ResNet+實作](https://www.google.com/search?q=ResNet+implementation+PyTorch)
- [影像分類實戰](https://www.google.com/search?q=image+classification+PyTorch+tutorial)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*