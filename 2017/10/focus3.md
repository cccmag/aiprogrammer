# GAN 訓練技巧：Mode Collapse 與解決方案

## 前言

GAN 的訓練被譽為「深度學習中最困難的訓練任務之一」。訓練過程中常見的問題包括 Mode Collapse、梯度消失、訓練不穩定等。本篇文章將深入分析這些問題的原因，並探討現有的解決方案。

## Mode Collapse 問題

### 什麼是 Mode Collapse？

Mode Collapse 是 GAN 訓練中最常見的問題之一。簡單來說，生成器只學習到了真實資料分佈的「部分模式」（modes），而忽略了其他模式。

```
┌─────────────────────────────────────────────────────────┐
│                  Mode Collapse 示意圖                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  真實資料分佈（多峰）           學習到的分佈（單峰）      │
│                                                         │
│     █                               █                   │
│   █ █ █                           █   █   █              │
│ █ █ █ █ █      ──────→          ███████████             │
│   █ █ █                               █                   │
│     █                                                       │
│                                                         │
│  真實分佈有多種數字          生成器只產生「1」           │
│  （0-9）                                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Mode Collapse 的原因

Mode Collapse 的根本原因在於生成器和判別器之間的競爭關係失衡：

```python
# 當判別器太強時
# 生成器的梯度信号變弱
# 生成器傾向於找到「騙過判別器」的捷徑
# 即找到一種「萬能」的模式来欺骗判別器

# 數學上：
# log(1 - D(G(z))) 的梯度在 D(G(z)) 接近 0 時趨近於 0
# 導致生成器無法學習
```

## 解決方案

### 1. 損失函數修改

#### 原始 GAN 損失的問題

```python
# 原始 GAN：min log(1 - D(G(z)))
# 問題：當 D(G(z)) 接近 0 時，梯度趨近於 0

# 解決方案：使用不同的損失函數
```

#### Modified GAN (非飽和損失)

```python
# 方法 1: 替換生成器損失
# 原始：min log(1 - D(G(z)))
# 修改：max log(D(G(z)))

# 這被稱為「non-saturated GAN」
G_loss = -torch.mean(torch.log(D(fake_images)))
```

#### 最小二乘 GAN (LSGAN)

```python
# 方法 2: 使用最小二乘損失
D_loss = 0.5 * (torch.mean((D(real_images) - 1)**2)
              + torch.mean(D(fake_images)**2))
G_loss = 0.5 * torch.mean((D(fake_images) - 1)**2)
```

### 2. 特徵匹配

```python
# 方法 3: 特徵匹配
# 生成器的目標不僅是欺騙判別器
# 還要讓生成的特徵與真實資料相似

real_features = discriminator(real_images).mean()
fake_features = discriminator(fake_images).detach().mean()

G_loss = torch.mean((fake_features - real_features)**2)
```

### 3. 小批次判別 (Mini-batch Discrimination)

```python
# 方法 4: 小批次判別
# 讓判別器一次看多個樣本
# 如果生成器產生總是相似的樣本，判別器可以識別

class MiniBatchDiscrimination(nn.Module):
    def __init__(self, input_dim, num_kernels, kernel_dim):
        super().__init__()
        self.T = nn.Parameter(torch.randn(input_dim, num_kernels, kernel_dim))

    def forward(self, x):
        # 計算每個樣本與其他樣本的距離
        matrices = x.unsqueeze(0) - x.unsqueeze(1)
        matrices = matrices.pow(2).sum(-1).sqrt()
        matrices = torch.exp(-matrices @ self.T)
        return matrices.sum(0) / (x.size(0) - 1)
```

### 4. 標籤平滑 (Label Smoothing)

```python
# 方法 5: 標籤平滑
# 真實標籤不使用 1.0，而是使用 0.9 或 0.7
# 這可以防止判別器過度自信，穩定訓練

real_labels = torch.full((batch_size,), 0.9)  # 而非 1.0
fake_labels = torch.zeros(batch_size)
```

### 5. 實例標準化 (Instance Normalization)

```python
# 方法 6: 使用實例標準化而非批量標準化
# 適用於影像生成任務

