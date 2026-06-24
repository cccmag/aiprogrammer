# NoSQL 運動：文件資料庫興起

## NoSQL 的興起

### 2009 年的 NoSQL

```markdown
# 2009 年 NoSQL 地圖

Key-Value 儲存：
- Redis（快速成長）
- Memcached（經典）
- Riak（分散式）

文件資料庫：
- MongoDB 1.0（8月）
- CouchDB 0.10

列儲存：
- Cassandra 0.4
- HBase（穩定）

圖資料庫：
- Neo4j 1.0
```

## MongoDB 1.0

### 發布內容

```python
# MongoDB 1.0 核心功能

# 文件儲存
db.users.insert({
    "name": "張三",
    "age": 30,
    "address": {
        "city": "台北"
    }
})

# 動態查詢
db.users.find({"age": {"$gt": 18}})

# 索引
db.users.ensure_index("name")

# 副本集
rs.initiate({
    _id: "myapp",
    members: [
        {_id: 0, host: "mongo1:27017"},
        {_id: 1, host: "mongo2:27017"}
    ]
})
```

## CouchDB

### 特色

```python
# CouchDB HTTP API

# 建立資料庫
curl -X PUT http://localhost:5984/mydb

# 新增文件
curl -X POST http://localhost:5984/mydb \
  -H "Content-Type: application/json" \
  -d '{"name": "張三"}'

# 查詢
curl http://localhost:5984/mydb/_all_docs
```

## NoSQL 的價值

```markdown
# NoSQL 的價值

1. 規模化
   - 水平擴展簡單
   - 處理巨量資料

2. 彈性
   - 無固定 Schema
   - 快速迭代

3. 高效能
   - 針對特定場景優化
   - 簡單的讀寫操作

4. 高可用
   - 自動故障轉移
   - 最終一致性
```

## CAP 理論

```markdown
# NoSQL 的一致性選擇

CP（一致 + 分區容錯）：
- MongoDB
- HBase
- Redis

AP（可用 + 分區容錯）：
- Cassandra
- CouchDB
- DynamoDB
```

## 結語

2009 年 NoSQL 運動興起，改變了資料庫的格局。

---

*本篇文章為「AI 程式人雜誌 2009 年 12 月號」焦點系列之一。*