# 生產部署：ONNX 與 TorchScript

## 1. ONNX 匯出

### 為什麼要 ONNX？

ONNX（Open Neural Network Exchange）是一種開放式模型交換格式，可以在不同框架之間轉換。

```python
import torch.onnx

# 匯出為 ONNX
model = MyModel()
model.eval()

dummy_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model,
    dummy_input,
    'model.onnx',
    export_params=True,
    opset_version=10,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output']
)
```

### 驗證 ONNX 模型

```python
import onnx

# 載入並驗證
model_onnx = onnx.load('model.onnx')
onnx.checker.check_model(model_onnx)

# 比較輸出
import numpy as np

torch_output = model(torch.randn(1, 3, 224, 224)).detach().numpy()
onnx_output = onnx_session.run(['output'], {'input': torch.randn(1, 3, 224, 224).numpy()})[0]

print(np.allclose(torch_output, onnx_output, rtol=1e-3))
```

## 2. TorchScript

### 追蹤（Tracing）

```python
model = MyModel()
model.eval()

# 使用 torch.jit.trace
traced_model = torch.jit.trace(model, torch.randn(1, 3, 224, 224))
traced_model.save('model_traced.pt')
```

### 腳本（Scripting）

```python
@torch.jit.script
def hello_script(x):
    return x + 1

# 用於包含控制流的模型
class MyModel(nn.Module):
    def forward(self, x):
        if x.sum() > 0:
            return x * 2
        else:
            return x / 2
```

## 3. C++ 部署

### 載入 TorchScript 模型

```cpp
// torch_cpp_inference.cpp
#include <torch/script.h>

int main() {
    torch::jit::script::Module model = torch::jit::load("model_traced.pt");
    model.eval();

    std::vector<torch::jit::IValue> inputs;
    inputs.push_back(torch::randn({1, 3, 224, 224}));

    at::Tensor output = model.forward(inputs).toTensor();
    std::cout << output.slice(/*dim=*/0, /*start=*/0, /*end=*/5) << std::endl;
}
```

### 編譯執行

```bash
g++ -std=c++14 -I/path/to/libtorch/include \
    -L/path/to/libtorch/lib -ltorch \
    torch_cpp_inference.cpp -o inference
```

## 4. 小結

ONNX 和 TorchScript 為 PyTorch 模型提供了多樣的部署選項，從 Python 到 C++、從伺服器到邊緣裝置都能支援。

---

**參考資料**
- [PyTorch Deployment Guide](https://www.google.com/search?q=PyTorch+deployment+ONNX+TorchScript)
- [TorchScript Tutorial](https://www.google.com/search?q=TorchScript+tutorial+PyTorch)