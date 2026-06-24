# 焦點文章 2：卷積層原理

## 前言

卷積層是 CNN 的核心元件，負責從輸入中提取特徵。本章節詳細解說卷積操作的數學原理與實際意義。

## 卷積的直覺理解

卷積可以理解為一個「濾鏡」在影像上滑動：

```
輸入影像 * 卷積核 = 特徵圖
```

卷積核就像是一個「特徵偵測器」：
- 垂直邊緣濾鏡檢測垂直邊緣
- 水平邊緣濾鏡檢測水平邊緣
- 更多層的濾鏡檢測更複雜的圖案

## 卷積的數學定義

對於二維離散卷積：

```
(output)[i,j] = Σ Σ (kernel)[m,n] × (input)[i+m, j+n]
```

在 CNN 中，通常使用互相關（Cross-Correlation）：

```python
import numpy as np

def conv2d(image, kernel, stride=1, padding=0):
    if padding > 0:
        image = np.pad(image, padding, mode='constant')

    kh, kw = kernel.shape
    ih, iw = image.shape

    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1

    output = np.zeros((out_h, out_w))
    for i in range(0, out_h, stride):
        for j in range(0, out_w, stride):
            output[i // stride, j // stride] = np.sum(
                image[i:i+kh, j:j+kw] * kernel
            )
    return output
```

## 卷積核的視覺化效果

不同的卷積核產生不同的效果：

| 卷積核類型 | 效果 |
|------------|------|
| 銳化濾鏡 | 增強邊緣 |
| 模糊濾鏡 | 平滑影像 |
| 邊緣檢測 | 提取輪廓 |

### 常見濾鏡

```python
import scipy.ndimage as ndimage

# 銳化
sharp_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])

# 邊緣檢測
edge_kernel = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
])
```

## 卷積層的關鍵參數

### 1. 卷積核大小（Kernel Size）

常見大小：1×1、3×3、5×5、7×7

較大的卷積核能捕捉更大的感受野，但計算量也更大。

### 2. 步長（Stride）

卷積核每次移動的像素數：

- Stride=1：每個位置都計算
- Stride=2：跳過一個位置

### 3. 填充（Padding）

在輸入邊緣添加像素：

| 類型 | 效果 |
|------|------|
| Valid | 不填充，輸出變小 |
| Same | 填充保持輸出大小 |

### 4. 特徵圖數量

每個卷積層可以有多個卷積核，每個產生一個特徵圖：

```
Input: H × W × C_in
Output: H' × W' × C_out
```

其中 C_out 等於卷積核數量。

## 多通道卷積

彩色影像有三個通道（RGB）：

```python
# 輸入：H × W × 3
# 輸出：H' × W' × N（N 個卷積核）
```

每個卷積核同時作用於所有輸入通道。

## 總結

卷積層透過局部連接與權重共享，能有效提取影像特徵。理解卷積的參數（核大小、步長、填充）是設計 CNN 的基礎。

## 延伸閱讀

- https://www.google.com/search?q=convolutional+layer+stride+padding+explained
- https://www.google.com/search?q=CNN+kernel+filter+visualization