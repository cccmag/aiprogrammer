# 專題 3：PostgreSQL 關聯式資料庫

## 功能最豐富的開源資料庫

PostgreSQL 被廣泛認為是最先進的開源關聯式資料庫，以其穩定性、功能豐富性和標準合規性著稱。

### 核心特性

#### ACID 事務保證
PostgreSQL 提供完整的事務支援，包括 MVCC（多版本並發控制）、保存點（Savepoint）與可序列化隔離層級。

```javascript
// 使用 pg 套件執行事務
import pg from 'pg'
const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL })

async function transfer(fromId, toId, amount) {
  const client = await pool.connect()
  try {
    await client.query('BEGIN')
    await client.query('UPDATE accounts SET balance = balance - $1 WHERE id = $2', [amount, fromId])
    await client.query('UPDATE accounts SET balance = balance + $1 WHERE id = $2', [amount, toId])
    await client.query('COMMIT')
  } catch (e) {
    await client.query('ROLLBACK')
    throw e
  } finally {
    client.release()
  }
}
```

#### 進階資料類型
PostgreSQL 支援豐富的資料類型，包括 JSON/JSONB、陣列、範圍類型、網路位址類型、幾何類型與自定義類型。

```javascript
// JSONB 欄位查詢範例
const result = await pool.query(`
  SELECT * FROM products
  WHERE metadata @> '{"category": "electronics"}'
  AND price < $1
`, [1000])
```

#### 索引多樣性
提供 B-tree、Hash、GiST、GIN、SP-GiST、BRIN 等多種索引類型，適應不同的查詢模式。

```javascript
// GIN 索引加速 JSONB 查詢
await pool.query(`
  CREATE INDEX idx_products_metadata
  ON products USING GIN (metadata)
`)
```

### 使用場景

- **金融系統**：嚴格的資料完整性與事務保證
- **地理資訊系統**：PostGIS 擴展提供專業的地理空間功能
- **資料倉儲**：平行查詢執行與視窗函數支援分析查詢
- **全文搜尋**：內建全文搜尋引擎，支援分詞與排名

### 擴展生態系統

PostgreSQL 擁有豐富的擴展生態：

- **PostGIS**：地理空間資料處理
- **pgvector**：向量相似度搜尋，支援 AI 應用
- **TimescaleDB**：時間序列資料最佳化
- **Citus**：水平分佈式擴展
- **pg_partman**：自動化資料分割管理

### 效能調校

1. **shared_buffers**：通常設為系統記憶體的 25%
2. **work_mem**：排序與雜湊操作的記憶體限制
3. **effective_cache_size**：作業系統快取估算
4. **maintenance_work_mem**：維護操作（如 VACUUM）的記憶體

延伸閱讀：https://www.google.com/search?q=PostgreSQL+database+tutorial
https://www.google.com/search?q=PostgreSQL+performance+tuning+guide
