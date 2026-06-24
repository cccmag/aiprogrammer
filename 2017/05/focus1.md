# 焦點文章 1：卷積神經網路簡介

## 前言

卷積神經網路（Convolutional Neural Network, CNN）是深度學習在電腦視覺領域的核心技術。本章節介紹 CNN 的基本概念、核心元件與應用領域。

## 與全連接網路的區別

傳統的全連接（Fully Connected）網路：
- 每個神經元與上一層所有神經元相連
- 參數量大，難以處理高維輸入
- 忽略空間結構

CNN 的創新：
- **局部連接**：每個神經元只連接輸入的局部區域
- **權重共享**：同一卷積核在整個輸入上共享權重
- 保留輸入的空間結構

## CNN 的三大組成部分

### 1. 卷積層（Convolutional Layer）

使用卷積核在輸入上滑動，提取特徵：

```python
import numpy as np

def convolve2d(image, kernel, stride=1, padding=0):
    if padding > 0:
        image = np.pad(image, padding, mode='constant')
    output_shape = ((image.shape[0] - kernel.shape[0]) // stride + 1,
                    (image.shape[1] - kernel.shape[1]) // stride + 1)
    output = np.zeros(output_shape)
    for i in range(0, output_shape[0], stride):
        for j in range(0, output_shape[1], stride):
            output[i, j] = np.sum(image[i:i+kernel.shape[0], j:j+kernel.shape[1]] * kernel)
    return output
```

### 2. 池化層（Pooling Layer）

下採樣特徵圖，减少計算量並提供平移不變性：

- **最大池化（Max Pooling）**：取區域最大值
- **平均池化（Average Pooling）**：取區域平均值

### 3. 全連接層（Fully Connected Layer）

在網路末端，将特徵圖展平後進行分類。

## CNN 特徵學習能力

CNN 能自動學習層次化的特徵表示：

| 層次 | 學習到的特徵 |
|------|--------------|
| 淺層 | 邊緣、紋理、顏色 |
| 中層 | 形狀、物體部件 |
| 深層 | 完整物體、語義概念 |

## CNN 的應用領域

- **影像分類**：ImageNet 競賽
- **物體偵測**：YOLO、Faster R-CNN
- **語義分割**：FCN、U-Net
- **人臉識別**：FaceNet、DeepID
- **風格遷移**：神經風格轉換

## CNN 發展里程碑

1. **1998 LeNet**：在手寫數字辨識取得成功
2. **2012 AlexNet**：ImageNet 突破，深度學習覺醒
3. **2014 VGG/GoogLeNet**：更深更複雜的架構
4. **2015 ResNet**：殘差連接解決深度網路訓練問題

## 總結

CNN 是電腦視覺深度學習的基礎架構。透過局部連接與權重共享，CNN 能有效處理高維影像資料並學習層次化特徵。

## 延伸閱讀

- https://www.google.com/search?q=CNN+convolutional+neural+network+introduction
- https://www.google.com/search?q=LeNet+AlexNet+CNN+history