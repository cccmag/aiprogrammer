# 卷積運算

## 濾波器與特徵擷取

卷積運算是 CNN 的核心。它透過濾波器（卷積核）在輸入影像上滑動，提取有意義的特徵。

---

## 卷積運算原理

### 基本概念

```python
import numpy as np

def convolution_2d(image, kernel, stride=1, padding=0):
    """
    2D 卷積運算
    """
    if padding > 0:
        image = np.pad(image, ((padding, padding), (padding, padding)), mode='constant')

    kh, kw = kernel.shape
    ih, iw = image.shape

    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1

    output = np.zeros((out_h, out_w))

    for i in range(0, out_h * stride, stride):
        for j in range(0, out_w * stride, stride):
            region = image[i:i+kh, j:j+kw]
            output[i//stride, j//stride] = np.sum(region * kernel)

    return output
```

### 視覺化解釋

```
輸入影像 (5x5):              卷積核 (3x3):           輸出特徵圖 (3x3):
[1 2 3 4 5]                 [0 1 0]              [?? ?? ??]
[5 4 3 2 1]    *            [1 2 1]        =      [?? ?? ??]
[1 2 3 4 5]                 [0 1 0]              [?? ?? ??]
[5 4 3 2 1]
[1 2 3 4 5]
  ─────────────────────────►
        滑動窗口
```

### 計算過程

```python
# 滑動窗口計算
# 每個位置：element-wise 乘法後求和
# (-1)*1 + 0*2 + 1*3 + (-1)*5 + 0*4 + 1*3 + (-1)*1 + 0*2 + 1*3 = 0
```

---

## 卷積核的類型

### 邊緣檢測

```python
# Sobel 邊緣檢測
sobel_x = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
])

sobel_y = np.array([
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]
])
```

### 模糊/平滑

```python
# 平均模糊
box_blur = np.ones((3, 3)) / 9

# 高斯模糊
gaussian = np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
]) / 16
```

### 銳化

```python
# 銳化卷積核
sharpen = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])
```

### 特徵映射

```
┌─────────────────────────────────────────────────────────┐
│                    不同卷積核的效果                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  原始影像                                                 │
│     │                                                    │
│     ├──► 邊緣檢測 → 輪廓                                 │
│     │                                                    │
│     ├──► 模糊   → 平滑                                   │
│     │                                                    │
│     └──► 銳化   → 細節增強                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 填充與步長

### Valid vs Same

```python
# Valid 卷積（無填充）
# 輸出尺寸 = (輸入尺寸 - 卷積核尺寸) / 步長 + 1

# Same 卷積（填充後輸出與輸入相同）
# pad = (卷積核尺寸 - 1) / 2
```

### 步長（Stride）

```python
# stride=1: 每次移動 1 格
# stride=2: 每次移動 2 格（輸出尺寸減半）

def convolution_stride(image, kernel, stride):
    # 步長影響輸出尺寸
    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1
```

---

## 多通道卷積

### RGB 影像

```python
# 輸入：(H, W, 3) - 3 個通道
# 卷積核：(K, K, 3) - 必須匹配輸入通道
# 輸出：(H', W')

# 如果有多個卷積核
# 卷積核：(K, K, 3, num_filters)
# 輸出：(H', W', num_filters)
```

### 卷積層的表示

```python
# Keras 中的表示
from keras.layers import Conv2D

conv = Conv2D(
    filters=64,      # 輸出通道數
    kernel_size=(3, 3),  # 卷積核大小
    strides=(1, 1),  # 步長
    padding='same',  # 'valid' 或 'same'
    activation='relu'
)
```

---

## 1x1 卷積

1x1 卷積是一個看似簡單但非常重要的操作：

```python
# 1x1 卷積的作用
# 1. 降維/升維
# 2. 增加非線性
# 3. 通道間資訊整合

# 例如：192 通道 → 32 通道
# 輸入：(H, W, 192) → Conv(32, 1x1) → 輸出：(H, W, 32)
```

---

## 深度學習框架中的卷積

### TensorFlow

```python
import tensorflow as tf

output = tf.nn.conv2d(
    input,
    filter=kernel,
    strides=[1, 1, 1, 1],
    padding='SAME'
)
```

### PyTorch

```python
import torch
import torch.nn.functional as F

output = F.conv2d(
    input,
    weight=kernel,
    stride=1,
    padding=0
)
```

---

## 延伸閱讀

- [卷積運算詳解](https://www.google.com/search?q=convolution+operation+explained)
- [視覺化 CNN 特徵圖](https://www.google.com/search?q=CNN+feature+visualization)
- [卷積核的類型](https://www.google.com/search?q=types+of+convolution+kernels)

---

*本篇文章為「AI 程式人雜誌 2019 年 5 月號」系列文章之一。*