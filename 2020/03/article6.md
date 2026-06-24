# TensorFlow Lite

## 模型轉換

### Keras 模型轉換

```python
import tensorflow as tf

# 建立模型
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dense(10, activation='softmax')
])

# 轉換
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

### SavedModel 轉換

```python
converter = tf.lite.TFLiteConverter.from_saved_model('saved_model_dir')
tflite_model = converter.convert()
```

## 量化（Quantization）

```python
# 訓練後量化
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# 量化到 float16
converter.target_spec.supported_types = [tf.float16]

# 動態範圍量化（不需要資料集）
converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
```

## 模型大小比較

| 格式 | 大小（MB） | 精度 |
|------|-----------|------|
| Keras (.h5) | 3.2 | 98.5% |
| TFLite (float) | 3.1 | 98.5% |
| TFLite (int8) | 0.8 | 98.1% |
| TFLite (float16) | 1.6 | 98.3% |

## Android 部署

```kotlin
// MainActivity.kt
val model = LiteModel.newInstance(this, "model.tflite")
val input = TensorBuffer.createFixedSize(intArrayOf(1, 784), DataType.FLOAT32)
input.loadBuffer(buffer)

val outputs = model.process(input)
val output = outputs.outputFeature0AsTensorBuffer
```

## iOS 部署

```swift
// ViewController.swift
let modelPath = Bundle.main.path(forResource: "model", ofType: "tflite")!
let interpreter = try Interpreter(modelPath: modelPath)

var inputBuffer = try interpreter.input(at: 0)
inputBuffer.copy(to: inputData)

try interpreter.invoke()
let outputBuffer = try interpreter.output(at: 0)
```

## 邊緣裝置推論

```python
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])
```

## 硬體加速

```python
# Android 上使用 GPU delegate
import tflite_runtime.interpreter as tflite

delegate = tflite.GpuDelegate()
interpreter = tflite.Interpreter(
    model_path='model.tflite',
    experimental_delegates=[delegate]
)
```

## 參考資源

- https://www.google.com/search?q=TensorFlow+Lite+conversion+tutorial+quantization+2020
- https://www.google.com/search?q=TensorFlow+Lite+Android+iOS+deployment+2020
- https://www.google.com/search?q=TFLite+model+size+optimization+performance+2020