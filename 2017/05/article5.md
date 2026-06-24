# 文章 5：影像處理與濾波器

## 前言

濾波器是影像處理的基礎工具，可用於去噪、邊緣檢測、銳化等任務。本章節介紹常見的影像濾波器及其實現。

## 卷積核與濾波器

```python
import numpy as np
from scipy import ndimage

def apply_kernel(image, kernel):
    return ndimage.convolve(image, kernel, mode='constant')
```

## 常見濾波器

### 1. 均值濾波（平滑）

```python
mean_kernel = np.ones((3, 3)) / 9
smoothed = apply_kernel(image, mean_kernel)
```

### 2. 高斯濾波

```python
from scipy.ndimage import gaussian_filter

smoothed = gaussian_filter(image, sigma=1)
```

### 3. 銳化濾波

```python
sharp_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])
sharpened = apply_kernel(image, sharp_kernel)
```

### 4. 邊緣檢測

#### Sobel 算子

```python
sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

gx = apply_kernel(image, sobel_x)
gy = apply_kernel(image, sobel_y)
edges = np.sqrt(gx**2 + gy**2)
```

#### Laplacian 算子

```python
laplacian = np.array([
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0]
])
edges = apply_kernel(image, laplacian)
```

## 中值濾波

對脈衝噪聲（椒鹽噪聲）效果好：

```python
from scipy.ndimage import median_filter

filtered = median_filter(image, size=3)
```

## 頻率域處理

### 傅立葉變換

```python
import numpy as np

# 2D FFT
F = np.fft.fft2(image)
F_shifted = np.fft.fftshift(F)
magnitude = np.abs(F_shifted)

# 顯示頻譜
plt.imshow(np.log1p(magnitude), cmap='gray')
```

### 低通與高通濾波

```python
# 低通濾波 - 只保留低頻（模糊）
rows, cols = image.shape
crow, ccol = rows // 2, cols // 2
mask = np.zeros((rows, cols))
mask[crow-30:crow+30, ccol-30:ccol+30] = 1
low_pass = F_shifted * mask
```

## 總結

影像濾波器是電腦視覺的基礎工具。這些傳統方法在深度學習時代仍然重要，可作為預處理或與深度方法結合使用。

## 延伸閱讀

- https://www.google.com/search?q=image+filter+convolution+edge+detection
- https://www.google.com/search?q=Sobel+Laplacian+edge+detection+python