# Dropout 與其他正則化技術

## 前言

Dropout 是深度學習中最重要的正則化技術之一，由 Hinton 等人於 2012 年提出。本篇文章介紹 Dropout 和其他正則化方法。

## Dropout 原理

```python
class Dropout(nn.Module):
    def __init__(self, p=0.5):
        super().__init__()
        self.p = p  # 丟棄機率

    def forward(self, x):
        if self.training:
            # 訓練時隨機丟棄
            mask = torch.rand(x.size()) > self.p
            return x * mask / (1 - self.p)  # 縮放保持期望
        else:
            # 推論時使用完整網路
            return x
```

## Dropout 的效果

```
┌─────────────────────────────────────────────────────────┐
│              Dropout 示意圖                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  訓練時:                                               │
│  輸入 ──→ ○ ──→ ○ ──→ 輸出     (○ 表示可能丟棄的神經元)│
│                                                         │
│  推論時:                                               │
│  輸入 ──→ ● ──→ ● ──→ 輸出     (● 完整神經元)          │
│                                                         │
│  每一個 forward pass 都是不同的「稀疏」網路              │
│  減少神經元之間的共適應                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Dropout 變體

### 1. Spatial Dropout

```python
# 丟棄整個通道
nn.Dropout2d(p=0.3)
```

### 2. Alpha Dropout

```python
# 配合 SELU 激活使用
nn.AlphaDropout(p=0.5)
```

### 3. DropBlock

```python
# 丟棄連續區域，比 Dropout 更有效
class DropBlock2d(nn.Module):
    def __init__(self, block_size=7, p=0.5):
        super().__init__()
        self.block_size = block_size
        self.p = p
```

## 其他正則化技術

### L1/L2 正則化

```python
# L2 (Weight Decay)
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001,
    weight_decay=1e-4  # L2 正則化
)

# L1
def l1_regularization(model, lambda_l1=0.01):
    return sum(p.abs().sum() for p in model.parameters()) * lambda_l1
```

### Early Stopping

```python
# 監控驗證集表現
best_val_loss = float('inf')
patience = 10
patience_counter = 0

for epoch in range(num_epochs):
    val_loss = evaluate(model, val_loader)
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        save_checkpoint(model)
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print("Early stopping!")
            break
```

### 資料增強

```python
# 影像資料增強
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(0.2, 0.2),
    transforms.ToTensor(),
])
```

## 組合使用

```python
class RegularizedModel(nn.Module):
    def __init__(self):
        super().__init__()
        # 網路結構
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Dropout2d(0.25),  # 卷積層後的 Dropout
        )

        self.classifier = nn.Sequential(
            nn.Linear(64 * 32 * 32, 256),
            nn.ReLU(),
            nn.Dropout(0.5),  # 全連接層的 Dropout
            nn.Linear(256, 10)
        )
```

## 正則化強度比較

| 方法 | 效果 | 額外成本 |
|------|------|----------|
| Dropout | 強 | 訓練時間增加 |
| L2 Decay | 中 | 幾乎無 |
| Early Stopping | 強 | 需監控 |
| Data Augmentation | 強 | 需額外處理 |
| Batch Normalization | 中 | 些微增加 |

---

**延伸閱讀**

- [Dropout Paper (Srivastava et al., 2014)](https://www.google.com/search?q=dropout+srivastava+2014)
- [Dropout Regularization](https://www.google.com/search?q=dropout+regularization+deep+learning)

---

*本篇文章為「AI 程式人雜誌 2017 年 11 月號」AI 相關文章之一。*