# 檢查點與 Early Stopping

## 模型檢查點基本操作

```python
import torch

# 儲存
torch.save({
    "epoch": epoch,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "loss": loss,
}, "checkpoint.pth")

# 載入
checkpoint = torch.load("checkpoint.pth")
model.load_state_dict(checkpoint["model_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
epoch = checkpoint["epoch"]
loss = checkpoint["loss"]
```

## 完整檢查點類別

```python
class CheckpointManager:
    def __init__(self, model, optimizer, checkpoint_dir="checkpoints"):
        self.model = model
        self.optimizer = optimizer
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(checkpoint_dir, exist_ok=True)
    
    def save(self, epoch, metric):
        checkpoint = {
            "epoch": epoch,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "metric": metric
        }
        path = os.path.join(self.checkpoint_dir, f"checkpoint_epoch_{epoch}.pth")
        torch.save(checkpoint, path)
        return path
    
    def load(self, path):
        checkpoint = torch.load(path)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        return checkpoint["epoch"], checkpoint["metric"]
    
    def save_best(self, metric_value, metric_name="loss"):
        # 儲存最佳模型
        best_path = os.path.join(self.checkpoint_dir, "best_model.pth")
        torch.save({
            "model_state_dict": self.model.state_dict(),
            "metric": metric_value
        }, best_path)
        print(f"新的最佳 {metric_name}: {metric_value:.4f}")
```

## Early Stopping

```python
class EarlyStopping:
    def __init__(self, patience=7, min_delta=0, mode="min"):
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.counter = 0
        self.best = None
        self.should_stop = False
    
    def __call__(self, metric):
        if self.best is None:
            self.best = metric
            return False
        
        if self.mode == "min":
            improved = metric < self.best - self.min_delta
        else:
            improved = metric > self.best + self.min_delta
        
        if improved:
            self.best = metric
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
        
        return self.should_stop
```

## 訓練循環整合

```python
def train_with_checkpointing(model, train_loader, val_loader, epochs=100):
    optimizer = torch.optim.Adam(model.parameters())
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer)
    checkpoint_manager = CheckpointManager(model, optimizer)
    early_stopping = EarlyStopping(patience=10, mode="min")
    
    for epoch in range(epochs):
        # 訓練
        train_loss = train_epoch(model, train_loader, optimizer)
        
        # 驗證
        val_loss = validate(model, val_loader)
        
        # 學習率排程
        scheduler.step(val_loss)
        
        # 儲存檢查點
        checkpoint_manager.save(epoch, val_loss)
        
        # 早停
        if early_stopping(val_loss):
            print(f"在第 {epoch+1} epoch 早停")
            break
    
    # 載入最佳模型
    checkpoint_manager.load_best()
```

## 只儲存權重

```python
# 只儲存模型權重（不包含優化器等）
torch.save(model.state_dict(), "model_weights.pth")

# 載入權重
model = MyModel()
model.load_state_dict(torch.load("model_weights.pth"))
```

## 參考資源

- https://www.google.com/search?q=PyTorch+checkpoint+save+load+model+training+tutorial+2020
- https://www.google.com/search?q=early+stopping+PyTorch+implementation+training+patience
- https://www.google.com/search?q=model+checkpoint+best+practice+deep+learning+training+save