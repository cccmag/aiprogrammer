# TensorFlow 2.0 正式發布：深度學習新時代

## 前言

2019 年 9 月，Google 正式發布 TensorFlow 2.0，這是 TensorFlow 歷史上最重要的版本更新。

## 核心變化

### 1. Eager Execution 默認

```python
# TensorFlow 2.0 的預設行為
import tensorflow as tf

result = tf.constant([1, 2, 3]) + tf.constant([4, 5, 6])
print(result.numpy())  # [5, 7, 9]
```

### 2. tf.keras 統一

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

### 3. API 清理

```python
# 移除 tf.app, tf.flags -> 使用 absl-py
# 移除 tf.contrib -> 重構或移除
```

---

## 遷移

### 從 TF1 遷移

```python
import tensorflow.compat.v1 as tf1

# 使用舊版 API
with tf1.Session() as sess:
    result = sess.run(tf1.constant(1) + tf1.constant(2))
```

---

## 結語

TensorFlow 2.0 的發布標誌著深度學習框架進入了一個更易用、更高效的新時代。

---

**延伸閱讀**

- [TensorFlow 2.0 Official](https://www.google.com/search?q=TensorFlow+2.0+official+release+September+2019)
- [TensorFlow+2.0+migration](https://www.google.com/search?q=TensorFlow+2.0+migration+guide)