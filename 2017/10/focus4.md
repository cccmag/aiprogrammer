# WGAN 與條件式 GAN：穩定訓練的新方法

## 前言

2017 年是 GAN 發展史上的重要年份。這一年提出了兩個重要的改進：Wasserstein GAN (WGAN) 和條件式 GAN (Conditional GAN)。這兩項工作從不同角度解決了 GAN 的核心問題——訓練穩定性和可控生成。

## Wasserstein GAN (WGAN)

### 背景與動機

原始 GAN 的損失函數基於 JS 散度（Jensen-Shannon Divergence），當兩個分佈不重疊時，JS 散度趨近於常數，導致梯度消失。

### Earth Mover Distance

WGAN 提出了使用 Earth Mover Distance（又稱 Wasserstein-1 距離）來替代 JS 散度：

```python
# Earth Mover Distance 的直觀理解
# 想象有兩堆土（兩個分佈）
# EM distance 是將一堆土移動成另一堆的最小平均距離

# 數學定義：
# W(p_r, p_g) = inf_γ∈Π(p_r,p_g) E_(x,y)∼γ[||x-y||]
# 其中 Π(p_r, p_g) 是所有聯合分佈的集合
```

### WGAN 演算法

```python
# WGAN 的關鍵變化：

# 1. 判別器輸出不再是機率，而是「打分」
# 2. 移除 Sigmoid 輸出層
# 3. 權重裁剪 (Weight Clipping)
# 4. 使用 RMSProp 或 SGD（不用 Adam）

# 判別器（此時稱為 Critic）的損失：
d_loss = -torch.mean(critic(real_images)) + torch.mean(critic(fake_images))

# 生成器的損失：
g_loss = -torch.mean(critic(fake_images))
```

### 權重裁剪

```python
# WGAN 的權重裁剪
# 將判別器參數限制在 [-c, c] 範圍內

class Critic(nn.Module):
    def __init__(self):
        super().__init__()
        # 網路架構
        ...

    def forward(self, x):
        return self.main(x).view(-1)

def clip_weights(critic, clip_value=0.01):
    for p in critic.parameters():
        p.data.clamp_(-clip_value, clip_value)
```

### WGAN-GP (Gradient Penalty)

權重裁剪會導致最適化問題，因此後來提出了 Gradient Penalty：

```python
# WGAN-GP: 使用梯度懲罰替代權重裁剪

def gradient_penalty(critic, real_images, fake_images):
    batch_size = real_images.size(0)
    alpha = torch.rand(batch_size, 1, 1, 1)
    interpolated = alpha * real_images + (1 - alpha) * fake_images
    interpolated.requires_grad_(True)

    critic_interpolated = critic(interpolated)

    gradients = torch.autograd.grad(
        outputs=critic_interpolated,
        inputs=interpolated,
        grad_outputs=torch.ones_like(critic_interpolated),
        create_graph=True
    )[0]

    gradients = gradients.view(batch_size, -1)
    gradient_norm = gradients.norm(2, dim=1)
    penalty = ((gradient_norm - 1) ** 2).mean()

    return penalty

# WGAN-GP 損失
gp = gradient_penalty(critic, real_images, fake_images)
d_loss = -torch.mean(critic(real_images)) + torch.mean(critic(fake_images)) + 10 * gp
```

## 條件式 GAN (Conditional GAN)

### 基本思想

條件式 GAN 允許我們控制生成器的輸出，通過添加條件資訊（如類別標籤）來指導生成過程。

```
┌─────────────────────────────────────────────────────────┐
│               條件式 GAN 架構                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   噪音 z ──┐                                            │
│            ├──→ 生成器 G ──→ 生成影像 G(z|y)           │
│   標籤 y ──┘         ↑                                   │
│                     │                                   │
│                     │                                   │
│            條件輸入（類別）                              │
│                                                         │
│   真實影像 x ──┐                                        │
│                ├──→ 判別器 D ──→ D(x|y)                │
│   標籤 y ──────┘                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 條件資訊的加入方式

```python
# 方法 1: 拼接 (Concatenation)

# 生成器
noise = torch.randn(batch_size, latent_dim)
label_embedding = embedding_layer(label)  # 將標籤轉為向量
combined = torch.cat([noise, label_embedding], dim=1)
generated = generator(combined)

# 判別器
combined_real = torch.cat([real_images, label_embedding], dim=1)
decision = discriminator(combined_real)

