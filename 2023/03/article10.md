# 資料結構在資料庫的應用

## B-Tree

B-Tree（B 樹）是一種自平衡的多路搜尋樹，廣泛用於資料庫的索引系統。與二元搜尋樹不同，B-Tree 的每個節點可以包含多個鍵值與多個子節點，這種設計大幅降低了樹的高度，非常適合磁碟存取。

**B-Tree 的特性**：
- 所有葉節點都在同一層，保證平衡。
- 每個節點最多包含 2t-1 個鍵（t 為最小度數）。
- 內部節點最多有 2t 個子節點。
- 搜尋、插入、刪除皆為 O(log n)。
- 高分支因子減少樹高，每次讀取節點就是一次 I/O。

**B+ Tree 變體**：MySQL InnoDB 儲存引擎使用 B+ Tree。與 B-Tree 的主要差異是：所有資料都存在葉節點，內部節點只儲存鍵值作為導航。葉節點之間透過鏈結串列連接，支援高效的範圍查詢（Range Query）。

## LSM-Tree

LSM-Tree（Log-Structured Merge-Tree）是專為寫入最佳化的資料結構，廣泛用於 LevelDB、RocksDB、Cassandra 等 NoSQL 資料庫。

**運作原理**：
1. 新資料先寫入記憶體中的有序結構（MemTable）。
2. MemTable 滿時，寫入磁碟成為 SSTable（Sorted String Table）。
3. 背景 Compaction 將多個 SSTable 合併，清除過期資料。

LSM-Tree 寫入效率極高（順序寫入），但讀取較慢（需檢查多層 SSTable），常搭配 Bloom Filter 加速鍵不存在判斷。

## 雜湊索引

使用雜湊表將鍵直接映射到磁碟位置，支援 O(1) 精確查詢，但不支援範圍查詢。Redis 的字典就是純記憶體的雜湊索引。

## 索引比較

| 索引類型 | 優點 | 缺點 | 典型資料庫 |
|---------|------|------|-----------|
| B+ Tree | 範圍查詢、穩定 O(log n) | 寫入開銷大 | MySQL InnoDB |
| LSM-Tree | 寫入極快（順序 I/O） | 讀取較慢 | Cassandra, LevelDB |
| Hash Index | 精確查詢 O(1) | 不支援範圍查詢 | Redis（部分） |

## 延伸閱讀

- https://www.google.com/search?q=B+Tree+database+index+InnoDB+儲存引擎+磁碟存取
- https://www.google.com/search?q=LSM+Tree+vs+B+Tree+write+amplification+compaction+比較
- https://www.google.com/search?q=資料庫+索引+B+Tree+Hash+LSM+Tree+設計+選擇
