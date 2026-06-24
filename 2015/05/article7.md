# NumPy 基礎：向量運算

## 為何使用 NumPy

Python 的列表雖然靈活，但處理大規模數值計算時效率較低。NumPy 提供了高效的陣列物件和向量化運算，大幅提升效能。

## 創建陣列

```python
import numpy as np

# 從列表創建
a = np.array([1, 2, 3, 4, 5])
print(a)  # [1 2 3 4 5]

# 特殊陣列
zeros = np.zeros((3, 3))      # 3x3 零矩陣
ones = np.ones((2, 4))        # 2x4 統一矩陣
identity = np.eye(4)          # 4x4 單位矩陣
range_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1]
```

## 基本運算

```python
a = np.array([1, 2, 3, 4, 5])
b = np.array([2, 3, 4, 5, 6])

# 元素級別運算
print(a + b)   # [3, 5, 7, 9, 11]
print(a - b)   # [-1, -1, -1, -1, -1]
print(a * b)   # [2, 6, 12, 20, 30]
print(a / b)   # [0.5, 0.666, 0.75, 0.8, 0.833]
print(a ** 2)  # [1, 4, 9, 16, 25]

# 標量運算
print(a * 2)   # [2, 4, 6, 8, 10]
print(a + 10)  # [11, 12, 13, 14, 15]
```

## 索引和切片

```python
a = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

print(a[2])      # 2
print(a[2:5])     # [2, 3, 4]
print(a[:5])      # [0, 1, 2, 3, 4]
print(a[5:])      # [5, 6, 7, 8, 9]
print(a[::2])     # [0, 2, 4, 6, 8]（每兩個取一個）
print(a[::-1])    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]（反轉）
```

## 多維陣列

```python
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print(matrix[0])          # [1, 2, 3]
print(matrix[0, 0])       # 1
print(matrix[:, 0])       # [1, 4, 7]
print(matrix[1:, 1:])     # [[5, 6], [8, 9]]
```

## 通用函式

```python
a = np.array([1, 4, 9, 16])

print(np.sqrt(a))  # [1, 2, 3, 4]
print(np.log(a))   # [0, 1.386, 2.197, 2.773]
print(np.exp(a))   # [2.718, 54.598, 8103, 8886110]
print(np.sin(a))   # 正弦值
```

## 聚合函式

```python
a = np.array([1, 2, 3, 4, 5])

print(np.sum(a))    # 15
print(np.min(a))    # 1
print(np.max(a))    # 5
print(np.mean(a))   # 3.0
print(np.std(a))    # 標準差
print(np.var(a))    # 變異數
print(np.median(a)) # 3.0

# 軸向運算
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(np.sum(matrix, axis=0))  # [5, 7, 9]（按列）
print(np.sum(matrix, axis=1))  # [6, 15]（按行）
```

## 廣播

NumPy 可以自動處理形狀不同的陣列運算：

```python
a = np.array([[1, 2, 3], [4, 5, 6]])
b = np.array([1, 2, 3])

# b 會廣播到每行
print(a + b)
# [[2, 4, 6],
#  [5, 7, 9]]
```

## 矩陣運算

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(np.dot(A, B))      # 矩陣乘法
print(A @ B)             # Python 3.5+ 的 @ 運算子

# 更多矩陣操作
print(np.linalg.inv(A))  # 反矩陣
print(np.linalg.det(A))  # 行列式
print(np.linalg.eigvals(A))  # 特徵值
```

## 結論

NumPy 是 Python 資料科學生態的基礎。掌握好向量運算和陣列操作，對後續學習 Pandas、機器學習等內容至關重要。