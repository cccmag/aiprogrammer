# MySQL 5.1 發布：資料庫新特性

2007 年，MySQL 5.1 進入候選發布階段，帶來了多項重要的企業級功能。

## MySQL 5.1 的新特性

### 表格劃分 (Table Partitioning)

```sql
-- 水平劃分
CREATE TABLE sales (
    id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
)
PARTITION BY RANGE (YEAR(sale_date)) (
    PARTITION p2006 VALUES LESS THAN (2007),
    PARTITION p2007 VALUES LESS THAN (2008),
    PARTITION p2008 VALUES LESS THAN MAXVALUE
);

-- 查詢自動使用分區剪裁
SELECT * FROM sales WHERE sale_date BETWEEN '2007-01-01' AND '2007-12-31';
```

### 事件排程器

```sql
-- 建立事件
CREATE EVENT my_event
ON SCHEDULE EVERY 1 HOUR
DO
    INSERT INTO stats (timestamp, count)
    VALUES (NOW(), 0);

-- 檢視事件
SHOW EVENTS;
```

### 視圖效能改進

```sql
-- 具體化視圖的效能改進
CREATE ALGORITHM=MERGE VIEW sales_summary AS
SELECT region, SUM(amount) as total
FROM sales
GROUP BY region;
```

## 結語

MySQL 5.1 的新功能使其更適合企業級應用，為後續的發展奠定了基礎。

---

*延伸閱讀：[MySQL 官方網站](https://developers.google.com/search/?q=mysql+official)*