# 自動微分機制

## autograd 原理

PyTorch 的 autograd 系統自動追蹤張量上的運算，構建計算圖：

```python
x = torch.tensor([1.0, 2.0], requires_grad=True)
y = x ** 2
z = y.sum()
z.backward()  # 自動計算梯度
print(x.grad)  # [2, 4]
```

## 計算圖

```
x → square → y → sum → z
              ↓
         dz/dx = 2x = [2, 4]
```

## 梯度模式

```python
# 訓練模式（追蹤梯度）
model.train()

# 評估模式（不追蹤）
model.eval()

# 不追蹤
with torch.no_grad():
    output = model(input)
```

## 自定義運算

```python
class MyFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        return input.clamp(min=0)

    @staticmethod
    def backward(ctx, grad_output):
        input, = ctx.saved_tensors
        return grad_output * (input > 0).float()
```

---

## 延伸閱讀

- [autograd 官方文檔](https://www.google.com/search?q=PyTorch+autograd+documentation)
- [自動微分原理](https://www.google.com/search?q=automatic+differentiation+PyTorch)
- [backward+函數詳解](https://www.google.com/search?q=backward+function+PyTorch)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*