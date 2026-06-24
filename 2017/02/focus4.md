# PyTorch 的崛起：動態計算圖的魅力

## 前言

PyTorch 由 Facebook 的人工智慧研究團隊（FAIR）開發，於 2016 年 10 月發布。雖然比 TensorFlow 晚一年問世，但其動態計算圖設計迅速在研究社群獲得了廣大人氣。

## PyTorch 的起源

### 從 Torch 到 PyTorch

```
2002 年：Torch - Lua 語言的科學計算庫
    ↓
2016 年：PyTorch 發布 - Python 優先的深度學習框架
```

### 為什麼選擇 PyTorch？

```python
# TensorFlow 1.x 的寫法
import tensorflow as tf

# 需要先定義計算圖
x = tf.placeholder(tf.float32)
y = x * 2

with tf.Session() as sess:
    result = sess.run(y, feed_dict={x: 3.0})
```

```python
# PyTorch 的寫法
import torch

# 直接執行，無需 Session
x = torch.tensor([3.0], requires_grad=True)
y = x * 2
print(y.item())  # 6.0
```

## 動態計算圖

### 什麼是動態計算圖？

動態計算圖允許在每次執行時動態建構圖：

```python
# PyTorch：每次執行都可以不同
def forward(x):
    if x.sum() > 0:
        return x * 2
    else:
        return x * 3

# TensorFlow：圖在執行前就確定了
# 需要條件節點來處理不同情況
```

### 動態圖的優勢

1. **除錯簡單**：可以直接列印張量值
2. **條件邏輯**：自然地表達動態控制流
3. **可變輸入**：自然處理變長輸入
4. **快速實驗**：無需每次重建整個圖

```python
import torch

# 複雜的控制流
def dynamic_network(input):
    hidden = input
    for i in range(10):
        hidden = torch.relu(hidden @ W[i] + b[i])
        if hidden.mean() > 0.5:
            hidden = hidden * 0.5
    return hidden
```

## PyTorch 核心概念

### 張量（Tensor）

```python
import torch

# 建立張量
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.zeros(3, 4)
z = torch.randn(2, 3, 4)

# 張量運算
a = torch.tensor([1.0, 2.0])
b = torch.tensor([3.0, 4.0])
c = a + b  # 加法
d = a @ b  # 點積
```

### autograd：自動微分

PyTorch 的 autograd 提供了自動微分能力：

```python
import torch

# requires_grad 追蹤梯度
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x + 1

# 自動計算梯度
y.backward()
print(x.grad)  # dy/dx = 2x + 3 = 7
```

### 神經網路模組

```python
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.softmax(self.fc2(x), dim=1)
        return x

model = Net()
```

### 訓練流程

```python
import torch.optim as optim

# 定義模型、損失函數和優化器
model = Net()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 訓練循環
for epoch in range(10):
    for data, target in train_loader:
        optimizer.zero_grad()      # 梯度歸零
        output = model(data)       # 前向傳播
        loss = criterion(output, target)  # 計算損失
        loss.backward()            # 反向傳播
        optimizer.step()          # 更新參數
```

## PyTorch 與 TensorFlow 的比較

| 特性 | PyTorch | TensorFlow |
|------|---------|------------|
| 計算圖 | 動態 | 靜態（1.x）/ 動態（2.x）|
| 除錯 | 簡單 | 相對複雜 |
| 生態系統 | 成長中 | 完善 |
| 部署 | 較弱 | 較強 |
| 研究人氣 | 高 | 高 |
| 產業應用 | 較少 | 較多 |

### 各自優勢場景

```python
# 適合使用 PyTorch 的場景：
# - 研究和實驗
# - 需要動態控制流的模型
# - 快速原型開發
# - 處理變長輸入

# 適合使用 TensorFlow 的場景：
# - 生產環境部署
# - 需要大規模分散式訓練
# - 需要完整的工具鏈
# - TPU 或特殊硬體支援
```

## torchvision

PyTorch 提供了專門的視覺任務庫：

```python
import torchvision
import torchvision.transforms as transforms

# 資料增強
transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# 載入 CIFAR-10
trainset = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform
)
trainloader = torch.utils.data.DataLoader(
    trainset, batch_size=128, shuffle=True, num_workers=2
)
```

## 結語

PyTorch 的崛起代表了深度學習框架的一個重要方向——動態計算圖。其簡潔的 API 和靈活性使其迅速成為研究者的最愛。雖然在產業應用中 TensorFlow 仍然佔據主導地位，但 PyTorch 的成長勢頭強勁。

選擇框架時，應根據具體場景和需求來決定。對於研究和新實驗，PyTorch 是一個很好的選擇；對於生產部署，TensorFlow 提供了更完整的工具鏈。

---

## 延伸閱讀

- [PyTorch 官方網站](https://www.google.com/search?q=PyTorch+official+website)
- [PyTorch+動態計算圖](https://www.google.com/search?q=PyTorch+dynamic+computation+graph)
- [PyTorch+vs+TensorFlow+2017](https://www.google.com/search?q=PyTorch+vs+TensorFlow+comparison+2017)
- [PyTorch+ tutorials](https://www.google.com/search?q=PyTorch+tutorials+deep+learning)

---

*本篇文章為「AI 程式人雜誌 2017 年 2 月號」焦點系列之一。*