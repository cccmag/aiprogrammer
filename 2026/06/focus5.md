# 分散式資料庫與 NoSQL：CAP 定理、Bigtable 與 MongoDB（2000s-2010s）

## 關聯式資料庫的極限

2000 年代中期，網際網路公司面臨了一個前所未有的挑戰：資料量呈指數級增長。Google 需要索引數十億網頁，Amazon 需要管理數億商品目錄和交易記錄，Facebook 需要儲存數十億使用者的社交關係。

傳統的關聯式資料庫在這種規模下遇到了根本性的瓶頸——**垂直擴展的極限**。

```
垂直擴展 vs 水平擴展：
─────────────────

垂直擴展（Scale Up）：用更強大的機器
├── 更快的 CPU（但摩爾定律放緩）
├── 更大的記憶體（但價格昂貴）
├── 更快的磁碟（NVMe，但仍有物理限制）
└── 上限：單台機器總有極限

水平擴展（Scale Out）：用更多機器
├── 成本更低（一般硬體即可）
├── 可彈性擴展（加機器即可）
├── 更高可用性（機器故障影響有限）
└── 挑戰：如何讓多台機器像一台一樣工作
```

## CAP 定理

### 定理的提出

2000 年，Eric Brewer 在 PODC 會議上提出了 CAP 猜想。2002 年，Seth Gilbert 和 Nancy Lynch 證明了這個猜想——從此 CAP 定理成為分散式系統設計的基石。

```
CAP 定理：
─────────────────

一個分散式系統最多只能同時滿足以下三個中的兩個：

C：一致性（Consistency）
   所有節點在同一時間看到相同的資料
   └── 讀取任一節點都得到最新的寫入結果

A：可用性（Availability）
   每個請求都能得到（非錯誤的）回應
   └── 系統總是可用的

P：分割容忍（Partition Tolerance）
   即使節點之間的通訊中斷（網路分割），系統仍能正常運作
   └── 分散式系統必然存在網路分割風險，所以 P 是必須的


                                一致
                                │
                            CP  │  CA
                                │
                        ────────┼──────── 可用
                                │
                            AP  │
                                │
                              分割
```

### CAP 的取捨

```
三種可能的組合：
─────────────────

CP（一致 + 分割容忍）
犧牲：可用性
代表：ZooKeeper、etcd、HBase
場景：金融交易、設定管理
行為：網路分割時停止寫入以保證一致性

AP（可用 + 分割容忍）
犧牲：一致性
代表：Amazon DynamoDB、Cassandra、CouchDB
場景：社群媒體、產品目錄
行為：網路分割時繼續寫入，但資料可能不一致

CA（一致 + 可用）
犧牲：分割容忍
代表：單機 PostgreSQL、MySQL
場景：傳統企業應用
行為：無法處理網路分割（因為不是分散式系統）
```

## Google Bigtable

### Bigtable 的誕生

2006 年，Google 發表了 Bigtable 論文——這是 NoSQL 運動的開端。Bigtable 是一個分散式的、基於 LSM-Tree 的鍵值儲存系統。

```
Bigtable 的資料模型：
─────────────────

不是表格(table)，而是巨大的、稀疏的、分散式的映射(map)

(row_key, column_family, column_qualifier, timestamp) → value

例如儲存網頁資訊：

"cnn.com/index.html" →
    contents:
        "html": "<html>CNN News...</html>"  (t3)
        "html": "<html>CNN...</html>"       (t2)
    anchor:
        "nytimes.com": "CNN News"           (t1)
    metadata:
        "language": "en"                    (t2)
        "crawl_time": "2026-06-01"          (t1)
```

### Bigtable 的架構

```
Bigtable 集群架構：
─────────────────

          ┌─────────────────────┐
          │   Chubby Lock       │
          │   Service           │  ← 分散式鎖定服務
          └──────────┬──────────┘
                     │
          ┌──────────┴──────────┐
          │    Master Server     │  ← 管理元資料
          └──────────┬──────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───┴───┐      ┌────┴────┐     ┌────┴────┐
│Tablet │      │ Tablet  │     │ Tablet  │
│Server │      │ Server  │     │ Server  │
│ 1     │      │ 2       │     │ 3       │
└───┬───┘      └────┬────┘     └────┬────┘
    │                │                │
    └────────────────┼────────────────┘
                     │
          ┌──────────┴──────────┐
          │   GFS (Google File  │
          │   System)           │  ← 底層分散式檔案系統
          └─────────────────────┘
```

