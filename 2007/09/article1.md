# SQLite 3.4：輕量級資料庫

## 概述

2007 年，SQLite 3.4 的發布進一步鞏固了其在嵌入式資料庫領域的領導地位。SQLite 是一個軟體庫，實現了一個小巧、快速、自包含、高可靠性、功能完整的 SQL 資料庫引擎。

## SQLite 的設計理念

SQLite 的核心設計理念是「簡單」：
- 無需单独的伺服器程序
- 完整的資料庫存儲在單一磁碟文件中
- 非常適合嵌入式系統和小型應用

## SQLite 3.4 的新功能

### 表格劃分增強

```python
"""
SQLite 3.4 概念展示
展示 SQLite 的核心功能和特點
"""

def demo():
    print("=" * 50)
    print("SQLite 3.4 概念展示")
    print("=" * 50)

    print("\n--- SQLite 特性 ---")
    features = [
        "零配置 - 無需安裝或設定",
        "無伺服器 - 嵌入式資料庫",
        "單一檔案 - 整個資料庫在一個檔案中",
        "跨平台 - Windows, Linux, macOS, etc.",
        "ACID 相容 - 事務處理可靠",
        "大小僅幾百 KB",
    ]
    for f in features:
        print(f"  - {f}")

    print("\n--- 與其他資料庫比較 ---")
    print("""
| 特性      | SQLite   | MySQL    | PostgreSQL |
|-----------|----------|----------|------------|
| 架構      | 嵌入式   | 客戶端/伺服器 | 客戶端/伺服器 |
| 並發      | 有限     | 完整     | 完整       |
| 規模      | 小型     | 中型     | 大型       |
| 部署      | 簡單     | 中等     | 複雜       |
""")

    print("\n--- SQL 語法範例 ---")
    sql_examples = """
-- 建立表格
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入資料
INSERT INTO users (name, email) VALUES ('張三', 'zhang@example.com');

-- 查詢
SELECT * FROM users WHERE name LIKE '張%';

-- 索引
CREATE INDEX idx_email ON users(email);

-- 事務
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
"""
    print(sql_examples)

    print("\n" + "=" * 50)
    print("SQLite 概念展示完成")

if __name__ == "__main__":
    demo()