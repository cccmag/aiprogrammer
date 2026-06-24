# GAN 與影像生成藝術

## 前言

生成對抗網路（GAN，Generative Adversarial Networks）由 Ian Goodfellow 於 2014 年提出，是深度學習領域最重要的生成模型之一。2017 年，GAN 在影像生成和藝術創作方面取得了顯著進展。

## GAN 的原理

### 對抗訓練

GAN 包含兩個神經網路：

```
生成器 (Generator)：生成假樣本
    ↑
    |（對抗信號）
    ↓
判別器 (Discriminator)：區分真假
```

```python
# 生成器
G = Generator(z)  # 輸入隨機噪聲，輸出影像

# 判別器
D = Discriminator(x)  # 輸入影像，輸出真假概率

# 對抗目標
# D 希望盡可能正確區分真假
# G 希望 D 盡可能犯錯（把假的當成真的）
```

### 訓練過程

```python
# 訓練迴圈
for epoch in range(num_epochs):
    # 訓練判別器
    real_images = get_real_batch()
    fake_images = G(get_random_noise())
    d_loss = -torch.mean(torch.log(D(real_images)) + torch.log(1 - D(fake_images)))

    # 訓練生成器
    g_loss = -torch.mean(torch.log(D(G(z))))

    # 更新參數
    d_optimizer.step()
    g_optimizer.step()
```

## GAN 的進展

### DCGAN (2015)

深度卷積 GAN：

```python
# DCGAN 的關鍵技術：
# - 使用轉置卷積
# - Batch Normalization
# - Leaky ReLU
# - 穩定訓練
```

### 2017 年的進展

```
GAN 家族的分支：
- DCGAN：基礎卷積 GAN
- Wasserstein GAN：改善穩定性
- Conditional GAN：條件生成
- StyleGAN：影像樣式控制
- CycleGAN：風格遷移
```

## 應用場景

### 影像生成

```python
# 虛構人物影像
# 藝術創作
# 影像修復
# 超解析度重建
```

### 影像修復

```python
# 去馬賽克
# 填補缺失區域
# 去除不需要的物體
```

### 風格遷移

```python
# CycleGAN
# 將一種類別的影像轉換為另一類
# 馬 → 斑馬
# 照片 → 油畫
```

## 藝術與創意

### AI 生成藝術

藝術家開始使用 GAN 進行創作：

- **Edmond de Belamy**：AI 生成的人物畫像
- **Obvious**：使用 GAN 的藝術團體
- **Mario Klingemann**：著名的數位藝術家

### 倫理問題

```python
# Deepfake 的隱憂
# 虛假資訊
# 肖像權
# 著作權
```

## 結語

GAN 是深度學習領域的重要創新，它開創了生成模型的新時代。從影像生成到藝術創作，GAN 的應用範圍廣泛。然而，GAN 也帶來了新的倫理和社會問題，需要社會共同面對和解決。

---

## 延伸閱讀

- [GAN+生成對抗網路](https://www.google.com/search?q=GAN+generative+adversarial+network+Ian+Goodfellow)
- [DCGAN+影像生成](https://www.google.com/search?q=DCGAN+deep+convolutional+GAN+image+generation)
- [GAN+藝術創作](https://www.google.com/search?q=GAN+art+artificial+intelligence)

---

*本篇文章為「AI 程式人雜誌 2017 年 2 月號」文章系列之一。*