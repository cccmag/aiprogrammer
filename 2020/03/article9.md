# 遷移與共存

## 為什麼需要遷移？

- 效能需求：某框架在特定場景有優勢
- 團隊技能：成員熟悉不同框架
- 專案階段：研究用 PyTorch，生產用 TensorFlow

## ONNX 中間格式

ONNX（Open Neural Network Exchange）是跨框架的模型格式：

```python
# PyTorch -> ONNX
import torch.onnx

model = MyModel()
model.eval()
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model, dummy_input, "model.onnx",
    input_names=['input'],
    output_names=['output'],
    opset_version=11
)
```

```python
# TensorFlow Lite 從 ONNX 轉換
# 需要先從 ONNX 轉到 TF，再從 TF 轉 TFLite
```

## 跨框架模型轉換工具

| 工具 | 功能 |
|------|------|
| MMdnn | Microsoft 維護的跨框架轉換工具 |
| tf2onnx | TensorFlow 到 ONNX |
| onnx-tensorflow | ONNX 到 TensorFlow |
| onnx2torch | ONNX 到 PyTorch |

## MMdnn 使用

```bash
pip install mmdnn
mmdownload -f pytorch -n resnet50
mmconvert -sf pytorch -in resnet50.pth -iw resnet50.json -df tensorflow -outmodel resnet50.pb
```

## 共存策略

### 同時使用多個框架

```python
# 在同一個 Python 腳本中使用多個框架
import torch
import tensorflow as tf

# PyTorch 訓練
pytorch_model = train_pytorch()

# 轉換為 TF 模型
torch.onnx.export(pytorch_model, dummy_input, "model.onnx")
# 使用 onnx-tensorflow 轉換
```

## 統一介面設計

```python
class UnifiedModel:
    def __init__(self, framework='pytorch'):
        self.framework = framework
        if framework == 'pytorch':
            self.model = load_pytorch_model()
        elif framework == 'tensorflow':
            self.model = load_tf_model()

    def predict(self, x):
        if self.framework == 'pytorch':
            return self.model(torch.tensor(x))
        else:
            return self.model(x)
```

## 資料流程一致化

```python
def preprocess_pytorch(image):
    # PyTorch 格式
    return image.resize((224, 224)).transpose(2, 0, 1) / 255.0

def preprocess_tensorflow(image):
    # TF 格式
    image = tf.image.resize(image, (224, 224))
    image = image / 255.0
    return image
```

## 迁移建議

1. **不要過早優化**：先用順手的框架
2. **保持介面一致**：方便日後替換
3. **版本控制**：記錄每個框架的版本
4. **測試覆蓋**：確保遷移後行為一致

## 參考資源

- https://www.google.com/search?q=ONNX+model+conversion+TensorFlow+PyTorch+2020
- https://www.google.com/search?q=MMdnn+model+migration+cross+framework+2020
- https://www.google.com/search?q=TensorFlow+PyTorch+coexistence+hybrid+2020