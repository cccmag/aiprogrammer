# AI 時代的資料庫：向量資料庫與 AI 原生儲存（2020s 展望）

## AI 對資料庫的改變

AI 與資料庫的關係是雙向的：AI 正在改變資料庫（智慧最佳化、自動化管理），資料庫也在改變 AI（向量資料庫、AI 資料平台）。

```
AI 與資料庫的雙向影響：
─────────────────

AI → 資料庫：
├── 查詢最佳化：ML 模型預測查詢成本
├── 自動調優：AI 建議索引和統計資訊
├── 異常檢測：自動發現效能問題
├── 自然語言查詢：NL2SQL
└── 自主管理：無人值守的 DBA

資料庫 → AI：
├── 向量資料庫：嵌入儲存與相似度搜索
├── 特徵儲存（Feature Store）：ML 特徵管理
├── ML 生命週期管理：模型版本、實驗追蹤
└── 資料治理：AI 資料的品質與合規
```

## 向量資料庫

### 為什麼需要向量資料庫？

LLM 時代的核心需求是「相似度搜索」——給定一個查詢嵌入，找到最相似的資料嵌入。

```
向量資料庫 vs 傳統搜尋：
─────────────────

傳統搜尋（關鍵字）：
查詢：「可愛的貓咪影片」
匹配：包含「可愛」「貓咪」「影片」的結果
問題：無法理解語義（「毛茸茸的喵星人」不會被匹配）

向量搜尋（語義）：
查詢：「可愛的貓咪影片」
      ↓
嵌入模型：[0.23, 0.87, -0.12, ..., 0.45]
      ↓
向量資料庫找到最相似的向量
      ↓
結果：「毛茸茸的喵星人玩耍畫面」（語義相關但沒有共同關鍵字）
```

### 向量嵌入

向量嵌入（Embedding）是 `AI → 向量` 的轉換過程：

```
嵌入的維度：
─────────────────

文字嵌入：
「資料庫系統」 → [0.12, -0.45, 0.78, ..., 0.33]  (1536 維)

圖片嵌入：
  🐱           → [0.89, 0.23, -0.56, ..., 0.12]  (1024 維)

多模態嵌入：
「一隻橘貓在鍵盤上睡覺」
  + 🐱 圖片    → [0.67, 0.34, -0.78, ..., 0.91]  (共同語義空間)
```

### 向量搜尋演算法

向量搜尋的核心挑戰是「在百萬到十億級的向量中快速找到最近鄰」：

```
最近鄰搜尋演算法：
─────────────────

精確最近鄰（KNN）
├── 計算查詢向量與所有向量的距離
├── 回傳距離最近的 k 個
├── 時間複雜度：O(n)
└── 適合：小資料集（< 10 萬）

近似最近鄰（ANN）
├── 使用索引結構加速
├── 犧牲一點準確度換取巨大效能提升
└── 適合：大資料集（> 100 萬）

主要的 ANN 演算法：

1. IVFFlat（Inverted File Index）
   將向量空間劃分為多個單元
   查詢時只搜索最近的單元
   └── 時間複雜度：O(log n)

2. HNSW（Hierarchical Navigable Small World）
   建立多層圖結構
   自上而下搜索
   └── 高精度、快速，但記憶體使用較多

3. PQ（Product Quantization）
   壓縮向量減少儲存空間
   壓縮比可達 32x
   └── 適合超大規模資料集
```

### 向量資料庫的實作

```python
# 使用 Pinecone 向量資料庫
import pinecone

pinecone.init(api_key="...")

# 建立索引
pinecone.create_index(
    name="product-search",
    dimension=1536,
    metric="cosine"
)

index = pinecone.Index("product-search")

# 插入向量
index.upsert([
    ("prod_001", [0.12, -0.45, ..., 0.33],
     {"name": "無線滑鼠", "price": 1290}),
    ("prod_002", [0.89, 0.23, ..., -0.12],
     {"name": "機械鍵盤", "price": 3990}),
])

# 搜尋相似
results = index.query(
    vector=[0.15, -0.40, ..., 0.30],
    top_k=10,
    include_metadata=True
)
```

