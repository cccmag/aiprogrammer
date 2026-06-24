# 自動微分

## autograd 機制詳解

PyTorch 的 autograd 系統自動計算梯度，是深度學習訓練的基礎。

---

## 基本概念

### 什麼是自動微分？

自動微分（Automatic Differentiation）不同於：
- **數值微分**：有限差分近似，有精度誤差
- **符號微分**：完整數學表達式，複雜

自動微分可以精確地計算任意複雜函數的梯度。

### 計算圖

```python
# PyTorch 使用動態計算圖
# 每次操作都記錄 op、輸入輸出

x = torch.tensor([1.0], requires_grad=True)
y = x ** 2
z = y * 3

# 計算圖：
# x -> y = x**2 -> z = y*3
```

---

## 使用 autograd

### 基本用法

```python
x = torch.tensor([2.0, 3.0], requires_grad=True)

# 前向傳播
y = x ** 2
z = y.sum()

# 反向傳播
z.backward()

# 查看梯度
print(x.grad)  # tensor([4., 6.])
# dz/dx = 2x = [4, 6]
```

### 梯度的計算規則

```python
# 簡單範例：y = x^2, dy/dx = 2x
x = torch.tensor([3.0], requires_grad=True)
y = x ** 2
y.backward()
print(x.grad)  # tensor([6.])

# 鏈式法則
# z = y^2, y = 2x
# dz/dx = dz/dy * dy/dx = 2y * 2 = 2*(2x) * 2 = 8x
x = torch.tensor([3.0], requires_grad=True)
y = 2 * x
z = y ** 2
z.backward()
print(x.grad)  # tensor([48.])
```

---

## 控制梯度計算

### 停止梯度追蹤

```python
# 方法 1：使用 detach()
x = torch.tensor([1.0], requires_grad=True)
y = x * 2
y_detached = y.detach()  # 新的張量，不需要梯度

# 方法 2：使用 no_grad()
with torch.no_grad():
    z = x ** 2  # 不會被記錄
```

### torch.no_grad() vs requires_grad

```python
# 全域禁用
torch.set_grad_enabled(False)

# 局部禁用
with torch.no_grad():
    z = x ** 2

# 個別張量
x = torch.tensor([1.0], requires_grad=False)  # 不追蹤梯度
```

---

## 梯度的累積

```python
# 梯度預設會累積
x = torch.tensor([1.0], requires_grad=True)

for i in range(3):
    y = x ** 2
    y.backward()
    print(x.grad)  # 會累加：2, 4, 6

# 需要手動清零
x = torch.tensor([1.0], requires_grad=True)
for i in range(3):
    y = x ** 2
    y.backward()
    print(x.grad)
    x.grad.zero_()  # 清零
```

---

## 高階導數

```python
# 計算二階導數
x = torch.tensor([2.0], requires_grad=True)
y = x ** 3

# 第一階導數
first_grad = torch.autograd.grad(y, x, create_graph=True)
print(first_grad)  # tensor([12.])

# 第二階導數
second_grad = torch.autograd.grad(first_grad[0], x)
print(second_grad)  # tensor([12.])
# d/dx(x^3) = 3x^2, at x=2: 3*4 = 12
# d/dx(3x^2) = 6x, at x=2: 6*2 = 12
```

---

## 自定義 autograd 函數

```python
import torch.nn.functional as F

class ReLU(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        return input.clamp(min=0)

    @staticmethod
    def backward(ctx, grad_output):
        input, = ctx.saved_tensors
        grad_input = grad_output.clone()
        grad_input[input < 0] = 0
        return grad_input
```

---

## 在神經網路中的使用

```python
import torch.nn as nn
import torch.optim as optim

# 定義模型
model = nn.Linear(10, 1)
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 訓練迴圈
for data, target in dataloader:
    optimizer.zero_grad()      # 1. 清零梯度
    output = model(data)       # 2. 前饋
    loss = criterion(output, target)
    loss.backward()            # 3. 反向傳播
    optimizer.step()          # 4. 更新參數
```

---

## 延伸閱讀

- [PyTorch autograd 文檔](https://www.google.com/search?q=pytorch+autograd+tutorial)
- [自動微分原理](https://www.google.com/search?q=automatic+differentiation+deep+learning)

---

*本篇文章為「AI 程式人雜誌 2019 年 6 月號」系列文章之一。*