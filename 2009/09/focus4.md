# CouchDB 與事件溯源：離線優先的文件資料庫

## CouchDB 的起源

### Apache 專案

CouchDB 由 Apache Software Foundation 開發，2005 年由 Damien Katz 創建，2008 年成為 Apache 孵化專案。

```markdown
CouchDB 設計理念：

1. 離線優先
   - 完全支援離線操作
   - 自動同步

2. 文件導向
   - JSON 文件儲存
   - 無 Schema

3. 分散式
   - 多主複製
   - 衝突檢測和解決

4. 容錯
   - 最終一致性
   - 事件溯源
```

## CouchDB 的特色

### RESTful API

```bash
# CouchDB 使用 HTTP API

# 建立資料庫
curl -X PUT http://localhost:5984/mydb

# 新增文件
curl -X POST http://localhost:5984/mydb \
  -H "Content-Type: application/json" \
  -d '{"name": "張三", "age": 30}'

# 查詢文件
curl http://localhost:5984/mydb/doc_id

# 查詢所有文件
curl http://localhost:5984/mydb/_all_docs

# 刪除文件
curl -X DELETE http://localhost:5984/mydb/doc_id
```

### 視圖和 MapReduce

```javascript
// CouchDB 視圖使用 MapReduce

// 首先在設計文件中定義視圖
{
  "_id": "_design/users",
  "views": {
    "by_age": {
      "map": "function(doc) { if (doc.age) { emit(doc.age, doc.name); } }"
    },
    "count_by_age": {
      "map": "function(doc) { if (doc.age) { emit(doc.age, 1); } }",
      "reduce": "_count"
    }
  }
}

// 查詢視圖
# 取得所有年齡
curl http://localhost:5984/mydb/_design/users/_view/by_age

# 帶reduce的查詢
curl http://localhost:5984/mydb/_design/users/_view/count_by_age?group=true
```

### 複製和同步

```bash
# CouchDB 複製

# 單向複製
curl -X POST http://localhost:5984/_replicate \
  -H "Content-Type: application/json" \
  -d '{
    "source": "mydb",
    "target": "http://remote:5984/mydb"
  }'

# 連續複製（持續同步）
curl -X POST http://localhost:5984/_replicate \
  -H "Content-Type: application/json" \
  -d '{
    "source": "mydb",
    "target": "http://remote:5984/mydb",
    "continuous": true
  }'
```

## 事件溯源架構

### 事件溯源的概念

```python
# 事件溯源的原理

# 傳統：儲存當前狀態
{
    "user_id": 1,
    "name": "張三",
    "balance": 1000
}

# 事件溯源：儲存事件序列
[
    {"event": "create_account", "balance": 0},
    {"event": "deposit", "amount": 500, "balance": 500},
    {"event": "deposit", "amount": 500, "balance": 1000}
]

# 好處：
# - 完整的審計軌跡
# - 可以回溯到任意時間點
# - 可以重建任何狀態
```

### CouchDB 的事件儲存

```javascript
// CouchDB 作為事件儲存

// 事件文件
{
  "_id": "event:2009-09-01:001",
  "type": "event",
  "aggregate": "account",
  "aggregate_id": "acc-001",
  "event_type": "deposit",
  "timestamp": "2009-09-01T10:00:00Z",
  "data": {
    "amount": 500
  }
}

// 查詢帳戶的所有事件
db.view('events', 'by_aggregate', {
    key: "acc-001"
})
```

## 離線優先

### 這個概念

```markdown
離線優先的優勢：

1. 更好的使用者體驗
   - 不受網路影響
   - 即時回應

2. 減少伺服器負載
   - 本地處理
   - 批量同步

3. 更好的可擴展性
   - 離線也能工作
   - 連線時同步
```

### CouchDB 的離線支援

```python
# CouchDB 離線工作流程

# 1. 本地 CouchDB
# 應用程式連線到本地 CouchDB

# 2. 離線操作
# 所有操作寫入本地 CouchDB

# 3. 網路恢復
# CouchDB 自動同步到遠端

# 4. 衝突解決
# CouchDB 檢測衝突並提供選項
```

## CouchDB vs MongoDB

```markdown
| 特性       | CouchDB         | MongoDB         |
|-----------|-----------------|-----------------|
| API       | HTTP/REST       | 專有協定        |
| 語言       | Erlang          | C++             |
| 查詢       | MapReduce       | 動態查詢        |
| 複製       | 多主複製        | 主從複製        |
| 一致性     | 最終一致        | 可調整一致      |
| 離線支援   | 完整支援        | 基本支援        |
| 適用場景   | 離線應用、CDN   | Web 應用、高效能|
```

## 結語

CouchDB 代表了文件資料庫的另一條路線：離線優先和事件溯源。2009 年的 CouchDB 0.10 版本展示了這種設計的可行性。

下一篇文章將介紹 CAP 理論和分散式資料庫的一致性問題。

---

## 延伸閱讀

- [CouchDB 官方網站](https://www.google.com/search?q=Apache+CouchDB+official+website)
- [CouchDB 與離線應用](https://www.google.com/search?q=CouchDB+offline+first+2009)
- [事件溯源架構](https://www.google.com/search?q=event+sourcing+architecture)

---

*本篇文章為「AI 程式人雜誌 2009 年 9 月號」焦點系列之一。*