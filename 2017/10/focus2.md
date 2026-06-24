# DCGAN：深度卷積 GAN 的突破（2015-2016）

## 前言

2014 年的原始 GAN 雖然概念創新，但在實際應用中面臨嚴重的訓練不穩定問題。生成器往往會崩潰，產生模糊或無意義的輸出。這個問題直到 2015-2016 年 DCGAN（Deep Convolutional Generative Adversarial Network）的出現才得到顯著改善。

## DCGAN 的誕生

2015 年，Alec Radford、Luke Metz 和 Soumith Chintala 發表了論文《Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks》，提出了 DCGAN 架構。這是第一個成功將卷積神經網路應用於 GAN 的方案。

## DCGAN 的核心技術

### 架構原則

DCGAN 提出了以下關鍵設計原則：

```
┌─────────────────────────────────────────────────────┐
│               DCGAN 設計原則                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. 移除池化層：使用轉置卷積（Fractional Strided     │
│     Convolutions）替代池化操作                       │
│                                                     │
│  2. Batch Normalization：在生成器和判別器中都使用    │
│     Batch Normalization，穩定訓練                   │
│                                                     │
│  3. 移除全連接層：使用全局池化（Global Pooling）     │
│                                                     │
│  4. Leaky ReLU：判別器使用 Leaky ReLU 激活函數      │
│                                                     │
│  5. ReLU/Tanh：生成器使用 ReLU 輸出，Tanh 激活      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 生成器架構

```
┌─────────────────────────────────────────────────────────┐
│                   DCGAN 生成器架構                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  輸入：100 維噪音向量 Z                                │
│                                                         │
│  ↓ Reshape to 100x1x1                                  │
│                                                         │
│  → ConvTranspose2d(100, 1024, 4, 1, 0)                 │
│  → BatchNorm → ReLU                                    │
│                                                         │
│  → ConvTranspose2d(1024, 512, 4, 2, 1)                 │
│  → BatchNorm → ReLU                                    │
│                                                         │
│  → ConvTranspose2d(512, 256, 4, 2, 1)                  │
│  → BatchNorm → ReLU                                    │
│                                                         │
│  → ConvTranspose2d(256, 128, 4, 2, 1)                  │
│  → BatchNorm → ReLU                                    │
│                                                         │
│  → ConvTranspose2d(128, 3, 4, 2, 1)                    │
│  → Tanh                                                │
│                                                         │
│  輸出：64x64x3 RGB 影像                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 判別器架構

```
┌─────────────────────────────────────────────────────────┐
│                   DCGAN 判別器架構                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  輸入：64x64x3 RGB 影像                                 │
│                                                         │
│  → Conv2d(3, 128, 4, 2, 1)                             │
│  → LeakyReLU(0.2)                                      │
│                                                         │
│  → Conv2d(128, 256, 4, 2, 1)                           │
│  → BatchNorm → LeakyReLU(0.2)                          │
│                                                         │
│  → Conv2d(256, 512, 4, 2, 1)                           │
│  → BatchNorm → LeakyReLU(0.2)                          │
│                                                         │
│  → Conv2d(512, 1024, 4, 2, 1)                          │
│  → BatchNorm → LeakyReLU(0.2)                          │
│                                                         │
│  → Conv2d(1024, 1, 4, 1, 0)                            │
│  → Sigmoid                                             │
│                                                         │
│  輸出：0-1 之間的機率值                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Batch Normalization 的重要性

Batch Normalization 是 DCGAN 成功的關鍵因素之一：

```python
# 沒有 BatchNorm 的問題
# 各層輸入分佈變化（Internal Covariate Shift）
# 導致訓練不穩定