Bigtable 的影響是深遠的：
- 啟發了 HBase（Hadoop 生態系的 Bigtable 實作）
- 啟發了 Cassandra（Facebook 開發，融合 Bigtable 和 Dynamo 思想）
- 啟發了 Accumulo（美國國家安全局的 Bigtable 實作）

## Amazon Dynamo

### Dynamo 的設計哲學

2007 年，Amazon 發表了 Dynamo 論文——這是一個 AP 風格的分散式鍵值儲存系統。與 Bigtable 不同，Dynamo 犧牲一致性換取極高的可用性。

```
Dynamo 的關鍵技術：
─────────────────

1. 一致性雜湊（Consistent Hashing）
   新增或移除節點時只需重新分配部分資料
   
2. 向量時鐘（Vector Clock）
   追蹤同一份資料的不同版本

3. 讀取修復（Read Repair）
   讀取時如果發現不一致，在背景修復

4. 謠言協議（Gossip Protocol）
   節點之間透過謠言傳播了解集群狀態

5. Hinted Handoff
   節點暫時不可用時，其他節點代為儲存資料
```

### 一致性雜湊

```
一致性雜湊的工作原理：
─────────────────

      Ring 空間（0 到 2^32 - 1）
      
                   0
                   │
          Node D   │   Node A
             ╱    ╲│╱    ╲
            │     ring      │
             ╲    ╱│╲    ╱
          Node C   │   Node B
                   │
                 2^32

每個節點和每個鍵都對應到 ring 上的一個位置
鍵被分配給 ring 上順時針方向的下一個節點

新增節點時：
 只影響相鄰的少量鍵，而非全部分配
```

Dynamo 的影響：啟發了 Amazon DynamoDB、Riak、Voldemort 等系統。

## MongoDB 與文件資料庫

### 文件模型的優勢

2009 年發布的 MongoDB 將文件資料庫推向了主流。文件模型與關聯式模型的核心差異在於：

```javascript
// 關聯式模型（正規化）
// employee 表格
{ id: 101, name: "Alice", dept_id: "D1" }
// department 表格
{ id: "D1", name: "Engineering" }

// 文件模型（嵌入）
{
  _id: 101,
  name: "Alice",
  department: {
    name: "Engineering",
    location: "Building A"
  },
  skills: ["Python", "SQL", "Kubernetes"],
  salary_history: [
    { year: 2024, amount: 70000 },
    { year: 2025, amount: 75000 },
    { year: 2026, amount: 82000 }
  ]
}
```

文件資料庫的優勢：
1. **Schema-less**：不同文件可以有不同結構
2. **巢狀資料**：自然地表示一對多關係
3. **陣列支援**：原生支援陣列和巢狀物件
4. **開發效率**：與 JSON/物件模型直接對應

### MongoDB 的擴展

MongoDB 透過分片（Sharding）實現水平擴展：

```
MongoDB 分片集群：
─────────────────

         ┌──────────────┐
         │  mongos      │  ← 路由層（應用程式連接到這裡）
         │  (Router)    │
         └──────┬───────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───┴───┐  ┌───┴───┐  ┌───┴───┐
│Shard 1│  │Shard 2│  │Shard 3│  ← 資料分片
│       │  │       │  │       │
│Primary│  │Primary│  │Primary│
│  │    │  │  │    │  │  │    │
│Secondary│  │Secondary│  │Secondary│  ← 副本
└────────┘  └────────┘  └────────┘
```

## Cassandra：Bigtable + Dynamo 的融合

### 設計目標

Cassandra（2008 年由 Facebook 開源）結合了 Bigtable 的資料模型和 Dynamo 的分散式架構：

