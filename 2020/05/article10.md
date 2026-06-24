# 完整訓練流程實作

## 完整範例

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.cuda.amp import autocast, GradScaler

class Trainer:
    def __init__(self, model, train_loader, val_loader, config):
        self.model = model.cuda()
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config
        
        self.optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=config["lr"],
            weight_decay=config["weight_decay"]
        )
        self.scheduler = torch.optim.lr_scheduler.OneCycleLR(
            self.optimizer,
            max_lr=config["lr"],
            epochs=config["epochs"],
            steps_per_epoch=len(train_loader)
        )
        self.scaler = GradScaler()
        self.criterion = nn.CrossEntropyLoss()
        
        self.best_loss = float("inf")
        self.early_stopping = EarlyStopping(patience=7)
    
    def train_epoch(self):
        self.model.train()
        total_loss = 0
        
        for batch_idx, (data, target) in enumerate(self.train_loader):
            data, target = data.cuda(), target.cuda()
            
            self.optimizer.zero_grad()
            
            with autocast():
                output = self.model(data)
                loss = self.criterion(output, target)
            
            self.scaler.scale(loss).backward()
            self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.scaler.step(self.optimizer)
            self.scaler.update()
            self.scheduler.step()
            
            total_loss += loss.item()
        
        return total_loss / len(self.train_loader)
    
    def validate(self):
        self.model.eval()
        total_loss = 0
        
        with torch.no_grad():
            for data, target in self.val_loader:
                data, target = data.cuda(), target.cuda()
                
                with autocast():
                    output = self.model(data)
                    loss = self.criterion(output, target)
                
                total_loss += loss.item()
        
        return total_loss / len(self.val_loader)
    
    def train(self):
        for epoch in range(self.config["epochs"]):
            train_loss = self.train_epoch()
            val_loss = self.validate()
            
            print(f"Epoch {epoch+1}/{self.config['epochs']}")
            print(f"  Train Loss: {train_loss:.4f}")
            print(f"  Val Loss: {val_loss:.4f}")
            print(f"  LR: {self.optimizer.param_groups[0]['lr']:.6f}")
            
            if val_loss < self.best_loss:
                self.best_loss = val_loss
                torch.save(self.model.state_dict(), "best_model.pth")
            
            if self.early_stopping(val_loss):
                print("Early stopping triggered")
                break


# 設定
config = {
    "lr": 1e-3,
    "weight_decay": 0.01,
    "epochs": 100,
    "batch_size": 32,
    "accumulation_steps": 4
}

# 初始化
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4, pin_memory=True)
val_loader = DataLoader(val_dataset, batch_size=32, num_workers=4, pin_memory=True)

model = MyModel()
trainer = Trainer(model, train_loader, val_loader, config)
trainer.train()
```

## 最終模型載入

```python
# 載入最佳模型
model = MyModel()
model.load_state_dict(torch.load("best_model.pth"))
model.eval()

# 使用模型
with torch.no_grad():
    output = model(input_tensor.cuda())
```

## 參考資源

- https://www.google.com/search?q=complete+PyTorch+training+loop+AMP+checkpoint+early+stopping+2020
- https://www.google.com/search?q=full+training+pipeline+example+deep+learning+best+practices
- https://www.google.com/search?q=PyTorch+trainer+class+template+production+training+workflow