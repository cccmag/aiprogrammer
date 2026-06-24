# torch.autograd 自動微分詳解

## PyTorch 的自動微分引擎

### 反向傳播的核心

PyTorch 的 `torch.autograd` 套件自動計算梯度，無需手動推導和實現反向傳播。

### 基本用法

```python
import torch

# 建立需要梯度的張量
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)

# 進行運算
y = x ** 2 + 2 * x + 1

# 計算梯度（預設只對葉節點計算）
y.sum().backward()

# 查看梯度
print(x.grad)  # tensor([4., 6., 8.])
# dy/dx = 2x + 2
```

### 計算圖機制

```python
# 每個運算都會建立 Function 節點
a = torch.tensor([1.0], requires_grad=True)
b = a * 2
c = b + 3
d = c ** 2

# 圖結構：a -> mul -> b -> add -> c -> pow -> d
# 反向傳播時沿著這個圖計算梯度
d.backward()
print(a.grad)  # dy/da = dy/dc * dc/db * db/da = 2c * 2 * 2 = 32
```

### 梯度累積

```python
# 梯度預設會累加
x = torch.tensor([1.0], requires_grad=True)

for _ in range(3):
    y = x ** 2
    y.backward()
    print(x.grad)  # 會累加

# 需要手動清除
x.grad.zero_()
```

### 禁用梯度計算

```python
# 兩種方式
with torch.no_grad():
    z = x + y
    # z 不會被記錄到計算圖

# 或裝飾器
@torch.no_grad()
def eval_model():
    return model(x)
```

### 自訂 autograd 函數

```python
from torch.autograd import Function

class Exp(Function):
    @staticmethod
    def forward(ctx, x):
        result = torch.exp(x)
        ctx.save_for_backward(result)
        return result

    @staticmethod
    def backward(ctx, grad_output):
        result, = ctx.saved_tensors
        return grad_output * result

# 使用自訂函數
y = Exp.apply(x)
```

### 向量對向量 Jacobian

```python
# 當輸出是多維張量時，需要傳入 gradient 參數
x = torch.tensor([1.0, 2.0], requires_grad=True)
y = x ** 2  # y = [1, 4]

# 等價於：d(y1, y2)/d(x1, x2)
# 全 1 向量會得到每個輸出的梯度總和
y.sum().backward()
# 等價於
# y.backward(torch.ones(2))
```

### 功能運算

```python
# detach：斷開計算圖
x = torch.tensor([1.0], requires_grad=True)
y = x * 2
z = y.detach()  # z 不會追蹤梯度

# retain_grad：保留中間層梯度
y.retain_grad()
z = y * 2
z.sum().backward()
print(y.grad)  # 中間層梯度也會保留
```

### 小結

`torch.autograd` 透過動態構建計算圖實現自動微分，開發者只需專注於前向傳播的實現。

---

**下一步**：[nn.Module 神經網路模組化](focus4.md)