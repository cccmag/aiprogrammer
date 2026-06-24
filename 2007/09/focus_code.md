#!/usr/bin/env python3
"""
SQL 查詢展示
展示常見的 SQL 操作和查詢範例
"""

def demo():
    print("=" * 50)
    print("SQL 查詢展示")
    print("=" * 50)

    print("\n--- 基本 SQL 查詢 ---")
    basic_queries = [
        ("SELECT * FROM users", "查詢所有資料"),
        ("SELECT name, email FROM users", "選擇特定欄位"),
        ("SELECT * FROM users WHERE age > 18", "條件查詢"),
        ("SELECT * FROM users ORDER BY name", "排序"),
        ("SELECT COUNT(*) FROM users", "聚合函數"),
    ]
    for query, desc in basic_queries:
        print(f"\n-- {desc}")
        print(f"{query};")

    print("\n--- JOIN 操作 ---")
    join_queries = [
        ("SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id", "INNER JOIN"),
        ("SELECT u.name, o.total FROM users u LEFT JOIN orders o ON u.id = o.user_id", "LEFT JOIN"),
        ("SELECT u.name, o.total FROM users u RIGHT JOIN orders o ON u.id = o.user_id", "RIGHT JOIN"),
    ]
    for query in join_queries:
        print(f"\n{query};")

    print("\n--- 子查詢 ---")
    subquery = """
SELECT name FROM users
WHERE id IN (
    SELECT user_id FROM orders
    WHERE total > 1000
);"""
    print(subquery)

    print("\n--- 聚合查詢 ---")
    aggregate = """
SELECT department, COUNT(*) as count, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;"""
    print(aggregate)

    print("\n--- 索引使用 ---")
    index_example = """
-- 建立索引
CREATE INDEX idx_name ON users(name);

-- 複合索引
CREATE INDEX idx_dept_salary ON employees(department, salary);

-- 查詢使用索引
SELECT * FROM users WHERE name = 'John';
"""
    print(index_example)

    print("\n" + "=" * 50)
    print("SQL 查詢展示完成")

if __name__ == "__main__":
    demo()