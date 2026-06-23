# RAG：檢索增強生成（2020-2026）

## RAG 架構設計模式

RAG（Retrieval-Augmented Generation）解決 LLM 的核心限制：知識靜止於訓練資料，無法獲取即時或私有資訊。

### 三代架構演進

**Naive RAG（2020-2022）**：最簡單的「檢索 → 讀取」流程

```
查詢 → 嵌入 → 向量檢索 → 拼接提示 → LLM 生成
```

缺點：只檢索一次、無查詢重寫、混雜不相關文檔。

**Advanced RAG（2023-2024）**：加入預處理和後處理

```
查詢 → 查詢重寫 → 混合檢索 → 重排序 → 壓縮 → LLM 生成
↑               ↑          ↑         ↑
HyDE/SRQ        BM25+     Cohere    LLMLingua
                向量        rerank   extract
```

**Modular RAG（2025-2026）**：可插拔模組的組裝架構

```
RAG 模組選單：
├── 查詢模組：查詢重寫、查詢分解、HyDE
├── 檢索模組：稀疏 (BM25)、稠密 (嵌入)、圖檢索
├── 路由模組：意圖分類、查詢路由
├── 後處理模組：重排序、過濾、壓縮
└── 生成模組：引用溯源、事實性校驗
```

## 向量資料庫選擇

| 資料庫 | 部署方式 | 索引演算法 | 適合場景 |
|--------|---------|-----------|---------|
| **Chroma** | 嵌入式/local | HNSW | 原型開發、小規模 |
| **Pinecone** | 雲端 SaaS | 專有 | 生產環境、不想維運 |
| **Weaviate** | 自託管/雲端 | HNSW | 需要混合檢索 |
| **Qdrant** | 自託管/雲端 | HNSW | 高效能、過濾豐富 |
| **Milvus** | 自託管/雲端 | IVF/HNSW | 大規模 (億級) |

## 分塊策略

分塊（Chunking）直接影響檢產品質。不同策略適用不同場景：

### Fixed Chunking（固定大小）

```python
def fixed_chunks(text, chunk_size=512, overlap=64):
    chunks = []
    for i in range(0, len(text) - chunk_size + 1, chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks
```

簡單但可能切斷句子或段落。

### Semantic Chunking（語義分塊）

使用嵌入相似度或 LLM 判斷斷點：

```python
def semantic_chunks(sentences, threshold=0.85):
    chunks = [sentences[0]]
    for s in sentences[1:]:
        sim = cosine_sim(embed(s), embed(chunks[-1]))
        if sim > threshold:
            chunks[-1] += " " + s
        else:
            chunks.append(s)
    return chunks
```

### Agentic Chunking（2025-2026）

使用 LLM 自主決定如何分割文檔，能理解文件結構：

```python
# 提示範例
SYSTEM_PROMPT = """
你是一個文件分割助手。分析以下文檔，
在語義完整的邊界插入 [CHUNK] 標記。
每個 chunks 應該是獨立的知識單元。
"""
```

## 嵌入模型與混合檢索

### 嵌入模型選擇（2026 年推薦）

| 模型 | 維度 | 最長輸入 | 檢索任務 |
|------|------|---------|---------|
| `text-embedding-3-large` | 3072 | 8191 | 通用最佳 |
| `BGE-M3` | 1024 | 8192 | 多語言、混合 |
| `E5-mistral-7b` | 4096 | 32768 | 密集檢索 |
| `gte-Qwen2-7b` | 3584 | 32768 | 長文檔 |

### 混合檢索（Hybrid Search）

結合關鍵詞（BM25）和語義（向量）檢索，取得最佳效果：

```python
def hybrid_search(query, alpha=0.5, top_k=10):
    # 稀疏檢索（詞彙匹配）
    bm25_scores = bm25.search(query)  # 精確匹配專有名詞
    # 稠密檢索（語義匹配）
    dense_scores = vector_db.search(embed(query))
    # 線性融合
    scores = alpha * normalize(bm25_scores) + \
             (1 - alpha) * normalize(dense_scores)
    return top_k_documents(scores)
```

2026 年的趨勢是使用 RRF（Reciprocal Rank Fusion）取代線性融合，無需調整 α 超參數。

---

## 延伸閱讀

- [Retrieval-Augmented Generation 原始論文](https://www.google.com/search?q=Retrieval-Augmented+Generation+for+Knowledge-Intensive+NLP+tasks)
- [向量資料庫比較](https://www.google.com/search?q=vector+database+comparison+Chroma+Pinecone+Weaviate+Qdrant+Milvus)
- [RAG 分塊策略](https://www.google.com/search?q=RAG+chunking+strategies+fixed+semantic+agentic)
- [BGE 嵌入模型](https://www.google.com/search?q=BGE+embedding+model+BAAI)

---

*AI 程式人雜誌 2026 年 7 月號 — 大型語言模型實戰*
