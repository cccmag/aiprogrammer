# Keras 整合與高層 API：降低深度學習的門檻

## 前言

Keras 以其簡潔優雅的 API 設計，成為深度學習初學者最喜愛的框架。隨著 TensorFlow 1.0 的發布，Keras 作為 tf.keras 整合進 TensorFlow，進一步強化了 TensorFlow 的高層 API 能力。

## Keras 的起源與發展

### Keras 簡介

Keras（κέρας，希臘語「角」）由 Francois Chollet 開發：

```
2015 年：Keras 首次發布
2016 年：支援多後端（TensorFlow、Theano、CNTK）
2017 年：整合進 TensorFlow，成為官方高層 API
```

### Keras 的設計原則

1. **使用者優先**：API 簡潔、直觀、易於擴展
2. **模組化**：網路、層、優化器都是獨立模組
3. **Python 原生**：完全使用 Python 編寫，無額外配置

## Keras 核心概念

### 模型建構

Keras 提供兩種主要的模型建構方式：

```python
# 方式一：Sequential 模型（最常用）
from keras.models import Sequential
from keras.layers import Dense

model = Sequential([
    Dense(128, activation='relu', input_shape=(784,)),
    Dense(64, activation='relu'),
    Dense(10, activation='softmax')
])

# 方式二：函數式 API（更靈活）
from keras.layers import Input, Dense
from keras.models import Model

inputs = Input(shape=(784,))
x = Dense(128, activation='relu')(inputs)
predictions = Dense(10, activation='softmax')(x)
model = Model(inputs=inputs, outputs=predictions)
```

### 編譯模型

```python
# 編譯模型，指定優化器、損失函數和評估指標
model.compile(
    optimizer='adam',  # 或 'sgd', 'rmsprop' 等
    loss='categorical_crossentropy',  # 或 'mse', 'binary_crossentropy' 等
    metrics=['accuracy']  # 或 ['accuracy', 'mae'] 等
)
```

### 訓練模型

```python
# 訓練模型
model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,  # 或 validation_data=(x_val, y_val)
    verbose=1
)
```

### 評估與預測

```python
# 評估模型
loss, accuracy = model.evaluate(x_test, y_test)
print(f"Loss: {loss}, Accuracy: {accuracy}")

# 預測
predictions = model.predict(x_new)
```

## Sequential 模型範例

### 多層感知器（MLP）

```python
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import to_categorical
from keras.datasets import mnist

# 載入資料
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 預處理
x_train = x_train.reshape(60000, 784).astype('float32') / 255
y_train = to_categorical(y_train, 10)
x_test = x_test.reshape(10000, 784).astype('float32') / 255
y_test = to_categorical(y_test, 10)

# 建構模型
model = Sequential([
    Dense(512, activation='relu', input_shape=(784,)),
    Dropout(0.2),
    Dense(512, activation='relu'),
    Dropout(0.2),
    Dense(10, activation='softmax')
])

# 編譯和訓練
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.1)
```

### 卷積神經網路（CNN）

```python
from keras.layers import Conv2D, MaxPooling2D, Flatten

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])
```

### 循環神經網路（RNN）

```python
from keras.layers import LSTM, Embedding

model = Sequential([
    Embedding(10000, 128, input_length=100),
    LSTM(128, dropout=0.2, recurrent_dropout=0.2),
    Dense(1, activation='sigmoid')
])
```

## 函數式 API

### 共享層

```python
from keras.layers import Input, Dense, LSTM, concatenate

# 共享的 LSTM 層
shared_lstm = LSTM(64)

# 兩個輸入分支
input_a = Input(shape=(100, 64))
input_b = Input(shape=(100, 64))

# 兩個輸出
encoded_a = shared_lstm(input_a)
encoded_b = shared_lstm(input_b)

# 合併
merged = concatenate([encoded_a, encoded_b])
output = Dense(1, activation='sigmoid')(merged)

model = Model(inputs=[input_a, input_b], outputs=output)
```

### 多輸入多輸出

```python
# 主輸入：文章內容
main_input = Input(shape=(100,), dtype='int32', name='main_input')
title_input = Input(shape=(20,), dtype='int32', name='title_input')

# 嵌入層
x = Embedding(10000, 128)(main_input)
title_embed = Embedding(10000, 128)(title_input)

# 特徵提取
lstm_out = LSTM(64)(x)
title_lstm = LSTM(64)(title_embed)

# 多輸出
main_output = Dense(1, activation='sigmoid', name='main_output')(lstm_out)
title_output = Dense(1, activation='sigmoid', name='title_output')(title_lstm)

model = Model(inputs=[main_input, title_input], outputs=[main_output, title_output])
```

## tf.keras 整合

### TensorFlow 1.0 中的 Keras

```python
# TensorFlow 1.1+ 包含 tf.keras
import tensorflow as tf
from tensorflow import keras

# tf.keras 是完整的 Keras 實現
model = keras.Sequential([
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

### 與 TensorFlow 原生 API 的差異

```python
# tf.keras 的優點
# - 與 TensorFlow 無縫整合
# - 可以使用 tf.data 等工具
# - 模型可以直接匯出為 TensorFlow SavedModel

# 適合快速原型開發和標準模型
```

## 回調函數

```python
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard

callbacks = [
    EarlyStopping(patience=3, restore_best_weights=True),
    ModelCheckpoint('best_model.h5', save_best_only=True),
    TensorBoard('./logs')
]

model.fit(
    x_train, y_train,
    epochs=50,
    callbacks=callbacks
)
```

## 結論

Keras 以其簡潔的 API 大幅降低了深度學習的門檻。通過與 TensorFlow 的整合，Keras 獲得了更廣的使用者群和更強大的底層支援。

無論你是深度學習的新手還是有經驗的實踐者，Keras 都是快速原型開發和標準模型訓練的理想選擇。

---

## 延伸閱讀

- [Keras 官方文檔](https://www.google.com/search?q=Keras+official+documentation)
- [Keras+Sequential+模型](https://www.google.com/search?q=Keras+Sequential+model+tutorial)
- [tf.keras+教程](https://www.google.com/search?q=tf.keras+tutorial+TensorFlow)
- [Keras+vs+TensorFlow+比較](https://www.google.com/search?q=Keras+vs+TensorFlow+slim)

---

*本篇文章為「AI 程式人雜誌 2017 年 2 月號」焦點系列之一。*