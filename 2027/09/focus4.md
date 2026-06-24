# 向量資料庫架構（2019-2026）

## 從向量索引到完整資料庫系統

### 儲存引擎設計

向量資料庫的儲存引擎需要同時管理兩種資料：**向量資料**（高維浮點陣列）和**結構化中繼資料**（JSON、數值、字串）。常見的架構方式有三種：

```python
# 混合儲存架構示意
class StorageEngine:
    def __init__(self):
        self.vector_store = VectorStore()
        self.metadata_store = MetadataStore()

    def search(self, query_vector, filters=None, k=10):
        ids = self.metadata_store.filter(filters) if filters else None
        results = self.vector_store.search(query_vector, k=k, allowed_ids=ids)
        for r in results:
            r.metadata = self.metadata_store.get(r.id)
        return results
```

### 過濾與混合搜尋

混合搜尋是向量資料庫最具挑戰性的部分——如何在高維向量搜尋中同時支援結構化過濾？三種主流策略：

| 策略 | 流程 | 優點 | 缺點 |
|------|------|------|------|
| Pre-filter | 先過濾再向量搜尋 | 過濾精確 | 過濾後可能無候選 |
| Post-filter | 先搜尋再過濾 | 方便實作 | 可能回傳不足 k 個 |
| Hybrid | 同時過濾與向量搜尋 | 最佳品質 | 實作複雜 |

```python
# Hybrid 搜尋示意
def hybrid_search(query_emb, filters, alpha=0.5):
    """同時考慮向量相似度與過濾條件的混合搜尋"""
    vec_score = vector_index.search(query_emb)
    filter_score = metadata_index.search(filters)
    # 加權合併
    combined = alpha * vec_score + (1 - alpha) * filter_score
    return combined.top_k(10)
```

### 分散式架構

2026 年向量資料庫的分散式架構已成熟，核心挑戰是：

1. **資料分片**：按向量空間劃分（如 IVF 的分區機制），或按 hash 分片
2. **複製策略**：多副本保證可用性，但新增向量時需同步更新所有副本的 HNSW 圖
3. **一致性模型**：最終一致性為主，因 ANN 搜尋本就允許誤差

```python
# 分散式查詢示意
class DistributedVectorDB:
    def __init__(self, shards):
        self.shards = shards  # 多個分片
    
    def search(self, query, k=10):
        # 向所有分片發送查詢
        partial_results = []
        for shard in self.shards:
            partial = shard.search(query, k=k)
            partial_results.extend(partial)
        # 合併排序
        return sorted(partial_results, key=lambda x: -x.score)[:k]
```

### 2026 的主流實作

各資料庫的底層核心：

- **Pinecone**：專有引擎，基於分層 HNSW + SSD 快取
- **Weaviate**：自訂儲存 + 物件關聯圖
- **Qdrant**：Rust 實作，Arc-Welded 向量索引
- **Chroma**：Embeddings 優先，簡化部署
- **pgvector**：PostgreSQL 擴展，利用其 indexing framework

### 未來方向

2026 年向量資料庫的架構演進方向是**儲存-計算分離**，讓向量索引和儲存各自獨立擴展，以及**機密計算**——在加密資料上直接進行向量搜尋。

---

**下一步**：[AI 驅動的資料管理](focus5.md)

## 延伸閱讀

- [混合搜尋架構比較](https://www.google.com/search?q=hybrid+search+vector+database+architecture)
- [向量資料庫分散式設計](https://www.google.com/search?q=distributed+vector+database+design)
