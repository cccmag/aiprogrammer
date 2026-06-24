#!/usr/bin/env python3
"""NoSQL 示範 - MongoDB、CouchDB、Redis 基本操作"""

def demo():
    print("=" * 50)
    print("NoSQL 資料庫示範")
    print("=" * 50)

    # 模擬 MongoDB 操作
    print("\n1. MongoDB 文件操作（模擬）:")
    doc = {
        'name': 'John',
        'age': 30,
        'tags': ['python', 'mongodb'],
        'address': {'city': 'Taipei', 'country': 'Taiwan'}
    }
    print(f"   文件：{doc}")
    print("   查詢：db.users.find_one({'name': 'John'})")

    # 模擬 CouchDB 操作
    print("\n2. CouchDB 文件操作（模擬）:")
    couch_doc = {
        '_id': 'doc123',
        'name': 'Mary',
        'tags': ['python', 'couchdb']
    }
    print(f"   文件：{couch_doc}")
    print("   API：GET /mydb/doc123")

    # 模擬 Redis 操作
    print("\n3. Redis 操作（模擬）:")
    redis_operations = [
        ("SET name 'John'", "OK"),
        ("GET name", "John"),
        ("INCR counter", "1"),
        ("HSET user:1 name John", "OK"),
        ("HGETALL user:1", "{'name': 'John'}"),
        ("LPUSH mylist a b c", "3"),
        ("LRANGE mylist 0 -1", "['c', 'b', 'a']"),
        ("SADD tags python mongodb", "2"),
        ("SMEMBERS tags", "{'python', 'mongodb'}"),
        ("ZADD scores John 100 Mary 90", "2"),
        ("ZREVRANGE scores 0 0 WITHSCORES", "[('John', 100)]")
    ]
    for cmd, result in redis_operations:
        print(f"   {cmd} → {result}")

    print("\n" + "=" * 50)
    print("NoSQL 資料庫各有特色：")
    print("- MongoDB: 靈活文件，豐富查詢")
    print("- CouchDB: RESTful API，離線同步")
    print("- Redis: 記憶體儲存，豐富資料結構")
    print("=" * 50)

if __name__ == "__main__":
    demo()