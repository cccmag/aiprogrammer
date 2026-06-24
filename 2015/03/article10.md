# 資料庫監控工具

## 前言

監控是確保資料庫健康運行的關鍵，本篇介紹常見的監控工具。

## 開源工具

### pgAdmin（PostgreSQL）

```sql
-- 即時查詢監控
SELECT * FROM pg_stat_activity;

-- 慢查詢
SELECT * FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### MySQL Enterprise Monitor

```sql
-- 查詢監控
SHOW PROCESSLIST;

-- 慢查詢日誌
SHOW VARIABLES LIKE 'slow_query%';
```

## 雲端監控

```
雲端監控服務：
──────────────

AWS:
  - CloudWatch
  - Performance Insights

Google Cloud:
  - Cloud Monitoring
  - Query Insights

Azure:
  - Azure Monitor
  - Query Performance Insight
```

## 關鍵指標

```
監控指標：
──────────

連線：
  - 目前連線數
  - 最大連線數

效能：
  - 查詢延遲
  - 吞吐量（QPS）
  - 緩衝區命中率

資源：
  - CPU 使用率
  - 記憶體使用
  - 磁碟 I/O

錯誤：
  - 連線錯誤
  - 查詢錯誤
  - 死結
```

---

## 延伸閱讀

- [Database Monitoring Tools](https://www.google.com/search?q=database+monitoring+tools+open+source)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」文章之一。*