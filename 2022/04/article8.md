# 模型 checkpoint 管理

## 為什麼需要 checkpoint？

深度學習模型訓練通常需要大量時間。妥善的 checkpoint 管理可以：
- 在訓練中斷時從最近狀態恢復
- 保留訓練過程中的最佳模型
- 記錄完整的訓練歷史供後續分析

## 基礎 checkpoint 架構

一個完整的 checkpoint 應包含：

```python
def save_checkpoint(state, filename):
    torch.save({
        'epoch': state['epoch'],
        'model_state_dict': state['model'].state_dict(),
        'optimizer_state_dict': state['optimizer'].state_dict(),
        'scheduler_state_dict': state['scheduler'].state_dict(),
        'best_loss': state['best_loss'],
        'train_losses': state['train_losses'],
        'val_losses': state['val_losses'],
    }, filename)
```

## 最佳模型篩選

只儲存驗證集上表現最好的模型，避免過擬合後期覆寫好的權重：

```python
best_loss = float('inf')
for epoch in range(num_epochs):
    train_loss = train_one_epoch()
    val_loss = validate()

    if val_loss < best_loss:
        best_loss = val_loss
        torch.save(model.state_dict(), 'best_model.pth')
        print(f"Epoch {epoch}: new best model saved")
```

## 定期 checkpoint 與備份

除了最佳模型外，建議定期儲存完整 checkpoint：

```python
if epoch % 10 == 0:
    save_checkpoint({
        'epoch': epoch,
        'model': model,
        'optimizer': optimizer,
        'scheduler': scheduler,
        'best_loss': best_loss,
        'train_losses': train_losses,
        'val_losses': val_losses,
    }, f'checkpoint_epoch_{epoch}.pth')
```

## 中斷恢復訓練

```python
def load_checkpoint(filename, model, optimizer, scheduler):
    checkpoint = torch.load(filename)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
    return checkpoint['epoch'], checkpoint['best_loss']
```

## 版本管理與命名慣例

建議的 checkpoint 命名方式：
```
{project}/{run_id}/checkpoint_epoch_{epoch:04d}_{val_loss:.4f}.pth
{project}/{run_id}/best_model.pth
{project}/{run_id}/last_model.pth
```

## 使用 Lightning 內建管理

PyTorch Lightning 自動處理 checkpoint 管理：

```python
trainer = pl.Trainer(
    callbacks=[
        ModelCheckpoint(
            monitor='val_loss',
            mode='min',
            save_top_k=3,
            filename='{epoch}-{val_loss:.2f}'
        )
    ]
)
```

## 參考資料

- 模型儲存載入教學：https://pytorch.org/tutorials/beginner/saving_loading_models.html
- Lightning ModelCheckpoint：https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html
- MLflow Model Registry：https://mlflow.org/docs/latest/model-registry.html
