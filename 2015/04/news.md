# 本月新知

## 2015 年 4 月程式與技術動態

### 程式語言與框架

**Python 3.5 接近完成**

Python 3.5 於 2015 年 4 月達到功能凍結階段，預計於 9 月正式發布。本月看到社區持續討論 PEP 492 引入的 `async`/`await` 語法，這將大幅簡化非同步程式設計。type hints (PEP 484) 的引入也備受關注，為靜態類型檢查鋪路。

**JavaScript ES6 全面普及**

ECMAScript 6 將於 2015 年 6 月正式發布，各瀏覽器加速實現新特性。Node.js 0.12 版本持續最佳化 V8 引擎效能。Flow 和 TypeScript 的採用率上升，靜態類型在 JavaScript 生態中獲得越來越多關注。

**Go 1.5 開發中**

Go 語言持續發展，1.5 版本預計引入重大的建置系統改進。goroutine 的调度器和並發模型的優化是社群討論的焦點。

### NoSQL 與資料庫

**Redis 3.0 正式發布**

2015 年 4 月，Redis 3.0 正式發布，最大亮點是原生支援 Redis Cluster。這個分散式解決方案提供自動分片和失敗轉移能力，讓 Redis 能夠水平擴展到數百個節點。Redis Cluster 使用 16384 個雜湊槽進行資料分發，大幅簡化分散式部署的複雜度。

**MongoDB 3.0 帶來儲存引擎革命**

MongoDB 3.0 於 2015 年 3 月發布，4 月開始被廣泛採用。WiredTiger 儲存引擎是最大亮點，提供文件級並發控制和壓縮支援。根據官方測試，WiredTiger 可將寫入效能提升 7-10 倍，儲存空間節省 50-80%。MMAPv1 引擎仍然保留作為預設選項。

**CouchDB 1.7 持續改進**

Apache CouchDB 持續更新，1.7 版本強化了 replication 功能和效能。CouchDB 的離線優先架構在物聯網和邊緣運算場景中獲得關注。

### 開發工具

**Docker 1.6 發布**

Docker 1.6 引入了 Docker Registry 2.0、標籤和日誌驅動程式增強。容器化技術在 2015 年持續火爆，Docker Compose 和 Docker Swarm 的整合也在加強。

**Git 2.4 發布**

Git 2.4 帶來了 `git --force-with-lease` 等安全性改進，讓強制推送有更安全的替代方案。

### 雲端與運算

**AWS 強化大數據服務**

AWS 在 2015 年持續擴展大數據處理能力，EMR、Kinesis 和 Redshift 服務都有更新。Lambda 無伺服器運算的概念開始獲得關注。

**Google 雲端平台新功能**

Google 發布了 Cloud Dataflow 等新服務，強調自動擴展和無伺服器架構的理念。

### 業界動態

- **Swift 開源消息**：Apple 的 Swift 程式語言傳出將開源的消息，社群充滿期待
- **Facebook 發布 Relay**：React 生態系的 GraphQL 用戶端框架獲得關注
- **Node.js Foundation 成立**：Node.js 治理結構走向基金會模式
- **Hadoop 10 週年**：Apache Hadoop 自 2005 年誕生以來已走過十個年頭

### 標準與規範

- **HTTP/2 協議推進**：HTTP/2 在 2015 年獲得主流支援
- **WebSocket 標準化完成**：即時雙向通訊成為網頁標準
- **HTML5 正式推薦**：W3C 宣佈 HTML5 作為正式標準

---

*本期新知聚焦 NoSQL 資料庫的最新發展，特別是 Redis 3.0 和 MongoDB 3.0 的新功能。*