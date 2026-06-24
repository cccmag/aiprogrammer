# PyTorch 1.1 新特性

## 前言

PyTorch 1.1 於 2019 年 5 月發布，带来多項改進。

## 主要新特性

### 1. JIT 改進

```python
# 更好的 TorchScript 支援
@torch.jit.script
def function(x):
    return x ** 2
```

### 2. TensorBoard 原生支援

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment')
writer.add_scalar('loss', loss, epoch)
writer.add_histogram('weights', model.weight, epoch)
writer.close()
```

### 3. 改進的量化支援

```python
model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
torch.quantization.prepare(model, inplace=True)
```

## 升級建議

```bash
pip install torch==1.1.0 -f https://download.pytorch.org/whl/torch_stable.html
```

## 延伸閱讀

- [PyTorch 1.1 發布說明](https://www.google.com/search?q=Pytorch+1.1+release+notes)