# 訓練流程

## 前饋、損失、優化、迭代

完整的 PyTorch 訓練流程。

---

## 基本訓練迴圈

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# 1. 準備
model = MyModel().to(device)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 2. 訓練迴圈
for epoch in range(num_epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)

        # 前饋
        optimizer.zero_grad()           # 清零梯度
        output = model(data)            # 預測
        loss = criterion(output, target) # 計算損失

        # 反向傳播
        loss.backward()

        # 更新參數
        optimizer.step()

        if batch_idx % 100 == 0:
            print(f'Epoch: {epoch}, Batch: {batch_idx}, Loss: {loss.item()}')
```

---

## 損失函數

```python
# 迴歸
criterion = nn.MSELoss()        # 均方誤差
criterion = nn.L1Loss()         # 平均絕對誤差

# 分類
criterion = nn.CrossEntropyLoss()  # 交叉熵（自動 softmax）
criterion = nn.BCEWithLogitsLoss() # 二元交叉熵

# 自定義損失
class MyLoss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, pred, target):
        return torch.mean((pred - target) ** 2)
```

---

## 優化器

```python
# SGD
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Adam（常用）
optimizer = optim.Adam(model.parameters(), lr=0.001)

# AdamW
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

# 學習率排程
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
# 每 10 個 epoch 將 learning rate 乘以 0.1
```

---

## 完整範例

```python
def train_epoch(model, dataloader, criterion, optimizer, device):
    model.train()  # 設為訓練模式
    total_loss = 0

    for data, target in dataloader:
        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(dataloader)

def evaluate(model, dataloader, criterion, device):
    model.eval()  # 設為評估模式
    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for data, target in dataloader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)

            total_loss += loss.item()

            # 計算準確率（分類）
            _, predicted = torch.max(output, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()

    return total_loss / len(dataloader), correct / total
```

---

## 訓練技巧

```python
# 1. 梯度裁剪
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# 2. 早停
best_loss = float('inf')
if val_loss < best_loss:
    best_loss = val_loss
    torch.save(model.state_dict(), 'best_model.pth')
else:
    patience -= 1
    if patience == 0:
        break

# 3. 權重初始化
def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight)
        nn.init.zeros_(m.bias)

model.apply(init_weights)
```

---

## 延伸閱讀

- [PyTorch 訓練教程](https://www.google.com/search?q=pytorch+training+tutorial)
- [訓練技巧](https://www.google.com/search?q=deep+learning+training+tricks)

---

*本篇文章為「AI 程式人雜誌 2019 年 6 月號」系列文章之一。*