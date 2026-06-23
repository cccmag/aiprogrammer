# TensorFlow Lite Micro 實戰

## 1. 什麼是 TFLite Micro

TensorFlow Lite Micro（TFLM）是 Google 專為微控制器設計的推論框架，可在僅數 KB 記憶體的 MCU 上運行機器學習模型。它支援 ARM Cortex-M、ESP32、Arduino 等常見嵌入式平臺。

## 2. 工作流程

TFLM 的工作流程與標準 TFLite 類似：先訓練模型，再轉換成 TFLite 格式，最後部署到 MCU。關鍵在於量化——將權重從 FP32 降到 INT8，可大幅減少模型體積。

```python
import tensorflow as tf

# 訓練一個簡單模型
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(4,)),
    tf.keras.layers.Dense(3, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy')

# 轉換為 TFLite，使用 INT8 量化
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.int8]
tflite_model = converter.convert()

with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

## 3. 在 MCU 上運行

TFLM 使用 C++ 撰寫，部署時需將模型轉為 C 陣列：

```python
# 將 TFLite 模型轉為 C 位元組陣列
import binascii

with open('model.tflite', 'rb') as f:
    data = f.read()
    hex_str = binascii.hexlify(data).decode()

# 輸出成 C 語言陣列格式
c_array = 'const unsigned char model_data[] = {\n'
for i in range(0, len(hex_str), 2):
    c_array += f'0x{hex_str[i:i+2]}, '
    if (i // 2 + 1) % 16 == 0:
        c_array += '\n'
c_array += '};\n'
c_array += f'const unsigned int model_data_len = {len(data)};\n'
print(c_array)
```

## 4. 實用工具

Google 提供的 `xxd` 工具可直接將二進位檔案轉為 C 陣列：`xxd -i model.tflite > model_data.cpp`。

## 5. 結語

TFLite Micro 讓人人手中的微控制器都能執行 AI 推論。更多資訊請參考 https://www.google.com/search?q=TensorFlow+Lite+Micro+tutorial
