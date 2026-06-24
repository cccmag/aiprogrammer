# 3. PyTorch 1.4/1.5

## PyTorch 核心特色

PyTorch 的動態計算圖（Define-by-Run）讓模型定義與 Python 程式碼完全整合。這意味著你可以使用標準 Python 流程控制來定義模型結構。

## 基本操作

```python
import torch

# 張量建立
x = torch.randn(3, 4)
print(x.shape)
print(x.dtype)

# GPU 支援
if torch.cuda.is_available():
    x = x.cuda()
    print(f"Device: {x.device}")
```

## 動態計算圖

```python
# 每一次執行都會重新建立計算圖
a = torch.tensor([1.0, 2.0], requires_grad=True)
b = a ** 2
c = b.sum()
c.backward()
print(a.grad)
```

## 模型定義

```python
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = x.view(-1, 784)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

model = SimpleNet()
print(model)
```

## 訓練循環

```python
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(5):
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
```

## torchvision

```python
import torchvision
import torchvision.transforms as transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

trainset = torchvision.datasets.MNIST(
    root='./data', train=True, download=True, transform=transform
)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=32, shuffle=True)
```

## PyTorch JIT (TorchScript)

```python
# TorchScript 追蹤
@torch.jit.script
def forward(x):
    return model(x)

# 腳本化
class MyModule(torch.jit.ScriptModule):
    def __init__(self):
        super().__init__()
        self.weights = torch.rand(10)

    @torch.jit.script_method
    def forward(self, x):
        return x * self.weights
```

## 模型儲存與載入

```python
# 儲存整個模型
torch.save(model, 'model.pth')

# 僅儲存參數（推薦）
torch.save(model.state_dict(), 'model_weights.pth')

# 載入
model.load_state_dict(torch.load('model_weights.pth'))
```

## 參考資源

- https://www.google.com/search?q=PyTorch+1.4+1.5+tutorial+dynamic+computation+graph+2020
- https://www.google.com/search?q=PyTorch+training+loop+nn+module+2020
- https://www.google.com/search?q=PyTorch+TorchScript+JIT+deployment+2020