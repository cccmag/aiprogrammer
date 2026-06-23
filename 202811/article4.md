# ESP32 與 Arduino AI

## 1. 為什麼是 ESP32

ESP32 是樂鑫科技推出的 Wi-Fi/BLE 微控制器，售價不到 3 美元，卻擁有雙核心 240MHz 處理器、520KB SRAM 和 4MB Flash，足以執行輕量級 AI 模型。

## 2. 使用 EloquentTinyML

EloquentTinyML 是專為 Arduino 生態系設計的 TFLite Micro 包裝庫：

```python
# 訓練模型（Python 端）
import tensorflow as tf
import numpy as np

# 模擬感測器資料：溫度、濕度 -> 是否需要開啟空調
X = np.random.randn(1000, 2)
y = (X[:, 0] > 0.5) & (X[:, 1] < 0.3)
y = y.astype(np.float32)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(8, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy')
model.fit(X, y, epochs=20, verbose=0)

# 轉換並量化
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open('esp_model.tflite', 'wb') as f:
    f.write(tflite_model)
print(f'模型大小: {len(tflite_model)} bytes')
```

## 3. 類比 Arduino 程式碼

以下是在 ESP32 上的推論流程（類比 C++ 結構）：

```python
# Python 模擬 ESP32 推論
import numpy as np
import tensorflow.lite as tflite

# 載入模型
interpreter = tflite.Interpreter(model_path='esp_model.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def esp32_inference(temperature, humidity):
    # 模擬感測器讀數
    input_data = np.array([[temperature, humidity]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    result = interpreter.get_tensor(output_details[0]['index'])
    return result[0][0] > 0.5

print(f'空調開啟: {esp32_inference(0.7, 0.2)}')
print(f'空調關閉: {esp32_inference(0.3, 0.5)}')
```

## 4. 省電技巧

ESP32 支援深度睡眠（Deep Sleep），推論完成後可立即休眠，待感測器中斷喚醒，使電池續航達數月之久。

## 5. 結語

ESP32 結合 TFLite Micro，讓 AI 走入低成本的 IoT 裝置。更多資訊請參考 https://www.google.com/search?q=ESP32+TinyML+tutorial
