# 處理缺失值

## 前言

缺失值是現實資料中無法避免的問題。問卷調查的漏答、感測器的暫時故障、資料庫的 NULL 值，都會導致資料集中出現缺失值。如何正確處理缺失值，直接影響後續分析的準確性。

## 缺失值的表示

Pandas 使用 `NaN`（Not a Number）表示缺失值，屬於 `float` 型別：

```python
import pandas as pd
import numpy as np

s = pd.Series([1, 2, np.nan, 4, np.nan])
print(s)

# 檢查是否缺失
print(s.isna())      # True/False
print(s.notna())     # 反向
```

## 偵測缺失值

```python
df = pd.DataFrame({
    "A": [1, 2, np.nan, 4, np.nan],
    "B": [np.nan, 2, 3, np.nan, 5],
    "C": [1, 2, 3, 4, 5],
    "D": [np.nan, np.nan, np.nan, np.nan, np.nan],
})

# 總覽
print(df.info())
print(df.isnull().sum())

# 可視化缺失值
import matplotlib.pyplot as plt
import seaborn as sns
sns.heatmap(df.isnull(), cbar=False)
plt.show()
```

## 刪除缺失值

```python
# 刪除任何包含缺失值的列
df_clean = df.dropna()

# 刪除全部為缺失值的列
df_clean = df.dropna(how="all")

# 保留至少有 n 個非缺失值的列
df_clean = df.dropna(thresh=3)

# 刪除特定欄位有缺失值的列
df_clean = df.dropna(subset=["A", "B"])

# 刪除整欄
df_clean = df.dropna(axis=1, thresh=3)
```

## 填補缺失值

```python
# 固定值填補
df["A"] = df["A"].fillna(0)
df["B"] = df["B"].fillna("未知")

# 統計值填補
df["A"] = df["A"].fillna(df["A"].mean())
df["B"] = df["B"].fillna(df["B"].median())
df["C"] = df["C"].fillna(df["C"].mode()[0])

# 前向/後向填補
df["A"] = df["A"].fillna(method="ffill")    # 前一個值
df["B"] = df["B"].fillna(method="bfill")    # 後一個值
```

## 進階填補策略

### 線性插值

```python
# 線性插值
df_interp = df.interpolate(method="linear")

# 時間序列插值
ts = pd.Series([1, np.nan, np.nan, 4], index=pd.date_range("2026-01-01", periods=4))
print(ts.interpolate(method="time"))
```

### 群組填補

```python
# 按群組平均值填補
df["數值"] = df.groupby("類別")["數值"].transform(lambda x: x.fillna(x.mean()))
```

### KNN 填補

```python
from sklearn.impute import KNNImputer

imputer = KNNImputer(n_neighbors=3)
df_filled = pd.DataFrame(
    imputer.fit_transform(df[["A", "B", "C"]]),
    columns=["A", "B", "C"],
)
```

## 實戰範例

```python
def smart_fill(df, strategy="auto"):
    """智慧填補缺失值"""
    result = df.copy()
    for col in result.columns:
        na_count = result[col].isnull().sum()
        if na_count == 0:
            continue
        if result[col].dtype in ["int64", "float64"]:
            if strategy == "auto":
                fill_val = result[col].median()
            else:
                fill_val = result[col].mean()
        else:
            fill_val = result[col].mode()[0]
        result[col] = result[col].fillna(fill_val)
    return result
```

---

**延伸閱讀**
- [Pandas 缺失值處理指南](https://www.google.com/search?q=Pandas+missing+data+handling)
- [Scikit-learn 缺失值填補](https://www.google.com/search?q=Scikit-learn+impute+missing+values)
