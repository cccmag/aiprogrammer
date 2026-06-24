# CNN 在影像辨識的突破

## 前言

卷積神經網路（CNN）已經成為影像辨識的標準方法。從 LeNet 到 ResNet，CNN 的演進代表了深度學習的成功。

## CNN 的核心組件

### 卷積層

使用濾波器提取特徵：

```python
Conv2D(filters=32, kernel_size=3, activation='relu')
```

### 池化層

減少空間維度：

```python
MaxPooling2D(pool_size=2)
```

### 全連接層

最終分類：

```python
Dense(units=10, activation='softmax')
```

## 經典架構

| 網路 | 年份 | 創新 |
|------|------|------|
| LeNet | 1998 | 早期 CNN |
| AlexNet | 2012 | 深度學習突破 |
| VGGNet | 2014 | 小型化濾波器 |
| ResNet | 2015 | 殘差連接 |
| Inception | 2015 | Inception 模組 |

## 應用場景

1. **影像分類**：物體辨識
2. **物體偵測**：YOLO、Faster R-CNN
3. **語義分割**：FCN、U-Net
4. **人臉識別**：DeepFace、FaceNet

## 結語

CNN 是電腦視覺的基礎，開創了深度學習的黃金時代。

---

**延伸閱讀**

- [CNN 教程](https://www.google.com/search?q=CNN+tutorial+convolutional+neural+network)
- [AlexNet 論文](https://www.google.com/search?q=AlexNet+2012+NIPS)