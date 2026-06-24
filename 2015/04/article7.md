# 文件資料庫的查詢優化

## 前言

文件資料庫提供了靈活的資料模型，但如果不注意查詢優化，可能會遇到效能問題。本文探討如何優化文件資料庫的查詢效能。

## 索引策略

### 基本索引

索引是查詢優化的基礎：

```javascript
// MongoDB 索引範例
// 單欄位索引
db.users.createIndex({ "email": 1 }, { unique: true })

// 複合索引
db.orders.createIndex({ "customer_id": 1, "created_at": -1 })

// 陣列索引
db.articles.createIndex({ "tags": 1 })

// 文字索引
db.posts.createIndex({ "content": "text", "title": "text" })
```

### 複合索引的順序

複合索引中欄位的順序很重要：

```javascript
// 查詢：{ status: "active", created_at: { $gt: ... }, name: ... }
// 好的索引設計
db.orders.createIndex({ "status": 1, "created_at": -1, "name": 1 })

// 索引最左前綴原則
// 這個索引支援：
// - { status: "active" }
// - { status: "active", created_at: { $gt: ... } }
// - { status: "active", created_at: { $gt: ... }, name: ... }
// 但不支援：
// - { created_at: { $gt: ... } }
```

## 查詢模式分析

### 使用 explain() 分析

```javascript
// 分析查詢計劃
db.orders.find({ "customer_id": "C123" }).explain("executionStats")

// 輸出範例解讀
{
    "executionStats": {
        "nReturned": 150,
        "executionTimeMillis": 45,
        "totalKeysExamined": 150,
        "totalDocsExamined": 150,
        "winningPlan": {
            "stage": "FETCH",
            "inputStage": {
                "stage": "IXSCAN",
                "keyPattern": { "customer_id": 1 }
            }
        }
    }
}

// 理想情況：totalDocsExamined == nReturned（覆蓋查詢）
```

### 避免全集合掃描

```python
# 不好：沒有利用索引
for user in db.users.find({"status": "active"}):
    process(user)

# 好：確保有合適的索引
if db.users.find({"status": "active"}).count() > 0:
    # 使用索引的查詢

# 更好：使用 limit
active_users = list(db.users.find({"status": "active"}).limit(1000))
```

## 投影優化

### 只取需要的欄位

```javascript
// 不需要傳回整個文件
// 僅取需要的欄位
db.users.find(
    { "status": "active" },
    { "name": 1, "email": 1, "_id": 0 }
)
```

### 覆蓋查詢

當索引包含查詢需要的所有欄位時，MongoDB 可以直接從索引回傳資料，不需要讀取文件：

```javascript
// 建立覆蓋索引
db.orders.createIndex(
    { "customer_id": 1, "status": 1 },
    { name: "covering_index" }
)

// 這個查詢可以直接從索引回傳
db.orders.find(
    { "customer_id": "C123", "status": "completed" },
    { "_id": 0, "status": 1, "amount": 1 }
)
```

## 聚合管道優化

### 階段順序

```javascript
// 好的順序：先篩選再聚合
db.orders.aggregate([
    { $match: { status: "completed" } },  // 先篩選
    { $group: { _id: "$customer_id", total: { $sum: "$amount" } } },
    { $sort: { total: -1 } },
    { $limit: 10 }
])

// 不好：先排序再篩選
db.orders.aggregate([
    { $sort: { created_at: -1 } },
    { $match: { status: "completed" } }
])
```

### 使用 $lookup 優化

```javascript
// 關聯查詢
db.orders.aggregate([
    { $match: { "customer_id": "C123" } },
    { $lookup: {
        from: "customers",
        localField: "customer_id",
        foreignField: "_id",
        as: "customer_info"
    }},
    { $unwind: "$customer_info" },
    { $project: {
        order_id: 1,
        amount: 1,
        "customer_info.name": 1
    }}
])
```

## 快取策略

### Redis 快取層

```python
import redis
import json
from pymongo import MongoClient

client = MongoClient()
db = client['mydb']
cache = redis.Redis(decode_responses=True)

def get_user_with_cache(user_id):
    cache_key = f"user:{user_id}"

    # 先查快取
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    # 快取未命中，查詢資料庫
    user = db.users.find_one({"_id": user_id})
    if user:
        cache.setex(cache_key, 3600, json.dumps(user))

    return user
```

## 分頁優化

### 基於鍵的分頁

```javascript
// 基於 _id 的分頁（高效）
function get_page_cursor(last_id, limit=20):
    if last_id:
        return db.articles.find({ "_id": { "$lt": last_id } })
    return db.articles.find()

// 假設 last_id 是 ObjectId
page = list(get_page_cursor(last_id).limit(20))
```

### 基於日期的分頁

```javascript
function get_orders_by_date(before_date, limit=20):
    query = {}
    if before_date:
        query["created_at"] = { "$lt": before_date }

    return db.orders.find(query).sort({ created_at: -1 }).limit(limit)
```

## 監控與維護

### 監控慢查詢

```javascript
// 開啟 profiling
db.setProfilingLevel(2, { slowms: 100 })

// 查詢慢查詢日誌
db.system.profile.find().sort({ millis: -1 }).limit(10)
```

### 定期分析

```python
def analyze_collections():
    """分析並優化集合"""
    db = client['mydb']

    # 收集統計資訊
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        stats = collection.stats()

        # 找出需要優化的集合
        if stats.get('avgObjSize', 0) > 16 * 1024 * 1024:  # > 16MB
            print(f"{collection_name}: 文件過大")
```

## 結論

文件資料庫的查詢優化需要綜合考慮索引設計、查詢模式、網路傳輸等多個因素。定期監控和分析是保持效能的關鍵。