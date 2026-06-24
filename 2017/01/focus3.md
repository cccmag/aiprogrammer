# 科學計算生態系：NumPy、SciPy、Pandas 與 Matplotlib

## 前言

Python 之所以成為資料科學領域的首選語言，離不開其強大的科學計算生態系。NumPy、SciPy、Pandas 和 Matplotlib 這些庫构成了資料處理和分析的基石。本篇文章將介紹這些工具的核心概念和使用方法。

## NumPy：數值計算的基礎

### 為什麼需要 NumPy？

Python 的內建列表在科學計算中存在效能問題：

```python
# Python 列表：效能低
a = list(range(1000000))
b = list(range(1000000))
c = [x + y for x, y in zip(a, b)]  # 慢！

# NumPy 陣列：效能高
import numpy as np
a = np.arange(1000000)
b = np.arange(1000000)
c = a + b  # 快！向量化操作
```

### ndarray 物件

NumPy 的核心是 `ndarray`（N 維陣列）：

```python
import numpy as np

# 創建陣列
a = np.array([1, 2, 3, 4, 5])
b = np.zeros((3, 4))       # 3x4 的零矩陣
c = np.ones((2, 3))        # 2x3 的一矩陣
d = np.arange(0, 10, 2)    # [0, 2, 4, 6, 8]
e = np.linspace(0, 1, 5)   # [0, 0.25, 0.5, 0.75, 1]
f = np.random.rand(3, 3)   # 3x3 隨機矩陣

# 陣列屬性
print(a.shape)   # (5,)
print(a.ndim)    # 1
print(a.dtype)   # int64
print(a.size)    # 5
```

### 基本運算

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 元素級別運算
print(a + b)     # [5, 7, 9]
print(a - b)     # [-3, -3, -3]
print(a * b)     # [4, 10, 18]
print(a / b)     # [0.25, 0.4, 0.5]

# 聚合函數
print(a.sum())   # 6
print(a.mean())  # 2.0
print(a.max())   # 3
print(a.min())   # 1
print(a.std())   # 標準差

# 矩陣運算
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(np.dot(A, B))              # 矩陣乘法
print(A @ B)                     # Python 3.5+ 的 @ 運算子
```

### 索引與切片

```python
a = np.arange(12).reshape(3, 4)
print(a)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

print(a[1, 2])        # 6（第二行、第三列）
print(a[0:2, 1:3])    # 切片
print(a[a > 5])       # 條件索引：[6, 7, 8, 9, 10, 11]
```

## SciPy：科學計算工具箱

### SciPy 簡介

SciPy 是基於 NumPy 的科學計算庫，提供了更多高等數學功能：

```python
from scipy import stats, optimize, integrate, linalg

# 統計分析
data = np.random.normal(0, 1, 1000)
print(stats.norm.mean(data))     # 均值
print(stats.norm.std(data))      # 標準差
print(stats.norm.pdf(0))         # 機率密度函數

# 最佳化
def f(x):
    return x**2 + 2*x + 1
result = optimize.minimize_scalar(f)
print(result.x)                  # 最小值點：-1

# 數值積分
def f(x):
    return np.exp(-x**2)
integral, error = integrate.quad(f, -np.inf, np.inf)
print(f"Integral: {integral}, Error: {error}")

# 線性代數
A = np.array([[1, 2], [3, 4]])
print(linalg.det(A))             # 行列式：-2
print(linalg.inv(A))             # 逆矩陣
```

### 常用 SciPy 模組

| 模組 | 功能 |
|------|------|
| `scipy.stats` | 統計分析、機率分佈 |
| `scipy.optimize` | 函數最佳化 |
| `scipy.integrate` | 數值積分 |
| `scipy.linalg` | 線性代數 |
| `scipy.fftpack` | 傅立葉變換 |
| `scipy.signal` | 訊號處理 |
| `scipy.ndimage` | 影像處理 |

## Pandas：資料分析的瑞士刀

### Series 與 DataFrame

Pandas 提供了兩種主要的資料結構：

```python
import pandas as pd