### 向量資料庫的選擇

| 資料庫 | 類型 | ANN 演算法 | 優點 | 適合場景 |
|-------|------|-----------|------|---------|
| Pinecone | 雲端託管 | HNSW | 全託管、高可用 | 生產環境 |
| Weaviate | 雲端/本地 | HNSW + PQ | 內建搜尋+向量 | 混合搜尋 |
| Qdrant | 雲端/本地 | HNSW + 過濾 | 高效過濾查詢 | 大規模系統 |
| Milvus | 分散式 | IVF/HNSW | 超高效能 | 企業級 |
| Chroma | 嵌入式 | HNSW | 輕量、本地 | 開發原型 |
| pgvector | PostgreSQL | IVFFlat/HNSW | 與 SQL 整合 | 已有 PG |

### pgvector：PostgreSQL 中的向量搜尋

2026 年，pgvector 被納入 PostgreSQL 核心（PostgreSQL 20），標誌著向量搜尋成為關聯式資料庫的標準功能：

```sql
-- PostgreSQL 20 中的向量搜尋
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    embedding VECTOR(1536)  -- 原生向量型別
);

-- 建立 HNSW 索引
CREATE INDEX idx_product_embedding 
ON products USING HNSW (embedding vector_cosine_ops);

-- 相似度查詢
SELECT name, 
       embedding <=> '[0.12, -0.45, ..., 0.33]'::vector 
       AS similarity
FROM products
ORDER BY similarity
LIMIT 10;

-- 混合查詢（向量 + 關鍵字）
SELECT name, 
       embedding <=> query_embedding AS similarity
FROM products
WHERE category = '電子產品'
  AND price < 5000
ORDER BY similarity
LIMIT 10;
```

## AI 驅動的查詢最佳化

### 學習型最佳化器

傳統的基於成本的查詢最佳化器依賴於靜態的統計資訊和啟發式規則。AI 驅動的最佳化器使用機器學習來做更好的決策：

```
ML 在查詢最佳化的應用：
─────────────────

1. 基數估算（Cardinality Estimation）
   問題：傳統直方圖無法準確估算複雜過濾條件的選擇率
   解決：用神經網路學習查詢條件的真實選擇率
   └── 誤差從 1000% 降至 50%

2. JOIN 順序選擇
   問題：n 個表的 JOIN 有 O(4^n) 種可能
   解決：用強化學習學習最佳 JOIN 策略
   └── 複雜查詢的執行時間減少 30-50%

3. 索引建議
   問題：該建立哪些索引？
   解決：使用 ML 分析工作負載並推薦索引
   └── AWS Automatic Index Tuning 已內建此功能
```

### Oracle Autonomous Database

Oracle 的 Autonomous Database 是 AI 驅動資料庫管理的先驅：

```
Autonomous Database 的自動化能力：
─────────────────

1. 自動調優
   監控工作負載，自動調整參數
   自動建立/刪除索引

2. 自動安全
   自動偵測威脅
   自動套用安全修補

3. 自動備份
   自動排程備份
   自動測試恢復

4. 自動擴展
   根據負載自動調整資源
   零停機擴展

5. 自動修復
   偵測到故障自動切換
   自動修復資料頁面
```

## NL2SQL：自然語言查詢資料庫

### 從 SQL 到自然語言

NL2SQL（Natural Language to SQL）是 AI 時代資料庫最重要的使用者體驗變革：

```sql
-- 使用者的自然語言查詢：
"上個月的銷售額排名前 5 的產品是什麼？"

-- AI 自動轉換為 SQL：
SELECT p.name, SUM(o.amount) as total_sales
FROM products p
JOIN orders o ON p.id = o.product_id
WHERE o.order_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  AND o.order_date < DATE_TRUNC('month', CURRENT_DATE)
GROUP BY p.id, p.name
ORDER BY total_sales DESC
LIMIT 5;

-- 使用者不需要懂 SQL！
```

### NL2SQL 的挑戰

