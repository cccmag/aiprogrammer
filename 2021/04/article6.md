# Article 6：Parquet 格式與資料湖架構

## Parquet 的優勢

Parquet 是一種列式儲存格式，專為高效分析的儲存而設計。與行式格式相比，Parquet 在以下場景表現更佳：只需要讀取部分欄位時只需讀取對應列、相同類型的值連續儲存可獲得更好的壓縮、以及列式儲存更適合向量化的列處理。

## 使用 pyarrow 處理 Parquet

```python
import pyarrow.parquet as pq
import pandas as pd

# 讀取
table = pq.read_table('data.parquet')
df = table.to_pandas()

# 寫入
df.to_parquet('output.parquet', engine='pyarrow')
```

## 分割區和壓縮

Parquet 支援分割區儲存，按某欄位分目錄儲存，加速查詢。常用壓縮編碼包括：SNAPPY（平衡速度和壓縮率）、GZIP（更高壓縮率）、或 ZSTD（阿里巴巴開源，高壓縮比）。選擇時要根據查詢模式和儲存成本權衡。

## 資料湖架構中的 Parquet

在資料湖架構中，Parquet 是常見的儲存格式。配合 Delta Lake 或 Apache Iceberg，可提供 ACID 事務、時間旅行查詢、和 schema 演化能力。這使得資料湖不僅是儲存，更具備資料庫的管理能力。

## 參考資源

- Parquet Format：https://www.google.com/search?q=Apache+Parquet+format
- Delta Lake：https://www.google.com/search?q=Delta+Lake+data+lake