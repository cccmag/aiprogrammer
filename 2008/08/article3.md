# 資料庫索引設計

## 索引類型

```sql
-- B-tree 索引（預設）
CREATE INDEX idx ON users(email);

-- 複合索引
CREATE INDEX idx ON orders(user_id, created_at);
```

## 結論

好的索引設計是效能關鍵。

---

**延伸閱讀**

- [資料庫查詢優化](focus5.md)