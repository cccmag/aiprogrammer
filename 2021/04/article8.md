# Article 8：Pandas 與 SQL 的轉換技巧

## 對照表

兩者的核心概念有對應關係：SELECT 對應 `df[['a', 'b']]`、WHERE 對應 `df[df['a'] > 1]`、JOIN 對應 `pd.merge()`、GROUP BY 對應 `df.groupby()`。理解這些對應關係可幫助你將 SQL 查詢轉換為 pandas 操作。

## 簡單查詢

SQL: `SELECT a, b FROM df WHERE a > 1`
Pandas: `df[df['a'] > 1][['a', 'b']]`

SQL: `SELECT a, SUM(b) FROM df GROUP BY a`
Pandas: `df.groupby('a')['b'].sum()`

## 複雜查詢

多表連接：
```python
pd.merge(df1, df2, on='key', how='inner')
```

窗口函數：
```python
df.assign(rank=df.groupby('a')['b'].rank(ascending=False))
```

子查詢：用 `df[df['a'].isin(subquery)]` 實現 IN，或用 `merge` 實現 EXISTS。

## pandas 特有的功能

pandas 有些 SQL 沒有的強大功能：如 `pivot_table` 的透視能力、`resample` 的時間序列重採樣、`rolling` 的移動窗口計算。熟練掌握這些功能可簡化很多 SQL 中繁瑣的操作。

## 參考資源

- pandas SQL Comparison：https://www.google.com/search?q=pandas+sql+comparison
- pandas vs SQL：https://www.google.com/search?q=pandas+vs+SQL+translation