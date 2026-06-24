# 混合精度訓練範例

## 基礎 AMP 設定

```python
import torch
from torch.cuda.amp import autocast, GradScaler

model = MyModel().cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
scaler = GradScaler()

for batch in train_loader:
    optimizer.zero_grad()
    
    with autocast():
        output = model(batch["input"].cuda())
        loss = criterion(output, batch["target"].cuda())
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## 完整訓練範例

```python
import torch
import torch.nn as nn
from torch.cuda.amp import autocast, GradScaler

class SimpleClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Linear(256, 10)
        )
    
    def forward(self, x):
        return self.net(x)

def train_with_amp(model, train_loader, epochs=3):
    device = torch.device("cuda")
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()
    scaler = GradScaler()
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            
            with autocast():
                output = model(data)
                loss = criterion(output, target)
            
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            
            total_loss += loss.item()
            
            if batch_idx % 100 == 0:
                print(f"Epoch {epoch+1}, Batch {batch_idx}, Loss: {loss.item():.4f}")
        
        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1} Average Loss: {avg_loss:.4f}")

# 使用範例
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST("./data", train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=4, pin_memory=True)

model = SimpleClassifier()
train_with_amp(model, train_loader)
```

## 與梯度累積結合

```python
def train_amp_accumulation(model, train_loader, accum_steps=4):
    optimizer = torch.optim.Adam(model.parameters())
    scaler = GradScaler()
    criterion = nn.CrossEntropyLoss()
    
    model.train()
    optimizer.zero_grad()
    
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.cuda(), target.cuda()
        
        with autocast():
            output = model(data)
            loss = criterion(output, target) / accum_steps
        
        scaler.scale(loss).backward()
        
        if (batch_idx + 1) % accum_steps == 0:
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad()
```

## 自定義區域使用 FP32

某些操作需要在 FP32 中執行：

```python
from torch.cuda.amp import autocast

model = MyModel().cuda()

# 大部分運算使用 FP16
with autocast():
    output = model(input_fp16)
    
    # 明確轉換為 FP32
    output_fp32 = output.float()
    
    # 繼續在 FP32 中處理
    logits = layer_norm(output_fp32)
```

## 參考資源

- https://www.google.com/search?q=PyTorch+AMP+automatic+mixed+precision+complete+example+2020
- https://www.google.com/search?q=GradScaler+gradient+accumulation+PyTorch+combination+tutorial
- https://www.google.com/search?q=mixed+precision+training+FP16+memory+speed+optimization+example