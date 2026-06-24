# NoSQL 程式實作

## 文件資料庫操作範例

本文件提供 MongoDB 和 CouchDB 的 Python 操作範例。

## MongoDB 示範

```python
from pymongo import MongoClient

def demo_mongodb():
    """MongoDB 操作示範"""
    client = MongoClient('localhost', 27017)
    db = client['demo']

    # 插入文件
    doc = {
        'name': 'John',
        'age': 30,
        'tags': ['python', 'mongodb'],
        'address': {'city': 'Taipei', 'country': 'Taiwan'}
    }
    result = db.users.insert_one(doc)
    print(f"Inserted: {result.inserted_id}")

    # 查詢
    user = db.users.find_one({'name': 'John'})
    print(f"Found: {user}")

    # 更新
    db.users.update_one({'name': 'John'}, {'$set': {'age': 31}})

    # 刪除
    db.users.delete_one({'name': 'John'})

    client.close()

if __name__ == "__main__":
    demo_mongodb()
```

## CouchDB 示範

```python
import couchdb

def demo_couchdb():
    """CouchDB 操作示範"""
    server = couchdb.Server('http://localhost:5984/')
    db = server['demo']

    # 插入文件
    doc = {
        'name': 'Mary',
        'age': 25,
        'tags': ['python', 'couchdb']
    }
    db.save(doc)
    print(f"Inserted: {doc['_id']}")

    # 查詢
    for doc in db:
        print(doc)

if __name__ == "__main__":
    demo_couchdb()
```

## Redis 示範

```python
import redis

def demo_redis():
    """Redis 操作示範"""
    r = redis.Redis(host='localhost', port=6379)

    # 字串操作
    r.set('name', 'John')
    print(f"GET: {r.get('name')}")

    # 計數器
    r.set('counter', 0)
    r.incr('counter')
    print(f"Counter: {r.get('counter')}")

    # 雜湊
    r.hset('user:1', 'name', 'John')
    r.hset('user:1', 'email', 'john@example.com')
    print(f"Hash: {r.hgetall('user:1')}")

    # 列表
    r.lpush('mylist', 'a', 'b', 'c')
    print(f"List: {r.lrange('mylist', 0, -1)}")

    # 集合
    r.sadd('tags', 'python', 'mongodb')
    print(f"Set: {r.smembers('tags')}")

    # 有序集合
    r.zadd('scores', {'Alice': 100, 'Bob': 90})
    print(f"Top: {r.zrevrange('scores', 0, 0, withscores=True)}")

    r.close()

if __name__ == "__main__":
    demo_redis()
```

## 執行說明

```bash
# 啟動 MongoDB
mongod --dbpath /data/db

# 啟動 CouchDB
couchdb

# 啟動 Redis
redis-server

# 執行示範
python3 nosql_demo.py
```

## 參考資源

- [MongoDB+Python](https://www.google.com/search?q=MongoDB+Python+tutorial)
- [CouchDB+Python](https://www.google.com/search?q=CouchDB+Python+tutorial)
- [Redis+Python](https://www.google.com/search?q=Redis+Python+tutorial)