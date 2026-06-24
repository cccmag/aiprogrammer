# 3. 混合精度訓練 (AMP)

## 為什麼需要混合精度

混合精度訓練使用 FP16 進行大部分運算，同時保留關鍵區域的 FP32 精度，既加速訓練又保持模型準確度。

優點：
- 訓練速度提升 1.5-3 倍
- 記憶體使用減少約 50%
- 大多數模型精度幾乎不受影響

## PyTorch AMP 使用

PyTorch 1.6+ 內建 AMP 支援：

```python
from torch.cuda.amp import autocast, GradScaler

model = MyModel().cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
scaler = GradScaler()

for batch in train_loader:
    optimizer.zero_grad()
    
    with autocast():
        outputs = model(batch["input"].cuda())
        loss = criterion(outputs, batch["target"].cuda())
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## GradScaler 詳解

GradScaler 自動處理梯度縮放，避免 FP16 下溢（underflow）問題：

```python
scaler = GradScaler()

# 訓練循環
for data, target in train_loader:
    optimizer.zero_grad()
    
    with autocast():
        output = model(data.cuda())
        loss = loss_fn(output, target.cuda())
    
    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)  # 解除縮放以正確裁剪
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    scaler.step(optimizer)
    scaler.update()
```

## 記憶體節省範例

| 配置 | 批次大小 | 可用 GPU |
|------|---------|---------|
| FP32 | 16 | 1 張 |
| FP16 | 32 | 1 張 |
| FP16 + 梯度累積 | 64 | 1 張（分 4 次累積） |

## 何時使用 FP32

建議在以下操作保持 FP32：
- 優化器狀態（如 Adam 的動量）
- 梯度裁剪
- 極敏感的 LayerNorm/BatchNorm

## BF16 vs FP16

A100 引入了 BF16（Brain Float 16）：
- BF16：1 個符號位 + 8 個指數位 + 7 個尾數位
- FP16：1 個符號位 + 5 個指數位 + 10 個尾數位

BF16 的指數位與 FP32 相同動態範圍，不易溢出，但精度較低。

## 參考資源

- https://www.google.com/search?q=PyTorch+AMP+automatic+mixed+precision+tutorial+training+2020
- https://www.google.com/search?q=mixed+precision+FP16+BF16+deep+learning+memory+speed+optimization
- https://www.google.com/search?q=GradScaler+gradient+scaling+AMP+PyTorch+example