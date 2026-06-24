# 焦點文章 7：CNN 實作與應用

## 前言

本章節展示如何使用 Python 和 NumPy 從零實現簡單的 CNN，並介紹 CNN 在實際問題中的應用。

## 從零實現 CNN

### 完整 CNN 架構

```python
import numpy as np

class ConvLayer:
    def __init__(self, num_filters, kernel_size, stride=1, padding=0):
        self.num_filters = num_filters
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.filters = np.random.randn(num_filters, kernel_size, kernel_size) * 0.1

    def forward(self, input_data):
        self.input = input_data
        h, w = input_data.shape
        out_h = (h + 2*self.padding - self.kernel_size) // self.stride + 1
        out_w = (w + 2*self.padding - self.kernel_size) // self.stride + 1
        output = np.zeros((self.num_filters, out_h, out_w))

        padded = np.pad(input_data, self.padding, mode='constant')
        for f in range(self.num_filters):
            for i in range(0, out_h * self.stride, self.stride):
                for j in range(0, out_w * self.stride, self.stride):
                    output[f, i//self.stride, j//self.stride] = np.sum(
                        padded[i:i+self.kernel_size, j:j+self.kernel_size] * self.filters[f]
                    )
        return output

class MaxPoolLayer:
    def __init__(self, pool_size=2, stride=2):
        self.pool_size = pool_size
        self.stride = stride

    def forward(self, input_data):
        self.input = input_data
        c, h, w = input_data.shape
        out_h = h // self.stride
        out_w = w // self.stride
        output = np.zeros((c, out_h, out_w))

        for f in range(c):
            for i in range(0, h, self.stride):
                for j in range(0, w, self.stride):
                    if i // self.stride < out_h and j // self.stride < out_w:
                        output[f, i//self.stride, j//self.stride] = np.max(
                            input_data[f, i:i+self.pool_size, j:j+self.pool_size]
                        )
        return output

class SimpleCNN:
    def __init__(self, num_classes=10):
        self.conv1 = ConvLayer(8, 3, padding=1)
        self.pool1 = MaxPoolLayer(2, 2)
        self.conv2 = ConvLayer(16, 3, padding=1)
        self.pool2 = MaxPoolLayer(2, 2)
        self.num_classes = num_classes

    def forward(self, x):
        x = self.conv1.forward(x)
        x = np.maximum(0, x)  # ReLU
        x = self.pool1.forward(x)
        x = self.conv2.forward(x)
        x = np.maximum(0, x)  # ReLU
        x = self.pool2.forward(x)
        return x

    def predict(self, x):
        features = self.forward(x)
        return np.mean(features, axis=(1, 2))  # 簡化分類
```

## 使用 Keras 實作 CNN

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
```

## CNN 應用案例

### 1. 手寫數字辨識

```python
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(-1, 28, 28, 1) / 255.0
X_test = X_test.reshape(-1, 28, 28, 1) / 255.0

model.fit(X_train, y_train, epochs=5, validation_split=0.1)
```

### 2. 影像風格遷移

使用預訓練 VGG 網路提取內容與風格特徵：

```python
# 內容影像 + 風格影像 → 生成影像
content_features = vgg.predict(content_image)
style_features = vgg.predict(style_image)
# 優化生成的影像使其同時匹配內容與風格
```

### 3. 物體偵測

使用預訓練 CNN 作為骨幹網路：
- Faster R-CNN
- YOLO
- SSD

## 遷移學習

使用預訓練模型加速開發：

```python
from tensorflow.keras.applications import VGG16

base_model = VGG16(weights='imagenet', include_top=False,
                    input_shape=(224, 224, 3))

for layer in base_model.layers:
    layer.trainable = False

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dense(num_classes, activation='softmax')
])
```

## 總結

CNN 從理論到實作有完整的流程。現代深度學習框架如 TensorFlow 和 PyTorch 大幅簡化了 CNN 的實現，但理解底層原理仍然重要。

## 延伸閱讀

- https://www.google.com/search?q=CNN+implementation+Keras+MNIST
- https://www.google.com/search?q=convolutional+neural+network+transfer+learning