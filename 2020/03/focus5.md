# 5. Keras 與 tf.keras

## Keras 的定位

Keras 最初是一個獨立的深度學習 API，專注於快速原型開發。TensorFlow 2.0 將 Keras（tf.keras）作為官方高階 API，提供從研究到生產的完整流程。

## tf.keras vs 獨立 Keras

| 特性 | tf.keras | 獨立 Keras |
|------|----------|------------|
| 張量後端 | TF (CUDA/cuDNN) | 多後端 |
| 模型部署 | TF Lite / TF Serving | 需轉換 |
| TF 特功能 | 原生支援 | 有限 |
| tf.data | 原生支援 | 需要 adapter |
| 生態系 | 完整 | 獨立發展 |

## Sequential API

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(256, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

## Functional API

```python
# 多輸入、多輸出模型
inputs = tf.keras.Input(shape=(784,))
x = tf.keras.layers.Dense(64, activation='relu')(inputs)
x = tf.keras.layers.Dense(32, activation='relu')(x)
output1 = tf.keras.layers.Dense(10, activation='softmax', name='digit')(x)
output2 = tf.keras.layers.Dense(1, name='confidence')(x)

model = tf.keras.Model(inputs=inputs, outputs=[output1, output2])
```

## Callbacks

```python
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=3),
    tf.keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only=True),
    tf.keras.callbacks.TensorBoard(log_dir='./logs')
]

model.fit(x_train, y_train, epochs=50, callbacks=callbacks)
```

## 自訂層

```python
class MyDenseLayer(tf.keras.layers.Layer):
    def __init__(self, units):
        super().__init__()
        self.units = units

    def build(self, input_shape):
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer='glorot_uniform',
            trainable=True
        )
        self.b = self.add_weight(
            shape=(self.units,),
            initializer='zeros',
            trainable=True
        )

    def call(self, inputs):
        return tf.matmul(inputs, self.w) + self.b
```

## 自訂訓練

```python
@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x, training=True)
        loss = loss_fn(y, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss
```

## 模型視覺化

```python
# 顯示模型結構
tf.keras.utils.plot_model(
    model,
    to_file='model.png',
    show_shapes=True,
    show_layer_names=True
)

# 模型摘要
model.summary()
```

## 參考資源

- https://www.google.com/search?q=Keras+tf.keras+TensorFlow+2+tutorial+2020
- https://www.google.com/search?q=tf.keras+Sequential+Functional+API+callbacks+2020
- https://www.google.com/search?q=Keras+TensorFlow+custom+layer+training+loop+2020