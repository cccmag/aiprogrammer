# TorchScript 與模型部署

## TorchScript 是什麼？

TorchScript 是 PyTorch 的機器編譯格式，可將 PyTorch 模型轉換為可部署的形式：

- **靜態圖**：擺脫 Python 執行開銷
- **可序列化**：保存和載入模型
- **跨平台**：支援 C++、行動裝置等

## 兩種使用方式

### 1. torch.jit.script（追蹤）

```python
import torch.jit

class Net(nn.Module):
    def forward(self, x):
        return torch.relu(self.fc(x))

model = Net()
scripted = torch.jit.script(model)
scripted.save('model.pt')
```

### 2. torch.jit.trace（腳本）

```python
example_input = torch.randn(1, 10)
traced = torch.jit.trace(model, example_input)
traced.save('model.pt')
```

## C++ 部署範例

```cpp
#include <torch/script.h>

torch::jit::script::Module module = torch::jit::load("model.pt");
std::vector<torch::jit::IValue> inputs;
inputs.push_back(torch::randn({1, 10}));
at::Tensor output = module.forward(inputs).toTensor();
```

## 生產部署架構

```
Python 訓練
    ↓
導出 TorchScript
    ↓
部署環境（C++/Java/Mobile）
    ↓
推理服務
```

## 效能優化

```python
# 最佳化推理效能
with torch.no_grad():
    output = model(input)

# 使用 JIT 最佳化
model = torch.jit.optimize_for_inference(torch.jit.script(model))
```

---

## 延伸閱讀

- [TorchScript 官方文檔](https://www.google.com/search?q=TorchScript+documentation)
- [PyTorch+C++部署教程](https://www.google.com/search?q=PyTorch+C++deployment+tutorial)
- [JIT+編譯原理](https://www.google.com/search?q=TorchScript+JIT+compilation)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*