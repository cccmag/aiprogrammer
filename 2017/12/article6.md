# 深度學習硬體：GPU 與 TPU

## 前言

硬體是深度學習成功的基礎。2017 年 NVIDIA Volta 和 Google TPU v2 的發布將 AI 運算能力推向新高度。

## NVIDIA Volta (V100)

```python
# Tesla V100 規格

specs = {
    "Architecture": "Volta",
    "CUDA Cores": 5120,
    "Tensor Cores": 640,
    "Memory": "16/32 GB HBM2",
    "Memory Bandwidth": "900 GB/s",
    "Deep Learning Performance": "120 TFLOPS (Tensor Core)",
    "Single Precision": "15 TFLOPS",
    "Double Precision": "7.5 TFLOPS"
}

# Tensor Core 使用
import torch
from torch.cuda.amp import autocast, GradScaler

model = model.cuda()
scaler = GradScaler()

for data, target in dataloader:
    with autocast():
        output = model(data)
        loss = criterion(output, target)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## Google TPU v2

```python
# TPU v2 規格

tpu_specs = {
    "Peak Performance": "180 TFLOPS",
    "Memory": "64 GB HBM",
    "Memory Bandwidth": "700 GB/s",
    "Cores": "2 (Cloud TPU v2)"
}

# TensorFlow 使用 TPU
import tensorflow as tf

resolver = tf.distribute.TPUClusterResolver(tpu='gs://my-project/tpus')
tf.config.experimental_connect_to_cluster(resolver)

strategy = tf.distribute.experimental.TPUStrategy(resolver)

with strategy.scope():
    model = tf.keras.applications.ResNet50()
    model.compile(optimizer='adam', loss='categorical_crossentropy')
```

## Edge AI 硬體

```python
# 2017 年 Edge AI 硬體

edge_devices = {
    "Apple Core ML": {
        "platform": "iOS 11+",
        "framework": "Core ML",
        "capability": "影像、NLP、聲音"
    },

    "Qualcomm Snapdragon 845": {
        "platform": "Android",
        "neural_engine": "Hexagon 685",
        "capability": "AI 推論加速"
    },

    "NVIDIA Jetson TX2": {
        "platform": "Embedded",
        "gpu": "Pascal (256 cores)",
        "capability": "邊緣 AI、機器人"
    }
}
```

## 硬體比較

| 硬體 | 供應商 | 峰值效能 | 功耗 | 適用場景 |
|------|--------|----------|------|----------|
| V100 | NVIDIA | 120 TFLOPS | 300W | 雲端訓練 |
| P100 | NVIDIA | 21 TFLOPS | 250W | 雲端訓練 |
| TPU v2 | Google | 180 TFLOPS | 280W | GCP 訓練 |
| TX2 | NVIDIA | 1.5 TFLOPS | 7.5W | Edge |
| Snapdragon 845 | Qualcomm | - | 2W | Mobile |

## 對 AI 發展的影響

```
┌─────────────────────────────────────────────────────────┐
│              硬體進步對 AI 的影響                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  訓練時間縮短:                                         │
│  - ImageNet 訓練: 14天 → 1.8天 (V100)                  │
│                                                         │
│  模型規模擴大:                                         │
│  - 更大的 batch size                                    │
│  - 更大的模型                                           │
│                                                         │
│  邊緣部署:                                             │
│  - 模型壓縮技術                                        │
│  - 延遲降低                                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

**延伸閱讀**

- [NVIDIA Volta](https://www.google.com/search?q=NVIDIA+Volta+V100)
- [Google TPU](https://www.google.com/search?q=Google+TPU+v2)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*