# 模型架構優化

## 可呼叫的 Module

將模型改為可呼叫類以提高效能：

```python
class OptimizedModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Linear(256, 10)
        )
    
    def forward(self, x):
        return self.layers(x)

# 錯誤：每次創建新模組
if i % 2 == 0:
    layer = nn.Linear(768, 256).cuda()
else:
    layer = nn.Linear(768, 256).cuda()

# 正確：在 __init__ 中創建
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer = nn.Linear(768, 256)  # 只創建一次
```

## 梯度檢查點 (Gradient Checkpointing)

用時間換取記憶體：

```python
from torch.utils.checkpoint import checkpoint_sequential

class CheckpointedModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.Linear(512, 512) for _ in range(12)
        ])
    
    def forward(self, x):
        # 將模型分為多個區塊，每個區塊使用檢查點
        segments = 3
        segment_size = len(self.layers) // segments
        
        for i in range(segments):
            start = i * segment_size
            end = start + segment_size if i < segments - 1 else len(self.layers)
            segment = nn.Sequential(*self.layers[start:end])
            x = checkpoint_sequential(segment, segment_size, x)
        
        return x
```

## 移除不必要的張量

```python
# 訓練後刪除不需要的張量
del intermediate_activation
torch.cuda.empty_cache()
```

## 使用更高效的模組

```python
# 原始：用兩個 Linear 層
class OriginalAttention(nn.Module):
    def __init__(self):
        super().__init__()
        self.q = nn.Linear(512, 512)
        self.k = nn.Linear(512, 512)
        self.v = nn.Linear(512, 512)
    
    def forward(self, x):
        Q = self.q(x)
        K = self.k(x)
        V = self.v(x)
        # ...

# 優化：使用一個 Linear 層，然後分割
class OptimizedAttention(nn.Module):
    def __init__(self):
        super().__init__()
        self.qkv = nn.Linear(512, 512 * 3)
    
    def forward(self, x):
        qkv = self.qkv(x)
        Q, K, V = qkv.chunk(3, dim=-1)
        # ...
```

## 避免 Python 迴圈

```python
# 緩慢：Python 迴圈
outputs = []
for i in range(len(inputs)):
    outputs.append(model(inputs[i]))

# 快速：批次處理
outputs = model(inputs)
```

## 預計算常量

```python
# 將常量移到 GPU 後固定
constants = torch.randn(1000, 1000).cuda()
constants = constants.detach()  # 不需要梯度
constants = constants.requires_grad_(False)
```

## 參考資源

- https://www.google.com/search?q=model+architecture+optimization+PyTorch+memory+efficiency+tutorial+2020
- https://www.google.com/search?q=gradient+checkpointing+memory+tradeoff+implementation+PyTorch
- https://www.google.com/search?q=Neural+network+efficiency+optimization+techniques+GPU+memory