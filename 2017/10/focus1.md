# GAN 基礎：生成對抗網路的誕生（2014）

## 前言

2014 年，Ian Goodfellow 在蒙特婁大學攻讀博士學位期間，與他的導師 Yoshua Bengio 以及其他研究者進行了一場熱烈的討論。在酒吧中的靈感催生了一個革命性的想法——讓兩個神經網路相互「對抗」，透過競爭來學習生成逼真的資料。這就是生成對抗網路（Generative Adversarial Network，簡稱 GAN）的誕生。

## GAN 的核心思想

GAN 的核心思想源自博弈論中的零和遊戲（Zero-Sum Game）。在 GAN 中，我們有兩個玩家：

```
┌─────────────────────────────────────────────────────┐
│              GAN 的零和遊戲                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│   生成器 G (Generator)                              │
│   - 輸入：隨機噪音 z                               │
│   - 輸出：生成的資料 G(z)                          │
│   - 目標：欺騙判別器                               │
│                                                     │
│        ↕ 對抗 ↕                                    │
│                                                     │
│   判別器 D (Discriminator)                         │
│   - 輸入：真實資料 x 或 生成資料 G(z)              │
│   - 輸出：資料為真實的機率 D(x)                    │
│   - 目標：正確區分真假                             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 對抗訓練示意圖

```
真實資料 x ──┐
             ├──→ 判別器 D ──→ D(x) ≈ 1 (真實)
             │                   │
             │                   ▼
生成器 G ←───┼──── 噪音 z        │ 目標函數
             │                   │ V(D,G)
             │                   ▼
             ├──→ 判別器 D ──→ D(G(z)) ≈ 0 (假的)
假資料 G(z) ──┘
```

## 數學形式

GAN 的目標函數是一個 minimax 問題：

```python
min_G max_D V(D, G) = E_x~p_data[log D(x)] + E_z~p_z[log(1 - D(G(z)))]
```

### 判別器的目標

判別器 D 希望能夠最大化目標函數：
- 對於真實資料 x：D(x) 應該接近 1
- 對於假資料 G(z)：D(G(z)) 應該接近 0

因此，判別器要最大化：
```
E_x~p_data[log D(x)] + E_z~p_z[log(1 - D(G(z)))]
```

### 生成器的目標

生成器 G 希望能夠最小化目標函數，即讓判別器認為生成的資料是真的：
- G(z) 應該讓 D(G(z)) 接近 1

因此，生成器要最小化：
```
E_z~p_z[log(1 - D(G(z)))]
```

## 訓練過程

GAN 的訓練過程可以分為以下步驟：

```python
for epoch in range(num_epochs):
    for batch in dataloader:
        # 步驟 1: 訓練判別器
        real_images = batch
        noise = torch.randn(batch_size, latent_dim)
        fake_images = generator(noise)

        # 計算判別器損失
        d_loss = -torch.mean(torch.log(discriminator(real_images))
                          + torch.log(1 - discriminator(fake_images)))

        d_loss.backward()
        discriminator_optimizer.step()

        # 步驟 2: 訓練生成器
        noise = torch.randn(batch_size, latent_dim)
        fake_images = generator(noise)

        # 計算生成器損失
        g_loss = -torch.mean(torch.log(discriminator(fake_images)))

        g_loss.backward()
        generator_optimizer.step()
```

### 訓練流程圖

```
┌─────────────────────────────────────────────────────────┐
│                    GAN 訓練流程                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  初始化：生成器 G_0, 判別器 D_0                         │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │  FOR each epoch:                                │  │
│  │                                                 │  │
│  │    ┌─────────────────────────────────────────┐  │  │
│  │    │  FOR each batch:                        │  │  │
│  │    │                                         │  │  │
│  │    │  1. 更新判別器 (固定 G)                  │  │  │
│  │    │     - 取真實資料 x                      │  │  │
│  │    │     - 取噪音 z，生成 G(z)               │  │  │
│  │    │     - 最大化 log D(x) + log(1-D(G(z)))  │  │  │
│  │    │                                         │  │  │
│  │    │  2. 更新生成器 (固定 D)                 │  │  │
│  │    │     - 取噪音 z，生成 G(z)              │  │  │
│  │    │     - 最小化 log(1-D(G(z)))            │  │  │
│  │    │                                         │  │  │
│  │    └─────────────────────────────────────────┘  │  │
│  │                                                 │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Nash 均衡

