# 模型訓練實務

## 簡介

模型訓練是機器學習的核心流程。本篇介紹從資料準備到模型訓練、評估的完整實務流程。

## 資料準備

### 載入資料

```python
from keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(f"訓練集: {x_train.shape}")
print(f"測試集: {x_test.shape}")
```

### 資料前處理

```python
import numpy as np

# 歸一化（將像素值縮放到 0-1）
x_train = x_train.reshape(-1, 784) / 255.0
x_test = x_test.reshape(-1, 784) / 255.0

# 標籤 one-hot 編碼
from keras.utils import to_categorical

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
```

### 訓練驗證集分割

```python
from sklearn.model_selection import train_test_split

x_train, x_val, y_train, y_val = train_test_split(
    x_train, y_train,
    test_size=0.1,
    random_state=42
)
```

## 建立模型

```python
from keras.models import Sequential
from keras.layers import Dense, Dropout

model = Sequential([
    Dense(512, activation='relu', input_shape=(784,)),
    Dropout(0.3),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(10, activation='softmax')
])

model.summary()
```

## 編譯模型

```python
from keras.optimizers import Adam

model.compile(
    optimizer=Adam(lr=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```

## 訓練模型

### 基本訓練

```python
history = model.fit(
    x_train, y_train,
    epochs=20,
    batch_size=32,
    validation_data=(x_val, y_val),
    verbose=1
)
```

### 訓練歷史

```python
import matplotlib.pyplot as plt

# 繪製 Loss 曲線
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# 繪製 Accuracy 曲線
plt.subplot(1, 2, 2)
plt.plot(history.history['acc'], label='Training Accuracy')
plt.plot(history.history['val_acc'], label='Validation Accuracy')
plt.title('Accuracy Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()
```

## 評估模型

### 在測試集上評估

```python
loss, accuracy = model.evaluate(x_test, y_test)
print(f"測試集 Loss: {loss:.4f}")
print(f"測試集準確率: {accuracy:.4f}")
```

### 預測

```python
# 預測
predictions = model.predict(x_test)
predicted_classes = np.argmax(predictions, axis=1)

# 混淆矩陣
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(np.argmax(y_test, axis=1), predicted_classes)
sns.heatmap(cm, annot=True, fmt='d')
plt.show()
```

## 過擬合處理

### 徵兆

- 訓練集準確率高，驗證集低
- 驗證集 loss 開始上升

### 解決方法

```python
from keras.layers import Dropout, BatchNormalization
from keras.regularizers import l2

# 1. Dropout
model = Sequential([
    Dense(512, activation='relu', input_shape=(784,)),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])

# 2. L2 正規化
model = Sequential([
    Dense(512, activation='relu', input_shape=(784,),
          kernel_regularizer=l2(0.01)),
    Dense(256, activation='relu',
          kernel_regularizer=l2(0.01)),
    Dense(10, activation='softmax')
])

# 3. Early Stopping
from keras.callbacks import EarlyStopping

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)
```

## 模型調參

### 超參數

- 學習率
- 批次大小
- 網路架構
- 訓練輪數

### Grid Search

```python
from sklearn.model_selection import GridSearchCV

# 定義要搜尋的參數
param_grid = {
    'batch_size': [32, 64, 128],
    'epochs': [10, 20],
    'optimizer': ['adam', 'sgd']
}

# Keras 沒有直接支援 sklearn 的 GridSearchCV
# 需要使用 wrapper 或手動訓練
```

## 模型儲存與部署

### 儲存整個模型

```python
model.save('model.h5')
```

### 儲存權重

```python
model.save_weights('weights.h5')
```

### 載入

```python
from keras.models import load_model

model = load_model('model.h5')
```

## 完整流程示例

```python
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.datasets import mnist
from keras.utils import to_categorical

# 1. 載入資料
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 2. 前處理
x_train = x_train.reshape(-1, 784) / 255.0
x_test = x_test.reshape(-1, 784) / 255.0
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# 3. 建立模型
model = Sequential([
    Dense(512, activation='relu', input_shape=(784,)),
    Dropout(0.4),
    Dense(256, activation='relu'),
    Dropout(0.4),
    Dense(10, activation='softmax')
])

# 4. 編譯
model.compile(
    optimizer=Adam(lr=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 5. 訓練
early_stop = EarlyStopping(monitor='val_loss', patience=5)
history = model.fit(x_train, y_train,
                    epochs=20,
                    batch_size=32,
                    validation_split=0.1,
                    callbacks=[early_stop])

# 6. 評估
loss, acc = model.evaluate(x_test, y_test)
print(f"測試集準確率: {acc:.4f}")

# 7. 儲存
model.save('mnist_model.h5')
```

## 練習題

1. 完成 MNIST 資料集的完整訓練流程
2. 觀察過擬合現象並嘗試用 Dropout 改善
3. 比較不同學習率對訓練的影響
4. 使用 Early Stopping 避免過擬合