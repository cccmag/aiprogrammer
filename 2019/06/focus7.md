# 模型存取與部署

## 保存、載入、 TorchScript

PyTorch 提供多種方式保存和部署模型。

---

## 模型保存

### 保存整個模型

```python
# 保存
torch.save(model, 'model.pth')

# 載入
model = torch.load('model.pth')
```

### 保存參數（推薦）

```python
# 保存
torch.save(model.state_dict(), 'model_weights.pth')

# 載入
model = MyModel()
model.load_state_dict(torch.load('model_weights.pth'))
```

### 保存檢查點

```python
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}
torch.save(checkpoint, 'checkpoint.pth')

# 載入
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
```

---

## TorchScript

TorchScript 是 PyTorch 的部署方案，可以將模型轉換為可部署格式。

### 追蹤（Tracing）

```python
import torch.jit as jit

class MyModel(nn.Module):
    def forward(self, x):
        return x ** 2

model = MyModel()
model.eval()

# 追蹤
example_input = torch.tensor([1.0, 2.0, 3.0])
traced_model = jit.trace(model, example_input)

# 保存
traced_model.save('traced_model.pt')

# 載入
loaded_model = jit.load('traced_model.pt')
```

### 腳本（Scripting）

```python
import torch.jit as jit

@jit.script
def scripted_function(x):
    return x ** 2

# 或
class MyModule(nn.Module):
    @jit.script_method
    def forward(self, x):
        return x ** 2
```

---

## ONNX 導出

```python
import torch.onnx

# 導出為 ONNX
model = MyModel()
model.eval()

dummy_input = torch.randn(1, 10)
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

# 驗證
import onnx
model_onnx = onnx.load('model.onnx')
onnx.checker.check_model(model_onnx)
```

---

## PyTorch Mobile

```python
# Lite Interpreter
model = MyModel()
model.eval()
model._run_lazy_scripts()  # 初始化

# 儲存為 Lite 格式
model._save_for_lite_interpreter('model.ptl')
```

---

## 推論優化

```python
# 評估模式
model.eval()

# 使用 torch.no_grad()
with torch.no_grad():
    output = model(input)

# 量化
model quantized = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)
```

---

## 延伸閱讀

- [PyTorch 模型保存](https://www.google.com/search?q=pytorch+model+save+load+tutorial)
- [TorchScript 教程](https://www.google.com/search?q=torchscript+tutorial+pytorch)
- [ONNX 官網](https://www.google.com/search?q=onnx+official+website)

---

*本篇文章為「AI 程式人雜誌 2019 年 6 月號」系列文章之一。*