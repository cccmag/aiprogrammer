# 特徵映射與池化

## 特徵映射（Feature Maps）

卷積層的輸出稱為特徵映射（Feature Maps）。每個卷積核產生一個特徵映射。

```
輸入影像 (RGB)
    ↓
卷積層 (32 個卷積核)
    ↓
32 個特徵映射 (每個 28x28)
```

## 卷積層的運算

```python
import numpy as np

def conv_layer(image, kernels, stride=1, padding=0):
    """
    模擬卷積層
    image: (H, W, C)
    kernels: (K, K, C, num_kernels)
    """
    kh, kw, kc, num_kernels = kernels.shape
    h, w, c = image.shape

    out_h = (h - kh + 2*padding) // stride + 1
    out_w = (w - kw + 2*padding) // stride + 1

    # 輸出 (out_h, out_w, num_kernels)
    output = np.zeros((out_h, out_w, num_kernels))

    for k in range(num_kernels):
        for i in range(out_h):
            for j in range(out_w):
                si, sj = i * stride, j * stride
                region = image[si:si+kh, sj:sj+kw, :]
                kernel = kernels[:, :, :, k]
                output[i, j, k] = np.sum(region * kernel)

    return output
```

## 池化（Pooling）

降低特徵圖尺寸，減少參數與計算量。

### 最大池化（Max Pooling）

取區域內最大值。

```python
def max_pooling(feature_map, pool_size=2, stride=2):
    h, w, c = feature_map.shape

    out_h = (h - pool_size) // stride + 1
    out_w = (w - pool_size) // stride + 1

    output = np.zeros((out_h, out_w, c))

    for i in range(out_h):
        for j in range(out_w):
            si, sj = i * stride, j * stride
            region = feature_map[si:si+pool_size, sj:sj+pool_size, :]
            output[i, j, :] = np.max(region, axis=(0, 1))

    return output
```

### 平均池化（Average Pooling）

取區域內平均值。

```python
def avg_pooling(feature_map, pool_size=2, stride=2):
    h, w, c = feature_map.shape

    out_h = (h - pool_size) // stride + 1
    out_w = (w - pool_size) // stride + 1

    output = np.zeros((out_h, out_w, c))

    for i in range(out_h):
        for j in range(out_w):
            si, sj = i * stride, j * stride
            region = feature_map[si:si+pool_size, sj:sj+pool_size, :]
            output[i, j, :] = np.mean(region, axis=(0, 1))

    return output
```

### 全域池化（Global Pooling）

每個特徵圖池化為單一值。

```python
def global_avg_pooling(feature_map):
    # 對每個 channel 取平均
    return np.mean(feature_map, axis=(0, 1))

def global_max_pooling(feature_map):
    # 對每個 channel 取最大
    return np.max(feature_map, axis=(0, 1))
```

## 池化的作用

1. **降低維度**：減少後續層的參數
2. **保持特徵**：主要保留最顯著的特征
3. **控制過擬合**：提供輕微的正則化
4. **旋轉/平移不變性**：輕微的幾何變化不影響輸出

## 展示池化效果

```python
def visualize_pooling():
    feature_map = np.array([
        [[1, 2, 3, 4],
         [5, 6, 7, 8],
         [9, 10, 11, 12],
         [13, 14, 15, 16]]
    ], dtype=float).reshape(4, 4, 1)

    pooled = max_pooling(feature_map, pool_size=2, stride=2)

    print("原始特徵圖 (4x4):")
    print(feature_map[:, :, 0])
    print("\n2x2 最大池化結果 (2x2):")
    print(pooled[:, :, 0])
```

## 深度學習框架的實現

### Keras

```python
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, AvgPool2D

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),  # 14x14
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),  # 7x7
    # ...
])
```

### PyTorch

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Conv2d(1, 32, 3),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(32, 64, 3),
    nn.ReLU(),
    nn.MaxPool2d(2),
)
```

## 空洞池化 / 擴張卷積

在pooling/卷積中插入空洞。

```python
# 空洞池化概念
def dilated_pooling(feature_map, pool_size=2, dilation=2):
    """空洞池化"""
    h, w, c = feature_map.shape

    out_h = (h - pool_size * dilation) // dilation + 1
    out_w = (w - pool_size * dilation) // dilation + 1

    output = np.zeros((out_h, out_w, c))

    for i in range(out_h):
        for j in range(out_w):
            si, sj = i * dilation, j * dilation
            region = feature_map[si:si+pool_size*dilation:dilation,
                                sj:sj+pool_size*dilation:dilation]
            output[i, j, :] = np.max(region, axis=(0, 1))

    return output
```

## 總結

特徵映射記錄卷積核在輸入上的響應。池化則降維並提取顯著特徵。最大池化是最常用的方法，因其能保留最強的回應。