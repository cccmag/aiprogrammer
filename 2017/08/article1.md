# NumPy 陣列操作

## 陣列基礎

```python
import numpy as np

# 創建陣列
a = np.array([1, 2, 3, 4, 5])
b = np.array([[1, 2, 3], [4, 5, 6]])

print(a.shape)  # (5,)
print(b.shape)  # (2, 3)
```

## 創建陣列

```python
# 從列表
arr = np.array([1, 2, 3])

# 零矩陣
zeros = np.zeros((3, 3))

# 單位矩陣
identity = np.eye(3)

# 範圍
range_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]

# 等差
linspace = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1]

# 隨機
random = np.random.rand(3, 3)
random_int = np.random.randint(0, 10, (3, 3))
```

## 索引與切片

```python
a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 基本索引
print(a[0])        # 第一列
print(a[0, 0])     # 第一列第一個元素

# 切片
print(a[0:2])      # 前兩列
print(a[:, 0])     # 第一欄
print(a[1:, :-1])  # 第二列之後，倒數第一欄之前

# 布林索引
print(a[a > 5])    # 大於5的元素
```

## 陣列運算

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 元素級運算
print(a + b)   # [5, 7, 9]
print(a * b)   # [4, 10, 18]
print(a ** 2)  # [1, 4, 9]

# 矩陣乘法
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(np.dot(A, B))
print(A @ B)  # Python 3.5+
```

## 聚合函數

```python
a = np.array([[1, 2, 3], [4, 5, 6]])

print(np.sum(a))       # 總和
print(np.sum(a, axis=0))  # 按欄
print(np.sum(a, axis=1))  # 按列

print(np.mean(a))      # 平均
print(np.max(a))       # 最大
print(np.min(a))       # 最小
print(np.std(a))       # 標準差
```

## 形狀操作

```python
a = np.array([[1, 2, 3], [4, 5, 6]])

# reshape
print(a.reshape(3, 2))

# flatten
print(a.flatten())

# transpose
print(a.T)

# 新軸
a = np.array([1, 2, 3])
print(a[:, np.newaxis])  # (3,) -> (3, 1)
```

## 廣播

NumPy 自動擴展小型陣列以進行運算。

```python
A = np.array([[1, 2, 3], [4, 5, 6]])
B = np.array([10, 20, 30])

print(A + B)  # 廣播 B 到每列
```

## 複製與檢視

```python
a = np.array([1, 2, 3])

# 檢視（共享資料）
b = a[:2]
print(b.base is a)  # True

# 複製（獨立資料）
c = a.copy()
print(c.base is None)  # True
```

## 總結

NumPy 是 Python 數值計算的基礎。正確的索引與廣播操作是高效資料處理的關鍵。