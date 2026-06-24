# SQLite 3.21：效能提升與修復

## 前言

SQLite 3.21 於 2017 年發布，帶來了多項效能優化和錯誤修復。

## 新功能

### JSON 函式增強

```sql
-- 新增 json_replace, json_set 等函式
SELECT json_replace('{"name":"John"}', '$.name', 'Jane');
-- 結果: {"name":"Jane"}

SELECT json_set('{"name":"John"}', '$.age', '30');
-- 結果: {"name":"John","age":"30"}
```

### 查詢優化

```sql
-- 自動使用覆蓋索引
CREATE INDEX idx ON users(email, id);
SELECT email, id FROM users WHERE email = 'test@example.com';
```

## 效能改進

SQLite 3.21 的改進：

- 加快了 LIKE 和 GLOB 查詢
- 優化了 WITH 查詢（CTE）
- 改進了交易並發效能

---

**延伸閱讀**

- [SQLite 3.21 Release](https://www.google.com/search?q=SQLite+3.21+release)