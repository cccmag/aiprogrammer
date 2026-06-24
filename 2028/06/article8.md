# 邊緣裝置推論最佳化

## 邊緣推論的挑戰

邊緣裝置（手機、IoT、機器人）的運算資源極為有限：
- **記憶體**：數百 MB 而非數十 GB
- **運算力**：數 GFLOPS 而非數 TFLOPS
- **功耗**：數瓦而非數百瓦
- **頻寬**：邊緣網路延遲高，無法頻繁回傳雲端

## 模型輕量化技術

### 1. 動態量化（Dynamic Quantization）

PyTorch 提供的動態量化只量化權重，活化值仍用 FP32。幾乎零成本：

```python
import torch

class EdgeModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = torch.nn.Linear(512, 256)
        self.fc2 = torch.nn.Linear(256, 10)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))

model = EdgeModel()
quantized = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
# Memory: 4x reduction, speed: 2-3x
```

### 2. 結構化剪枝（Structured Pruning）

移除整個 channel 而非單一權重，可直接獲得實體加速：

```python
def channel_prune(weights, keep_ratio=0.5):
    """Prune channels by L2 norm"""
    norms = [sum(w**2 for w in ch) ** 0.5 for ch in zip(*weights)]
    threshold = sorted(norms, reverse=True)[int(len(norms) * keep_ratio)]
    return [
        [w for w, n in zip(row, norms) if n >= threshold]
        for row in weights
    ]
```

## 邊緣推論引擎

```python
class EdgeInferenceEngine:
    def __init__(self, model_path: str, backend: str = "TFLite"):
        self.backend = backend
        self.interpreter = None
        if backend == "TFLite":
            import tflite_runtime
            self.interpreter = tflite_runtime.Interpreter(model_path)
        elif backend == "ONNX":
            import onnxruntime
            self.interpreter = onnxruntime.InferenceSession(model_path)
        elif backend == "NCNN":
            print("NCNN backend ready — optimized for ARM CPUs")

    def infer(self, input_data):
        if self.backend == "TFLite":
            self.interpreter.allocate_tensors()
            input_details = self.interpreter.get_input_details()
            output_details = self.interpreter.get_output_details()
            self.interpreter.set_tensor(input_details[0]["index"], input_data)
            self.interpreter.invoke()
            return self.interpreter.get_tensor(output_details[0]["index"])
        return None
```

## 硬體加速 API

### Apple CoreML / ANE

```python
def optimize_for_apple_neural_engine(model_path: str):
    """Convert to CoreML with ANE optimization"""
    # import coremltools as ct
    # model = ct.models.MLModel(model_path)
    # model = ct.models.neural_network.quantization_utils.quantize_weights(model, nbits=8)
    # model.save("model_ane.mlpackage")
    pass
```

### Android NNAPI / QNN

```python
def optimize_for_android(model_path: str):
    """Delegation to NNAPI or Qualcomm Hexagon"""
    # On-device GPU/NPU delegation via NNAPI
    print("Android: NNAPI delegate enabled")
    print("Qualcomm: HTP (Hexagon Tensor Processor) detected")
```

## 工具生態

| 框架 | 支援平台 | 模型格式 |
|------|---------|---------|
| TensorFlow Lite | Android/iOS/Linux | TFLite |
| ONNX Runtime | 全平台 | ONNX |
| NCNN | ARM/x86 | NCNN param/bin |
| CoreML | Apple 全生態 | mlpackage |

## 延伸閱讀

- [TensorFlow Lite 量化](https://www.google.com/search?q=TensorFlow+Lite+quantization)
- [NCNN 邊緣部署](https://www.google.com/search?q=NCNN+edge+deployment)
- [Qualcomm AI Engine](https://www.google.com/search?q=Qualcomm+AI+Engine+inference)

邊緣推論的關鍵是組合拳：量化減小模型、結構化剪枝消除冗餘、以及選擇正確的硬體後端。在 1W 功耗內跑出可用的推論結果，才是真正的工程挑戰。
