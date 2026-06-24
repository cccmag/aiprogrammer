# 向量資料庫安全與多租戶隔離

## 1. 向量資料庫的安全挑戰

向量資料庫儲存的不只是數字——向量本身可能包含敏感資訊的語義特徵。研究顯示，透過逆向工程可以從嵌入向量部分還原原始文字。因此，向量資料庫的安全防護比傳統資料庫多了一層語義層面的考量。

## 2. 多租戶隔離策略

多租戶系統需要確保租戶 A 的資料不會被租戶 B 看到，同時維持向量搜尋的效能。

### 2.1 每租戶獨立集合

最簡單也最安全的策略——每個租戶使用獨立的集合（Collection）：

```python
from qdrant_client import QdrantClient

class MultiTenantManager:
    def __init__(self):
        self.client = QdrantClient("localhost", port=6333)

    def get_collection_name(self, tenant_id):
        return f"tenant_{tenant_id}_vectors"

    def create_tenant(self, tenant_id, vector_size=768):
        from qdrant_client.models import VectorParams, Distance
        name = self.get_collection_name(tenant_id)
        self.client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(
                size=vector_size, distance=Distance.COSINE
            ),
        )

    def search(self, tenant_id, query_vec, top_k=10):
        name = self.get_collection_name(tenant_id)
        return self.client.search(
            collection_name=name,
            query_vector=query_vec,
            limit=top_k,
        )
```

**優點**：資料完全隔離，索引獨立，租戶間不互相影響
**缺點**：管理成本高，資源利用率較低

### 2.2 共享集合 + Payload 過濾

所有租戶共用一個集合，透過 Payload 中的 `tenant_id` 欄位進行隔離：

```python
def add_document(self, tenant_id, doc):
    self.client.upsert(
        collection_name="shared_collection",
        points=[PointStruct(
            id=doc["id"],
            vector=doc["vector"],
            payload={"tenant_id": tenant_id, **doc["metadata"]}
        )]
    )

def search(self, tenant_id, query_vec, top_k=10):
    from qdrant_client.models import Filter, FieldCondition
    return self.client.search(
        collection_name="shared_collection",
        query_vector=query_vec,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="tenant_id",
                    match={"value": tenant_id}
                )
            ]
        ),
        limit=top_k,
    )
```

**優點**：資源利用率高，管理簡單，適合大量小型租戶
**缺點**：搜尋時仍需掃描過濾所有租戶資料，可能影響效能

### 2.3 Pre-filtering vs Post-filtering

過濾的時機對效能有重大影響：

- **Pre-filtering**：先過濾出符合條件的租戶資料，再進行向量搜尋
  - 過濾條件選擇性高時效果好
  - 需要 Payload 索引支援
  
- **Post-filtering**：先進行向量搜尋，再過濾租戶資料
  - 過濾條件選擇性低時效果好
  - 可能回傳不屬於該租戶的結果（安全性漏洞）

```python
# Pre-filtering（推薦）
def search_pre_filter(self, tenant_id, query_vec, k=10):
    from qdrant_client.models import Filter, FieldCondition
    return self.client.search(
        collection_name="shared",
        query_vector=query_vec,
        query_filter=Filter(
            must=[FieldCondition(key="tenant_id",
                                 match={"value": tenant_id})]
        ),
        limit=k,
        # 告訴系統先過濾再搜尋
        params={"exact": False, "hnsw_ef": 128}
    )
```

## 3. 資料加密

### 3.1 靜態加密

向量資料在儲存層應進行加密。但需要注意：加密後的向量無法直接進行相似度計算。解決方案有：

```python
import os
from cryptography.fernet import Fernet

class EncryptedVectorStore:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def _encrypt_vector(self, vector):
        import struct
        packed = struct.pack(f'{len(vector)}f', *vector)
        return self.cipher.encrypt(packed)

    def _decrypt_vector(self, encrypted):
        import struct
        packed = self.cipher.decrypt(encrypted)
        return list(struct.unpack(f'{len(packed)//4}f', packed))
```

### 3.2 傳輸加密（TLS）

所有向量資料庫客戶端應啟用 TLS：

```python
# Qdrant 啟用 TLS
client = QdrantClient(
    url="https://secure-instance.qdrant.io",
    api_key="your-key",
    https=True,
)

# Milvus 啟用 TLS
from pymilvus import connections
connections.connect(
    host="secure-milvus.example.com",
    port=19530,
    secure=True,
    server_name="milvus.example.com",
)
```

## 4. 訪問控制

向量資料庫的訪問控制應包含三個層級：

| 層級 | 控制對象 | 實作方式 |
|------|---------|---------|
| API 層 | 請求來源 | API Key + IP 白名單 |
| 集合層 | 資料庫操作 | RBAC 權限模型 |
| 記錄層 | 單筆資料 | Payload 過濾（Row-Level Security） |

### RBAC 實作範例

```python
class RBACController:
    def __init__(self):
        self.roles = {
            "admin": {"read", "write", "delete", "manage"},
            "editor": {"read", "write"},
            "viewer": {"read"},
        }
        self.user_roles = {}

    def check_permission(self, user_id, action, tenant_id):
        role = self.user_roles.get(user_id)
        if not role:
            return False
        actions = self.roles.get(role, set())
        return action in actions
```

## 5. 稽核與監控

```python
import logging
from datetime import datetime

audit_logger = logging.getLogger("vector_db_audit")

def audit_search(user_id, tenant_id, query_vector, results):
    audit_logger.info({
        "timestamp": datetime.utcnow().isoformat(),
        "action": "search",
        "user_id": user_id,
        "tenant_id": tenant_id,
        "query_hash": hash_vector(query_vector),
        "num_results": len(results),
    })
```

## 6. 安全性檢查清單

- [ ] 啟用 TLS/SSL 傳輸加密
- [ ] 實作多租戶資料隔離
- [ ] 設定 API Key 輪換策略（每 90 天）
- [ ] 限制向量搜尋回傳數量（上限 1000）
- [ ] 定期審計所有查詢記錄
- [ ] 向量逆向攻擊防護（對高頻查詢加入擾動）
- [ ] 刪除資料的徹底清除（而非軟刪除）
- [ ] Payload 敏感欄位的脫敏處理

## 參考資料

- [向量資料庫安全指南](https://www.google.com/search?q=vector+database+security+best+practices)
- [多租戶向量搜尋](https://www.google.com/search?q=multi+tenant+vector+database+isolation)
- [OWASP API 安全](https://www.google.com/search?q=OWASP+API+security+best+practices)
