# 張量運算

## 張量創建、操作、變換

張量是 PyTorch 中的基本資料結構，可以看作是 N 維矩陣的推廣。

---

## 張量創建

### 從資料創建

```python
import torch

# 從 Python list
x = torch.tensor([1, 2, 3])

# 從 NumPy 陣列
import numpy as np
arr = np.array([1, 2, 3])
x = torch.from_numpy(arr)

# 拷貝
x = torch.tensor(arr)  # 新記憶體
```

### 特殊張量

```python
# 全零/全一
zeros = torch.zeros(3, 4)
ones = torch.ones(3, 4)

# 單位矩陣
eye = torch.eye(5)

# 區間
linspace = torch.linspace(0, 10, steps=5)  # [0, 2.5, 5, 7.5, 10]

# 隨機
rand = torch.rand(3, 4)      # [0, 1) 均勻分布
randn = torch.randn(3, 4)    # 標準常態分布
randint = torch.randint(0, 10, (3, 4))  # 整數
```

### 設備指定

```python
# CPU 張量（預設）
x = torch.tensor([1, 2, 3])

# GPU 張量
if torch.cuda.is_available():
    x = torch.tensor([1, 2, 3], device='cuda')

# 移動張量
x_gpu = x.to('cuda')
x_cpu = x_gpu.cpu()
```

---

## 張量操作

### 基本算術

```python
a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])

# 加法
c = a + b
c = torch.add(a, b)
c = a.add(b)  # in-place 版本（加底線）

# 減法、乘法、除法類似
```

### 矩陣運算

```python
# 矩陣乘法
A = torch.randn(3, 4)
B = torch.randn(4, 5)
C = torch.matmul(A, B)
C = A @ B

# 元素乘法
C = A * B

# 轉置
A_t = A.t()
```

### 索引和切片

```python
x = torch.randn(3, 4, 5)

# 基本索引
x[0]       # 第一維的第一個
x[0, 1]    # 第一維的第一個，第二維的第二個
x[0, 1, 2] # 具體元素

# 切片
x[1:]      # 除第一個外的所有
x[:2]      # 前兩個
x[::2]     # 跳過一個

# 條件索引
mask = x > 0
positive = x[mask]
```

---

## 張量變換

### 形狀變換

```python
x = torch.randn(3, 4, 5)

# view（共享記憶體）
y = x.view(12, 5)   # 變為 (12, 5)
y = x.view(-1, 5)   # 自動推斷第一維

# reshape（可能拷貝）
y = x.reshape(12, 5)

# squeeze/unsqueeze
x = torch.randn(1, 3, 1, 4)  # (1, 3, 1, 4)
y = x.squeeze()              # (3, 4) - 移除所有 size=1 的維度
y = x.squeeze(0)             # (3, 1, 4) - 移除指定維度

z = torch.randn(3, 4)        # (3, 4)
z = z.unsqueeze(0)           # (1, 3, 4) - 添加維度
```

### 維度變換

```python
# permute - 重新排列維度
x = torch.randn(3, 4, 5)
y = x.permute(2, 0, 1)  # (5, 3, 4)

# transpose - 交換兩個維度
y = x.transpose(0, 2)   # (5, 4, 3)

# contiguous - 確保記憶體連續
x = torch.randn(3, 4)
y = x.t()               # 轉置後不連續
z = y.contiguous()      # 變為連續
```

---

## 張量屬性

```python
x = torch.randn(3, 4)

print(x.shape)     # torch.Size([3, 4])
print(x.dtype)     # torch.float32
print(x.device)   # cpu 或 cuda:0
print(x.ndim)      # 2 (維度數)
print(x.numel())   # 12 (元素總數)
```

---

## 與 NumPy 的轉換

```python
# PyTorch -> NumPy
x = torch.randn(3, 4)
arr = x.numpy()  # 共享記憶體！

# NumPy -> PyTorch
arr = np.random.randn(3, 4)
x = torch.from_numpy(arr)  # 共享記憶體

# 拷貝
arr_copy = x.clone().numpy()
```

---

## 延伸閱讀

- [PyTorch 張量文檔](https://www.google.com/search?q=pytorch+tensor+tutorial)
- [張量操作指南](https://www.google.com/search?q=pytorch+tensor+operations)

---

*本篇文章為「AI 程式人雜誌 2019 年 6 月號」系列文章之一。*