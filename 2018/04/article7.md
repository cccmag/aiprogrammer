# TensorFlow 1.7 整合 Keras

## 前言

TensorFlow 1.7 正式將 Keras 2 整合為 TensorFlow 的官方高階 API，大幅簡化了神經網路的建立流程。

## Keras 整合的好處

### 1. 簡潔的 API

```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(784,)),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
```

### 2. 更好的整合

- 使用 `tf.keras` 而非獨立的 Keras
- 與 TensorFlow 生態系統完美整合
- 支援 Eager Execution

### 3. 支援更多功能

- TensorBoard 整合
- 分散式訓練
- 模型序列化

## 結論

Keras 整合讓 TensorFlow 更加親民，吸引了更多開發者。

---

**延伸閱讀**

- [TensorFlow 官方網站](https://www.google.com/search?q=TensorFlow+official+site)
- [tf.keras 文檔](https://www.google.com/search?q=tf.keras+documentation)