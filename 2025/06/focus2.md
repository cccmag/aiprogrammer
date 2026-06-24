# SQL 基礎：CREATE、INSERT、SELECT

## DDL 與 DML

SQL 指令可以分為兩大類：

**DDL（Data Definition Language）**：定義資料庫結構

- `CREATE`：建立資料庫或表格
- `ALTER`：修改表格結構
- `DROP`：刪除資料庫或表格

**DML（Data Manipulation Language）**：操作資料內容

- `INSERT`：新增資料
- `SELECT`：查詢資料
- `UPDATE`：修改資料
- `DELETE`：刪除資料

## CREATE TABLE：建立表格

### 基本語法

```sql
CREATE TABLE table_name (
    column1 datatype constraints,
    column2 datatype constraints,
    column3 datatype constraints,
    ...
);
```

### 完整範例

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER DEFAULT 18,
    enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

這個命令建立了 `students` 表格，包含五個欄位：

- `id`：整數，主鍵，自動遞增
- `name`：文字，不可為空
- `email`：文字，唯一且不可為空
- `age`：整數，預設值 18
- `enrolled_at`：日期時間，預設為當前時間

### 常用的約束條件

| 約束 | 說明 |
|------|------|
| `PRIMARY KEY` | 主鍵，唯一標識每筆記錄 |
| `FOREIGN KEY` | 外鍵，引用其他表格的主鍵 |
| `NOT NULL` | 不可為空 |
| `UNIQUE` | 值必須唯一 |
| `DEFAULT value` | 預設值 |
| `CHECK (condition)` | 檢查條件 |

## INSERT：插入資料

### 基本語法

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);
```

### 範例

```sql
INSERT INTO students (name, email, age)
VALUES ('王小明', 'wang@example.com', 20);

INSERT INTO students (name, email)
VALUES ('李小華', 'lee@example.com');
-- age 會使用預設值 18

INSERT INTO students (name, email, age)
VALUES ('張小英', 'chang@example.com', 22),
       ('陳小豪', 'chen@example.com', 21),
       ('林小美', 'lin@example.com', 19);
-- 一次插入多筆資料
```

## SELECT：查詢資料

### 基本語法

```sql
SELECT column1, column2, ...
FROM table_name;
```

### 範例

```sql
-- 選取特定欄位
SELECT name, email FROM students;

-- 選取所有欄位
SELECT * FROM students;

-- 選取時使用別名
SELECT name AS 姓名, age AS 年齡 FROM students;

-- 選取時使用運算式
SELECT name || '(' || age || '歲)' AS 簡介 FROM students;
```

## 完整範例

以下是一個完整的資料庫操作流程：

```sql
-- 建立表格
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    category TEXT
);

-- 插入商品資料
INSERT INTO products (name, price, stock, category)
VALUES ('iPhone 17', 35900, 50, '手機'),
       ('MacBook Air', 42900, 30, '筆電'),
       ('iPad Pro', 34900, 40, '平板');

-- 查詢所有商品
SELECT * FROM products;

-- 查詢手機類別的商品
SELECT name, price FROM products WHERE category = '手機';

-- 查詢庫存不足的商品
SELECT name, stock FROM products WHERE stock < 35;
```

## 建立資料庫

在 SQLite 中，建立資料庫非常簡單：

```bash
$ sqlite3 mydb.db
sqlite> CREATE TABLE ...
```

當你首次連接到一個不存在的資料庫檔案時，SQLite 會自動建立它。

## 實戰練習

假設你要為一個圖書館建立資料庫：

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE,
    published_year INTEGER,
    available INTEGER DEFAULT 1
);

INSERT INTO books (title, author, isbn, published_year)
VALUES ('資料庫系統概論', '陳鍾誠', '978-986-XXX-XXX-X', 2024),
       ('SQL 實戰寶典', '張三', '978-986-YYY-YYY-Y', 2025),
       ('Python 程式設計', '李四', '978-986-ZZZ-ZZZ-Z', 2023);

SELECT title, author, published_year
FROM books
WHERE published_year >= 2024
ORDER BY published_year DESC;
```

## 參考資料

- [SQL CREATE TABLE 語法](https://www.google.com/search?q=SQL+CREATE+TABLE+syntax)
- [SQL INSERT 語法](https://www.google.com/search?q=SQL+INSERT+syntax)
- [SQL SELECT 語法](https://www.google.com/search?q=SQL+SELECT+syntax)
- [SQLite DDL 教學](https://www.google.com/search?q=SQLite+CREATE+TABLE+tutorial)
