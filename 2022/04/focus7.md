# PyTorch Lightning 與高階 API

## 訓練管線的痛點

在 PyTorch 中訓練一個模型需要撰寫大量的樣板程式碼：迴圈、loss 計算、梯度歸零、反向傳播、參數更新、學習率調整、驗證、日誌記錄等。這些程式碼在不同專案中高度重複。PyTorch Lightning 正是為了解決這個問題而誕生。

## Lightning 的核心設計

PyTorch Lightning 將程式碼分為兩個部分：
- **LightningModule**：定義模型架構、前向傳播、訓練/驗證/測試步驟
- **Trainer**：控制訓練流程（GPU 管理、梯度累積、分散式訓練等）

```python
import pytorch_lightning as pl

class MyModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.layer = nn.Linear(32, 10)

    def forward(self, x):
        return self.layer(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        loss = F.cross_entropy(self(x), y)
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)
```

## Trainer 的強大功能

```python
trainer = pl.Trainer(
    max_epochs=100,
    accelerator='auto',       # 自動偵測 GPU/TPU
    devices='auto',
    log_every_n_steps=10,
    enable_checkpointing=True,
)
trainer.fit(model, dataloader)
```

## Lightning 的關鍵優勢

- **自動裝置管理**：不需要手動呼叫 `.to(device)`
- **內建 checkpoint**：自動儲存最佳模型
- **TensorBoard 整合**：自動記錄訓練指標
- **16-bit 混合精度訓練**：一行程式碼啟用
- **分散式訓練**：DP、DDP、DeepSpeed 等策略

## 其他高階 API

- **Ignite**：由 PyTorch 團隊維護的進階訓練框架
- **Catalyst**：專注於電腦視覺的訓練框架
- **Hugging Face Trainer**：針對 Transformer 模型的訓練封裝

## 參考資料

- PyTorch Lightning 官方文件：https://lightning.ai/docs/pytorch/stable/
- LightningModule API：https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html
- Trainer 參數說明：https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html
