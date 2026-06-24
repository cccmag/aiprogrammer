# PostgreSQL 的成熟

## 前言

PostgreSQL 在 2007 年持續成熟，成為最先進的開源關聯式資料庫。

## PostgreSQL 特性

```sql
-- 2007 年 PostgreSQL 8.2 的功能
SELECT * FROM products
WHERE price > 100
ORDER BY price DESC
LIMIT 10;

-- 窗口函數
SELECT name, department,
       AVG(salary) OVER (PARTITION BY department)
FROM employees;
```

## 結論

PostgreSQL 的穩定性和功能完整性使其在 2007 年獲得更多採用。

---

*本篇文章為「AI 程式人雜誌 2007 年 3 月號」文章集錦系列。*