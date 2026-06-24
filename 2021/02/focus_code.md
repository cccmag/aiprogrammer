# PyTorch Lightning 實作範例

## 前言

本篇文章展示如何使用 PyTorch Lightning 快速建構訓練流程，包括基本的分類模型和常用功能。

完整的 Python 實作請參考：[_code/lightning_demo.py](_code/lightning_demo.py)

## 核心程式碼

### 基本分類模型

```python
import pytorch_lightning as pl
import torch.nn as nn
import torch.nn.functional as F

class LitClassifier(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 10)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return self.fc2(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)
```

### 訓練器設定

```python
from pytorch_lightning import Trainer

model = LitClassifier()
trainer = Trainer(
    gpus=1 if torch.cuda.is_available() else 0,
    max_epochs=10,
    progress_bar_refresh_rate=20
)
trainer.fit(model, train_dataloader)
```

### 驗證循環

```python
class LitClassifierWithVal(pl.LightningModule):
    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        val_loss = F.cross_entropy(y_hat, y)
        self.log('val_loss', val_loss, prog_bar=True)

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        acc = accuracy(y_hat, y)
        self.log('test_acc', acc)
```

### Early Stopping

```python
from pytorch_lightning.callbacks import EarlyStopping

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    mode='min'
)

trainer = Trainer(callbacks=[early_stop])
```

## 常用技巧

### 模型檢查點

```python
from pytorch_lightning.callbacks import ModelCheckpoint

checkpoint = ModelCheckpoint(
    monitor='val_loss',
    dirpath='checkpoints/',
    filename='best-model'
)
trainer = Trainer(callbacks=[checkpoint])
```

### 學習率排程

```python
def configure_optimizers(self):
    optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer, step_size=1, gamma=0.95
    )
    return [optimizer], [scheduler]
```

### 梯度裁剪

```python
trainer = Trainer(gradient_clip_val=1.0)
```

---

## 延伸閱讀

- [PyTorch Lightning 官方文檔](https://www.google.com/search?q=PyTorch+Lightning+documentation)
- [Lightning+範例庫](https://www.google.com/search?q=PyTorch+Lightning+examples)
- [MNIST+Lightning+教學](https://www.google.com/search?q=MNIST+PyTorch+Lightning+tutorial)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」補充文章。*