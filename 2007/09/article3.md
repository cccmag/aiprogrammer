# CouchDB：文件資料庫

## 概述

CouchDB 是一個面向文件的開源 NoSQL 資料庫，使用 JSON 儲存文件，透過 RESTful API 進行訪問。2007 年 CouchDB 0.8 的發布，展示了離線優先和文件導向設計的潛力。

## CouchDB 的核心概念

### 文件導向

```python
"""
CouchDB 概念展示
展示文件資料庫的設計理念
"""

def demo():
    print("=" * 50)
    print("CouchDB 文件資料庫概念展示")
    print("=" * 50)

    print("\n--- 文件模型 vs 關聯式模型 ---")
    print("""
關聯式模型：
users 表          orders 表
+-----------+     +-----------+
| id        |     | id        |
| name      |     | user_id   |
| email     |     | total     |
+-----------+     +-----------+

文件模型：
{
  "_id": "user123",
  "name": "張三",
  "email": "zhang@example.com",
  "orders": [
    {"order_id": "o1", "total": 100},
    {"order_id": "o2", "total": 200}
  ]
}
""")

    print("\n--- RESTful API ---")
    api_examples = """
# 创建文件
PUT /database/user123
{"name": "張三", "email": "zhang@example.com"}

# 讀取文件
GET /database/user123

# 更新文件
PUT /database/user123
{"_rev": "1-xxx", "name": "張三", "email": "zhang2@example.com"}

# 刪除文件
DELETE /database/user123?rev=2-xxx

# 查詢
GET /database/_all_docs
POST /database/_find
{"selector": {"name": "張三"}}
"""
    print(api_examples)

    print("\n--- 視圖與 MapReduce ---")
    mapreduce = """
// Map 函數
function(doc) {
  if (doc.type === 'order') {
    emit(doc.user_id, doc.total);
  }
}

// Reduce 函數
function(keys, values) {
  return sum(values);
}

// 使用視圖
GET /database/_design/orders/_view/by_user?group=true
"""
    print(mapreduce)

    print("\n--- 離線同步特性 ---")
    sync_features = [
        "離線優先設計",
        "自動衝突檢測",
        "多主複製",
        "最終一致性",
    ]
    for f in sync_features:
        print(f"  - {f}")

    print("\n" + "=" * 50)
    print("CouchDB 概念展示完成")

if __name__ == "__main__":
    demo()