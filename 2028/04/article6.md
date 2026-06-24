# 資料湖 vs 資料倉儲

## 前言

在 AI 時代，企業需要儲存和分析海量資料。資料湖（Data Lake）和資料倉儲（Data Warehouse）是兩種主流的資料架構，各有適用場景。本文從 AI 資料工程的角度比較兩者。

## 架構理念對比

資料倉儲採用 Schema-on-Write 模式，寫入時就需要定義結構；資料湖採用 Schema-on-Read，讀取時才解析結構。

```python
""" 模擬兩種架構的差異 """
import pandas as pd
import json

# Schema-on-Write（資料倉儲）
def write_to_warehouse(df: pd.DataFrame):
    """必須符合預定義的 schema"""
    expected_schema = {
        "user_id": "int64",
        "name": "object",
        "email": "object",
    }
    for col, dtype in expected_schema.items():
        assert df[col].dtype == dtype, f"欄位 {col} 型別不符"
    print("寫入資料倉儲")

# Schema-on-Read（資料湖）
def read_from_lake(filepath: str) -> pd.DataFrame:
    """讀取時彈性解析"""
    with open(filepath) as f:
        raw = json.load(f)
    df = pd.json_normalize(raw)
    print(f"從資料湖讀取，推斷 schema: {dict(df.dtypes)}")
    return df
```

## 資料湖：Delta Lake 實戰

Delta Lake 為資料湖加入了交易日誌和版本控制：

```python
from delta import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DataLakeDemo") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# 寫入 Delta 表
data = spark.range(0, 1000)
data.write.format("delta").save("/data/delta/numbers")

# 讀取歷史版本
df_v1 = spark.read.format("delta") \
    .option("versionAsOf", 0) \
    .load("/data/delta/numbers")

df_v1.show(5)

# Delta Lake 支援 ACID 交易、時間旅行和 Schema 演進
```

## 資料倉儲：現代架構

Snowflake 和 BigQuery 等雲端倉儲提供了極致的查詢效能：

```python
"""使用 DuckDB 模擬倉儲查詢"""
import duckdb

conn = duckdb.connect("warehouse.db")

# 定義結構化表
conn.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER,
        product_id INTEGER,
        amount DECIMAL(10,2),
        sale_date DATE
    )
""")

# 高速聚合查詢
result = conn.execute("""
    SELECT 
        DATE_TRUNC('month', sale_date) as month,
        COUNT(*) as transactions,
        SUM(amount) as revenue,
        AVG(amount) as avg_ticket
    FROM sales
    GROUP BY month
    ORDER BY month
""").fetchdf()

print(result)
```

## 選擇指南

| 維度 | 資料湖 | 資料倉儲 |
|------|--------|----------|
| 資料類型 | 結構化 + 非結構化 | 結構化為主 |
| Schema | 讀取時定義 | 寫入時定義 |
| 查詢效能 | 中等 | 極佳 |
| 成本 | 較低 | 較高 |
| 典型用途 | 資料探索、ML 訓練 | BI 報表、分析 |

## 結語

現代企業通常採用「湖倉一體」（Lakehouse）架構——以資料湖為基礎，加上倉儲級的查詢引擎（如 Databricks SQL、Apache Iceberg）。對於 AI 專案，資料湖更適合儲存原始資料和特徵，而倉儲則適合聚合分析與監控儀表板。

---

**延伸閱讀**

- [Delta Lake 官方文件](https://www.google.com/search?q=Delta+Lake+documentation)
- [Lakehouse 架構介紹](https://www.google.com/search?q=Lakehouse+architecture+data)
- [資料湖 vs 資料倉儲比較](https://www.google.com/search?q=data+lake+vs+data+warehouse+comparison)
