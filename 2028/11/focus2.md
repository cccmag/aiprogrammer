# TinyML 與 MCU 推論（2019-2028）

## 什麼是 TinyML？

TinyML 是指在微控制器（MCU）上執行機器學習推論的技術，功耗通常低於毫瓦等級。相較於手機或樹莓派，MCU 僅有 KB 級記憶體與 MHz 級時脈，對模型極度輕量化的需求催生了 TinyML 生態系。

## 關鍵里程碑

- **2019** — TensorFlow Lite Micro 發布，可在 ARM Cortex-M 系列上執行（[Google 搜尋](https://www.google.com/search?q=TensorFlow+Lite+Micro+2019+ARM+Cortex+M)）。
- **2020** — 第一屆 TinyML 高峰會舉行，Google、ARM、Qualcomm 等大廠參與。
- **2021** — CMSIS-NN 函式庫成熟，ARM Cortex-M 上卷積運算加速達 4.6 倍。
- **2022** — Arduino Nicla Voice 問世，搭載 Syntiant 神經加速器。
- **2023** — Edge Impulse 平台使用者突破 10 萬，支援自動模型最佳化。
- **2024** — 業界首款通用 TinyML SoC — Alif Semiconductor Ensemble — 量產。
- **2025** — 微型 Transformer 架構（MobileBERT-Tiny、TinyGPT）開始在 MCU 上運行。
- **2026** — Arm Ethos-U85 整合至主流 MCU，NPU 成為 Cortex-M 標準配備。
- **2027** — 感測器融合 TinyML 在工業預測維護中大規模部署。
- **2028** — TinyML 規範標準化（MLCommons 推出 TinyML Benchmark v2）。

## 技術挑戰

TinyML 的核心限制在於記憶體。典型的 MCU 僅有 256 KB SRAM 與 2 MB Flash，因此必須使用 INT8 量化（甚至二值化神經網路）。模型蒸餾與剪枝也是必備技術。

## 程式碼範例

以下為 TensorFlow Lite Micro 推論範例，使用 Python 訓練後轉換為 TFLite 模型：

```python
import tensorflow as tf

# 訓練一個簡單的模型
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(10,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy')

# 轉換為 TFLite 並進行 INT8 量化
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.int8]
tflite_model = converter.convert()

with open('model_quantized.tflite', 'wb') as f:
    f.write(tflite_model)
print(f"Quantized model size: {len(tflite_model)} bytes")
```

## 參考資源

- [Google 搜尋：TinyML getting started](https://www.google.com/search?q=TinyML+TensorFlow+Lite+Micro+tutorial)
- [Google 搜尋：MCU machine learning 2025](https://www.google.com/search?q=MCU+machine+learning+inference+benchmark)
