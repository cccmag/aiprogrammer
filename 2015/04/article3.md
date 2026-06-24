# CouchDB 離線優先設計

## 離線優先的概念

離線優先（Offline-First）是一種軟體架構理念，強調應用程式在沒有網路連接的情況下也能正常運作。當網路恢復時，自動同步資料。這種設計特別適合：

- 行動應用
- 物聯網設備
- 偏遠地區的系統
- 需要高可用性的應用

CouchDB 是實現離線優先架構的理想資料庫選擇。

## CouchDB 的同步機制

### 雙向 Replication

CouchDB 的 Replication 功能讓資料庫之間可以雙向同步：

```bash
# 本機到遠端的單次同步
curl -X POST http://localhost:5984/_replicate \
    -H "Content-Type: application/json" \
    -d '{
        "source": "mydb",
        "target": "http://remote:5984/mydb"
    }'

# 連續同步（持續監聽變更）
curl -X POST http://localhost:5984/_replicate \
    -H "Content-Type: application/json" \
    -d '{
        "source": "mydb",
        "target": "http://remote:5984/mydb",
        "continuous": true
    }'
```

### 過濾式 Replication

只同步符合條件的文件：

```bash
# 定義過濾函數（在設計文件中）
# _design/filters
# {
#     "filters": {
#         "by_user": "function(doc, req) { return doc.user_id == req.query.user_id; }"
#     }
# }

# 使用過濾器同步
curl -X POST http://localhost:5984/_replicate \
    -H "Content-Type: application/json" \
    -d '{
        "source": "mydb",
        "target": "http://remote:5984/mydb",
        "filter": "filters/by_user",
        "query_params": {
            "user_id": "user123"
        }
    }'
```

## 版本衝突處理

### 修訂樹結構

CouchDB 使用修訂樹（Revision Tree）來追蹤文件的變更歷史：

```python
import couchdb

server = couchdb.Server('http://localhost:5984')
db = server['mydb']

# 文件的修訂歷史
doc = db['doc_id']
# _rev 格式：{版本号}-{雜湊}
# 例如：3-abc123, 2-def456, 1-ghi789
```

### 衝突偵測與解決

```python
def resolve_conflicts(db, doc_id):
    doc = db[doc_id]
    conflicts = db.get(doc_id, conflicts=True).get('_conflicts', [])

    if not conflicts:
        return

    print(f"發現 {len(conflicts)} 個衝突")

    for conflict_rev in conflicts:
        conflict_doc = db.get(doc_id, rev=conflict_rev)
        print(f"衝突版本：{conflict_rev}")
        print(f"內容：{conflict_doc}")

        # 策略一：刪除衝突版本（保留主版本）
        # 適用於主版本已經是正確的情況
        del db[doc_id, rev=conflict_rev]

        # 策略二：合併內容
        # 根據業務邏輯合併欄位
        # doc['count'] = max(doc.get('count', 0), conflict_doc.get('count', 0))
        # db.save(doc)

        # 策略三：使用時間戳決定保留版本
        # if conflict_doc.get('timestamp', '') > doc.get('timestamp', ''):
        #     db[doc_id] = conflict_doc
```

## 實際應用場景

### 行動應用範例

```python
# 假設是一個離線記事本應用
class OfflineNotesApp:
    def __init__(self, local_db, remote_url):
        self.local_db = local_db
        self.remote_url = remote_url

    def create_note(self, title, content):
        note = {
            '_id': f'note:{self._generate_id()}',
            'type': 'note',
            'title': title,
            'content': content,
            'created_at': self._get_timestamp(),
            'updated_at': self._get_timestamp(),
            'sync_status': 'pending'
        }
        self.local_db.save(note)
        return note

    def sync(self):
        """與遠端同步"""
        # 推送本地改動到遠端
        self._replicate(
            source=self.local_db.name,
            target=self.remote_url
        )
        # 從遠端拉取改動
        self._replicate(
            source=self.remote_url,
            target=self.local_db.name
        )

    def _replicate(self, source, target):
        # 實際使用 couchdb 的Replication API
        pass

    def get_conflicts(self, doc_id):
        """取得並解決衝突"""
        doc = self.local_db[doc_id]
        conflicts = self.local_db.get(doc_id, conflicts=True).get('_conflicts', [])

        for conflict_rev in conflicts:
            conflict_doc = self.local_db.get(doc_id, rev=conflict_rev)
            # 自動合併策略：保留較新的版本
            if conflict_doc['updated_at'] > doc['updated_at']:
                # 用衝突版本替換當前版本
                self.local_db[doc_id] = conflict_doc
            # 刪除衝突版本
            del self.local_db[doc_id, rev=conflict_rev]
```

### 物聯網應用

```python
# 感測器資料收集
class SensorDataCollector:
    def __init__(self, db):
        self.db = db

    def record_reading(self, sensor_id, temperature, humidity):
        reading = {
            '_id': f'sensor:{sensor_id}:{self._get_timestamp()}',
            'sensor_id': sensor_id,
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': self._get_timestamp()
        }
        self.db.save(reading)
        return reading

    def get_latest_readings(self, sensor_id, limit=10):
        """取得最新的讀數"""
        return list(self.db.view(
            '_design/sensors/_view/latest',
            startkey=[sensor_id, {}],
            descending=True,
            include_docs=True,
            limit=limit
        ))
```

## 設計考量

### 離線優先的優點

- **使用者體驗**：不受網路品質影響
- **效能**：本地讀取速度極快
- **可靠性**：網路中斷不會造成資料遺失
- **可擴展性**：減少伺服器負載

### 離線優先的挑戰

- **衝突處理**：需要謹慎的業務邏輯設計
- **存儲空間**：本地資料庫會持續增長
- **同步策略**：何時同步、同步頻率都需要規劃
- **安全性**：離線設備可能遺失或被竊

## 最佳實踐

1. **文件 ID 設計**：使用有意義的 ID 方便索引和查詢
2. **控制文件大小**：避免過度巢狀，影響網路傳輸
3. **定期清理**：使用 compaction 減少資料庫大小
4. **衝突監控**：定期檢查和處理衝突
5. **測試同步**：在各种網路條件下測試同步行為

CouchDB 的離線優先設計為現代應用提供了一種可靠、彈性的資料管理方式。