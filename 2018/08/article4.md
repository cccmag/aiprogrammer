# 模型儲存與載入

## 1. 儲存模型的方法

### 方法一：儲存整個模型（不推薦）

```python
# 儲存（包含模型結構和參數）
torch.save(model, 'model.pth')

# 載入（模型結構會自動恢復）
model = torch.load('model.pth')
```

### 方法二：儲存參數（推薦）

```python
# 儲存（只儲存參數，結構需要自己定義）
torch.save(model.state_dict(), 'model_weights.pth')

# 載入（需要先建立模型結構）
model = MyModel()
model.load_state_dict(torch.load('model_weights.pth'))
```

## 2. 完整範例

```python
# 建立模型
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 2)

    def forward(self, x):
        return self.fc(x)

model = Net()

# 儲存
torch.save({
    'epoch': 50,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': 0.05,
}, 'checkpoint.tar')

# 載入
checkpoint = torch.load('checkpoint.tar')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']
```

## 3. 跨設備儲存

```python
# 儲存（不論模型在 CPU 還是 GPU）
torch.save(model.state_dict(), 'weights.pth')

# 載入到 GPU
device = torch.device('cuda')
model.load_state_dict(torch.load('weights.pth'))
model.to(device)

# 載入到 CPU（明確指定）
model.load_state_dict(torch.load('weights.pth', map_location='cpu'))
```

## 4. 只儲存部分參數

```python
# 只儲存某幾層
torch.save({
    'fc1_weights': model.fc1.weight,
    'fc1_bias': model.fc1.bias
}, 'partial_weights.pth')

# 或過濾
weights_to_save = {k: v for k, v in model.state_dict().items() if 'fc' in k}
torch.save(weights_to_save, 'fc_weights.pth')
```

## 5. ONNX 匯出

```python
# 匯出為 ONNX 格式
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model,
    dummy_input,
    'model.onnx',
    export_params=True,
    opset_version=10,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output']
)

# 驗證 ONNX 模型
import onnx
model_onnx = onnx.load('model.onnx')
onnx.checker.check_model(model_onnx)
```

## 6. 最佳實踐

```python
# 建議的儲存方式
def save_checkpoint(model, optimizer, epoch, loss, path):
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss,
    }
    torch.save(checkpoint, path)

def load_checkpoint(model, optimizer, path):
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    return checkpoint['epoch'], checkpoint['loss']
```

## 7. 小結

最佳實踐是儲存 `state_dict()` 而非完整模型，並使用檢查點（checkpoint）機制保存訓練進度。

---

**參考資料**
- [PyTorch Model Saving Guide](https://www.google.com/search?q=PyTorch+save+load+model+tutorial)
- [ONNX Export Guide](https://www.google.com/search?q=PyTorch+ONNX+export+tutorial)