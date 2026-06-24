# NumPy 陣列運算基礎

## ndarray — 核心資料結構

NumPy 的核心是 ndarray（N-dimensional array）物件。與 Python 原生的 list 不同，ndarray 的所有元素必須是相同型別，這使得 NumPy 可以進行高效的向量化運算。

### 建立陣列

```python
import numpy as np

# 從 list 建立
a = np.array([1, 2, 3, 4, 5])

# 二維陣列
b = np.array([[1, 2], [3, 4], [5, 6]])

# 特殊陣列
zeros = np.zeros((3, 4))      # 全零陣列
ones = np.ones((2, 3))        # 全一陣列
empty = np.empty((2, 2))      # 未初始化陣列
eye = np.eye(3)               # 單位矩陣
```

### 陣列屬性

```python
print(a.shape)     # (5,)
print(b.shape)     # (3, 2)
print(a.dtype)     # int64
print(b.ndim)      # 2
print(a.size)      # 5
```

## 向量化運算

向量化是 NumPy 的核心優勢。與 Python 迴圈相比，向量化運算不僅程式碼更簡潔，執行速度也快數十倍到數百倍。

```python
arr = np.array([1, 2, 3, 4, 5])

# 向量化算術
print(arr + 10)       # [11 12 13 14 15]
print(arr * 2)        # [2 4 6 8 10]
print(arr ** 2)       # [1 4 9 16 25]

# 陣列間運算
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b)          # [5 7 9]
print(a * b)          # [4 10 18]

# 通用函式 (ufunc)
print(np.sin(arr))
print(np.exp(arr))
print(np.sqrt(arr))
```

## 索引與切片

NumPy 的索引與 Python list 類似，但更強大：

```python
arr = np.array([10, 20, 30, 40, 50])
print(arr[0])         # 10
print(arr[-1])        # 50
print(arr[1:4])       # [20 30 40]

# 多維陣列索引
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d[0, 1])    # 2
print(arr2d[:, 0])    # [1 4 7]  第一列
print(arr2d[0, :])    # [1 2 3]  第一行
```

## 廣播機制

廣播（Broadcasting）是 NumPy 最強大的特性之一。它允許不同形狀的陣列之間進行運算：

```python
# 純量與陣列
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr + 100)

# 一維與二維
row = np.array([10, 20, 30])
print(arr + row)      # 將 row 廣播到每一行
```

## 重塑與轉置

```python
arr = np.arange(12)
print(arr.reshape(3, 4))    # 改為 3x4 矩陣
print(arr.reshape(2, -1))   # -1 自動計算

# 轉置
matrix = np.array([[1, 2], [3, 4]])
print(matrix.T)
```

## 聚合運算

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.sum())          # 21
print(arr.mean())         # 3.5
print(arr.sum(axis=0))    # [5 7 9]   沿行方向加總
print(arr.sum(axis=1))    # [6 15]    沿列方向加總
```

---

**延伸閱讀**
- [NumPy 快速入門](https://www.google.com/search?q=NumPy+quickstart+tutorial)
- [NumPy 廣播機制說明](https://www.google.com/search?q=NumPy+broadcasting+explained)
