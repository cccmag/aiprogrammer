# 統計摘要與相關性

## 前言

在進行複雜的建模之前，先對資料進行統計摘要和相關性分析，可以快速掌握資料的全貌。這些分析幫助我們發現資料中的模式、趨勢和異常，為後續的深入分析奠定基礎。

## 描述性統計

Pandas 的 `describe` 方法提供了一個快速的統計摘要：

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "age": np.random.randint(18, 65, 100),
    "salary": np.random.randint(30000, 150000, 100),
    "experience": np.random.randint(0, 40, 100),
    "score": np.random.randn(100) * 10 + 70,
})

print(df.describe())

# 指定百分位數
print(df.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]))
```

### 自訂統計摘要

```python
summary = pd.DataFrame({
    "mean": df.mean(),
    "median": df.median(),
    "std": df.std(),
    "min": df.min(),
    "max": df.max(),
    "range": df.max() - df.min(),
    "skew": df.skew(),
    "kurtosis": df.kurtosis(),
})
print(summary.round(2))
```

## 相關性分析

### 相關係數矩陣

```python
# Pearson 相關係數 (預設)
corr_pearson = df.corr(method="pearson")

# Spearman 等級相關係數
corr_spearman = df.corr(method="spearman")

# Kendall 相關係數
corr_kendall = df.corr(method="kendall")
```

### 解讀相關係數

| 相關係數範圍 | 相關強度 |
|-------------|---------|
| 0.0 - 0.3 | 弱相關 |
| 0.3 - 0.7 | 中等相關 |
| 0.7 - 1.0 | 強相關 |

### 視覺化相關性

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 6))
sns.heatmap(corr_pearson, annot=True, cmap="coolwarm",
            vmin=-1, vmax=1, center=0,
            linewidths=0.5)
plt.title("相關係數矩陣")
plt.show()
```

## 共變異數

```python
cov_matrix = df.cov()
print(cov_matrix)
```

## 統計檢定

### t 檢定

```python
from scipy import stats

# 兩組樣本的 t 檢定
group_a = df[df["age"] < 30]["salary"]
group_b = df[df["age"] >= 30]["salary"]

t_stat, p_value = stats.ttest_ind(group_a, group_b)
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

### 相關性顯著性檢定

```python
# Pearson 相關性檢定
corr, p_value = stats.pearsonr(df["experience"], df["salary"])
print(f"Pearson correlation: {corr:.4f}")
print(f"p-value: {p_value:.4f}")
```

## 群組統計比較

```python
# 按類別分組比較
df["age_group"] = pd.cut(df["age"], bins=[0, 30, 45, 100],
                          labels=["young", "mid", "senior"])

group_stats = df.groupby("age_group")["salary"].agg(["mean", "std", "count"])
print(group_stats)
```

## 實戰：資料摘要報告

```python
def generate_summary_report(df):
    """產生完整的資料摘要報告"""
    report = {
        "shape": df.shape,
        "missing": df.isnull().sum().to_dict(),
        "dtypes": df.dtypes.to_dict(),
        "numeric_summary": df.describe().to_dict(),
        "correlation": df.corr().to_dict(),
    }
    return report
```

---

**延伸閱讀**
- [Pandas 統計函式參考](https://www.google.com/search?q=Pandas+statistical+functions)
- [SciPy 統計檢定教學](https://www.google.com/search?q=Scipy+statistical+tests+tutorial)
