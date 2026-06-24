# 7. 生態系與部署

## TensorFlow 生態系

### TensorFlow Extended (TFX)

端到端的機器學習平台：

```python
# TFX 元件
import tfx
from tfx.components import (
    CsvExampleGen,
    StatisticsGen,
    SchemaGen,
    ExampleValidator,
    Trainer,
    Evaluator,
    Pusher
)
```

### TensorFlow Lite

用於行動與邊緣裝置：

```bash
# 轉換模型
tflite_convert \
  --model_file=model.pb \
  --output_file=model.tflite \
  --input_format=TENSORFLOW_GRAPH_DEF \
  --output_format=TFLITE_GRAPH_DEF \
  --input_shape=1,784
```

### TensorFlow.js

瀏覽器端推論：

```javascript
import * as tf from '@tensorflow/tfjs';

// 載入模型
const model = await tf.loadLayersModel('https://.../model.json');

// 推論
const input = tf.tensor2d([[1,2,3,...]]);
model.predict(input);
```

## PyTorch 生態系

### TorchServe

模型服務框架（2020 年初推出）：

```bash
# 安裝
pip install torchserve

# 部署模型
torchserve --start --model-name my_model --model-dir ./model
```

### PyTorch Mobile

行動端部署：

```bash
# Android
pip install torch==1.5.0 torchvision==0.6.0

# iOS (Swift API)
# 需要 PyTorch iOS library
```

### ONNX 支援

```python
# 匯出到 ONNX
torch.onnx.export(
    model, dummy_input,
    "model.onnx",
    input_names=['input'],
    output_names=['output']
)
```

## JAX / Flax 生態系

### Flax

神經網路庫：

```python
import flax.nn as nn

class MLP(nn.Module):
    def apply(self, x, hidden_sizes=[128, 64], num_classes=10):
        for size in hidden_sizes:
            x = nn.Dense(x, size)
            x = nn.relu(x)
        x = nn.Dense(x, num_classes)
        return nn.softmax(x)
```

### Haiku

另一個 JAX 的 neural network 庫：

```python
import haiku as hk

def forward(x):
    mlp = hk.Sequential([
        hk.Linear(128), jax.nn.relu,
        hk.Linear(10)
    ])
    return mlp(x)

forward = hk.transform(forward)
```

## 模型轉換

```python
# ONNX：中間格式
# 可在 TF、PyTorch、MXNet 之間轉換
```

## 部署選項

| 平台 | TensorFlow | PyTorch | JAX |
|------|------------|---------|-----|
| Server | TF Serving | TorchServe | 需要轉換 |
| Mobile | TF Lite | PyTorch Mobile | 需要轉換 |
| Browser | TF.js | ONNX.js | 需要轉換 |
| Edge | TF Lite | PyTorch Mobile | 需要轉換 |

## 雲端部署

### TensorFlow on GCP

```python
from google.cloud import aiplatform

aiplatform.init(project='my-project')
endpoint = aiplatform.deploy_model(
    model_display_name='my-model',
    serving_container_image_uri='gcr.io/...'
)
```

## 參考資源

- https://www.google.com/search?q=TensorFlow+TFX+TFLite+TF+js+ecosystem+2020
- https://www.google.com/search?q=PyTorch+TorchServe+Mobile+ONNX+2020
- https://www.google.com/search?q=JAX+Flax+Haiku+neural+network+library+2020