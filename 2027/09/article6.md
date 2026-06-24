# 分散式向量資料庫架構

## 1. 為什麼需要分散式架構？

當向量資料從百萬成長到億級別時，單機記憶體和計算能力都成為瓶頸。一個 768 維的向量佔用約 3KB 記憶體，1 億條向量在記憶體中就需要 300GB——這還不包括索引結構的額外開銷。分散式架構是應對這種規模的唯一選擇。

## 2. 分散式向量資料庫核心元件

### 2.1 資料分片（Sharding）

向量資料的分片策略與傳統資料庫有所不同，因為向量之間沒有自然的範圍劃分：

```python
import hashlib

class ShardManager:
    def __init__(self, num_shards=8):
        self.num_shards = num_shards
        self.shards = [Shard(i) for i in range(num_shards)]

    def assign_shard(self, doc_id):
        hash_val = int(hashlib.md5(
            doc_id.encode()).hexdigest(), 16)
        return hash_val % self.num_shards

    def add_document(self, doc):
        shard_id = self.assign_shard(doc.id)
        self.shards[shard_id].add(doc)

    def search(self, query_vec, top_k=10, nprobe=3):
        results = []
        for shard in self.shards:
            results.extend(shard.search(query_vec, top_k))
        results.sort(key=lambda x: -x.score)
        return results[:top_k]
```

常見分片策略：
- **Hash 分片**：根據文件 ID 或叢集 ID 分配，簡單但可能造成資料傾斜
- **叢集分片**：先對向量做 K-means，按叢集分配，搜尋時只查詢相關分片
- **虛擬節點**：使用一致性 Hash 減少重新分片時的資料遷移量

### 2.2 複製（Replication）

為了高可用性，每個分片應有 2-3 個副本：

```python
class ReplicatedShard:
    def __init__(self, shard_id, replication_factor=3):
        self.primary = Shard(shard_id)
        self.replicas = [Shard(shard_id)
                        for _ in range(replication_factor - 1)]

    def write(self, doc):
        self.primary.add(doc)
        for replica in self.replicas:
            replica.add(doc)  # 非同步複製

    def read(self, consistency="eventual"):
        if consistency == "strong":
            for replica in self.replicas:
                if not replica.is_synced():
                    return self.primary.search(...)
        return random.choice(self.replicas).search(...)
```

### 2.3 分散式索引

在分散式環境中，每個節點維護局部索引，協調節點負責合併結果。Pinecone 使用「叢集感知」的索引策略：

```
協調節點 ─┬─ 分片 0（IVF 索引，nlist=100）
           ├─ 分片 1（IVF 索引，nlist=100）
           ├─ 分片 2（IVF 索引，nlist=100）
           └─ 分片 3（IVF 索引，nlist=100）
```

## 3. 主流分散式向量資料庫架構

### 3.1 Pinecone（專有雲端服務）

Pinecone 是託管服務，使用者無需管理基礎設施。內部使用基於 HNSW 的分布式索引，支援自動縮放。Pod-based 架構，每個 Pod 包含 CPU/GPU 資源。

### 3.2 Milvus（雲端原生開源）

Milvus 使用「儲存計算分離」架構：

```
SDK → 負載平衡器 → Proxy → Query Node → 物件儲存（MinIO/S3）
                      ↓
                  Meta Store（etcd）
```

- **Proxy**：接收請求，路由到 Query Node
- **Query Node**：實際執行向量搜尋
- **Index Node**：負責建構索引
- **Data Node**：處理資料寫入與持久化
- **Object Storage**：S3/MinIO 儲存向量資料與索引檔案

### 3.3 Qdrant（Rust 實作）

Qdrant 採用基於 RAFT 共識協議的分散式設計：

```python
# Qdrant 分散式部署範例
from qdrant_client import QdrantClient

client = QdrantClient(
    url="https://cluster-1.qdrant.io",
    api_key="your-key",
    prefer_grpc=True  # 分散式環境建議使用 gRPC
)

# 建立分散式集合
client.create_collection(
    collection_name="my_collection",
    shard_number=6,
    replication_factor=2,
    vectors_config={"size": 768, "distance": "Cosine"}
)
```

## 4. 分散式查詢流程

```
1. 客戶端發送查詢向量
2. 協調節點接收請求
3. 協調節點將查詢廣播到所有分片
4. 每個分片執行局部 ANN 搜尋
5. 各分片返回局部 Top-K 結果
6. 協調節點進行合併與重新排序
7. 返回最終結果給客戶端
```

## 5. 一致性與可用性權衡

分散式向量資料庫需要在 CAP 定理的框架下進行取捨：

| 系統 | 一致性模型 | 可用性 | 分區容忍性 |
|------|-----------|-------|-----------|
| Milvus | 最終一致性 | 高 | 是 |
| Qdrant | 可調一致性 | 高 | 是 |
| Weaviate | 強一致性（RAFT） | 中 | 是 |

## 6. 效能調校

- **分片數量**：建議分片數 = 節點數 × 2，便於重新平衡
- **批量寫入**：使用批次 API 而非逐條寫入
- **索引建構時機**：在離線或低峰時段建構索引
- **GPU 加速**：使用 GPU 節點處理大規模搜尋

## 參考資料

- [Milvus 分散式架構](https://www.google.com/search?q=Milvus+distributed+architecture)
- [Qdrant 分散式部署](https://www.google.com/search?q=Qdrant+distributed+deployment)
- [Pinecone 架構](https://www.google.com/search?q=Pinecone+architecture+pod+based)
