# GraphRAG：知識圖譜與 LLM 的深度融合

## 從傳統 RAG 到 GraphRAG

Retrieval-Augmented Generation（RAG）已成為 LLM 應用的事實標準架構。傳統 RAG 的核心流程是：將文件切割成片段（chunk）→ 轉換為向量嵌入 → 查詢時進行向量相似度搜索 → 將檢索結果注入 LLM 上下文。

但傳統 RAG 有兩個根本性弱點：

```
向量相似度搜索的局限性
─────────────────

問題一：全局性問題
┌─ 查詢：「公司過去五年的研發策略演變？」
│  需要跨多份文件、多年資料的綜合推理
│  向量搜索只能找到局部相關片段
│  無法理解主題之間的層次關係
└─ 結果：回答片面或遺漏關鍵脈絡

問題二：連接性問題
┌─ 查詢：「A 團隊的技術決策如何影響了 B 部門的產品路線圖？」
│  需要理解實體之間的間接關聯
│  向量搜索只能找到直接包含 A 和 B 的文件
│  無法推導因果鏈條
└─ 結果：無法回答跨領域的推理問題
```

Microsoft GraphRAG 正是為解決這些問題而生。

## GraphRAG 的核心架構

GraphRAG 的核心理念是：**將非結構化文字轉換為結構化知識圖譜，再用圖譜來增強 LLM 的生成品質**。

```
GraphRAG 索引流程
─────────────────

原始文件（非結構化文字）
    ↓
1. 實體識別（Entity Extraction）
   └── LLM 從文字中提取人物、組織、概念、事件等實體
    ↓
2. 關係抽取（Relationship Extraction）
   └── LLM 識別實體之間的關係（影響、屬於、導致...）
    ↓
3. 圖譜建構（Graph Construction）
   └── 節點 = 實體，邊 = 關係，形成知識圖譜
    ↓
4. 社群層級劃分（Community Detection）
   └── Leiden 演算法進行層級聚類
    ↓
5. 社群摘要生成（Community Summarization）
   └── LLM 為每個社群產生摘要報告
    ↓
儲存：知識圖譜 + 社群摘要 + 向量索引
```

### GraphRAG 2.0 的改進

GraphRAG 2.0（2025 年 2 月發布，v2.0.0）引入了**動態社群選擇**機制：

```
GraphRAG 2.0 動態社群選擇
─────────────────

傳統 GraphRAG 查詢：
1. 找出查詢相關的所有社群
2. 將所有社群摘要送入 LLM
3. 生成回答
   └── 問題：不相關的社群浪費 tokens 和計算資源

GraphRAG 2.0 查詢：
1. 從圖譜根節點開始
2. LLM 評估每個社群報告的相關性
   ├── 不相關 → 剪除該社群及其子節點
   └── 相關 → 深入子節點重複評估
3. 僅將相關社群摘要傳入 map-reduce
   └── 效益：token 成本降低 77%
```

## 實戰：使用 GraphRAG 建立知識庫

```python
import graphrag

config = graphrag.Config(
    llm=graphrag.LLMConfig(model="claude-fable-5", max_tokens=4000),
    embeddings=graphrag.EmbeddingConfig(model="text-embedding-3-large"),
)

indexer = graphrag.Indexer(config)
indexer.run(documents=["./docs/*.md"], output_dir="./graphrag_index")

query_engine = graphrag.GlobalSearch(index_dir="./graphrag_index", config=config)
result = query_engine.search("公司在量子計算領域的研發策略是怎麼演變的？")
print(result.response)
```

## GraphRAG 的查詢模式

GraphRAG 提供四種查詢模式，因應不同的問題類型：

