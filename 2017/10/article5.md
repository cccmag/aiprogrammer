# SQLite 3.20：新增 JSON 處理函式

## 前言

SQLite 3.20 於 2017 年發布，引入了重要的 JSON 處理功能，使這個輕量級資料庫更加現代化。

## JSON 函式支援

```sql
-- 提取 JSON 值
SELECT json_extract('{"name": "John", "age": 30}', '$.name');
-- 結果: John

-- 創建 JSON
SELECT json_object('name', 'Alice', 'age', 25);
-- 結果: {"name": "Alice", "age": 25}

-- JSON 陣列操作
SELECT json_array(1, 2, 3);
-- 結果: [1, 2, 3]
```

## 應用場景

- 儲存半結構化資料
- 與現代 Web API 整合
- 簡化 NoSQL 使用場景

## 效能優化

SQLite 3.20 還包含了多項效能優化，包括更好的查詢規劃和索引使用。

---

**延伸閱讀**

- [SQLite 3.20 Release](https://www.google.com/search?q=SQLite+3.20+release)
- [SQLite JSON Functions](https://www.google.com/search?q=SQLite+JSON+functions)