# 模型部署策略

## TorchScript 導出

```python
import torch.jit

model = MyModel()
model.eval()

# 追蹤
example_input = torch.randn(1, 3, 224, 224)
traced = torch.jit.trace(model, example_input)
traced.save('model.pt')
```

## 模型量化

### 動態量化

```python
quantized = torch.quantization.quantize_dynamic(
    model, {nn.Linear, nn.LSTM}, dtype=torch.qint8
)
```

### 靜態量化

```python
model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
torch.quantization.prepare(model, inplace=True)
# calibration...
torch.quantization.convert(model, inplace=True)
```

## TorchServe 部署

```python
# torchserve 配置文件 config.properties
service_envelope=kservev2
Inference_address=http://0.0.0.0:8080
```

```bash
torchserve --start --model-name=model --model-file=model.py
```

## Mobile 部署

```python
# TorchScript to Lite
model = torch.jit.script(model)
optimized = torch.utils.mobile_optimizer.optimize_for_mobile(model)
optimized.save('model_lite.pt')
```

---

## 延伸閱讀

- [TorchServe+部署教學](https://www.google.com/search?q=TorchServe+deployment+tutorial)
- [PyTorch+模型量化](https://www.google.com/search?q=PyTorch+quantization+tutorial)
- [模型部署最佳實踐](https://www.google.com/search?q=PyTorch+deployment+best+practices)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*