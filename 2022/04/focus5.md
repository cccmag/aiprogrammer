# 最佳化器與學習率排程

## 最佳化器概述

最佳化器（Optimizer）負責根據梯度更新模型參數。PyTorch 在 `torch.optim` 中提供了豐富的最佳化演算法。

```python
import torch.optim as optim

optimizer = optim.Adam(model.parameters(), lr=0.001)
```

## 常用最佳化器

### SGD
隨機梯度下降是最基礎的演算法，常搭配動量（momentum）使用：
```python
optim.SGD(params, lr=0.01, momentum=0.9)
```

### Adam
結合 Momentum 與 RMSProp 的優點，是目前最廣泛使用的預設最佳化器：
```python
optim.Adam(params, lr=0.001, betas=(0.9, 0.999))
```

### AdamW
修正 Adam 的權重衰減實作方式，在 Transformer 架構中表現更佳：
```python
optim.AdamW(params, lr=0.001, weight_decay=0.01)
```

## 學習率排程器

學習率排程器（Scheduler）在訓練過程中動態調整學習率：

### Step Decay
```python
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)
```

### Cosine Annealing
學習率餘弦衰減，在訓練後期溫和降低學習率：
```python
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)
```

### ReduceLROnPlateau
當 loss 不再下降時自動降低學習率：
```python
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', patience=5
)
```

## 排程器的正確使用方式

每個 epoch 結束後呼叫 `scheduler.step()`。注意 ReduceLROnPlateau 需要傳入監控指標。

## 學習率熱身（Warmup）

在訓練初期使用較小的學習率，避免模型震盪。可自訂 LambdaLR：

```python
lambda_lr = lambda epoch: min(1.0, epoch / 5) * 1.0
scheduler = optim.lr_scheduler.LambdaLR(optimizer, lambda_lr)
```

## 參考資料

- torch.optim 文件：https://pytorch.org/docs/stable/optim.html
- 學習率排程：https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate
- AdamW 論文：https://arxiv.org/abs/1711.05101
