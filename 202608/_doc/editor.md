# AI 輔助雜誌編輯實戰手冊 — 八月號

## 前言

本文記錄使用 AI（OpenCode + Big Pickle）編輯《AI 程式人雜誌》2026 年 8 月號的完整流程與技巧。本月主題是「Rust 生態系統實戰—Tokio、Axum 與資料庫」。

---

## 一、專案結構設計

### 1.1 目錄規劃

```
202608/
├── _code/                 # Rust Web 專案
│   ├── Cargo.toml        # 依賴管理
│   ├── src/main.rs       # miniblog 部落格 API
│   └── test.sh          # 測試腳本
├── _doc/
│   └── editor.md        # 編輯技巧記錄（本文件）
├── focus.md              # 本期主題概覽
├── focus1-7.md          # 7 篇生態深入文章
├── focus_code.md        # miniblog 專案文件
├── news.md              # 本月新知
├── article1-10.md      # 精選文章
├── articles.md         # 文章索引
├── end.md              # 結語
└── README.md           # 雜誌總索引
```

### 1.2 技術棧

```
Tokio 2.0   非同步執行時期
Axum 0.8    HTTP 框架
SQLx 0.9    資料庫存取
redis-rs    快取與訊息佇列
tower-http  中介軟體
serde       序列化
UUID + Chrono  工具庫
```

---

## 二、Rust Web 專案的 AI 輔助開發

### 2.1 專案選擇

本月程式專案是 **miniblog**——一個用 Axum + SQLx + Tokio 打造的部落格 REST API。選擇這個專案的原因：

1. **展示完整的 Web 開發流程**：CRUD、錯誤處理、測試
2. **使用真實的 Rust Web 生態**：Axum、SQLx、Tokio
3. **生產級程式碼品質**：統一回應格式、恰當的錯誤處理
4. **可測試**：使用 SQLite 記憶體資料庫進行測試

### 2.2 AI 輔助開發流程

**Phase 1: 需求分析**

```
人類：建立一個部落格 API，支援 CRUD，使用 Axum + SQLx + Tokio
AI：建議技術方案、依賴選擇、專案結構
```

**Phase 2: 程式碼生成**

```
AI 生成：
- Cargo.toml（精確的版本號）
- 資料模型（Post、CreatePost、UpdatePost）
- Handler（5 個 CRUD 端點）
- 錯誤處理（AppError enum）
- 資料庫初始化（SQLite）
- 測試（4 個整合測試）
```

**Phase 3: 除錯與編譯**

```
1. cargo build → 編譯錯誤
   - imports 問題：Axum 0.8 API 差異
   - error：axum 版本號 0.10 不存在，改為 0.8
   
2. cargo test → 測試失敗
   - hyper::body::to_bytes → axum::body::to_bytes
   - PostList / CreatePost 缺少 Deserialize/Serialize derive
   
3. 測試再失敗
   - IntoResponse 未正確設置狀態碼：Json(...) 預設 200
   - 修復：使用 (status, Json(...)).into_response()
   
4. cargo test → 全部通過（4/4）
```

**重要經驗**：Rust Web 開發中，Axum 版本之間的 API 變化和正確的錯誤處理是最容易出錯的地方。AI 在這方面可以快速修復編譯錯誤。

### 2.3 Axum 錯誤處理的陷阱

```
// 錯誤寫法（狀態碼永遠是 200）
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, msg) = match self { ... };
        Json(ApiResponse::err(msg)).into_response()  // ❌ 忽略 status
    }
}

// 正確寫法
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, msg) = match self { ... };
        (status, Json(ApiResponse::err(msg))).into_response()  // ✅
    }
}
```

---

## 三、文章主題寫作經驗

### 3.1 主題規劃

```
Tokio           → 20% (focus1 + article1)
Axum            → 15% (focus2 + article2)
SQLx            → 15% (focus3 + article3)
ORM             → 10% (focus4)
Redis           → 10% (focus5 + article4)
Web 服務        → 10% (focus6 + article5)
AI + Rust Web   → 20% (focus7 + article6-10)
```

### 3.2 與上期（Rust 語言本身）的區別

上期 focus：Rust 語言的歷史與核心設計（2006-2026）
本期 focus：Rust 生態的實際應用（Tokio、Axum、SQLx）

**寫作重點差異**：
- 上期：所有權、借用、生命週期
- 本期：非同步、路由、資料庫存取、快取

---

## 四、常見問題與解決方案

### 4.1 版本相容性

**問題**：Cargo.toml 中指定的版本號與實際發布版本不匹配
**解決**：使用 `cargo search <crate>` 檢查實際版本號

```
$ cargo search axum
axum = "0.8.9"  # 不是 0.10！
```

### 4.2 資料庫選擇

**問題**：需要可測試的程式碼，但可能沒有 PostgreSQL 執行環境
**解決**：使用 SQLite 記憶體資料庫進行開發和測試

```rust
let pool = SqlitePool::connect("sqlite::memory:").await.unwrap();
```

### 4.3 依賴管理

**問題**：SQLx 的 feature flags 很多，容易漏掉
**解決**：確保加入需要的 feature

```toml
sqlx = { version = "0.9", features = [
    "runtime-tokio",  # 與 Tokio 整合
    "sqlite",         # SQLite 支援
    "postgres",       # PostgreSQL 支援（可選）
    "uuid",           # UUID 支援
    "chrono",         # 時間類型支援
] }
```

---

## 五、常用指令參考

```bash
# Rust Web 專案開發
cargo add axum tokio sqlx serde   # 加入依賴
cargo build                        # 編譯
cargo test                         # 執行測試
cargo run                          # 啟動服務

# 測試 API
curl http://localhost:3000/api/posts
curl -X POST -H "Content-Type: application/json" \
  -d '{"title":"Hello","content":"World","author":"Alice"}' \
  http://localhost:3000/api/posts

# 資料庫
sqlx migrate run                   # 執行 Migration
sqlx prepare                       # 生成離線資料
```

---

## 六、最佳實踐總結

1. **先 cargo build 再寫文章**：確保程式碼可編譯，文章中的程式碼範例才是正確的
2. **版本相容性檢查**：AI 常猜錯 crate 版本號，用 `cargo search` 確認
3. **錯誤處理測試**：Axum 的錯誤處理最容易出錯，用測試驗證每個錯誤路徑
4. **使用 SQLite 記憶體測試**：快速、隔離、無需外部依賴
5. **專注於生態而不是語言本身**：本期重點是套件的使用，不是 Rust 語法

---

*本文為《AI 程式人雜誌》編輯技巧記錄*
