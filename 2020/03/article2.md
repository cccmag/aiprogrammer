# PyTorch 動態計算圖

## autograd 核心

PyTorch 的自動微分系統（autograd）是其核心特色：

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x ** 2
z = y.sum()

z.backward()
print(x.grad)  # tensor([2., 4., 6.])
```

## 動態圖優勢

```python
# 可以使用 Python 流程控制
def dynamic_network(input_size, num_layers):
    layers = []
    for i in range(num_layers):
        if i == 0:
            layers.append(torch.nn.Linear(input_size, 64))
        else:
            layers.append(torch.nn.Linear(64, 64))
        layers.append(torch.nn.ReLU())
    return torch.nn.Sequential(*layers)

# 每次呼叫都可能不同
net1 = dynamic_network(100, 3)
net2 = dynamic_network(100, 5)
```

## Backward 鉤子

```python
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2

def hook_fn(grad):
    print(f"Gradient: {grad}")
    return grad * 2  # 修改梯度

handle = y.register_hook(hook_fn)
y.backward()
print(x.grad)  # 輸出梯度並修改後的值
handle.remove()
```

## 學習率排程

```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

for epoch in range(20):
    train(model)
    scheduler.step()
```

## 梯度裁剪

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
# 或
torch.nn.utils.clip_grad_value_(model.parameters(), clip_value=1.0)
```

## GPU 遷移

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
x = x.to(device)

# 單一模型在 CPU/GPU 間移動
model.cpu()
model.cuda()
```

## no_grad 上下文

```python
# 推論時不需要梯度
with torch.no_grad():
    output = model(x)

# 或裝飾器
@torch.no_grad()
def evaluate(model, x):
    return model(x)
```

## 參考資源

- https://www.google.com/search?q=PyTorch+autograd+dynamic+computation+graph+tutorial+2020
- https://www.google.com/search?q=PyTorch+backward+hook+gradient+manipulation+2020
- https://www.google.com/search?q=PyTorch+GPU+training+no_grad+2020