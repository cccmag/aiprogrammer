# 專題 2：MongoDB 文件資料庫

## 靈活的文件資料庫解決方案

MongoDB 是最受歡迎的文件導向 NoSQL 資料庫之一，以其靈活的資料模型、強大的查詢語言和水平擴展能力聞名。

### 核心特性

#### 文件模型
MongoDB 將資料儲存為 BSON（二進位 JSON）文件，支援巢狀結構與陣列。這種設計讓開發者可以以更自然的方式表達複雜的資料關係。

```javascript
// MongoDB 文件範例
const user = {
  _id: ObjectId('664f1a2b3c4d5e6f7a8b9c0d'),
  name: 'Alice Chen',
  email: 'alice@example.com',
  profile: {
    age: 28,
    location: 'Taipei',
    interests: ['programming', 'AI', 'music']
  },
  createdAt: new Date()
}
```

#### 查詢語言
MongoDB 提供豐富的查詢運算子，支援範圍查詢、正則表達式、地理空間查詢與聚合管線。

```javascript
// MongoDB 查詢範例
db.users.find({
  'profile.location': 'Taipei',
  'profile.interests': 'AI',
  createdAt: { $gte: new Date('2024-01-01') }
}).sort({ createdAt: -1 }).limit(10)
```

#### 索引策略
適當的索引設計是 MongoDB 效能的關鍵。支援單一欄位索引、複合索引、文字索引與地理空間索引。

```javascript
// 建立複合索引
db.users.createIndex(
  { 'profile.location': 1, createdAt: -1 },
  { name: 'location_date_idx' }
)
```

### 使用場景

- **內容管理系統**：文章、評論等半結構化資料
- **即時分析**：搭配聚合管線進行即時資料分析
- **物聯網資料儲存**：感測器資料的時間序列儲存
- **使用者設定檔**：不同使用者可能有不同的設定檔結構

### 注意事項

1. **文件大小限制**：單一文件最大 16MB
2. **巢狀深度**：文件巢狀層級不宜過深（建議不超過 100 層）
3. **索引記憶體**：索引應能容納於記憶體中以維持效能
4. **JOIN 操作**：MongoDB 不支援傳統的 JOIN，需透過 $lookup 聚合或應用層處理

### 安全性最佳實踐

MongoDB 的安全性配置至關重要：
1. **啟用認證**：設定資料庫使用者與密碼
2. **網路隔離**：限制 IP 白名單，避免暴露於公開網路
3. **TLS/SSL 加密**：確保客戶端與伺服器之間的通訊加密
4. **稽核日誌**：啟用稽核功能記錄所有資料庫操作

### 部署與管理

MongoDB 提供複本集（Replica Set）以實現高可用性，以及分片叢集（Sharded Cluster）以實現水平擴展。可選擇自建或使用 MongoDB Atlas 雲端託管服務。Atlas 提供自動化備份、監控與擴展功能，大幅降低運維負擔。

延伸閱讀：https://www.google.com/search?q=MongoDB+document+database+tutorial
https://www.google.com/search?q=MongoDB+aggregation+pipeline+guide
