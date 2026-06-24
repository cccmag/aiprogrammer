# 遷移學習與微調策略

## 1. 遷移學習概述

遷移學習利用在大規模資料集（如 ImageNet）上預訓練的模型，作為新任務的起點。

```python
# 兩種主要策略
# 1. 特徵萃取：凍結預訓練模型，只訓練新分類頭
# 2. 微調：解凍並訓練部分或全部層
```

## 2. 為什麼遷移學習有效？

```python
# 低層學到的通用特徵
# - 邊、角落、紋理 → 幾乎所有影像任務都適用
# - 形狀、部件 → 視覺任務通用
# - 高層語義 → 與任務相關，需要微調
```

ImageNet 預訓練模型學習到的特徵可以推廣到各種視覺任務。

## 3. 特徵萃取

```python
import torch
from torchvision import models

# 載入預訓練模型
resnet = models.resnet18(pretrained=True)

# 凍結所有層
for param in resnet.parameters():
    param.requires_grad = False

# 只訓練新分類頭
num_features = resnet.fc.in_features
resnet.fc = torch.nn.Linear(num_features, 10)  # 10 類

# 只優化 fc 層
optimizer = torch.optim.Adam(resnet.fc.parameters())
```

### 適用場景

- 新任務資料集很小
- 新任務與預訓練任務相似
- 只想快速取得基線模型

## 4. 微調策略

### 策略一：微調最後幾層

```python
# 只解凍最後一個 block
for param in resnet.layer4.parameters():
    param.requires_grad = True

# layer4 和 fc 會被訓練
optimizer = torch.optim.Adam([
    {'params': resnet.layer4.parameters(), 'lr': 1e-4},
    {'params': resnet.fc.parameters(), 'lr': 1e-3}
])
```

### 策略二：微調整個網路

```python
# 解凍所有層
for param in resnet.parameters():
    param.requires_grad = True

# 預訓練層使用較小學習率
optimizer = torch.optim.Adam([
    {'params': resnet.conv1.parameters(), 'lr': 1e-5},
    {'params': resnet.layer4.parameters(), 'lr': 1e-4},
    {'params': resnet.fc.parameters(), 'lr': 1e-3}
])
```

### 策略三：區域性微調

```python
# 分階段訓練
# 階段 1：只訓練分類頭
train_class_head()

# 階段 2：微調最後幾層
fine_tune_last_layers()

# 階段 3：微調整個網路（小學習率）
fine_tune_all()
```

## 5. Keras 微調範例

```python
from keras.applications import VGG16
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model

# 載入預訓練 VGG16
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# 添加自訂分類頭
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
predictions = Dense(10, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# 凍結預訓練層
for layer in base_model.layers:
    layer.trainable = False

# 編譯並訓練分類頭
model.compile(optimizer='adam', loss='categorical_crossentropy')
model.fit(train_data, epochs=10)

# 解凍並微調
for layer in base_model.layers[-4:]:
    layer.trainable = True

model.compile(optimizer=Adam(1e-5), loss='categorical_crossentropy')
model.fit(train_data, epochs=5)
```

## 6. 資料增強與微調

```python
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# 微調時使用較弱的增強
fine_tune_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    horizontal_flip=True
)
```

## 7. 小結

遷移學習是 2018 年深度學習實踐的核心技術。選擇合適的微調策略需要考慮任務相似度、資料量大小和計算資源。

---

**下一步**：[物件偵測：R-CNN 到 YOLO](focus5.md)