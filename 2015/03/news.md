# 本月新知

## 2015 年 3 月資料庫技術動態

### 關聯式資料庫

**PostgreSQL 9.5 發布**

PostgreSQL 9.5 帶來多項企業級功能：

- **BRIN 索引**：專為大型資料表設計的空間索引
- **Upsert（INSERT ... ON CONFLICT）**：簡化更新邏輯
- **CUBE/ROLLUP/GROUPING SETS**：進階分析功能
- **改良的效能**：整體效能提升 20-30%

```sql
-- Upsert 範例
INSERT INTO users (id, name, email)
VALUES (1, '王小明', 'wang@example.com')
ON CONFLICT (id) DO UPDATE
  SET name = EXCLUDED.name, email = EXCLUDED.email;
```

**MySQL 5.7 開發里程碑**

MySQL 5.7 进入 GA 阶段：

- **原生 JSON 支援**：在 SQL 中操作 JSON 文件
- **multi-source replication**：多主機複製
- **優化的效能**：查詢效能提升
- **GIS 增強**：更完整的地理空間支援

**SQLite 3.9**

SQLite 3.9 加入重要功能：

- **JSON1 擴展**：在 SQLite 中處理 JSON
- **ICU 擴展**：更好的國際化支援
- **效能改進**：查詢最佳化器增強

### NoSQL 資料庫

**Redis 3.0 RC 發布**

Redis 3.0 引入了期待已久的叢集功能：

```
Redis Cluster 功能：
─────────────────────
- 自動分片（16384 槽）
- 節點故障自動轉移
- 支援多個 master
- 客戶端自動路由
```

**MongoDB 3.0 準備中**

MongoDB 3.0 即將發布：

- **WiredTiger 儲存引擎**（可選）
- **壓縮率高達 80%**
- **寫入效能提升 7-10x**

### 雲端資料庫

**AWS RDS 服務更新**

- **Aurora 支援 Read Replica**
- **PostgreSQL 9.4 支援**
- **改進的監控功能**

**Azure SQL Database 更新**

- **彈性資料庫集區**
- **威脅偵測**
- **稽核功能增強**

### 業界動態

- **Percona 發布 XtraBackup 2.3**：更快的備份
- **TokuDB 開源**：寫入優化的儲存引擎
- **CockroachDB 獲得投資**：分散式 SQL 資料庫興起
- **FoundationDB 開源**：蘋果收購後重新開源

### 標準與規範

- **SQL:2016 制定中**：包含 JSON 路徑運算
- **NoSQL 資料庫標準化討論**：業界尋求共識

---

*本期新知到此結束。下期我們將持續追蹤技術前沿。*