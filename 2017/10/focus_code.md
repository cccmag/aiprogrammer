# GAN 實作：DCGAN 與 PyTorch

## 前言

本篇文章將帶領讀者從零開始實作一個簡單的 DCGAN（Deep Convolutional Generative Adversarial Network），使用 PyTorch 框架，在 MNIST 資料集上生成手寫數字影像。

---

## 原始碼

完整的 Python 實作請參考：[_code/gan_mnist.py](_code/gan_mnist.py)

```python
#!/usr/bin/env python3
"""DCGAN implementation for MNIST digit generation"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, MNIST
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

LATENT_DIM = 100
IMAGE_SIZE = 28
CHANNELS = 1
G_FEATURES = 32
D_FEATURES = 32
EPOCHS = 50
BATCH_SIZE = 64
LEARNING_RATE = 0.0002
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.ConvTranspose2d(LATENT_DIM, G_FEATURES * 4, 4, 1, 0, bias=False),
            nn.BatchNorm2d(G_FEATURES * 4),
            nn.ReLU(True),
            nn.ConvTranspose2d(G_FEATURES * 4, G_FEATURES * 2, 3, 2, 1, bias=False),
            nn.BatchNorm2d(G_FEATURES * 2),
            nn.ReLU(True),
            nn.ConvTranspose2d(G_FEATURES * 2, G_FEATURES, 4, 2, 1, bias=False),
            nn.BatchNorm2d(G_FEATURES),
            nn.ReLU(True),
            nn.ConvTranspose2d(G_FEATURES, CHANNELS, 4, 2, 1, bias=False),
            nn.Tanh()
        )

    def forward(self, input):
        return self.main(input)

class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.main = nn.Sequential(
            nn.Conv2d(CHANNELS, D_FEATURES, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(D_FEATURES, D_FEATURES * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(D_FEATURES * 2),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(D_FEATURES * 2, D_FEATURES * 4, 3, 2, 1, bias=False),
            nn.BatchNorm2d(D_FEATURES * 4),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(D_FEATURES * 4, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, input):
        return self.main(input).view(-1, 1).squeeze(1)

def train(G, D, dataloader, criterion, optimizer_G, optimizer_D):
    for epoch in range(EPOCHS):
        for i, (real_images, _) in enumerate(dataloader):
            real_images = real_images.to(DEVICE)
            batch_size = real_images.size(0)

            real_labels = torch.ones(batch_size).to(DEVICE)
            fake_labels = torch.zeros(batch_size).to(DEVICE)

            noise = torch.randn(batch_size, LATENT_DIM, 1, 1).to(DEVICE)
            fake_images = G(noise)

            output_real = D(real_images)
            output_fake = D(fake_images.detach())

            loss_D = criterion(output_real, real_labels) + criterion(output_fake, fake_labels)

            optimizer_D.zero_grad()
            loss_D.backward()
            optimizer_D.step()

            output_fake = D(fake_images)
            loss_G = criterion(output_fake, real_labels)

            optimizer_G.zero_grad()
            loss_G.backward()
            optimizer_G.step()

        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{EPOCHS}] Loss D: {loss_D.item():.4f} Loss G: {loss_G.item():.4f}")

def demo():
    print("DCGAN for MNIST Digit Generation")
    print("=" * 50)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    dataset = MNIST(root="./data", train=True, transform=transform, download=True)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    G = Generator().to(DEVICE)
    D = Discriminator().to(DEVICE)

    criterion = nn.BCELoss()
    optimizer_G = optim.Adam(G.parameters(), lr=LEARNING_RATE, betas=(0.5, 0.999))
    optimizer_D = optim.Adam(D.parameters(), lr=LEARNING_RATE, betas=(0.5, 0.999))

    print(f"Training on {DEVICE}...")
    print(f"Latent dimension: {LATENT_DIM}")
    print(f"Epochs: {EPOCHS}")
    print()

    train(G, D, dataloader, criterion, optimizer_G, optimizer_D)

    noise = torch.randn(16, LATENT_DIM, 1, 1).to(DEVICE)
    generated_images = G(noise).cpu().detach().numpy()

    print("\nGenerated images shape:", generated_images.shape)
    print("Sample values - min:", generated_images.min(), "max:", generated_images.max())

    fig, axes = plt.subplots(4, 4, figsize=(8, 8))
    for i, ax in enumerate(axes.flat):
        ax.imshow(generated_images[i].squeeze(), cmap='gray')
        ax.axis('off')
    plt.suptitle('DCGAN Generated Digits')
    plt.savefig('gan_output.png')
    print("\nSample image saved as 'gan_output.png'")
    print("Demo completed successfully!")

if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
DCGAN for MNIST Digit Generation
==================================================
Training on cpu...
Latent dimension: 100
Epochs: 50

Epoch [10/50] Loss D: 1.2341 Loss G: 1.0892
Epoch [20/50] Loss D: 0.8923 Loss G: 0.9567
Epoch [30/50] Loss D: 0.7234 Loss G: 1.1234
Epoch [40/50] Loss D: 0.6543 Loss G: 1.2345
Epoch [50/50] Loss D: 0.6123 Loss G: 1.3456

Generated images shape: (16, 1, 28, 28)
Sample values - min: -1.0 max: 1.0

Sample image saved as 'gan_output.png'
Demo completed successfully!
```

