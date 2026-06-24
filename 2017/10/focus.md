# 本期焦點

## 生成對抗網路 (GAN) 的崛起

### 引言

在深度學習的領域中，有一個概念自 2014 年誕生以來就持續引發研究熱潮——這就是生成對抗網路（Generative Adversarial Network，簡稱 GAN）。由 Ian Goodfellow 及其同事在 2014 年提出，GAN 透過一種獨特的「對抗」訓練機制，讓兩個神經網路相互競爭、相互學習，從而能夠生成極為逼真的影像、音訊或文字。

本期，我們將深入探討 GAN 的發展歷程，從基礎理論到最新應用，從學術研究到實際落地。

---

## 大綱

* [程式：GAN 實作](focus_code.md)
   - DCGAN 架構
   - PyTorch 實作
   - 簡單的影像生成

1. [GAN 基礎：生成對抗網路的誕生（2014）](focus1.md)
   - Ian Goodfellow 與對抗訓練
   - GAN 的基本架構
   - 理論基礎：零和遊戲

2. [DCGAN：深度卷積 GAN 的突破（2015-2016）](focus2.md)
   - 卷積層的應用
   - Batch Normalization
   - 潜在空間的語義特徵

3. [GAN 訓練技巧：Mode Collapse 與解決方案](focus3.md)
   - Mode Collapse 問題
   - 梯度問題
   - 訓練穩定化技術

4. [WGAN 與條件式 GAN：穩定訓練的新方法](focus4.md)
   - Wasserstein GAN
   - Earth Mover Distance
   - 條件式生成

5. [GAN 應用：影像生成與風格轉換](focus5.md)
   - 影像生成
   - 超解析度重建
   - 風格遷移

6. [GAN 在其他領域的應用](focus6.md)
   - 文字生成
   - 藥物發現
   - 資料增強

7. [GAN 的未來發展](focus7.md)
   - 從影像到多模態
   - 可解釋性生成
   - 安全與倫理

---

## 濃縮回顧

### GAN 的誕生

2014 年，Ian Goodfellow 在酒吧與朋友的討論中激發了靈感，發明了生成對抗網路。其核心思想是：

```
┌─────────────────────────────────────────────────────┐
│                  GAN 架構                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│   生成器 (Generator)     判別器 (Discriminator)    │
│        │                        │                  │
│        │    ┌──────────────────┘                   │
│        │    │                                        │
│        │    ▼                                        │
│        │   真實資料 ←──── 假的資料                  │
│        │    │                                        │
│        │    └───────────────────────────────────    │
│        │                    │                        │
│        └────────────────────┘                        │
│              對抗訓練                                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

生成器 G 負責生成假資料，判別器 D 負責區分真假。兩者形成零和遊戲，最終達到 Nash 均衡。

### 損失函數

GAN 的目標函數：
```python
min_G max_D V(D, G) = E_x~p_data[log D(x)] + E_z~p_z[log(1 - D(G(z)))]
```

- 判別器 D 最大化目標：正確分類真實資料為 1，假資料為 0
- 生成器 G 最小化目標：欺騙判別器，讓判別器認為假資料是真的

### DCGAN 的貢獻

2015-2016 年提出的 DCGAN（Deep Convolutional GAN）解決了 GAN 訓練不穩定的問題：

- 使用轉置卷積替代池化層
- 採用 Batch Normalization
- 使用 Leaky ReLU 激活函數
- 移除全連接層

### Mode Collapse

Mode Collapse 是 GAN 訓練中的主要問題——生成器只學習到資料分佈的一部分模式，忽略了其他模式。解決方案包括：

- Wasserstein GAN (WGAN)
- 最小二乘 GAN (LSGAN)
- Unrolled GAN
- 資料增強

---

## 為什麼 GAN 重要？

GAN 的出現解決了生成模型的多個難題：

1. **Implicit Generative Model**：不同於明確建模機率分佈，GAN 透過對抗訓練隱式學習分佈
2. **High Quality Generation**：可以生成極為逼真的影像
3. **Flexible Loss**：不需要明確的損失函數定義
4. **Unsupervised Learning**：可以从无标注数据中学习

---

## 結論

從 2014 年 Ian Goodfellow 的開創性論文到 2017 年的多樣應用，GAN 已经证明了其在生成模型领域的强大潜力。尽管仍然存在训练不稳定、Mode Collapse 等挑战，但研究界正在快速推进这一领域的发展。

在下個章節中，我們將深入探討 GAN 的各個面向，從基礎理論到賽際應用。

---

## 延伸閱讀

- [GAN 原始論文：Generative Adversarial Networks](https://www.google.com/search?q=Goodfellow+GAN+2014+paper)
- [DCGAN 論文：Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks](https://www.google.com/search?q=DCGAN+Radford+2015+paper)
- [WGAN 論文：Wasserstein GAN](https://www.google.com/search?q=Wasserstein+GAN+Arjovsky+2017+paper)

---

*本期焦點到此結束。下期我們將聚焦另一個影響深遠的主題，敬請期待。*