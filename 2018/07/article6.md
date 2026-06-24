# CNN 基礎：卷積層與池化層

## 1. 為什麼需要 CNN？

全連接層處理的問題：維度災難

```python
# 100x100 RGB 影像 -> 全連接層
input_size = 100 * 100 * 3  # 30,000 維
first_layer = 512
# 權重數量：30,000 * 512 = 15,360,000 個參數！
```

卷積層的局部連接和權重共享，大幅減少參數量。

## 2. 卷積層

### 核心概念

```python
import numpy as np

def conv2d(image, kernel, stride=1, padding=0):
    # 計算輸出維度
    h_out = (image.shape[0] - kernel.shape[0] + 2*padding) // stride + 1
    w_out = (image.shape[1] - kernel.shape[1] + 2*padding) // stride + 1
    
    # 結果陣列
    output = np.zeros((h_out, w_out))
    
    for i in range(0, h_out, stride):
        for j in range(0, w_out, stride):
            output[i, j] = np.sum(
                image[i:i+kernel.shape[0], j:j+kernel.shape[1]] * kernel
            )
    return output
```

### Keras 卷積層

```python
from keras.layers import Conv2D

# 32 個 3x3 卷積核
Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1))
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

### Keras 池化層

```python
from keras.layers import MaxPooling2D, AveragePooling2D

MaxPooling2D(pool_size=(2, 2), strides=2)
AveragePooling2D(pool_size=(2, 2))
```

## 4. 經典 CNN 架構

### LeNet-5

```python
# LeNet-5 結構（1998）
model = Sequential([
    # 卷積層
    Conv2D(6, (5, 5), activation='relu', input_shape=(32, 32, 1)),
    MaxPooling2D((2, 2)),
    
    Conv2D(16, (5, 5), activation='relu'),
    MaxPooling2D((2, 2)),
    
    # 全連接層
    Flatten(),
    Dense(120, activation='relu'),
    Dense(84, activation='relu'),
    Dense(10, activation='softmax')
])
```

## 5. 卷積層的權重數量計算

```python
# 輸入：3 通道，圖像 32x32
# 卷積核：6 個，每個 5x5

# 權重數量 = (5*5*3 + 1) * 6 = 456 個參數
# （+1 是 bias）

# 如果用全連接：32*32*3 * 6 = 18,432 個參數
```

## 6. 小結

CNN 通过卷積核的局部連接和權重共享，大幅減少了图像任务的參數量，是電腦視覺的基礎架構。

---

**參考資料**
- [CNN Architecture Overview](https://www.google.com/search?q=CNN+convolutional+neural+network+tutorial)
- [LeNet Architecture](https://www.google.com/search?q=LeNet+5+architecture)