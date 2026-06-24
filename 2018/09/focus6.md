# 語義分割：FCN 與 U-Net

## 1. 語義分割任務

```python
# 任務：對影像每個像素進行分類
# 輸出：與輸入相同尺寸的分割圖（每像素一個類別）

# 不同於物件偵測（預測邊界框）
# 不同於實例分割（區分同類別不同個體）
```

## 2. FCN（2015）

### 核心思想：用卷積層替換全連接層

```python
# 傳統 CNN（分類）
# CONV -> CONV -> POOL -> CONV -> CONV -> POOL -> FC -> FC -> Softmax

# FCN（全卷積網路）
# CONV -> CONV -> POOL -> CONV -> CONV -> POOL -> CONV -> CONV -> CONV
#                                                    |
#                                               upsampling
#                                                    |
#                                              segmentation map
```

### 上取樣（Upsampling）

```python
# 轉置卷積（反捲積）
# 輸入：小型特徵圖
# 輸出：放大的特徵圖

from keras.layers import Conv2DTranspose

Conv2DTranspose(filters=256, kernel_size=4, strides=2, padding='same')
# 尺寸變大，通道數減少
```

### FCN-8s 架構

```python
# VGG-16 作為骨幹
# Block 5 output: 7x7x512
# -> Conv2DTranspose(4, strides=2) -> 14x14x256
# -> 與 Pool4 拼接
# -> Conv2DTranspose(4, strides=2) -> 28x28x128
# -> 與 Pool3 拼接
# -> Conv2DTranspose(8, strides=4) -> 224x224xn_classes
```

## 3. U-Net（2015）

### 對稱 Encoder-Decoder 架構

```python
# U-Net 結構
# Encoder（左側）：壓縮路徑，擷取特徵
# Decoder（右側）：擴展路徑，回復空間解析度
# Skip Connections：拼接編碼器和解碼器特徵

#         Encoder              Decoder
#    572x572 ──┐          ┌── 388x388
#    570x570   ├─> 28x28 ─┤
#    284x284   │          │  44x44
#    282x282   ├─> 44x44 ─┤
#    140x140   │          │  76x76
#    138x138   ├─> 76x76 ─┤
#    68x68     │          │  100x100
#    66x66     ├─> 100x100┤
#    32x32     │          │  196x196
#    30x30     └─> 196x196┘
```

### Keras 實現

```python
from keras.layers import Conv2D, MaxPooling2D, concatenate, Conv2DTranspose

def unet_model():
    inputs = Input(shape=(572, 572, 1))

    # Encoder
    c1 = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
    c1 = Conv2D(64, (3, 3), activation='relu', padding='same')(c1)
    p1 = MaxPooling2D((2, 2))(c1)  # 28x28

    c2 = Conv2D(128, (3, 3), activation='relu', padding='same')(p1)
    c2 = Conv2D(128, (3, 3), activation='relu', padding='same')(c2)
    p2 = MaxPooling2D((2, 2))(c2)  # 14x14

    # ... 更多 Encoder 層 ...

    # Bridge
    c5 = Conv2D(1024, (3, 3), activation='relu', padding='same')(p4)

    # Decoder
    u6 = Conv2DTranspose(512, (2, 2), strides=(2, 2), padding='same')(c5)
    u6 = concatenate([u6, c4])
    c6 = Conv2D(512, (3, 3), activation='relu', padding='same')(u6)

    # ... 更多 Decoder 層 ...

    outputs = Conv2D(1, (1, 1), activation='sigmoid')(c9)

    return Model(inputs, outputs)
```

## 4. 其他分割架構

### SegNet

```python
# 類似 U-Net，但使用 Pooling Index 進行上取樣
# 記憶體效率更高
```

### DeepLab（系列）

```python
# DeepLab v1: ASPP + CRF
# DeepLab v2:空洞卷積 + ASPP
# DeepLab v3: 改進的 ASPP
# DeepLab v3+:Encoder-Decoder + ASPP

# 核心：空洞卷積（Dilated/Atrous Convolution）
# 擴大感受野而不損失解析度
Conv2D(filters, kernel_size, dilation_rate=2)  # 空洞卷積
```

## 5. 損失函數

```python
# 交叉熵（Pixel-wise）
cross_entropy = -y_true * tf.log(y_pred + epsilon)
loss = tf.reduce_mean(cross_entropy)

# Dice Loss（常用於分割）
def dice_loss(y_true, y_pred):
    smooth = 1.0
    intersection = tf.reduce_sum(y_true * y_pred)
    return 1 - (2. * intersection + smooth) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth)

# Focal Loss（處理類別不平衡）
def focal_loss(y_true, y_pred):
    # 類似分割中的類別不平衡問題
```

## 6. 評估指標

```python
# Pixel Accuracy
accuracy = (預測正確的像素數) / (總像素數)

# Mean IoU
# IoU = |交集| / |併集|
# Mean IoU = 所有類別 IoU 的平均

def iou_score(y_true, y_pred, num_classes):
    ious = []
    for c in range(num_classes):
        true_class = y_true == c
        pred_class = y_pred == c
        intersection = (true_class & pred_class).sum()
        union = (true_class | pred_class).sum()
        ious.append(intersection / union if union > 0 else 1.0)
    return np.mean(ious)
```

## 7. 小結

語義分割從 FCN 的粗略分割到 U-Net 的精確分割，經歷了快速發展。 Encoder-Decoder 架構和 Skip Connections 是分割網路的標準設計。

---

**下一步**：[影像生成：GAN 的濫觴](focus7.md)