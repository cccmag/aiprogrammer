# 資料清理與前處理

## 為什麼資料清理如此重要

真實世界的資料很少是乾淨整齊的。調查資料可能含有空白欄位，感測器資料可能出現異常值，合併不同來源的資料可能導致格式不一致。資料科學家常說：「資料清理佔了分析工作 80% 的時間。」學會有效率的清理技巧，是成為資料分析師的必經之路。

## 缺失值處理

Pandas 使用 `NaN`（Not a Number）來表示缺失值：

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "A": [1, 2, np.nan, 4, 5],
    "B": [np.nan, 2, 3, np.nan, 5],
    "C": [1, 2, 3, 4, 5],
})
```

### 偵測缺失值

```python
print(df.isnull())            # 布林矩陣
print(df.isnull().sum())      # 各欄缺失值數量
print(df.isnull().sum().sum()) # 總缺失值數量
```

### 刪除缺失值

```python
df.dropna()                   # 刪除包含 NaN 的列
df.dropna(axis=1)             # 刪除包含 NaN 的欄
df.dropna(thresh=3)           # 保留至少有 3 個非 NaN 值的列
```

### 填補缺失值

```python
df.fillna(0)                  # 用 0 填補
df.fillna(df.mean())          # 用該欄平均值填補
df["A"].fillna(method="ffill") # 前向填補
df["B"].fillna(method="bfill") # 後向填補
df.interpolate()              # 線性插值
```

## 重複資料處理

```python
df = pd.DataFrame({
    "name": ["A", "B", "A", "C", "B"],
    "value": [1, 2, 1, 3, 2],
})

print(df.duplicated())               # 標記重複列
print(df.duplicated(subset=["name"])) # 根據特定欄位判斷
df_unique = df.drop_duplicates()      # 移除重複
```

## 型別轉換

```python
# 檢查型別
print(df.dtypes)

# 型別轉換
df["數值"] = pd.to_numeric(df["數值"], errors="coerce")
df["日期"] = pd.to_datetime(df["日期"])
df["類別"] = df["類別"].astype("category")
```

## 資料正規化

將資料縮放到特定範圍，有助於機器學習演算法的收斂：

```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# 最小最大值正規化
scaler = MinMaxScaler()
df_norm = scaler.fit_transform(df[["數值"]])

# 標準化 (z-score)
scaler = StandardScaler()
df_std = scaler.fit_transform(df[["數值"]])
```

## 異常值處理

```python
# 使用 IQR 方法偵測異常值
Q1 = df["數值"].quantile(0.25)
Q3 = df["數值"].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df["數值"] < Q1 - 1.5 * IQR) | (df["數值"] > Q3 + 1.5 * IQR)]
```

## 實戰範例

```python
# 完整的清理流程
def clean_data(df):
    df = df.copy()
    df = df.drop_duplicates()
    df = df.dropna(subset=["必要欄位"])
    df["數值欄"] = pd.to_numeric(df["數值欄"], errors="coerce")
    df["數值欄"] = df["數值欄"].fillna(df["數值欄"].median())
    df["日期"] = pd.to_datetime(df["日期"])
    return df
```

---

**延伸閱讀**
- [Pandas 資料清理教學](https://www.google.com/search?q=Pandas+data+cleaning+tutorial)
- [資料前處理技術總覽](https://www.google.com/search?q=data+preprocessing+techniques+Python)
