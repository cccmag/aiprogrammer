# SQLx 資料庫程式設計實戰

## 前言

在 Rust 生態系中，SQLx 已成為非同步資料庫操作的事實標準。不同於 Diesel 這類 ORM，SQLx 採用「接近 SQL」的哲學——你寫 SQL，它幫你安全地執行。本文將深入探討 SQLx 的核心機制與實戰技巧，幫助你在生產環境中寫出高效、安全的資料庫程式。

## SQLx 0.9/1.0 的新功能

SQLx 自 0.9 起引入了多項關鍵改進，而即將到來的 1.0 版本更是標誌性的里程碑：

**0.9 重點**
- 增強的健康檢查機制：`Pool::acquire()` 現在會在連線失效時自動重試
- 更好的 TLS 支援：原生支援 `rustls` 與 `native-tls` 雙後端
- 改進的 PostgreSQL 類型映射：涵蓋 `TIMESTAMPTZ`、`NUMERIC`、`JSONB` 等
- 更嚴格的編譯期檢查錯誤訊息，準確指出 SQL 問題所在

**1.0 預覽**
- API 穩定性保證：1.0 之後將遵循 semver，不再有破壞性變更
- 移除所有 deprecated API，簡化公共介面
- 統一的 `Column` 與 `TypeInfo` 介面讓資料庫後端切換更平滑
- 官方 Migration 工具鏈大幅強化

## 編譯期 SQL 檢查

SQLx 最獨特的功能就是能在編譯時檢查 SQL 語法與型別正確性。原理並不複雜：`sqlx::query!` 與 `sqlx::query_as!` 等巨集會在編譯期間連線到指定的資料庫，解析 SQL 並比對參數與回傳型別。

**設定方式**（`.env` 或環境變數）：

```
DATABASE_URL=postgres://user:pass@localhost/mydb
```

```rust
// 如果 SQL 有誤，這一行就編譯不過
let users = sqlx::query!("SELECT id, name, email FROM users WHERE id = $1", user_id)
    .fetch_all(&pool)
    .await?;
```

巨集回傳的型別會自動推導——`id` 是 `i32`，`name` 是 `String`，`email` 是 `Option<String>`，完全不需要手動標註。

**注意事項**：編譯期檢查需要實際的資料庫連線。在 CI 環境中，建議使用 SQLite 記憶體資料庫進行檢查，或透過 `SQLX_OFFLINE=true` 搭配 `cargo sqlx prepare` 產生的 offline 資料來繞過連線需求。

```bash
# 在開發機上產生 offline 資料
cargo sqlx prepare --database-url postgres://localhost/dev

# CI 中使用 offline 模式
SQLX_OFFLINE=true cargo check
```

## 非同步查詢與連線池管理

SQLx 基於 `tokio` 或 `async-std` 的非同步執行器，提供真正的非同步資料庫存取。

**建立連線池**：

```rust
let pool = PgPoolOptions::new()
    .max_connections(20)
    .connect(&database_url)
    .await?;
```

**連線池的關鍵參數**：
- `max_connections`：最大連線數，建議根據資料庫端上限設定
- `min_connections`：最小閒置連線，避免突發流量時冷啟動
- `acquire_timeout`：取得連線的超時時間，預設 30 秒
- `idle_timeout`：閒置連線關閉時間，預設 10 分鐘

**執行查詢的三種方式**：

```rust
// 方式一：自動從池中取連線
sqlx::query("SELECT * FROM users").fetch_all(&pool).await?;

// 方式二：手動持有連線，適合交易
let mut conn = pool.acquire().await?;
sqlx::query("SELECT 1").fetch_one(&mut *conn).await?;

// 方式三：直接使用 PgConnection（不建議在 Web 應用中使用）
```

## Migration 實戰

SQLx 提供內建的 migration 系統，省去外部工具的依賴。

**初始化**：

```bash
cargo sqlx migrate add create_users_table
```

這會在 `migrations/` 目錄下產生類似 `20260601000001_create_users_table.sql` 的檔案，內含兩個 `-- Add migration script here` 註解，分別對應 `up` 與 `down`。

**範例 migration**：

```sql
-- migrations/20260601000001_create_users_table.sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

```sql
-- down migration
DROP TABLE IF EXISTS users;
```

**程式內執行 migration**：

```rust
sqlx::migrate!("./migrations")
    .run(&pool)
    .await?;
```

這段程式碼通常放在 `main` 函式或應用啟動階段。SQLx 會自動追蹤已執行過的 migration，不會重複套用。

**生產部署建議**：
- 使用 `cargo sqlx migrate run` 指令在部署流程中手動執行
- 永遠不要修改已上線的 migration 檔案，只新增新的 migration
- 資料庫備份與 migration 指令應包在同一個自動化腳本中

## PostgreSQL vs SQLite vs MySQL

SQLx 對三大資料庫後端的支援程度各有不同：

| 特性 | PostgreSQL | SQLite | MySQL |
|------|-----------|--------|-------|
| 豐富型別 | 完整支援（陣列、JSON、範圍） | 基本型別 | 基本型別 |
| 非同步驅動 | `tokio-postgres` | `rusqlite`（同步） | `sqlx-mysql` |
| 編譯期檢查 | 完整 | 完整 | 完整 |
| 交易支援 | 完整 + 保存點 | 完整 | 完整 |
| 連線池 | 池化連線 | 僅單連線 | 池化連線 |
| 生產推薦度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐（開發/測試） | ⭐⭐⭐⭐ |
| 遷移支援 | 完整 | 完整 | 完整 |

**選擇建議**：
- **PostgreSQL**：生產環境首選，型別系統最完整，非同步驅動最成熟
- **SQLite**：開發測試與單機應用首選，零設定，但缺乏連線池與並寫支援
- **MySQL**：若團隊已有 MySQL 基礎設施可選，但 SQLx 對 MySQL 的支援不如 PostgreSQL 全面

## 最佳實踐

### 交易管理

```rust
let mut tx = pool.begin().await?;