class InstanceNorm2d(nn.Module):
    def forward(self, x):
        b, c = x.shape[:2]
        x = x.view(b, c, -1)
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, keepdim=True)
        return (x - mean) / (std + 1e-8)
```

## 訓練穩定性技巧

### 1. 學習率策略

```python
# 使用不同的學習率訓練 G 和 D
optimizer_G = optim.Adam(G.parameters(), lr=0.0001, betas=(0.0, 0.9))
optimizer_D = optim.Adam(D.parameters(), lr=0.0004, betas=(0.0, 0.9))
```

### 2. 梯度裁剪

```python
# 裁剪梯度範圍，防止梯度爆炸
torch.nn.utils.clip_grad_norm_(G.parameters(), max_norm=1.0)
torch.nn.utils.clip_grad_norm_(D.parameters(), max_norm=1.0)
```

### 3. 緩慢學習判別器

```python
# 每訓練一次 G，訓練 D 多次
for _ in range(k):
    # 訓練 D
    ...

# 或降低 D 的學習率
```

## 訓練監控

### 監控指標

```python
# 監控以下指標來判斷訓練狀態：

# 1. 判別器損失
d_loss = loss_D.item()

# 2. 生成器損失
g_loss = loss_G.item()

# 3. 生成影像的品質（可以用 FID, IS 等）
# 4. 潛在空間插值的平滑度
```

### 訓練異常診斷

| 現象 | 原因 | 解決方案 |
|------|------|---------|
| Loss D ≈ 0 | 判別器太強 | 提高 D 學習率或降低 G 學習率 |
| Loss G 不下降 | 生成器梯度消失 | 使用替代損失或特徵匹配 |
| 影像品質下降 | Mode Collapse | 使用小批次判別 |
| 訓練震盪 | 學習率太高 | 降低學習率 |

## 實驗：對比不同技巧

```python
#!/usr/bin/env python3
"""GAN training techniques comparison"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

def demo():
    print("GAN Training Techniques Demo")
    print("=" * 50)

    print("\n1. Mode Collapse Problem:")
    print("   - Generator learns only partial distribution")
    print("   - Often produces similar outputs")

    print("\n2. Solution Techniques:")
    print("   a) Non-saturated loss: max log(D(G(z)))")
    print("   b) LSGAN: Least squares loss")
    print("   c) Feature matching: Match intermediate features")
    print("   d) Mini-batch discrimination: Consider batch diversity")
    print("   e) Label smoothing: Use 0.9 instead of 1.0")
    print("   f) Instance normalization: For image tasks")

    print("\n3. Training Stability Tips:")
    print("   a) Use different lr for G and D")
    print("   b) Gradient clipping")
    print("   c) Train D more times than G")
    print("   d) Add noise to inputs")

    print("\n4. Implementation Example:")

    LATENT_DIM = 100
    BATCH_SIZE = 32

    # Simulated loss values
    d_loss = 0.693  # Binary cross entropy of random guessing
    g_loss = 0.693

    print(f"\n   Initial losses (random):")
    print(f"   D loss: {d_loss:.4f}")
    print(f"   G loss: {g_loss:.4f}")

    # After training progress
    d_loss_final = 0.45
    g_loss_final = 1.25

    print(f"\n   After training:")
    print(f"   D loss: {d_loss_final:.4f}")
    print(f"   G loss: {g_loss_final:.4f}")

    if d_loss_final < 0.3:
        print("\n   Warning: D might be too strong!")
        print("   Consider: lower D lr or increase D lr ratio")

    if g_loss_final > 2.0:
        print("\n   Warning: G is not learning well!")
        print("   Consider: use non-saturated loss or feature matching")

    print("\n   Demo completed!")

if __name__ == "__main__":
    demo()
```

---

## 延伸閱讀

- [Salimans et al., 2016: Improved Techniques for Training GANs](https://www.google.com/search?q=Improved+Techniques+Training+GANs+Salimans+2016)
- [GAN Training Tips](https://www.google.com/search?q=GAN+training+tips+mode+collapse)
- [How to Train a GAN?](https://www.google.com/search?q=how+to+train+GAN+github)

---

*本篇文章為「AI 程式人雜誌 2017 年 10 月號」 GAN 系列之三。*