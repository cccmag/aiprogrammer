# 主題五：CouchDB 與其他文件資料庫

## CouchDB 概述

Apache CouchDB 是一個開源的文件資料庫，以其獨特的離線優先架構和強大的 Replication 功能聞名。與其他文件資料庫不同，CouchDB 從設計之初就將分散式和離線使用場景作為核心目標。

CouchDB 的名字來自於「couch」，象徵其作為數據「舒適港灣」的定位。

## 核心架構

### RESTful API

CouchDB 採用純 HTTP RESTful API 作為介面，這使其可以被任何支持 HTTP 的用戶端訪問。這種設計簡化了整合，也方便了除錯。

```bash
# CouchDB API 範例
# 創建資料庫
curl -X PUT http://localhost:5984/mydb

# 插入文件
curl -X PUT http://localhost:5984/mydb/doc1 \
    -H "Content-Type: application/json" \
    -d '{"title": "Hello", "content": "World"}'

# 查詢文件
curl http://localhost:5984/mydb/doc1

# 刪除文件
curl -X DELETE http://localhost:5984/mydb/doc1?rev=1-xxx
```

### 雙向 Replication

CouchDB 最強大的功能之一是支援雙向 Replication。資料庫可以與其他 CouchDB 實例同步，支援：
- 單對單同步
- 一對多同步（主動複製）
- 多對多同步

這種 Replication 是增量且衝突可處理的，非常適合離線應用和分散式部署。

## 離線優先設計

CouchDB 的離線優先（Offline-First）架構是其最大特點：

### 衝突處理機制

當多個離線的資料庫實例重新連接時，可能產生衝突。CouchDB 採用版本樹（Revision Tree）來追蹤文件的變更歷史：

```python
# CouchDB 衝突處理範例（使用 python-couchdb）
import couchdb

server = couchdb.Server('http://localhost:5984')
db = server['mydb']

# 假設有衝突的文件
doc = db['doc_id']

# 取得衝突的所有版本
conflicts = doc.get('_conflicts', [])

# 解決衝突：刪除衝突版本或合併內容
for conflict_rev in conflicts:
    conflict_doc = db.get('doc_id', rev=conflict_rev)
    # 合併邏輯
    del db[conflict_rev]  # 刪除衝突版本
```

### 變更追蹤

CouchDB 的 `_changes` 端點提供了即時的資料變更通知，可以用來驅動下游的處理流程：

```json
{
    "results": [
        {"seq": 1, "id": "doc1", "changes": [{"rev": "1-abc"}]},
        {"seq": 2, "id": "doc2", "changes": [{"rev": "1-def"}]}
    ],
    "last_seq": 2
}
```

## CouchDB 的應用場景

### 適合的場景

- **邊緣運算**：物聯網設備需要在網路不穩定環境下運作
- **行動應用**：需要支援離線資料修改，然後同步
- **多站點部署**：跨地理區域的資料同步
- **內容管理**：發布/訂閱模式

### 不適合的場景

- 需要複雜的關聯查詢
- 需要嚴格事務支援
- 超大規模單一資料庫

## Elasticsearch 簡介

Elasticsearch 是另一個重要的文件資料庫，更強調搜尋和分析能力：

### 特點

- 基於 Apache Lucene 的全文搜尋引擎
- 支援複雜的聚合分析
- 原生 JSON 查詢 DSL
- 通常與 Logstash、Kibana 一起使用（ELK 堆疊）

### 與 CouchDB 的比較

| 特性 | CouchDB | Elasticsearch |
|------|---------|--------------|
| 主要用途 | 儲存與同步 | 搜尋與分析 |
| 查詢能力 | MapReduce 視圖 | 強大全文搜尋 |
| 即時性 | 依賴 Replication | 接近即時 |
| 叢集支援 | 原生 Replication | 原生分散式 |

## RethinkDB 簡介

RethinkDB 是另一個值得關注的文件資料庫，其最大的特色是即時推送（Realtime Push）功能。

###  Changefeeds

RethinkDB 的 Changefeeds 功能允許用戶訂閱資料庫變更：

```python
# RethinkDB changefeed 範例
import rethinkdb as r

r.connect().run_query(
    r.db('test').table('players')
    .changes()
    .run()
)

# 當有任何變更時，立即收到通知
```

### 與 CouchDB 的比較

| 特性 | CouchDB | RethinkDB |
|------|---------|-----------|
| 即時推送 | 透過 Replication | 原生 Changefeeds |
| 查詢語言 | JavaScript/MapReduce | ReQL |
| 架構重點 | 離線優先 | 即時應用 |
| 叢集 | CouchDB Server | 原生分散式 |

## 選擇指南

選擇文件資料庫時，應考慮：

1. **離線需求**：是否需要支援離線編輯和同步？
2. **查詢複雜度**：需要多複雜的查詢能力？
3. **即時性要求**：需要多快的變更通知？
4. **擴展性需求**：預期的資料規模和流量？

CouchDB 適合離線優先和跨地域同步的需求；Elasticsearch 適合需要強大搜尋能力的場景；RethinkDB 則適合需要即時資料推送的應用。