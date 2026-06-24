# 卷積運算原理

## 什麼是卷積？

卷積是兩個函數的數學運算，產生第三個函數。在影像處理中：
- **輸入影像**：f(x, y)
- **卷積核/濾波器**：g(x, y)
- **輸出特徵圖**：h(x, y) = f * g

## 2D 卷積定義

h(x, y) = Σ Σ f(i, j) · g(x-i, y-j)
          i   j

或等價地：

h(x, y) = Σ Σ f(x-i, y-j) · g(i, j)
          i   j

## 簡單實現

```python
import numpy as np

def conv2d(image, kernel, stride=1, padding=0):
    """2D 卷積運算"""
    if padding > 0:
        image = np.pad(image, padding, mode='constant')

    kh, kw = kernel.shape
    ih, iw = image.shape

    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1

    output = np.zeros((out_h, out_w))

    for i in range(0, ih - kh + 1, stride):
        for j in range(0, iw - kw + 1, stride):
            output[i // stride, j // stride] = np.sum(
                image[i:i+kh, j:j+kw] * kernel
            )

    return output
```

## 卷積核類型

### 1. 邊緣偵測

```python
# Sobel X
sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

# Sobel Y
sobel_y = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]])

# Laplacian（邊緣與細節）
laplacian = np.array([[0, 1, 0],
                      [1, -4, 1],
                      [0, 1, 0]])
```

### 2. 模糊/平滑

```python
# 均值模糊
blur = np.ones((3, 3)) / 9

# 高斯模糊
gaussian = np.array([[1, 2, 1],
                     [2, 4, 2],
                     [1, 2, 1]]) / 16

# 更多高斯
# 5x5
gaussian_5 = np.array([
    [1, 4, 6, 4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, 36, 24, 6],
    [4, 16, 24, 16, 4],
    [1, 4, 6, 4, 1]
]) / 256
```

### 3. 銳化

```python
sharpen = np.array([[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]])

# 強銳化
sharpen_strong = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
```

## 卷積的屬性

### 1. 交換律
f * g = g * f

### 2. 結合律
(f * g) * h = f * (g * h)

### 3. 分配律
f * (g + h) = f * g + f * h

## 填充（Padding）

控制輸出尺寸與邊緣處理。

```python
# valid：無填充，輸出變小
# same：填充使輸出等於輸入
# full：完全交叉相關

# 計算 same 填充
def get_padding(kernel_size):
    return (kernel_size - 1) // 2
```

## 步長（Stride）

控制卷積核移動的間距。

```python
# stride=1：每步移動 1 像素
# stride=2：每步移動 2 像素

# 輸出尺寸計算
# out_size = floor((input_size - kernel_size + 2*padding) / stride) + 1
```

## 多通道卷積

```python
# 輸入: H x W x C_in
# 輸出: H' x W' x C_out

def multi_channel_conv2d(volume, kernels):
    """
    volume: (H, W, C_in)
    kernels: (K, K, C_in, C_out)
    """
    h, w, c_in = volume.shape
    k, k2, c_in2, c_out = kernels.shape

    out = np.zeros((h, w, c_out))
    for c in range(c_out):
        for ci in range(c_in):
            out[:, :, c] += conv2d(volume[:, :, ci],
                                   kernels[:, :, ci, c])
    return out
```

## 深度學習中的卷積

```python
# 在 CNN 中
# 輸入: (batch, height, width, channels)
# 權重: (kernel_h, kernel_w, in_channels, out_channels)
# 輸出: (batch, out_h, out_w, out_channels)
```

## 轉置卷積（Deconvolution）

上採樣操作，用於生成網路。

```python
def conv2d_transpose(x, kernel, stride=1, padding=0):
    """轉置卷積（上採樣）"""
    # 實現較複雜，這裡是概念示意
    h, w = x.shape
    kh, kw = kernel.shape

    # 插入零
    out_h = h * stride + kh - 1 - 2 * padding
    out_w = w * stride + kw - 1 - 2 * padding

    return out_h, out_w
```

## 總結

卷積是CNN的核心運算：
- 卷積核在輸入上滑動，計算加權和
- 不同卷積核提取不同特徵（邊緣、紋理等）
- 填充與步長控制輸出尺寸
- 多通道輸入輸出透過多個卷積核實現