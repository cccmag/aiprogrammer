# 深度學習硬體支援：GPU、TPU 與效能優化

## 前言

深度學習的快速發展離不開硬體的進步。GPU 的並行計算能力大幅加速了神經網路的訓練，TPU 等專用硬體則代表了未來的方向。本篇文章介紹深度學習的硬體支援和效能優化技巧。

## GPU 加速

### 為什麼深度學習需要 GPU？

傳統 CPU 適合序列計算，而深度學習需要大量的並行矩陣運算：

```
CPU：少量強大核心，擅長複雜邏輯
GPU：數千個小型核心，擅長並行計算

矩陣乘法：1x4M 次乘法
- CPU：順序執行，需要數十億個時鐘週期
- GPU：並行執行，數千核心同時工作
```

### NVIDIA CUDA 和 cuDNN

```bash
# CUDA：NVIDIA 的並行計算平台
# cuDNN：優化過的深度學習原語

# 安裝
pip install tensorflow-gpu  # TensorFlow GPU 版本
```

### 使用 GPU

```python
import tensorflow as tf

# 檢查 GPU 是否可用
print(tf.test.is_gpu_available())

# 指定設備
with tf.device('/gpu:0'):
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    b = tf.constant([[5.0, 6.0], [7.0, 8.0]])
    c = tf.matmul(a, b)

# 或者使用 with tf.device 動態指定
```

### PyTorch 中的 GPU 使用

```python
import torch

# 檢查 GPU
print(torch.cuda.is_available())
print(torch.cuda.device_count())

# 移動到 GPU
device = torch.device('cuda')
model = model.to(device)
x = x.to(device)

# 或使用 DataParallel
model = torch.nn.DataParallel(model)
```

## TPU：張量處理單元

### TPU 簡介

Google 開發的 TPU（Tensor Processing Unit）是專為深度學習設計的 ASIC：

```
2016 年：TPU 首次公佈，用於 AlphaGo
2017 年：TPU 2.0，提供雲端服務
```

### TPU 與 GPU 的比較

| 特性 | GPU | TPU |
|------|-----|-----|
| 開發商 | NVIDIA | Google |
| 靈活性 | 高 | 中 |
| 效能 | 高 | 極高 |
| 可用性 | 廣泛 | 雲端專用 |
| 功耗效率 | 中 | 高 |

### 使用 TPU

```python
import tensorflow as tf

# TensorFlow 1.x 使用 TPU
resolver = tf.contrib.cluster_resolver.TPUClusterResolver(tpu='grpc://' + os.environ['COLAB_TPU_ADDR'])
tf.contrib.tpu.configureDistributedTPU(cluster=resolver)

# 定義 TPU 模型
def model_fn(features, labels, mode):
    # 模型定義
    return tf.contrib.tpu.TPUEstimatorSpec(mode=mode, predictions=predictions)

# 訓練
estimator = tf.contrib.tpu.TPUEstimator(model_fn=model_fn, config=run_config)
estimator.train(input_fn=train_input_fn, steps=1000)
```

## 效能優化技巧

### 資料傳輸優化

```python
# 使用 prefetch 重疊資料傳輸和計算
import tensorflow as tf

dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
dataset = dataset.cache().shuffle(10000).batch(32).prefetch(tf.data.experimental.AUTOTUNE)
```

### 記憶體優化

```python
# TensorFlow 配置
config = tf.ConfigProto()
config.gpu_options.allow_growth = True  # 漸進分配記憶體
config.gpu_options.per_process_gpu_memory_fraction = 0.8  # 限制使用量
sess = tf.Session(config=config)
```

### 模型優化

```python
# 混合精度訓練（TensorFlow 1.x）
# 使用 float16 而非 float32 加速

from tensorflow.contrib.mixed_precision import create_loss_scale_manager, LossScaleOptimizer

loss_scale_manager = create_loss_scale_manager(128.0, 1024.0)
optimizer = LossScaleOptimizer(optimizer, loss_scale_manager)
```

### 批量正規化

```python
# 批量正規化加速訓練
from tensorflow.keras.layers import BatchNormalization

model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
```

## 分散式訓練

### TensorFlow 分散式訓練

```python
# TensorFlow 分散式策略
strategy = tf.contrib.distribute.MirroredStrategy()
with strategy.scope():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
```

### PyTorch 分散式訓練

```python
import torch.nn as nn
import torch.distributed as dist

# 資料平行
model = nn.DataParallel(model)  # 多 GPU

# 或者使用 DistributedDataParallel
```

## 硬體選擇建議

### 訓練 vs 推論

| 場景 | 推薦硬體 | 原因 |
|------|---------|------|
| 研究/實驗 | 單 GPU (GTX 1080) | 成本效益高 |
| 中等規模訓練 | 4-8 GPU | 平衡效能和成本 |
| 大規模訓練 | 多機多 GPU 或 TPU | 極致效能 |
| 邊緣部署 | NVIDIA Jetson | 低功耗 |
| 生產推論 | CPU 或專用晶片 | 成本和延遲 |

### 記憶體與計算平衡

```
深度學習瓶頸：
1. 記憶體頻寬
2. 計算吞吐量
3. 資料傳輸延遲

優化方向：
1. 減少模型大小
2. 提高計算效率
3. 優化資料流
```

## 結語

硬體是深度學習發展的重要支柱。從消費級 GPU 到資料中心 GPU，再到 TPU 等專用硬體，硬體的進步推動了深度學習的快速發展。

選擇合適的硬體和優化策略，可以顯著提升深度學習的訓練和推論效率。隨著硬體技術的持續進步，我們可以期待更多強大且高效的深度學習應用。

---

## 延伸閱讀

- [NVIDIA+GPU+深度學習](https://www.google.com/search?q=NVIDIA+GPU+deep+learning+performance)
- [Google+TPU+介紹](https://www.google.com/search?q=Google+TPU+Tensor+Processing+Unit)
- [深度學習+效能優化](https://www.google.com/search?q=deep+learning+performance+optimization+tips)
- [CUDA+cuDNN+安裝](https://www.google.com/search?q=CUDA+cuDNN+TensorFlow+installation)

---

*本篇文章為「AI 程式人雜誌 2017 年 2 月號」焦點系列之一。*