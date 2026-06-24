# TFHub 遷移學習模組庫

## 預訓練模型的共享平台

### TFHub 是什麼？

TFHub 是 Google 推出的預訓練模型分享平台，讓開發者能輕鬆下載和使用預訓練模型進行遷移學習。

官方網址：https://tfhub.dev

### 核心概念

- **Module**：可重用的模型組件
- **Handle**：模組的 URL 或路徑
- **Signature**：統一的輸入輸出介面

### 基本用法

```python
import tensorflow as tf
import tensorflow_hub as hub

# 載入文字嵌入模組
module_url = "https://tfhub.dev/google/nnlm-en-dim128/1"
embed = hub.Module(module_url)

# 使用
embeddings = embed(["Hello world", "TensorFlow Hub"])
```

### 影像分類模型

```python
# 載入 MobileNet
module_url = "https://tfhub.dev/google/imagenet/mobilenet_v1_224/feature_vector/4"

# 方法一：Keras
model = tf.keras.Sequential([
    hub.KerasLayer(module_url, input_shape=(224, 224, 3)),
    tf.keras.layers.Dense(10, activation='softmax')
])

# 方法二：Estimator
def model_fn(features, labels, mode):
    net = hub.KerasLayer(module_url)(features)
    logits = tf.layers.dense(net, 10)
    return tf.estimator.EstimatorSpec(mode, logits=logits)

# 方法三：Eager Mode
model = hub.KerasLayer(module_url, input_shape=(224, 224, 3))
features = model(image_batch)
```

### 文字分類範例

```python
# 完整文字分類流程
import tensorflow as tf
import tensorflow_hub as hub

# 資料處理
train_input_fn = tf.estimator.inputs.pandas_input_fn(
    x=train_df[['sentence']],
    y=train_df['label'],
    batch_size=32,
    num_epochs=5,
    shuffle=True
)

# 特徵欄位
text_feature_column = hub.text_embedding_column(
    "sentence",
    "https://tfhub.dev/google/nnlm-en-dim128/1"
)

# 建立 Estimator
estimator = tf.estimator.DNNClassifier(
    hidden_units=[128, 64],
    feature_columns=[text_feature_column],
    n_classes=2
)

# 訓練
estimator.train(input_fn=train_input_fn)
```

### 常用模組

| 模組類型 | 名稱 | 用途 |
|----------|------|------|
| 文字 | nnlm-en-dim128 | 文字嵌入 |
| 文字 | universal-sentence-encoder | 句子嵌入 |
| 影像 | mobilenet_v1_224 | 影像特徵 |
| 影像 | inception_v3 | 影像分類 |
| 影像 | resnet_v1_50 | 影像特徵 |

### 模組版本管理

```python
# 指定版本
module_url = "https://tfhub.dev/google/imagenet/mobilenet_v1_224/feature_vector/1"

# 未指定版本（自動使用最新版）
module_url = "https://tfhub.dev/google/imagenet/mobilenet_v1_224/feature_vector"
```

### 離線使用

```python
# 下載模組到本地
import os
os.environ["TFHUB_CACHE_DIR"] = "./hub_cache"

# 首次執行時會快取到本地
module = hub.KerasLayer(module_url)
```

### 小結

TFHub 大幅簡化了遷移學習的流程，讓沒有大量計算資源的開發者也能使用高質量預訓練模型。

---

**下一步**：[程式實作：Keras 模型建構實務](focus_code.md)

## 延伸閱讀

- [TFHub Official Site](https://www.google.com/search?q=TFHub+tensorflow+hub+tutorial)
- [Transfer Learning Guide](https://www.google.com/search?q=transfer+learning+tensorflow+hub+2018)