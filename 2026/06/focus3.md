# 儲存引擎與索引技術：B-tree、LSM-Tree 與記憶體資料庫（1980s-2000s）

## 資料庫的核心：儲存引擎

儲存引擎是資料庫管理系統中最底層的元件，負責實際的資料儲存和檢索。關聯式資料庫將 SQL 查詢轉化為儲存引擎的操作——而儲存引擎的效能直接決定了資料庫的整體表現。

```
資料庫的層次架構：
─────────────────

  SQL 查詢
      │
      ▼
  ┌──────────────┐
  │  SQL 解析器   │
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  查詢最佳化器  │
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  執行引擎     │
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  儲存引擎     │  ← 我們在這裡
  │              │
  │  ┌────────┐  │
  │  │ 索引    │  │
  │  │ B-tree │  │
  │  │ Hash   │  │
  │  └────────┘  │
  │  ┌────────┐  │
  │  │ 緩衝池  │  │
  │  │ (Buffer)│  │
  │  └────────┘  │
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  磁碟/SSD    │
  └──────────────┘
```

## B-tree 與 B+ tree

### B-tree 的發明

1970 年，Rudolf Bayer 和 Edward McCreight 在波音公司發明了 B-tree。B 代表「Balanced」或「Bayer」——至今仍有爭議。

B-tree 解決了一個根本問題：**如何在磁碟上高效地組織有序資料**。

```
B-tree 的核心特性：
─────────────────

1. 平衡：所有葉節點在同一層
2. 多路：每個節點有多個子節點（不像二元樹只有兩個）
3. 有序：節點內的鍵值有序排列
4. 高效：插入、刪除、查詢都是 O(log n)

                 ┌─────┬─────┬─────┐
                 │  10 │  20 │  30 │
                 └──┬──┴──┬──┴──┬──┘
                    │     │     │
        ┌───────────┘     │     └───────────┐
        │                 │                 │
   ┌────┴────┐      ┌────┴────┐      ┌────┴────┐
   │ 1, 5, 8 │      │12,15,18│      │22,25,28│
   └─────────┘      └─────────┘      └─────────┘
```

### B+ tree：B-tree 的改進

1980 年代，B+ tree 成為資料庫索引的事實標準。它與 B-tree 的關鍵區別是：

```
B-tree vs B+ tree：
─────────────────

B-tree：
- 所有節點都儲存資料
- 內部節點也可作為查詢目標
- 範圍查詢需要在中序遍歷時回溯

B+ tree：
- 只有葉節點儲存資料
- 內部節點只儲存鍵值和指標
- 葉節點透過鏈結串列連接
- 範圍查詢只需要掃描葉節點鏈結串列

B+ tree 的結構：
                 ┌─────┬─────┬─────┐
                 │  10 │  20 │  30 │  ← 內部節點（只存鍵值）
                 └──┬──┴──┬──┴──┬──┘
                    │     │     │
        ┌───────────┘     │     └───────────┐
        │                 │                 │
   ┌────┴────┐      ┌────┴────┐      ┌────┴────┐
   │ 1,5,8   │──────│12,15,18 │──────│22,25,28 │  ← 葉節點
   │ data1   │  →   │ data2   │  →   │ data3   │  （存資料+鏈結）
   └─────────┘      └─────────┘      └─────────┘
```

B+ tree 在資料庫中的應用：

```sql
-- 在 PostgreSQL 中建立 B-tree 索引
CREATE INDEX idx_employee_salary ON employee USING BTREE (salary);

-- 這個索引加速了以下查詢：
SELECT * FROM employee WHERE salary = 75000;       -- 精確查詢
SELECT * FROM employee WHERE salary BETWEEN 50000 AND 80000;  -- 範圍查詢
SELECT * FROM employee ORDER BY salary;            -- 排序
```

### B-tree 的局限性

B-tree 在讀取多的場景表現優異，但在寫入多的場景有幾個問題：

1. **寫入放大**：每次插入可能導致多個節點分裂
2. **隨機寫入**：B-tree 的更新涉及多個位置的隨機寫入
3. **空間放大**：節點分裂後可能只有半滿

## LSM-Tree：寫入最佳化

### LSM-Tree 的誕生

1996 年，Patrick O'Neil 等人發表了 LSM-Tree（Log-Structured Merge-Tree）。LSM-Tree 專為寫入密集的工作負載設計。

```
LSM-Tree 的工作原理：
─────────────────

寫入流程：
1. 寫入 MemTable（記憶體中的有序結構）
2. MemTable 滿了 → 凍結為不可變的 SSTable
3. SSTable 寫入磁碟（順序寫入，非常快）
4. 背景進行 Compaction（合併多個 SSTable）

讀取流程：
1. 先在 MemTable 中查詢
2. 再在未凍結的 MemTable 中查詢
3. 從最新的 SSTable 到最舊的 SSTable 依次查詢
4. 使用布隆過濾器（Bloom Filter）跳過不相關的 SSTable

        寫入
          │
          ▼
    ┌──────────┐     ┌──────────┐
    │ MemTable │     │ Immutable│
    │ (記憶體)  │────►│ (凍結)   │
    └──────────┘     └────┬─────┘
                          │ flush
                          ▼
                   ┌──────────────┐
                   │ SSTable 0    │  ← Level 0（最新）
                   ├──────────────┤
                   │ SSTable 1    │
                   ├──────────────┤
                   │ SSTable 2    │  ← Level 1（合併後）
                   ├──────────────┤
                   │    ...       │
                   └──────────────┘
```

