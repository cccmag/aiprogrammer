#!/usr/bin/env python3
"""CNN 卷積運算實作"""

import numpy as np

try:
    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
    from keras.datasets import mnist
    from keras.utils import to_categorical
    HAS_KERAS = True
except ImportError:
    HAS_KERAS = False
    print("Keras not available")

def convolution_2d(image, kernel, stride=1, padding=0):
    if padding > 0:
        image = np.pad(image, ((padding, padding), (padding, padding)), mode='constant')

    kh, kw = kernel.shape
    ih, iw = image.shape

    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1

    output = np.zeros((out_h, out_w))

    for i in range(0, out_h * stride, stride):
        for j in range(0, out_w * stride, stride):
            region = image[i:i+kh, j:j+kw]
            output[i//stride, j//stride] = np.sum(region * kernel)

    return output

def max_pooling(image, pool_size=2, stride=2):
    kh, kw = pool_size, pool_size
    ih, iw = image.shape

    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1

    output = np.zeros((out_h, out_w))

    for i in range(0, out_h * stride, stride):
        for j in range(0, out_w * stride, stride):
            region = image[i:i+kh, j:j+kw]
            output[i//stride, j//stride] = np.max(region)

    return output

def create_sobel_kernel():
    sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    sobel_y = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])
    return sobel_x, sobel_y

def build_cnn_model(input_shape, num_classes):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def demo():
    print("=" * 60)
    print("CNN 卷積運算展示")
    print("=" * 60)

    image = np.array([
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5]
    ])

    kernel = np.array([
        [0, 1, 0],
        [1, 2, 1],
        [0, 1, 0]
    ])

    print("\n1. 簡單卷積運算：")
    print("-" * 40)
    print(f"輸入圖像：\n{image}")
    print(f"\n卷積核：\n{kernel}")

    result = convolution_2d(image, kernel)
    print(f"\n卷積結果：\n{result}")

    print("\n2. Max Pooling：")
    print("-" * 40)
    pooled = max_pooling(image, pool_size=2, stride=2)
    print(f"輸入圖像：\n{image}")
    print(f"\n池化結果：\n{pooled}")

    print("\n3. 邊緣檢測（Sobel）：")
    print("-" * 40)
    sobel_x, sobel_y = create_sobel_kernel()
    edge_x = convolution_2d(image, sobel_x)
    edge_y = convolution_2d(image, sobel_y)
    edge = np.sqrt(edge_x**2 + edge_y**2)
    print(f"Sobel X 結果：\n{edge_x}")
    print(f"Sobel Y 結果：\n{edge_y}")
    print(f"邊緣強度：\n{edge}")

    print("\n" + "=" * 60)
    print("NumPy 展示完成！")
    print("=" * 60)

    if HAS_KERAS:
        print("\n" + "=" * 60)
        print("Keras CNN 模型展示")
        print("=" * 60)

        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
        x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0
        y_train = to_categorical(y_train, 10)
        y_test = to_categorical(y_test, 10)

        print(f"\n訓練資料形狀：{x_train.shape}")
        print(f"標籤形狀：{y_train.shape}")

        model = build_cnn_model((28, 28, 1), 10)
        print("\n模型結構：")
        model.summary()

        print("\n開始訓練（1 epoch 示範）...")
        model.fit(x_train, y_train, epochs=1, batch_size=64, verbose=1)

        test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
        print(f"\n測試集準確率：{test_acc:.4f}")

        print("\n" + "=" * 60)
        print("展示完成！")
        print("=" * 60)
    else:
        print("\nKeras 未安裝，跳過 Keras 展示")
        print("安裝方式：pip install keras tensorflow")

if __name__ == "__main__":
    demo()