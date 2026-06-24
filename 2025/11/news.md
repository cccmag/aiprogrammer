# 本月新知

## 2026 年 11 月系統設計技術動態

### 分散式系統框架

**Apache Kafka 4.0 正式發布**

Kafka 4.0 於本月正式發布，這是 Apache Kafka 的重大版本升級。最大的變革在於移除了 ZooKeeper 依賴，全面採用 KRaft 共識機制。新版本在效能上有大幅提升，單叢集吞吐量突破每秒千萬筆訊息。此外，Kafka 4.0 引入了分層儲存架構，支援將冷資料自動轉移到物件儲存，大幅降低儲存成本。

**etcd 3.6 強化分散式一致性**

etcd 團隊發布了 3.6 版本，專注於分散式系統的核心一致性協定 Raft 的效能優化。新版本引入了「讀取管線化」機制，將唯讀請求的延遲降低 40%。同時新增了分散式鎖的監控指標，方便開發者診斷死鎖和競爭條件。

### API 與閘道技術

**GraphQL Federation 2.0 成為主流**

Apollo GraphQL 的 Federation 2.0 規範在本月獲得廣泛採用。新版本解決了分散式 GraphQL 架構中的型別衝突和欄位合併問題。多個大型企業（包括 Netflix 和 Airbnb）公開分享了他們遷移至 Federation 2.0 的經驗，證明了其在大型微服務架構中的價值。

**Envoy 發布 1.40 版，支援 WebAssembly 擴展**

CNCF 的 Envoy Proxy 發布 1.40 版，最重要的特性是 WebAssembly（WASM）擴展的正式穩定。開發者可以使用 Rust、C++ 或 AssemblyScript 編寫高效能的 filter 插件，在不重啟服務的情況下動態載入。這為 API 閘道的客製化路由和流量控制開闢了全新可能。

### 快取技術

**Redis 8.0 引入向量資料庫支援**

Redis 8.0 於本月發布 beta 版本，最大亮點是內建向量相似度搜尋功能。開發者可以直接在 Redis 中儲存 embedding 向量並執行 ANN 搜尋，支援 HNSW 和 FLAT 兩種索引演算法。這使得 Redis 從傳統的快取伺服器轉型為 AI 基礎設施的核心元件。

**Memcached 進入維護模式**

Memcached 團隊宣布，由於活躍維護者減少，專案將進入維護模式。社群建議新專案考慮使用 Redis 或其他現代快取解決方案。這標誌著一個時代的結束——Memcached 在 Web 快取領域服務了超過 20 年。

### 容器與編排

**Docker 發布新一代 BuildKit**

Docker 宣布新一代 BuildKit 引擎，支援遠端快取分享和並行層建構，能將 CI/CD 中的容器映像建構時間減少 60%。新引擎還支援 WASM 基礎映像，允許將 WebAssembly 模組容器化後運行在 Docker 環境中。

**Kubernetes 1.32 聚焦邊緣運算**

Kubernetes 1.32 的主要特性集中在邊緣運算場景，包括正式支援單節點叢集（Single-Node Cluster）、優化節點自動恢復機制，以及引入輕量級 kubelet 模式。這些改進使得 K8s 在物聯網和邊緣場景中的部署更加可行。

### 資料庫架構

**CockroachDB 發布無伺服器版**

CockroachDB 推出無伺服器資料庫服務，支援自動擴展和按用量付費。其分散式 SQL 引擎可以在跨區域部署時保持強一致性，解決了傳統資料庫在全球部署中的痛點。

**MySQL 9.1 強化合併複寫**

Oracle 發布 MySQL 9.1，其中合併複寫（Group Replication）功能獲得重大升級，支援自動故障檢測和透明的重新平衡。新版本還引入了基於效能的自適應複寫拓撲，能根據讀寫壓力自動調整架構。

### 業界動態

- **Amazon 推出 Distributed SQL Accelerator**：基於 FPGA 的查詢加速硬體
- **Google Cloud 宣布 AlloyDB 支援 PostgreSQL 16 相容性**
- **Cloudflare 發布 R2 事件通知**：支援 S3 相容的物件儲存事件驅動架構
- **Confluent 收購雲端原生事件閘道新創公司**

### 標準與規範

- **OpenTelemetry 1.30 發布**：分散式追蹤與指標收集的標準化進展
- **CNCF 發布 Service Mesh 互通性白皮書**：為 Istio、Linkerd 和 Consul 的互通提供指引
- **JSON Schema 2026-11 草案發布**：強化對事件資料的驗證支援
