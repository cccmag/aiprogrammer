# 池化層

## Max Pooling 與 Average Pooling

池化層（Pooling Layer）是 CNN 中的重要組成部分，用於降維和減少計算量。

---

## 池化操作

### Max Pooling

取區域內的最大值：

```python
def max_pooling(image, pool_size=2, stride=2):
    """Max Pooling 運算"""
    kh, kw = pool_size, pool_size
    ih, iw = image.shape

    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1

    output = np.zeros((out_h, out_w))

    for i in range(0, out_h * stride, stride):
        for j in range(0, out_w * stride, stride):
            region = image[i:i+kh, j:j+kw]
            output[i//stride, j//stride] = np.max(region)

    return output
```

### Average Pooling

取區域內的平均值：

```python
def avg_pooling(image, pool_size=2, stride=2):
    """Average Pooling 運算"""
    kh, kw = pool_size, pool_size
    ih, iw = image.shape

    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1

    output = np.zeros((out_h, out_w))

    for i in range(0, out_h * stride, stride):
        for j in range(0, out_w * stride, stride):
            region = image[i:i+kh, j:j+kw]
            output[i//stride, j//stride] = np.mean(region)

    return output
```

---

## 視覺化

```
輸入 (4x4):              Max Pooling (2x2, stride=2):    Avg Pooling (2x2, stride=2):
[1 2 3 4]               [6 8]                         [3.0 5.5]
[5 6 7 8]        →                                  [4.5 6.5]
[3 4 5 6]                [6 8]                         [?? ??]
[7 8 5 4]
```

---

## 全域池化

### Global Average Pooling

將每個特徵圖平均成一個數值：

```python
# GAP: (H, W, C) → (1, 1, C) → (C,)
# 或 (C,) → 全域平均

def global_avg_pooling(feature_maps):
    # feature_maps: (H, W, C)
    return np.mean(feature_maps, axis=(0, 1))  # (C,)
```

### Global Max Pooling

```python
def global_max_pooling(feature_maps):
    # feature_maps: (H, W, C)
    return np.max(feature_maps, axis=(0, 1))  # (C,)
```

### 優勢

- **減少參數**：消除全連接層
- **處理任意輸入大小**：不需固定輸入尺寸
- **更魯棒**：對輸入變化更加容忍

---

## 池化層的作用

### 降維

```
輸入：28x28x64
經過 2x2 Max Pooling stride=2
輸出：14x14x64
```

### 保持重要特徵

```
Max Pooling: 保留最顯著的特征
Average Pooling: 保留背景信息
```

### 提供平移不變性

```python
# 輕微的平移不會影響池化結果
# 因為無論物體在哪個位置，Max 都能抓到它
```

---

## 池化超參數

### Pool Size

常見選擇：2x2、3x3

```python
# 2x2 池化：輸出尺寸減半
# 3x3 池化：更大範圍的抽象
```

### Stride

```python
# stride=pool_size 常見
# 避免重疊池化區域
```

### 填充

很少在池化層使用填充，因為池化是確定性操作。

---

## 現代 CNN 中的趨勢

### 逐漸棄用池化

最新的一些架構（Facebook 的等）開始減少使用池化，改用 stride 來控制尺寸。

### 混合使用

```python
# 常見模式
# 使用 stride=2 替代部分池化層
Conv2D(64, (3, 3), strides=2)  # 替代 Conv + Pool
```

---

## 程式實作

### NumPy 實作

```python
import numpy as np

def max_pooling_2x2(image):
    """2x2 Max Pooling"""
    h, w = image.shape
    out_h, out_w = h // 2, w // 2
    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            region = image[i*2:(i+1)*2, j*2:(j+1)*2]
            output[i, j] = np.max(region)

    return output
```

### Keras

```python
from keras.layers import MaxPooling2D, AveragePooling2D, GlobalAveragePooling2D

# Max Pooling
MaxPooling2D(pool_size=(2, 2), strides=2)

# Average Pooling
AveragePooling2D(pool_size=(2, 2), strides=2)

# Global Average Pooling
GlobalAveragePooling2D()  # 輸出 (C,)
```

---

## 延伸閱讀

- [池化層詳解](https://www.google.com/search?q=max+pooling+vs+avg+pooling)
- [CNN 中的池化](https://www.google.com/search?q=pooling+in+convolutional+networks)
- [Global Average Pooling](https://www.google.com/search?q=global+average+pooling+CNN)

---

*本篇文章為「AI 程式人雜誌 2019 年 5 月號」系列文章之一。*