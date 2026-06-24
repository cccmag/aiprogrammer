# SQLite 嵌入式資料庫：輕量級、行動應用

## 前言

SQLite 是一款嵌入式資料庫，佔地小於 500KB，無需伺服器進程，適合嵌入式系統和行動應用。

## SQLite 特色

```
SQLite 特性：
─────────────
- 零設定：不需要管理員帳號
- 無伺服器：直接讀寫檔案
- 單一檔案：整個資料庫一個檔案
- 輕量級：小於 500KB
- 跨平台：Windows, Linux, Mac, iOS, Android
- 交易支援：完整的 ACID
- 多種語言支援：Python, Node.js, Java, C#, Ruby, Go
```

## 基本操作

### 命令列工具

```bash
# 進入 SQLite
sqlite3 myapp.db

# 基本命令
sqlite> .help           # 顯示幫助
sqlite> .tables          # 列出所有表格
sqlite> .schema users    # 查看表格結構
sqlite> .indices         # 列出所有索引
sqlite> .databases       # 列出所有資料庫
sqlite> .exit            # 退出
```

### 建立表格

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    age INTEGER DEFAULT 18,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
```

### CRUD 操作

```sql
-- 插入
INSERT INTO users (name, email, age) VALUES ('王小明', 'wang@example.com', 25);
INSERT INTO users (name, email) VALUES ('李小華', 'lee@example.com');

-- 查詢
SELECT * FROM users WHERE age >= 18 ORDER BY created_at DESC LIMIT 10;

-- 更新
UPDATE users SET age = age + 1 WHERE name = '王小明';

-- 刪除
DELETE FROM users WHERE id = 1;
```

## SQLite 與其他資料庫的差異

### 資料類型

```sql
-- SQLite 動態類型
-- NULL, INTEGER, REAL, TEXT, BLOB

-- 彈性類型（可儲存任何類型）
INSERT INTO users (name) VALUES (123);  -- 會儲存為 TEXT "123"
```

### AUTOINCREMENT

```sql
-- SQLite 語法
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

-- PostgreSQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT
);

-- MySQL
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT
);
```

### LIMIT

```sql
-- SQLite, PostgreSQL
SELECT * FROM users LIMIT 10;

-- MySQL
SELECT * FROM users LIMIT 10, 20;
-- 或
SELECT * FROM users LIMIT 20 OFFSET 10;
```

## SQLite 進階功能

### 觸發程序（Triggers）

```sql
-- 更新時間戳記觸發
CREATE TRIGGER update_users_timestamp
AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- 自動刪除關聯資料
CREATE TRIGGER delete_user_posts
AFTER DELETE ON users
BEGIN
    DELETE FROM posts WHERE user_id = OLD.id;
END;
```

### 視圖（Views）

```sql
-- 建立視圖
CREATE VIEW active_users AS
SELECT id, name, email
FROM users
WHERE created_at > datetime('now', '-30 days');

-- 查詢視圖
SELECT * FROM active_users;
```

### 交易

```sql
BEGIN TRANSACTION;

INSERT INTO users (name, email) VALUES ('王小明', 'wang@example.com');
INSERT INTO posts (user_id, title) VALUES (last_insert_rowid(), '第一篇文章');

COMMIT;
-- 或 ROLLBACK;
```

## 在應用程式中使用

### Node.js

```javascript
const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./myapp.db');

db.serialize(() => {
  db.run('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)');

  const stmt = db.prepare('INSERT INTO users (name) VALUES (?)');

  stmt.run('王小明');
  stmt.run('李小華');
  stmt.finalize();

  db.each('SELECT * FROM users', (err, row) => {
    console.log(row.id, row.name);
  });
});

db.close();
```

### Python

```python
import sqlite3

conn = sqlite3.connect('myapp.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')

cursor.execute('INSERT INTO users (name) VALUES (?)', ('王小明',))
cursor.execute('INSERT INTO users (name) VALUES (?)', ('李小華',))

conn.commit()

for row in cursor.execute('SELECT * FROM users'):
    print(row)

conn.close()
```

## 效能優化

### PRAGMA 設定

```sql
-- 開啟外鍵約束
PRAGMA foreign_keys = ON;

-- 同步模式（關閉提升寫入效能）
PRAGMA synchronous = OFF;

-- 快取大小（位元組）
PRAGMA cache_size = -64000;  -- 64MB

-- 開啟唯讀記憶體
PRAGMA mmap_size = 268435456;  -- 256MB

-- 自動 VACUUM
PRAGMA auto_vacuum = INCREMENTAL;
```

### 效能技巧

```sql
-- 批次插入（交易包裝）
BEGIN TRANSACTION;
INSERT INTO logs VALUES (1, 'message 1');
INSERT INTO logs VALUES (2, 'message 2');
-- ... 更多插入
COMMIT;

-- 建立索引
CREATE INDEX idx_logs_created ON logs(created_at);

-- 避免 SELECT *
SELECT id, name FROM users WHERE id = 1;

-- 使用 EXPLAINS
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'test@example.com';
```

### WAL 模式

```sql
-- 開啟 WAL（Write-Ahead Logging）
PRAGMA journal_mode = WAL;

-- WAL 優點
-- - 更好的並發效能
-- - 讀取不阻塞寫入
-- - 快速復原
```

## 使用情境

```
SQLite 適合：
───────────
✓ 嵌入式系統
✓ 行動應用（iOS, Android）
✓ 小型網站
✓ 開發/測試環境
✓ 單一使用者應用
✓ 需要攜帶的資料庫

SQLite 不適合：
─────────────
✗ 高並發寫入
✗ 分散式系統
✗ 超大資料庫（> 100GB）
✗ 需要網路存取
✗ 複雜的權限管理
```

## 結論

SQLite 是獨一無二的嵌入式資料庫。它的小巧、簡單和可靠性使其成為行動應用、瀏覽器和小型網站的首選。

---

## 延伸閱讀

- [SQLite 官方網站](https://www.google.com/search?q=SQLite+documentation)
- [SQLite vs PostgreSQL](https://www.google.com/search?q=SQLite+vs+PostgreSQL+comparison)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」歷史回顧系列之一。*