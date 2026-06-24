# 文章 6：電腦視覺導論

## 前言

電腦視覺（Computer Vision）旨在讓電腦理解和處理影像。本章節介紹電腦視覺的基本概念、發展歷程與主要任務。

## 什麼是電腦視覺

電腦視覺是人工智慧的一個分支，目標是讓電腦能夠「看懂」影像和影片。

人的視覺系統每秒處理大量資訊，而我們希望電腦也能做到類似的事情。

## 主要任務

### 1. 影像分類（Image Classification）

給定影像，辨識其中的物體類別：

```python
labels = ['cat', 'dog', 'bird', 'fish']
prediction = model.predict(image)
predicted_label = labels[np.argmax(prediction)]
```

### 2. 物體偵測（Object Detection）

不僅辨識類別，還要定位位置：

```python
# 輸出邊界框與類別
boxes, classes, confidences = model.detect(image)
```

### 3. 語義分割（Semantic Segmentation）

對每個像素分類：

```python
# 輸出每像素的類別
segmentation_map = model.segment(image)
```

### 4. 人臉識別（Face Recognition）

辨識身份：

```python
embedding = face_model.embed(face_image)
```

## 發展歷程

### 1960-1980：規則系統
- 邊緣檢測、線條擬合
- 專家系統，基於規則的方法

### 1980-2000：傳統機器學習
- SIFT、HOG 等特徵提取
- SVM、隨機森林等分類器

### 2012-至今：深度學習
- CNN 突破 ImageNet
- 特徵學習替代手工特徵
- 端到端學習

## 經典數據集

| 數據集 | 說明 |
|--------|------|
| MNIST | 手寫數字 |
| CIFAR-10/100 | 32x32 自然影像 |
| ImageNet | 1400萬張，1000類 |
| COCO | 目標檢測與分割 |

## 應用領域

- 自動駕駛
- 醫學影像分析
- 人臉識別系統
- 影片監控
- AR/VR

## 總結

電腦視覺經歷了從規則系統到深度學習的演變。CNN 的出現徹底改變了這個領域，使许多視覺任務的準確率大幅提升。

## 延伸閱讀

- https://www.google.com/search?q=computer+vision+introduction+overview
- https://www.google.com/search?q=image+classification+object+detection+history