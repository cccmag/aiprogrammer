# Pandas Series 與 DataFrame

## Pandas 的兩種核心資料結構

Pandas 提供了兩種主要的資料結構：Series（一維）和 DataFrame（二維）。兩者都建立在 NumPy 陣列之上，但加入了軸標籤（index）的功能。

## Series — 一維標籤陣列

Series 類似於帶有索引的 NumPy 一維陣列，或 Python 字典的推廣：

```python
import pandas as pd
import numpy as np

# 從 list 建立
s = pd.Series([10, 20, 30, 40])
print(s)
# 0    10
# 1    20
# 2    30
# 3    40

# 指定索引
s = pd.Series([10, 20, 30], index=["a", "b", "c"])

# 從 dict 建立
s = pd.Series({"台北": 250, "台中": 180, "高雄": 200})
print(s["台北"])    # 250
```

## DataFrame — 二維表格

DataFrame 是 Pandas 最重要的資料結構，類似於試算表或 SQL 表格：

```python
# 從 dict 建立
df = pd.DataFrame({
    "城市": ["台北", "台中", "高雄"],
    "人口": [250, 180, 200],
    "面積": [271.8, 221.4, 295.1],
})
print(df)
```

### 基本屬性

```python
print(df.shape)      # (3, 3)
print(df.columns)    # Index(['城市', '人口', '面積'], dtype='object')
print(df.index)      # RangeIndex(start=0, stop=3, step=1)
print(df.dtypes)     # 各欄位型別
print(df.info())     # 完整摘要資訊
```

### 資料選取

DataFrame 提供了多種選取資料的方式：

```python
# 選取欄位
print(df["城市"])           # 單一欄位，回傳 Series
print(df[["城市", "人口"]]) # 多個欄位，回傳 DataFrame

# 選取列 (loc / iloc)
print(df.loc[0])            # 第一列 (標籤索引)
print(df.iloc[0])           # 第一列 (整數索引)
print(df.loc[0:2])          # 第 0 到 2 列
print(df.iloc[:, 0])        # 所有列，第一欄
```

### 條件篩選

```python
print(df[df["人口"] > 190])     # 人口大於 190 的城市
print(df[(df["人口"] > 180) & (df["面積"] < 250)])
```

## 索引的重要性

Pandas 的索引（index）是區別於 NumPy 陣列的關鍵特性：

```python
df.index = ["北", "中", "南"]    # 自訂索引
print(df.loc["北"])               # 使用自訂索引選取
print(df.iloc[0])                 # 仍可用整數索引
```

### 重設與設定索引

```python
df.reset_index()     # 將索引還原為整數
df.set_index("城市")  # 將某欄設為索引
```

## 基本統計

```python
print(df.describe())         # 數值欄位的統計摘要
print(df["人口"].mean())     # 平均值
print(df["人口"].sum())      # 總和
print(df["人口"].min())      # 最小值
print(df["人口"].max())      # 最大值
```

---

**延伸閱讀**
- [Pandas 10 分鐘入門](https://www.google.com/search?q=Pandas+10+minutes+to+pandas)
- [Pandas DataFrame 官方教學](https://www.google.com/search?q=Pandas+DataFrame+tutorial)
