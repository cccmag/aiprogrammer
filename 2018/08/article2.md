# 張量操作完全指南

## 1. 張量基礎

### 建立張量

```python
import torch

# 從 Python list
a = torch.tensor([1, 2, 3])

# 初始化
zeros = torch.zeros(3, 4)      # 全零
ones = torch.ones(3, 4)        # 全一
rand = torch.rand(3, 4)        # 均勻分佈 [0, 1)
randn = torch.randn(3, 4)      # 標準常態分佈
empty = torch.empty(3, 4)      # 未初始化
full = torch.full((3, 4), 7.0) # 填充固定值
```

### 張量屬性

```python
x = torch.randn(3, 4, 5)
print(x.shape)     # torch.Size([3, 4, 5])
print(x.dtype)     # torch.float32
print(x.device)    # cpu
print(x.ndim)      # 3 (維度)
```

## 2. 張量運算

### 基本運算

```python
a = torch.randn(3, 4)
b = torch.randn(3, 4)

c = a + b              # 加法
c = torch.add(a, b)    # 等價

# 原地運算（結尾有底線）
a.add_(b)              # a 會被修改

# 減法、乘法、除法
c = a - b
c = a * b              # 元素級乘法
c = a / b
c = torch.matmul(a, b) # 矩陣乘法
```

### 索引與切片

```python
x = torch.randn(5, 6, 7)

x[0]                   # 第一個元素
x[:, 1]                # 所有維度的第二列
x[0, 2:4, :]           # 多維切片
x[x > 0]               # 條件索引
```

### 維度操作

```python
x = torch.randn(3, 4)

x.view(12)             # 展平為一維
x.view(-1, 6)          #自動推導第一維
x.reshape(12)          # 類似 view（可能複製）
x.squeeze()            # 移除 size=1 的維度
x.unsqueeze(0)         # 在位置 0 新增維度
x.t()                  # 轉置（僅適用於 2D）
x.permute(2, 0, 1)    # 任意維度重排
```

### 拼接與分割

```python
a = torch.randn(3, 4)
b = torch.randn(3, 4)

# 拼接
c = torch.cat([a, b], dim=0)   # (6, 4)
c = torch.cat([a, b], dim=1)   # (3, 8)

# 分離
 chunks = torch.chunk(c, 3, dim=0)
 split = torch.split(c, [2, 2], dim=0)
```

## 3. 與 NumPy 轉換

```python
import numpy as np

# Tensor -> NumPy
x = torch.randn(3, 4)
y = x.numpy()          # 共享記憶體

# NumPy -> Tensor
z = np.random.randn(3, 4)
w = torch.from_numpy(z)  # 共享記憶體
```

## 4. GPU 加速

```python
# 檢查 GPU
print(torch.cuda.is_available())

# 移到 GPU
x = x.cuda()
x = x.to('cuda')

# 移回 CPU
x = x.cpu()

# 指定 GPU
x = x.to(torch.device('cuda:0'))
```

## 5. 聚合運算

```python
x = torch.randn(3, 4)

x.sum()                 # 所有元素求和
x.sum(dim=0)            # 按維度求和
x.mean()                # 平均值
x.mean(dim=1)
x.std()                 # 標準差
x.max()                 # 最大值
x.max(dim=1)            # 最大值及索引
x.argmax()              # 最大值索引
x.min()                 # 最小值
x.prod()                # 所有元素乘積
```

## 6. 廣播機制

```python
# 自動廣播
a = torch.randn(3, 4)
b = torch.randn(4)

# b 會被廣播為 (1, 4) 再與 a 計算
c = a + b
```

## 7. 小結

PyTorch 張量操作與 NumPy 非常相似，對 Python 程式設計師非常友好。熟練掌握這些操作是深度學習開發的基礎。

---

**參考資料**
- [PyTorch Tensor Tutorial](https://www.google.com/search?q=PyTorch+tensor+tutorial+basics)
- [Tensor Operations Guide](https://www.google.com/search?q=pytorch+tensor+operations+guide)