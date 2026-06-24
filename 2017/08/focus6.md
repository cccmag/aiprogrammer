# 影像分割技術

## 分割的層次

### 1. 語義分割（Semantic Segmentation）

為每個像素分配類別標籤，不區分同類別的不同個體。

```
圖像 → 語義分割 → 每個像素標記為「車/路/人/建築...」
（所有車都是同一類，不區分是哪輛車）
```

### 2. 實例分割（Instance Segmentation）

不僅區分類別，還區分同類別的不同個體。

```
圖像 → 實例分割 → 每個車的實例分別標記
（紅色車 = instance 1, 藍色車 = instance 2）
```

### 3. 全景分割（Panoptic Segmentation）

結合語義分割與實例分割。

## 早期方法

### 滑動視窗

在圖像上滑動小窗口，對每個 patch 分類。

缺點：非常慢，重複計算過多。

### 超像素分割

使用 SLIC 等方法產生超像素，再對每個超像素分類。

## FCN（Fully Convolutional Network）

將分類網路的全連接層替換為卷積層，實現像素級分類。

```python
# VGG-16 改為 FCN
from keras.models import Model
from keras.layers import Conv2D, Reshape

# 輸入: 224x224x3
# 經過 VGG（最後一層捲積）: 7x7x512

# 替換為捲積
x = Conv2D(4096, (7, 7), activation='relu', padding='same')(backbone.output)
x = Conv2D(4096, (1, 1), activation='relu')(x)
x = Conv2D(num_classes, (1, 1))(x)  # 例如 21 類

# 上採樣（轉置卷積）回到原始尺寸
x = Conv2DTranspose(num_classes, (64, 64), strides=(32, 32), padding='same')(x)

# reshape 為像素
output = Reshape((-1, num_classes))(x)
output = Activation('softmax')(output)
```

### 跳躍連接

將淺層細節與深層語意結合。

```
輸入 → Encoder → 低解析度高語意
          ↓
        解碼
          ↓
淺層特徵 ──────→ 結合 → 輸出
```

## U-Net

專為醫學影像分割設計的架構。

```python
# U-Net 概念

# Encoder（左側）
conv1 → pool
conv2 → pool
conv3 → pool
conv4 → pool
conv5

# Decoder（右側）
up6 → concat(conv4) → conv6
up7 → concat(conv3) → conv7
up8 → concat(conv2) → conv8
up9 → conv9

# 輸出
1x1 conv → num_classes
```

## Mask R-CNN（2017）

Faster R-CNN 的擴展，同時輸出語意分割 mask。

```python
# Mask R-CNN 架構概念

# 1. Backbone (ResNet + FPN)
features = backbone(image)

# 2. RPN (Region Proposal Network)
proposals = rpn(features)

# 3. RoI Align（取代 RoI Pooling）
roi_features = roi_align(features, proposals)

# 4. 頭部分支
class_scores = classification_head(roi_features)  # 分类
boxes = regression_head(roi_features)            # 邊界框
masks = mask_head(roi_features)                 # 分割 mask
```

### RoI Align

解決 RoI Pooling 的量化誤差問題。

```python
# RoI Pooling 的問題
# 7x7 特徵圖，通過 2x2 池化
# 每格 = 7/2 = 3.5（量化）

# RoI Align 解決方案
# 使用雙線性插值計算浮點座標的值
# 不進行量化
```

## 語義分割實作

### 使用 Keras 實作簡單 FCN

```python
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Concatenate

def simple_fcn(input_shape=(224, 224, 3), num_classes=21):
    inputs = Input(input_shape)

    # Encoder
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    pool1 = MaxPooling2D((2, 2))(x)

    x = Conv2D(128, (3, 3), activation='relu', padding='same')(pool1)
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    pool2 = MaxPooling2D((2, 2))(x)

    # Bottleneck
    x = Conv2D(256, (3, 3), activation='relu', padding='same')(pool2)

    # Decoder
    up3 = UpSampling2D((2, 2))(x)
    x = Concatenate()([up3, pool2])
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)

    up4 = UpSampling2D((2, 2))(x)
    x = Concatenate()([up4, pool1])
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)

    # 輸出
    output = Conv2D(num_classes, (1, 1), activation='softmax')(x)

    return Model(inputs, output)
```

## 評估指標

### IoU（Intersection over Union）

對每個類別計算預測與真實的 IoU，再平均。

```python
def compute_iou(pred_mask, true_mask, class_id):
    pred = (pred_mask == class_id)
    true = (true_mask == class_id)

    intersection = np.logical_and(pred, true).sum()
    union = np.logical_or(pred, true).sum()

    return intersection / (union + 1e-6)

def mean_iou(pred_masks, true_masks, num_classes):
    ious = []
    for class_id in range(num_classes):
        iou = compute_iou(pred_masks, true_masks, class_id)
        ious.append(iou)
    return np.mean(ious)
```

## 資料集

| 資料集 | 說明 |
|--------|------|
| Cityscapes | 街景分割，30 類 |
| ADE20K | 室內外場景，150 類 |
| COCO-Stuff | COCO 的語義分割標注 |
| Pascal VOC | 20 類物體 + 背景 |

## 總結

語義分割從 FCN 的端到端方法開始，U-Net 提出了編碼器-解碼器架構，Mask R-CNN 實現了同時偵測與分割。深度學習大幅提升了分割的精度與效率。