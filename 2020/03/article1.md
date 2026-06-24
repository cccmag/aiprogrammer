# TensorFlow 2.0 自動微分

## tf.GradientTape

TensorFlow 2.0 的自動微分透過 `tf.GradientTape` 實現：

```python
import tensorflow as tf

# 基本用法
x = tf.Variable(3.0)

with tf.GradientTape() as tape:
    y = x ** 2

dy_dx = tape.gradient(y, x)
print(dy_dx)  # tf.Tensor(6.0, shape=(), dtype=float32)
```

## 多層次梯度

```python
x = tf.Variable(tf.random.normal([3, 3]))

with tf.GradientTape() as tape:
    with tf.GradientTape() as tape2:
        y = x ** 3
    dy_dx = tape2.gradient(y, x)
d2y_dx2 = tape.gradient(dy_dx, x)
```

## 訓練中的梯度

```python
# 模型與損失
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dense(10)
])

@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x, training=True)
        loss = tf.reduce_mean(tf.keras.losses.sparse_categorical_crossentropy(y, predictions))

    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer = tf.keras.optimizers.Adam()
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss
```

## tf.function 裝飾器

```python
@tf.function
def compute(x):
    result = 0
    for i in tf.range(100):
        result += i * x
    return result
```

## watch 機制

```python
# 訓練變數預設被 watch
trainable_var = tf.Variable(2.0)
with tf.GradientTape() as tape:
    result = trainable_var ** 2
print(tape.gradient(result, trainable_var))

# 非變數需要手動 watch
constant = tf.constant(3.0)
with tf.GradientTape() as tape:
    tape.watch(constant)
    result = constant ** 2
print(tape.gradient(result, constant))
```

## 客製化訓練

```python
class MyModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(10, activation='relu')
        self.dense2 = tf.keras.layers.Dense(10)

    def call(self, x):
        x = self.dense1(x)
        return self.dense2(x)

model = MyModel()
optimizer = tf.keras.optimizers.Adam()

@tf.function
def train_epoch(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x)
        loss = tf.reduce_mean(tf.keras.losses.sparse_categorical_crossentropy(y, predictions))
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss
```

## 參考資源

- https://www.google.com/search?q=TensorFlow+2.0+GradientTape+autograd+tutorial+2020
- https://www.google.com/search?q=TensorFlow+tf.function+Autograph+2020+tutorial
- https://www.google.com/search?q=TensorFlow+custom+training+loop+GradientTape+2020