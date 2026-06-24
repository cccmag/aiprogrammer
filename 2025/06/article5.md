# WHERE 條件過濾

## WHERE 的重要性

在 SQL 查詢中，WHERE 是最常使用的子句。它可以讓你精確地控制從資料庫中取得哪些資料。沒有 WHERE 的 SELECT 通常會返回過多資料，既浪費資源又難以分析。

## 基本條件運算子

### 比較運算子

```sql
-- 建立範例資料
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT,
    salary REAL,
    hire_date DATE,
    is_active INTEGER DEFAULT 1
);

INSERT INTO employees VALUES
(1, '王小明', '工程', 65000, '2020-03-15', 1),
(2, '李小華', '業務', 55000, '2021-07-01', 1),
(3, '張小英', '工程', 72000, '2019-11-20', 1),
(4, '陳小豪', '財務', 60000, '2022-01-10', 1),
(5, '林小美', '業務', 58000, '2023-06-01', 0),
(6, '黃小強', '工程', 48000, '2024-09-15', 1);

-- 等於
SELECT * FROM employees WHERE department = '工程';

-- 不等於
SELECT * FROM employees WHERE department != '業務';

-- 大於/小於
SELECT * FROM employees WHERE salary >= 60000;

-- 範圍
SELECT * FROM employees
WHERE salary >= 50000 AND salary <= 70000;
```

## 複合條件

### AND、OR、NOT

```sql
-- AND：所有條件都要成立
SELECT name, department, salary
FROM employees
WHERE department = '工程'
  AND salary > 60000
  AND is_active = 1;

-- OR：任一條件成立即可
SELECT name, department, salary
FROM employees
WHERE department = '工程'
   OR department = '財務';

-- NOT：反轉條件
SELECT * FROM employees
WHERE NOT department = '業務';

-- 組合使用（務必使用括號明確優先順序）
SELECT * FROM employees
WHERE (department = '工程' OR department = '業務')
  AND salary >= 60000
  AND is_active = 1;
```

邏輯運算子的優先順序：`NOT` > `AND` > `OR`

```sql
-- 危險！沒有括號可能不是你想要的意思
SELECT * FROM employees
WHERE department = '工程' OR department = '業務' AND salary > 70000;

-- 這等同於
SELECT * FROM employees
WHERE department = '工程' OR (department = '業務' AND salary > 70000);

-- 通常你想要的是
SELECT * FROM employees
WHERE (department = '工程' OR department = '業務')
  AND salary > 70000;
```

## 特殊條件

### IN：值集合

```sql
SELECT name, department
FROM employees
WHERE department IN ('工程', '財務', '人事');

-- 等同於
SELECT name, department
FROM employees
WHERE department = '工程'
   OR department = '財務'
   OR department = '人事';

-- NOT IN
SELECT name, department
FROM employees
WHERE department NOT IN ('業務');
```

### BETWEEN：範圍

```sql
SELECT name, salary
FROM employees
WHERE salary BETWEEN 50000 AND 70000;
-- 包含邊界值

SELECT name, hire_date
FROM employees
WHERE hire_date BETWEEN '2020-01-01' AND '2023-12-31';
```

### LIKE：模糊比對

```sql
-- %：任意長度字元
SELECT name FROM employees WHERE name LIKE '王%';   -- 以王開頭
SELECT name FROM employees WHERE name LIKE '%小%';  -- 包含小
SELECT name FROM employees WHERE name LIKE '%華';   -- 以華結尾

-- _：單一字元
SELECT name FROM employees WHERE name LIKE '王__';  -- 王加上兩個字
SELECT name FROM employees WHERE name LIKE '_小_';  -- 第二字為小
```

### NULL 處理

```sql
CREATE TABLE test_null (
    id INTEGER PRIMARY KEY,
    name TEXT,
    score INTEGER
);

INSERT INTO test_null VALUES (1, '王小明', 85);
INSERT INTO test_null VALUES (2, '李小華', NULL);  -- 缺考

-- 錯誤的 NULL 檢查（NULL 不等於任何值，包括 NULL）
SELECT * FROM test_null WHERE score = NULL;    -- 不會返回任何記錄！
SELECT * FROM test_null WHERE score <> NULL;   -- 也不會返回任何記錄！

-- 正確的 NULL 檢查
SELECT * FROM test_null WHERE score IS NULL;       -- 找到缺考者
SELECT * FROM test_null WHERE score IS NOT NULL;   -- 找到有成績者
```

## 字串與日期處理

```sql
-- SQLite 的字串函數
SELECT name, LENGTH(name) AS name_length
FROM employees;

SELECT UPPER(name) AS upper_name
FROM employees;

-- SQLite 的日期函數
SELECT name, hire_date,
       DATE('now') AS today,
       DATE(hire_date, '+1 year') AS anniversary
FROM employees;

SELECT * FROM employees
WHERE hire_date >= DATE('now', '-2 years');  -- 近兩年入職
```

## 實戰：複雜過濾

```sql
-- 找出工程部門中薪資在 60000-80000 之間的在職員工
SELECT name, salary, hire_date
FROM employees
WHERE department = '工程'
  AND salary BETWEEN 60000 AND 80000
  AND is_active = 1
ORDER BY salary DESC;

-- 找出業務部門或 2022 年前入職的員工
SELECT name, department, hire_date
FROM employees
WHERE department = '業務'
   OR hire_date < '2022-01-01'
ORDER BY hire_date;

-- 進階：根據薪資水準分群
SELECT name, salary,
  CASE
    WHEN salary >= 70000 THEN '高'
    WHEN salary >= 55000 THEN '中'
    ELSE '低'
  END AS level
FROM employees
WHERE is_active = 1;
```

## WHERE 效能提示

1. **盡量使用索引欄位**：對常用於 WHERE 的欄位建立索引
2. **避免在 WHERE 中對欄位使用函數**：`WHERE YEAR(hire_date) = 2020` 無法使用索引，改用 `WHERE hire_date BETWEEN '2020-01-01' AND '2020-12-31'`
3. **LIKE 以 % 開頭的查詢無法使用索引**：`LIKE '%keyword'` 會全表掃描
4. **使用 EXPLAIN 分析查詢計畫**：

```sql
EXPLAIN QUERY PLAN
SELECT * FROM employees WHERE department = '工程';
```

## 參考資料

- [SQL WHERE 子句教學](https://www.google.com/search?q=SQL+WHERE+clause+examples)
- [SQL LIKE 模糊查詢](https://www.google.com/search?q=SQL+LIKE+operator+wildcard)
- [SQL NULL 處理](https://www.google.com/search?q=SQL+IS+NULL+operator)
- [SQL 查詢效能最佳化](https://www.google.com/search?q=SQL+query+performance+WHERE+clause)
