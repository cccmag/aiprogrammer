# 文章 10：CNN 應用案例

## 前言

卷積神經網路在各個領域都有廣泛應用。本章節介紹 CNN 在不同領域的實際應用案例。

## 影像分類

### MNIST 手寫數字辨識

```python
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(-1, 28, 28, 1).astype('float32') / 255
X_test = X_test.reshape(-1, 28, 28, 1).astype('float32') / 255
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

model.fit(X_train, y_train, epochs=5, batch_size=64, validation_split=0.1)
```

## 物體偵測

### YOLO（You Only Look Once）

即時物體偵測：

```python
# 使用預訓練 YOLO
from yolo import YOLO

yolo = YOLO()
boxes = yolo.detect(image)
```

## 醫學影像分析

### 腫瘤偵測

```python
# X 光影像分類
model = load_trained_model('chest_xray_model.h5')
prediction = model.predict(x_ray_image)
```

## 人臉識別

### DeepFace

```python
from deepface import DeepFace

result = DeepFace.verify(img1, img2)
embedding = DeepFace.represent(img)
```

## 自動駕駛

### 車道線偵測

```python
# 使用 CNN 偵測車道線
lane_model = load_model('lane_detection.h5')
lane_mask = lane_model.predict(road_image)
```

## 藝術創作

### 神經風格遷移

```python
# 將藝術風格遷移到照片
styled_image = neural_style_transfer(content_image, style_image)
```

## 影片分析

### 動作辨識

```python
# 3D CNN 用於影片分類
video_model = Sequential([
    TimeDistributed(Conv2D(32, (3, 3))),
    TimeDistributed(MaxPooling2D((2, 2))),
    LSTM(64),
    Dense(num_classes, activation='softmax')
])
```

## 農業應用

### 病蟲害偵測

```python
# 識別植物病蟲害
pest_model = load_model('pest_detection.h5')
pest_type = pest_model.predict(leaf_image)
```

## 總結

CNN 的應用領域非常廣泛，從日常的影像分類到專業的醫學診斷都有 CNN 的身影。預訓練模型與遷移學習更進一步降低了應用門檻。

## 延伸閱讀

- https://www.google.com/search?q=CNN+applications+computer+vision+2017
- https://www.google.com/search?q=convolutional+neural+network+use+cases+examples