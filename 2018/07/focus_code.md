# 程式實作：Keras 模型建構實務

## 簡介

本實作使用 Keras 建構一個完整的圖像分類模型，展示從資料處理、模型建構、訓練到評估的完整流程。完整程式碼在 `_code/keras_demo.py`。

## 環境設定

```bash
pip install tensorflow keras numpy matplotlib
```

## 資料處理

```python
import numpy as np
from keras.datasets import mnist
from keras.utils import to_categorical

# 載入 MNIST 資料集
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 資料前處理
x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

# One-hot 編碼
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
```

## 模型建構

```python
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization

def create_model():
    model = Sequential([
        Dense(512, activation='relu', input_shape=(784,)),
        BatchNormalization(),
        Dropout(0.2),

        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.2),

        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.2),

        Dense(10, activation='softmax')
    ])
    return model

model = create_model()
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```

## 訓練設定

```python
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard

callbacks = [
    ModelCheckpoint('best_model.h5', monitor='val_acc', save_best_only=True),
    EarlyStopping(patience=5, restore_best_weights=True),
    TensorBoard(log_dir='./logs')
]

history = model.fit(
    x_train, y_train,
    epochs=30,
    batch_size=128,
    validation_split=0.2,
    callbacks=callbacks
)
```

## 評估與預測

```python
# 評估模型
loss, accuracy = model.evaluate(x_test, y_test)
print(f"Test accuracy: {accuracy:.4f}")

# 預測
predictions = model.predict(x_test[:10])
print(f"Predictions: {np.argmax(predictions, axis=1)}")
```

## 執行方式

```bash
cd _code
python3 keras_demo.py
```

## 延伸練習

1. **嘗試不同架構**：增加/減少層數、調整神經元數量
2. **使用不同資料集**：CIFAR-10、Fashion-MNIST
3. **資料增強**：使用 ImageDataGenerator 增加訓練資料
4. **遷移學習**：使用預訓練模型進行特徵提取
5. **模型視覺化**：使用 TensorBoard 觀察訓練過程