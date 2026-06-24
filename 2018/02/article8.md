# TensorFlow 入門

## 簡介

TensorFlow 是 Google 開發的開源深度學習框架，2015 年發布，2017 年發布 1.0 版本。目前是最受歡迎的深度學習框架之一。

## 安裝

```bash
pip install tensorflow
# 或指定版本
pip install tensorflow==1.5
```

## 基本概念

### 張量（Tensor）

TensorFlow 的基本資料結構：

- 0 維：純量（scalar）
- 1 維：向量（vector）
- 2 維：矩陣（matrix）
- N 維：N 維陣列

```python
import tensorflow as tf

# 建立張量
a = tf.constant(3)           # 純量
b = tf.constant([1, 2, 3])  # 向量
c = tf.constant([[1, 2], [3, 4]])  # 矩陣

print(a)
print(b)
print(c)
```

### 計算圖（Graph）

TensorFlow 1.x 使用計算圖模式：

```python
# 建立計算圖
x = tf.constant(2)
y = tf.constant(3)
z = x + y

# 建立 Session 來執行
with tf.Session() as sess:
    result = sess.run(z)
    print(result)  # 5
```

## 基本運算

### 算術運算

```python
a = tf.constant(5)
b = tf.constant(2)

with tf.Session() as sess:
    print(sess.run(a + b))   # 7
    print(sess.run(a - b))   # 3
    print(sess.run(a * b))   # 10
    print(sess.run(a / b))   # 2.5
```

### 矩陣運算

```python
A = tf.constant([[1, 2], [3, 4]])
B = tf.constant([[5, 6], [7, 8]])

with tf.Session() as sess:
    print(sess.run(tf.matmul(A, B)))  # 矩陣乘法
```

## 變數

### 建立變數

```python
# 建立變數
weights = tf.Variable(tf.random_normal([784, 256]))
biases = tf.Variable(tf.zeros([256]))

# 初始化所有變數
init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
```

### _assign 操作

```python
counter = tf.Variable(0)
new_value = tf.constant(100)

update = tf.assign(counter, new_value)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(sess.run(counter))  # 0
    sess.run(update)
    print(sess.run(counter))  # 100
```

## Placeholder

用於餵入資料：

```python
# 建立 placeholder
x = tf.placeholder(tf.float32, shape=(None, 784))
y = tf.placeholder(tf.float32, shape=(None, 10))

# 使用 placeholder
with tf.Session() as sess:
    #餵入資料
    result = sess.run(y, feed_dict={x: [[1]*784], y: [[0]*10]})
```

## Keras 高階 API

TensorFlow 整合了 Keras，可以更方便地建構模型：

```python
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam

# 建立模型
model = Sequential([
    Flatten(input_shape=(28, 28)),  # 784
    Dense(256, activation='relu'),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

# 編譯模型
model.compile(
    optimizer=Adam(lr=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 訓練模型
model.fit(x_train, y_train, epochs=10, batch_size=32)

# 評估
loss, accuracy = model.evaluate(x_test, y_test)
print(f"準確率: {accuracy}")
```

## 完整範例：手寫數字辨識

```python
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.datasets import mnist
from keras.utils import to_categorical

# 載入資料
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 前處理
x_train = x_train.reshape(-1, 784) / 255.0
x_test = x_test.reshape(-1, 784) / 255.0
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# 建立模型
model = Sequential([
    Dense(512, activation='relu', input_shape=(784,)),
    Dense(256, activation='relu'),
    Dense(10, activation='softmax')
])

# 編譯
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 訓練
model.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.1)

# 評估
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"測試集準確率: {test_acc:.4f}")
```

## Eager Execution（TensorFlow 1.5+）

TensorFlow 1.5 支援 eager execution，像 NumPy 一樣直覺：

```python
import tensorflow as tf
tf.enable_eager_execution()

# 直接執行，不需要 Session
a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])
print(tf.matmul(a, b))
```

## 儲存與載入模型

```python
from keras.models import load_model

# 儲存
model.save('my_model.h5')

# 載入
model = load_model('my_model.h5')

# 預測
predictions = model.predict(x_test)
```

## 建議

1. **新手推薦從 Keras 開始** - 較容易上手
2. **理解基本概念** - 張量、計算圖、Session
3. **多做練習** - 從簡單模型開始
4. **閱讀官方文檔** - tensorflow.org 有詳細教程