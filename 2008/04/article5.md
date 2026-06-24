# 巨量資料時代的資料工程

## 資料工程的興起

隨著資料量爆炸性成長，資料工程成為一個專門領域。資料工程師負責建構和維護處理巨量資料的系統。

## 資料工程師的角色

### 與其他角色的比較

| 角色 | 主要關注 | 工具 |
|------|----------|------|
| 資料工程師 | 資料管道 | Hadoop, Spark |
| 資料科學家 | 分析與模型 | R, Python |
| 軟體工程師 | 產品系統 | Java, Go |
| DBA | 資料庫調優 | SQL |

## 巨量資料技術棧

### 資料收集層

```
┌─────────────────────────────────────┐
│         資料來源                      │
│  Web 應用  │  日誌  │  IoT  │  API   │
└────────────┴────────┴───────┴───────┘
              ↓
┌─────────────────────────────────────┐
│        收集與傳輸                      │
│   Flume  │  Sqoop  │  Kafka  │  ETL  │
└────────────┴────────┴───────┴───────┘
```

### 儲存層

- **HDFS**：原始資料儲存
- **HBase**：即時讀取
- **Kafka**：訊息佇列
- **S3**：雲端儲存

### 處理層

- **MapReduce**：批次處理
- **Spark**：記憶體內處理
- **Flink**：串流處理

### 分析層

- **Hive**：SQL 查詢
- **Impala**：快速 SQL
- **Presto**：跨來源查詢

## 資料管道設計

### ETL vs ELT

```
ETL: Extract → Transform → Load
         ↓
     在載入前轉換

ELT: Extract → Load → Transform
         ↓
     先載入再轉換（利用 MPP）
```

### 即時 vs 批次

| 類型 | 延遲 | 適用場景 |
|------|------|----------|
| 批次 | 分鐘到小時 | 報表、分析 |
| 即時 | 秒級 | 監控、推薦 |
| 串流 | 毫秒級 | 交易、報價 |

## 資料建模

### 資料倉庫建模

```
┌────────────────────────────────────────┐
│           資料倉庫架構                   │
├────────────────────────────────────────┤
│  STAGING → ODS → DATA MART → DATAMART │
│     原始     整合     部門       分析   │
└────────────────────────────────────────┘
```

### 星型與雪花模型

```sql
-- 星型模型
SELECT 產品.名稱, SUM(銷售.金額)
FROM 銷售
JOIN 產品 ON 銷售.產品ID = 產品.ID
JOIN 時間 ON 銷售.時間ID = 時間.ID
WHERE 時間.年份 = 2008
GROUP BY 產品.名稱

-- 維度表：產品、時間、地點
-- 事實表：銷售、庫存、訂單
```

## 資料品質

### 品質檢查點

```python
def validate_data(df):
    # 完整性檢查
    assert df.count() == expected_count

    # 一致性檢查
    assert df['status'].isin(['active', 'inactive']).all()

    # 準確性檢查
    assert (df['price'] >= 0).all()

    # 及時性檢查
    assert df['timestamp'].max() < current_time
```

### 資料品質監控

- 自動化品質檢測
- 異常告警
- 血統追蹤

## 效能優化

### 分割區策略

```sql
-- 按時間分割
PARTITION BY (dt STRING)

-- 按鍵雜湊分割
PARTITION BY HASH(user_id) PARTITIONS 10
```

### 壓縮與編碼

```java
// 啟用壓縮
conf.set("mapred.compress.map.output", "true");
conf.set("mapred.map.output.compression.codec",
         "org.apache.hadoop.io.compress.SnappyCodec");
```

## 安全與合規

### 資料安全

- 傳輸加密（TLS/SSL）
- 靜態加密
- 存取控制（Kerberos）

### 隱私保護

- 資料遮罩
- 脫敏處理
- GDPR 合規

## 結論

資料工程是巨量資料時代的基礎設施建設。一個設計良好的資料管道，能讓資料科學家和分析師更高效地工作。

---

**延伸閱讀**

- [Hadoop 與巨量資料處理](focus.md)
- [Data+engineering+tutorial](https://www.google.com/search?q=data+engineering+tutorial)