# 方法 2: 條件 Batch Normalization
# 根據標籤調整 BatchNorm 的參數
class ConditionalBatchNorm(nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.bn = nn.BatchNorm2d(num_features)
        self.embed = nn.Embedding(num_classes, num_features * 2)
        # gamma 和 beta

    def forward(self, x, label):
        gamma_beta = self.embed(label)
        gamma, beta = gamma_beta.chunk(2, dim=1)
        out = self.bn(x)
        return gamma.view(-1) * out + beta.view(-1)
```

### CGAN 的訓練

```python
def train_cgan(generator, discriminator, dataloader, criterion,
               optimizer_G, optimizer_D, num_epochs):
    for epoch in range(num_epochs):
        for real_images, labels in dataloader:
            batch_size = real_images.size(0)

            # 訓練判別器
            noise = torch.randn(batch_size, latent_dim)
            fake_images = generator(noise, labels)

            real_output = discriminator(real_images, labels)
            fake_output = discriminator(fake_images.detach(), labels)

            real_labels = torch.ones(batch_size)
            fake_labels = torch.zeros(batch_size)

            d_loss = criterion(real_output, real_labels) + \
                     criterion(fake_output, fake_labels)

            optimizer_D.zero_grad()
            d_loss.backward()
            optimizer_D.step()

            # 訓練生成器
            noise = torch.randn(batch_size, latent_dim)
            fake_images = generator(noise, labels)
            fake_output = discriminator(fake_images, labels)

            g_loss = criterion(fake_output, real_labels)

            optimizer_G.zero_grad()
            g_loss.backward()
            optimizer_G.step()
```

## ACGAN (Auxiliary Classifier GAN)

ACGAN 是 CGAN 的一個變體，不僅讓判別器區分真假，還要求它預測類別：

```python
# ACGAN 判別器輸出：
# 1. 真/假 (Sigmoid)
# 2. 類別 (Softmax)

class ACGAN_Discriminator(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.features = convolutional_layers()
        self.adv_layer = nn.Linear(512, 1)  # 真/假
        self.aux_layer = nn.Linear(512, num_classes)  # 類別

    def forward(self, x):
        features = self.features(x)
        features = features.mean(-1).mean(-1)
        validity = torch.sigmoid(self.adv_layer(features))
        label = torch.softmax(self.aux_layer(features), dim=1)
        return validity, label

# ACGAN 損失
d_loss_real = bce(real_output, real_labels)
d_loss_fake = bce(fake_output, fake_labels)
d_loss_cls = ce(aux_output, labels)  # 類別損失

d_loss = d_loss_real + d_loss_fake + d_loss_cls
```

## 實作比較

```python
#!/usr/bin/env python3
"""WGAN and Conditional GAN implementation comparison"""

import torch
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, latent_dim, num_classes=None, use_condition=True):
        super().__init__()
        self.use_condition = use_condition

        input_dim = latent_dim + num_classes if use_condition else latent_dim

        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 512),
            nn.BatchNorm1d(512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 784),
            nn.Tanh()
        )

    def forward(self, z, labels=None):
        if self.use_condition and labels is not None:
            label_embedding = torch.zeros(z.size(0), labels.max().item() + 1)
            label_embedding.scatter_(1, labels.unsqueeze(1), 1)
            z = torch.cat([z, label_embedding], dim=1)
        return self.net(z).view(-1, 1, 28, 28)

def demo():
    print("WGAN and Conditional GAN Demo")
    print("=" * 50)

    latent_dim = 100
    num_classes = 10
    batch_size = 32

    print("\n1. WGAN Key Changes:")
    print("   - Uses Earth Mover Distance instead of JS Divergence")
    print("   - Critic outputs score, not probability")
    print("   - No Sigmoid at output")
    print("   - Weight clipping or Gradient Penalty")

    print("\n2. Conditional GAN:")
    print("   - Adds conditioning information (labels)")
    print("   - Generator input: noise + label")
    print("   - Discriminator input: image + label")

    print("\n3. ACGAN:")
    print("   - Discriminator predicts both authenticity and class")
    print("   - Adds auxiliary classifier loss")

    # Create models
    print("\n4. Implementation Test:")

    # Standard generator
    G_standard = Generator(latent_dim, use_condition=False)
    noise = torch.randn(batch_size, latent_dim)
    output = G_standard(noise)
    print(f"   Standard GAN output shape: {output.shape}")

    # Conditional generator
    G_cond = Generator(latent_dim, num_classes, use_condition=True)
    labels = torch.randint(0, num_classes, (batch_size,))
    output_cond = G_cond(noise, labels)
    print(f"   Conditional GAN output shape: {output_cond.shape}")

    print("\nDemo completed!")

if __name__ == "__main__":
    demo()
```

## 總結對比

| 特性 | 原始 GAN | WGAN | CGAN | ACGAN |
|------|----------|------|------|-------|
| 損失函數 | BCE | Wasserstein | BCE | BCE + CE |
| 訓練穩定性 | 差 | 好 | 一般 | 一般 |
| 可控生成 | 否 | 否 | 是 | 是 |
| 類別預測 | 否 | 否 | 否 | 是 |
| 輸出機率 | 是 | 否（打分） | 是 | 是 |

---

## 延伸閱讀

- [Arjovsky et al., 2017: Wasserstein GAN](https://www.google.com/search?q=Wasserstein+GAN+Arjovsky+2017)
- [Gulrajani et al., 2017: WGAN-GP](https://www.google.com/search?q=WGAN+GP+gradient+penalty+2017)
- [Mirza & Osindero, 2014: Conditional GAN](https://www.google.com/search?q=Conditional+GAN+Mirza+2014)

---

*本篇文章為「AI 程式人雜誌 2017 年 10 月號」 GAN 系列之四。*