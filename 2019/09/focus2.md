# Keras 的崛起

## 從封裝器到官方 API

Keras 的故事是一個關於易用性和社群力量的傳奇。從 2015 年 François Chollet 創建的一個高階封裝庫，到 2019 年成為 TensorFlow 的官方 API，Keras 徹底改變了我們構建深度學習模型的方式。

---

## Keras 的起源

### 2015 年：誕生

Keras 首次發布於 2015 年，作為 Theano 和 TensorFlow 的高階封裝：

```python
# 最初的 Keras
from keras.models import Sequential
from keras.layers import Dense, Activation

model = Sequential()
model.add(Dense(64, input_dim=784))
model.add(Activation('relu'))
model.add(Dense(10))
model.add(Activation('softmax'))
```

### 設計理念

Keras 的設計哲學源於幾個核心原則：

```
┌─────────────────────────────────────────────────────┐
│              Keras 設計原則                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│   1. 友好易用 (User-friendly)                       │
│      - 直覺的 API，減少認知負擔                      │
│      - 清晰的錯誤消息                                │
│                                                     │
│   2. 模組化 (Modular)                               │
│      - 每個組件都是獨立可用的                        │
│      - 模型、層、優化器皆可單獨使用                   │
│                                                     │
│   3. 容易擴展 (Extensible)                          │
│      - 支持自定義層                                 │
│      - 支持自定義損失函數和指標                      │
│                                                     │
│   4. Python 優先                                    │
│      - 原生 Python，不依賴外部配置                    │
│      - 動態計算圖                                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Keras 的發展歷程

### 2015-2016：Theano 時代

Keras 最初基於 Theano：

```python
# 基於 Theano 的 Keras
# 支援 CNN、RNN、LSTM、多輸入多輸出
# 訓練循環完全可自定義
```

### 2016-2017：TensorFlow 整合

TensorFlow 發布後，Keras 新增 TensorFlow 後端支持：

```python
# 設定後端
# ~/.keras/keras.json
{
    "backend": "tensorflow"
}
```

### 2017-2018：功能完善

增加大量新功能：
- Keras Applications：預訓練模型庫
- Keras Callbacks：訓練回調
- Keras Utilities：工具函數

### 2019：官方整合

TensorFlow 2.0 宣佈 `tf.keras` 作為官方高階 API：

```
Keras 版本           TensorFlow 版本
3.1.0          →    2.0.0 (整合)
2.3.0          →    2.1.0 (同步發布)
```

---

## Keras API 詳解

### Sequential API

最簡單的模型構建方式：

```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.4),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
```

### Functional API

構建複雜拓撲結構：

```python
# 多輸入
input_text = keras.Input(shape=(100,), name='text')
input_image = keras.Input(shape=(784,), name='image')

# 共用層
shared_dense = keras.layers.Dense(128)

text_features = shared_dense(input_text)
image_features = shared_dense(input_image)

# 融合
merged = keras.layers.concatenate([text_features, image_features])
output = keras.layers.Dense(1)(merged)

model = keras.Model([input_text, input_image], output)
```

### Subclassing API

完全靈活的自定義：

```python
class TransformerBlock(keras.Model):
    def __init__(self, embed_dim, num_heads, ff_dim):
        super().__init__()
        self.att = keras.layers.MultiHeadAttention(num_heads, embed_dim)
        self.ffn = keras.Sequential([
            keras.layers.Dense(ff_dim, activation='relu'),
            keras.layers.Dense(embed_dim)
        ])
        self.layernorm1 = keras.layers.LayerNormalization()
        self.layernorm2 = keras.layers.LayerNormalization()

    def call(self, inputs, training=False):
        attn_output = self.att(inputs, inputs)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        return self.layernorm2(out1 + ffn_output)
```

---

## 常用層

### 核心層

```python
# 密集層
keras.layers.Dense(128, activation='relu')

#  Dropout
keras.layers.Dropout(0.5)

# 扁平化
keras.layers.Flatten()

# 重塑
keras.layers.Reshape(target_shape)

# 連接
keras.layers.Concatenate()
```

### 卷積層

```python
# 2D 卷積
keras.layers.Conv2D(32, kernel_size=3, activation='relu')

# 3D 卷積
keras.layers.Conv3D(32, kernel_size=3, activation='relu')

# 空洞卷積
keras.layers.Conv2D(32, kernel_size=3, dilation_rate=2)
```

### 循環層

```python
# LSTM
keras.layers.LSTM(128, return_sequences=True)

# GRU
keras.layers.GRU(128, return_sequences=True)

# Bidirectional
keras.layers.Bidirectional(keras.layers.LSTM(128))
```

---

## 模型訓練

### 編譯

```python
model.compile(
    optimizer='adam',           # 或 tf.keras.optimizers.Adam()
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

### 訓練

```python
# 基本訓練
model.fit(x_train, y_train,
          epochs=10,
          batch_size=32,
          validation_split=0.2)

# 使用 tf.data
model.fit(train_dataset,
          epochs=10,
          validation_data=val_dataset,
          callbacks=[keras.callbacks.EarlyStopping(patience=3)])
```

### 評估和預測

```python
# 評估
loss, accuracy = model.evaluate(x_test, y_test)

# 預測
predictions = model.predict(x_new)
```

---

## 預訓練模型

### Keras Applications

```python
# 圖像分類
from tensorflow.keras.applications import ResNet50, VGG16, InceptionV3

model = ResNet50(weights='imagenet')

# 移除頂部，用於特徵提取
base_model = ResNet50(weights='imagenet', include_top=False)
```

### 模型微調

```python
# 凍結基礎層
for layer in base_model.layers:
    layer.trainable = False

# 添加自定義分類器
model = keras.Sequential([
    base_model,
    keras.layers.GlobalAveragePooling2D(),
    keras.layers.Dense(10, activation='softmax')
])
```

---

## 結語

Keras 的崛起證明了「易用性」在深度學習中的重要性。從一個簡單的封裝庫，成長為 TensorFlow 的官方 API，Keras 讓更多人能夠接觸和使用深度學習技術。

它的成功也啟示我們：有時候，最好的工具不是最強大的，而是最易用的。

---

**延伸閱讀**

- [Keras Official Documentation](https://www.google.com/search?q=Keras+official+documentation)
- [François+Chollet+Keras](https://www.google.com/search?q=Fran%C3%A7ois+Chollet+Keras+creator)
- [Keras+Deep+Learning+Tutorial](https://www.google.com/search?q=Keras+tutorial+deep+learning)

---

*本篇文章為「AI 程式人雜誌 2019 年 9 月號」TensorFlow 2.0 系列之二。*