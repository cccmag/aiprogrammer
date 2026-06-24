# Keras 2.0 發布：更簡潔的 API

## 前言

Keras 2.0 是 Keras 發展史上的重要里程碑。這一版本帶來了更簡潔的 API、更清晰的文檔，以及與 TensorFlow 的深度整合。

## Keras 2.0 的主要改進

### 更清晰的 API

```python
# Keras 1.x 的 Global average pooling
from keras.layers import GlobalAveragePooling2D
x = GlobalAveragePooling2D()(x)

# Keras 2.0：更直觀的命名
from keras.layers import GlobalAvgPool2D
x = GlobalAvgPool2D()(x)
```

### 批次處理改進

```python
# Keras 2.0 更好地處理批次維度
# input_shape=(784,) 自動識別為 (batch_size, 784)
```

### 層共享

```python
# Keras 2.0 更容易實現層共享
shared_lstm = LSTM(64)

# 兩個輸入共享同一 LSTM 層
output1 = shared_lstm(input1)
output2 = shared_lstm(input2)
```

## tf.keras 的整合

### 為什麼使用 tf.keras？

1. **與 TensorFlow 無縫整合**
2. **可以使用 tf.data 等工具**
3. **模型可以直接匯出為 SavedModel**
4. **更好的效能最佳化**

```python
import tensorflow as tf
from tensorflow import keras

# tf.keras 是官方推薦的高層 API
model = keras.Sequential([
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
```

## Keras 設計哲學

Keras 的成功來自其清晰的設計原則：

### 1. 用起來簡單

```python
# 簡潔的 API
model = Sequential([Dense(10, input_shape=(784,), activation='softmax')])
model.compile(optimizer='adam', loss='categorical_crossentropy')
model.fit(x_train, y_train)
```

### 2. 模組化

```python
# 每個組件都是獨立的
# 可以自由組合
```

### 3. 易擴展

```python
# 自訂層
class MyLayer(keras.layers.Layer):
    def call(self, inputs):
        return inputs * 2
    def get_config(self):
        return {}
```

## 結語

Keras 2.0 延續了 Keras 的設計理念，同時帶來了更穩定、更易用的 API。與 TensorFlow 的深度整合使其成為深度學習開發的最佳選擇之一。

---

## 延伸閱讀

- [Keras 2.0 發布說明](https://www.google.com/search?q=Keras+2.0+release+notes)
- [Keras+官方文檔](https://www.google.com/search?q=Keras+official+documentation)
- [tf.keras+教程](https://www.google.com/search?q=tf.keras+tutorial+TensorFlow)

---

*本篇文章為「AI 程式人雜誌 2017 年 2 月號」文章系列之一。*