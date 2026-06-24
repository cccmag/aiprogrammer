# SQLite 3.24 新特性

## 前言

SQLite 3.24 於 2018 年發布，帶來了多項改進。

## 主要更新

### 支援 UPSERT

終於支援「插入或更新」語法：

```sql
INSERT INTO user(id, name)
VALUES (1, '張三')
ON CONFLICT(id) DO UPDATE SET name = excluded.name;
```

### 窗口函數增強

對窗口函數的支援更加完善。

### 效能優化

查詢效能有所提升。

## 結論

SQLite 持續改進，是嵌入式和邊緣運算的首選資料庫。

---

**延伸閱讀**

- [SQLite 官方網站](https://www.google.com/search?q=SQLite+official+site)
- [SQLite 3.24 發布說明](https://www.google.com/search?q=SQLite+3.24+release+notes)