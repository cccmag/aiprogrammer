# TorchScript 與部署

## TorchScript 是什麼？

TorchScript 是 PyTorch 的模型序列化格式，可以將 PyTorch 模型轉換為可在無 Python 環境中執行的形式。

## 追蹤（Tracing）

```python
import torch
import torch.jit

class MyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = torch.nn.Linear(10, 5)

    def forward(self, x):
        return self.fc(x)

model = MyModel()
model.eval()

# 追蹤
example_input = torch.randn(1, 10)
traced_model = torch.jit.trace(model, example_input)
traced_model.save('model_traced.pt')
```

## 腳本化（Scripting）

```python
# 使用腳本（當模型有控制流時）
@torch.jit.script
def forward(x):
    if x.sum() > 0:
        return x * 2
    else:
        return x / 2

# 或針對整個模型
class ScriptedModel(torch.jit.ScriptModule):
    @torch.jit.script_method
    def forward(self, x):
        return torch.relu(x)
```

## TorchServe 部署

```bash
# 安裝
pip install torchserve

# 模型封裝
torch-model-archiver \
    --model-name my_model \
    --version 1.0 \
    --model-file model.py \
    --serialized-file model.pt \
    --handler handler.py \
    --extra-files index_to_name.json \
    --export-path /path/to/model/store

# 啟動服務
torchserve \
    --start \
    --ncs \
    --model-store /path/to/model/store \
    --models my_model=my_model.mar
```

## 處理器範例

```python
# handler.py
from torchserve.inference import BaseHandler

class MyHandler(BaseHandler):
    def preprocess(self, data):
        # 預處理
        return torch.tensor(data)

    def inference(self, data):
        # 推論
        return self.model(data)

    def postprocess(self, data):
        # 後處理
        return data.tolist()
```

## ONNX 匯出

```python
import torch.onnx

model = MyModel()
model.eval()

dummy_input = torch.randn(1, 10)
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
)
```

## C++ 載入

```cpp
// load_model.cpp
#include <torch/script.h>

int main() {
    torch::jit::script::Module model = torch::jit::load("model_traced.pt");
    std::vector<torch::jit::IValue> inputs;
    inputs.push_back(torch::randn({1, 10}));
    auto output = model.forward(inputs).toTensor();
}
```

## 參考資源

- https://www.google.com/search?q=TorchScript+PyTorch+JIT+deployment+tutorial+2020
- https://www.google.com/search?q=TorchServe+PyTorch+model+server+2020
- https://www.google.com/search?q=PyTorch+ONNX+export+C%2B%2B+deployment+2020