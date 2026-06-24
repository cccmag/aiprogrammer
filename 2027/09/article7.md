# 向量資料庫的 CRUD 操作

## 1. 向量資料庫的資料模型

向量資料庫的資料模型與傳統關係型資料庫有顯著差異。每筆記錄通常包含三個核心部分：

```python
class VectorRecord:
    def __init__(self, id, vector, payload=None):
        self.id = id           # 唯一識別符
        self.vector = vector   # 浮點數陣列（向量嵌入）
        self.payload = payload # 元資料（JSON-like 結構）
        self.tenant_id = None  # 多租戶支援
```

## 2. Create：建立與插入

Python 中使用 Qdrant 客戶端的範例：

```python
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

client = QdrantClient("localhost", port=6333)

# 建立集合（類似 SQL 的 CREATE TABLE）
client.create_collection(
    collection_name="articles",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
)

# 插入單筆資料
client.upsert(
    collection_name="articles",
    points=[
        PointStruct(
            id=1,
            vector=[0.1, 0.2, ...],  # 768 維
            payload={
                "title": "AI 原生資料庫",
                "author": "ccckmit",
                "tags": ["AI", "database"],
                "created_at": "2026-09-01",
                "views": 1234
            }
        )
    ]
)

# 批量插入（效能遠優於逐筆插入）
batch = [
    PointStruct(id=i, vector=vecs[i], payload=payloads[i])
    for i in range(1000)
]
client.upsert(collection_name="articles", points=batch)
```

## 3. Read：讀取與查詢

向量資料庫支援兩種讀取模式：**點查詢**（根據 ID 取得記錄）和**向量查詢**（根據相似度搜尋）。

```python
# 點查詢：根據 ID 取得記錄
result = client.retrieve(
    collection_name="articles",
    ids=[1, 2, 3]
)

# 向量查詢：相似度搜尋
results = client.search(
    collection_name="articles",
    query_vector=query_vec,
    limit=10,
    score_threshold=0.75,  # 只返回分數 > 0.75 的結果
    with_payload=True,     # 同時返回元資料
)

# 過濾查詢：結合結構化條件
from qdrant_client.models import Filter, FieldCondition, Range

results = client.search(
    collection_name="articles",
    query_vector=query_vec,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="tags",
                match={"value": "AI"}
            ),
            FieldCondition(
                key="views",
                range=Range(gte=100)
            )
        ]
    ),
    limit=10
)
```

## 4. Update：更新向量與元資料

向量資料庫的更新操作需要特別注意：**更新向量意味著可能需要重建索引**。

```python
# 只更新元資料（不需要重建索引）
client.set_payload(
    collection_name="articles",
    payload={"views": 5678, "updated_at": "2026-10-01"},
    points=[1],
)

# 更新向量（需要重建索引或增量更新）
client.upsert(
    collection_name="articles",
    points=[
        PointStruct(
            id=1,
            vector=[0.3, 0.4, ...],  # 新的嵌入向量
            payload={"title": "AI 原生資料庫（更新版）"}
        )
    ]
)

# 刪除特定欄位
client.delete_payload(
    collection_name="articles",
    keys=["temporary_field"],
    points=[1],
)
```

## 5. Delete：刪除操作

```python
# 根據 ID 刪除
client.delete(
    collection_name="articles",
    points_selector=[1, 2, 3]
)

# 根據過濾條件刪除
from qdrant_client.models import Filter, FieldCondition

client.delete(
    collection_name="articles",
    points_selector=Filter(
        must=[
            FieldCondition(
                key="created_at",
                range=Range(lt="2026-01-01")
            )
        ]
    )
)

# 刪除整個集合
client.delete_collection(collection_name="articles")
```

## 6. 索引管理

向量資料庫的索引管理是 CRUD 中最容易被忽略但影響最大的部分：

```python
# 建立索引參數
from qdrant_client.models import HnswConfigDiff

client.create_collection(
    collection_name="large_articles",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    hnsw_config=HnswConfigDiff(
        m=16,              # 每個節點的連接數
        ef_construct=100,  # 建索引時的動態列表大小
        full_scan_threshold=10000,  # 低於此數量的節點使用暴力掃描
    ),
    optimizers_config={
        "indexing_threshold": 10000,  # 超過此數量自動建索引
    }
)

# 手動觸發索引最佳化
client.update_collection(
    collection_name="large_articles",
    optimizer_config={
        "deleted_threshold": 0.2,  # 刪除 20% 後自動最佳化
    }
)
```

## 7. 實戰注意事項

- **批次寫入大小**：建議 500-1000 條/批次，避免記憶體不足
- **Payload 索引**：常用於過濾的 Payload 欄位應建立索引
- **向量維度**：一旦建立集合即無法修改維度，需要規劃好
- **ID 唯一性**：確保 ID 在全域唯一，UUID 是推薦方案
- **一致性層級**：高吞吐場景選擇 Eventual Consistency

## 8. CRUD 效能基準

| 操作 | 延遲（1000 條，768 維） | 說明 |
|------|----------------------|------|
| 批量插入 | 50-200ms | 取決於索引類型 |
| 點查詢 | 1-3ms | 根據 ID 檢索 |
| 向量搜尋 | 5-50ms | 取決於資料量和索引 |
| 更新元資料 | 5-20ms | 不涉及索引重建 |
| 更新向量 | 10-100ms | 可能需要部分索引重建 |
| 批量刪除 | 20-100ms | 軟刪除，硬刪除較慢 |

## 參考資料

- [Qdrant CRUD API](https://www.google.com/search?q=Qdrant+CRUD+API+documentation)
- [Pinecone 資料操作](https://www.google.com/search?q=Pinecone+upsert+update+delete)
- [向量資料庫資料模型設計](https://www.google.com/search?q=vector+database+data+model+design)
