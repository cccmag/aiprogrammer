# 本期焦點

## 電腦視覺與 CNN 演進

### 引言

電腦視覺（Computer Vision）是人工智慧領域中最激動人心的研究方向之一。從 2012 年 AlexNet 在 ImageNet 比賽中震驚業界，到 2021 年 Vision Transformer 的崛起，電腦視覺經歷了革命性的變化。

本期，我們將回顧 CNN 的發展歷程，探討從 AlexNet 到 EfficientNet 的經典架構，也會介紹 Vision Transformer 如何顛覆傳統 CNN 的主導地位。更重要的是，我們將介紹 CLIP 和 DALL-E 等多模態模型，這些模型正在重新定義我們對電腦視覺的想像。

---

## 大綱

* [程式：CNN 與 Vision Transformer 實作](focus_code.md)
   - 卷積層、池化層的實現
   - 殘差連接機制
   - Vision Transformer 簡化版

1. [CNN 的崛起與發展：AlexNet 到 ResNet](focus1.md)
   - ImageNet 競賽與深度學習革命
   - AlexNet、VGG、GoogLeNet
   - CNN 架構設計原則

2. [ResNet 與深度殘差學習：解決深度網路訓練問題](focus2.md)
   - 梯度消失與網路退化問題
   - 殘差連接的突破
   - ResNet 的多種變體

3. [EfficientNet 與模型效率：複合縮放的智慧](focus3.md)
   - 複合縮放策略
   - 效率與效能的平衡
   - MobileNet、 EfficientNet 系列

4. [Vision Transformer (ViT)：Transformer 進軍電腦視覺](focus4.md)
   - 圖像 Patch 劃分
   - Self-Attention 在視覺中的應用
   - ViT 的優勢與挑戰

5. [CLIP 與對比學習：文字-圖像對齊](focus5.md)
   - 對比學習原理
   - CLIP 的訓練方法
   - 零樣本分類能力

6. [DALL-E 與生成式圖像：文字生成圖像](focus6.md)
   - DALL-E 的架構
   - 文字到圖像的生成
   - 創意與應用

7. [未來展望：電腦視覺的發展方向](focus7.md)
   - 多模態學習
   - 自監督學習
   - 產業應用前景

---

## 濃縮回顧

### CNN 的歷史性突破

2012 年，AlexNet 在 ImageNet 競賽中以壓倒性優勢獲勝，錯誤率僅 15.3%，遠低於第二名的 26.2%。這一結果標誌著深度學習時代的開始。

**CNN 的核心組件**：
- 卷積層：提取局部特徵
- 池化層：降低維度、增加不變性
- 全連接層：分類決策

### ResNet 的創新

2015 年，ResNet（Residual Network）在 ImageNet 比賽中提出，通過殘差連接解決了深度網路的訓練問題。152 層的深度網路首次成功訓練，收斂速度和效果都大幅提升。

### Vision Transformer 的崛起

2020 年，Google 發表 ViT（Vision Transformer），首次將 Transformer 完全應用於圖像分類。雖然一開始需要更多資料訓練，但其發展潛力巨大。

### CLIP 與多模態學習

2021 年 1 月，OpenAI 發表 CLIP，這是一種能夠理解文字和圖像關係的模型。CLIP 的零樣本分類能力顛覆了傳統的影像分類方法。

---

## 結論與展望

電腦視覺領域正在經歷一場前所未有的變革。CNN 仍然是許多應用的基礎，但 Transformer 的引入為這個領域帶來了新的可能性。

多模態學習（如 CLIP、DALL-E）正在模糊不同 AI 領域之間的界限。未來的電腦視覺系統將更加智能、通用，能够像人類一样理解視覺世界。

---

## 延伸閱讀

- [CNN 的崛起與發展](focus1.md)
- [ResNet 與深度殘差學習](focus2.md)
- [EfficientNet 與模型效率](focus3.md)
- [Vision Transformer (ViT)](focus4.md)
- [CLIP 與對比學習](focus5.md)
- [DALL-E 與生成式圖像](focus6.md)
- [未來展望](focus7.md)

---

*本期焦點到此結束。下期我們將探討強化學習基礎，敬請期待。*