```
查詢模式比較
─────────────────

Global Search（全局搜索）
├── 適用：需要綜合多份文件的主題性問題
├── 使用：社群摘要 + map-reduce
├── 範例：「公司的整體技術策略是什麼？」
└── 特點：GraphRAG 2.0 動態社群選擇節省 77% 成本

Local Search（局部搜索）
├── 適用：針對特定實體的深度問題
├── 使用：實體鄰居展開 + 相關文字片段
├── 範例：「Explain Transformer 的注意力機制如何運作？」
└── 特點：結合圖譜結構與原始文字

DRIFT Search（導航搜索）
├── 適用：特定實體 + 社群脈絡
├── 使用：Local Search + 社群資訊
├── 範例：「Transformer 的注意力機制如何影響了 BERT 的設計？」
└── 特點：在局部和全局之間取得平衡

Basic Search（基礎搜索）
├── 適用：簡單的事實性問題
├── 使用：傳統 top-k 向量搜索
├── 範例：「PostgreSQL 是哪一年發布的？」
└── 特點：直接使用向量索引，與傳統 RAG 相同
```

## 向量資料庫支援圖譜搜尋

2026 年，主要的向量資料庫廠商紛紛加入圖譜支援：

| 資料庫 | 原生圖譜支援 | 圖譜演算法 | 與向量搜尋整合 |
|-------|------------|-----------|--------------|
| Neo4j + Vector | 原生圖資料庫 | PageRank, Louvain, GDS | 向量作為節點屬性 |
| Qdrant 2.0 | 圖譜過濾 | 自訂圖遍歷 | 向量 + 圖篩選聯合查詢 |
| Weaviate 2.0 | 內建 GraphRAG | HNSW + 圖遍歷 | 一鍵 GraphRAG 模式 |
| PostgreSQL pgvector | 透過擴充套件 | 需自訂 | SQL 遞迴 CTE + 向量 |
| Microsoft GraphRAG | 索引層圖譜 | Leiden 聚類 | 查詢時圖譜導航 |

### Qdrant 2.0 的圖譜過濾範例

```python
from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)

# 在向量搜尋中加入圖譜過濾
results = client.query(
    collection_name="documents",
    query_vector=[0.12, -0.45, ..., 0.33],
    limit=10,
    # 圖譜過濾：只搜尋屬於「深度學習」社群的節點
    graph_filter={
        "community": "deep_learning",
        "depth": 2,
        "relationship": ["extends", "implements"]
    }
)
```

### Weaviate 2.0 一鍵 GraphRAG

```python
import weaviate

client = weaviate.connect_to_local()

# Weaviate 2.0 內建 GraphRAG
client.graphrag.configure(
    auto_extract=True,       # 自動從文字提取實體
    build_communities=True,   # 自動建立社群
    llm_model="claude-fable-5"
)

# 查詢自動使用 GraphRAG
result = client.query.graphrag(
    "分析所有文件中提到的技術趨勢"
).do()
```

## 結語

GraphRAG 代表 RAG 技術從「平面向量搜索」到「結構化知識推理」的質變。它特別適合需要跨文件綜合理解、實體關係追蹤、層級主題分析的場景——這些正是傳統 RAG 最脆弱的地方。隨著 Microsoft GraphRAG 達到 3.1 版本（2026 年 5 月）以及向量資料庫廠商紛紛原生整合圖譜能力，GraphRAG 正從學術研究快速走向生產環境。如果你的 RAG 應用常遇到「遺漏關鍵脈絡」或「無法回答綜合性問題」的情況，GraphRAG 值得認真評估。

## 延伸閱讀

- [Microsoft GraphRAG GitHub](https://github.com/microsoft/graphrag)
- [GraphRAG 官方文件](https://microsoft.github.io/graphrag/)
- [圖譜 RAG 技術比較](https://www.google.com/search?q=GraphRAG+vs+traditional+RAG+comparison+2026)
- [向量資料庫圖譜支援](https://www.google.com/search?q=vector+database+graph+support+Qdrant+Weaviate+2026)
- [RAG 技術演進](https://www.google.com/search?q=RAG+evolution+2026+GraphRAG+Agentic+RAG)

---

*本文為 AI 程式人雜誌 2026 年 6 月號 AI 技術專題之一。*
