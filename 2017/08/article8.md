# CNN 架構演變

## CNN 發展時間線

- **1998**：LeNet-5 - 手寫數字辨識
- **2012**：AlexNet - ImageNet 競賽冠軍
- **2014**：VGGNet - 深度學習簡單化
- **2014**：GoogLeNet - Inception 模組
- **2015**：ResNet - 殘差連接
- **2016+**：DenseNet, MobileNet, EfficientNet...

## LeNet-5 (1998)

最早的 CNN 成功案例。

```
輸入 (32x32)
    ↓
C1: 6@28x28 (5x5 卷積)
    ↓
S2: 6@14x14 (2x2 最大池化)
    ↓
C3: 16@10x10 (5x5 卷積)
    ↓
S4: 16@5x5 (2x2 最大池化)
    ↓
C5: 120 (5x5 卷積)
    ↓
F6: 84 (全連接)
    ↓
輸出: 10 (徑向基函數)
```

```python
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten

lenet = Sequential([
    Conv2D(6, (5, 5), activation='tanh', input_shape=(32, 32, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(16, (5, 5), activation='tanh'),
    MaxPooling2D((2, 2)),
    Conv2D(120, (5, 5), activation='tanh'),
    Flatten(),
    Dense(84, activation='tanh'),
    Dense(10, activation='softmax')
])
```

## AlexNet (2012)

開啟深度學習視覺時代。

```
輸入 (227x227x3)
    ↓
Conv1: 96@55x55 (11x11, stride=4)
    ↓
MaxPool1: 96@27x27
    ↓
Conv2: 256@27x27 (5x5)
    ↓
MaxPool2: 256@13x13
    ↓
Conv3-5: 384@13x13 (3x3) × 3
    ↓
MaxPool3: 256@6x6
    ↓
FC6-8: 4096 → 4096 → 1000
```

創新點：
- ReLU 激活函數
- Dropout 正則化
- GPU 訓練
- 數據增強

## VGGNet (2014)

簡單而深遠的架構。

```
VGG-16:
輸入 (224x224x3)
    ↓
Conv3-64 × 2
    ↓
MaxPool
    ↓
Conv3-128 × 2
    ↓
MaxPool
    ↓
Conv3-256 × 3
    ↓
MaxPool
    ↓
Conv3-512 × 3
    ↓
MaxPool
    ↓
Conv3-512 × 3
    ↓
MaxPool
    ↓
FC-4096 × 2
    ↓
FC-1000
    ↓
Softmax
```

特點：
- 只用 3x3 卷積核
- 深度 16-19 層
- 結構統一，易於理解

## GoogLeNet / Inception (2014)

Inception 模組的創新。

```
Inception 模組:
輸入
    ├─ 1x1 conv → 
    ├─ 1x1 conv → 3x3 conv →
    ├─ 1x1 conv → 5x5 conv →
    └─ 3x3 maxpool → 1x1 conv →
    ↓
Concat
```

優點：
- 多尺度特徵融合
- 1x1 卷積降維減少參數
- 22 層網路，參數比 AlexNet 少

## ResNet (2015)

殘差連接解決深度網路訓練問題。

```
殘差區塊:
輸入 → Conv → Conv → (+) → 輸出
         ↓
       identity
```

```python
def residual_block(x, filters):
    shortcut = x

    x = Conv2D(filters, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv2D(filters, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)

    # 殘差連接
    if x.shape != shortcut.shape:
        shortcut = Conv2D(filters, (1, 1))(shortcut)

    x = Add()([x, shortcut])
    x = Activation('relu')(x)

    return x
```

## 架構比較

| 網路 | 年份 | 深度 | ImageNet Top-5 |
|------|------|------|----------------|
| AlexNet | 2012 | 8 | 84.7% |
| VGG-16 | 2014 | 16 | 92.7% |
| GoogLeNet | 2014 | 22 | 93.3% |
| ResNet-152 | 2015 | 152 | 95.5% |

## 選擇考量

| 場景 | 推薦網路 |
|------|----------|
| 入門 | LeNet, AlexNet |
| 平衡 | VGG-16 |
| 資源受限 | MobileNet |
| 最高精度 | ResNet, EfficientNet |

## 總結

CNN 架構從 LeNet 發展到 ResNet，主要趨勢是網路越來越深，使用的卷積核越來越小。殘差連接使得訓練更深網路成為可能。