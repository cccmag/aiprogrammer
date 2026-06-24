# 程式碼說明：資料庫與雲端服務範例

本期範例程式碼位於 `_code/db_cloud.js`，以 Node.js 實作了一個資料庫與雲端服務的模擬環境。程式碼示範了 MongoDB、Redis 和 Firebase 三種資料服務的核心操作。

## 程式結構

### MongoCollection 類別

模擬 MongoDB 文件資料庫的集合操作，使用記憶體陣列儲存文件。實作了四種 CRUD 方法：

- `insertOne(doc)`：插入單一文件，自動產生 `_id`
- `find(query)`：查詢文件，支援條件過濾
- `updateOne(query, update)`：更新符合條件的文件
- `deleteOne(query)`：刪除符合條件的文件

### RedisCache 類別

模擬 Redis 的鍵值儲存功能，底層使用 Map 實作：

- `get(key)`：讀取快取資料
- `set(key, value, ttl)`：寫入快取，支援過期時間
- `del(key)`：刪除快取鍵
- `flush()`：清除所有快取

### FirebaseStore 類別

模擬 Firebase Firestore 的集合與文件操作：

- `collection(name)`：取得或建立集合，回傳 MongoCollection 實例

### demo() 函數

執行完整的示範流程，依序進行 MongoDB CRUD 操作、Redis 快取讀寫、Firebase 文件儲存查詢，最後輸出執行結果。

```javascript
function demo() {
  // MongoDB 操作
  const db = new MongoCollection()
  db.insertOne({ user: 'Alice', score: 85 })
  db.find()
  db.updateOne({ user: 'Alice' }, { $set: { score: 90 } })
  db.deleteOne({ user: 'Bob' })

  // Redis 快取操作
  const cache = new RedisCache()
  cache.set('session:alice', { name: 'Alice', role: 'admin' }, 60000)
  cache.get('session:alice')
  cache.del('session:alice')

  // Firebase 操作
  const fb = new FirebaseStore()
  fb.collection('notes').insertOne({ title: '學習筆記', body: 'Firebase 即時資料庫' })
  fb.collection('notes').find()
}
```

## 執行方式

```bash
cd _code
bash test.sh
```

或直接執行：

```bash
node db_cloud.js
```

### 擴充練習建議

1. **新增排序功能**：為 MongoCollection 的 find 方法加入排序參數
2. **實作 TTL 精確過期**：改進 RedisCache 的 TTL 機制，支援精確的秒級過期
3. **加入查詢快取**：使用 RedisCache 為 MongoCollection 的查詢結果加上快取層
4. **實作即時監聽**：模擬 Firestore 的 onSnapshot 行為，支援變更事件回呼

## 學習重點

1. 理解資料庫 CRUD 操作的共通模式
2. 觀察快取層如何加速資料讀取
3. 比較文件資料庫與鍵值儲存的差異
4. 學習模擬外部服務的測試技巧

此範例適合初學者快速掌握資料庫操作的核心概念，並為後續學習真實資料庫服務打下基礎。
