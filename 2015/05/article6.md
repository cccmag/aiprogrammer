# Python 在資料科學的應用

## 資料科學的崛起

2015 年，資料科學正在經歷爆發式增長。Python 凭借其豐富的生態，成為資料科學領域最受歡迎的語言之一。

## Python 資料科學堆疊

### 核心工具

- **NumPy**：數值計算的基礎
- **SciPy**：科學計算工具
- **Pandas**：資料分析
- **Matplotlib**：資料視覺化

### 延伸工具

- **scikit-learn**：機器學習
- **TensorFlow**：深度學習（2015 年 11 月發布）
- **NLTK**：自然語言處理
- **NetworkX**：圖論和網路分析

## NumPy 基礎

NumPy 是 Python 資料科學的基石，提供了高效的多維陣列和數學運算功能：

```python
import numpy as np

# 創建陣列
a = np.array([1, 2, 3, 4, 5])
b = np.array([1, 2, 3, 4, 5])

# 基本運算
print(a + b)    # [2, 4, 6, 8, 10]
print(a * 2)    # [2, 4, 6, 8, 10]
print(a ** 2)    # [1, 4, 9, 16, 25]

# 向量化運算
print(np.sum(a))           # 15
print(np.mean(a))          # 3.0
print(np.std(a))           # 1.41421356...
```

### 多維陣列

```python
import numpy as np

# 2D 陣列
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print(matrix.shape)      # (3, 3)
print(matrix[0])         # [1, 2, 3]
print(matrix[:, 1])      # [2, 5, 8]
print(np.linalg.eigvals(matrix))  # 矩陣特徵值
```

## Pandas 入門

Pandas 提供了 DataFrame 結構，讓處理表格資料變得簡單直觀：

```python
import pandas as pd

# 創建 DataFrame
data = {
    'name': ['張小明', '李小華', '王小美'],
    'age': [28, 35, 24],
    'city': ['台北', '新北', '桃園']
}
df = pd.DataFrame(data)

# 基本操作
print(df.head())        # 前幾筆資料
print(df.describe())     # 統計摘要
print(df.info())        # 資料資訊

# 選擇資料
print(df['name'])       # 單欄
print(df[df['age'] > 25])  # 過濾
```

## Matplotlib 視覺化

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', label='sin(x)')
plt.plot(x, np.cos(x), 'r--', label='cos(x)')
plt.title('三角函數')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
```

## 機器學習與 scikit-learn

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 假裝這是特徵和標籤
X = np.random.rand(100, 4)
y = (X[:, 0] + X[:, 1] > 1).astype(int)

# 分割資料
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 訓練模型
clf = RandomForestClassifier(n_estimators=10)
clf.fit(X_train, y_train)

# 預測
predictions = clf.predict(X_test)
print(f"準確率：{accuracy_score(y_test, predictions):.2f}")
```

## 結論

Python 已經成為資料科學領域的主導語言。2015 年正是這個趨勢加速的時期，NumPy、Pandas、scikit-learn 等工具的成熟，使得 Python 成為資料科學家的首選。