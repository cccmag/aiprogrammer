# 2. TensorFlow 2.x 深度解析

## TensorFlow 2.0 的重大變化

TensorFlow 2.0 在 2019 年 9 月發布，带來了徹底的 API 改造：

1. **Eager execution 預設**：不再需要 `tf.Session`
2. **Keras 整合**：tf.keras 成為官方高階 API
3. **廢棄 API 清理**：移除過時的 tf.* 命名空間
4. **tf.function 裝飾器**：將 Python 程式碼編譯為效能最佳化的圖

## tf.function 與 AutoGraph

```python
import tensorflow as tf

@tf.function
def simple_function(x):
    return x ** 2

# 第一次呼叫會觸發追蹤（tracing）
result = simple_function(tf.constant(3.0))
print(result)  # tf.Tensor(9.0, shape=(), dtype=float32)
```

## 計算圖與效能

```python
import time

@tf.function
def compute():
    result = 0
    for i in tf.range(1000):
        result += i
    return result

# 效能測試
start = time.time()
for _ in range(100):
    compute()
print(f"耗時：{time.time() - start:.2f}秒")
```

## Keras Sequential API

```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

## Keras Functional API

```python
inputs = keras.Input(shape=(784,))
x = keras.layers.Dense(128, activation='relu')(inputs)
x = keras.layers.Dropout(0.2)(x)
outputs = keras.layers.Dense(10, activation='softmax')(x)
model = keras.Model(inputs, outputs)
```

## 訓練循環

```python
# 手動訓練迴圈
model = keras.Sequential([...])

optimizer = keras.optimizers.Adam()
loss_fn = keras.losses.SparseCategoricalCrossentropy()

for epoch in range(5):
    for batch in train_dataset:
        x, y = batch
        with tf.GradientTape() as tape:
            predictions = model(x)
            loss = loss_fn(y, predictions)
        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))
```

## tf.data 輸入管線

```python
dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
dataset = dataset.shuffle(10000)
dataset = dataset.batch(32)
dataset = dataset.prefetch(tf.data.AUTOTUNE)

for batch in dataset:
    # 訓練
    pass
```

## 預訓練模型

```python
from tensorflow.keras.applications import MobileNetV2

model = MobileNetV2(weights='imagenet')
predictions = model.predict(x_test)
```

## 參考資源

- https://www.google.com/search?q=TensorFlow+2.0+2.1+tutorial+eager+execution+tf.function+2020
- https://www.google.com/search?q=TensorFlow+Keras+Sequential+Functional+API+2020
- https://www.google.com/search?q=TensorFlow+2.0+performance+tf.function+autograph+2020