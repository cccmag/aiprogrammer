#!/usr/bin/env python3
"""
資料庫技術概念展示
展示 SQL、NoSQL 和資料庫設計的核心概念
"""

def demo():
    print("=" * 50)
    print("資料庫技術概念展示")
    print("=" * 50)

    print("\n--- 關聯式資料庫概念 ---")
    relational = """
常見操作：
SELECT * FROM users WHERE age > 18;
INSERT INTO users (name, email) VALUES ('張三', 'zhang@example.com');
UPDATE users SET age = 31 WHERE id = 1;
DELETE FROM users WHERE id = 1;

JOIN 操作：
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id;

聚合查詢：
SELECT department, COUNT(*) as count, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;
"""
    print(relational)

    print("\n--- NoSQL 資料庫分類 ---")
    nosql = {
        "鍵值儲存": ["Redis", "Amazon DynamoDB"],
        "文件資料庫": ["MongoDB", "CouchDB"],
        "列儲存": ["Cassandra", "HBase"],
        "圖資料庫": ["Neo4j", "InfoGrid"],
    }
    for category, dbs in nosql.items():
        print(f"  {category}: {', '.join(dbs)}")

    print("\n--- 索引類型 ---")
    indexes = """
B-Tree 索引：大多數場景，範圍查詢
Hash 索引：等值查詢，速度最快
GiST 索引：幾何資料、全文搜索
GIN 索引：陣列、JSON 資料
"""
    print(indexes)

    print("\n" + "=" * 50)
    print("資料庫概念展示完成")

if __name__ == "__main__":
    demo()