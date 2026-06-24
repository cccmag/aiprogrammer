# 備份與災難復原

## 前言

資料庫備份是資料保護的最後一道防線，本篇介紹備份策略。

## 備份類型

```
備份類型：
──────────

完整備份：
  - 備份整個資料庫
  - 簡單但耗時

增量備份：
  - 只備份變更
  - 快速但複雜

差異備份：
  - 備份與上次完整備份的差異
  - 平衡選擇
```

## PostgreSQL 備份

```bash
# 完整備份
pg_dump -Fc mydb > mydb.dump

# 恢復
pg_restore -d mydb mydb.dump

# 純 SQL 備份
pg_dump -Fp mydb > mydb.sql
```

## MySQL 備份

```bash
# 完整備份
mysqldump -u root -p mydb > mydb.sql

# 恢復
mysql -u root -p mydb < mydb.sql

# 增量備份（二進制日誌）
mysqladmin flush-logs
```

## 災難復原計畫

```
復原步驟：
──────────

1. 評估災情
2. 決定恢復點目標（RPO）
3. 決定恢復時間目標（RTO）
4. 執行恢復
5. 驗證資料完整性
```

---

## 延伸閱讀

- [Database Backup Strategies](https://www.google.com/search?q=database+backup+disaster+recovery)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」文章之一。*