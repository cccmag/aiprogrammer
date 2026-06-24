# tf.data 數據管線

## 高效的數據輸入管道

tf.data 是 TensorFlow 2.0 的核心組件，用於構建高效、可擴展的數據輸入管道。它讓數據處理變得更加簡潔和高效。

---

## tf.data 基礎

### Dataset 創建

```python
import tensorflow as tf

# 從 numpy 陣列創建
x = tf.constant([[1, 2], [3, 4], [5, 6]])
y = tf.constant([0, 1, 0])

dataset = tf.data.Dataset.from_tensor_slices((x, y))

# 遍歷
for element in dataset:
    print(element)
```

### 基本操作

```python
# 批次化
dataset = dataset.batch(32)

# 亂序
dataset = dataset.shuffle(buffer_size=1000)

# 重複
dataset = dataset.repeat(5)

# 映射
dataset = dataset.map(lambda x, y: (x * 2, y))

# 過濾
def filter_fn(x, y):
    return tf.reduce_sum(x) > 5

dataset = dataset.filter(filter_fn)
```

---

## 完整訓練管道

### MNIST 示例

```python
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# 創建 Dataset
train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))

# 管道配置
train_dataset = (
    train_dataset
    .shuffle(10000)               # 亂序，buffer_size 越大越隨機
    .map(
        lambda x, y: (
            tf.cast(x, tf.float32) / 255.0,  # 正規化
            tf.cast(y, tf.int32)              # 類型轉換
        )
    )
    .batch(32)                    # 批次
    .prefetch(tf.data.AUTOTUNE)  # 預取
)
```

### 預取優化

```python
# AUTOTUNE 讓 TensorFlow 自動選擇 buffer 大小
train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)

# 手動指定
train_dataset = train_dataset.prefetch(2)
```

---

## 數據增強

### 圖像數據增強

```python
def augment_image(image, label):
    # 隨機翻轉
    image = tf.image.random_flip_left_right(image)

    # 隨機對比度
    image = tf.image.random_contrast(image, 0.9, 1.1)

    # 隨機亮度
    image = tf.image.random_brightness(image, 0.1)

    return image, label

train_dataset = train_dataset.map(augment_image)
```

### 使用 tf.image

```python
# 裁剪
image = tf.image.resize_with_crop_or_pad(image, 200, 200)

# 旋轉
image = tf.image.rot90(image, k=1)  # 旋轉 90 度

# 標準化
image = tf.image.per_image_standardization(image)
```

---

## 處理較大數據集

### 從檔案讀取

```python
# 讀取 TFRecord
dataset = tf.data.TFRecordDataset(['data.tfrecord'])

# 解析 TFRecord
def parse_tfrecord(example):
    feature_description = {
        'image': tf.io.FixedLenFeature([], tf.string),
        'label': tf.io.FixedLenFeature([], tf.int64),
    }
    example = tf.io.parse_single_example(example, feature_description)
    image = tf.io.decode_image(example['image'])
    label = example['label']
    return image, label

dataset = dataset.map(parse_tfrecord)
```

### CSV 數據

```python
# 讀取 CSV
dataset = tf.data.experimental.make_csv_dataset(
    'data.csv',
    batch_size=32,
    label_name='label',
    num_epochs=5
)
```

---

## 性能優化

### 優化策略

```
┌─────────────────────────────────────────────────────┐
│           tf.data 性能優化策略                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│   1. 預取 (prefetch)                                │
│      - 訓練和數據加載並行                            │
│      - 使用 prefetch(tf.data.AUTOTUNE)              │
│                                                     │
│   2. 平行映射 (parallel map)                        │
│      - 使用 num_parallel_calls                       │
│      - tf.data.AUTOTUNE 自動選擇                    │
│                                                     │
│   3. Interleave                                     │
│      - 處理多個來源文件                              │
│                                                     │
│   4. Cache                                                                │
│      - 將數據緩存到記憶體                            │
│      - 適用於 Epoch 間不變的數據                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 完整優化示例

```python
# 完整優化的管道
train_dataset = (
    tf.data.Dataset.from_tensor_slices((x_train, y_train))
    .cache()                                    # 緩存（如果記憶體允許）
    .shuffle(buffer_size=10000)
    .map(
        lambda x, y: (tf.cast(x, tf.float32) / 255.0, y),
        num_parallel_calls=tf.data.AUTOTUNE
    )
    .map(
        augment_image,
        num_parallel_calls=tf.data.AUTOTUNE
    )
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)
```

---

## 處理多個輸入

```python
# 多輸入示例
x1 = tf.constant([[1], [2], [3]])
x2 = tf.constant([[4], [5], [6]])
y = tf.constant([0, 1, 0])

dataset = tf.data.Dataset.from_tensor_slices((
    {'input1': x1, 'input2': x2},
    y
))

# 模型
input1 = tf.keras.Input(shape=(1,), name='input1')
input2 = tf.keras.Input(shape=(1,), name='input2')
merged = tf.keras.layers.Concatenate()([input1, input2])
output = tf.keras.layers.Dense(1)(merged)

model = tf.keras.Model([input1, input2], output)

# 訓練
model.fit(dataset, epochs=5)
```

---

## 結語

tf.data 提供了高效、靈活的數據輸入管道。掌握 tf.data 是深度學習工程師的重要技能，特別是處理大規模數據時。

---

**延伸閱讀**

- [tf.data documentation](https://www.google.com/search?q=tf.data+tutorial)
- [TensorFlow+data+pipeline](https://www.google.com/search?q=TensorFlow+data+pipeline+performance)
- [TFRecord+tutorial](https://www.google.com/search?q=TFRecord+tutorial+TensorFlow)

---

*本篇文章為「AI 程式人雜誌 2019 年 9 月號」TensorFlow 2.0 系列之五。*