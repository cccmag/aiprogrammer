# 本期焦點

## 電腦視覺的進展：從 CNN 到 Vision Transformer

### 引言

電腦視覺是人工智慧最活躍的領域之一。從 2012 年 AlexNet 在 ImageNet 比賽中突破性獲勝，到 2020 年 Vision Transformer 的興起，深度學習徹底改變了我們處理圖像和影片的方式。

本期歷史回顧將帶領讀者探索電腦視覺的關鍵發展，從經典的 CNN 架構到最新的 Vision Transformer。

---

## 大綱

* [程式：實作簡單的 CNN](focus_code.md)
   - 用 Python 和 NumPy 實作卷積神經網路

1. [CNN 的基礎與經典架構](focus1.md)
   - 卷積、池化、感受野
   - LeNet, AlexNet, VGG

2. [ResNet 與深度網路的突破](focus2.md)
   - 殘差連接
   - 為何深層網路難以訓練

3. [EfficientNet：效率與效能的平衡](focus3.md)
   - 複合縮放
   - 深度可分離卷積

4. [Vision Transformer (ViT) 的興起](focus4.md)
   - 將 Transformer 應用於圖像
   - Patch Embedding

5. [物體檢測的進展](focus5.md)
   - R-CNN, Fast R-CNN, Faster R-CNN
   - YOLO, SSD

6. [語義分割與實例分割](focus6.md)
   - FCN, U-Net
   - Mask R-CNN

7. [未來展望：視覺的 Transformer 時代](focus7.md)
   - 多模態學習
   - 自監督視覺學習

---

## 濃縮回顧

### CNN 的核心運算

```
輸入圖像 -> 卷積層 -> 激活函數 -> 池化層 -> ... -> 全連接層 -> 輸出
```

- **卷積**：提取局部特徵
- **池化**：減少空間尺寸
- **激活函數**：引入非線性

### 經典架構演化

| 年份 | 模型 | 創新 |
|------|------|------|
| 1998 | LeNet | 早期 CNN |
| 2012 | AlexNet | 深度學習突破 |
| 2014 | VGGNet | 更深的網路 |
| 2015 | GoogLeNet | Inception 模組 |
| 2015 | ResNet | 殘差連接 |

### 2020 年的轉折

Vision Transformer (ViT) 論文發表（2020年末），展示了 Transformer 可以應用於圖像分類，挑戰了 CNN 的主導地位。

---

## 結論與展望

電腦視覺正處在一個轉型期：CNN 仍然是主力，但 Transformer 正在快速崛起。未來的趨勢可能是兩者的結合。

---

## 延伸閱讀

- [CNN 基礎](focus1.md)
- [ResNet](focus2.md)
- [EfficientNet](focus3.md)
- [Vision Transformer](focus4.md)
- [物體檢測](focus5.md)
- [語義分割](focus6.md)
- [未來展望](focus7.md)

---

*本期焦點到此結束。感謝閱讀本期 AI 程式人雜誌。*