# NumPy 效能優化

## NumPy 概述

NumPy 是 Python 數值計算的基礎，提供了高效的多維陣列與矩陣運算功能。

## 基本陣列操作

```python
import numpy as np

# 建立陣列
a = np.array([1, 2, 3, 4, 5])
b = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
c = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1]

# 多維陣列
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
```

## 向量化運算

NumPy 的向量化比 Python 迴圈快得多：

```python
import numpy as np
import time

# Python 迴圈
start = time.time()
result = sum(x**2 for x in range(10000))
python_time = time.time() - start

# NumPy 向量化
start = time.time()
arr = np.arange(10000)
result = np.sum(arr**2)
numpy_time = time.time() - start

print(f"Python: {python_time:.4f}s")
print(f"NumPy:  {numpy_time:.4f}s")
print(f"加速比: {python_time/numpy_time:.1f}x")
```

## 廣播机制

NumPy 自動擴展維度進行運算：

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

b = np.array([10, 20, 30])

# b 會廣播到每一列
print(a + b)
# [[11, 22, 33],
#  [14, 25, 36]]
```

## 矩陣運算

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 元素級別乘法
print(A * B)

# 矩陣乘法
print(np.matmul(A, B))
print(A @ B)  # Python 3.5+ 簡便語法
```

## 索引與切片

```python
arr = np.arange(12).reshape(3, 4)

# 基本切片
print(arr[1:, 2:])

# 布林索引
print(arr[arr > 5])

# Fancy indexing
print(arr[[0, 2], [1, 3]])  # (0,1) 和 (2,3) 位置
```

## 統計函數

```python
arr = np.arange(12).reshape(3, 4)

print(np.mean(arr))      # 平均值
print(np.std(arr))       # 標準差
print(np.sum(arr, axis=0))   # 按列求和
print(np.max(arr, axis=1))   # 每行最大值
```

## 效能技巧

### 避免複製

```python
# 不好：創建不必要的副本
b = a[:]
b[:] = 1

# 好：使用視圖
view = a[1:3]
view[:] = 1
```

### 預先配置記憶體

```python
# 預先分配結果陣列
result = np.empty(len(data))
for i, val in enumerate(data):
    result[i] = val * 2
```

### 使用 einsum

```python
A = np.random.rand(100, 100)
B = np.random.rand(100, 100)

# 傳統方式
C = np.matmul(A, B)

# einsum 可能更快
C = np.einsum('ij,jk->ik', A, B)
```

## ufunc 進階用法

```python
# 自動 ufunc
np.add.at(arr, indices, values)  # 原地新增
np.multiply.at(arr, indices, values)

# 歸約
arr = np.arange(1, 6)
print(np.add.reduce(arr))  # 1+2+3+4+5 = 15
print(np.add.accumulate(arr))  # [1, 3, 6, 10, 15]
```

## 參考資源

- https://www.google.com/search?q=NumPy+performance+optimization+tutorial+vectorization+2019
- https://www.google.com/search?q=NumPy+broadcasting+matrix+operations+einsum+2019
- https://www.google.com/search?q=NumPy+avoid+copy+memory+efficiency+Python+2019