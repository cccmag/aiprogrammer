# SQLite 入門

## 為什麼選擇 SQLite？

SQLite 是全世界使用最廣泛的資料庫——從手機、瀏覽器到嵌入式裝置，SQLite 無所不在。它的核心優勢是：

1. **零配置**：不需要安裝、不需要伺服器、不需要管理員
2. **單一檔案**：整個資料庫儲存在一個 `.db` 檔案中
3. **免授權費**：公有領域，任何用途都免費
4. **可靠穩定**：超過 20 年的發展歷史，每天服務數十億裝置

## 安裝與使用

### 檢查是否已安裝

```bash
$ sqlite3 --version
3.46.0 2024-05-23
```

macOS 和大多數 Linux 發行版已內建 SQLite。

### 基本操作

```bash
# 建立/開啟資料庫
$ sqlite3 mydb.db

# 在 SQLite 提示字元中
sqlite> .databases  -- 顯示資料庫
sqlite> .tables     -- 列出表格
sqlite> .schema     -- 顯示所有表格的結構
sqlite> .quit       -- 離開
```

## 建立第一個資料庫

```sql
-- 建立表格
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    price REAL,
    published DATE
);

-- 插入資料
INSERT INTO books (title, author, price, published)
VALUES ('資料庫系統概論', '陳鍾誠', 580, '2024-01-15');

INSERT INTO books (title, author, price, published)
VALUES ('SQL 實戰寶典', '張三', 720, '2025-06-01');

INSERT INTO books (title, author, price, published)
VALUES ('Python 程式設計', '李四', 650, '2023-09-20');

-- 查詢資料
SELECT * FROM books;
```

## 常用 SQLite 指令

### 點命令（Dot Commands）

| 指令 | 說明 |
|------|------|
| `.tables` | 列出所有表格 |
| `.schema [table]` | 顯示表格結構 |
| `.headers on` | 顯示欄位名稱 |
| `.mode column` | 以欄位對齊模式顯示 |
| `.import file.csv table` | 從 CSV 匯入資料 |
| `.output file.txt` | 將輸出寫入檔案 |
| `.dump` | 匯出整個資料庫為 SQL |
| `.read file.sql` | 執行 SQL 腳本檔案 |

### 格式化輸出

```bash
sqlite> .headers on
sqlite> .mode column
sqlite> SELECT * FROM books;
id  title            author    price  published
--  --------------   ------    -----  ----------
1   資料庫系統概論    陳鍾誠    580    2024-01-15
2   SQL 實戰寶典     張三      720    2025-06-01
3   Python 程式設計  李四      650    2023-09-20
```

## SQLite 的限制

雖然 SQLite 非常強大，但它並不適合所有場景：

| 限制 | 說明 |
|------|------|
| 並發寫入 | 同一時間只有一個寫入交易 |
| 網路存取 | 無內建網路服務，只能本地存取 |
| 使用者管理 | 無使用者權限系統 |
| 儲存大小 | 理論上限 140TB，但實務上適合小於 1TB |
| 儲存過程 | 不支援儲存過程 |

### 何時該避免使用 SQLite

- 高並發寫入的 Web 應用（改用 PostgreSQL/MySQL）
- 需要多使用者權限管理
- 資料量超過 100GB
- 需要網路存取資料庫

## 實戰：建立個人筆記系統

```sql
-- 建立筆記系統資料庫
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    category TEXT,
    tags TEXT,  -- 以逗號分隔
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- 插入範例資料
INSERT INTO categories VALUES (1, '資料庫', '資料庫相關筆記');
INSERT INTO categories VALUES (2, 'Python', 'Python 程式設計');
INSERT INTO categories VALUES (3, 'AI', '人工智慧與機器學習');

INSERT INTO notes (title, content, category, tags)
VALUES ('SQLite 入門', 'SQLite 是一個輕量級的嵌入式資料庫...', '資料庫', 'sqlite,資料庫,入門');

INSERT INTO notes (title, content, category, tags)
VALUES ('Python 串接 SQLite', '使用 sqlite3 模組連接資料庫...', 'Python', 'python,sqlite,資料庫');

-- 查詢特定分類的筆記
SELECT title, created_at FROM notes
WHERE category = '資料庫'
ORDER BY created_at DESC;

-- 搜尋包含特定標籤的筆記
SELECT title, tags FROM notes
WHERE tags LIKE '%sqlite%';
```

## 從命令列執行 SQL 腳本

```bash
# 建立 SQL 腳本
$ cat > init_db.sql << EOF
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);
INSERT INTO users (name, email) VALUES ('王小明', 'wang@test.com');
INSERT INTO users (name, email) VALUES ('李小華', 'lee@test.com');
SELECT * FROM users;
EOF

# 執行腳本
$ sqlite3 test.db < init_db.sql

# 或者使用 .read
$ sqlite3 test.db
sqlite> .read init_db.sql
```

## 參考資料

- [SQLite 官方文件](https://www.google.com/search?q=SQLite+official+documentation)
- [SQLite 點命令](https://www.google.com/search?q=SQLite+dot+commands+cheat+sheet)
- [SQLite 資料型別](https://www.google.com/search?q=SQLite+data+types)
