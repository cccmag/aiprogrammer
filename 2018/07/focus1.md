# TensorFlow 發展史與生態系（2015-2018）

## 從 Google Brain 到開源框架

### 前言

TensorFlow 在 2015 年 11 月開源後，迅速成為深度學習領域最具影響力的框架。本篇文章回顧其發展歷程與生態系演進。

### 2015-2016：誕生與早期採用

TensorFlow 前身是 Google Brain 內部的 DistBelief 系統。2015 年開源時，主要特點包括：

- **計算圖模型**：先定義後執行的靜態圖
- **自動微分**：自動計算梯度
- **跨平台支援**：CPU、GPU、行動裝置

```python
import tensorflow as tf

# 2016 年的經典寫法
x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)
z = tf.multiply(x, y)

with tf.Session() as sess:
    result = sess.run(z, feed_dict={x: 3.0, y: 4.0})
    print(result)  # 12.0
```

### 2017：Keras 崛起與 API 標準化

2017 年，Keras（由 François Chollet 開發）成為 TensorFlow 官方支援的高階 API。開發者社群出現明顯分化：

```python
# Keras 簡化後的寫法
from tensorflow import keras
model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy')
```

### 2018：1.10 版的里程碑

2018 年 7 月的 TensorFlow 1.10 版將 Keras 整合進核心：

```python
# TensorFlow 1.10+ 的標準寫法
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation='softmax')
])
```

### 生態系組件

| 組件 | 用途 | 發布年份 |
|------|------|----------|
| TensorBoard | 視覺化訓練過程 | 2016 |
| TensorFlow Serving | 模型部署服務 | 2017 |
| TensorFlow Lite | 行動裝置部署 | 2017 |
| TF-Hub | 預訓練模型庫 | 2018 |
| TFRecord | 資料格式 | 2016 |

### 小結

TensorFlow 從內部工具演進為開源生態系，API 設計從底層導向逐漸走向易用性。Keras 的整合是必然趨勢，反映了框架設計者對使用者體驗的重視。

---

**下一步**：[Keras：高階 API 的崛起](focus2.md)

## 延伸閱讀

- [TensorFlow Official Website](https://www.google.com/search?q=TensorFlow+official+tutorial+2018)
- [Keras Documentation](https://www.google.com/search?q=Keras+documentation+2018)
- [Google Brain DistBelief History](https://www.google.com/search?q=DistBelief+Google+Brain+history)