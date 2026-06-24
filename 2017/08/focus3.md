# 卷積神經網路（CNN）

## CNN 的核心概念

卷積神經網路（Convolutional Neural Network）是深度學習在視覺領域的核心架構。透過卷積層自動學習特徵，取代了傳統的手工特徵工程。

## 基本架構

```
輸入圖像
    ↓
卷積層 → 特徵提取
    ↓
池化層 → 降維
    ↓
卷積層 → 更抽象的特徵
    ↓
池化層
    ↓
全連接層 → 分類
    ↓
輸出
```

## 卷積運算

### 什麼是卷積？

卷積是濾波器（Kernel）與輸入影像的局部運算。

```python
import numpy as np

def convolution2d(image, kernel, padding=0, stride=1):
    # 確保影像為 2D
    if len(image.shape) > 2:
        image = np.mean(image, axis=-1)

    # 應用填充
    if padding > 0:
        image = np.pad(image, padding, mode='constant')

    # 計算輸出尺寸
    out_h = (image.shape[0] - kernel.shape[0]) // stride + 1
    out_w = (image.shape[1] - kernel.shape[1]) // stride + 1
    output = np.zeros((out_h, out_w))

    # 卷積運算
    for i in range(0, out_h, stride):
        for j in range(0, out_w, stride):
            output[i, j] = np.sum(
                image[i:i+kernel.shape[0], j:j+kernel.shape[1]] * kernel
            )

    return output

# 範例：邊緣偵測卷積核
image = np.array([
    [10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10],
    [0, 0, 0, 0, 0],
    [20, 20, 20, 20, 20],
    [20, 20, 20, 20, 20],
])

# Sobel 邊緣偵測核
sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
result = convolution2d(image, sobel_x)
print(result)
```

### 常見卷積核

```python
# 銳化核
sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

# 邊緣偵測
edge = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])

# 模糊核（均值）
blur = np.ones((3, 3)) / 9
```

## 池化層（Pooling）

降低特徵圖維度，同時保留重要資訊。

### Max Pooling

```python
def max_pooling(image, pool_size=2, stride=2):
    h, w = image.shape[:2]
    out_h = h // stride
    out_w = w // stride

    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            i_start = i * stride
            j_start = j * stride
            output[i, j] = np.max(
                image[i_start:i_start+pool_size, j_start:j_start+pool_size]
            )

    return output
```

### Average Pooling

```python
def avg_pooling(image, pool_size=2, stride=2):
    h, w = image.shape[:2]
    out_h = h // stride
    out_w = w // stride

    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            i_start = i * stride
            j_start = j * stride
            output[i, j] = np.mean(
                image[i_start:i_start+pool_size, j_start:j_start+pool_size]
            )

    return output
```

## Keras 實作 CNN

```python
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

model = Sequential([
    # 第一個卷積區塊
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),

    # 第二個卷積區塊
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),

    # 第三個卷積區塊
    Conv2D(64, (3, 3), activation='relu'),

    # 全連接層
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')  # MNIST 10 類別
])

model.summary()
```

## 卷積層參數

| 參數 | 說明 | 常用值 |
|------|------|--------|
| filters | 卷積核數量 | 32, 64, 128 |
| kernel_size | 卷積核大小 | 3x3, 5x5 |
| stride | 移動步長 | 1, 2 |
| padding | 邊界填充 | 'valid', 'same' |
| activation | 激活函數 | relu, sigmoid |

## 著名 CNN 架構

### LeNet-5 (1998)

最早的成功 CNN，用於手寫數字辨識。

```python
# LeNet-5 架構概念
lenet = Sequential([
    Conv2D(6, (5, 5), activation='tanh', input_shape=(32, 32, 1)),
    AveragePooling2D((2, 2)),
    Conv2D(16, (5, 5), activation='tanh'),
    AveragePooling2D((2, 2)),
    Conv2D(120, (5, 5), activation='tanh'),
    Flatten(),
    Dense(84, activation='tanh'),
    Dense(10, activation='softmax'),
])
```

### AlexNet (2012)

ImageNet 競賽冠軍，開啟深度學習視覺時代。

- 8 層網路
- ReLU 激活函數
- Dropout 正規化
- GPU 訓練

### VGG (2014)

簡單架構，深網路：
- 僅使用 3x3 卷積核
- 深度達 16-19 層
- 結構一致，易於理解

## CNN 的優勢

1. **局部連接**：減少參數量
2. **權值共用**：同一卷積核用於所有位置
3. **平移不變性**：物體位置變化不影響辨識
4. **層次化特徵**：淺層邊緣，深層物體

## 總結

CNN 是現代電腦視覺的基礎。卷積層提取特徵，池化層降維，全連接層分類。從 LeNet 到 ResNet，架構不斷創新，效能持續提升。