let user_id = sqlx::query_scalar::<_, i64>(
    "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id"
)
.bind(&name)
.bind(&email)
.fetch_one(&mut *tx)
.await?;

sqlx::query("INSERT INTO user_roles (user_id, role) VALUES ($1, $2)")
    .bind(user_id)
    .bind(&role)
    .execute(&mut *tx)
    .await?;

tx.commit().await?;
// 若上述任一失敗，tx.rollback() 會自動於 drop 時呼叫
```

### 批次操作

```rust
let mut tx = pool.begin().await?;

// 大量寫入使用迴圈批次（內部自動批次）
for user in users {
    sqlx::query("INSERT INTO users (name) VALUES ($1)")
        .bind(user.name)
        .execute(&mut *tx)
        .await?;
}

tx.commit().await?;
```

對於極大量資料，考慮使用 `COPY FROM`（PostgreSQL）或批次語法：

```rust
// PostgreSQL COPY 協議
use sqlx::postgres::PgCopyIn;

let mut tx = pool.begin().await?;
let mut copy = tx.copy_in_raw("COPY users (name, email) FROM STDIN (FORMAT CSV)").await?;
copy.send_all(&mut csv_data.as_ref()).await?;
copy.finish().await?;
tx.commit().await?;
```

### 錯誤處理

```rust
async fn get_user(pool: &PgPool, id: i64) -> Result<Option<User>, sqlx::Error> {
    sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(id)
        .fetch_optional(pool)
        .await
}
```

常見的 `sqlx::Error` 變體：
- `RowNotFound`：`fetch_one` 查無資料
- `Database`：資料庫層錯誤（唯一鍵衝突、型別不符等）
- `PoolClosed`：連線池已關閉
- `Io`：網路或 TLS 錯誤

```rust
// 根據錯誤類型分流處理
match result {
    Err(sqlx::Error::RowNotFound) => Ok(None),
    Err(e) => Err(e),
    Ok(row) => Ok(Some(row)),
}
```

## SQLx + SeaORM 混用策略

SeaORM 是基於 SQLx 的上層 ORM，底層連線池完全共用。混用兩者可以兼顧開發效率與靈活性。

**架構建議**：

```
┌─────────────────────────────┐
│          Service Layer       │
├──────────────┬──────────────┤
│   SeaORM     │   SQLx Raw   │
│  (CRUD 為主) │  (複雜查詢)   │
├──────────────┴──────────────┤
│        SQLx Pool            │
│   (PgPool / MySqlPool)      │
├─────────────────────────────┤
│          Database            │
└─────────────────────────────┘
```

**實作範例**：

```rust
use sea_orm::{Database, DatabaseConnection, EntityTrait, Set};
use sqlx::PgPool;

// 共用連線池
let pool = PgPoolOptions::new()
    .max_connections(20)
    .connect(&database_url)
    .await?;

// SeaORM 可透過 sqlx 連線池建立
let db: DatabaseConnection = Database::connect_sqlx_pg(pool.clone()).await?;

// 簡單 CRUD 用 SeaORM
let user = user::Entity::find_by_id(id).one(&db).await?;

// 複雜報表用 SQLx
let summary = sqlx::query_as::<_, ReportRow>(
    "SELECT u.name, COUNT(o.id) as order_count
     FROM users u JOIN orders o ON u.id = o.user_id
     GROUP BY u.name HAVING COUNT(o.id) > $1"
)
.bind(min_orders)
.fetch_all(&pool)
.await?;
```

**混用原則**：
- SeaORM 處理 CRUD、關聯載入、Migration（非 SQLx migration）
- SQLx 處理複雜 JOIN、CTE、視窗函數、批次寫入
- 兩者共用同一個底層連線池，不浪費資源
- 交易層面不可混用——要在 SeaORM 交易中執行 SQLx raw query，需透過 `DbConn::get_pg_connection()` 取得底層連線

## 總結

SQLx 提供了一條兼具安全性與靈活性的資料庫程式設計路徑。編譯期 SQL 檢查讓許多常見錯誤在編譯階段就被攔截，非同步連線池確保高效資源利用，而 migration 系統讓資料庫版本控制變得優雅。搭配 SeaORM 等高階工具時，SQLx 又能退居底層引擎，在需要精細控制時直接介入。

對於 Rust 後端開發者而言，掌握 SQLx 不只是學會一個套件，而是理解如何在型別系統的加持下寫出既安全又高效的資料庫程式碼。
