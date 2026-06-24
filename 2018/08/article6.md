# 遷移學習實戰

## 1. 遷移學習概述

遷移學習利用在大規模資料集（如 ImageNet）上預訓練的模型，加速新任務的訓練。

```python
# 兩種主要策略
# 1. 特徵萃取：凍結預訓練模型，只訓練新新增的分類頭
# 2. 微調：解凍並訓練部分或全部層
```

## 2. 特徵萃取

```python
from torchvision import models

# 載入預訓練模型
resnet = models.resnet18(pretrained=True)

# 凍結所有層
for param in resnet.parameters():
    param.requires_grad = False

# 只允許最後一層更新
num_features = resnet.fc.in_features
resnet.fc = nn.Linear(num_features, 10)  # 10 類分類

# 訓練時只有 fc 層會更新
optimizer = torch.optim.Adam(resnet.fc.parameters())
```

## 3. 微調策略

```python
# 微調策略一：微調最後幾層
for param in resnet.parameters():
    param.requires_grad = False

# 解凍最後一個 block 和 fc 層
for param in resnet.layer4.parameters():
    param.requires_grad = True

# 微調整個網路（較慢但通常效果更好）
for param in resnet.parameters():
    param.requires_grad = True
```

## 4. 學習率設定

```python
# 預訓練層使用較小學習率
optimizer = torch.optim.Adam([
    {'params': resnet.conv1.parameters(), 'lr': 1e-5},
    {'params': resnet.layer4.parameters(), 'lr': 1e-4},
    {'params': resnet.fc.parameters(), 'lr': 1e-3}
])
```

## 5. 完整範例

```python
def train_transfer_model(model, num_classes, train_loader, val_loader):
    # 替換分類頭
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, num_classes)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # 訓練
    best_acc = 0.0
    for epoch in range(20):
        train_loss, train_acc = train_epoch(model, train_loader)
        val_loss, val_acc = val_epoch(model, val_loader)

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), 'best_model.pth')

    return model
```

## 6. 小結

遷移學習是 2018 年深度學習的重要實踐，可以大幅減少訓練資料需求和訓練時間。

---

**參考資料**
- [Transfer Learning Guide](https://www.google.com/search?q=transfer+learning+CNN+PyTorch+tutorial)
- [Fine-tuning Tutorial](https://www.google.com/search?q=fine+tuning+pretrained+model+PyTorch)