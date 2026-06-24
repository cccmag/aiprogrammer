# 正則化技術

## 前言

深度神經網路容易過擬合，特別是當模型過於複雜或訓練資料不足時。正則化技術是防止過擬合、提高模型泛化能力的關鍵。本篇文章將介紹各種正則化方法。

## 過擬合問題

```
┌─────────────────────────────────────────────────────────┐
│              過擬合示意圖                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  損失                                                 │
│    ^                                                   │
│    |        ╭────── 訓練集                              │
│    |       ╱                                        │
│    |      ╱  ╭──── 驗證集                              │
│    |     ╱ ╱                                         │
│    |    ╱ ╱                                          │
│    |   ╱ ╱                                           │
│    │  ╱ ╱                                            │
│    │ ╱ ╱                                             │
│    └─────────────────────────────────────→           │
│                                                  訓練時間│
│    訓練和驗證差距過大 = 過擬合                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## L1 和 L2 正則化

### L2 正則化 (Weight Decay)

```python
# L2 正則化 = Weight Decay
# 損失函數中添加：λ * Σ w²

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001,
    weight_decay=0.01  # Lambda = 0.01
)
```

### L1 正則化

```python
def l1_regularization(model, lambda_l1=0.01):
    loss_l1 = 0
    for param in model.parameters():
        loss_l1 += torch.sum(torch.abs(param))
    return lambda_l1 * loss_l1

# 在訓練循環中
for data, target in dataloader:
    optimizer.zero_grad()
    output = model(data)
    loss = F.cross_entropy(output, target)
    loss += l1_regularization(model, lambda_l1=0.01)
    loss.backward()
    optimizer.step()
```

## Dropout

Dropout 是最常用的正則化技術之一：

```python
class DropoutNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, dropout_rate=0.5):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.dropout1 = nn.Dropout(p=dropout_rate)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.dropout2 = nn.Dropout(p=dropout_rate)
        self.fc3 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout1(x)  # 訓練時隨機丟棄
        x = torch.relu(self.fc2(x))
        x = self.dropout2(x)
        x = self.fc3(x)
        return x

# 推論時 dropout 會被關閉
model.eval()  # 切換到推論模式
```

### Dropout 變體

```python
# 1. Alpha Dropout (SELU 激活搭配)
nn.AlphaDropout(p=0.5)

# 2. Feature Dropout (drop entire channels)
nn.Dropout2d(p=0.5)

# 3. Dropout 2D for spatial data
nn.Dropout2d(p=0.5)
```

## Early Stopping

```python
class EarlyStopping:
    def __init__(self, patience=10, min_delta=0.001):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = float('inf')

    def should_stop(self, val_loss):
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
        return self.counter >= self.patience

# 使用
early_stopping = EarlyStopping(patience=5)

for epoch in range(num_epochs):
    # 訓練
    train_loss = train_epoch(model, optimizer, train_loader)

    # 驗證
    val_loss = evaluate(model, val_loader)

    if early_stopping.should_stop(val_loss):
        print(f"Early stopping at epoch {epoch}")
        break
```

## 資料增強 (Data Augmentation)

### 影像資料增強

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
```

### 標籤平滑 (Label Smoothing)

```python
class LabelSmoothingCrossEntropy(nn.Module):
    def __init__(self, smoothing=0.1):
        super().__init__()
        self.smoothing = smoothing

    def forward(self, pred, target):
        n_classes = pred.size(-1)
        log_preds = F.log_softmax(pred, dim=-1)

        # 平滑標籤
        with torch.no_grad():
            smooth_targets = torch.zeros_like(pred)
            smooth_targets.fill_(self.smoothing / (n_classes - 1))
            smooth_targets.scatter_(1, target.unsqueeze(1), 1 - self.smoothing)

        return (-smooth_targets * log_preds).sum(-1).mean()
```

## 集成 (Ensemble)

```python
# 訓練多個模型，預測時平均
models = [create_model() for _ in range(5)]

# 訓練每個模型
for i, model in enumerate(models):
    train_model(model, train_loader)

# 預測時平均
def ensemble_predict(models, input):
    with torch.no_grad():
        outputs = [model(input) for model in models]
        avg_output = torch.stack(outputs).mean(0)
    return avg_output
```

## Batch Normalization 作為正則化

```python
# BatchNorm 有輕微的正則化效果
# 因為 mini-batch 的統計特性有噪聲

# 如果需要更強的正則化，可以使用：
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.BatchNorm1d(256),
    nn.ReLU(),
    nn.Dropout(0.3),  # 加上 Dropout
    nn.Linear(256, 10)
)
```

## 實際應用

```python
class RegularizedModel(nn.Module):
    def __init__(self):
        super().__init__()
        # 較好的預設配置
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Dropout2d(0.25),  # 卷積層後的 Dropout

            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Dropout2d(0.25),
        )

        self.classifier = nn.Sequential(
            nn.Linear(128 * 8 * 8, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),  # 全連接層更強的 Dropout
            nn.Linear(256, 10)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x
```

## 總結

常見正則化技術的組合使用：

| 技術 | 作用 | 典型值 |
|------|------|--------|
| L2 Weight Decay | 懲罰大的權重 | 1e-4 ~ 1e-2 |
| Dropout | 減少神經元共適應 | 0.2 ~ 0.5 |
| Early Stopping | 防止過度訓練 | patience=5~10 |
| Data Augmentation | 增加資料多樣性 | 任務相關 |
| Label Smoothing | 防止過度自信 | 0.1 ~ 0.2 |

---

**延伸閱讀**

- [Dropout Paper](https://www.google.com/search?q=dropout+srivastava+2014)
- [Regularization Techniques](https://www.google.com/search?q=regularization+deep+learning)
- [Data Augmentation](https://www.google.com/search?q=data+augmentation+techniques)