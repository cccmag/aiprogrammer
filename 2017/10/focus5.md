# GAN 應用：影像生成與風格轉換

## 前言

GAN 的强大生成能力在影像領域展現得淋漓盡致。從高品質的人物頭像生成，到藝術風格轉換，再到影像修復和超解析度重建，GAN 正在革新我們處理影像的方式。本篇文章將探討 GAN 在影像領域的主要應用。

## 影像生成

### 人物頭像生成

2017 年最受矚目的應用之一是生成逼真的人物頭像。Progressive GAN (ProGAN) 通過逐步增加解析度，實現了 1024x1024 的人臉生成：

```
┌─────────────────────────────────────────────────────────┐
│            Progressive GAN 生長過程                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Stage 1: 4x4     Stage 2: 8x8    Stage 3: 16x16      │
│   ┌─┐              ┌──┐             ┌────┐             │
│   │█│              │██│             │████│             │
│   └─┘              └──┘             └────┘             │
│                                                         │
│   Stage 4: 32x32   Stage 5: 64x64   Stage 6: 128x128   │
│   ┌──────┐        ┌────────┐       ┌──────────┐        │
│   │██████│        │████████│       │██████████│        │
│   └──────┘        └────────┘       └──────────┘        │
│                                                         │
│   Stage 7: 256x256  Stage 8: 512x512  Stage 9: 1024x1024│
│   ┌──────────┐    ┌────────────┐  ┌──────────────┐    │
│   │██████████│    │████████████│  │██████████████│    │
│   │██████████│    │████████████│  │██████████████│    │
│   └──────────┘    └────────────┘  └──────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 場景生成

除了人物頭像，GAN 還能生成完整的室內場景和戶外景觀：

```python
# 簡單的場景生成示例
class SceneGenerator(nn.Module):
    def __init__(self, latent_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.ConvTranspose2d(latent_dim, 512, 4, 1, 0),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.ConvTranspose2d(512, 256, 4, 2, 1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.ConvTranspose2d(256, 128, 4, 2, 1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.ConvTranspose2d(128, 64, 4, 2, 1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 3, 4, 2, 1),
            nn.Tanh()
        )

    def forward(self, z):
        return self.net(z.view(-1, 100, 1, 1))
```

## 影像超解析度重建 (SRGAN)

SRGAN 是 GAN 在影像處理中的一個重要應用，可以將低解析度影像轉換為高解析度：

```python
class SRGAN_Generator(nn.Module):
    def __init__(self, num_res_blocks=16):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 9, 1, 4)

        self.res_blocks = nn.Sequential(*[
            ResidualBlock(64) for _ in range(num_res_blocks)
        ])

        self.conv2 = nn.Conv2d(64, 64, 3, 1, 1)
        self.upsample = nn.Sequential(
            nn.Conv2d(64, 256, 3, 1, 1),
            nn.PixelShuffle(2),
            nn.PReLU(),
            nn.Conv2d(64, 256, 3, 1, 1),
            nn.PixelShuffle(2),
            nn.PReLU()
        )
        self.conv3 = nn.Conv2d(64, 3, 9, 1, 4)

    def forward(self, x):
        out = self.conv1(x)
        residual = out
        out = self.res_blocks(out)
        out = self.conv2(out)
        out = out + residual
        out = self.upsample(out)
        out = self.conv3(out)
        return out

class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, 1, 1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.prelu = nn.PReLU()
        self.conv2 = nn.Conv2d(channels, channels, 3, 1, 1)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.prelu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        return out + residual
```

## 風格轉換 (Style Transfer)

### Pix2Pix

Pix2Pix 是影像轉換的經典方法，可以實現：
- 邊界圖 → 照片
- 白天 → 夜晚
- 速寫 → 卡通

```python
class Pix2Pix_Generator(nn.Module):
    def __init__(self, input_channels=3):
        super().__init__()
        # U-Net 架構
        self.encoder = nn.Sequential(
            nn.Conv2d(input_channels, 64, 4, 2, 1),
            nn.LeakyReLU(0.2),
            nn.Conv2d(64, 128, 4, 2, 1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2),
            nn.Conv2d(128, 256, 4, 2, 1),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2),
            nn.Conv2d(256, 512, 4, 2, 1),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2),
        )

        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(512, 256, 4, 2, 1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.ConvTranspose2d(256, 128, 4, 2, 1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.ConvTranspose2d(128, 64, 4, 2, 1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 3, 4, 2, 1),
            nn.Tanh()
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))
```

### CycleGAN

CycleGAN 實現了無需配對資料的風格轉換：

```
┌─────────────────────────────────────────────────────────┐
│                  CycleGAN 架構                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   領域 X                      領域 Y                    │
│   (如：馬)                    (如：斑馬)                │
│                                                         │
│        ┌──────┐         ┌──────┐                      │
│   ────►│  G   │────────►│  F   │────                  │
│   x    │X→Y   │   y'    │Y→X   │  x'                  │
│        └──┬───┘         └──┬───┘                      │
│           │               │                            │
│           │               │                            │
│           ▼               ▼                            │
│        ┌──────┐         ┌──────┐                      │
│   ────►│  D   │         │  D   │────                  │
│   x    │  Y   │         │  X   │  y                   │
│        └──────┘         └──────┘                      │
│                                                         │
│   循環一致性：F(G(x)) ≈ x, G(F(y)) ≈ y                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### CycleGAN 損失函數

