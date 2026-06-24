# 表格關聯與 JOIN

## 為什麼需要表格關聯？

在真實應用中，資料不會全部放在一個表格中。透過多個表格來組織資料可以避免重複、維持一致性。表格之間透過**鍵（Key）**來建立關聯。

### 外鍵（Foreign Key）

外鍵是一個表格中的欄位，它參考另一個表格的主鍵。透過外鍵，我們可以在表格之間建立關聯。

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,  -- 外鍵
    order_date DATE NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

## 三種關聯類型

### 一對一（1:1）

一個表格的一筆記錄對應另一個表格的一筆記錄。

```
person ── 1:1 ── id_card
```

### 一對多（1:N）

一個表格的一筆記錄對應另一個表格的多筆記錄。這是最常見的關聯類型。

```
customer ── 1:N ── orders
一個客戶可以有多筆訂單
```

### 多對多（M:N）

兩個表格的記錄都可以對應對方的多筆記錄。需要透過中間表（Junction Table）來實作。

```
student ── M:N ── course
透過 enrollment 中間表
```

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

-- 中間表
CREATE TABLE enrollments (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrolled_at DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

## JOIN 查詢

JOIN 用於將多個表格的資料合併查詢。

### INNER JOIN

只返回兩個表格中匹配的記錄。

```sql
SELECT customers.name, orders.order_date, orders.total
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id;
```

```
customers           orders
┌────┬──────┐     ┌────┬────────┬───────┐
│ id │ name │     │ id │cust_id │ total │
├────┼──────┤     ├────┼────────┼───────┤
│ 1  │ 王小明│     │ 101 │  1     │ 1500  │
│ 2  │ 李小華│     │ 102 │  1     │ 2500  │
│ 3  │ 張小英│     │ 103 │  3     │ 3200  │
└────┴──────┘     └────┴────────┴───────┘

INNER JOIN 結果：
王小明│ 2026-06-01 │ 1500
王小明│ 2026-06-02 │ 2500
張小英│ 2026-06-03 │ 3200
（李小華沒有訂單，所以不包含在結果中）
```

### LEFT JOIN（LEFT OUTER JOIN）

返回左表格的所有記錄，右表格沒有匹配時用 NULL 填充。

```sql
SELECT customers.name, orders.order_date, orders.total
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id;
```

```
LEFT JOIN 結果：
王小明│ 2026-06-01 │ 1500
王小明│ 2026-06-02 │ 2500
李小華│ NULL       │ NULL    ← 沒有訂單的客戶也會出現
張小英│ 2026-06-03 │ 3200
```

### RIGHT JOIN 與 FULL JOIN

SQLite 不支援 RIGHT JOIN 和 FULL JOIN。可以透過交換表格順序（使用 LEFT JOIN）或 UNION 來達到類似效果。

```sql
-- 模擬 FULL JOIN
SELECT customers.name, orders.order_date
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
UNION
SELECT customers.name, orders.order_date
FROM orders
LEFT JOIN customers ON orders.customer_id = customers.id;
```

## 多表格 JOIN

可以同時 JOIN 多個表格：

```sql
SELECT c.name, o.order_date, p.name AS product, oi.quantity
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE c.name = '王小明'
ORDER BY o.order_date;
```

## 實戰範例：圖書館管理系統

```sql
CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

CREATE TABLE borrowers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    borrower_id INTEGER NOT NULL,
    loan_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (borrower_id) REFERENCES borrowers(id)
);

INSERT INTO authors VALUES (1, '陳鍾誠'), (2, '張三');
INSERT INTO books VALUES (1, '資料庫系統概論', 1), (2, 'SQL 實戰寶典', 2);
INSERT INTO borrowers VALUES (1, '王小明'), (2, '李小華');
INSERT INTO loans VALUES (1, 1, 1, '2026-06-01', NULL), (2, 2, 1, '2026-06-05', NULL);

-- 查詢目前借出的書籍與借閱者
SELECT b.title, a.name AS author, br.name AS borrower, l.loan_date
FROM loans l
INNER JOIN books b ON l.book_id = b.id
INNER JOIN authors a ON b.author_id = a.id
INNER JOIN borrowers br ON l.borrower_id = br.id
WHERE l.return_date IS NULL;
```

## 表格別名

使用別名可以讓查詢更簡潔：

```sql
-- 長寫法
SELECT customers.name, orders.order_date
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id;

-- 使用別名（AS 可省略）
SELECT c.name, o.order_date
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;
```

## 參考資料

- [SQL JOIN 教學](https://www.google.com/search?q=SQL+JOIN+tutorial)
- [SQL INNER JOIN](https://www.google.com/search?q=SQL+INNER+JOIN+example)
- [SQL LEFT JOIN](https://www.google.com/search?q=SQL+LEFT+JOIN+example)
- [資料庫關聯設計](https://www.google.com/search?q=database+relationship+types)
