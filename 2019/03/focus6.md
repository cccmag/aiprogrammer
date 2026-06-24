# 6. Keras/TensorFlow 入門

## Keras 簡介

Keras 是一個高層類神經網路 API，支援快速實驗與原型開發。2019 年 3 月 Keras 已整合為 TensorFlow 的官方高層 API。

## 安裝

```bash
pip install tensorflow keras numpy matplotlib
```

## 基本 MLP 模型

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

print(f"TensorFlow 版本: {tf.__version__}")
print(f"Keras 版本: {keras.__version__}")

model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(784,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.summary()
```

## 編譯模型

```python
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

## 訓練模型

```python
from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

history = model.fit(
    x_train, y_train,
    epochs=5,
    batch_size=32,
    validation_split=0.1,
    verbose=1
)
```

## 評估模型

```python
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=1)
print(f"\n測試集準確率: {test_accuracy:.2%}")
```

## 預測

```python
predictions = model.predict(x_test[:5])
print(f"\n預測結果（前5筆）:")
for i, pred in enumerate(predictions):
    print(f"  樣本 {i}: 預測={np.argmax(pred)}, 實際={y_test[i]}")
```

## Functional API

對於多輸入、多輸出或共享層的模型，使用 Functional API。

```python
from tensorflow.keras import layers, Model

inputs = layers.Input(shape=(784,))
x = layers.Dense(64, activation='relu')(inputs)
x = layers.Dense(64, activation='relu')(x)
outputs = layers.Dense(10, activation='softmax')(x)

model = Model(inputs=inputs, outputs=outputs)
model.compile(optimizer='adam',
             loss='sparse_categorical_crossentropy',
             metrics=['accuracy'])

model.summary()
```

## Keras Tuner 超參數搜尋

```python
try:
    from kerastuner import RandomSearch

    def build_model(hp):
        model = keras.Sequential()
        model.add(layers.Dense(
            units=hp.Int('units', min_value=32, max_value=512, step=32),
            activation='relu',
            input_shape=(784,)
        ))
        model.add(layers.Dense(10, activation='softmax'))
        model.compile(
            optimizer=keras.optimizers.Adam(
                hp.Float('learning_rate', 1e-4, 1e-2, sampling='log')
            ),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    tuner = RandomSearch(build_model, objective='val_accuracy', max_trials=5)
    tuner.search(x_train, y_train, epochs=3, validation_split=0.2)
    best_model = tuner.get_best_models(1)[0]
except ImportError:
    print("Keras Tuner 未安裝")
```

## 保存與載入模型

```python
model.save('my_model.h5')

from tensorflow.keras.models import load_model
loaded_model = load_model('my_model.h5')
```

## Callbacks

```python
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

callbacks = [
    EarlyStopping(monitor='val_loss', patience=3),
    ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True)
]

history = model.fit(
    x_train, y_train,
    epochs=10,
    callbacks=callbacks
)
```

## TensorFlow 2.0 的 Eager Execution

```python
import tensorflow as tf

tf.enable_eager_execution()

a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])

c = tf.matmul(a, b)
print(f"矩陣乘法結果:\n{c.numpy()}")
```

## 參考資源

- https://www.google.com/search?q=Keras+TensorFlow+tutorial+MLP+MNIST+2019
- https://www.google.com/search?q=TensorFlow+2.0+eager+execution+Keras+API+2019
- https://www.google.com/search?q=Keras+sequential+model+functional+API+2019