# 資料庫系統導論

## 什麼是資料庫系統？

資料庫系統（Database System）是一套用於儲存、管理、查詢和分析資料的軟體系統。與傳統的檔案系統相比，資料庫系統提供了以下關鍵能力：

1. **結構化儲存**：資料以表格形式組織，每個欄位有明確的型別
2. **高效查詢**：透過 SQL 語言進行複雜的資料檢索
3. **交易管理**：保證多步驟操作的原子性
4. **並發控制**：多個使用者同時存取時保持資料一致性
5. **權限管理**：精細控制誰可以存取哪些資料

## 資料庫的歷史演進

### 檔案系統時代（1960 年代前）

在資料庫誕生之前，程式使用檔案系統儲存資料。每個應用程式自行定義檔案格式，資料重複、格式不一致、難以共享是常見問題。

```
┌────────────┐     ┌────────────┐
│ 應用程式 A  │────►│ 帳戶資料檔  │
├────────────┤     ├────────────┤
│ 應用程式 B  │────►│ 帳戶資料檔  │（格式不同）
├────────────┤     ├────────────┤
│ 應用程式 C  │────►│ 帳戶資料檔  │（又不同格式）
└────────────┘     └────────────┘
```

### 關聯式模型的誕生（1970）

1970 年，IBM 的 E.F. Codd 發表了劃時代的論文《A Relational Model of Data for Large Shared Data Banks》，提出了關聯式資料庫的理論基礎。他建議將所有資料以**關係（Relation）** — 也就是我們現在說的表格（Table）— 來表示。

```
關聯式模型的核心概念：
┌───────────────────────────────────────┐
│ 資料表（Relation/Table）               │
├────────┬────────┬────────┬────────────┤
│ 主鍵    │ 欄位1  │ 欄位2  │ ...        │
├────────┼────────┼────────┼────────────┤
│ 記錄1  │ 值     │ 值     │            │
│ 記錄2  │ 值     │ 值     │            │
│ ...    │        │        │            │
└────────┴────────┴────────┴────────────┘
```

### 商業資料庫時代（1980s-1990s）

Oracle、IBM DB2、Microsoft SQL Server 等商業資料庫主導市場。SQL 成為標準查詢語言（ANSI SQL 1986）。

### 開源資料庫時代（2000s-2010s）

MySQL 和 PostgreSQL 崛起，SQLite 成為嵌入式資料庫的首選。

### 多元資料庫時代（2020s-至今）

關聯式資料庫、NoSQL 資料庫、向量資料庫百花齊放。

## ACID 交易特性

交易（Transaction）是資料庫系統最重要的概念之一。ACID 是交易的四大特性：

### 原子性（Atomicity）

交易中的所有操作要麼全部成功，要麼全部失敗。如果中途發生錯誤，系統會回滾（Rollback）到交易開始前的狀態。

```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- 如果任何一步失敗，兩個 UPDATE 都不會生效
```

### 一致性（Consistency）

交易前後，資料庫必須保持業務規則的一致性。例如，轉帳後雙方帳戶的總餘額必須相等。

### 隔離性（Isolation）

多個交易同時執行時，彼此之間不應該互相干擾。資料庫提供了四種隔離層級：

| 隔離層級 | 髒讀 | 不可重複讀 | 幻讀 |
|---------|:---:|:--------:|:---:|
| READ UNCOMMITTED | 可能 | 可能 | 可能 |
| READ COMMITTED | 避免 | 可能 | 可能 |
| REPEATABLE READ | 避免 | 避免 | 可能 |
| SERIALIZABLE | 避免 | 避免 | 避免 |

### 持久性（Durability）

交易一旦提交（COMMIT），其結果就永久保存在資料庫中，即使系統當機也不會遺失。

## 資料庫的分類

### 關聯式資料庫（RDBMS）

以表格形式儲存資料，使用 SQL 查詢。代表產品：

- **PostgreSQL**：功能最完整的開源 RDBMS
- **MySQL/MariaDB**：廣泛應用的 Web 資料庫
- **SQLite**：嵌入式、零配置
- **Oracle**：企業級商業資料庫
- **Microsoft SQL Server**：微軟生態系統

### NoSQL 資料庫

非關聯式資料庫，適合特定場景：

- **MongoDB**：文件資料庫，JSON 格式
- **Redis**：鍵值儲存，記憶體資料庫
- **Neo4j**：圖形資料庫
- **Cassandra**：寬列儲存

### 新興資料庫

- **DuckDB**：嵌入式 OLAP 資料庫
- **SQLite 4.0**：內建向量搜尋
- **EdgeDB**：基於 PostgreSQL 的下一代資料庫

## 參考資料

- [E.F. Codd 關聯式模型論文](https://www.google.com/search?q=EF+Codd+relational+model+1970)
- [ACID 特性說明](https://www.google.com/search?q=ACID+database+transaction+properties)
- [資料庫系統概念](https://www.google.com/search?q=database+system+concepts+introduction)
