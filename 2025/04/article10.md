# 散佈圖與熱力圖

## 前言

散佈圖和熱力圖是探索變數之間關係的重要工具。散佈圖以點的位置展示兩個連續變數的相關性，熱力圖則以顏色深淺來呈現矩陣資料的數值大小。這兩種圖表在資料分析和機器學習的特徵工程中扮演著關鍵角色。

## 散佈圖 (Scatter Plot)

散佈圖將每個資料點繪製在二維平面上：

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(42)
n = 200
x = np.random.randn(n)
y = x * 0.7 + np.random.randn(n) * 0.5

# 基本散佈圖
plt.figure(figsize=(8, 6))
plt.scatter(x, y, alpha=0.6, edgecolors="black", linewidth=0.5)
plt.title("散佈圖")
plt.xlabel("X 變數")
plt.ylabel("Y 變數")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 加入迴歸線

```python
from scipy import stats

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
regression_line = slope * x + intercept

plt.figure(figsize=(8, 6))
plt.scatter(x, y, alpha=0.6, label="資料點")
plt.plot(x, regression_line, color="red", linewidth=2, label=f"迴歸線 (r={r_value:.3f})")
plt.legend()
plt.title(f"散佈圖與迴歸線 (相關係數: {r_value:.3f})")
plt.tight_layout()
plt.show()
```

### 分組散佈圖

```python
groups = np.random.choice(["A", "B", "C"], size=n)
colors = {"A": "red", "B": "blue", "C": "green"}

plt.figure(figsize=(8, 6))
for group in ["A", "B", "C"]:
    mask = groups == group
    plt.scatter(x[mask], y[mask], c=colors[group], label=f"Group {group}", alpha=0.6)

plt.legend()
plt.title("分組散佈圖")
plt.tight_layout()
plt.show()
```

### 氣泡圖 (Bubble Chart)

```python
sizes = np.random.randint(20, 200, n)
plt.figure(figsize=(8, 6))
plt.scatter(x, y, s=sizes, alpha=0.5, c=x, cmap="viridis")
plt.colorbar(label="X 值")
plt.title("氣泡圖 (點大小表示第三維度)")
plt.tight_layout()
plt.show()
```

## 熱力圖 (Heatmap)

熱力圖使用顏色編碼來表示矩陣中的數值：

```python
# 建立相關性矩陣
df = pd.DataFrame({
    "A": np.random.randn(100),
    "B": np.random.randn(100) * 0.5 + 0.3,
    "C": np.random.randn(100) * 0.8,
    "D": np.random.randn(100) * 0.3 - 0.2,
})
corr_matrix = df.corr()

# 使用 Matplotlib 繪製熱力圖
plt.figure(figsize=(8, 6))
plt.imshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1, aspect="auto")
plt.colorbar(label="相關係數")

# 標註數值
for i in range(len(corr_matrix)):
    for j in range(len(corr_matrix)):
        plt.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}",
                 ha="center", va="center", color="white" if abs(corr_matrix.iloc[i, j]) > 0.5 else "black")

plt.xticks(range(len(corr_matrix)), corr_matrix.columns)
plt.yticks(range(len(corr_matrix)), corr_matrix.columns)
plt.title("相關係數熱力圖")
plt.tight_layout()
plt.show()
```

### 使用 Seaborn 的熱力圖

```python
import seaborn as sns

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm",
            vmin=-1, vmax=1, center=0,
            linewidths=0.5, fmt=".2f")
plt.title("Seaborn 熱力圖")
plt.tight_layout()
plt.show()
```

## 散佈圖矩陣 (Scatter Matrix)

同時觀察多個變數之間的兩兩關係：

```python
# 使用 Pandas
pd.plotting.scatter_matrix(df, figsize=(10, 10), diagonal="hist")
plt.tight_layout()
plt.show()

# 使用 Seaborn
sns.pairplot(df)
plt.show()
```

## 實戰：探索資料關聯

```python
def explore_correlation(df, target):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    features = [col for col in df.columns if col != target]
    for ax, feature in zip(axes.ravel(), features[:4]):
        ax.scatter(df[feature], df[target], alpha=0.5)
        ax.set_xlabel(feature)
        ax.set_ylabel(target)
        corr = df[feature].corr(df[target])
        ax.set_title(f"{feature} vs {target} (r={corr:.3f})")
    plt.tight_layout()
    plt.show()
```

---

**延伸閱讀**
- [Matplotlib 散佈圖教學](https://www.google.com/search?q=Matplotlib+scatter+plot+tutorial)
- [Seaborn 熱力圖教學](https://www.google.com/search?q=Seaborn+heatmap+tutorial)
