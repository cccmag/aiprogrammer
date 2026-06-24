# tf.keras 深度學習

## 完整的 Keras 使用指南

在 TensorFlow 2.0 中，`tf.keras` 成為構建深度學習模型的標準方式。本章將詳細介紹如何使用 tf.keras 進行深度學習開發。

---

## tf.keras 與純 Keras 的區別

### 統一後的 API

```python
# 兩種導入方式是等價的
import tensorflow as tf
from tensorflow import keras

# 或者
import keras  # 仍然可以使用，但底層實際是 tf.keras
```

### TensorFlow 特定功能

```python
# tf.keras 專有的功能
from tensorflow import keras

# 分散式訓練策略
strategy = tf.distribute.MirroredStrategy()

# TPU 支援
resolver = tf.distribute.cluster_resolver.TPUClusterResolver()
tf.config.experimental_connect_to_cluster(resolver)
tf.tpu.experimental.initialize_tpu_system(resolver)

# TensorBoard 回調
tensorboard_cb = keras.callbacks.TensorBoard(log_dir='./logs')
```

---

## 模型構建實例

### 圖像分類：MNIST

```python
import tensorflow as tf
from tensorflow import keras

# 載入數據
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# 數據預處理
x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

# 構建模型
model = keras.Sequential([
    keras.layers.Dense(512, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# 編譯模型
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 訓練模型
history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.1
)

# 評估
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'測試準確率: {test_acc:.4f}')
```

### 文字分類：IMDB

```python
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 載入數據
vocab_size = 10000
max_length = 200
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=vocab_size)

# 填充序列
x_train = pad_sequences(x_train, maxlen=max_length)
x_test = pad_sequences(x_test, maxlen=max_length)

# 嵌入 + LSTM 模型
model = keras.Sequential([
    keras.layers.Embedding(vocab_size, 128, input_length=max_length),
    keras.layers.Bidirectional(keras.layers.LSTM(64)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.2)
```

### CNN 圖像分類：CIFAR-10

```python
from tensorflow.keras.datasets import cifar10

# 載入數據
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# 正規化
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# 資料增強
data_augmentation = keras.Sequential([
    keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
    keras.layers.experimental.preprocessing.RandomRotation(0.1),
])

# CNN 模型
inputs = keras.Input(shape=(32, 32, 3))
x = data_augmentation(inputs)
x = keras.layers.Conv2D(32, 3, activation='relu')(x)
x = keras.layers.MaxPooling2D(2)(x)
x = keras.layers.Conv2D(64, 3, activation='relu')(x)
x = keras.layers.MaxPooling2D(2)(x)
x = keras.layers.Conv2D(64, 3, activation='relu')(x)
x = keras.layers.Flatten()(x)
x = keras.layers.Dense(64, activation='relu')(x)
outputs = keras.layers.Dense(10, activation='softmax')(x)

model = keras.Model(inputs, outputs)
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(x_train, y_train, epochs=20, validation_split=0.1)
```

---

## 回調函數

### 常用回調

```python
callbacks = [
    # 早停
    keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    ),
    # 學習率調整
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=2,
        verbose=1
    ),
    # 模型檢查點
    keras.callbacks.ModelCheckpoint(
        'best_model.h5',
        monitor='val_accuracy',
        save_best_only=True
    ),
    # TensorBoard
    keras.callbacks.TensorBoard(
        log_dir='./logs',
        histogram_freq=1
    )
]

model.fit(x_train, y_train,
          epochs=20,
          callbacks=callbacks)
```

---

## 自定義層

### 簡單的自定義層

```python
class MyDenseLayer(keras.layers.Layer):
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

    def get_config(self):
        return {'units': self.units}
```

### 自定義模型

```python
class GAN(keras.Model):
    def __init__(self, discriminator, generator):
        super().__init__()
        self.discriminator = discriminator
        self.generator = generator

    def compile(self, d_optimizer, g_optimizer, loss_fn):
        super().compile()
        self.d_optimizer = d_optimizer
        self.g_optimizer = g_optimizer
        self.loss_fn = loss_fn

    def train_step(self, real_images):
        # 訓練邏輯
        ...
```

---

## 遷移學習

### 預訓練模型的使用

```python
# 載入預訓練模型
base_model = keras.applications.VGG16(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# 凍結基礎模型
base_model.trainable = False

# 添加分類頭
model = keras.Sequential([
    base_model,
    keras.layers.GlobalAveragePooling2D(),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(train_dataset, epochs=10)
```

---

## 模型保存和加載

### 保存整個模型

```python
# 保存
model.save('my_model.h5')

# 加載
model = keras.models.load_model('my_model.h5')
```

### 只保存權重

```python
# 保存權重
model.save_weights('my_weights.h5')

# 加載權重
model.load_weights('my_weights.h5')
```

---

## 結語

tf.keras 提供了完整的深度學習開發工具鏈，從模型構建到訓練、評估、部署，都能夠優雅地完成。掌握 tf.keras 是每個深度學習工程師的必備技能。

---

**延伸閱讀**

- [tf.keras Documentation](https://www.google.com/search?q=tf.keras+official+documentation)
- [Keras+Tutorial](https://www.google.com/search?q=Keras+tutorial+beginners)
- [MNIST+keras+example](https://www.google.com/search?q=MNIST+Keras+tutorial)

---

*本篇文章為「AI 程式人雜誌 2019 年 9 月號」TensorFlow 2.0 系列之三。*