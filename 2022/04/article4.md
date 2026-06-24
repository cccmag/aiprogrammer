# 損失函數選擇指南

## 分類任務

### CrossEntropyLoss（交叉熵損失）
最常用的分類損失函數，內部整合了 LogSoftmax 和 NLLLoss：
- 適用於多類別分類
- 輸入為原始 logits（不需要經過 softmax）
- 標籤為類別索引（非 one-hot）

```python
loss_fn = nn.CrossEntropyLoss()
loss = loss_fn(logits, labels)
```

### BCELoss 與 BCEWithLogitsLoss
二元分類的損失函數：
- `BCELoss` 需要輸入經過 sigmoid
- `BCEWithLogitsLoss` 內部整合 sigmoid，推薦使用

```python
loss_fn = nn.BCEWithLogitsLoss()
loss = loss_fn(logits, labels)
```

## 迴歸任務

### MSELoss（均方誤差）
最常見的迴歸損失，對異常值敏感：
```python
loss_fn = nn.MSELoss()
```

### L1Loss（平均絕對誤差）
對異常值更魯棒：
```python
loss_fn = nn.L1Loss()
```

### SmoothL1Loss（Huber Loss）
結合 MSE 和 L1 的優點，在誤差小時表現如 MSE，誤差大時如 L1：
```python
loss_fn = nn.SmoothL1Loss()
```

## 特殊任務損失

### ContrastiveLoss（對比損失）
用於 Siamese Network 或度量學習：
```python
def contrastive_loss(x1, x2, label, margin=1.0):
    dist = F.pairwise_distance(x1, x2)
    loss = label * dist.pow(2) + (1 - label) * F.relu(margin - dist).pow(2)
    return loss.mean()
```

### TripletMarginLoss
用於人臉辨識、特徵嵌入等任務。

## 自訂損失函數

PyTorch 中自訂損失函數非常直覺：

```python
def weighted_mse(pred, target, weights):
    return (weights * (pred - target) ** 2).mean()
```

或者包裝為 Module：
```python
class WeightedMSE(nn.Module):
    def __init__(self, weights):
        super().__init__()
        self.weights = weights
    def forward(self, pred, target):
        return (self.weights * (pred - target) ** 2).mean()
```

## 參考資料

- 損失函數列表：https://pytorch.org/docs/stable/nn.html#loss-functions
- 自訂損失函數：https://pytorch.org/docs/stable/notes/extending.html
- 不平衡分類處理：https://pytorch.org/docs/stable/data.html#torch.utils.data.WeightedRandomSampler