當 GAN 訓練收斂時，系統會達到 Nash 均衡，此時：

```
D*(x) = p_data(x) / (p_data(x) + p_g(x))
```

其中 p_data 是真實資料分佈，p_g 是生成器學習到的分佈。當 p_g = p_data 時，判別器輸出為 0.5，表示無法區分真假。

## 簡單的 GAN 實現

以下是一個最簡單的 GAN 實現示例：

```python
#!/usr/bin/env python3
"""Simple GAN implementation for demonstration"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

class Generator(nn.Module):
    def __init__(self, latent_dim, output_dim):
        super(Generator, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, output_dim),
            nn.Tanh()
        )

    def forward(self, z):
        return self.net(z)

class Discriminator(nn.Module):
    def __init__(self, input_dim):
        super(Discriminator, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)

def demo():
    print("Simple GAN Demo")
    print("=" * 40)

    latent_dim = 10
    data_dim = 2
    epochs = 1000
    lr = 0.001

    G = Generator(latent_dim, data_dim)
    D = Discriminator(data_dim)

    optimizer_G = optim.Adam(G.parameters(), lr=lr)
    optimizer_D = optim.Adam(D.parameters(), lr=lr)

    real_data = torch.randn(1000, data_dim) * 2 + torch.tensor([0, 0])

    print(f"Training on 2D data distribution...")
    print(f"Real data mean: {real_data.mean(dim=0)}")
    print(f"Real data std: {real_data.std(dim=0)}")

    for epoch in range(epochs):
        # Train Discriminator
        real_batch = real_data[torch.randint(0, len(real_data), (32,))]
        noise = torch.randn(32, latent_dim)
        fake_batch = G(noise).detach()

        d_loss = -torch.mean(torch.log(D(real_batch) + 1e-8)
                          + torch.log(1 - D(fake_batch) + 1e-8))

        optimizer_D.zero_grad()
        d_loss.backward()
        optimizer_D.step()

        # Train Generator
        noise = torch.randn(32, latent_dim)
        fake_batch = G(noise)
        g_loss = -torch.mean(torch.log(D(fake_batch) + 1e-8))

        optimizer_G.zero_grad()
        g_loss.backward()
        optimizer_G.step()

        if (epoch + 1) % 200 == 0:
            print(f"Epoch [{epoch+1}/{epochs}] D Loss: {d_loss.item():.4f} G Loss: {g_loss.item():.4f}")

    noise = torch.randn(100, latent_dim)
    generated = G(noise).detach()
    print(f"\nGenerated data mean: {generated.mean(dim=0)}")
    print(f"Generated data std: {generated.std(dim=0)}")
    print("Demo completed!")

if __name__ == "__main__":
    demo()
```

## 訓練 GAN 的挑戰

GAN 的訓練面臨幾個主要挑戰：

### 1. Mode Collapse

生成器可能只學習到資料分佈的少數模式，忽視了其他多樣性。例如，如果訓練資料包含多種數字，生成器可能只產生「1」。

### 2. 訓練不穩定

生成器和判別器之間需要保持平衡。如果判別器太強，生成器無法學習；如果生成器太強，判別器無法區分真假。

### 3. 梯度消失

當判別器表現太好時，生成器的梯度可能會消失，導致無法學習。

## 為什麼 GAN 重要？

GAN 的意義在於：

1. **新的生成模型範式**：不同於傳統的變分自編碼器（VAE），GAN 不需要明確建模機率分佈
2. **高品質生成**：可以生成極為逼真的影像、音訊、文字
3. **無監督學習**：可以從無標註資料中學習
4. **靈活性**：可以與各種網路架構結合

---

## 延伸閱讀

- [Goodfellow et al., 2014: Generative Adversarial Networks](https://www.google.com/search?q=Goodfellow+GAN+2014+paper)
- [Ian Goodfellow 訪談：GAN 的發明過程](https://www.google.com/search?q=Ian+Goodfellow+GAN+interview+history)
- [NIPS 2016 GAN Tutorial](https://www.google.com/search?q=NIPS+2016+GAN+tutorial)

---

*本篇文章為「AI 程式人雜誌 2017 年 10 月號」 GAN 系列之一。*