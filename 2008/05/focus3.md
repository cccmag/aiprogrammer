# 文件資料庫 CouchDB

## CouchDB 概述

Apache CouchDB 是一個文件導向的 NoSQL 資料庫，使用 JSON 格式儲存文件。2008 年 CouchDB 0.8 發布，開始受到關注。

### 特點

- **文件儲存**：JSON 格式
- **RESTful API**：使用 HTTP 操作
- **離線優先**：支援離線操作和同步
- **MapReduce**：用於查詢和聚合

## 安裝與設定

### 安裝 CouchDB

```bash
# Ubuntu
sudo apt-get install couchdb

# 或從原始碼編譯
wget http://archive.apache.org/dist/couchdb/0.8.0/apache-couchdb-0.8.0.tar.gz
./configure && make && sudo make install
```

### 啟動服務

```bash
# 啟動 CouchDB
sudo -u couchdb /usr/local/bin/couchdb

# 驗證
curl http://127.0.0.1:5984/
```

## 基本操作

### 建立資料庫

```bash
# 建立資料庫
curl -X PUT http://127.0.0.1:5984/mydb

# 列出所有資料庫
curl http://127.0.0.1:5984/_all_dbs
```

### 文件操作（CRUD）

```bash
# 建立文件
curl -X PUT http://127.0.0.1:5984/mydb/doc1 \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "age": 30}'

# 讀取文件
curl http://127.0.0.1:5984/mydb/doc1

# 更新文件
curl -X PUT http://127.0.0.1:5984/mydb/doc1 \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "age": 31, "_rev": "1-xxx"}'

# 刪除文件
curl -X DELETE http://127.0.0.1:5984/mydb/doc1?rev=2-xxx
```

## Python API

### 使用 couchdb-python

```python
import couchdb

# 連接到伺服器
server = couchdb.Server('http://127.0.0.1:5984/')

# 建立資料庫
db = server.create('mydb')

# 或連接到現有資料庫
db = server['mydb']

# 建立文件
doc = {
    '_id': 'user123',
    'name': 'John',
    'age': 30,
    'tags': ['python', 'database']
}
db.save(doc)

# 讀取文件
doc = db['user123']
print(doc['name'])

# 更新文件
doc['age'] = 31
db.save(doc)

# 刪除文件
del db['user123']

# 查詢
for doc in db:
    print(doc)
```

## MapReduce 檢視

### 設計文件

CouchDB 使用 JavaScript 定義 MapReduce：

```javascript
// _design/users
{
  "_id": "_design/users",
  "views": {
    "by_age": {
      "map": "function(doc) { if (doc.age) { emit(doc.age, doc.name); } }",
      "reduce": "_count"
    },
    "by_name": {
      "map": "function(doc) { if (doc.name) { emit(doc.name, doc); } }"
    }
  }
}
```

### 查詢檢視

```bash
# 查詢檢視
curl http://127.0.0.1:5984/mydb/_design/users/_view/by_age

# 带條件
curl "http://127.0.0.1:5984/mydb/_design/users/_view/by_age?startkey=20&endkey=30"
```

### Python 查詢

```python
# 查詢檢視
results = db.view('users/by_age', group=True)

for row in results:
    print(f"Age {row.key}: {row.value} users")
```

## Mango 查詢

CouchDB 2.0+ 支援 Mango（類似 MongoDB 的查詢）：

```python
# 使用 Mango 查詢
selector = {
    'age': {'$gte': 25},
    'tags': {'$in': ['python']}
}

for doc in db.find(selector):
    print(doc)
```

## 同步與複製

### 本地複製

```bash
# 複製資料庫
curl -X POST http://127.0.0.1:5984/_replicate \
  -H "Content-Type: application/json" \
  -d '{"source": "mydb", "target": "mydb_backup"}'
```

### 遠端同步

```python
# 即時同步
from couchdb.replication import replicate

replicate('http://localhost:5984/mydb',
          'http://remote:5984/mydb',
          continuous=True)
```

## 離線支援

### PouchDB（瀏覽器端）

```javascript
var db = new PouchDB('mydb');

// 與 CouchDB 同步
db.sync('http://localhost:5984/mydb');

// 離線操作
db.put({
    _id: 'offline_doc',
    data: 'stored offline'
});
```

## 結論

CouchDB 的 RESTful API 和離線優先設計使其成為 Web 和行動應用的理想選擇。文件同步功能特別適合需要離線支援的場景。

---

**延伸閱讀**

- [MongoDB 與 JSON 文件儲存](focus4.md)
- [NoSQL 程式實作](focus_code.md)
- [CouchDB+documentation](https://www.google.com/search?q=CouchDB+documentation)