# 雲端資料庫與 Data Lakehouse：Snowflake、Databricks 與 Serverless（2010s-2020s）

## 雲端運算對資料庫的影響

2010 年代，雲端運算從根本上改變了資料庫的部署和營運模式。傳統的「買伺服器、裝資料庫、手動管理」模式，被「按需使用、彈性擴展、全託管」的雲端服務所取代。

```
傳統資料庫 vs 雲端資料庫：
─────────────────────────

傳統模式：
├── 需要採購硬體（數週到數月）
├── 需要預估容量（容易過度或不足）
├── 需要 DBA 團隊（管理備份、修補、調優）
├── 擴展需要停機（更換更大機器）
└── 成本：固定成本（不管用不用都要付）

雲端模式：
├── 幾分鐘即可建立資料庫
├── 自動擴展（不用預估容量）
├── 全託管服務（備份、修補自動完成）
├── 零停機升級
└── 成本：按使用付費（用多少付多少）
```

## Amazon Aurora：雲端原生資料庫

### Aurora 的設計哲學

2014 年，Amazon 發布了 Aurora——一個與 MySQL 和 PostgreSQL 相容的雲端原生關聯式資料庫。Aurora 的核心創新是**計算與儲存分離**：

```
Aurora 的架構：
─────────────────

傳統資料庫：計算和儲存在同一台機器
┌─────────────────────┐
│     資料庫實例       │
│  ┌──────────────┐  │
│  │  CPU/記憶體  │  │
│  │  ────────   │  │
│  │  儲存 (本地磁碟)│  │
│  └──────────────┘  │
└─────────────────────┘

Aurora：計算和儲存分離
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Writer   │   │ Reader   │   │ Reader   │
│ Instance │   │ Instance │   │ Instance │
│ (計算)   │   │ (計算)   │   │ (計算)   │
└────┬─────┘   └────┬─────┘   └────┬─────┘
     │              │              │
     └──────────────┼──────────────┘
                    │
           ┌────────┴────────┐
           │  Shared Storage │  ← 6 副本跨 3 AZ
           │  (分散式儲存層)  │
           └─────────────────┘
```

### Aurora 的關鍵技術

```
Aurora 的創新：
─────────────────

1. 僅傳送日誌的複寫
   只將 REDO 日誌傳送到儲存層
   儲存層自行將日誌套用到資料頁面
   → 網路流量減少 100x

2. 6 副本儲存
   跨 3 個可用區域（AZ）儲存 6 份資料
   寫入需要 4/6 確認

3. 快速崩潰恢復
   傳統資料庫：啟動時需復原所有日誌
   Aurora：儲存層持續套用日誌
   → 崩潰後幾秒內即可恢復

4. 自動擴展儲存
   儲存自動從 10GB 擴展到 128TB
   完全透明，不需停機
```

## Snowflake：資料倉儲即服務

### Snowflake 的革命

2012 年成立、2014 年正式發布的 Snowflake 從頭開始設計了一個雲端原生資料倉儲。它實現了真正的**計算與儲存分離**和**按需付費**：

```
Snowflake 的三層架構：
─────────────────

查詢結果
    │
    ▲
┌───┴─────────────────┐
│  計算層（Warehouses） │  ← 獨立的計算集群
│                      │    可按需啟動/停止
│  Warehouse 1 (XL)    │    不同 Warehouse 可獨立擴展
│  Warehouse 2 (SMALL) │
│  Warehouse 3 (分析)   │
└──────────┬───────────┘
           │
           ▼
┌──────────┴───────────┐
│  查詢處理層           │  ← 全域查詢最佳化器
│  (Query Processing)  │
└──────────┬───────────┘
           │
           ▼
┌──────────┴───────────┐
│  儲存層               │  ← 壓縮、列式、不可變
│  (Cloud Storage)     │    S3/Blob Storage
│                      │    按實際儲存量付費
└──────────────────────┘
```

### Snowflake 的殺手級功能

```sql
-- 1. 零複製克隆（Zero-Copy Cloning）
-- 建立資料庫的「快照」而不實際複製資料
CREATE DATABASE production_clone
  CLONE production;

-- 2. 時間旅行（Time Travel）
-- 查詢過去任何時間點的資料
SELECT * FROM orders
  AT(TIMESTAMP => '2026-06-01 10:00:00'::TIMESTAMP);

-- 3. 資料共享
-- 跨 Snowflake 帳號共享資料，無需實際傳送
CREATE SHARE my_share;
GRANT SELECT ON DATABASE analytics TO SHARE my_share;
```

### Snowflake 的影響

Snowflake 的成功證明了「資料庫即服務」（DBaaS）的商業模式。它的 IPO（2020 年）是軟體史上最大的 IPO 之一。

## Databricks 與 Data Lakehouse

### 資料湖的困境

2010 年代後期，企業面臨一個尷尬的局面：

```
資料湖（Data Lake）：
├── 優點：便宜、儲存所有格式的資料
├── 缺點：缺乏交易支援、資料品質差
└── 口號：「把資料丟進去，然後...再也找不到」

資料倉儲（Data Warehouse）：
├── 優點：高效查詢、資料品質高
├── 缺點：昂貴、Schema 嚴格
└── 口號：「結構化查詢，但只接受結構化資料」
```

資料科學家需要在資料湖和資料倉儲之間來回搬運資料——這種「兩個系統」的模式效率極低。

### Lakehouse 架構的提出