# Series：一維標記陣列
s = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s)

# DataFrame：二維表格資料
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'score': [85.5, 90.0, 78.5]
})
print(df)
```

### 資料操作

```python
# 讀取 CSV
df = pd.read_csv('data.csv')

# 檢視前幾行
print(df.head())

# 基本統計
print(df.describe())

# 選擇列
print(df['name'])
print(df[['name', 'score']])

# 條件篩選
print(df[df['age'] > 25])

# 新增列
df['passed'] = df['score'] >= 60

# 刪除列
df = df.drop('passed', axis=1)
```

### 群組與聚合

```python
# 群組操作
grouped = df.groupby('department').agg({
    'salary': ['mean', 'max', 'min'],
    'performance': 'sum'
})

# 處理缺失值
df.dropna()              # 刪除缺失值
df.fillna(value=0)       # 填補缺失值
df.isnull().sum()        # 統計缺失值數量
```

### 資料合併

```python
# 連接兩個 DataFrame
result = pd.concat([df1, df2])

# 合併（類似 SQL JOIN）
merged = pd.merge(df1, df2, on='key')

# join：依索引合併
joined = df1.join(df2, how='inner')
```

## Matplotlib：資料視覺化

### 基本繪圖

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.title('Sin Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True)
plt.show()
```

### 多圖比較

```python
x = np.linspace(0, 2 * np.pi, 100)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title('sin(x)')

axes[0, 1].plot(x, np.cos(x))
axes[0, 1].set_title('cos(x)')

axes[1, 0].plot(x, np.tan(x))
axes[1, 0].set_title('tan(x)')
axes[1, 0].set_ylim(-5, 5)

axes[1, 1].plot(x, x**2)
axes[1, 1].set_title('x^2')

plt.tight_layout()
plt.show()
```

### 圖表類型

```python
# 散點圖
plt.scatter(x, y, c=z, cmap='viridis')
plt.colorbar()

# 柱狀圖
plt.bar(categories, values)

# 直方圖
plt.hist(data, bins=30)

# 箱線圖
plt.boxplot([data1, data2, data3])
```

### 樣式與自訂

```python
# 設定樣式
plt.style.use('seaborn-v0_8-darkgrid')

# 自訂顏色
plt.plot(x, y, color='#FF5733', linewidth=2, linestyle='--')

# 添加標注
plt.annotate('Peak', xy=(np.pi/2, 1), xytext=(np.pi, 0.8),
             arrowprops=dict(arrowstyle='->', color='red'))

# 圖例
plt.plot(x, np.sin(x), label='sin')
plt.plot(x, np.cos(x), label='cos')
plt.legend()
```

## 結論

Python 的科學計算生態系非常完善：

- **NumPy** 提供了高效的陣列運算和基礎數學函數
- **SciPy** 擴展了高等科學計算功能（統計、最佳化、積分等）
- **Pandas** 讓資料處理和分析變得優雅
- **Matplotlib** 提供了豐富的資料視覺化能力

這些工具的組合使得 Python 成為資料科學領域最強大的語言之一。掌握這些工具的基礎使用方法，將為後續的機器學習和深度學習學習打下堅實的基礎。

---

## 延伸閱讀

- [NumPy 官方文檔](https://www.google.com/search?q=NumPy+tutorial+documentation)
- [Pandas 官方文檔](https://www.google.com/search?q=Pandas+tutorial+data+analysis)
- [Matplotlib 官方文檔](https://www.google.com/search?q=Matplotlib+tutorial+python+plotting)
- [SciPy 官方文檔](https://www.google.com/search?q=SciPy+tutorial+scientific+python)

---

*本篇文章為「AI 程式人雜誌 2017 年 1 月號」焦點系列之一。*