```python
# 對抗損失
loss_G = bce(D_Y(G_XtoY(x)), ones)

# 循環一致性損失
loss_cycle = L1(F(G_XtoY(x)), x) + L1(G(F(y)), y)

# 身份損失（可選）
loss_identity = L1(G(x), x)

# 總損失
total_loss = loss_G + loss_F + lambda_cycle * loss_cycle + lambda_id * loss_identity
```

## 影像修復 (Inpainting)

GAN 還可以用於填充影像中被遮擋的區域：

```python
class InpaintingModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.generator = nn.Sequential(
            nn.Conv2d(4, 64, 4, 2, 1),  # 4 channels: RGB + mask
            nn.LeakyReLU(0.2),
            nn.Conv2d(64, 128, 4, 2, 1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2),
            # ... 更多卷積層 ...
            nn.ConvTranspose2d(512, 64, 4, 2, 1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 3, 3, 1, 1),
            nn.Tanh()
        )

    def forward(self, image, mask):
        # 將 mask 與影像拼接
        input_tensor = torch.cat([image, mask], dim=1)
        # 在 mask 區域填充
        output = self.generator(input_tensor)
        # 將填充區域與原圖混合
        return mask * output + (1 - mask) * image
```

## 實驗展示

```python
#!/usr/bin/env python3
"""GAN image generation applications demo"""

import torch
import torch.nn as nn
import numpy as np

def demo():
    print("GAN Image Generation Applications")
    print("=" * 50)

    print("\n1. Face Generation:")
    print("   - Progressive GAN: 1024x1024 faces")
    print("   - StyleGAN: Style mixing & interpolation")
    print("   - DCGAN: 64x64 faces")

    print("\n2. Image Super-Resolution:")
    print("   - SRGAN: 4x upscaling")
    print("   - ESRGAN: Enhanced SRGAN")
    print("   - RealSR: Real-world SR")

    print("\n3. Style Transfer:")
    print("   - Pix2Pix: Paired image translation")
    print("   - CycleGAN: Unpaired translation")
    print("   - UNIT: Unified image translation")

    print("\n4. Image Inpainting:")
    print("   - Context Encoder")
    print("   - Global & Local Attention")

    print("\n5. Neural Texture Synthesis:")
    print("   - Texture generation")
    print("   - Pattern creation")

    # Simulate generation
    print("\n6. Sample Generation Test:")
    batch_size = 4
    latent_dim = 100

    # Generate random samples
    noise = torch.randn(batch_size, latent_dim)
    print(f"   Input noise shape: {noise.shape}")

    # Simulated output (actual GAN would produce actual images)
    print(f"   Generated images: {batch_size} samples")
    print(f"   Resolution: 64x64x3")

    print("\nDemo completed!")

if __name__ == "__main__":
    demo()
```

## 應用對比表

| 應用 | 模型 | 輸入 | 輸出 |
|------|------|------|------|
| 人像生成 | ProGAN, StyleGAN | 噪音 | 高解析人像 |
| 超解析度 | SRGAN, ESRGAN | 低解析影像 | 高解析影像 |
| 風格轉換 | CycleGAN | 影像 | 風格化影像 |
| 影像轉換 | Pix2Pix | 條件影像 | 目標域影像 |
| 影像修復 | Context Encoder | 遮擋影像 | 填充影像 |
| 紋理生成 | TextureGAN | 噪音/紋理 | 新紋理 |

---

## 延伸閱讀

- [Ledig et al., 2017: SRGAN](https://www.google.com/search?q=SRGAN+Ledig+2017)
- [Isola et al., 2017: Pix2Pix](https://www.google.com/search?q=Pix2Pix+Isola+2017)
- [Zhu et al., 2017: CycleGAN](https://www.google.com/search?q=CycleGAN+Zhu+2017)

---

*本篇文章為「AI 程式人雜誌 2017 年 10 月號」 GAN 系列之五。*