# 有 BatchNorm 的效果
# 對每個 mini-batch 進行標準化
# 層輸入分佈穩定
# 可以使用更高的學習率
```

### BatchNorm 的數學定義

```python
# 對於 mini-batch B = {x1, x2, ..., xm}
# 計算：
#   mean_B = (1/m) * Σ xi
#   var_B = (1/m) * Σ (xi - mean_B)^2
#   x_norm = (xi - mean_B) / sqrt(var_B + ε)
#   y = γ * x_norm + β
```

## 潛在空間的語義特性

DCGAN 最重要的發現之一是潛在空間（Latent Space）具有語義連續性。研究者發現：

### 向量運算

在潛在空間中進行的向量運算可以對應到語義變化：

```
┌─────────────────────────────────────────────────────────┐
│                   潛在空間向量運算                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  戴墨鏡的男人 - 男人 + 女人 = 戴墨鏡的女人               │
│                                                         │
│  [vec(戴墨鏡男人)] - [vec(男人)] + [vec(女人)]          │
│  = vec(戴墨鏡女人)                                      │
│                                                         │
│  Smiling woman - Woman + Man = Smiling man              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 視覺化

研究者使用 t-SNE 將潛在空間視覺化，發現：
- 相似的圖像在潛在空間中聚集
- 沿特定方向移動可以產生語義連續的變化
- 可以進行「面部的年齡漸變」等操作

## DCGAN 的 PyTorch 實現

```python
#!/usr/bin/env python3
"""DCGAN implementation for image generation"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

LATENT_DIM = 100
G_FEATURES = 64
D_FEATURES = 64
IMAGE_channels = 3

class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.ConvTranspose2d(LATENT_DIM, G_FEATURES * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(G_FEATURES * 8),
            nn.ReLU(True),
            nn.ConvTranspose2d(G_FEATURES * 8, G_FEATURES * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(G_FEATURES * 4),
            nn.ReLU(True),
            nn.ConvTranspose2d(G_FEATURES * 4, G_FEATURES * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(G_FEATURES * 2),
            nn.ReLU(True),
            nn.ConvTranspose2d(G_FEATURES * 2, G_FEATURES, 4, 2, 1, bias=False),
            nn.BatchNorm2d(G_FEATURES),
            nn.ReLU(True),
            nn.ConvTranspose2d(G_FEATURES, IMAGE_channels, 4, 2, 1, bias=False),
            nn.Tanh()
        )

    def forward(self, input):
        return self.main(input)

class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.main = nn.Sequential(
            nn.Conv2d(IMAGE_channels, D_FEATURES, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(D_FEATURES, D_FEATURES * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(D_FEATURES * 2),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(D_FEATURES * 2, D_FEATURES * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(D_FEATURES * 4),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(D_FEATURES * 4, D_FEATURES * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(D_FEATURES * 8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(D_FEATURES * 8, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, input):
        return self.main(input).view(-1, 1).squeeze(1)

def demo():
    print("DCGAN Architecture Demo")
    print("=" * 50)

    G = Generator()
    D = Discriminator()

    print("Generator architecture:")
    print(G)
    print()

    print("Discriminator architecture:")
    print(D)
    print()

    noise = torch.randn(4, LATENT_DIM, 1, 1)
    fake_images = G(noise)

    print(f"Input noise shape: {noise.shape}")
    print(f"Generated images shape: {fake_images.shape}")
    print(f"Image value range: [{fake_images.min():.2f}, {fake_images.max():.2f}]")

    output = D(fake_images)
    print(f"Discriminator output shape: {output.shape}")
    print(f"Discriminator output: {output}")

    total_params_G = sum(p.numel() for p in G.parameters())
    total_params_D = sum(p.numel() for p in D.parameters())
    print(f"\nGenerator parameters: {total_params_G:,}")
    print(f"Discriminator parameters: {total_params_D:,}")

    print("\nDemo completed!")

if __name__ == "__main__":
    demo()
```

## DCGAN 的應用

DCGAN 的成功為後續研究開闢了道路：

### 1. 條件生成

將類別標籤作為條件輸入，實現可控生成。

### 2. 影像轉換

結合同一時期的 Pix2Pix 等技術，實現風格轉換。

### 3. 表徵學習

DCGAN 學習到的潛在空間可用於下游任務，如分類、檢索等。

---

## 延伸閱讀

- [Radford et al., 2015: DCGAN Paper](https://www.google.com/search?q=DCGAN+Radford+2015+paper)
- [Convolutional Neural Network](https://www.google.com/search?q=convolutional+neural+network+tutorial)
- [Batch Normalization](https://www.google.com/search?q=batch+normalization+paper)

---

*本篇文章為「AI 程式人雜誌 2017 年 10 月號」 GAN 系列之二。*