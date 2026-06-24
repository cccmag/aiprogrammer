# MongoDB 3.0 效能調校實戰

## 前言

MongoDB 3.0 引入的 WiredTiger 儲存引擎為效能帶來了質的飛躍，但這不意味著我們可以忽視效能調校。正確的配置和優化可以讓 MongoDB 的效能進一步提升，本文將分享實際可行的調校策略。

## 硬體與作業系統優化

### 儲存配置

WiredTiger 的效能高度依賴儲存子系統。固態硬碟（SSD）是首選，特別是對於寫入密集型工作負載。如果使用傳統硬碟，建議使用 RAID 10 配置。

```bash
# 監控磁碟 I/O
iostat -x 1

# 檢查檔案系統建議
# XFS 是 MongoDB 推薦的檔案系統
mkfs.xfs -f /dev/sdb1
```

### 記憶體配置

WiredTiger 預設使用一半的可用記憶體作為緩衝區。確保機器的記憶體足夠，並且不要讓其他程序佔用過多記憶體。

```javascript
// 檢視目前記憶體使用
db.serverStatus().tcmalloc

// 設定 WiredTiger 緩衝區大小（在 mongod.conf 中）
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 64
```

## 索引優化

### 複合索引設計

正確的索引設計是查詢效能的關鍵：

```javascript
// 為經常查詢的欄位組合建立複合索引
db.orders.createIndex({ "customer_id": 1, "created_at": -1 })

// 覆蓋查詢：索引包含所有需要回傳的欄位
db.orders.createIndex(
    { "customer_id": 1, "created_at": -1 },
    { "name": "orders_covering_idx" }
)

// 查詢計劃分析
db.orders.find({ "customer_id": "C123" }).explain("executionStats")
```

### 索引類型選擇

MongoDB 支援多種索引類型，選擇合適的類型可以提升特定場景的效能：

```javascript
// 多鍵索引：用於陣列欄位
db.articles.createIndex({ "tags": 1 })

// 文字索引：用於全文搜尋
db.articles.createIndex({ "content": "text" })

// 地理位置索引：用於空間查詢
db.locations.createIndex({ "location": "2dsphere" })
```

## 查詢優化

### 避免全集合掃描

使用 `hint()` 強制使用特定索引，或使用 `explain()` 分析查詢計劃：

```javascript
// 分析查詢計劃
db.orders.find({ "status": "pending" }).explain("allPlansExecution")

// 強制使用索引
db.orders.find({ "customer_id": "C123" }).hint({ "customer_id": 1 })
```

### 使用投影減少傳輸量

只回傳需要的欄位：

```javascript
// 只回傳 title 和 author，不回傳 content
db.articles.find(
    { "category": "tech" },
    { "title": 1, "author": 1, "_id": 0 }
)
```

## 寫入優化

### 批次寫入

使用 bulk write 操作減少網路往返：

```python
from pymongo import MongoClient, BulkWriteOperation

client = MongoClient()
collection = client['mydb']['orders']

operations = []
for i in range(1000):
    operations.append({
        'insertOne': {
            {'order_id': f'ORD{i}', 'amount': i * 10}
        }
    })

result = collection.bulk_write(operations)
print(f"插入: {result.inserted_count}, 耗時: {result.bulk_api_result}")
```

### Write Concern 調整

根據資料重要性調整寫入確認級別：

```python
# 快速寫入（ fire and forget ）
collection.insert_one(doc, write_concern={'w': 0})

# 預設確認
collection.insert_one(doc, write_concern={'w': 1})

# 多數確認（強一致性）
collection.insert_one(doc, write_concern={'w': 'majority'})
```

## 監控與診斷

### 使用プロファイル

開啟慢查詢日誌：

```javascript
// 設定慢查詢閾值為 100 毫秒
db.setProfilingLevel(1, { slowms: 100 })

// 查詢最近的慢查詢
db.system.profile.find().sort({ millis: -1 }).limit(10)
```

### MMS 監控

MongoDB Cloud Manager（或社群版 Ops Manager）提供即時監控儀表板。

## 結論

MongoDB 3.0 的效能調校需要綜合考慮硬體、配置、索引設計和監控等多個面向。建議從基礎做起，逐步優化，並且在修改任何配置之前先在測試環境驗證。