```sql
-- Cassandra CQL（類似 SQL 的查詢語言）
CREATE TABLE user_timeline (
    user_id UUID,
    tweet_id UUID,
    content TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, created_at, tweet_id)
) WITH CLUSTERING ORDER BY (created_at DESC);

-- 寫入：任何節點都可以處理
INSERT INTO user_timeline (user_id, tweet_id, content, created_at)
VALUES (uuid(), uuid(), 'Hello World!', toTimestamp(now()));

-- 讀取：根據 partition key 路由到正確的節點
SELECT * FROM user_timeline WHERE user_id = ?;
```

### Cassandra 的特點

```
Cassandra 的關鍵特性：
─────────────────

1. 無主節點架構（Masterless）
   所有節點對等，沒有單點故障

2. 線性擴展
   加機器 = 線性提升吞吐量

3. 可調和的一致性
   每次操作可以選擇一致性等級（ONE, QUORUM, ALL）

4. 多資料中心支援
   原生支援跨資料中心複寫
```

## NewSQL：試圖兩全其美

### NewSQL 的嘗試

NewSQL 是 2010 年代初期出現的一個運動——試圖在不犧牲 ACID 交易的前提下實現水平擴展：

```
NewSQL 的代表系統：
─────────────────

Google Spanner (2012)
├── 全球分散式資料庫
├── TrueTime API：用 GPS + 原子鐘實現全域一致性
├── 外部一致性（External Consistency）
└── SQL 查詢 + 交易支援

CockroachDB (2015)
├── 開源的 Spanner 實作
├── 自動修復和重新平衡
├── 相容 PostgreSQL 協議
└── 支援地理分佈部署

TiDB (2016)
├── 相容 MySQL 協議
├── 儲存與計算分離
├── HTAP（同時支援交易和分析）
└── 使用 Raft 共識協議
```

### Google Spanner 的突破

Spanner 解決了分散式資料庫中最困難的問題——全域一致性：

```
Spanner 的 TrueTime API：
─────────────────

問題：在分散式系統中，如何同步時間？
傳統方法：NTP（網路時間協定），誤差大

Spanner 方法：
├── 每個資料中心安裝 GPS 接收器和原子鐘
├── TrueTime API 回傳時間區間 [earliest, latest]
├── commit 時等待到 latest 時間過去
└── 保證：所有節點看到的時間順序一致

這個設計讓 Spanner 實現了：
- 外部一致性（相當於單機 Serializable）
- 全域分散式交易
- 無鎖定的唯讀交易
```

## NoSQL vs SQL：不是戰爭，是工具選擇

### 選擇指南

```
場景            推薦                    不推薦
────────────────────────────────────
交易處理 (OLTP)  PostgreSQL, MySQL        MongoDB (需自行處理交易)
內容管理          MongoDB, Couchbase      關係型 (Schema 限制)
日誌系統          Elasticsearch, Cassandra 關係型 (寫入瓶頸)
社交關係圖        Neo4j, ArangoDB         關聯式 (JOIN 過多)
時間序列          InfluxDB, TimescaleDB   通用資料庫 (未最佳化)
全域分佈          Spanner, CockroachDB    單機資料庫 (無法擴展)
快取              Redis                   磁碟資料庫 (延遲高)
```

## 結語

分散式資料庫與 NoSQL 的興起是 2000 年代資料管理領域最重要的變革。CAP 定理為分散式系統提供了理論框架，Bigtable 和 Dynamo 提供了實作典範，MongoDB 和 Cassandra 將這些理念帶給了廣大開發者。

2010 年代中期以後，我們看到了一個「收斂」的趨勢：關聯式資料庫開始吸收 NoSQL 的優點（如 JSON 支援、水平擴展），而 NoSQL 資料庫也開始加入更多的關聯式功能（交易、SQL 查詢）。同質化的趨勢在雲端資料庫時代更加明顯——這正是我們下一篇文章的主題。

---

## 延伸閱讀

- [CAP 定理](https://www.google.com/search?q=CAP+theorem+Brewer+distributed+systems)
- [Google Bigtable 論文](https://www.google.com/search?q=Bigtable+a+distributed+storage+system+structured+data)
- [Amazon Dynamo 論文](https://www.google.com/search?q=Dynamo+Amazon+highly+available+key-value+store)
- [Google Spanner 論文](https://www.google.com/search?q=Spanner+Google+globally+distributed+database)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」歷史回顧系列之一。*
