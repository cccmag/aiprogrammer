# Keras 快速上手

## 簡介

Keras 是一個高階神經網路 API，最初由 François Chollet 開發（2015 年），後來整合到 TensorFlow 中。Keras 的設計理念是使用者友好、模組化、易擴展。

## 安裝

```bash
pip install keras
# Keras 已內建於 TensorFlow
pip install tensorflow
```

## 基本概念

### Sequential 模型

```python
from keras.models import Sequential
from keras.layers import Dense

# 建立序列模型
model = Sequential()

# 添加層
model.add(Dense(128, activation='relu', input_shape=(784,)))
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax'))
```

### Dense 層

全連接層（每個神經元與上一層所有神經元連接）：

```python
Dense(units, activation=None, input_shape=None)

# 範例
from keras.layers import Dense

# 第一層需要指定 input_shape
model.add(Dense(256, activation='relu', input_shape=(784,)))

# 後續層只需指定輸出維度
model.add(Dense(128, activation='relu'))

# 輸出層
model.add(Dense(10, activation='softmax'))
```

## 模型編譯

### 編譯模型

```python
model.compile(
    optimizer='adam',           # 優化器
    loss='categorical_crossentropy',  # 損失函數
    metrics=['accuracy']         # 評估指標
)
```

### 常用優化器

```python
from keras.optimizers import Adam, SGD, RMSprop

# Adam（預設推薦）
model.compile(optimizer=Adam(lr=0.001), ...)

# 隨機梯度下降
model.compile(optimizer=SGD(lr=0.01, momentum=0.9), ...)

# RMSprop
model.compile(optimizer=RMSprop(lr=0.001), ...)
```

### 常用損失函數

```python
# 二元分類
loss='binary_crossentropy'

# 多類分類
loss='categorical_crossentropy'

# 迴歸
loss='mse'
```

## 模型訓練

### fit 方法

```python
history = model.fit(
    x_train, y_train,
    epochs=10,                 # 訓練輪數
    batch_size=32,              # 批次大小
    validation_split=0.1,       # 驗證集比例
    verbose=1                   # 顯示模式
)
```

### 訓練過程

```python
# 訓練並記錄歷史
history = model.fit(x_train, y_train,
                    epochs=10,
                    batch_size=32,
                    validation_data=(x_val, y_val))

# 查看訓練歷史
print(history.history.keys())
# dict_keys(['loss', 'acc', 'val_loss', 'val_acc'])

# 繪製訓練曲線
import matplotlib.pyplot as plt

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'])
plt.show()
```

## 模型評估

### evaluate

```python
loss, accuracy = model.evaluate(x_test, y_test)
print(f"Loss: {loss:.4f}")
print(f"Accuracy: {accuracy:.4f}")
```

### predict

```python
# 預測
predictions = model.predict(x_test)

# 取得類別
predicted_classes = np.argmax(predictions, axis=1)
```

## 常見層

### Flatten

將多維輸入攤平：

```python
from keras.layers import Flatten

# 將 28x28 圖像攤平為 784
model.add(Flatten(input_shape=(28, 28)))
```

### Dropout

防止過擬合：

```python
from keras.layers import Dropout

model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))  # 50% 的神經元隨機關閉
```

### BatchNormalization

批次正規化：

```python
from keras.layers import BatchNormalization

model.add(Dense(256, activation='relu'))
model.add(BatchNormalization())
```

## 完整範例：衣物分類

```python
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.datasets import fashion_mnist
from keras.utils import to_categorical
from keras.optimizers import Adam

# 載入資料
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

# 前處理
x_train = x_train.reshape(-1, 784) / 255.0
x_test = x_test.reshape(-1, 784) / 255.0
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# 建立模型
model = Sequential([
    Dense(512, activation='relu', input_shape=(784,)),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])

# 編譯
model.compile(
    optimizer=Adam(lr=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 訓練
model.fit(x_train, y_train, epochs=10, batch_size=128, validation_split=0.1)

# 評估
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"測試集準確率: {test_acc:.4f}")
```

## 回調函數

```python
from keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
    TensorBoard
)

callbacks = [
    # 監控驗證 loss，10 輪沒進步就停止
    EarlyStopping(monitor='val_loss', patience=10),

    # 儲存最佳模型
    ModelCheckpoint('best_model.h5',
                    monitor='val_loss',
                    save_best_only=True),

    # 學習率衰減
    ReduceLROnPlateau(monitor='val_loss',
                      factor=0.5,
                      patience=5)
]

model.fit(x_train, y_train,
          callbacks=callbacks)
```

## 模型儲存與載入

```python
from keras.models import load_model

# 儲存整個模型
model.save('my_model.h5')

# 載入模型
model = load_model('my_model.h5')

# 只儲存權重
model.save_weights('my_weights.h5')

# 載入權重
model.load_weights('my_weights.h5')
```

## 練習題

1. 使用 Keras 建構一個分類器辨識 MNIST 手寫數字
2. 比較不同優化器的效果
3. 使用 Dropout 和 BatchNormalization 改善過擬合
4. 建立一個多層神經網路進行迴歸預測