# NoSQL 與 SQL 的取捨

## 選擇的困境

選擇資料庫是系統設計中最基礎但也是最重要的決定之一。多年來，關聯式資料庫（SQL）一直是主流選擇，但 NoSQL 的興起提供了另一種可能。讓我們從多個角度來分析何時該選擇哪種技術。

## 資料模型對比

### SQL 的結構化世界

關聯式資料庫以表格為基礎，每個表格有固定的 Schema。資料以行列形式儲存，表之間通過外鍵關聯。這種結構的優點是：

- **嚴格的資料一致性**：ACID 事務保障
- **豐富的查詢能力**：複雜的 JOIN、聚合、子查詢
- **成熟的工具生態**：大量的管理工具和最佳化技術

```sql
-- SQL 的強大之處
SELECT
    u.name,
    COUNT(o.order_id) as order_count,
    SUM(o.amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE u.created_at > '2023-01-01'
GROUP BY u.user_id
HAVING COUNT(o.order_id) > 5
ORDER BY total_spent DESC
LIMIT 10;
```

### NoSQL 的彈性世界

NoSQL 資料庫提供了不同的資料模型：

- **文件資料庫**：JSON 格式，無需 Schema
- **鍵值資料庫**：簡單的鍵-值對
- **列族資料庫**：動態列，高壓縮比
- **圖形資料庫**：節點和邊，擅長關聯查詢

```python
# MongoDB 的查詢
db.users.aggregate([
    { $match: { created_at: { $gt: datetime(2023,1,1) } } },
    { $lookup: {
        from: "orders",
        localField: "user_id",
        foreignField: "user_id",
        as: "user_orders"
    }},
    { $project: {
        name: 1,
        order_count: { $size: "$user_orders" },
        total_spent: { $sum: "$user_orders.amount" }
    }},
    { $match: { order_count: { $gt: 5 } } },
    { $sort: { total_spent: -1 } },
    { $limit: 10 }
])
```

## 效能比較

### 讀取效能

| 場景 | SQL | NoSQL |
|------|-----|-------|
| 簡單鍵查詢 | 快 | 非常快 |
| 複雜 JOIN | 強大 | 有限 |
| 大量掃描 | 一般 | 可透過分片優化 |

### 寫入效能

| 場景 | SQL | NoSQL |
|------|-----|-------|
| 單一記錄寫入 | 快 | 快 |
| 批次寫入 | 一般 | 可優化 |
| 分散式寫入 | 需要額外設定 | 原生支援 |

## 一致性模型

### SQL：強一致性

```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;
-- 保證原子性，全部成功或全部失敗
```

### NoSQL：多樣的一致性選擇

```python
# MongoDB：可配置的一致性
# 快速寫入（可能丟失）
collection.insert_one(doc, write_concern={'w': 0})

# 強一致性寫入
collection.insert_one(doc, write_concern={'w': 'majority'})
```

## 擴展方式

### SQL：垂直擴展

傳統上，SQL 資料庫通過更強大的硬體來提升效能（垂直擴展）。也有一些分散式 SQL 解決方案：

- **Google Spanner**：全球分散式 SQL
- **CockroachDB**：分散式 SQL
- **TiDB**：分散式 MySQL 相容資料庫

### NoSQL：水平擴展

NoSQL 的設計從一開始就考慮了水平擴展：

```python
# MongoDB 分片範例
shards = [
    "shard1:27017",
    "shard2:27017",
    "shard3:27017"
]

# 自動分發資料到多個分片
collection = db['orders']
collection.create_index([("customer_id", 1), ("created_at", -1)])
```

## 選擇指南

### 適合使用 SQL 的場景

1. **交易系統**：需要嚴格 ACID 的金融系統
2. **複雜查詢**：需要多表 JOIN 和複雜聚合
3. **結構穩定**：Schema 很少變化
4. **報表分析**：需要複雜的 SQL 分析能力
5. **團隊熟悉度**：團隊對 SQL 有豐富經驗

### 適合使用 NoSQL 的場景

1. **快速迭代**：需求變動快，Schema 需要彈性
2. **大規模資料**：需要水平擴展能力
3. **高並發寫入**：寫入負載極高
4. **靈活資料結構**：文檔結構差異大
5. **快取層**：作為讀取密集型的快取

## 混合使用策略

現代架構常常同時使用 SQL 和 NoSQL：

```
+------------------+
|    應用層        |
+--------+---------+
|                 |
v                 v
+--------+   +--------+
|  SQL   |   | NoSQL  |
+--------+   +--------+
|                  |
v                  v
+--------+   +--------+
| 主資料 |   | 快取/日誌|
+--------+   +--------+
```

常見模式：
- **SQL 主資料庫 + NoSQL 快取**：Redis 作為熱門資料的快取
- **SQL + NoSQL 文件儲存**：MySQL 存交易資料，MongoDB 存用戶生成內容
- **NoSQL + SQL 分析**：MongoDB 存原始資料，PostgreSQL 做分析

## 結論

沒有絕對的「最好」，只有「更適合」。理解兩者的優缺點，根據具體需求做出選擇，是每個開發者必須掌握的能力。