# 主題五：NoSQL 的萌芽

## 非關聯式資料庫興起

2007 年，NoSQL 資料庫開始嶄露頭角。這些非傳統的資料庫挑戰了關聯式模型的假設，為特定場景提供了更靈活和可擴展的解決方案。

## NoSQL 的驅動因素

### 網路規模的挑戰

```python
"""
為什麼需要 NoSQL？
"""

def why_nosql():
    challenges = {
        "規模問題": "Web 2.0 時代需要處理 PB 級資料",
        "擴展性": "RDBMS 難以水平擴展",
        "彈性": "固定 Schema 不夠靈活",
        "可用性": "需要更高的可用性",
        "效能": "大量寫入時 RDBMS 成為瓶頸",
    }

    print("傳統 RDBMS 的挑戰：")
    for issue, desc in challenges.items():
        print(f"  {issue}: {desc}")

    solutions = {
        "鍵值儲存": "簡單查詢、極高效能",
        "文件資料庫": "靈活 Schema、文件導向",
        "列儲存": "大規模資料、寬欄位",
        "圖資料庫": "複雜關聯、社交網路",
    }

    print("\nNoSQL 解決方案：")
    for db_type, desc in solutions.items():
        print(f"  {db_type}: {desc}")

why_nosql()
```

## NoSQL 的 CAP 定理

```markdown
# CAP 定理

任何分散式系統只能同時滿足以下三個中的兩個：

1. Consistency（一致性）
   - 所有節點看到相同的資料

2. Availability（可用性）
   - 每個請求都收到回應

3. Partition Tolerance（分隔容忍）
   - 系統在網路分割時仍能運作

# 常見選擇

CP（犧牲可用性）：
- BigTable
- HBase
- Redis

AP（犧牲一致性）：
- Cassandra
- CouchDB
- DynamoDB
```

## 鍵值儲存

### Redis 概念

```python
# Redis 鍵值操作概念
def redis_operations():
    operations = {
        "SET": "設定鍵值",
        "GET": "取得值",
        "DEL": "刪除鍵",
        "INCR": "遞增計數器",
        "EXPIRE": "設定過期時間",
    }

    print("Redis 基本操作：")
    for cmd, desc in operations.items():
        print(f"  {cmd}: {desc}")

redis_operations()
```

### 使用場景

```markdown
# Redis 適合的場景
- 會話儲存（Session Store）
- 快取層（Cache Layer）
- 即時排行榜
- 訊息佇列
- 簡單計數器
```

## 文件資料庫

### MongoDB 文件結構

```python
"""
MongoDB 文件範例
"""

def mongo_document():
    user_doc = {
        "_id": "ObjectId(...)",
        "name": "John Doe",
        "email": "john@example.com",
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "zip": "10001"
        },
        "tags": ["premium", "early-adopter"],
        "orders": [
            {"order_id": 1, "total": 99.99},
            {"order_id": 2, "total": 149.99}
        ],
        "created_at": "2007-01-15T10:30:00Z"
    }

    print("MongoDB 文件範例：")
    print(f"姓名: {user_doc['name']}")
    print(f"地址: {user_doc['address']['city']}")
    print(f"第一筆訂單: {user_doc['orders'][0]}")

mongo_document()
```

### CouchDB 特點

```json
// CouchDB 文件（JSON）
{
    "_id": "user_123",
    "_rev": "1-abc123",
    "type": "user",
    "name": "John",
    "preferences": {
        "theme": "dark",
        "notifications": true
    }
}
```

## 列儲存資料庫

### Cassandra 資料模型

```python
"""
Cassandra 列儲存概念
"""

def cassandra_concepts():
    print("""
Cassandra Keyspace -> Column Family -> Column

Keyspace:   相當於資料庫
Column:     (name, value, timestamp)
Row:        根據 Key 組織的 Column 集合
Column Family: 相當於資料表
    """)

    print("\n Wide Column 範例：")
    row = {
        "user_123": {
            "name": "John",
            "email": "john@example.com",
            "order_2007_01": "order_details...",
            "order_2007_02": "order_details...",
            "order_2007_03": "order_details...",
        }
    }
    print(f"使用者 123 的所有訂單：{len(row['user_123'])} 筆")

cassandra_concepts()
```

## NoSQL 的未來

### 與 RDBMS 的比較

| 方面 | RDBMS | NoSQL |
|------|-------|-------|
| 資料模型 | 固定Schema | 靈活Schema |
| 查詢語言 | SQL | 各有不同的 API |
| 擴展方式 | 垂直 | 水平 |
| 事務 | ACID | 最終一致 |
| 適用場景 | 結構化資料 | 大規模、非結構化 |

### 混合使用

```python
"""
NoSQL + RDBMS 混合架構

通常的做法：
- RDBMS：用於核心業務資料（訂單、使用者）
- Redis：用於快取和 session
- MongoDB：用於日誌和分析
- Cassandra：用於時間序列資料
"""
```

## 結語

NoSQL 的興起不是要完全取代關聯式資料庫，而是為特定場景提供了更適合的選擇。2007 年，這個運動剛剛開始，但已經預示了未來十年資料庫技術的多樣化發展。

---

*延伸閱讀：*
- [NoSQL 資料庫介紹](https://developers.google.com/search/?q=nosql+databases)
- [CAP 定理](https://developers.google.com/search/?q=cap+theorem)*