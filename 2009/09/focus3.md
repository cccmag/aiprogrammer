# MongoDB 1.0 發布：文件資料庫的里程碑

## MongoDB 的起源

### 10gen 公司的成立

MongoDB 由 10gen 公司（前身為 ObjectKnowledge）開發，2007 年開始研發，2009 年正式發布 1.0 版本。

```markdown
MongoDB 命名由來：

「Humongous」- 巨大的

因為 MongoDB 設計用於處理巨量資料。
```

## MongoDB 1.0 的核心功能

### 文件儲存

```python
# MongoDB 文件操作

from pymongo import MongoClient

client = MongoClient()
db = client.myapp

# 插入文件
db.users.insert({
    "name": "張三",
    "age": 30,
    "email": "zhang@example.com"
})

# 查詢
for user in db.users.find({"age": {"$gt": 18}}):
    print(user["name"])

# 更新
db.users.update(
    {"name": "張三"},
    {"$set": {"age": 31}}
)

# 刪除
db.users.remove({"name": "張三"})
```

### JavaScript Shell

```javascript
// MongoDB Shell 是 MongoDB 的一大特色

// 啟動 Shell
$ mongo

// 基本操作
> use myapp
switched to db myapp

> db.users.insert({name: "張三", age: 30})
> db.users.find()
{ "_id": ObjectId("..."), "name": "張三", "age": 30 }

> db.users.findOne({name: "張三"})
> db.users.update({name: "張三"}, {$set: {age: 31}})
> db.users.remove({name: "張三"})
```

### 索引

```python
# MongoDB 索引

# 單一欄位索引
db.users.ensure_index("name")

# 複合索引
db.users.ensure_index([("name", 1), ("age", -1)])

# 唯一索引
db.users.ensure_index("email", unique=True)

# 地理空間索引
db.places.ensure_index([("location", "2dsphere")])
```

## MongoDB 的特色

### 動態查詢

```python
# MongoDB 的靈活查詢

# 無需預先定義查詢
db.users.find({"name": "張三"})
db.users.find({"age": {"$gt": 18, "$lt": 65}})
db.users.find({"tags": {"$all": ["vip", "active"]}})
```

### 自動切片

```python
# MongoDB 分片（Sharding）

# 切片鍵
db.users.ensure_index({"user_id": "hashed"})

# 切片配置
sh.addShard("shard1.example.com:27017")
sh.addShard("shard2.example.com:27017")

# 開啟切片
sh.enableSharding("myapp")
sh.shardCollection("myapp.users", {"user_id": "hashed"})
```

### 聚合框架

```python
# MongoDB 聚合

# 計算每個年齡段的人數
db.users.aggregate([
    {"$group": {
        "_id": {
            "$floor": {"$divide": ["$age", 10]}
        },
        "count": {"$sum": 1}
    }},
    {"$sort": {"_id": 1}}
])
```

## MongoDB 1.0 的限制

```markdown
2009 年的 MongoDB 1.0 限制：

1. 無事務
   - 單文件原子性
   - 無跨文件事務

2. 無 JOIN
   - 需要手動處理
   - 或使用 MapReduce

3. 記憶體使用
   - 使用記憶體映射檔案
   - 需要足夠記憶體

4. 成熟度
   - 1.0 版本相對新
   - 生態系統在建構中
```

## MongoDB 的生態

```markdown
2009 年的 MongoDB 生態：

1. 驅動程式
   - JavaScript (原生)
   - Python (pymongo)
   - Ruby
   - Java

2. 管理工具
   - MongoDB Shell
   - PhpMoAdmin
   - RockMongo

3. ORM
   - Mongoid (Ruby)
   - Doctrine MongoDB (PHP)

4. 社群
   - MongoDB User Groups
   - 線上文件
```

## 結語

MongoDB 1.0 的發布標誌著文件資料庫進入實用階段。其 JavaScript Shell 和靈活的文件模型深受開發者喜愛。

下一篇文章將介紹 CouchDB 和另一條文件資料庫的路線。

---

## 延伸閱讀

- [MongoDB 官方網站](https://www.google.com/search?q=MongoDB+official+website)
- [MongoDB 1.0 發布公告](https://www.google.com/search?q=MongoDB+1.0+release)
- [MongoDB 查詢語言](https://www.google.com/search?q=MongoDB+query+language)

---

*本篇文章為「AI 程式人雜誌 2009 年 9 月號」焦點系列之一。*