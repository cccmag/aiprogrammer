# NumPy 廣播機制

## 廣播的直覺理解

NumPy 的廣播（Broadcasting）是其向量化運算中最強大的特性之一。它允許不同形狀的陣列進行算術運算，而無需手動建立相同形狀的陣列副本。

```python
import numpy as np

# 基本廣播：純量 + 陣列
a = np.array([1, 2, 3])
b = a + 5  # [6, 7, 8]
```

直覺上，你可以把廣播理解為「小陣列沿著缺失的維度自動擴展」。

## 廣播規則

NumPy 的廣播遵循兩條簡單規則：

**規則一**：如果兩個陣列的維度數不同，則在較小陣列的形狀前面補 1。

**規則二**：如果兩個陣列在某個維度上的大小不一致，但其中一個大小為 1，則該維度可以擴展。

```
陣列 A：    3 x 4
陣列 B：        4    → 補 1 → 1 x 4
結果：      3 x 4

陣列 A：    3 x 1
陣列 B：        4    → 補 1 → 1 x 4
結果：      3 x 4
```

### 合法廣播範例

```python
# 形狀 (3,) + (3,) → (3,)
np.array([1, 2, 3]) + np.array([4, 5, 6])

# 形狀 (3, 1) + (3,) → (3, 3)
# (3, 1) 廣播為 (3, 3)
# (3,) 補 1 為 (1, 3) 再廣播為 (3, 3)
np.array([[1], [2], [3]]) + np.array([4, 5, 6])

# 形狀 (1, 3) + (3, 1) → (3, 3)
np.array([[1, 2, 3]]) + np.array([[4], [5], [6]])
```

### 非法廣播

```python
# 形狀 (3,) + (4,) → 錯誤！
# 維度大小不匹配且均不為 1
np.array([1, 2, 3]) + np.array([4, 5, 6, 7])
```

## 廣播的實際應用

### 標準化（Z-score）

```python
data = np.random.randn(100, 10)  # 100 筆樣本，10 個特徵
mean = data.mean(axis=0)          # 形狀 (10,)
std = data.std(axis=0)            # 形狀 (10,)

# 廣播讓減法自動沿列方向傳播
normalized = (data - mean) / std   # 形狀 (100, 10)
```

### 距離矩陣計算

```python
# 計算點集之間的歐式距離
points = np.random.randn(10, 2)    # 10 個二維點

# 廣播技巧：擴展維度
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
distances = np.sqrt((diff ** 2).sum(axis=2))  # 10 x 10 距離矩陣
```

### 外積運算

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
outer = a[:, np.newaxis] * b[np.newaxis, :]
```

## 效能考量

廣播不涉及實際的資料複製——它只在運算時建立虛擬視圖。這使得廣播在記憶體和計算上都極為高效。

## 延伸閱讀

- [NumPy 廣播官方文件](https://www.google.com/search?q=NumPy+broadcasting+documentation)
- [NumPy 廣播規則](https://www.google.com/search?q=NumPy+broadcasting+rules)
- [Deep NumPy 廣播](https://www.google.com/search?q=NumPy+broadcasting+deep+dive)
