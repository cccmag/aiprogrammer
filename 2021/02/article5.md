# 模型訓練流程實作

## 基本訓練迴圈

```python
model = Net()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

for epoch in range(num_epochs):
    for batch_idx, (inputs, targets) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
```

## 完整流程

```python
def train_model(model, train_loader, num_epochs):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for batch in train_loader:
            inputs, targets = batch
            inputs = inputs.to(device)
            targets = targets.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch}: loss = {avg_loss:.4f}")
```

## 監控與保存

```python
# 保存模型
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, 'checkpoint.pth')

# 載入模型
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
```

## 學習率排程

```python
scheduler = torch.optim.lr_scheduler.StepLR(
    optimizer, step_size=10, gamma=0.1
)

for epoch in range(num_epochs):
    train()
    scheduler.step()
```

---

## 延伸閱讀

- [訓練流程最佳實踐](https://www.google.com/search?q=PyTorch+training+loop+best+practices)
- [模型保存與載入](https://www.google.com/search?q=PyTorch+save+load+model)
- [學習率排程詳解](https://www.google.com/search?q=learning+rate+scheduler+PyTorch)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*