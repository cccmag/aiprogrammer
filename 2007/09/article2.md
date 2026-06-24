# Redis：高效的鍵值儲存

## 概述

Redis 是一個開源的記憶體資料結構儲存系統，可用作為資料庫、緩存和消息隊列。2007 年，Redis 正在快速發展，為高效能場景提供了嶄新的解決方案。

## Redis 的核心特性

### 記憶體優先

Redis 將資料存儲在記憶體中，提供了極高的讀寫效能：

```python
"""
Redis 概念展示
展示 Redis 的資料結構和操作
"""

def demo():
    print("=" * 50)
    print("Redis 概念展示")
    print("=" * 50)

    print("\n--- Redis 資料結構 ---")
    data_structures = {
        "String": "最基本類型，可存儲字串、數字",
        "Hash": "鍵值對集合，類似 Python dict",
        "List": "順序列表，支援push/pop",
        "Set": "無序不重複集合",
        "Sorted Set": "帶分數的有序集合",
    }
    for ds, desc in data_structures.items():
        print(f"  {ds}: {desc}")

    print("\n--- String 操作 ---")
    string_ops = """
SET user:1:name "張三"
GET user:1:name
INCR page_views
DECR page_views
APPEND user:1:bio " 工程師"
"""
    print(string_ops)

    print("\n--- Hash 操作 ---")
    hash_ops = """
HSET user:1 name "張三" email "zhang@example.com" age "30"
HGET user:1 name
HGETALL user:1
HINCRBY user:1 age 1
"""
    print(hash_ops)

    print("\n--- List 操作 ---")
    list_ops = """
LPUSH tasks "task1"
LPUSH tasks "task2"
RPUSH tasks "task3"
LRANGE tasks 0 -1
LPOP tasks
"""
    print(list_ops)

    print("\n--- 使用場景 ---")
    scenarios = [
        ("緩存", "熱門資料加速訪問"),
        ("Session 儲存", "使用者登入狀態"),
        ("消息隊列", "非同步任務處理"),
        ("計數器", "訪問統計、限流"),
        ("排行榜", "Sorted Set 实现"),
    ]
    for name, desc in scenarios:
        print(f"  {name}: {desc}")

    print("\n" + "=" * 50)
    print("Redis 概念展示完成")

if __name__ == "__main__":
    demo()