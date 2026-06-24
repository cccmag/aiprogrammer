# 文章 2：NumPy 陣列操作

## 前言

NumPy 是 Python 數值計算的基礎套件，提供了高效的多維陣列物件。本章節介紹 NumPy 的基本操作，為機器學習打下基礎。

## 創建陣列

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.zeros((3, 4))      # 3x4 零矩陣
c = np.ones((2, 3))       # 2x3 一矩陣
d = np.random.rand(2, 2)  # 隨機矩陣
e = np.arange(0, 10, 2)   # [0, 2, 4, 6, 8]
```

## 陣列屬性

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape)   # (2, 3)
print(arr.ndim)    # 2
print(arr.size)    # 6
print(arr.dtype)   # int64
```

## 基本運算

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(a + b)   # [5, 7, 9]
print(a * b)   # [4, 10, 18]
print(a * 2)   # [2, 4, 6]
```

## 矩陣乘法

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

C = A @ B          # 矩陣乘法
D = np.dot(A, B)   # 同上
E = A * B          # 元素對應相乘
```

## 索引與切片

```python
arr = np.array([0, 1, 2, 3, 4, 5])

print(arr[2])      # 2
print(arr[1:4])    # [1, 2, 3]
print(arr[:3])     # [0, 1, 2]
print(arr[::2])    # [0, 2, 4]

# 二維索引
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix[0, 0])     # 1
print(matrix[:, 1])     # [2, 5, 8]
print(matrix[1:, :2])   # [[4, 5], [7, 8]]
```

## 形態變換

```python
arr = np.array([[1, 2], [3, 4], [5, 6]])
print(arr.reshape(2, 3))
# [[1, 2, 3],
#  [4, 5, 6]]

print(arr.flatten())  # [1, 2, 3, 4, 5, 6]
```

## 統計函數

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(np.mean(arr))        # 3.5
print(np.sum(arr, axis=0)) # [5, 7, 9]
print(np.max(arr, axis=1)) # [3, 6]
print(np.std(arr))         # 標準差
```

## 廣播（Broadcasting）

NumPy 自動擴展小型陣列以匹配大型陣列：

```python
A = np.array([[1, 2, 3], [4, 5, 6]])
b = np.array([1, 2, 3])

print(A + b)  # [[2, 4, 6], [5, 7, 9]]
```

## 總結

NumPy 是機器學習的基礎工具。熟練掌握陣列操作將使後續的矩陣運算與模型實現更加順暢。

## 延伸閱讀

- https://www.google.com/search?q=NumPy+tutorial+array+operations
- https://www.google.com/search?q=NumPy+broadcasting+explained