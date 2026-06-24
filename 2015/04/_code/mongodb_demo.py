#!/usr/bin/env python3
"""
MongoDB 基本操作範例
展示文件的新增、查詢、更新和刪除操作
"""

from pymongo import MongoClient
from datetime import datetime

def demo():
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=1000)
        client.server_info()
    except Exception as e:
        print(f"MongoDB 未運行，跳過實際操作: {e}")
        print("=== MongoDB 操作演示（無需實際執行）===")
        print("這個程式會執行以下操作：")
        print("1. 連接到 MongoDB")
        print("2. 插入多個使用者文件")
        print("3. 查詢所有使用者")
        print("4. 查詢會 Python 的使用者")
        print("5. 更新使用者年齡")
        print("6. 刪除一個使用者")
        print("=== 程式結束 ===")
        return

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