### LSM-Tree 的優勢

| 特性 | B-tree | LSM-Tree |
|------|--------|----------|
| 寫入效能 | 隨機寫入，慢 | 順序寫入，快 10-100x |
| 讀取效能 | O(log n)，穩定 | 可能需掃描多個 SSTable |
| 空間放大 | ~1.3x（節點分裂） | ~2-3x（未合併的 SSTable）|
| 寫入放大 | 中等 | 高（Compaction 開銷）|
| 範圍查詢 | 高效 | 高效（SSTable 有序）|

### LSM-Tree 的代表性實作

```
LSM-Tree 在業界的使用：
─────────────────

Google Bigtable (2006)
├── 第一個大規模 LSM-Tree 實作
├── 啟發了 HBase、Cassandra 等系統
└── 使用 GFS 作為底層儲存

Apache Cassandra (2008)
├── 寫入效能極佳
├── 支援多資料中心複寫
└── 使用 LSM-Tree + 布隆過濾器

LevelDB/RocksDB (2011)
├── Facebook 開發的嵌入式 LSM-Tree
├── 用於 MySQL（MyRocks 引擎）
└── 也用於 Kafka、TiDB 等系統
```

## 記憶體資料庫

### 記憶體 vs 磁碟的權衡

傳統資料庫將資料存在磁碟上，使用記憶體作為快取。2000 年代後，記憶體價格的下降催生了純記憶體資料庫：

```
磁碟資料庫 vs 記憶體資料庫：
─────────────────────────

磁碟資料庫（如 PostgreSQL、MySQL InnoDB）：
├── 主要儲存在磁碟
├── 使用 Buffer Pool 快取熱資料
├── 適合大量資料（TB 級）
├── 持久化是內建設計
└── 查詢延遲：毫秒級

記憶體資料庫（如 Redis、SAP HANA、VoltDB）：
├── 所有資料存在記憶體
├── 使用快照或日誌做持久化
├── 適合高效能場景
├── 持久化是「附加功能」
└── 查詢延遲：微秒級
```

### Redis（2009）

Redis 是最受歡迎的記憶體資料庫。它的成功證明了「簡單也可以很快」：

```python
import redis

r = redis.Redis()

# 字串
r.set('user:101:name', 'Alice')
r.get('user:101:name')

# 串列
r.lpush('queue', 'task1', 'task2')
r.rpop('queue')

# 雜湊
r.hset('user:101', mapping={'name': 'Alice', 'age': '30'})
r.hget('user:101', 'name')

# 有序集合（Sorted Set）
r.zadd('leaderboard', {'Alice': 100, 'Bob': 85, 'Charlie': 95})
r.zrevrange('leaderboard', 0, 2, withscores=True)
```

Redis 的資料總是常駐記憶體，因此達到了極高的效能（每秒數十萬次操作）。

### SAP HANA（2010）

SAP HANA 是企業級記憶體資料庫的代表，它證明了記憶體資料庫不僅可以處理簡單的鍵值操作，也可以處理複雜的分析查詢。

```
SAP HANA 的關鍵技術：
─────────────────

1. 列式儲存（Column Store）
   分析型查詢只需讀取相關欄位

2. 插入式執行
   將 SQL 編譯為機器碼執行

3. 資料壓縮
   記憶體較貴，需要高效壓縮

4. 多引擎
   關聯式 + 圖形 + 文字搜尋
```

## 儲存引擎的選型

### 場景決定選擇

```
使用場景分析：
─────────────────

高讀取、低寫入（內容管理系統）
→ B-tree（PostgreSQL、MySQL InnoDB）

高寫入、低讀取（日誌系統、IoT）
→ LSM-Tree（Cassandra、RocksDB）

低延遲快取（Session 管理、計數器）
→ 記憶體資料庫（Redis、Memcached）

分析型查詢（BI、報表）
→ 列式儲存（ClickHouse、Redshift）

即時交易（金融、電商）
→ B-tree + 強交易（PostgreSQL、Oracle、SQL Server）
```

### 儲存引擎的未來

```
儲存引擎的發展趨勢：
─────────────────

1. 統一儲存層
   └── 一個引擎同時支援行式和列式儲存

2. 計算-儲存分離
   └── 雲端原生架構（如 Amazon Aurora）

3. 新型硬體支援
   └── NVMe、Optane、CXL 記憶體擴展

4. AI 輔助
   └── 智慧緩存、預熱、預取
```

## 結語

儲存引擎是資料庫最「物理」的層次，直接面對硬體的特性。從 B-tree 到 LSM-Tree，從磁碟到記憶體，每一代儲存技術都在不同的取捨之間找到了適合的應用場景。

理解儲存引擎的工作原理，對於資料庫效能調優和技術選型至關重要。正如計算機科學家 Jim Gray 所說：「**記憶體是新的磁碟，磁碟是新的磁帶**」——儲存層次的變化永遠在重塑資料庫技術的面貌。

下一篇文章將介紹在儲存引擎之上——SQL 查詢處理與最佳化——如何將高階的 SQL 查詢轉化為高效的儲存引擎操作。

---

## 延伸閱讀

- [B-tree 發明論文](https://www.google.com/search?q=Bayer+McCreight+B-tree+paper)
- [LSM-Tree 論文](https://www.google.com/search?q=LSM-Tree+O'Neil+paper)
- [RocksDB 架構](https://www.google.com/search?q=RocksDB+architecture+design)
- [Redis 技術解析](https://www.google.com/search?q=Redis+internals+data+structures)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」歷史回顧系列之一。*
