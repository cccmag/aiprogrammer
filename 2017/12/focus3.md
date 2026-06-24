# 硬體加速與 GPU 運算：NVIDIA Volta, TPU

## 前言

深度學習的成功離不開硬體的進步。2017 年，NVIDIA Volta、Google TPU 等硬體創新大幅提升了 AI 運算能力。

## NVIDIA Tesla V100

### Volta 架構創新

2017 年 5 月發布的 Tesla V100 是當時最快的深度學習加速器：

```
┌─────────────────────────────────────────────────────────┐
│              Tesla V100 規格                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  GPU 架構              : Volta                          │
│  CUDA 核心             : 5120                           │
│  Tensor 核心           : 640                            │
│  記憶體                : 16/32 GB HBM2                   │
│  記憶體頻寬            : 900 GB/s                       │
│  深度學習效能          : 120 TFLOPS (Tensor Core)       │
│  雙精度效能            : 7.5 TFLOPS                     │
│  單精度效能            : 15 TFLOPS                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Tensor Core 原理

```python
# Tensor Core 執行 4x4 矩陣乘法累加
# 每個 Tensor Core 每時鐘週期執行 64 個 FMA 操作

# 混合精度訓練
import torch

# V100 的 Tensor Core 自動加速 FP16
model = model.cuda()
optimizer = torch.optim.Adam(model.parameters())

# 前向傳播：FP16 輸入輸出
# 權重：FP16
# 計算：Tensor Core 加速

# 反向傳播：自動處理
```

### V100 對訓練的影響

```
效能提升對比：
訓練時間 (ImageNet, ResNet-50)

M40 (2016):     14.2 天
P100 (2016):    7.1 天
V100 (2017):    1.8 天

加速比：8x 相對於 M40
```

## Google TPU

### TPU v2 (2017)

Google 在 2017 年發布了第二代 TPU：

```python
# TPU 使用說明（TensorFlow API）
import tensorflow as tf

# 指定 TPU 執行
resolver = tf.distribute.TPUClusterResolver(
    tpu='gs://my-project/tpus'
)
tf.config.experimental_connect_to_cluster(resolver)

# 策略
strategy = tf.distribute.experimental.TPUStrategy(resolver)

# 訓練
with strategy.scope():
    model = tf.keras.applications.ResNet50()
    model.compile(optimizer='adam', loss='categorical_crossentropy')

# TPU 優化
# - 脈動陣列 (Systolic Array)
# - 專用矩陣乘法單元
# - 高頻寬記憶體
```

### TPU 特性

| 特性 | TPU v1 | TPU v2 |
|------|--------|--------|
| 發布年份 | 2016 | 2017 |
| 峰值效能 | 92 TFLOPS | 180 TFLOPS |
| 記憶體 | 8 GB | 64 GB |
| 記憶體頻寬 | 34 GB/s | 700 GB/s |

## Edge AI 硬體

### Apple Core ML

Core ML 於 2017 年 6 月發布，讓 AI 推論進入行動裝置：

```swift
// Swift Core ML 使用示例
import CoreML

let model = try MLModel(contentsOf: modelURL)

let input = try MLDictionaryFeatureProvider(dictionary: ["image": pixelBuffer])

let prediction = try model.prediction(from: input)
```

### Qualcomm Snapdragon NPE

高通的神經網路處理引擎（NPE）為行動裝置提供 AI 加速。

## GPU 程式設計基礎

```python
import torch

# 檢查 GPU
print(torch.cuda.is_available())  # True
print(torch.cuda.get_device_name(0))  # Tesla V100-SXM2-16GB

# 移動到 GPU
model = model.cuda()
x = x.cuda()

# 混合精度
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for data, target in dataloader:
    with autocast():
        output = model(data)
        loss = criterion(output, target)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## 硬體選擇指南

```
┌─────────────────────────────────────────────────────────┐
│              AI 硬體選擇指南                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  雲端訓練:                                             │
│  - NVIDIA V100 (最佳效能)                               │
│  - Google TPU (TensorFlow 專家)                         │
│  - AWS P3 (彈性)                                        │
│                                                         │
│  研究/實驗:                                             │
│  - RTX 3090 (性價比)                                    │
│  - Tesla V100 (記憶體大)                               │
│                                                         │
│  邊緣部署:                                             │
│  - NVIDIA Jetson (邊緣 AI)                              │
│  - Apple Neural Engine (iOS)                            │
│  - Qualcomm NPE (Android)                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 2017 年硬體發展總結

```
重要發布：
- NVIDIA Volta V100 (5月)
- Intel Nervana Neural Network Processor (測試階段)
- Google TPU v2 (5月)
- Apple Core ML (6月)
- Qualcomm Snapdragon 845 (12月)
```

## 對 AI 發展的影響

硬體進步帶來的影響：

1. **訓練時間大幅縮短**：從數週到數天
2. **模型規模擴大**：更大的模型成為可能
3. **邊緣 AI 普及**：推論從雲端走向終端
4. **成本降低**：摩爾定律持續生效

---

**延伸閱讀**

- [NVIDIA Volta](https://www.google.com/search?q=NVIDIA+Volta+V100)
- [Google TPU](https://www.google.com/search?q=Google+TPU+v2+2017)
- [Deep Learning Hardware](https://www.google.com/search?q=deep+learning+hardware+GPU+TPU)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*