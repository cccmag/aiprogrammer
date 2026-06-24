# Keras：高階 API 的崛起

## 讓深度學習變得簡單

### Keras 的設計哲學

Keras 由 François Chollet 開發，核心理念是：**人類應該能夠在不看框架文件的情況下，用 Keras 實現深度學習**。

四大原則：
1. 模組化 — 每個層、優化器、損失函數都是獨立模組
2. 最小化 — 最少的使用範例就能解釋核心概念
3. 可擴展性 — 容易新增自訂層、損失函數
4. Python 原生 — 不需要額外設定檔

### Sequential API：快速原型

```python
from keras.models import Sequential
from keras.layers import Dense, Dropout

model = Sequential([
    Dense(512, activation='relu', input_shape=(784,)),
    Dropout(0.2),
    Dense(256, activation='relu'),
    Dropout(0.2),
    Dense(10, activation='softmax')
])
```

### Functional API：複雜網路

處理多輸入、多輸出、非順序結構：

```python
from keras.layers import Input, Dense, concatenate
from keras.models import Model

# 兩個輸入分支
input1 = Input(shape=(784,))
input2 = Input(shape=(128,))

x1 = Dense(64, activation='relu')(input1)
x2 = Dense(64, activation='relu')(input2)

merged = concatenate([x1, x2])
output = Dense(10, activation='softmax')(merged)

model = Model(inputs=[input1, input2], outputs=output)
```

### 預訓練模型：遷移學習

Keras 內建多個預訓練模型：

```python
from keras.applications import VGG16, ResNet50

# VGG16 預訓練模型
vgg = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# 凍結權重，只訓練新加入的層
for layer in vgg.layers:
    layer.trainable = False

# 添加分類頭
x = vgg.output
x = Dense(256, activation='relu')(x)
predictions = Dense(10, activation='softmax')(x)
model = Model(inputs=vgg.input, outputs=predictions)
```

### 訓練迴圈

```python
# 編譯模型
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 訓練
model.fit(
    x_train, y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    callbacks=[EarlyStopping(patience=5)]
)
```

### Callback 機制

訓練過程中的鉤子：

```python
from keras.callbacks import ModelCheckpoint, TensorBoard, ReduceLROnPlateau

callbacks = [
    ModelCheckpoint('best_model.h5', save_best_only=True),
    TensorBoard(log_dir='./logs'),
    ReduceLROnPlateau(factor=0.5, patience=3)
]

model.fit(x_train, y_train, callbacks=callbacks)
```

### 小結

Keras 以其簡潔的 API 成為深度學習入首選。2018 年整合進 TensorFlow 核心後，生態系更加完整。

---

**下一步**：[Eager Execution 動態圖模式](focus3.md)