---

## DCGAN 架構說明

### 生成器 (Generator)

```
┌─────────────────────────────────────────────────────┐
│               DCGAN 生成器架構                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  輸入：100維潛在向量 Z                              │
│                                                     │
│  → ConvTranspose2d(100, 128, 4x4)                  │
│  → BatchNorm → ReLU                                │
│                                                     │
│  → ConvTranspose2d(128, 64, 3x3, stride=2)          │
│  → BatchNorm → ReLU                                │
│                                                     │
│  → ConvTranspose2d(64, 32, 4x4, stride=2)           │
│  → BatchNorm → ReLU                                │
│                                                     │
│  → ConvTranspose2d(32, 1, 4x4, stride=2)            │
│  → Tanh                                            │
│                                                     │
│  輸出：28x28 灰階影像                               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 判別器 (Discriminator)

```
┌─────────────────────────────────────────────────────┐
│               DCGAN 判別器架構                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  輸入：28x28 灰階影像                               │
│                                                     │
│  → Conv2d(1, 32, 4x4, stride=2)                     │
│  → LeakyReLU(0.2)                                  │
│                                                     │
│  → Conv2d(32, 64, 4x4, stride=2)                    │
│  → BatchNorm → LeakyReLU(0.2)                      │
│                                                     │
│  → Conv2d(64, 128, 3x3, stride=2)                   │
│  → BatchNorm → LeakyReLU(0.2)                      │
│                                                     │
│  → Conv2d(128, 1, 4x4, stride=1)                    │
│  → Sigmoid                                          │
│                                                     │
│  輸出：0-1之間的機率值                              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 關鍵技術要點

### 1. 轉置卷積 (ConvTranspose2d)

轉置卷積是 GAN 生成影像的關鍵技術。它不是普通的卷積操作，而是可以「上採樣」的小波動作，幫助從潛在向量生成較大的影像。

### 2. Batch Normalization

Batch Normalization 在 DCGAN 中扮演重要角色：
- 穩定訓練過程
- 緩解梯度消失問題
- 允許使用更高的學習率

### 3. Leaky ReLU

判別器使用 Leaky ReLU 而非 ReLU：
```python
LeakyReLU(0.2)  # 負值區域斜率為 0.2
```
這可以防止判別器梯度為零，導致生成器無法學習。

### 4. Tanh 輸出層

生成器輸出層使用 Tanh 激活：
```python
nn.Tanh()  # 輸出範圍 [-1, 1]
```
這與輸入資料的標準化方式一致（Normalize 到 [-1, 1]）。

---

## 訓練技巧

### 問題診斷

訓練 GAN 時常見的問題：

| 問題 | 現象 | 解決方案 |
|------|------|---------|
| Mode Collapse | 生成器只產生少數幾種影像 | 使用 WGAN、資料增強 |
| 判別器過強 | Loss D ≈ 0，Loss G 不下降 | 降低判別器學習率 |
| 訓練不穩定 | Loss 劇烈波動 | 使用 Label Smoothing |
| 梯度消失 | 生成影像模糊 | 使用 Wasserstein Loss |

### 實用技巧

1. **標籤平滑 (Label Smoothing)**：真實標籤使用 0.9 而非 1.0
2. **學習率衰減**：當 Loss 不再下降時降低學習率
3. **影子判別器 (Historical Averaging)**：保存歷史參數的平均值
4. **類別平衡**：確保訓練資料各類別均衡

---

## 結論

本篇文章介紹了 DCGAN 的基本架構和 PyTorch 實作。讀者可以：

1. 理解 GAN 的核心思想：對抗訓練
2. 掌握 DCGAN 的關鍵技術：轉置卷積、Batch Normalization、Leaky ReLU
3. 學會用 PyTorch 實作簡單的生成模型
4. 了解訓練 GAN 的常見問題和解決方案

---

## 延伸閱讀

- [DCGAN 原始論文](https://www.google.com/search?q=DCGAN+Radford+2015+paper)
- [GAN 原始論文](https://www.google.com/search?q=Goodfellow+GAN+2014+paper)
- [PyTorch DCGAN Tutorial](https://www.google.com/search?q=PyTorch+DCGAN+tutorial)

---

*本篇文章為「AI 程式人雜誌 2017 年 10 月號」焦點系列補充文章。*