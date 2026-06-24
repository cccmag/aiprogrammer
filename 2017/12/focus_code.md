# 深度學習發展時間線：從 2012 到 2017

## 前言

2012 年 AlexNet 的成功點燃了深度學習革命的導火線。從那時起，深度學習經歷了爆發式成長。本篇文章回顧從 2012 到 2017 年的重要里程碑。

---

## 原始碼

完整的 Python 實作請參考：[_code/deep_learning_timeline.py](_code/deep_learning_timeline.py)

```python
#!/usr/bin/env python3
"""Deep Learning Timeline 2012-2017"""

import torch
import torch.nn as nn
import matplotlib.pyplot as plt

def show_timeline():
    print("Deep Learning Timeline: 2012-2017")
    print("=" * 50)

    milestones = [
        ("2012", "AlexNet", "深度學習復興，ImageNet 錯誤率從 26% 降至 15%"),
        ("2013", "OverFeat", "統一的物體檢測、分類、定位框架"),
        ("2014", "VGGNet", "更深網路(16-19層)，簡單架構"),
        ("2014", "GAN", "生成對抗網路誕生"),
        ("2014", "Inception", "GoogLeNet，稀疏結構"),
        ("2015", "ResNet", "152層，殘差學習，ImageNet錯誤率3.6%"),
        ("2015", "Batch Norm", "加速訓練，穩定梯度"),
        ("2016", "YOLO", "即時物體檢測"),
        ("2016", "DenseNet", "密集連接，每層與所有層相連"),
        ("2017", "Transformer", "純注意力機制，超越 RNN"),
        ("2017", "AlphaGo Zero", "從零學習，超越所有人類知識"),
    ]

    print("\n重要里程碑:")
    for year, name, desc in milestones:
        print(f"\n{year}: {name}")
        print(f"  {desc}")

    print("\n" + "=" * 50)
    print("Key Observations:")
    print("1. 網路深度大幅增加 (8 → 152+ layers)")
    print("2. 錯誤率持續下降 (26% → 3.6%)")
    print("3. 新任務不斷拓展 (分類 → 檢測 → 生成)")
    print("4. 框架生態成熟 (TensorFlow, PyTorch)")
    print("\nDemo completed!")

def compare_architectures():
    print("\nArchitecture Comparison (2012-2017):")
    print("-" * 50)

    # AlexNet style
    class AlexNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(3, 96, 11, stride=4),
                nn.ReLU(),
                nn.MaxPool2d(3, stride=2),
                nn.Conv2d(96, 256, 5, padding=2),
                nn.ReLU(),
                nn.MaxPool2d(3, stride=2),
                nn.Conv2d(256, 384, 3, padding=1),
                nn.ReLU(),
                nn.Conv2d(384, 384, 3, padding=1),
                nn.ReLU(),
                nn.Conv2d(384, 256, 3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(3, stride=2),
            )
            self.classifier = nn.Linear(256 * 5 * 5, 4096)
            self.fc2 = nn.Linear(4096, 4096)
            self.fc3 = nn.Linear(4096, 1000)

    # ResNet style (simplified)
    class BasicBlock(nn.Module):
        def __init__(self, in_channels, out_channels, stride=1):
            super().__init__()
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
            out = torch.relu(self.bn1(self.conv1(x)))
            out = self.bn2(self.conv2(out))
            out += self.shortcut(x)
            out = torch.relu(out)
            return out

    print("\nAlexNet (2012):")
    print("  - 8 layers")
    print("  - 60M parameters")
    print("  - 3x11, 5x5, 3x3 convolutions")
    print("  - Max pooling throughout")

    print("\nResNet (2015):")
    print("  - 152 layers (ResNet-152)")
    print("  - Residual connections")
    print("  - Batch normalization")
    print("  - Global average pooling")

    print("\n" + "=" * 50)

def demo():
    show_timeline()
    compare_architectures()

if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
Deep Learning Timeline: 2012-2017
==================================================

重要里程碑:

2012: AlexNet
  深度學習復興，ImageNet 錯誤率從 26% 降至 15%

2013: OverFeat
  統一的物體檢測、分類、定位框架

2014: VGGNet
  更深網路(16-19層)，簡單架構

2014: GAN
  生成對抗網路誕生

2014: Inception
  GoogLeNet，稀疏結構

2015: ResNet
  152層，殘差學習，ImageNet錯誤率3.6%

2015: Batch Norm
  加速訓練，穩定梯度

2016: YOLO
  即時物體檢測

2016: DenseNet
  密集連接，每層與所有層相連

2017: Transformer
  純注意力機制，超越 RNN

2017: AlphaGo Zero
  從零學習，超越所有人類知識

==================================================
Key Observations:
1. 網路深度大幅增加 (8 → 152+ layers)
2. 錯誤率持續下降 (26% → 3.6%)
3. 新任務不斷拓展 (分類 → 檢測 → 生成)
4. 框架生態成熟 (TensorFlow, PyTorch)

Demo completed!
```

---

## 架構演進對比

| 年份 | 模型 | 層數 | ImageNet Top-5 錯誤率 |
|------|------|------|---------------------|
| 2012 | AlexNet | 8 | 15.3% |
| 2013 | ZFNet | 8 | 14.8% |
| 2014 | VGG-16 | 16 | 7.3% |
| 2014 | GoogLeNet | 22 | 6.7% |
| 2015 | ResNet-152 | 152 | 3.6% |
| 2016 | DenseNet-269 | 269 | 3.0% |
| 2017 | SENet | 154 | 2.3% |

---

## 從 AlexNet 到 ResNet

### AlexNet (2012)

```
Input (224x224x3)
  ↓
Conv(11x11, 96) + ReLU + MaxPool(3,2)
  ↓
Conv(5x5, 256) + ReLU + MaxPool(3,2)
  ↓
Conv(3x3, 384) × 2 + ReLU
  ↓
Conv(3x3, 256) + ReLU + MaxPool(3,2)
  ↓
FC(4096) → FC(4096) → FC(1000)
```

### ResNet (2015)

```
Input (224x224x3)
  ↓
Conv(7x7, 64, stride=2)
  ↓
MaxPool(3,2)
  ↓
[Bottleneck × 3]
  ↓
AvgPool(7)
  ↓
FC(1000)
```

關鍵創新：殘差連接允許訓練更深層網路

---

## 結論

2012-2017 年見證了深度學習的黃金時代。從 AlexNet 到 Transformer，從 8 層到 152+ 層，從 15% 到 3.6% 的錯誤率，每一步都是計算機視覺領域的重大進步。

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列補充文章。*