# 電腦視覺概述

## 什麼是電腦視覺？

電腦視覺（Computer Vision）旨在讓電腦能夠「看懂」圖像和影片。從具體物體到抽象概念，從二維圖像到三維場景重建，都是電腦視覺的研究範疇。

## 核心任務

### 1. 圖像分類（Image Classification）

辨識圖像屬於哪個類別。

```
圖像 → [模型] → 類別（貓/狗/車）
```

### 2. 物體偵測（Object Detection）

找出圖像中所有物體的位置與類別。

```
圖像 → [模型] → [(邊界框, 類別), ...]
```

### 3. 語意分割（Semantic Segmentation）

為每個像素標記類別。

```
圖像 → [模型] → 像素級類別標籤
```

### 4. 實例分割（Instance Segmentation）

區分同類別的不同個體。

```
圖像 → [模型] → 每個物體的獨立分割區域
```

### 5. 人體姿態估計（Pose Estimation）

偵測人體關鍵點位置。

```python
# 概念範例
keypoints = {
    "nose": (100, 50),
    "left_eye": (95, 45),
    "right_eye": (105, 45),
    "left_shoulder": (80, 80),
    "right_shoulder": (120, 80),
}
```

## 傳統方法 vs 深度學習

### 傳統電腦視覺

```python
# SIFT 特徵提取
import cv2
img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
sift = cv2.xfeatures2d.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(gray, None)
```

常用方法：
- SIFT、SURF、ORB 特徵點偵測
- HOG（方向梯度直方圖）
- Haar 特徵用於人臉偵測

### 深度學習方法

```python
# 使用預訓練模型進行分類
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
import numpy as np

model = ResNet50(weights='imagenet')
img_path = 'elephant.jpg'
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
predictions = model.predict(x)
```

常用模型：
- AlexNet、VGG、GoogLeNet、ResNet
- R-CNN、YOLO、SSD 用於物體偵測

## 應用場景

| 應用 | 說明 |
|------|------|
| 人臉辨識 | 門禁系統、手機解鎖 |
| 自駕車 | 行人偵測、交通號誌辨識 |
| 醫療影像 | X光、CT 影像分析 |
| 品質檢測 | 工廠產品缺陷偵測 |
| 監控系統 | 異常行為偵測 |
| AR/VR | 場景理解與互動 |

## 重要資料集

| 資料集 | 說明 |
|--------|------|
| ImageNet | 1400萬張圖像，2萬類別 |
| COCO | 33萬張圖像，80類別，目標偵測標注 |
| Pascal VOC | 訓練/驗證/測試，20類別 |
| MNIST | 手寫數字辨識 |
| CIFAR-10 | 60000張 32x32 影像，10類別 |

## 評估指標

### 精確率（Precision）

預測為正的樣本中，實際為正的比例。

```
Precision = TP / (TP + FP)
```

### 召回率（Recall）

實際為正的樣本中，被正確預測的比例。

```
Recall = TP / (TP + FN)
```

### mAP（mean Average Precision）

物體偵測常用的評估指標。

## 總結

電腦視覺經歷了從特徵工程到深度學習的重大轉變。2012 年 AlexNet 的成功開創了新時代。此後 CNN 架構不斷創新，物體偵測方法層出不窮，達到甚至超越人類水準。