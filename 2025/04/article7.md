# 分組與聚合實戰

## 前言

分組與聚合是資料分析的核心能力。無論是計算各部門的業績總和、各產品的平均銷售量，還是各區域的客戶數，groupby 操作都是實現這些分析的關鍵工具。

## 基本 groupby

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "date": pd.date_range("2026-01-01", periods=12, freq="ME"),
    "department": ["業務", "業務", "工程", "工程", "業務", "管理",
                    "工程", "業務", "管理", "工程", "業務", "管理"],
    "revenue": np.random.randint(100, 500, 12),
    "cost": np.random.randint(50, 300, 12),
})
```

### 單鍵分組

```python
# 基本聚合
dept_sum = df.groupby("department")["revenue"].sum()
print(dept_sum)

# 多個聚合函式
dept_stats = df.groupby("department")["revenue"].agg(["sum", "mean", "std", "count"])
print(dept_stats)
```

## 進階聚合

### 多欄位多函式

```python
result = df.groupby("department").agg({
    "revenue": ["sum", "mean", "max"],
    "cost": ["sum", "mean"],
})
print(result)
```

### 命名聚合

```python
result = df.groupby("department").agg(
    total_revenue=("revenue", "sum"),
    avg_revenue=("revenue", "mean"),
    total_cost=("cost", "sum"),
    profit=("revenue", lambda x: x.sum() * 0.7),
)
```

## transform — 群組內運算

`transform` 回傳與原始 DataFrame 相同形狀的結果：

```python
# 計算各部門業績佔比
df["dept_revenue_pct"] = (
    df["revenue"] / df.groupby("department")["revenue"].transform("sum")
)

# 群組內排名
df["dept_rank"] = df.groupby("department")["revenue"].rank(ascending=False)
```

## filter — 群組過濾

```python
# 只保留總業績大於 1000 的部門
result = df.groupby("department").filter(lambda x: x["revenue"].sum() > 1000)
```

## apply — 自訂函式

`apply` 是最靈活的操作：

```python
def top_n_by_revenue(group, n=2):
    return group.nlargest(n, "revenue")

result = df.groupby("department").apply(top_n_by_revenue, n=2)
```

## 多層次分組

```python
# 多鍵分組
df["quarter"] = df["date"].dt.quarter
result = df.groupby(["department", "quarter"]).agg(
    total_revenue=("revenue", "sum"),
    total_cost=("cost", "sum"),
)
print(result)
```

## 樞紐分析表

```python
pivot = df.pivot_table(
    values="revenue",
    index="department",
    columns=df["date"].dt.month,
    aggfunc="sum",
    fill_value=0,
)
print(pivot)
```

## 實戰：銷售分析

```python
def sales_analysis(df):
    result = df.groupby(["region", "product"]).agg(
        total_sales=("amount", "sum"),
        avg_sales=("amount", "mean"),
        transaction_count=("amount", "count"),
    ).reset_index()
    result["pct_of_region"] = (
        result.groupby("region")["total_sales"]
        .transform(lambda x: x / x.sum() * 100)
    )
    return result.sort_values("total_sales", ascending=False)
```

---

**延伸閱讀**
- [Pandas groupby 官方教學](https://www.google.com/search?q=Pandas+groupby+tutorial+documentation)
- [Pandas 聚合函式參考](https://www.google.com/search?q=Pandas+aggregation+functions+reference)
