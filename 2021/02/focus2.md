# PyTorch Lightning 簡介

## 為何需要 Lightning？

傳統的 PyTorch 訓練迴圈充滿了樣板程式碼：

```python
# 傳統方式
for epoch in range(num_epochs):
    for batch in dataloader:
        optimizer.zero_grad()
        inputs, targets = batch
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
```

Lightning 將這些繁瑣的細節自動化，讓研究人員專注於模型設計。

## Lightning 的核心概念

### 1. 繼承 LightningModule

```python
import pytorch_lightning as pl

class LitModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(...)

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)
```

### 2. Trainer 自動處理

```python
trainer = pl.Trainer(
    gpus=2,
    max_epochs=10,
    accelerator='ddp'
)
trainer.fit(model, train_dataloader)
```

## 常用功能

### 自動紀錄

```python
def training_step(self, batch, batch_idx):
    loss = ...
    self.log('train_loss', loss)
    return loss
```

### 驗證與測試

```python
def validation_step(self, batch, batch_idx):
    loss = self.shared_eval(batch)
    self.log('val_loss', loss)

def test_step(self, batch, batch_idx):
    self.shared_eval(batch)
```

### Callbacks

```python
from pytorch_lightning.callbacks import EarlyStopping

early_stop = EarlyStopping(monitor='val_loss', patience=3)
trainer = Trainer(callbacks=[early_stop])
```

---

## 延伸閱讀

- [PyTorch Lightning 官方網站](https://www.google.com/search?q=PyTorch+Lightning+official)
- [Lightning+快速上手](https://www.google.com/search?q=PyTorch+Lightning+tutorial+quick+start)
- [Lightning+與原生PyTorch比較](https://www.google.com/search?q=Lightning+vs+PyTorch+boilerplate)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*