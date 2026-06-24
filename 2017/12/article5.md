# 資料庫技術：SQLite, PostgreSQL, NoSQL

## 前言

2017 年資料庫領域繼續發展，傳統 SQL 資料庫和 NoSQL 都有重要更新。

## SQLite 3.21

```sql
-- SQLite 3.21 更新

-- JSON 函式增強
SELECT json_extract('{"name": "John"}', '$.name');

-- 效能改進
PRAGMA cache_size = -2000;  -- 2MB cache

-- 索引優化
CREATE INDEX idx ON users(email, id);
```

## PostgreSQL 10

```sql
-- PostgreSQL 10 新特性

-- 原生分區表
CREATE TABLE sales (
    id SERIAL,
    date DATE,
    amount NUMERIC
) PARTITION BY RANGE (date);

-- 邏輯複製
-- pglogical 擴展

-- 全文搜尋改進
-- 支援 JSON 和 JSONB

-- 並行查詢增強
EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT TEXT)
SELECT * FROM large_table;
```

## NoSQL 資料庫

```
┌─────────────────────────────────────────────────────────┐
│              2017 年 NoSQL 資料庫                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  MongoDB 3.6 (2017年11月)                              │
│  - 改進的複製集                                         │
│  - 變更流 (Change Streams)                              │
│  - 更好的索引                                           │
│                                                         │
│  Redis 4.0 (2017年9月)                                 │
│  - 模組系統                                             │
│  - 記憶體優化                                           │
│  - Lua 腳本改進                                         │
│                                                         │
│  Cassandra 3.11                                        │
│  - 效能提升                                            │
│  - 更好的工具                                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 時序資料庫

```python
# InfluxDB (時序資料庫)

from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'admin', 'admin')

# 寫入時序資料
json_body = [
    {
        "measurement": "cpu_load",
        "tags": {"host": "server01"},
        "time": "2017-12-01T12:00:00Z",
        "fields": {"value": 0.5}
    }
]

client.write_points(json_body)

# 查詢
query = 'SELECT * FROM cpu_load WHERE host="server01"'
result = client.query(query)
```

## NewSQL 興起

2017 年見證了 NewSQL 資料庫的興起：

- **Google Spanner**：全球化分散式 SQL
- **CockroachDB**：分散式 SQL
- **TiDB**：MySQL 相容的分散式資料庫

---

**延伸閱讀**

- [PostgreSQL 10 Release](https://www.google.com/search?q=PostgreSQL+10+release)
- [MongoDB 3.6 Release](https://www.google.com/search?q=MongoDB+3.6+release)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*