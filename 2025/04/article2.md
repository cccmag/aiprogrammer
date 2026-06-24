# NumPy 陣列建立與操作

## 前言

NumPy 是 Python 資料科學的基礎套件。無論是 Pandas、Scikit-learn 還是 TensorFlow，底層都依賴 NumPy 的陣列結構。掌握 NumPy 陣列的建立與操作，是學習資料分析的必經之路。

## 建立陣列

### 從 Python 序列建立

```python
import numpy as np

# 一維陣列
arr1d = np.array([1, 2, 3, 4, 5])

# 二維陣列
arr2d = np.array([[1, 2, 3], [4, 5, 6]])

# 指定資料型別
arr = np.array([1, 2, 3], dtype=np.float32)
```

### 使用 NumPy 內建函式

```python
# 全零陣列
zeros = np.zeros((3, 4))

# 全一陣列
ones = np.ones((2, 3))

# 單位矩陣
eye = np.eye(4)

# 未初始化陣列
empty = np.empty((2, 2))

# 填充特定值
full = np.full((3, 3), 7)

# 固定間距
arange = np.arange(0, 10, 2)      # [0 2 4 6 8]
linspace = np.linspace(0, 1, 5)   # [0. 0.25 0.5 0.75 1.]
```

### 隨機陣列

```python
np.random.seed(42)  # 固定隨機種子

# 均勻分佈 [0, 1)
rand = np.random.rand(3, 3)

# 標準常態分佈
randn = np.random.randn(4, 4)

# 整數隨機
randint = np.random.randint(0, 100, size=(3, 3))
```

## 陣列操作

### 索引與切片

```python
arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

print(arr[0])          # 第一列
print(arr[:, 0])       # 第一欄
print(arr[0:2, 1:3])   # 子矩陣
print(arr[::-1])       # 反向

# 花式索引 (Fancy Indexing)
indices = [0, 2]
print(arr[indices])     # 選取第 0 和第 2 列

# 布林索引
mask = arr > 5
print(arr[mask])        # 選取大於 5 的元素
```

### 陣列變形

```python
arr = np.arange(12)

print(arr.reshape(3, 4))    # 轉為 3x4
print(arr.reshape(2, -1))   # -1 自動推斷
print(arr.ravel())          # 展平為一維

# 新增 / 移除維度
print(arr[:, np.newaxis].shape)  # (12, 1)
print(np.squeeze(np.zeros((1, 3, 1))).shape)  # (3,)
```

### 合併與分割

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])

print(np.vstack((a, b)))        # 垂直堆疊
print(np.hstack((a, a)))        # 水平堆疊
print(np.concatenate((a, b.T), axis=1))

# 分割
arr = np.arange(12).reshape(3, 4)
print(np.split(arr, 3))         # 水平分割
print(np.hsplit(arr, 2))        # 垂直分割
```

## 實戰範例

### 資料正規化

```python
data = np.array([10, 20, 30, 40, 50])
normalized = (data - data.min()) / (data.max() - data.min())
print(normalized)  # [0. 0.25 0.5 0.75 1.]
```

### 統計運算

```python
data = np.random.randn(1000)
print(f"Mean: {data.mean():.4f}")
print(f"Std:  {data.std():.4f}")
print(f"Min:  {data.min():.4f}")
print(f"Max:  {data.max():.4f}")
```

---

**延伸閱讀**
- [NumPy 官方教學](https://www.google.com/search?q=NumPy+official+quickstart+tutorial)
- [NumPy 陣列操作指南](https://www.google.com/search?q=NumPy+array+manipulation)
