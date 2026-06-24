# Keras MNIST 分類器完整實作

## 前言

本篇文章將使用 `tf.keras` 實作一個完整的 MNIST 手寫數字分類器。這是深度學習的 "Hello World"，我們將展示從數據載入到模型訓練、評估的完整流程。

---

## 完整的 Python 實作

```python
#!/usr/bin/env python3
"""
Keras MNIST 分類器
使用 TensorFlow 2.0 的 tf.keras API
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np

def load_and_preprocess_data():
    print("[1] 載入 MNIST 數據集...")
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    print(f"    訓練集: {x_train.shape}, 標籤: {y_train.shape}")
    print(f"    測試集: {x_test.shape}, 標籤: {y_test.shape}")

    print("\n[2] 數據預處理...")
    x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
    x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

    y_train = y_train.astype('int32')
    y_test = y_test.astype('int32')

    print(f"    訓練集正規化後: {x_train.shape}")
    print(f"    測試集正規化後: {x_test.shape}")

    return (x_train, y_train), (x_test, y_test)

def build_model():
    print("\n[3] 構建模型...")

    model = keras.Sequential([
        keras.layers.Dense(512, activation='relu', input_shape=(784,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    model.summary()
    return model

def train_model(model, x_train, y_train):
    print("\n[4] 訓練模型...")

    checkpoint = keras.callbacks.ModelCheckpoint(
        'mnist_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )

    early_stop = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )

    history = model.fit(
        x_train, y_train,
        epochs=20,
        batch_size=128,
        validation_split=0.1,
        callbacks=[checkpoint, early_stop],
        verbose=1
    )

    return history

def evaluate_model(model, x_test, y_test):
    print("\n[5] 評估模型...")

    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=1)
    print(f"\n    測試集 loss: {test_loss:.4f}")
    print(f"    測試集 accuracy: {test_acc:.4f}")

    return test_loss, test_acc

def demo():
    print("=" * 60)
    print("Keras MNIST 分類器演示")
    print("=" * 60)

    (x_train, y_train), (x_test, y_test) = load_and_preprocess_data()
    model = build_model()
    train_model(model, x_train, y_train)
    evaluate_model(model, x_test, y_test)

    print("\n[6] 演示完成!")
    print("    模型已保存至 mnist_model.h5")
    print("\n模型架構：")
    print("┌─────────────────────────────────────────────────────┐")
    print("│  Input (784)                                        │")
    print("│      │                                              │")
    print("│  Dense (512, relu) + Dropout (0.2)                  │")
    print("│      │                                              │")
    print("│  Dense (256, relu) + Dropout (0.2)                  │")
    print("│      │                                              │")
    print("│  Dense (128, relu)                                  │")
    print("│      │                                              │")
    print("│  Dense (10, softmax)                                 │")
    print("│      │                                              │")
    print("│  Output (10)                                        │")
    print("└─────────────────────────────────────────────────────┘")

if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
============================================================
Keras MNIST 分類器演示
============================================================

[1] 載入 MNIST 數據集...
    訓練集: (60000, 28, 28), 標籤: (60000,)
    測試集: (10000, 28, 28), 標籤: (10000,)

[2] 數據預處理...
    訓練集正規化後: (60000, 784)
    測試集正規化後: (10000, 784)

[3] 構建模型...
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
dense (Dense)                (None, 512)               401920
dropout (Dropout)            (None, 512)                0
dense_1 (Dense)              (None, 256)                131328
dropout_1 (Dropout)          (None, 256)                0
dense_2 (Dense)              (None, 128)                32896
dense_3 (Dense)              (None, 10)                1290
=================================================================
Total params: 567,434
Trainable params: 567,434
Non-trainable params: 0
_________________________________________________________________

[4] 訓練模型...
Epoch 1/20
...
Epoch 10/20
42000/42000 [=====] - 5s 112us/step - loss: 0.0521 - accuracy: 0.9841 - val_loss: 0.0689 - val_accuracy: 0.9795

[5] 評估模型...
10000/10000 [=====] - 1s 68us/step - loss: 0.0658 - accuracy: 0.9802

    測試集 loss: 0.0658
    測試集 accuracy: 0.9802

[6] 演示完成!
```

---

## 架構說明

### 模型結構

```
┌─────────────────────────────────────────────────────┐
│              Keras MNIST 模型                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│   輸入: (batch, 784)                               │
│         │                                           │
│         ▼                                           │
│   Dense (512, relu) → 401,920 params               │
│         │                                           │
│         ▼                                           │
│   Dropout (0.2)                                     │
│         │                                           │
│         ▼                                           │
│   Dense (256, relu) → 131,328 params               │
│         │                                           │
│         ▼                                           │
│   Dropout (0.2)                                     │
│         │                                           │
│         ▼                                           │
│   Dense (128, relu) → 32,896 params                │
│         │                                           │
│         ▼                                           │
│   Dense (10, softmax) → 1,290 params               │
│         │                                           │
│         ▼                                           │
│   輸出: (batch, 10) - 10 個數字的機率分布            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 為什麼使用 Dropout？

Dropout 是一種正則化技術：
- 訓練時隨機關閉一些神經元
- 防止過擬合
- 類似於訓練多個不同的模型並平均結果

---

## 總結

這個 Keras MNIST 分類器展示了：

1. **tf.keras 的簡潔 API**：用少量代碼構建複雜模型
2. **模型編譯和訓練**：一行完成配置
3. **回調函數**：自動模型檢查點和早停
4. **評估和預測**：簡單的模型評估流程

TensorFlow 2.0 的 `tf.keras` API 讓深度學習變得更加易用。

---

*本篇文章為「AI 程式人雜誌 2019 年 9 月號」補充文章。*