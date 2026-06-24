#!/usr/bin/env python3
"""
Redis 基本操作範例
展示各種資料結構的使用：字串、雜湊、串列、集合
"""

import redis

def demo():
    try:
        client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        client.ping()
    except Exception as e:
        print(f"Redis 未運行，跳過實際操作: {e}")
        print("=== Redis 操作演示（無需實際執行）===")
        print("這個程式會執行以下操作：")
        print("1. 設定字串值")
        print("2. 操作雜湊資料結構")
        print("3. 操作串列資料結構")
        print("4. 操作集合資料結構")
        print("5. 操作有序集合")
        print("6. 設定過期時間")
        print("=== 程式結束 ===")
        return

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