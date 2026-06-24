# 本月新知

## 2026 年 6 月程式與 AI 技術動態

### 資料庫技術

**SQLite 4.0 發布 — 向量搜尋與 WASM 原生支援**

SQLite 團隊於本月發布 4.0 重大版本更新。最大的亮點是內建向量搜尋引擎（Vector Search Engine），支援儲存和查詢浮點數向量，可直接用於 RAG 應用。此外，SQLite 4.0 將 WebAssembly 編譯目標提升為一等平台，瀏覽器中的 SQLite 執行效能達到原生水準的 90% 以上。

**PostgreSQL 20 引入原生機器學習擴展**

PostgreSQL 20 發布，其中最受矚目的功能是「內建 ML 擴展」— 使用者可以直接在 SQL 中呼叫 Hugging Face 模型進行推論。新的 `pg_ml` 模組支援文字分類、情感分析和向量嵌入生成。此外，PG20 的並行查詢效能提升了 3 倍，特別是複雜 JOIN 和聚合查詢的場景。

**MySQL HeatWave GenAI 整合向量資料庫**

甲骨文宣布 MySQL HeatWave 服務全面整合向量儲存與生成式 AI 能力。使用者可以在同一個 MySQL 資料庫中執行 OLTP、OLAP 和向量相似度搜尋。HeatWave 的 GPU 加速查詢引擎現已支援 Llama 4 和 GPT-6 的嵌入模型。

**EdgeDB 4.0 正式發布**

EdgeDB 4.0 發布，這是一個基於 PostgreSQL 的下一代關聯式資料庫，提供了更現代的資料模型和查詢語言。新版本引入了「計算屬性」（Computed Properties）和「全域變數」（Global Variables），讓 schema 定義更加靈活。EdgeDB 的 EdgeQL 查詢語言持續獲得開發者好評。

### 程式語言與框架

**Python 4.0 alpha 1 發布**

Python 4.0 第一個 alpha 版本於本月發布，這是 Python 語言自 2008 年以來的首個重大版本。主要變更包括：移除 GIL（全域直譯器鎖定）、新的型別語法（`list[int]` 不再需要 `from __future__ import annotations`）、模式匹配的強化，以及「凍結集合字面量」（FrozenSet Literal）的引入。

**DuckDB 2.0 — 嵌入式 OLAP 資料庫的重大升級**

DuckDB 2.0 發布，這個「嵌入式 PostgreSQL 的 OLAP 對手」持續進化。新版本引入了多檔案分割區表、增量 Materialized View 更新、以及 Python UDF 的原生支援。DuckDB 在單機分析場景下的效能已超越許多傳統資料倉儲。

### AI 與機器學習

**向量資料庫市場整合加速**

2026 年 6 月，向量資料庫（Vector Database）市場出現重大整合。Pinecone 宣布收購 Weaviate，Chroma 與 Milvus 宣布合併。市場分析師指出，向量資料庫正在從獨立產品轉變為主流資料庫的內建功能 — SQLite 4.0 和 PostgreSQL 20 的向量搜尋功能就是最好的證明。

**RAG 2.0：結構化資料檢索的崛起**

學術界提出了 RAG 2.0 的概念，強調結合結構化資料（SQL 資料庫）和非結構化資料（向量資料庫）的混合檢索。傳統 RAG 只檢索文字片段，而 RAG 2.0 能夠同時查詢關聯式資料庫和向量索引，大幅提升了問答系統的準確度。

**Dataherald 開源 Text-to-SQL 引擎**

Dataherald 團隊開源了全新的 Text-to-SQL 引擎，使用 GPT-6 微調模型，在 Spider 2.0 基準測試上達到 92% 的準確率。該引擎支援多輪對話、資料庫 schema 感知，以及複雜 JOIN 和子查詢的生成。

### 開發工具與雲端服務

**GitHub Copilot 資料庫模式感知**

GitHub 宣布 Copilot 新增資料庫模式感知功能。當開發者在 SQL 檔案或 ORM 程式碼中工作時，Copilot 能夠自動讀取資料庫 schema 並提供上下文感知的 SQL 補全和最佳化建議。

**Vercel Postgres Edge 支援全球分佈**

Vercel 發布 Postgres Edge，這是一個基於 PostgreSQL 的全域分佈式資料庫服務。Edge 節點自動快取資料，讓全球使用者的查詢延遲低於 10 毫秒。Vercel Postgres 支援完整的 SQL 語法和即時訂閱功能。

### 業界動態

- **Google 開源 AlloyDB 核心元件**：基於 PostgreSQL 的雲端資料庫核心程式碼開源
- **Snowflake 收購 Databricks**：資料倉儲與資料湖的巨額合併
- **MongoDB 推出 SQL 相容層**：文件資料庫對 SQL 生態的進一步靠攏
- **Oracle 發布免費版 Oracle 24c**：提供完整的 SQL 功能支援

### 標準與規範

- **ISO 正式發布 SQL:2026 標準**：新增 JSON 功能、向量資料型別和圖形查詢語法
- **W3C 啟動 Web SQL Database API 2.0**：瀏覽器端本地資料庫的新標準
- **IEEE 發布資料庫加密標準**：定義了靜態資料和傳輸中資料的加密規範
