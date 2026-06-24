# MNIST 資料集處理

## MNIST 資料集概述

MNIST 是手寫數字辨識的經典資料集，包含 70,000 張 28x28 灰階圖片。

## 載入資料

```python
from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

print(f"訓練集: {x_train.shape}")
print(f"測試集: {x_test.shape}")
print(f"標籤: {np.unique(y_train)}")
```

## 基本預處理

```python
import numpy as np

x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

y_train = y_train.astype('int32')
y_test = y_test.astype('int32')

print(f"標準化後訓練集: {x_train.shape}, 範圍 [{x_train.min():.2f}, {x_train.max():.2f}]")
```

## 資料視覺化

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 5, figsize=(12, 8))
for i, ax in enumerate(axes.flat):
    ax.imshow(x_train[i].reshape(28, 28), cmap='gray')
    ax.set_title(f'Label: {y_train[i]}')
    ax.axis('off')

plt.tight_layout()
plt.show()
```

## 標籤編碼

```python
from tensorflow.keras.utils import to_categorical

y_train_onehot = to_categorical(y_train, num_classes=10)
y_test_onehot = to_categorical(y_test, num_classes=10)

print(f"One-hot 編碼後: {y_train_onehot.shape}")
print(f"範例: {y_train[0]} -> {y_train_onehot[0]}")
```

## 資料增強（Data Augmentation）

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    shear_range=0.1
)

datagen.fit(x_train.reshape(-1, 28, 28, 1))

fig, axes = plt.subplots(2, 5, figsize=(15, 6))
x_batch = x_train[0].reshape(1, 28, 28, 1)

for i, ax in enumerate(axes.flat):
    for x in datagen.flow(x_batch, batch_size=1):
        ax.imshow(x[0].reshape(28, 28), cmap='gray')
        ax.axis('off')
        break

plt.suptitle('Data Augmentation Examples')
plt.tight_layout()
plt.show()
```

## Fashion MNIST

Fashion MNIST 是 MNIST 的替代挑戰，更具難度：

```python
from tensorflow.keras.datasets import fashion_mnist

(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

fashion_labels = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat',
                  'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

fig, axes = plt.subplots(3, 5, figsize=(12, 8))
for i, ax in enumerate(axes.flat):
    ax.imshow(x_train[i], cmap='gray')
    ax.set_title(fashion_labels[y_train[i]])
    ax.axis('off')

plt.tight_layout()
plt.show()
```

## 批次處理

```python
batch_size = 32
train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_dataset = train_dataset.shuffle(10000).batch(batch_size)

for batch_x, batch_y in train_dataset.take(1):
    print(f"批次形狀: {batch_x.shape}, {batch_y.shape}")
    print(f"標籤: {batch_y[:5]}")
```

## tf.data 優化

```python
import tensorflow as tf

train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_dataset = (
    train_dataset
    .shuffle(10000)
    .map(lambda x, y: (tf.cast(x, tf.float32) / 255.0, y))
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)
```

## 驗證集分割

```python
from sklearn.model_selection import train_test_split

x_train_full, x_val, y_train_full, y_val = train_test_split(
    x_train, y_train, test_size=0.1, random_state=42
)

print(f"訓練集: {x_train_full.shape}")
print(f"驗證集: {x_val.shape}")
```

## 參考資源

- https://www.google.com/search?q=MNIST+dataset+preprocessing+Keras+TensorFlow+2019
- https://www.google.com/search?q=Fashion+MNIST+dataset+image+classification+2019
- https://www.google.com/search?q=data+augmentation+MNIST+Keras+ImageDataGenerator+2019