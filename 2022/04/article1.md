# Tensor 基礎與裝置管理

## 張量的建立

PyTorch 的 Tensor 可以透過多種方式建立：

```python
import torch

# 從資料建立
a = torch.tensor([[1, 2], [3, 4]])

# 從 NumPy 陣列轉換
import numpy as np
b = torch.from_numpy(np.array([1, 2, 3]))

# 特殊初始化
c = torch.zeros(3, 4)       # 全零
d = torch.ones(2, 5)        # 全一
e = torch.randn(3, 3)       # 標準常態分佈
f = torch.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
g = torch.linspace(0, 1, 5) # [0, 0.25, 0.5, 0.75, 1.0]
```

## 張量的屬性

每個 Tensor 都有以下屬性：
- `shape` / `size()`：張量的形狀
- `dtype`：資料型別（float32、int64 等）
- `device`：所在的裝置（CPU 或 GPU）
- `requires_grad`：是否需要計算梯度

## 裝置管理

PyTorch 支援透明的 CPU/GPU 切換：

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x = torch.randn(100, 100).to(device)
```

多 GPU 環境下可以使用：
```python
if torch.cuda.device_count() > 1:
    model = nn.DataParallel(model)
```

## 資料型別轉換

```python
x = torch.tensor([1, 2, 3], dtype=torch.float32)
y = x.to(torch.int64)
z = x.half()  # float16，用於混合精度訓練
```

## 記憶體管理

- `torch.cuda.empty_cache()`：釋放未使用的快取記憶體
- `del variable`：刪除變數以釋放記憶體
- 使用 `pin_memory=True` 加速 CPU→GPU 傳輸

## 常見陷阱

1. `torch.tensor` vs `torch.Tensor`：前者推斷 dtype，後者預設 float32
2. In-place 操作（如 `x.add_(y)`）會影響 Autograd 的計算圖
3. 大型 Tensor 的拷貝開銷很大，盡量使用 view 或切片

## 參考資料

- Tensor 文件：https://pytorch.org/docs/stable/tensors.html
- 裝置管理指南：https://pytorch.org/docs/stable/notes/cuda.html
- 型別轉換：https://pytorch.org/docs/stable/tensor_attributes.html
