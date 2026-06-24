#!/usr/bin/env python3
"""
Keras MNIST 分類器演示
使用 TensorFlow 2.0 的 tf.keras API
"""

import tensorflow as tf
from tensorflow import keras

def demo():
    print("=" * 60)
    print("Keras MNIST 分類器演示")
    print("=" * 60)

    print(f"\n[1] TensorFlow 版本: {tf.__version__}")
    print(f"    Eager Execution: {tf.executing_eagerly()}")

    print("\n[2] 載入 MNIST 數據集...")
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    print(f"    訓練集: {x_train.shape}")
    print(f"    測試集: {x_test.shape}")

    print("\n[3] 數據預處理...")
    x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
    x_test = x_test.reshape(-1, 784).astype('float32') / 255.0
    print(f"    正規化後形狀: {x_train.shape}")

    print("\n[4] 構建模型...")
    model = keras.Sequential([
        keras.layers.Dense(512, activation='relu', input_shape=(784,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    print(f"    參數總量: {model.count_params():,}")

    print("\n[5] 快速訓練演示（只訓練1個epoch）...")
    model.fit(x_train[:10000], y_train[:10000],
              epochs=1, batch_size=128, verbose=1)

    print("\n[6] 評估模型...")
    loss, acc = model.evaluate(x_test[:1000], y_test[:1000], verbose=0)
    print(f"    測試 loss: {loss:.4f}")
    print(f"    測試 accuracy: {acc:.4f}")

    print("\n[7] 演示完成！")

if __name__ == "__main__":
    demo()