2020 年，Databricks 提出了 Lakehouse 架構——試圖在資料湖的低成本儲存上實現資料倉儲的交易和查詢能力：

```
Lakehouse 架構：
─────────────────

┌──────────────────────────────────────┐
│  BI 工具 │ 資料科學 │ ML 訓練 │ SQL  │
└──────────┴──────────┴────────┴──────┘
                    │
                    ▼
┌──────────────────────────────────────┐
│         查詢引擎                      │
│  (Spark SQL, Presto, DuckDB)        │
└────────────────┬─────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│  開放資料表格式                       │
│  ┌────────┬────────┬────────┐       │
│  │ Apache │ Delta  │ Apache │       │
│  │ Iceberg│ Lake   │ Hudi   │       │
│  └────────┴────────┴────────┘       │
│  ┌──────────────────────────────┐   │
│  │  ACID 交易、版本控制、Schema │   │
│  │  演進、時間旅行              │   │
│  └──────────────────────────────┘   │
└────────────────┬─────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│  物件儲存（S3、ADLS、GCS）          │
│  Parquet/ORC/Avro 格式               │
└──────────────────────────────────────┘
```

### Apache Iceberg 與開放格式

湖倉一體的關鍵是開放資料表格式。Apache Iceberg 是其中最受歡迎的：

```sql
-- Iceberg 的關鍵特性在 SQL 中的體現

-- Schema 演進：新增欄位不中斷查詢
ALTER TABLE orders ADD COLUMN discount DOUBLE;

-- 時間旅行：查詢歷史版本
SELECT * FROM orders FOR SYSTEM_TIME AS OF '2026-06-01';

-- 隱藏分割：不需管理分區
-- 寫入時自動根據 partition 欄位組織資料

-- 資料壓縮：自動合併小檔案
CALL system.rewrite_data_files('orders');
```

## Amazon Redshift Spectrum 與查詢聯邦

### 跨資料來源查詢

雲端資料庫的發展還有一個重要趨勢——查詢聯邦（Query Federation）：

```
Redshift Spectrum：
─────────────────

一個 SQL 查詢可以同時查詢：
├── Redshift 本地資料
├── S3 上的 Parquet 資料
└── 其他 AWS 服務的資料

SELECT r.order_id, r.amount, s.sentiment
FROM redshift.orders r
JOIN spectrum.reviews s ON r.product_id = s.product_id
WHERE r.date > '2026-01-01'
  AND s.sentiment = 'positive';
-- 不需要資料搬移！
```

## Serverless 資料庫

### 從預置容量到按需使用

Serverless 是資料庫雲端化的終極形態——開發者完全不需要管理任何基礎設施：

```
資料庫管理的演進：
─────────────────

2000s：自行管理
├── 買硬體、裝系統、設定備份、
├── 監控效能、套用修補、處理故障
└── 需要專業 DBA 團隊

2010s：託管服務（RDS、Cloud SQL）
├── 自動備份、修補、監控
├── 但仍然需要「預置」容量
└── 需要選擇實體大小

2020s：Serverless（Aurora Serverless、Neon）
├── 自動擴展：從零到數千 TPS
├── 按使用付費：不用時不收費
└── 不需要管理任何基礎設施
```

### Neon：開源的 Serverless PostgreSQL

Neon（2022 年發布）展示了 Serverless 資料庫的設計方向：

```
Neon 的關鍵技術：
─────────────────

1. 計算-儲存完全分離
   計算節點無狀態，可隨時啟動/停止

2. 頁面伺服器（Page Server）
   將資料分為「基礎版本」和「變更日誌」
   類似 Git 的版本管理

3. 分支（Branching）
   像 Git 分支一樣複製資料庫
   用於開發、測試、CI/CD

4. 冷啟動加速
   使用預熱池減少啟動延遲
   從休眠到回應僅需數百毫秒
```

## 雲端資料庫的未來

### 多雲與全球分佈

```
雲端資料庫的發展方向：
─────────────────

1. 多雲支援
   Google Spanner → 跨 AWS、Azure、GCP
   CockroachDB → 任意雲端或本地部署
   MongoDB Atlas → 多雲託管

2. 全球分佈
   讀取：就近讀取（<10ms 延遲）
   寫入：全域一致性（Spanner）
   衝突處理：CRDT（Conflict-free Replicated Data Types）

3. AI 整合
   向量搜尋（內建）
   自然語言查詢（NL2SQL）
   自動效能調優
```

## 結語

雲端資料庫與 Data Lakehouse 代表了資料管理從「產品」到「服務」的轉變。隱藏背後的複雜性、提供按需使用的彈性、分離儲存與計算——這些理念讓資料庫的部署和營運變得前所未有的簡單。

而在這個時代，一個新的趨勢正在浮現：AI 與資料庫的深度融合。向量資料庫、AI 最佳化器、自然語言查詢——這些技術正在開啟資料庫管理的新時代。

下一篇文章將介紹 AI 時代的資料庫——向量資料庫與 AI 原生儲存。

---

## 延伸閱讀

- [Amazon Aurora 論文](https://www.google.com/search?q=Amazon+Aurora+design+considerations)
- [Snowflake 架構](https://www.google.com/search?q=Snowflake+database+architecture+cloud)
- [Lakehouse 架構](https://www.google.com/search?q=Lakehouse+architecture+Databricks)
- [Apache Iceberg](https://www.google.com/search?q=Apache+Iceberg+table+format)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」歷史回顧系列之一。*
