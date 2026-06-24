# PyTorch 轉 ONNX 部署

## 什麼是 ONNX？

ONNX（Open Neural Network Exchange）是一個開放的神經網路交換格式，由微軟和 Facebook 共同開發。它讓模型可以在不同框架之間遷移：用 PyTorch 訓練，用 ONNX Runtime 或 TensorRT 部署。

## PyTorch 匯出 ONNX

PyTorch 的 `torch.onnx.export` 可以將模型轉換為 ONNX 格式：

```python
import torch.onnx

model = MyModel()
model.eval()

dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model,
    dummy_input,
    'model.onnx',
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={
        'input': {0: 'batch_size'},
        'output': {0: 'batch_size'},
    },
    opset_version=12,
)
```

## 關鍵參數說明

- **dynamic_axes**：指定可變維度，讓模型可以接受不同 batch size 的輸入
- **opset_version**：ONNX 算子集版本，越高支援越多運算
- **do_constant_folding**：是否進行常數折疊最佳化

## 使用 ONNX Runtime 推理

ONNX Runtime 是微軟推出的跨平台推理引擎：

```python
import onnxruntime as ort

session = ort.InferenceSession('model.onnx')
inputs = {session.get_inputs()[0].name: numpy_array}
outputs = session.run(None, inputs)
```

支援 GPU 加速：
```python
session = ort.InferenceSession('model.onnx',
    providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
```

## 常見問題與解決方案

### 不支援的運算
某些 PyTorch 運算沒有對應的 ONNX 算子。解決方案：
1. 使用 `torch.onnx.symbolic.register_op` 註冊自訂映射
2. 修改模型架構以避開不支援的運算

### 動態控制流
含有 `if` 或 `for` 的模型需要透過 TorchScript 轉換：

```python
scripted = torch.jit.script(model)
torch.onnx.export(scripted, dummy_input, 'model.onnx')
```

## 部署方案比較

| 方案 | 優點 | 缺點 |
|------|------|------|
| ONNX Runtime | 跨平台、高效 | 算子支援有限 |
| TensorRT | NVIDIA GPU 極致效能 | 僅限 NVIDIA |
| TorchScript | 完整 PyTorch 支援 | 依賴 LibTorch |
| OpenVINO | Intel 平台最佳化 | 僅限 Intel |

## 參考資料

- ONNX 官方網站：https://onnx.ai/
- ONNX Runtime 文件：https://onnxruntime.ai/docs/
- PyTorch ONNX 匯出教學：https://pytorch.org/docs/stable/onnx.html
- TensorRT 文件：https://developer.nvidia.com/tensorrt
