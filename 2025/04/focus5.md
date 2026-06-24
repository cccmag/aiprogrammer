# 資料聚合與分組運算

## groupby 機制

資料聚合（Aggregation）是資料分析中最常見的操作之一。Pandas 的 `groupby` 機制遵循「拆分—應用—合併」（Split-Apply-Combine）模式：

1. **拆分**：根據某個或多個鍵將 DataFrame 拆分為多個組
2. **應用**：對每個組獨立應用某個函式
3. **合併**：將結果合併為新的 DataFrame

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "部門": ["業務", "工程", "業務", "工程", "管理"],
    "區域": ["北", "北", "南", "南", "北"],
    "業績": [100, 150, 200, 120, 180],
    "成本": [60, 80, 90, 70, 100],
})
```

### 基本分組

```python
# 單鍵分組
grouped = df.groupby("部門")
print(grouped["業績"].sum())

# 多鍵分組
grouped = df.groupby(["部門", "區域"])
print(grouped["業績"].mean())
```

### 聚合函式

```python
# 使用 agg 指定多個聚合函式
result = df.groupby("部門").agg({
    "業績": ["sum", "mean", "max"],
    "成本": ["sum", "mean"],
})
print(result)

# 使用命名聚合
result = df.groupby("部門").agg(
    總業績=("業績", "sum"),
    平均業績=("業績", "mean"),
    總成本=("成本", "sum"),
)
```

## transform

`transform` 與 `agg` 的差別在於：`agg` 回傳的是縮減後的結果，而 `transform` 回傳的是與原始 DataFrame 相同形狀的結果：

```python
# 計算各部門業績佔比
df["部門業績佔比"] = df["業績"] / df.groupby("部門")["業績"].transform("sum")
```

## filter

根據分組條件過濾資料：

```python
# 只保留總業績大於 250 的部門
result = df.groupby("部門").filter(lambda x: x["業績"].sum() > 250)
```

## apply

`apply` 是最靈活的操作，可以接受任何自訂函式：

```python
def top_n(group, n=2):
    return group.sort_values("業績", ascending=False).head(n)

result = df.groupby("部門").apply(top_n, n=2)
```

## 樞紐分析表

樞紐分析表（Pivot Table）是 Excel 資料分析中最受歡迎的功能之一，Pandas 提供了完整的支援：

```python
pivot = df.pivot_table(
    values="業績",
    index="部門",
    columns="區域",
    aggfunc="sum",
    fill_value=0,
)
print(pivot)
```

### 多重聚合的樞紐表

```python
pivot = df.pivot_table(
    values=["業績", "成本"],
    index="部門",
    columns="區域",
    aggfunc={"業績": "sum", "成本": "mean"},
    fill_value=0,
)
```

## cross tab

交叉分析表（crosstab）適合計算頻率或計數：

```python
pd.crosstab(df["部門"], df["區域"], margins=True)
```

---

**延伸閱讀**
- [Pandas groupby 官方教學](https://www.google.com/search?q=Pandas+groupby+tutorial)
- [Pandas 樞紐分析表](https://www.google.com/search?q=Pandas+pivot+table+tutorial)
