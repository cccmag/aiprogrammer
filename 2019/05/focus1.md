# 電腦視覺與神經網路

## CNN 的起源與發展

卷積神經網路的概念可以追溯到 1990 年代，但真正爆發是在 2012 年 AlexNet 之後。

---

## 早期發展

### 感受野的概念

David Hubel 和 Torsten Wiesel 在 1960 年代對貓的視覺系統研究發現：

```
簡單細胞 → 邊緣檢測
複雜細胞 → 對方向不變
```

這種層次化的資訊處理啟發了後來的神經網路設計。

### LeNet（1998）

Yann LeCun 等人提出 LeNet-5，這是最早的 CNN 架構之一：

```python
# LeNet-5 結構
# Input(32x32) → Conv(6,5x5) → Pool(2x2) → Conv(16,5x5) → Pool(2x2)
# → Conv(120,5x5) → FC(84) → Output(10)
```

應用於手寫數字辨識（MNIST）。

---

## AlexNet：突破時刻（2012）

### 關鍵創新

2012 年，Alex Krizhevsky 等人在 ImageNet 競賽中以 16.4% 的錯誤率大幅領先第二名的 26.2%。

**技術突破**：

1. **深度**：8 層網路
2. **ReLU**：使用 ReLU 啟動函數
3. **GPU 訓練**：使用 GTX 580 加速
4. **Dropout**：防止過擬合
5. **Data Augmentation**：增加訓練樣本

### 架構

```python
# AlexNet 簡化結構
Conv(96, 11x11, stride=4) → ReLU → Pool(3x3) → Norm
Conv(256, 5x5) → ReLU → Pool(3x3) → Norm
Conv(384, 3x3) → ReLU
Conv(384, 3x3) → ReLU
Conv(256, 3x3) → ReLU → Pool(3x3)
FC(4096) → ReLU → Dropout
FC(4096) → ReLU → Dropout
FC(1000)
```

---

## 與傳統方法的比較

### 傳統電腦視覺

```python
# 傳統方法流程
extractor = SIFT()  # 特徴點提取
keypoints = extractor.detect(image)
descriptor = extractor.compute(image, keypoints)

matcher = BFMatcher()
matches = matcher.match(descriptor1, descriptor2)
```

缺點：
- 手動設計特徵
- 難以擴展到新類別
- 受光照、角度影響大

### 深度學習方法

```python
# 深度學習方法
model = load_pretrained_cnn()
features = model.extract(image)
prediction = classifier.predict(features)
```

優點：
- 自動學習特徵
- 端到端訓練
- 泛化能力強

---

## ImageNet 競賽歷史

| 年份 | 模型 | Top-5 錯誤率 |
|-----|------|------------|
| 2010 | SIFT + FVs | 28.2% |
| 2011 | Classifier Ensemble | 25.7% |
| 2012 | AlexNet | 16.4% |
| 2013 | VGG | 7.3% |
| 2014 | GoogLeNet | 6.7% |
| 2014 | VGG-19 | 7.3% |
| 2015 | ResNet | 3.6% |

---

## CNN 的核心思想

### 局部連接

每個神經元只連接輸入的一部分：

```
傳統：每個神經元連接所有輸入
CNN：每個神經元只連接局部區域
```

### 權重共用

同一層使用相同的卷積核：

```python
# 權重共用大幅減少參數
# 輸入 1000x1000, 隱藏 1M
# 傳統：1000*1000*1M = 10^12 參數
# CNN：100*100*100 = 10^6 參數
```

### 層次化特徵

```
低層特徵：邊緣、角落、紋理
    ↓
中層特徵：形狀、部件
    ↓
高層特徵：物體、場景
```

---

## 為什麼 CNN 有效？

### 平移不變性

CNN 對物體位置的變化更加魯棒：

```python
# 同一張圖經過 Pooling 後
# 物體稍微移動仍然能被檢測
```

### 空間層次結構

```python
# 層層抽象
Conv1: 邊緣 → 紋理
Conv2: 紋理 → 圖案
Conv3: 圖案 → 部件
Conv4: 部件 → 物體
```

---

## 延伸閱讀

- [AlexNet 原始論文](https://www.google.com/search?q=AlexNet+Krizhevsky+2012)
- [CNN 歷史回顧](https://www.google.com/search?q=history+convolutional+neural+networks)
- [LeNet 詳解](https://www.google.com/search?q=LeNet+LeCun+1998)

---

*本篇文章為「AI 程式人雜誌 2019 年 5 月號」系列文章之一。*