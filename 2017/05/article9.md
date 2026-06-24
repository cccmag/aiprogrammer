# 文章 9：TensorFlow 基礎

## 前言

TensorFlow 是 Google 開發的開源深度學習框架，廣泛應用於學術研究與工業部署。本章節介紹 TensorFlow 的基礎用法。

## 安裝 TensorFlow

```bash
pip install tensorflow
```

## 基本概念

### 張量（Tensor）

TensorFlow 的基本資料結構：

```python
import tensorflow as tf

# 0維張量（標量）
scalar = tf.constant(5)

# 1維張量（向量）
vector = tf.constant([1, 2, 3])

# 2維張量（矩陣）
matrix = tf.constant([[1, 2], [3, 4]])

# 查看形狀
print(scalar.shape)  # ()
print(vector.shape)  # (3,)
print(matrix.shape)  # (2, 2)
```

### 計算圖（Computation Graph）

TensorFlow 1.x 使用靜態圖：

```python
import tensorflow as tf

# 定義計算圖
a = tf.constant(2)
b = tf.constant(3)
c = a + b

# 執行
with tf.Session() as sess:
    result = sess.run(c)
    print(result)  # 5
```

### 變數與佔位符

```python
# 變數（可訓練）
W = tf.Variable(tf.random_normal([784, 128]))
b = tf.Variable(tf.zeros([128]))

# 佔位符（餵入數據）
x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])
```

## Keras 高階 API

TensorFlow 已內建 Keras：

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

model = Sequential([
    Dense(128, activation='relu', input_shape=(784,)),
    Dropout(0.5),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
```

## 建立模型

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])
```

## 訓練與評估

```python
# 訓練
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# 評估
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test accuracy: {accuracy:.4f}')

# 預測
predictions = model.predict(X_new)
```

## 儲存與載入模型

```python
# 儲存整個模型
model.save('my_model.h5')

# 載入模型
from tensorflow.keras.models import load_model
loaded_model = load_model('my_model.h5')
```

## 總結

TensorFlow 從 1.x 到 2.x 經歷了巨大變化，eager execution 與 Keras 整合使開發更加直觀。掌握 TensorFlow 是進入深度學習領域的重要技能。

## 延伸閱讀

- https://www.google.com/search?q=TensorFlow+tutorial+beginners+2017
- https://www.google.com/search?q=Keras+TensorFlow+MNIST+example