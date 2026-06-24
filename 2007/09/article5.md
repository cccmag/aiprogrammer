# MongoDB：文件儲存的興起

## 概述

2007 年，MongoDB 正在積極開發中，採用文件導向的資料模型，為 Web 應用提供靈活、可擴展的資料儲存方案。

## 文件資料庫的優勢

### 彈性 Schema

```python
"""
MongoDB 概念展示
展示文件資料庫的特點和操作
"""

def demo():
    print("=" * 50)
    print("MongoDB 文件資料庫概念展示")
    print("=" * 50)

    print("\n--- 與關聯式資料庫的比較 ---")
    print("""
關聯式：users 表有固定欄位
+--------+-------------+-------------+
| user_id| name        | email       |
+--------+-------------+-------------+
| 1      | 張三        | z@ex.com    |
+--------+-------------+-------------+

MongoDB：users 集合，每個文件結構可不同
{
  "_id": ObjectId("..."),
  "name": "張三",
  "contact": {
    "phone": "0912-345-678",
    "address": "台北市"
  },
  "orders": [...]
}
""")

    print("\n--- CRUD 操作 ---")
    crud_ops = """
// 插入
db.users.insert({
    name: "張三",
    email: "zhang@example.com",
    age: 30
});

// 查詢
db.users.find({ age: { $gte: 18 } });
db.users.findOne({ name: "張三" });

// 更新
db.users.update(
    { name: "張三" },
    { $set: { age: 31 } }
);

// 刪除
db.users.remove({ name: "張三" });
"""
    print(crud_ops)

    print("\n--- 查詢運算子 ---")
    operators = {
        "$eq": "等於",
        "$ne": "不等於",
        "$gt/$gte": "大於/大於等於",
        "$lt/$lte": "小於/小於等於",
        "$in/$nin": "在陣列中/不在陣列中",
        "$regex": "正規表達式",
        "$exists": "欄位存在",
    }
    for op, desc in operators.items():
        print(f"  {op}: {desc}")

    print("\n--- 索引 ---")
    index_code = """
// 單一欄位索引
db.users.createIndex({ email: 1 });

// 複合索引
db.orders.createIndex({ user_id: 1, created_at: -1 });

// 文字索引
db.articles.createIndex({ content: "text" });
"""
    print(index_code)

    print("\n--- 聚合框架 ---")
    aggregation = """
db.orders.aggregate([
    { $match: { status: "completed" } },
    { $group: {
        _id: "$user_id",
        total: { $sum: "$amount" }
    }},
    { $sort: { total: -1 } },
    { $limit: 10 }
]);
"""
    print(aggregation)

    print("\n" + "=" * 50)
    print("MongoDB 概念展示完成")

if __name__ == "__main__":
    demo()