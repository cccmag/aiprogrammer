# Pandas 資料操作

## 從資料科學的角度出發

Pandas 是由 Wes McKinney 於 2008 年創建的 Python 資料分析函式庫。Wes 當時在 AQR Capital Management 工作，他發現 Python 缺乏一個像 R 的 data.frame 一樣方便的工具來處理結構化資料。這個需求催生了 Pandas——如今已成為資料科學家手中最重要的工具之一。

## DataFrame 與 Series

Pandas 有兩個核心資料結構：

**Series**：一維標籤陣列
```
索引 → 值
0   → Alice
1   → Bob
2   → Charlie
dtype: object
```

**DataFrame**：二維標籤表格
```
       name    age  salary  dept
0    Alice     25   50000    IT
1      Bob     32   62000    HR
2  Charlie     37   78000    IT
```

```python
import pandas as pd

# 從字典建立 DataFrame
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 32, 37],
    "salary": [50000, 62000, 78000],
    "dept": ["IT", "HR", "IT"]
})

# 讀取 CSV
df = pd.read_csv("data.csv")
```

## 資料清洗

真實世界的資料總是髒的。Pandas 提供了完整的清洗工具鏈：

```python
# 檢查缺失值
df.isnull().sum()

# 填充缺失值
df.fillna(0)
df["age"].fillna(df["age"].median())

# 移除重複
df.drop_duplicates()

# 類型轉換
df["date"] = pd.to_datetime(df["date"])

# 字串處理
df["name"] = df["name"].str.strip().str.lower()
```

## 資料篩選與切片

Pandas 的索引語法靈活而強大：

```python
# 列選擇
df["name"]
df[["name", "age"]]

# 行選擇（loc / iloc）
df.loc[df["age"] > 30]
df.iloc[1:3]

# 複合條件篩選
df[(df["age"] > 25) & (df["dept"] == "IT")]
```

## 分組與聚合

split-apply-combine 是 Pandas 最強大的功能之一：

```python
# 分組聚合
df.groupby("dept")["salary"].mean()

# 多重聚合
df.groupby("dept").agg({
    "salary": ["mean", "std", "count"],
    "age": "mean"
})

# 資料透視表
pd.pivot_table(df, values="salary", index="dept",
               columns="gender", aggfunc="mean")
```

## 合併與連接

```python
# SQL 風格的 join
pd.merge(df1, df2, on="key", how="left")

# 縱向連接
pd.concat([df1, df2], axis=0)

# 橫向連接
pd.concat([df1, df2], axis=1)
```

## 時間序列處理

Pandas 在時間序列方面有著深厚的積累：

```python
# 建立日期索引
df.index = pd.date_range("2022-01-01", periods=len(df), freq="D")

# 重採樣
df.resample("M").mean()

# 滾動視窗
df["rolling_mean"] = df["value"].rolling(window=7).mean()
```

## 為什麼 Pandas 如此重要？

Pandas 的成功可以歸因於：

1. **R 用戶的親切感**：DataFrame 模型對 R 用戶自然友好
2. **與 NumPy 的深度整合**：底層用 NumPy 陣列儲存，效能可靠
3. **豐富的 I/O 支援**：CSV、Excel、SQL、Parquet、HDF5
4. **活躍的社群**：持續的開發和廣泛的第三方擴展

## 延伸閱讀

- [Pandas 官方教學](https://www.google.com/search?q=Pandas+tutorial)
- [Pandas 資料清洗指南](https://www.google.com/search?q=Pandas+data+cleaning)
- [Pandas 時間序列](https://www.google.com/search?q=Pandas+time+series)

---

*本篇文章為「AI 程式人雜誌 2022 年 3 月號」歷史回顧系列之一。*
