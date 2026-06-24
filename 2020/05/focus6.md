# 6. PyTorch 訓練優化實戰

## 基礎訓練迴圈

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

model = MyModel().cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
criterion = nn.CrossEntropyLoss()

for epoch in range(num_epochs):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.cuda(), target.cuda()
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
```

## 啟用所有優化

```python
from torch.cuda.amp import autocast, GradScaler

model = MyModel().cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
criterion = nn.CrossEntropyLoss()
scaler = GradScaler()

train_loader = DataLoader(
    dataset,
    batch_size=32,
    num_workers=4,
    pin_memory=True
)

for epoch in range(num_epochs):
    model.train()
    for batch in train_loader:
        optimizer.zero_grad()
        
        with autocast():
            output = model(batch["input"].cuda())
            loss = criterion(output, batch["target"].cuda())
        
        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()
```

## 資料載入優化

```python
from torch.utils.data import DataLoader

# 多程序載入
train_loader = DataLoader(
    dataset,
    batch_size=32,
    num_workers=4,  # 通常設為 CPU 核心數
    pin_memory=True,
    persistent_workers=True,  # PyTorch 1.7+
    prefetch_factor=2  # 每個程序預取多少批次
)
```

## 推論優化

```python
model.eval()
with torch.no_grad():
    for batch in test_loader:
        # 關閉梯度計算加速推論
        output = model(batch.input.cuda())
```

## torch.jit.script

將模型 JIT 編譯加速：

```python
model = MyModel().cuda()
model.eval()

# JIT 編譯
scripted_model = torch.jit.script(model)
scripted_model.save("model.pt")
```

## 效能瓶頸檢查

```python
import time

def benchmark(model, input_size, iterations=100):
    model.eval()
    x = torch.randn(*input_size).cuda()
    
    # 預熱
    for _ in range(10):
        _ = model(x)
    
    # 計時
    start = time.time()
    for _ in range(iterations):
        _ = model(x)
    elapsed = time.time() - start
    
    return elapsed / iterations * 1000  # ms
```

## 參考資源

- https://www.google.com/search?q=PyTorch+training+optimization+tips+speed+GPU+2020
- https://www.google.com/search?q=PyTorch+DataLoader+num_workers+pin_memory+performance
- https://www.google.com/search?q=PyTorch+inference+optimization+JIT+scripted+model+speed+up