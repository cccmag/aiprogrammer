# 技術文章索引

本期共有十篇技術文章，涵蓋資料庫與雲端服務的各個面向，從基礎概念到進階實戰。

## 文章列表

### 1. 雲端資料庫 vs 本地資料庫
比較雲端託管資料庫與自建資料庫的優缺點，探討成本、效能、安全性與維護等面向。
[閱讀全文](article1.md)

### 2. MongoDB CRUD 操作
深入介紹 MongoDB 的新增、查詢、更新與刪除操作，搭配 Node.js 驅動程式的實際範例。
[閱讀全文](article2.md)

### 3. Mongoose ODM
介紹 Mongoose 這個 MongoDB ODM 函式庫，學習資料模型定義與驗證。
[閱讀全文](article3.md)

### 4. PostgreSQL 連線與查詢
從連線設定到 SQL 查詢，學習使用 PostgreSQL 進行資料操作。
[閱讀全文](article4.md)

### 5. Prisma ORM
介紹 Prisma ORM 的使用方法，從資料模型定義到關係查詢。
[閱讀全文](article5.md)

### 6. Redis 快取策略
探討常見的 Redis 快取策略，包括快取穿透、雪崩與失效處理。
[閱讀全文](article6.md)

### 7. AWS EC2 與 RDS
學習在 AWS 上部署 EC2 運算執行個體與 RDS 資料庫服務。
[閱讀全文](article7.md)

### 8. Firebase Firestore
介紹 Firebase Firestore 的文件資料庫，學習即時資料同步與查詢。
[閱讀全文](article8.md)

### 9. 資料庫備份策略
探討資料庫備份的最佳實踐，包括完整備份、增量備份與時間點恢復。
[閱讀全文](article9.md)

### 10. 雲端成本最佳化
學習如何分析與優化雲端服務成本，掌握 FinOps 的基本原則。
[閱讀全文](article10.md)

## 建議閱讀順序

- **初學者**：建議從文章 1 開始建立基礎概念，再依序閱讀 2、4、6、8，逐步熟悉各類型資料庫
- **中級開發者**：可直接閱讀 3、5、7，學習 ORM 與雲端服務的使用
- **進階開發者**：建議閱讀 9 與 10，深入了解備份策略與成本管理

### 技術涵蓋範圍

本期文章涵蓋以下技術與工具：

- **資料庫系統**：MongoDB、PostgreSQL、Redis、Firebase Firestore
- **驅動程式與 ORM**：MongoDB Node.js Driver、Mongoose、pg、Prisma
- **雲端平台**：AWS (EC2, RDS, S3, Lambda)、Firebase (Auth, Firestore, Cloud Functions, Storage)
- **工具與方法**：pg_dump、mongodump、AWS CLI、FinOps、備份策略

### 實作練習建議

1. 安裝 MongoDB 與 PostgreSQL 在本機環境
2. 註冊 AWS Free Tier 帳號進行雲端實作
3. 使用 `_code/db_cloud.js` 作為起點，擴充更多功能
4. 嘗試將模擬的 MongoDB 替換為真實資料庫連線

### 學習路徑圖

建議按照以下路徑逐步學習：
1. 先讀文章 1 建立雲端與本地資料庫的基礎概念
2. 依序學習 MongoDB (文章 2-3) 與 PostgreSQL (文章 4-5)
3. 掌握 Redis 快取策略 (文章 6)
4. 進入雲端實作：AWS (文章 7) 與 Firebase (文章 8)
5. 最後學習備份策略 (文章 9) 與成本管理 (文章 10)

每篇文章皆附有程式碼範例與參考資源，歡迎讀者親手實作。如果有任何問題或建議，歡迎至 GitHub 專案頁面發起討論！
