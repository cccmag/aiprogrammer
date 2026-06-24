# 文件資料庫 Schema 設計模式

## 前言

文件資料庫的 Schema-less 特性提供了很大的彈性，但這不意味著可以完全忽視資料模型設計。好的設計模式可以提升效能、簡化查詢、並讓應用更容易維護。

## 常見設計模式

### 1. 反正規化模式

將關聯式資料庫中需要 JOIN 查詢的資料，嵌入到同一個文件中：

```python
# 電子商務訂單模型
order = {
    "_id": "order:1001",
    "order_number": "ORD-2024-001",
    "customer": {
        "id": "cust:500",
        "name": "張小明",
        "email": "zhang@example.com"
    },
    "items": [
        {
            "product_id": "prod:100",
            "name": "筆記型電腦",
            "price": 45000,
            "quantity": 1
        },
        {
            "product_id": "prod:200",
            "name": "滑鼠",
            "price": 500,
            "quantity": 2
        }
    ],
    "shipping_address": {
        "city": "台北市",
        "district": "大安區",
        "zip": "106",
        "address": "復興南路一段..."
    },
    "total_amount": 46000,
    "status": "shipped"
}
```

這種設計的優點：
- 一次查詢就能取得完整訂單資訊
- 不需要 JOIN 操作
- 查詢效能佳

缺點：
- 如果商品價格變動，歷史訂單的價格也會改變
- 同一商品的資訊可能在多個文件中重複

### 2. 鄰接列表模式

適用於需要表示樹狀結構的資料：

```python
# 組織架構
company = {
    "_id": "company:1",
    "name": "科技公司",
    "departments": [
        {
            "id": "dept:engineering",
            "name": "工程部",
            "employees": ["emp:1", "emp:2", "emp:3"]
        },
        {
            "id": "dept:sales",
            "name": "業務部",
            "employees": ["emp:4", "emp:5"]
        }
    ]
}
```

### 3. 桶模式（Bucket Pattern）

將同類資料分組到單一文件中，減少文件數量：

```python
# 物聯網感測器讀數 - 按月份分桶
sensor_bucket_2024_01 = {
    "_id": "sensor:temp:2024:01",
    "sensor_id": "temp:001",
    "month": "2024-01",
    "readings": [
        {"day": 1, "hour": 0, "value": 22.5},
        {"day": 1, "hour": 1, "value": 22.3},
        # ... 更多讀數
    ],
    "metadata": {
        "location": "台北",
        "unit": "celsius"
    }
}
```

### 4. 擴展引用模式

當一對多關係中，「多」的一方數量很大時，使用引用而不是嵌入：

```python
# 部落格文章（引用作者）
article = {
    "_id": "article:100",
    "title": "MongoDB 入門",
    "content": "...",
    "author_id": "user:50"  # 引用
}

# 作者（獨立文件）
author = {
    "_id": "user:50",
    "name": "張小明",
    "bio": "...",
    "social_links": {...}
}
```

### 5. 變異模式（Outlier Pattern）

處理少數特殊文件：

```python
# 大多數產品
product_normal = {
    "_id": "prod:100",
    "name": "一般商品",
    "price": 100,
    "inventory": 50
}

# 少數特殊產品（需要擴展欄位）
product_special = {
    "_id": "prod:999",
    "name": "豪華套裝",
    "price": 10000,
    "inventory": 5,
    # 擴展欄位
    "includes": ["item1", "item2", "item3"],
    "warranty": "終身保固",
    "delivery_priority": "express"
}
```

## Schema 版本管理

隨著應用演進，資料結構也會改變：

```python
def migrate_document(doc):
    """文件遷移函數"""
    schema_version = doc.get('schema_version', 1)

    if schema_version < 2:
        # v1 -> v2：新增欄位
        doc['updated_at'] = doc.get('created_at')
        doc['schema_version'] = 2

    if schema_version < 3:
        # v2 -> v3：重構欄位
        if 'full_name' in doc:
            parts = doc['full_name'].split(' ')
            doc['first_name'] = parts[0] if parts else ''
            doc['last_name'] = parts[-1] if len(parts) > 1 else ''
            del doc['full_name']
        doc['schema_version'] = 3

    return doc
```

## 設計檢查清單

在設計文件結構時，考慮以下問題：

1. **查詢模式**：文檔會被如何查詢？頻率如何？
2. **寫入模式**：資料多久寫入一次？誰會寫入？
3. **資料大小**：文檔預計多大？會超過限制嗎？
4. **關聯性**：文檔之間的關係是什麼？
5. **擴展性**：未來可能需要新增什麼欄位？
6. **一致性需求**：需要多強的一致性保證？

好的 Schema 設計是 NoSQL 應用成功的關鍵。