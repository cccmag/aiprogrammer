# 資料合併與連接

## 前言

在真實的資料分析場景中，資料往往分散在不同的表格或檔案中。客戶資料在一個表格，訂單記錄在另一個表格；產品資訊和庫存資料分屬不同系統。學會合併與連接資料，是整合這些資訊的關鍵技能。

## concat — 簡單串接

`pd.concat` 用於將多個 DataFrame 沿著行或列方向串接：

```python
import pandas as pd

df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})

# 垂直串接 (增加行)
result = pd.concat([df1, df2])
print(result)

# 水平串接 (增加列)
result = pd.concat([df1, df2], axis=1)

# 忽略索引
result = pd.concat([df1, df2], ignore_index=True)
```

### 處理索引重複

```python
# 加上層次化索引
result = pd.concat([df1, df2], keys=["first", "second"])
print(result.loc["first"])
```

## merge — SQL 風格的連接

`pd.merge` 類似於 SQL 的 JOIN 操作：

```python
customers = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "city": ["台北", "台中", "高雄"],
})

orders = pd.DataFrame({
    "customer_id": [1, 2, 1, 3, 2],
    "product": ["A", "B", "C", "A", "B"],
    "amount": [100, 200, 150, 300, 250],
})
```

### 四種連接類型

```python
# Inner Join (預設)
result = pd.merge(customers, orders, left_on="id", right_on="customer_id")

# Left Join
result = pd.merge(customers, orders, left_on="id", right_on="customer_id", how="left")

# Right Join
result = pd.merge(customers, orders, left_on="id", right_on="customer_id", how="right")

# Outer Join
result = pd.merge(customers, orders, left_on="id", right_on="customer_id", how="outer")
```

### 索引連接

```python
# 使用索引進行連接
result = pd.merge(df1, df2, left_index=True, right_index=True)
```

## join — 簡化的 DataFrame 方法

`join` 是 `merge` 的簡化版本，預設使用索引進行連接：

```python
# 使用 join
result = customers.set_index("id").join(
    orders.set_index("customer_id"),
    how="inner",
)
```

## 處理重複欄位名稱

```python
# 自動加上後綴
result = pd.merge(
    customers, orders,
    left_on="id", right_on="customer_id",
    suffixes=("_cust", "_ord"),
)
```

## 多鍵連接

```python
# 使用多個鍵進行連接
result = pd.merge(
    df1, df2,
    on=["key1", "key2"],
    how="inner",
)
```

## 實戰範例

```python
# 完整資料整合流程
def integrate_data(customers, orders, products):
    result = pd.merge(customers, orders, left_on="id", right_on="customer_id")
    result = pd.merge(result, products, on="product_id")
    result = result[result["amount"] > 0]
    return result
```

### 檢查連接結果

```python
# 檢查是否有未匹配的資料
merged = pd.merge(customers, orders, left_on="id", right_on="customer_id", how="left", indicator=True)
print(merged["_merge"].value_counts())
```

---

**延伸閱讀**
- [Pandas merge 官方教學](https://www.google.com/search?q=Pandas+merge+join+tutorial)
- [Pandas concat 使用方法](https://www.google.com/search?q=Pandas+concat+function)
