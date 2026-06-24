# 自訂模型層

## 為什麼需要自訂層？

雖然 PyTorch 內建了豐富的神經網路層（Linear、Conv2d、LSTM 等），但在實際專案中，我們經常需要實作自訂的運算邏輯。PyTorch 的模組化設計讓自訂層變得非常簡單。

## 基本自訂層

建立自訂層只需要繼承 `nn.Module` 並實作 `__init__` 和 `forward`：

```python
import torch.nn as nn
import torch.nn.functional as F

class MyLinear(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(out_features, in_features))
        self.bias = nn.Parameter(torch.zeros(out_features))

    def forward(self, x):
        return F.linear(x, self.weight, self.bias)
```

## 無參數層

有些自訂層不需要可訓練的參數，例如啟動函數或正規化層：

```python
class CustomReLU(nn.Module):
    def forward(self, x):
        return torch.where(x > 0, x, x * 0.01)
```

## 結合多個操作的層

```python
class ConvBlock(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()
        self.conv = nn.Conv2d(in_c, out_c, 3, padding=1)
        self.bn = nn.BatchNorm2d(out_c)

    def forward(self, x):
        return F.relu(self.bn(self.conv(x)))
```

## 使用 nn.Parameter

`nn.Parameter` 是 Tensor 的子類，當賦值為 Module 的屬性時，會自動被註冊為可訓練參數。

除了直接使用 `nn.Parameter`，我們也可以使用 `nn.ParameterDict` 或 `nn.ParameterList` 來管理動態數量的參數。

## 自訂 autograd Function

如果需要自訂反向傳播的行為，可以繼承 `torch.autograd.Function`：

```python
class CustomSigmoid(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        out = 1 / (1 + (-x).exp())
        ctx.save_for_backward(out)
        return out

    @staticmethod
    def backward(ctx, grad_out):
        out, = ctx.saved_tensors
        return grad_out * out * (1 - out)
```

## 參考資料

- 擴充 PyTorch 指南：https://pytorch.org/docs/stable/notes/extending.html
- nn.Parameter 文件：https://pytorch.org/docs/stable/generated/torch.nn.Parameter.html
- 自訂 autograd Function 教學：https://pytorch.org/tutorials/beginner/examples_autograd/two_layer_net_custom_function.html
