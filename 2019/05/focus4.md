# CNN 架構

## LeNet、AlexNet、VGG

讓我們回顧經典的 CNN 架構，它們奠定了現代深度視覺的基礎。

---

## LeNet（1998）

Yann LeCun 等人提出的開創性架構。

### 結構

```python
# LeNet-5
# Input(32x32) → Conv(6, 5x5) → Pool(2x2) → Conv(16, 5x5) → Pool(2x2)
# → Conv(120, 5x5) → FC(84) → Output(10)
```

### 特點

- 使用 Sigmoid/Tanh 激活
- 平均池化
- 參數共享
- 應用於手寫數字辨識

---

## AlexNet（2012）

突破性的深度卷積網路。

### 結構

```python
# AlexNet
Conv(96, 11x11, stride=4) → ReLU → Pool(3x3) → LRN
Conv(256, 5x5) → ReLU → Pool(3x3) → LRN
Conv(384, 3x3) → ReLU
Conv(384, 3x3) → ReLU
Conv(256, 3x3) → ReLU → Pool(3x3)
FC(4096) → ReLU → Dropout
FC(4096) → ReLU → Dropout
FC(1000) → Softmax
```

### 關鍵創新

1. **ReLU 激活**：更快收斂
2. **GPU 訓練**：使用 CUDA
3. **LRN**：局部響應正規化
4. **Dropout**：防止過擬合
5. **Data Augmentation**：增加訓練樣本

---

## VGGNet（2014）

牛津大學視覺幾何組提出。

### VGG-16 結構

```python
# VGG-16
Conv(64, 3x3) → Conv(64, 3x3) → Pool(2x2)       # Block 1: 224→112
Conv(128, 3x3) → Conv(128, 3x3) → Pool(2x2)      # Block 2: 112→56
Conv(256, 3x3) → Conv(256, 3x3) → Conv(256, 3x3) → Pool(2x2)  # Block 3: 56→28
Conv(512, 3x3) → Conv(512, 3x3) → Conv(512, 3x3) → Pool(2x2)  # Block 4: 28→14
Conv(512, 3x3) → Conv(512, 3x3) → Conv(512, 3x3) → Pool(2x2)  # Block 5: 14→7
FC(4096) → FC(4096) → FC(1000)
```

### VGG 特點

- **簡單一致**：只使用 3x3 卷積
- **更深**：16-19 層
- **小卷積核**：多層堆疊取代大卷積核

### 為什麼 3x3 更好？

```
一個 7x7 卷積：
- 參數：49 個

三層 3x3 卷積：
- 參數：3 × 9 = 27 個
- 更多的非線性、更深的感受野
```

---

## 架構比較

| 架構 | 年份 | 層數 | 參數數量 | Top-5 錯誤率 |
|-----|------|-----|---------|------------|
| LeNet-5 | 1998 | 5 | 60K | N/A |
| AlexNet | 2012 | 8 | 60M | 15.3% |
| VGG-16 | 2014 | 16 | 138M | 24.4% |
| VGG-19 | 2014 | 19 | 144M | 24.4% |

---

## 設計原則

### 1. 層次化結構

```
輸入 → [Conv-Pool] × N → [FC] → 輸出
       低→中→高層特徵
```

### 2. 遞增通道數

```python
# 隨著網路加深，通道數增加
# 224x224x3 → 112x112x64 → 56x56x128 → 28x28x256 → 14x14x512 → 7x7x512
```

### 3. 降維策略

- Pooling（傳統）
- Stride 卷積（現代）
- 兩者混合

### 4. 跳躍連接（預處理）

```python
# 某些變體使用跳躍連接
# 幫助梯度流動
```

---

## Keras 實現

```python
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

def build_lenet():
    model = Sequential([
        Conv2D(6, (5, 5), activation='tanh', input_shape=(32, 32, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(16, (5, 5), activation='tanh'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(120, activation='tanh'),
        Dense(84, activation='tanh'),
        Dense(10, activation='softmax')
    ])
    return model

def build_alexnet():
    model = Sequential([
        Conv2D(96, (11, 11), strides=4, activation='relu', input_shape=(224, 224, 3)),
        MaxPooling2D((3, 3), strides=2),
        Conv2D(256, (5, 5), activation='relu', padding='same'),
        MaxPooling2D((3, 3), strides=2),
        Conv2D(384, (3, 3), activation='relu', padding='same'),
        Conv2D(384, (3, 3), activation='relu', padding='same'),
        Conv2D(256, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((3, 3), strides=2),
        Flatten(),
        Dense(4096, activation='relu'),
        Dropout(0.5),
        Dense(4096, activation='relu'),
        Dropout(0.5),
        Dense(1000, activation='softmax')
    ])
    return model
```

---

## 延伸閱讀

- [AlexNet 論文](https://www.google.com/search?q=AlexNet+Krizhevsky+2012)
- [VGGNet 論文](https://www.google.com/search?q=VGG+Simonyan+2014)
- [CNN 架構演進](https://www.google.com/search?q=evolution+CNN+architectures)

---

*本篇文章為「AI 程式人雜誌 2019 年 5 月號」系列文章之一。*