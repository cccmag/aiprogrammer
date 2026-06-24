# SQLite 3.9：JSON 支援

## 前言

SQLite 3.9 加入了原生 JSON 支援，讓 SQLite 可以儲存和查詢 JSON 資料。

## JSON1 擴展

```sql
-- JSON 函式
SELECT json_extract('{"name": "王小明", "age": 25}', '$.name');

SELECT json_object('name', '王小明', 'age', 25);

SELECT json_array('a', 'b', 'c');
```

## 使用範例

```sql
-- 儲存 JSON
CREATE TABLE config (
    id INTEGER PRIMARY KEY,
    data TEXT
);

INSERT INTO config VALUES (1, '{"theme": "dark", "notifications": true}');

-- 查詢 JSON 欄位
SELECT json_extract(data, '$.theme') FROM config;
```

---

## 延伸閱讀

- [SQLite JSON1 文檔](https://www.google.com/search?q=SQLite+JSON1+extension)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」文章之一。*