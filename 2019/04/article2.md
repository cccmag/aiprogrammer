# TensorFlow 2.0 搶先看：Eager Execution 與 Keras 整合

## 前言

TensorFlow 2.0 在 2019 年 9 月正式發布，其中最重要的改變是預設啟用 Eager Execution 和深度整合 Keras。

## Eager Execution（即時執行）

### 動態圖模式

```python
import tensorflow as tf

# TensorFlow 1.x 需要 session
# with tf.Session() as sess:
#     result = sess.run(output, feed_dict={input: data})

# TensorFlow 2.0 直接執行
x = tf.constant([[1.0, 2.0], [3.0, 4.0]])
y = tf.constant([[5.0, 6.0], [7.0, 8.0]])

result = x @ y  # 矩陣乘法
print(result)  # 立即輸出結果
```

### 優勢

- **除錯方便**：可以直接列印張量
- **直覺**：像普通 Python 程式碼一樣
- **更簡潔**：減少樣板程式碼

## Keras 整合

### tf.keras 是官方高階 API

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

### Keras Subclassing API

```python
class MyModel(keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = keras.layers.Dense(128, activation='relu')
        self.dense2 = keras.layers.Dense(10, activation='softmax')

    def call(self, inputs):
        x = self.dense1(inputs)
        return self.dense2(x)

model = MyModel()
```

## 模型訓練

```python
# 載入資料
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# 正規化
x_train = x_train / 255.0
x_test = x_test / 255.0

# 訓練
model.fit(x_train, y_train, epochs=5, validation_split=0.1)

# 評估
model.evaluate(x_test, y_test)
```

## 遷移到 TF 2.0

```python
# 使用 tf.compat.v1 作為過渡
import tensorflow.compat.v1 as tf1
tf1.disable_v2_behavior()
```

## 結論

TensorFlow 2.0 大幅簡化了 API，提高了易用性。Eager Execution 和 Keras 整合使得實驗和開發更加高效。

---

**延伸閱讀**

- [TensorFlow 2.0 官方文檔](https://www.google.com/search?q=TensorFlow+2.0+tutorial)
- [Keras 中文文檔](https://www.google.com/search?q=Keras+documentation+Chinese)