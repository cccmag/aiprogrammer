# 倒傳遞演算法

倒傳遞（Backpropagation）是神經網路的訓練核心。

## 1. 梯度下降

```python
def gradient_descent(parameters, gradients, learning_rate):
    for param, grad in zip(parameters, gradients):
        param -= learning_rate * grad
```

## 2. 自動微分

PyTorch 的 autograd 自動計算梯度：

```python
x = torch.tensor([1.0, 2.0], requires_grad=True)
y = x ** 2
y.sum().backward()
print(x.grad)
```

## 3. 訓練循環

```python
model = SimpleNN(4, 128, 2)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

for epoch in range(100):
    optimizer.zero_grad()
    output = model(X)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
```

---

## 延伸閱讀

- [Backpropagation 詳解](https://www.google.com/search?q=backpropagation+algorithm+explained)
- [自動微分原理](https://www.google.com/search?q=automatic+differentiation+deep+learning)