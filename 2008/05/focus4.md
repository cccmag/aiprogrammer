# MongoDB 與 JSON 文件儲存

## MongoDB 概述

MongoDB 是一個文件導向的 NoSQL 資料庫，使用 JSON 類似的 BSON 格式儲存文件。2008 年 MongoDB 開始開發，2009 年發布首個版本。

### 特點

- **文件儲存**：靈活的文件結構
- **高性能**：記憶體映射儲存
- **豐富查詢**：支援複雜查詢
- **水平擴展**：副本集和分片

## 安裝與設定

### 安裝 MongoDB

```bash
# Ubuntu
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
echo "deb http://downloads.mongodb.org/osx/10gen/" | sudo tee /etc/apt/sources.list.d/mongodb.list
sudo apt-get update
sudo apt-get install mongodb-stable
```

### 啟動服務

```bash
# 啟動 MongoDB
mongod --dbpath /data/db --port 27017

# 連接客戶端
mongo
```

## 基本操作

### 建立資料庫

```javascript
// 選擇或建立資料庫
use mydb

// 當前資料庫
db

// 列出所有資料庫
show dbs
```

### 文件操作（CRUD）

```javascript
// 插入文件
db.users.insert({
    name: "John",
    age: 30,
    email: "john@example.com",
    tags: ["python", "mongodb"],
    address: {
        city: "Taipei",
        country: "Taiwan"
    }
})

// 查詢文件
db.users.find()
db.users.findOne({ name: "John" })

// 更新文件
db.users.update(
    { name: "John" },
    { $set: { age: 31 } }
)

// 刪除文件
db.users.remove({ name: "John" })
```

## Python API

### 使用 pymongo

```python
from pymongo import MongoClient

# 連接到伺服器
client = MongoClient('localhost', 27017)
db = client['mydb']

# 插入文件
user = {
    'name': 'John',
    'age': 30,
    'email': 'john@example.com'
}
db.users.insert_one(user)

# 查詢
user = db.users.find_one({'name': 'John'})
print(user['email'])

# 查詢多個
for user in db.users.find({'age': {'$gte': 25}}):
    print(user['name'])

# 更新
db.users.update_one(
    {'name': 'John'},
    {'$set': {'age': 31}}
)

# 刪除
db.users.delete_one({'name': 'John'})
```

## 查詢運算子

### 比較運算子

```python
# 等於（預設）
db.users.find({'age': 30})

# 大於
db.users.find({'age': {'$gt': 25}})

# 小於
db.users.find({'age': {'$lt': 30}})

# 範圍
db.users.find({'age': {'$gte': 25, '$lte': 35}})
```

### 邏輯運算子

```python
# 或
db.users.find({'$or': [{'name': 'John'}, {'name': 'Mary'}]})

# 和
db.users.find({'age': {'$gte': 25}, 'name': 'John'})

# 非
db.users.find({'age': {'$not': {'$lt': 30}}})
```

### 陣列運算子

```python
# 包含
db.users.find({'tags': 'python'})

# 全部包含
db.users.find({'tags': {'$all': ['python', 'mongodb']}})

# 陣列長度
db.users.find({'tags': {'$size': 3}})
```

## 文件結構設計

### 嵌入式 vs 引用

```python
# 嵌入式（適合一對少數）
user = {
    'name': 'John',
    'address': {
        'city': 'Taipei',
        'street': '123 Main St'
    }
}

# 引用式（適合一對多或正規化）
orders = [
    {'order_id': 1, 'user_id': 'user123', 'total': 100},
    {'order_id': 2, 'user_id': 'user123', 'total': 200}
]

# 需要 JOIN 時
for order in db.orders.find({'user_id': user_id}):
    print(order)
```

### 設計原則

| 原則 | 說明 |
|------|------|
| 避免過度嵌入式 | 文件過大影響效能 |
| 考量查詢模式 | 讀多寫少可嵌入式 |
| 考慮一致性 | 引用式需要多次查詢 |

## 索引

### 建立索引

```python
# 單欄索引
db.users.create_index('name')

# 複合索引
db.users.create_index([('age', 1), ('name', -1)])

# 唯一索引
db.users.create_index('email', unique=True)

# 文字索引
db.users.create_index([('description', 'text')])
```

### 查詢計畫

```python
# 解釋查詢
db.users.find({'name': 'John'}).explain()
```

## 副本集

### 設定副本集

```python
# 初始化副本集
rs.initiate({
    '_id': 'myReplSet',
    'members': [
        { '_id': 0, 'host': 'localhost:27017' },
        { '_id': 1, 'host': 'localhost:27018' },
        { '_id': 2, 'host': 'localhost:27019' }
    ]
})
```

### 讀取偏好

```python
# 從副本讀取
db.users.find(read_preference=ReadPreference.SECONDARY)
```

## 結論

MongoDB 以其靈活的文件和豐富的查詢功能，成為最受歡迎的 NoSQL 資料庫之一。其副本集和水平擴展能力支援大規模部署。

---

**延伸閱讀**

- [CouchDB 文件資料庫](focus3.md)
- [Cassandra 列式資料庫](focus5.md)
- [MongoDB+documentation](https://www.google.com/search?q=MongoDB+documentation)