```
NL2SQL 的技術挑戰：
─────────────────

1. 語意模糊
   「上個月的資料」→ 哪個月份？自然月還是 30 天？

2. 多表關聯
   使用者不一定知道資料庫的結構
   需要自動推導 JOIN 路徑

3. 計算邏輯
   「成長率」、「佔比」→ 需要理解業務定義

4. 安全控管
   確認使用者有查詢這些資料的權限

5. 幻覺控制
   不生成不存在欄位的查詢
```

## AI 原生資料庫的願景

### 從 Database 到 AI Data Platform

未來的資料平台將不僅僅是儲存和查詢資料——它將是一個完整的 AI 開發平台：

```
AI 原生資料平台（2026+）：
─────────────────

┌──────────────────────────────────────────┐
│  應用層                                   │
│  ┌────────┬────────┬────────┬────────┐  │
│  │ SQL    │ NL 查詢│ RAG    │ Agent  │  │
│  │ 查詢   │        │ 應用   │ 記憶   │  │
│  └────────┴────────┴────────┴────────┘  │
├──────────────────────────────────────────┤
│  AI 引擎                                 │
│  ┌────────┬────────┬────────┬────────┐  │
│  │ 向量    │ 嵌入   │ 重新   │ LLM   │  │
│  │ 搜尋    │ 生成   │ 排序   │ 推理   │  │
│  └────────┴────────┴────────┴────────┘  │
├──────────────────────────────────────────┤
│  資料引擎                                │
│  ┌────────┬────────┬────────┬────────┐  │
│  │ 關聯式  │ 文件   │ 圖形   │ 串流   │  │
│  │ 儲存    │ 儲存   │ 儲存   │ 處理   │  │
│  └────────┴────────┴────────┴────────┘  │
├──────────────────────────────────────────┤
│  統一儲存層（Object Store）              │
│  ┌──────────────────────────────────┐   │
│  │  Parquet / Iceberg / Delta Lake   │   │
│  └──────────────────────────────────┘   │
└──────────────────────────────────────────┘
```

### 關鍵技術趨勢

```
AI 原生資料庫的技術趨勢：
─────────────────

1. 多模型融合
   單一資料庫支援關聯式、文件、圖形、向量
   └── PostgreSQL 20, SQL:2026 標準支援多模型

2. 嵌入原生生
   資料庫內建嵌入生成功能
   └── 不再需要外部模型 API

3. 即時 RAG
   資料庫原生支援 RAG 工作流程
   └── 查詢 → 檢索 → 生成，一站式完成

4. 自主管理
   AI 完全接管 DBA 工作
   └── 索引管理、效能調優、安全防護全自動化

5. 資料+AI 合規
   內建資料治理和 AI 合規功能
   └── 自動化資料溯源、偏差檢測、隱私保護
```

## 結語

AI 時代的資料庫正處於一個激動人心的轉折點。向量資料庫將語義理解帶入了資料搜尋，ML 最佳化器讓資料庫更聰明、更自動化，NL2SQL 讓資料查詢變得前所未有的簡單。

展望未來，資料庫與 AI 的界線將越來越模糊——資料平台將不僅儲存和管理資料，還將理解、分析和生成洞察。正如六十年來資料庫技術的每一次躍進，AI 原生資料庫的核心目標始終不變：**讓開發者能夠更簡單、更高效地從資料中獲取價值**。

本期完整歷史回顧到此結束。從打孔卡到向量資料庫，資料管理技術的六十年演進見證了人類對資料的永恆追求——理解世界、做出更好決策、創造更大價值。

---

## 延伸閱讀

- [向量資料庫比較](https://www.google.com/search?q=vector+database+comparison+Pinecone+Weaviate+Qdrant)
- [pgvector 文件](https://www.google.com/search?q=pgvector+PostgreSQL+vector+search)
- [Oracle Autonomous Database](https://www.google.com/search?q=Oracle+Autonomous+Database+architecture)
- [NL2SQL 技術](https://www.google.com/search?q=NL2SQL+natural+language+to+SQL)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」歷史回顧系列之一。*
