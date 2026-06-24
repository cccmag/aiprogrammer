# 模型優化技巧

## 正則化

### Dropout

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, 10)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)
```

### L2 正則化

```python
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=1e-3,
    weight_decay=1e-5  # L2 正則化
)
```

### Early Stopping

```python
best_loss = float('inf')
patience = 5
counter = 0

for epoch in range(num_epochs):
    val_loss = validate()
    if val_loss < best_loss:
        best_loss = val_loss
        counter = 0
    else:
        counter += 1
        if counter >= patience:
            break
```

## 學習率排程

```python
# Step LR
scheduler = torch.optim.lr_scheduler.StepLR(
    optimizer, step_size=10, gamma=0.1
)

# Cosine Annealing
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=50
)

# Warmup
scheduler = torch.optim.lr_scheduler.LinearLR(
    optimizer, start_factor=0.1, total_iters=10
)
```

## 批次歸一化

```python
# 1D
nn.BatchNorm1d(num_features)

# 2D (CNN)
nn.BatchNorm2d(num_features)
```

---

## 延伸閱讀

- [正則化技術比較](https://www.google.com/search?q=regularization+techniques+deep+learning)
- [學習率排程詳解](https://www.google.com/search?q=learning+rate+scheduler+pytorch)
- [Early+Stopping+實作](https://www.google.com/search?q=early+stopping+pytorch)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*