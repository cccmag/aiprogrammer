# PyTorch 自動微分

## 為什麼需要自動微分？

如前文所述，反向傳播計算梯度涉及複雜的鏈式法則推導。對於簡單網路我們可以手算，但對於現代深度學習模型（數百層、複雜分支），手動推導是不可能的。

自動微分（Automatic Differentiation, AD）解決了這個問題——它自動追蹤計算圖並計算梯度。

## PyTorch 的自動微分機制

PyTorch 使用「動態計算圖」的方式實現自動微分。

```python
import torch

# 創建需要梯度的張量
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
w = torch.tensor([0.5, 0.3, 0.2], requires_grad=True)
b = torch.tensor([0.1], requires_grad=True)

# 前向計算（PyTorch 自動建構計算圖）
z = torch.dot(x, w) + b
y = torch.sigmoid(z)

# 反向傳播（自動計算梯度）
y.backward()

# 查看梯度
print(w.grad)  # 自動計算出的梯度
print(b.grad)
```

### requires_grad

`requires_grad=True` 告訴 PyTorch 追蹤這個張量的所有運算，以便後續計算梯度。

### backward() 方法

`backward()` 從當前張量開始，反向遍歷計算圖，使用鏈式法則計算所有 `requires_grad=True` 的張量的梯度。

## 計算圖

PyTorch 將計算過程表示為有向無環圖：

```
           x ──┐
           w ──┼── dot ──┐
           b ──┼────(+)──┼── sigmoid ── y
               └─────────┘
```

節點是張量，邊是運算。每次 forward 時，PyTorch 自動建構這個圖；backward 時，圖被用來計算梯度。

### 動態圖

PyTorch 的圖是「動態」的——每次迭代重新建構。這意味著：

```python
for epoch in range(10):
    # 每次循環都建立新的計算圖
    z = torch.dot(x, w) + b
    y = torch.sigmoid(z)
    loss = (y - target) ** 2
    loss.backward()
    # 更新權重
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
    # 清除梯度
    w.grad.zero_()
    b.grad.zero_()
```

## 實戰範例

### 定義一個簡單的 MLP

```python
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(2, 4)   # 2→4
        self.fc2 = nn.Linear(4, 1)   # 4→1
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.sigmoid(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x

model = MLP()
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.5)
```

### 訓練循環

```python
X = torch.tensor([[0,0],[0,1],[1,0],[1,1]], dtype=torch.float32)
Y = torch.tensor([[0],[1],[1],[0]], dtype=torch.float32)

for epoch in range(10000):
    # 前向傳播
    y_pred = model(X)
    loss = criterion(y_pred, Y)
    
    # 反向傳播
    optimizer.zero_grad()
    loss.backward()
    
    # 更新權重
    optimizer.step()
    
    if epoch % 2000 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.6f}")
```

### 自動做了什麼？

使用 PyTorch 時，我們不需要手動推導任何梯度。框架自動完成了：
- 計算圖的建構
- 鏈式法則的應用
- 所有參數的梯度計算
- 優化器的參數更新

## 高階自動微分

### 自訂 autograd 函數

```python
class MyReLU(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return x.clamp(min=0)

    @staticmethod
    def backward(ctx, grad_output):
        x, = ctx.saved_tensors
        grad_input = grad_output.clone()
        grad_input[x < 0] = 0
        return grad_input
```

### 計算二階梯度

```python
x = torch.tensor([1.0], requires_grad=True)
y = x ** 3
grad = torch.autograd.grad(y, x, create_graph=True)
second_grad = torch.autograd.grad(grad, x)
```

## 自動微分 vs 其他方法

| 方法 | 精度 | 效能 | 實作難度 |
|------|------|------|---------|
| 手動梯度 | 高 | 最快 | 極難 |
| 數值微分 | 低（誤差） | 慢 | 簡單 |
| 符號微分 | 高 | 中等 | 複雜 |
| 自動微分 | 高 | 快 | 最簡單 |

---

## 延伸閱讀

- [PyTorch Autograd 文檔](https://www.google.com/search?q=PyTorch+autograd+tutorial)
- [Automatic Differentiation 介紹](https://www.google.com/search?q=automatic+differentiation+explained)
- [計算圖深度理解](https://www.google.com/search?q=computation+graph+deep+learning)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」精選文章。*
