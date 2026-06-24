# NumPy 快速上手

## 簡介

NumPy 是 Python 數值計算的核心庫，提供了高效的多維陣列对象和豐富的數學函式。

## 安裝與基本使用

```bash
pip install numpy
```

```python
import numpy as np
print(np.__version__)
```

## 陣列建立

### 基本建立方式

```python
import numpy as np

# 從列表建立
a = np.array([1, 2, 3, 4, 5])
print(f"array: {a}")

# 零陣列
zeros = np.zeros(5)
print(f"zeros: {zeros}")  # [0. 0. 0. 0. 0.]

ones = np.ones((2, 3))
print(f"ones:\n{ones}")

# 範圍陣列
range_arr = np.arange(0, 10, 2)  # 0, 2, 4, 6, 8
print(f"arange: {range_arr}")

# 等差陣列
linspace = np.linspace(0, 1, 5)  # 0, 0.25, 0.5, 0.75, 1
print(f"linspace: {linspace}")

# 單位矩陣
eye = np.eye(3)
print(f"eye:\n{eye}")
```

### 亂數陣列

```python
np.random.seed(42)

# 隨機浮點數 [0, 1)
rand = np.random.rand(3, 4)
print(f"rand:\n{rand}")

# 隨機整數
randint = np.random.randint(1, 10, (3, 3))
print(f"randint:\n{randint}")

# 常態分布
normal = np.random.normal(0, 1, 100)
print(f"normal mean: {normal.mean():.4f}")
```

## 陣列屬性

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

print(f"shape: {a.shape}")     # (2, 3)
print(f"ndim: {a.ndim}")      # 2
print(f"size: {a.size}")      # 6
print(f"dtype: {a.dtype}")    # int64
```

## 陣列索引與切片

```python
a = np.array([0, 1, 2, 3, 4, 5])

# 基本索引
print(a[0])    # 0
print(a[-1])   # 5

# 切片
print(a[1:4])  # [1, 2, 3]
print(a[::2])  # [0, 2, 4]  間隔2
print(a[::-1]) # [5, 4, 3, 2, 1, 0]  反向

# 二維陣列
b = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

print(b[0])      # [1, 2, 3]
print(b[0, 0])   # 1
print(b[1:, :2])  # [[4, 5], [7, 8]]
```

## 陣列運算

### 基本運算

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 元素 wise 運算
print(f"a + b = {a + b}")   # [5, 7, 9]
print(f"a * b = {a * b}")   # [4, 10, 18]
print(f"a - b = {a - b}")   # [-3, -3, -3]
print(f"a / b = {a / b}")   # [0.25, 0.4, 0.5]

# 純量運算
print(f"a * 2 = {a * 2}")   # [2, 4, 6]
print(f"a ** 2 = {a ** 2}")  # [1, 4, 9]
```

### 矩陣乘法

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 元素 wise 乘法
print(A * B)

# 矩陣乘法
C = np.dot(A, B)
print(f"A @ B:\n{C}")

# 或使用 @
print(A @ B)
```

## 常用函式

### 統計函式

```python
a = np.array([1, 2, 3, 4, 5])

print(f"sum: {np.sum(a)}")
print(f"mean: {np.mean(a)}")
print(f"std: {np.std(a)}")
print(f"min: {np.min(a)}")
print(f"max: {np.max(a)}")
print(f"argmax: {np.argmax(a)}")  # 最大值索引
```

### 陣列形狀操作

```python
a = np.arange(12)  # [0, 1, ..., 11]

# 重塑
b = a.reshape(3, 4)
print(f"reshaped:\n{b}")

# 攤平
c = b.flatten()
print(f"flattened: {c}")

# 轉置
d = b.T
print(f"transposed:\n{d}")
```

### 合併與分割

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 合併
concat = np.concatenate([a, b])
print(f"concat: {concat}")  # [1, 2, 3, 4, 5, 6]

vstack = np.vstack([a, b])  # 垂直合併
print(f"vstack:\n{vstack}")

hstack = np.hstack([a, b])  # 水平合併
print(f"hstack: {hstack}")

# 分割
arr = np.arange(10)
split = np.split(arr, 5)  # 分成5等份
print(f"split: {split}")
```

## 廣播（Broadcasting）

NumPy 自動擴展小型陣列以進行運算：

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

b = np.array([10, 20, 30])

# b 會被廣播為 [[10, 20, 30], [10, 20, 30]]
print(a + b)

# 純量自動廣播
print(a + 1)
```

## 實際應用

### 線性迴歸

```python
import numpy as np

# 資料
X = np.array([[1, 1], [1, 2], [1, 3], [1, 4]])  # 加一列1
y = np.array([2, 4, 5, 7])

# 最小二乘法
XtX = X.T @ X
XtX_inv = np.linalg.inv(XtX)
Xty = X.T @ y
w = XtX_inv @ Xty

print(f"係數: {w}")  # w[0]=b, w[1]=m  y = b + mx
```

### 歐氏距離

```python
def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

p1 = np.array([1, 2, 3])
p2 = np.array([4, 6, 3])

print(f"Distance: {euclidean_distance(p1, p2):.4f}")
```

## 練習題

1. 建立一個 5x5 的單位矩陣
2. 計算兩個向量 [1, 2, 3] 和 [4, 5, 6] 的內積
3. 將一維陣列 [1, 2, 3, 4, 5, 6] 轉換為 2x3 矩陣並計算轉置
4. 計算矩陣 [[1, 2], [3, 4]] 和其轉置的乘積