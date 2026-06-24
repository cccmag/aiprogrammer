# TensorFlow 2.0 的革命

## 2019 年 9 月的重大發布

2019 年 9 月，Google 正式發布 TensorFlow 2.0，這是 TensorFlow 自 2015 年發布以來最重要的版本更新。TensorFlow 2.0 帶來了革命性的變化，讓深度學習開發變得更加直觀和高效。

---

## TensorFlow 2.0 的核心變化

### 1. Eager Execution 默認開啟

TensorFlow 2.0 默認使用 Eager Execution（急切執行），告別了繁瑣的 `tf.Session`：

```python
# TensorFlow 1.x
sess = tf.Session()
with sess.as_default():
    result = tf.add(1, 2).eval()

# TensorFlow 2.0
result = tf.add(1, 2)
print(result.numpy())  # 3
```

### 2. Keras 作為官方高階 API

`tf.keras` 成為構建和訓練模型的首選方式：

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
```

### 3. API 清理與統一

TensorFlow 2.0 清理了大量冗餘的 API：

```python
# 移除的 API
# tf.flags -> absl-py
# tf.contrib -> 移除或重構
# tf.app -> absl-py

# 保留的 API
# tf.data, tf.keras, tf.function, tf.distribute
```

### 4. 向後兼容性

使用 `tf.compat.v1` 保持與舊代碼的兼容性：

```python
import tensorflow as tf
import tensorflow.compat.v1 as tf1

# 使用舊版 API
with tf1.Session() as sess:
    result = sess.run(tf1.constant(1) + tf1.constant(2))
```

---

## 安裝和使用

### 安裝 TensorFlow 2.0

```bash
pip install tensorflow==2.0.0
```

### 驗證安裝

```python
import tensorflow as tf
print(tf.__version__)  # 2.0.0

# 確認 eager execution 開啟
print(tf.executing_eagerly())  # True
```

---

## 模型構建示例

### Keras Sequential API

```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(512, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation='softmax')
])
```

### Keras Functional API

```python
# Functional API 用於更複雜的模型
inputs = keras.Input(shape=(784,))
x = keras.layers.Dense(512, activation='relu')(inputs)
x = keras.layers.Dropout(0.2)(x)
outputs = keras.layers.Dense(10, activation='softmax')(x)
model = keras.Model(inputs, outputs)
```

### 自定義模型

```python
class MyModel(keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.dense1 = keras.layers.Dense(512, activation='relu')
        self.dropout = keras.layers.Dropout(0.2)
        self.dense2 = keras.layers.Dense(10, activation='softmax')

    def call(self, inputs, training=False):
        x = self.dense1(inputs)
        if training:
            x = self.dropout(x)
        return self.dense2(x)
```

---

## tf.function 加速

使用 `@tf.function` 裝飾器加速計算：

```python
@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images, training=True)
        loss = loss_object(labels, predictions)

    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss
```

---

## 效能優化

### GPU 支援

```python
# TensorFlow 自動使用可用的 GPU
# 明確指定 GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
```

### XLA 編譯

```python
# 啟用 XLA 編譯
@tf.function(jit_compile=True)
def train_step(x):
    ...
```

---

## 遷移指南

### 從 TF1 遷移到 TF2

```python
# 1. 啟用 TF2 行為
import tensorflow as tf
tf.enable_v2_behavior()

# 2. 替換 tf.Session
# 舊: sess = tf.Session()
# 新: 直接運算

# 3. 使用 tf.keras 替代舊的 tf.layers
# 4. 使用 tf.data 替代隊列
```

---

## 生態系統

### TensorFlow Extended (TFX)

端到端的機器學習平台：

```python
# TFX 元件
# ExampleGen: 數據攝入
# StatisticsGen: 數據統計
# SchemaGen: 數據模式
# ExampleValidator: 數據驗證
# Trainer: 模型訓練
# Evaluator: 模型評估
# InfraValidator: 服務驗證
# Pusher: 模型部署
```

### TensorFlow Lite

移動和邊緣裝置部署：

```python
# 轉換模型
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# 保存模型
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

### TensorFlow.js

瀏覽器和 Node.js 中的深度學習：

```javascript
// 加載模型
const model = await tf.loadLayersModel('model.json');

// 預測
const prediction = model.predict(inputTensor);
```

---

## 結語

TensorFlow 2.0 的發布開創了深度學習框架的新時代。通過 Eager Execution、統一的 Keras API 和清理後的 API，TensorFlow 變得更加易用和高效。

---

**延伸閱讀**

- [TensorFlow 2.0 Official Release](https://www.google.com/search?q=TensorFlow+2.0+official+release+September+2019)
- [TensorFlow+2.0+tutorial](https://www.google.com/search?q=TensorFlow+2.0+tutorial)
- [Migrating+to+TensorFlow+2](https://www.google.com/search?q=migrating+to+TensorFlow+2)

---

*本篇文章為「AI 程式人雜誌 2019 年 9 月號」TensorFlow 2.0 系列之一。*