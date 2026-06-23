# CoreML 與 Apple Silicon

## 1. CoreML 簡介

CoreML 是 Apple 的行動端機器學習框架，深度整合 A 系列與 M 系列晶片的神經網路引擎（Neural Engine）。從 iPhone X 的 A11 開始，Apple 就在晶片中加入了專用的 NPU 區塊。

## 2. 轉換模型

使用 `coremltools` 將訓練好的模型轉成 `.mlpackage` 格式：

```python
import coremltools as ct
import tensorflow as tf

# 載入 TensorFlow 模型
model = tf.keras.models.load_model('my_model.h5')

# 轉換為 CoreML
mlmodel = ct.convert(
    model,
    inputs=[ct.TensorType(shape=(1, 224, 224, 3))],
    compute_precision=ct.precision.FLOAT16,
    minimum_deployment_target=ct.target.iOS18
)

# 儲存
mlmodel.save('MyModel.mlpackage')
print('CoreML 模型轉換完成')
```

## 3. 執行推論

CoreML 在 Apple Silicon 上會自動利用 Neural Engine、GPU 和 CPU 進行最佳化排程：

```python
import coremltools as ct
from PIL import Image
import numpy as np

# 載入 CoreML 模型
model = ct.models.MLModel('MyModel.mlpackage')

# 預處理影像
img = Image.open('cat.jpg').resize((224, 224))
img_array = np.array(img).astype(np.float32) / 255.0
img_batch = np.expand_dims(img_array, axis=0)

# 推論
result = model.predict({'input_1': img_batch})
pred_class = np.argmax(result['Identity'])
print(f'預測類別: {pred_class}')
```

## 4. 效能對比

Apple Silicon 的 Neural Engine 可在極低功耗下達到驚人的推論速度。以 ResNet50 為例，M4 晶片的 Neural Engine 推論延遲約 5ms，比純 CPU 快 20 倍以上。

## 5. 結語

CoreML 結合 Apple Silicon 的硬體加速，是行動裝置 AI 的標竿方案。更多資訊請參考 https://www.google.com/search?q=CoreML+Apple+Neural+Engine+tutorial
