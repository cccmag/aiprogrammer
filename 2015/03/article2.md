# MySQL 5.7 GA 發布

## 前言

MySQL 5.7 是重要的里程碑版本，引入了多項改進。

## 主要新功能

### 原生 JSON 支援

```sql
-- JSON 欄位
CREATE TABLE config (
    id INT PRIMARY KEY,
    data JSON
);

-- JSON 查詢
INSERT INTO config VALUES (1, '{"theme": "dark", "lang": "zh"}');

SELECT data->>'$.theme' FROM config;
```

### GIS 增強

```sql
-- 更好的地理空間支援
SELECT ST_Distance(
    ST_GeomFromText('POINT(121.5 25.0)'),
    ST_GeomFromText('POINT(121.6 25.1)')
);
```

### 預設值

```sql
-- 支援函式預設值
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## 延伸閱讀

- [MySQL 5.7 新特性](https://www.google.com/search?q=MySQL+5.7+new+features)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」文章之一。*