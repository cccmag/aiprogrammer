# 本月新知

## 2026 年 8 月程式與 AI 技術動態

### Rust 生態系統

**Tokio 2.0 發布：非同步執行時期全面升級**

Tokio 2.0 於本月正式發布，這是 Rust 非同步執行時期最大的一次升級。新版本引入了「可插拔 I/O 引擎」架構，支援 io_uring（Linux）、kqueue（macOS）和 IOURing（Windows）後端。Tokio 2.0 在 I/O 密集型場景下效能提升了 2-3 倍，記憶體使用量減少了 40%。向後相容性方面，大部分 Tokio 1.x 程式碼只需修改 Cargo.toml 即可遷移。

**Axum 0.10 發布：WebSocket 與 SSE 原生支援**

Axum 0.10 發布，新增了原生的 WebSocket 和 Server-Sent Events（SSE）支援，無需額外的 tower-http 中介軟體。新版本也引入了 Request/Response 攔截器（Interceptor）和 OpenAPI 3.1 自動文件生成。Axum 0.10 在 TechEmpower 基準測試中排名第七，是排名最高的 Rust Web 框架。

**SQLx 1.0 達到生產就緒**

Rust 的非同步 SQL 框架 SQLx 達到 1.0 里程碑。SQLx 以其「編譯期 SQL 檢查」聞名——在編譯階段就能驗證 SQL 語句的正確性。1.0 版本強化了 PostgreSQL 和 SQLite 支援，新增了 SQL Server 的生產級別支援。SQLx 在 Rust 2024 調查中被評為「最受歡迎的資料庫存取框架」。

**SeaORM 1.0：非同步 ORM 的成熟**

SeaORM 1.0 發布，成為 Rust 生態中最完整的非同步 ORM 框架。SeaORM 1.0 支援 PostgreSQL、MySQL、SQLite 和 SQL Server，提供了類似 TypeORM 和 ActiveRecord 的 API。新版本引入了 Migration Generator（自動從資料庫逆向生成程式碼）和 Schema Migration 工具。

### 非 Rust 領域

**Apache Kafka 4.0 發布**

Kafka 4.0 引入了「無限儲存層」（Infinite Storage Tier），允許將歷史資料卸載到物件儲存（S3、GCS），同時保持即時查詢能力。Kafka 4.0 也原生支援了 Rust 用戶端——社區版本的 rdkafka 被官方採用。

**Redis Stack 8.0：向量資料庫功能的成熟**

Redis Stack 8.0 發布，其內建的向量搜尋（RediSearch）模組達到了專用向量資料庫的效能水準。Redis 8.0 也引入了「雙寫」模式（同時寫入記憶體和磁碟），在資料持久性上達到資料庫等級。

**WebGPU 1.0 正式規範**

W3C 發布了 WebGPU 1.0 正式規範。WebGPU 是下一代 Web 圖形 API，提供了比 WebGL 更高效能和更低開銷的 GPU 存取。Rust 生態的 wgpu 程式庫在第一時間就完成了 WebGPU 1.0 的完整支援。

### AI 與機器學習

**MCP 協議 1.0 發布**

Model Context Protocol（MCP）1.0 正式發布。MCP 是由 Anthropic 發起的開放協議，規範了 AI 模型與外部工具/資料庫的互動方式。MCP 1.0 新增了「工具註冊」、「資源發現」和「安全審計」三大核心功能。Rust 社群發布了官方的 MCP SDK——`rust-mcp`。

**Llama 4 在邊緣裝置上達到實用化**

Meta 發布了 Llama 4 的邊緣版本——Llama 4 Edge，參數量從 1B 到 8B。Llama 4 Edge 可以在手機和 IoT 裝置上運行，支援語音辨識、影像分類和文字生成。Rust 的 Candle 和 mistral.rs 框架在第一時間提供了 Llama 4 Edge 的推論支援。

**AI Agent 框架的 Rust 化**

多家公司發布了 Rust 實作的 AI Agent 框架，包括 AgentRS（社群專案）和 Rig（商業支援）。這些框架提供類似 LangChain 的功能——Agent、Tool、Memory、Chain——但使用 Rust 實作，適合高效能場景（如交易系統、即時控制）。

**AI 資料庫設計工具成熟**

AI 輔助資料庫設計工具在本月達到成熟。多款工具支援自然語言描述需求 → 自動生成 ER 圖 → 自動生成 SQL Schema → 自動產生 Rust 資料庫程式碼的完整流程。這讓開發者從「手動設計資料庫」轉變為「描述業務邏輯，AI 自動完成」。

### 開發工具

**VS Code 的 Rust 開發體驗再升級**

VS Code 的 rust-analyzer 擴充套件在 8 月更新中整合了 Tokio 除錯器——可以視覺化 async task 的排程和執行狀態。新增的「借用檢查器視覺化」功能可以圖形化顯示變數的生命週期和所有權流。

**Cargo 2.0 進入測試階段**

Cargo 2.0（代號「Cargo Next」）進入公開測試階段。Cargo 2.0 引入了工作空間級別的平行編譯、ML 驅動的依賴解析和 Docker 原生建置支援。

### 業界動態

- **AWS 全面擁抱 Rust**：AWS 宣布所有新基礎設施服務都將使用 Rust 開發
- **Fuchsia OS 採用 Rust 作為核心語言**：Google 的 Fuchsia OS 正式將 Rust 設為驅動程式開發的第一語言
- **ISO Rust 安全標準 v2**：基於 Rust 2026 的航空級安全規範擴展到汽車和醫療設備
- **Stack Overflow 調查**：Rust 連續第十年獲得「最受歡迎語言」第一名
