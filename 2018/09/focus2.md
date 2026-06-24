# 卷積層、池化層原理詳解

## 1. 卷積運算

### 什麼是卷積？

卷積是一種線性運算，通过滑動卷積核（kernel）在輸入上進行局部計算。

```python
import numpy as np

def conv2d(image, kernel, stride=1, padding=0):
    # 輸入：image (H, W)，核心：kernel (K, K)
    # 輸出：(H-K+2P)/S + 1, (W-K+2P)/S + 1

    if padding > 0:
        image = np.pad(image, padding, mode='constant')

    h_out = (image.shape[0] - kernel.shape[0]) // stride + 1
    w_out = (image.shape[1] - kernel.shape[1]) // stride + 1
    output = np.zeros((h_out, w_out))

    for i in range(h_out):
        for j in range(w_out):
            output[i, j] = np.sum(
                image[i*stride:i*stride+kernel.shape[0],
                      j*stride:j*stride+kernel.shape[1]] * kernel
            )
    return output
```

### 卷積的特性

| 特性 | 說明 |
|------|------|
| 局部連接 | 每個輸出只依賴局部輸入 |
| 權重共享 | 同一卷積核在整個輸入上共享 |
| 平移不變性 | 對特征的平移不敏感 |

## 2. 卷積層詳解

### Keras 卷積層

```python
from keras.layers import Conv2D

# 基本用法
Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3))

# 引數說明
# - 第一個：卷積核數量（輸出通道數）
# - (3, 3)：卷積核大小
# - activation：激活函數
# - padding='same' 或 'valid'
# - strides=(1, 1)
# - dilation_rate=(1, 1)  # 空洞卷積
```

### 多通道卷積

```python
# 輸入：(H, W, C_in)
# 卷積核：(K, K, C_in)
# 輸出：(H', W', C_out)

# 如果有多個卷積核，每個都產生一個輸出通道
# 輸出通道數 = 卷積核數量
```

### 權重數量計算

```python
# 輸入：3 通道（RGB）
# 卷積核：3x3
# 輸出：64 通道

# 權重數量 = (3*3*3 + 1) * 64 = 1792
# （+1 是 bias）
```

## 3. 池化層

### 最大池化

```python
def max_pooling(image, pool_size=2, stride=2):
    h_out = (image.shape[0] - pool_size) // stride + 1
    w_out = (image.shape[1] - pool_size) // stride + 1
    output = np.zeros((h_out, w_out))

    for i in range(h_out):
        for j in range(w_out):
            output[i, j] = np.max(
                image[i*stride:i*stride+pool_size,
                      j*stride:j*stride+pool_size]
            )
    return output
```

### 平均池化

```python
def avg_pooling(image, pool_size=2, stride=2):
    h_out = (image.shape[0] - pool_size) // stride + 1
    w_out = (image.shape[1] - pool_size) // stride + 1
    output = np.zeros((h_out, w_out))

    for i in range(h_out):
        for j in range(w_out):
            output[i, j] = np.mean(
                image[i*stride:i*stride+pool_size,
                      j*stride:j*stride+pool_size]
            )
    return output
```

### 池化特點

| 類型 | 作用 | 適用場景 |
|------|------|----------|
| MaxPool | 保留显著特征 | 一般首選 |
| AvgPool | 平均池化 | 替代全連接層 |
| GlobalPool | 池化到單一值 | 特徵壓縮 |

## 4. 漸層式特徵學習

```python
# CNN 特徵學習層次結構
# 低層：邊、角落、紋理
# 中層：形狀、部件
# 高層：物體、概念
```

## 5. 小結

卷積層通過局部連接和權重共享大幅減少了參數量，池化層則提供特徵不變性和計算效率。兩者組合形成 CNN 的核心。

---

**下一步**：[經典架構：VGG、GoogLeNet、ResNet](focus3.md)