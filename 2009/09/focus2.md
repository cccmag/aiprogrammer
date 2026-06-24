# 文件資料庫的概念：JSON 文件模型

## 文件資料庫的核心概念

### 什麼是文件？

```python
# 文件（Document）是自描述的記錄

# JSON 文件範例
{
    "name": "張三",
    "age": 30,
    "email": "zhang@example.com",
    "address": {
        "city": "台北",
        "zip": "100"
    },
    "orders": [
        {"id": 101, "total": 500},
        {"id": 102, "total": 300}
    ]
}

# 等價的關聯式模型需要：
# - Users 表
# - Addresses 表（透過外鍵）
# - Orders 表（透過外鍵）
# 需要多次 JOIN 才能獲取完整資訊
```

### 文件 vs 關聯式

```markdown
比較：單一用戶的完整訂單查詢

關聯式資料庫：
1. JOIN users 和 addresses
2. JOIN 結果和 orders
3. JOIN 結果和 order_items

文件資料庫：
1. 直接查詢 users 集合
2. 文件本身就包含 addresses 和 orders

代價：
- 關聯式：多次磁碟 I/O
- 文件：單次讀取
```

## 動態 Schema

### 彈性結構

```python
# 文件資料庫的彈性 Schema

# 用戶 A 的文件
{
    "name": "張三",
    "age": 30,
    "city": "台北"
}

# 用戶 B 的文件（不同的結構）
{
    "name": "李四",
    "email": "li@example.com",
    "phone": "0912-345-678",
    "company": "某某公司"
}

# 用戶 C 的文件（更複雜）
{
    "name": "王五",
    "preferences": {
        "theme": "dark",
        "notifications": true,
        "language": "zh-TW"
    },
    "social": {
        "twitter": "@wangwu",
        "facebook": "wang.wu"
    }
}
```

### Schema 版本控制

```python
# 處理 Schema 變化

# v1: 最初設計
{
    "name": "張三",
    "age": 30
}

# v2: 新增 phone 欄位
# 應用層處理相容性

def get_user_v2(doc):
    # 處理缺少 phone 的舊文件
    if 'phone' not in doc:
        doc['phone'] = '未知'
    return doc

def get_user_v3(doc):
    # 處理所有版本
    if 'preferences' in doc:
        doc['notification_email'] = doc['preferences'].get('email', False)
    return doc
```

## 巢狀文件

### 巢狀的價值

```python
# 巢狀文件範例：部落格文章

{
    "title": "MongoDB 教程",
    "author": {
        "name": "張三",
        "email": "zhang@example.com",
        "bio": "軟體工程師"
    },
    "content": "這是文章的正文...",
    "comments": [
        {
            "author": "李四",
            "text": "寫得很好！",
            "timestamp": "2009-09-01T10:00:00Z"
        },
        {
            "author": "王五",
            "text": "感謝分享",
            "timestamp": "2009-09-01T11:30:00Z"
        }
    ],
    "tags": ["MongoDB", "NoSQL", "教程"],
    "related": [
        {"id": 1, "title": "Redis 教程"},
        {"id": 2, "title": "Node.js 教程"}
    ]
}

# 查詢：取得所有關於 NoSQL 的評論
# MongoDB:
db.posts.find(
    {"tags": "NoSQL"},
    {"comments.author": 1, "comments.text": 1}
)
```

### 巢狀的深度

```python
# 巢狀深度建議

# 好的設計：限制巢狀深度
{
    "order": {
        "customer": {
            "name": "張三",
            "id": "C001"
        },
        "items": [
            {"product_id": "P001", "name": "商品 A", "quantity": 2}
        ]
    }
}

# 避免過度巢狀
# 如果需要，可以考慮引用（References）
{
    "order": {
        "customer_id": "C001",  # 引用而不是嵌入
        "items": [
            {"product_id": "P001", "quantity": 2}  # 引用而不是嵌入完整商品資訊
        ]
    }
}
```

## 文件資料庫的操作

### CRUD 操作

```python
# MongoDB-style 操作

# Create（新增）
db.users.insert({
    "name": "張三",
    "age": 30
})

# Read（查詢）
db.users.find({"name": "張三"})
db.users.find_one({"_id": ObjectId("...")})

# Update（更新）
db.users.update(
    {"name": "張三"},
    {"$set": {"age": 31}}
)

# Delete（刪除）
db.users.remove({"name": "張三"})
```

### 查詢運算子

```python
# 比較運算子
db.users.find({"age": {"$gt": 18}})  # 大於 18
db.users.find({"age": {"$gte": 18}}) # 大於等於 18
db.users.find({"age": {"$lt": 65}})  # 小於 65
db.users.find({"age": {"$lte": 65}}) # 小於等於 65

# 邏輯運算子
db.users.find({"$or": [
    {"age": {"$lt": 18}},
    {"age": {"$gt": 65}}
]})

# 正規表達式
db.users.find({"name": /張.*/})

# 陣列查詢
db.posts.find({"tags": "NoSQL"})      # 包含 NoSQL
db.posts.find({"tags": {"$all": ["NoSQL", "教程"]}})  # 包含所有
db.comments.find({"replies.0.author": "張三"})  # 巢狀查詢
```

## 文件資料庫的限制

### 不適合的場景

```markdown
文件資料庫的限制：

1. 複雜的 JOIN
   - 文件資料庫不擅長多表 JOIN
   - 需要在應用層處理

2. 事務
   - 早期 MongoDB 無事務（1.0）
   - 跨文件事務更困難

3. 深度巢狀查詢
   - 過度巢狀的文件難以查詢
   - 需要正規化

4. 嚴格 Schema 需求
   - 如果需要嚴格資料驗證
   - 需要在應用層處理
```

## 結語

文件資料庫以其靈活的 JSON 文件模型，為 Web 應用開發帶來了極大的便利。MongoDB 1.0 的發布標誌著這項技術的成熟。

下一篇文章將介紹 MongoDB 1.0 的技術特點和生態系統。

---

## 延伸閱讀

- [文件資料庫概念](https://www.google.com/search?q=document+database+concepts+2009)
- [JSON 文件模型](https://www.google.com/search?q=JSON+document+model)
- [MongoDB 查詢](https://www.google.com/search?q=MongoDB+query+operators)
- [巢狀文件設計](https://www.google.com/search?q=nested+document+design+patterns)

---

*本篇文章為「AI 程式人雜誌 2009 年 9 月號」焦點系列之一。*