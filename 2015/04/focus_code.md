# 附加：NoSQL 實作範例

## 程式實作總覽

本期我們提供三個 NoSQL 資料庫的實作範例，分別展示 MongoDB、Redis 和 CouchDB 的基本操作。所有範例都使用 Python 編寫，可以直接在 Python 3 環境中運行。

## 環境準備

```bash
pip install pymongo redis couchdb
```

## MongoDB 操作範例

```python
#!/usr/bin/env python3
"""
MongoDB 基本操作範例
展示文件的新增、查詢、更新和刪除操作
"""

from pymongo import MongoClient
from datetime import datetime

def demo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['test']
    collection = db['users']

    collection.delete_many({})

    users = [
        {
            "name": "張小明",
            "email": "zhang@example.com",
            "age": 28,
            "tags": ["Python", "MongoDB"],
            "created_at": datetime.now()
        },
        {
            "name": "李小華",
            "email": "li@example.com",
            "age": 35,
            "tags": ["JavaScript", "Node.js"],
            "created_at": datetime.now()
        },
        {
            "name": "王小美",
            "email": "wang@example.com",
            "age": 24,
            "tags": ["Python", "Data Science"],
            "created_at": datetime.now()
        }
    ]

    result = collection.insert_many(users)
    print(f"插入 {len(result.inserted_ids)} 筆資料")

    all_users = list(collection.find())
    print(f"查詢所有使用者：{len(all_users)} 筆")

    python_users = list(collection.find({"tags": "Python"}))
    print(f"會 Python 的使用者：{len(python_users)} 筆")

    collection.update_one(
        {"name": "張小明"},
        {"$set": {"age": 29}}
    )

    updated_user = collection.find_one({"name": "張小明"})
    print(f"更新後的年齡：{updated_user['age']}")

    collection.delete_one({"name": "王小美"})
    remaining = collection.count_documents({})
    print(f"刪除後剩餘：{remaining} 筆")

    print("MongoDB 操作完成！")

if __name__ == "__main__":
    demo()
```

## Redis 操作範例

```python
#!/usr/bin/env python3
"""
Redis 基本操作範例
展示各種資料結構的使用：字串、雜湊、串列、集合
"""

import redis
import json

def demo():
    client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    client.flushdb()

    client.set('name', 'AI 程式人雜誌')
    print(f"字串操作 - name: {client.get('name')}")

    client.hset('user:1', mapping={
        'name': '張小明',
        'email': 'zhang@example.com',
        'role': 'admin'
    })
    user_info = client.hgetall('user:1')
    print(f"雜湊操作 - user:1: {user_info}")

    client.lpush('tasks', 'task1', 'task2', 'task3')
    tasks = client.lrange('tasks', 0, -1)
    print(f"串列操作 - tasks: {tasks}")

    client.sadd('tags', 'python', 'redis', 'mongodb', 'python')
    unique_tags = client.smembers('tags')
    print(f"集合操作 - tags: {unique_tags}")
    print(f"集合大小: {client.scard('tags')}")

    client.zadd('leaderboard', {'alice': 100, 'bob': 200, 'charlie': 150})
    top3 = client.zrevrange('leaderboard', 0, 2, withscores=True)
    print(f"有序集合操作 - leaderboard top 3: {top3}")

    client.setex('session:123', 3600, 'user_data_json')
    ttl = client.ttl('session:123')
    print(f"過期操作 - session:123 TTL: {ttl} 秒")

    print("Redis 操作完成！")

if __name__ == "__main__":
    demo()
```

## CouchDB 操作範例

```python
#!/usr/bin/env python3
"""
CouchDB 基本操作範例
展示文件的 CRUD 操作和視圖查詢
"""

import couchdb

def demo():
    try:
        server = couchdb.Server('http://localhost:5984')
    except:
        print("CouchDB 連線失敗，請確認 CouchDB 服務已啟動")
        print("本範例展示程式邏輯，實際執行需要 CouchDB 服務")
        return

    try:
        db = server.create('test_db')
    except couchdb.http.ResourceConflict:
        db = server['test_db']

    db.delete_many(doc['_id'] for doc in db)

    doc1 = {
        '_id': 'user:1',
        'type': 'user',
        'name': '張小明',
        'skills': ['Python', 'MongoDB']
    }

    doc_id, doc_rev = db.save(doc1)
    print(f"文件建立 - ID: {doc_id}, Rev: {doc_rev}")

    doc2 = {
        '_id': 'user:2',
        'type': 'user',
        'name': '李小華',
        'skills': ['JavaScript', 'Node.js']
    }
    db.save(doc2)

    doc3 = {
        '_id': 'post:1',
        'type': 'post',
        'title': 'CouchDB 入門',
        'author': 'user:1'
    }
    db.save(doc3)

    retrieved = db['user:1']
    print(f"文件查詢 - name: {retrieved['name']}")

    doc = db['user:1']
    doc['skills'].append('Redis')
    db.save(doc)
    updated = db['user:1']
    print(f"文件更新 - skills: {updated['skills']}")

    results = list(db.view('_all_docs', include_docs=True))
    print(f"視圖查詢 - 總文件數: {len(results)}")

    del db['user:1']
    print("文件刪除完成")

    print("CouchDB 操作完成！")

if __name__ == "__main__":
    demo()
```

## 執行方式

確保相關資料庫服務正在運行後，執行：

```bash
python3 mongodb_demo.py
python3 redis_demo.py
python3 couchdb_demo.py
```

或使用 test.sh 自動執行所有範例。