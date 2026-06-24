# 資料篩選與過濾

## 前言

篩選與過濾是資料分析中最常見的操作之一。無論是找出符合條件的客戶、篩選特定時間範圍的記錄，還是過濾異常值，Pandas 提供了多種靈活的方式來完成這些任務。

## 布林索引（Boolean Indexing）

布林索引是 Pandas 最基本的篩選方式：

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "David"],
    "age": [25, 30, 35, 28],
    "city": ["台北", "台中", "台北", "高雄"],
    "salary": [50000, 60000, 70000, 48000],
})

# 單一條件
print(df[df["age"] > 30])

# 多條件 (使用 &, |, ~)
print(df[(df["age"] > 28) & (df["salary"] > 50000)])
print(df[(df["city"] == "台北") | (df["city"] == "高雄")])

# 反向條件
print(df[~(df["city"] == "台中")])
```

## isin 方法

當需要篩選多個特定值時，`isin` 比多個 `|` 條件更簡潔：

```python
# 篩選台北或高雄的資料
print(df[df["city"].isin(["台北", "高雄"])])

# 反向：排除特定值
print(df[~df["city"].isin(["台中"])])
```

## query 方法

對於熟悉 SQL 的使用者，`query` 提供了更接近 SQL WHERE 子句的語法：

```python
# 使用 query
result = df.query("age > 28 and salary > 50000")
print(result)

# 引用外部變數
threshold = 55000
result = df.query("salary > @threshold")

# 包含字串條件
result = df.query('city == "台北"')
```

## loc 與 iloc

`loc` 使用標籤索引，`iloc` 使用整數位置索引：

```python
# loc：標籤選取
print(df.loc[0:2])                    # 第 0 到 2 列
print(df.loc[df["age"] > 30, ["name", "salary"]])  # 條件 + 欄位選取

# iloc：整數位置選取
print(df.iloc[0:3, 0:2])             # 前 3 列前 2 欄
print(df.iloc[:, [0, 2]])            # 所有列，第 0 與第 2 欄
```

## 字串方法

Pandas 的字串操作透過 `.str` 存取器：

```python
# 模糊匹配
print(df[df["name"].str.contains("li", case=False)])

# 開頭/結尾匹配
print(df[df["name"].str.startswith("A")])
print(df[df["city"].str.endswith("北")])

# 正規表示式
print(df[df["name"].str.match(r"^[A-C]")])
```

## 時間範圍篩選

```python
dates = pd.date_range("2026-01-01", periods=100)
ts_df = pd.DataFrame({"value": range(100)}, index=dates)

# 日期範圍篩選
print(ts_df.loc["2026-01-10":"2026-01-20"])

# 年份/月份篩選
print(ts_df.loc["2026-03"])
```

## 實戰：清理與篩選流程

```python
def filter_and_clean(df):
    result = df.copy()
    result = result.dropna(subset=["必要欄位"])
    result = result[result["數值"] > 0]           # 移除負值
    result = result[result["數值"] < result["數值"].quantile(0.99)]  # 移除極端值
    result = result[result["類別"].isin(["A", "B", "C"])]           # 只保留有效類別
    return result
```

---

**延伸閱讀**
- [Pandas 索引與選取資料](https://www.google.com/search?q=Pandas+indexing+and+selecting+data)
- [Pandas query 方法教學](https://www.google.com/search?q=Pandas+query+method+tutorial)
