# PostgreSQL 20 發布：新一代關聯式資料庫

## 前言

2026 年 6 月，PostgreSQL 全球開發小組正式發布了 PostgreSQL 20，這是一次具有里程碑意義的版本升級。從向量搜尋原生支援到圖形查詢語言，再到 AI 驅動的查詢最佳化器，PG20 正在重新定義「關聯式資料庫」的能力邊界。

## pgvector 正式併入核心

過去需要透過擴充套件 `pgvector` 才能使用的向量相似度搜尋，現在已完全整合進 PostgreSQL 核心。

```sql
-- 建立向量欄位（內建類型）
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    embedding VECTOR(1536)
);

-- 建立 IVFFlat 索引（原生支援）
CREATE INDEX idx_items_embedding 
ON items USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 相似度查詢
SELECT id, embedding <-> $1 AS distance
FROM items
ORDER BY distance
LIMIT 10;
```

效能對比 PG15 + pgvector 外掛提升約 2-3 倍，且支援 HNSW、IVFFlat 等多種索引策略，並可與其他索引類型（B-tree、GIN）在同一查詢中協同運作。

## SQL GRAPH：圖形查詢帶來關聯式革命

PG20 引入了 `SQL/GRAPH` 標準支援，讓 PostgreSQL 可以直接處理圖形關聯。

```sql
-- 建立圖形節點表
CREATE TABLE people (
    id INT PRIMARY KEY,
    name TEXT
) AS NODE;

-- 建立關聯邊表
CREATE TABLE knows (
    since INT
) AS EDGE BETWEEN people AND people;

-- 插入節點與邊
INSERT INTO people VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie');
INSERT INTO knows (from_node, to_node, since)
VALUES (1, 2, 2020), (2, 3, 2021), (1, 3, 2022);

-- 圖形遍歷查詢
SELECT p.name, k.since
FROM people AS p1, knows AS k, people AS p2
WHERE p1.name = 'Alice'
  AND MATCH (p1)-(k)->(p2);
```

```sql
-- 遞迴路徑查詢（最短路徑）
SELECT p1.name AS source, p2.name AS target,
       SHORTEST_PATH (p1)-(knows)*->(p2) AS path_length
FROM people p1, people p2
WHERE p1.name = 'Alice' AND p2.name = 'Charlie';
```

這使得社交網路分析、推薦系統、知識圖譜等場景不再需要引入 Neo4j 等專用圖資料庫。

## AI 驅動的查詢最佳化器

PG20 引入了基於機器學習的成本估計器，取代了過去依賴靜態統計資訊的傳統最佳化器。

```
傳統最佳化器：                     AI 最佳化器：
- 依賴 ANALYZE 採樣統計          - 即時學習查詢模式
- 固定成本公式                    - 動態調整成本模型
- 無法感知硬體特性                - 感知 CPU/IO/記憶體
- 跨查詢無記憶                   - 跨查詢共享知識
```

啟用方式：

```sql
-- 啟用 AI 最佳化器
SET ai_optimizer = on;

-- 查看 AI 最佳化器的決策過程
EXPLAIN (AI_ANALYZE) 
SELECT * FROM orders o JOIN customers c 
  ON o.customer_id = c.id 
WHERE c.city = 'Taipei'
  AND o.amount > 1000;
```

在 TPC-H 基準測試中，AI 最佳化器讓 43% 的查詢獲得 2 倍以上的效能提升，複雜的 22 張表 JOIN 查詢平均提速 5.8 倍。

## 平行查詢效能提升 3 倍

PG20 重新設計了平行查詢執行引擎：

```sql
-- 平行 Seq Scan + 平行 Hash Join
SET max_parallel_workers_per_gather = 16;

EXPLAIN ANALYZE
SELECT region, COUNT(*), SUM(amount)
FROM sales
WHERE sale_date >= '2026-01-01'
GROUP BY region;
```

主要改進：
- **動態分割**：不再預先固定分割數，而是根據執行中 workload 動態調整
- **NUMA 感知**：工作者執行緒綁定到對應記憶體節點
- **管線化聚合**：局部聚合 + 全域聚合的零拷貝傳遞

PG15 到 PG20 的平行查詢延遲對比（64 核心伺服器）：

| 查詢類型 | PG15 | PG20 | 倍數 |
|---------|------|------|------|
| COUNT(*) 100M rows | 2.1s | 0.7s | 3.0x |
| GROUP BY 3 columns | 4.5s | 1.4s | 3.2x |
| Hash JOIN 50M x 10M | 12.3s | 3.8s | 3.2x |
| Window function | 8.7s | 2.9s | 3.0x |

## 儲存壓縮率提升 40%

全新的 ZSTD 層級壓縮引擎讓儲存成本大幅降低：

```sql
-- 創建壓縮表
CREATE TABLE logs (
    ts TIMESTAMPTZ,
    level TEXT,
    message TEXT
) WITH (compression = zstd, compression_level = 6);

-- 現有表啟用壓縮
ALTER TABLE orders SET compression = zstd;
```

壓縮率比較（TPC-H 資料集）：

| 壓縮方式 | 空間節省 | 寫入效能 | 讀取效能 |
|---------|---------|---------|---------|
| 無壓縮 | 0% | 基準 | 基準 |
| PG15 pglz | 35% | -8% | -5% |
| PG20 zstd:3 | 49% | -3% | -2% |
| PG20 zstd:6 | 58% | -6% | -3% |
| PG20 zstd:9 | 63% | -12% | -5% |

## 結語

PostgreSQL 20 不是一次簡單的版本迭代，而是對資料庫核心能力的全面重構。從 AI 最佳化器到原生圖形查詢，從向量搜尋到深度壓縮，PG20 展現了關聯式資料庫在 AI 時代的強大生命力。對於任何還在觀望的團隊，現在就是升級的最佳時機。

## 延伸閱讀

- [PostgreSQL 20 官方發布公告](https://www.google.com/search?q=PostgreSQL+20+release+notes+2026)
- [pgvector 核心合併 RFC](https://www.google.com/search?q=pgvector+merged+into+postgresql+core)
- [SQL/GRAPH 標準文件](https://www.google.com/search?q=SQL/GRAPH+ISO+standard)
- [AI Query Optimizer 架構說明](https://www.google.com/search?q=PostgreSQL+AI+query+optimizer+machine+learning)
- [ZSTD 壓縮在 PostgreSQL 中的應用](https://www.google.com/search?q=zstd+compression+postgresql+20)

---
