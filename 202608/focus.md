# 本期焦點

## Rust 生態系統實戰：Tokio、Axum 與資料庫

### 引言

上一期我們探索了 Rust 語言的歷史與核心設計。本期將把焦點轉向 Rust 的實際應用——如何用 Rust 建構真實世界的網路服務。

Rust 的生態系統已經發展到一個令人驚訝的成熟度：

- **Tokio** 提供了世界級的非同步執行時期，效能媲美 C++ 的 Boost.Asio
- **Axum** 提供了既安全又高效的 Web 框架，型別系統確保路由不會出錯
- **SQLx/SeaORM** 提供了編譯期檢查的資料庫存取，SQL 錯誤在編譯時就被捕獲

這三者的組合——Tokio + Axum + SQLx——已經成為 Rust Web 開發的事實標準。本期將深入探討這些套件的設計哲學、使用技巧和實戰經驗。

---

## 大綱

* [程式：實作 miniblog — 用 Axum + SQLx 打造 RESTful API](focus_code.md)
   - 從零開始建立部落格 API 專案
   - 使用者認證、文章 CRUD、分頁查詢
   - 完整的測試與文件

1. [Tokio 執行時期（2016-2026）](focus1.md)
   - Rust 非同步的設計哲學
   - Tokio 的架構與核心元件
   - 工作竊取排程器
   - Tokio 2.0 的新特性

2. [Axum Web 框架（2021-2026）](focus2.md)
   - Tower 生態系統與中介軟體
   - Extractor 與 Responder
   - 路由設計與型別安全
   - Axum 0.10 的 WebSocket/SSE

3. [SQLx 資料庫存取（2020-2026）](focus3.md)
   - 編譯期 SQL 檢查的設計
   - 非同步查詢與連線池
   - Migration 管理
   - PostgreSQL 與 SQLite

4. [ORM 框架比較（2018-2026）](focus4.md)
   - Diesel：同步 ORM 的穩定性
   - SeaORM：非同步 ORM 的靈活性
   - Prisma：Schema-first 的選擇
   - 何時使用 ORM、何時使用 SQLx

5. [Redis 整合（2017-2026）](focus5.md)
   - redis-rs 用戶端
   - 快取策略與失效模式
   - 工作佇列與 Pub/Sub
   - 會話管理與速率限制

6. [完整 Web 服務（2024-2026）](focus6.md)
   - 專案結構與模組劃分
   - 錯誤處理與統一回應
   - 認證與授權（JWT）
   - 測試、文件與部署

7. [AI + Rust Web 開發（2025-2026）](focus7.md)
   - AI 輔助建立 REST API
   - 自動生成 CRUD 程式碼
   - 資料庫 Schema 設計
   - 從自然語言到完整應用

---

## 生態系統地圖

```
                      ┌─────────────┐
                      │   Axum      │  Web 框架
                      │  (Web 層)   │
                      └──────┬──────┘
                             │
                      ┌──────┴──────┐
                      │   Tower     │  中介軟體層
                      │ (Middleware)│
                      └──────┬──────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────┴──────┐ ┌────┴────┐ ┌───────┴──────┐
       │   Tokio     │ │  SQLx   │ │   redis-rs   │
       │ (Async RT)  │ │   (DB)  │ │   (Cache)    │
       └──────┬──────┘ └─────────┘ └──────────────┘
              │
       ┌──────┴──────┐
       │  mio/io_uring│  I/O 事件驅動
       └─────────────┘
```

## 濃縮回顧

### Tokio：Rust 非同步的基石

Tokio 是 Rust 非同步生態的核心。它提供了：
- **多執行緒工作竊取排程器**：類似 Go 的 M:N 排程
- **非同步 I/O 驅動器**：基於 OS 的事件驅動 I/O
- **實用工具集**：Timer、Signal、Process 管理等

2016 年發布 0.1 版，2018 年 async/await 穩定後完全重寫，2024 年發布 2.0 版本。Tokio 2.0 引入了可插拔 I/O 引擎架構。

### Axum：從 Tower 生態誕生

Axum 是 Tokio 團隊開發的 Web 框架，於 2021 年首次發布。它基於 Tower 生態系統——一個模組化的中介軟體框架。Axum 的核心設計理念是「用 Rust 的型別系統來表達 Web 應用的結構」。

### SQLx：編譯期 SQL 檢查

SQLx 的最大創新是編譯期 SQL 檢查——在編譯階段連接資料庫驗證 SQL 語句的正確性。這意味著 SQL 語法錯誤、表格名稱錯誤、欄位類型不匹配等問題在編譯時就被發現，而不是等到執行時期。

### 組合的威力

Tokio + Axum + SQLx 的組合不僅僅是技術的堆疊，更是一種開發理念的體現：
- **安全**：Rust 的型別系統確保 Web 層和資料庫層的正確性
- **效能**：Tokio 的非同步 I/O 讓 Web 服務可以處理數萬個並發連接
- **生產力**：Axum 的 Extractor/Responder 模式讓 API 開發快速而優雅

---

## 結論與展望

Rust Web 生態在 2026 年已經達到了令人驚嘆的成熟度。Tokio、Axum、SQLx 等套件的組合讓 Rust 不僅僅是系統程式語言，也是建構生產級 Web 服務的絕佳選擇。

展望未來，我們可以看到幾個趨勢：

1. **Rust Web 框架將繼續簡化**：Axum 正在簡化 API，減少樣板程式碼
2. **編譯期檢查將延伸到更多領域**：從 SQL 到 API 合約，更多錯誤在編譯時被捕獲
3. **AI + Rust 開發將成為常態**：AI 輔助生成 CRUD 程式碼、資料庫 Schema、API 文件
4. **Rust 在微服務中的採用將加速**：效能、安全性和部署簡便性使其成為微服務的理想選擇

無論應用如何演進，Rust 的核心使命始終不變：**讓開發者能夠編寫高效、可靠的程式碼，而不需要在安全性和生產力之間妥協**。

---

## 延伸閱讀

- [Tokio 執行時期](focus1.md)
- [Axum Web 框架](focus2.md)
- [SQLx 資料庫存取](focus3.md)
- [ORM 框架比較](focus4.md)
- [Redis 整合](focus5.md)
- [完整 Web 服務](focus6.md)
- [AI + Rust Web 開發](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦另一個影響深遠的主題，敬請期待。*
