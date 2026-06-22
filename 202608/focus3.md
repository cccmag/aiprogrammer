# SQLx 資料庫存取

## 編譯期檢查的 SQL 操作（2020-2026）

### 前言

在傳統的資料庫開發中，SQL 錯誤是最常見的執行時期錯誤之一：

```python
# Python：SQL 錯誤直到執行時才被發現
cursor.execute("SELECT * FORM users")  # 執行時期報錯：FORM 拼寫錯誤
```

Rust 的 SQLx 從根本上改變了這個局面——**SQL 語句在編譯階段就被檢查**。

### SQLx 的設計哲學

SQLx 的核心理念是：**SQL 不應該是你需要猜測的東西**。

```rust
// SQLx：編譯時檢查 SQL
let user = sqlx::query!(
    "SELECT id, name, email FROM users WHERE id = $1",
    user_id
)
.fetch_one(&pool)
.await?;
// 編譯器知道回傳型別：User { id: i32, name: String, email: Option<String> }
```

如果在編譯時連接資料庫，SQLx 會：
1. 連接資料庫
2. 解析 SQL 語句
3. 驗證表格和欄位是否存在
4. 檢查型別是否匹配
5. 自動生成 Rust 結構體

**這意味著**：
- `FROMM` 拼寫錯誤 → 編譯錯誤
- `users` 表格不存在 → 編譯錯誤
- `email` 欄位不存在 → 編譯錯誤
- 傳入 `&str` 但資料庫期望 `i32` → 編譯錯誤

### 編譯期檢查的實現

SQLx 透過 `sqlx::query!` 和 `query_as!` 這兩個宏來實現編譯期檢查：

```rust
// 運行時需要 DATABASE_URL 環境變數
// cargo build 時會連接資料庫，檢查 SQL
let posts = sqlx::query_as!(
    Post,  // 自動映射到 Post 結構體
    r#"SELECT id, title, content, created_at 
       FROM posts 
       WHERE published = $1 
       ORDER BY created_at DESC
       LIMIT $2"#,
    true,   // $1: published
    10      // $2: limit
)
.fetch_all(&pool)
.await?;
```

**執行流程**：
```
cargo build → sqlx 連接資料庫 → 檢查 SQL 語法
→ 檢查表格/欄位 → 檢查型別 → 生成映射程式碼 → 編譯
```

### 離線模式

在沒有資料庫的環境中（如 CI/CD），SQLx 支援離線模式：

```bash
# 生成 SQLx 離線資料
cargo sqlx prepare --database-url postgres://...

# 在 CI 中使用離線資料
# 不需要資料庫連接，使用之前生成的 .sqlx/ 目錄
cargo build --features sqlx/offline
```

### 連線池管理

```rust
use sqlx::postgres::PgPoolOptions;

let pool = PgPoolOptions::new()
    .max_connections(100)    // 最大連線數
    .min_connections(10)     // 最小維持連線
    .acquire_timeout(Duration::from_secs(30))  // 取得連線超時
    .idle_timeout(Duration::from_secs(600))    // 空閒連線超時
    .connect("postgres://user:pass@localhost/db")
    .await?;
```

### 非同步查詢

SQLx 從設計之初就是非同步的——它使用 Tokio 作為執行時期：

```rust
// 單一查詢
let user = sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
    .bind(user_id)
    .fetch_one(&pool)
    .await?;

// 多筆查詢
let users = sqlx::query_as::<_, User>(
    "SELECT * FROM users WHERE created_at > $1"
)
    .bind(since_date)
    .fetch_all(&pool)
    .await?;

// 可選結果
let maybe_user = sqlx::query_as::<_, User>(
    "SELECT * FROM users WHERE email = $1"
)
    .bind(&email)
    .fetch_optional(&pool)
    .await?;
```

### Migration 管理

SQLx 內建 migration 系統——使用原始的 SQL 檔案來管理資料庫變更：

```sql
-- migrations/20260801000001_create_users.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

```rust
// Rust 代碼中執行 migration
sqlx::migrate!()  // 自動載入 migrations/ 目錄
    .run(&pool)
    .await?;
```

### 支援的資料庫

| 資料庫 | Crate 名稱 | 特色 |
|--------|-----------|------|
| PostgreSQL | `sqlx-postgres` | 完整支援，編譯期檢查 |
| MySQL | `sqlx-mysql` | 完整支援 |
| SQLite | `sqlx-sqlite` | 零配置，適合開發/測試 |
| MSSQL | `sqlx-mssql` | 1.0 後加入 |

### 類型映射

SQLx 自動處理 Rust 型別與資料庫型別的映射：

```rust
// 自訂類型映射
struct UserId(i64);

impl Type<Postgres> for UserId {
    fn type_info() -> PgTypeInfo {
        PgTypeInfo::with_name("int8")
    }
}

impl Encode<'_, Postgres> for UserId {
    fn encode_by_ref(&self, buf: &mut PgArgumentBuffer) -> IsNull {
        <i64 as Encode<Postgres>>::encode(self.0, buf)
    }
}

impl Decode<'_, Postgres> for UserId {
    fn decode(value: PgValueRef<'_>) -> Result<Self, BoxDynError> {
        Ok(UserId(<i64 as Decode<Postgres>>::decode(value)?))
    }
}
```

### 交易處理

```rust
let mut tx = pool.begin().await?;

// 多步驟操作在一個交易中
sqlx::query("UPDATE accounts SET balance = balance - $1 WHERE id = $2")
    .bind(100.0)
    .bind(from_id)
    .execute(&mut *tx)
    .await?;

sqlx::query("UPDATE accounts SET balance = balance + $1 WHERE id = $2")
    .bind(100.0)
    .bind(to_id)
    .execute(&mut *tx)
    .await?;

// 提交或回滾
tx.commit().await?;  // 或 tx.rollback().await?;
```

### SQLx vs 其他選擇

| 特性 | SQLx | Diesel | SeaORM |
|------|------|--------|--------|
| 編譯期 SQL 檢查 | ✅ | 🟡 部分 | ❌ |
| 非同步 | ✅ | 🟡 同步為主 | ✅ |
| Raw SQL | ✅ 首選 | 🟡 支援 | 🟡 支援 |
| ORM 功能 | ❌ 純 SQL | ✅ 完整 ORM | ✅ 完整 ORM |
| Migration | ✅ 純 SQL 檔案 | ✅ DSL + SQL | ✅ Schema 格式 |
| 學習曲線 | 低（需要懂 SQL） | 高（自訂 DSL） | 中 |

### 小結

SQLx 的設計體現了 Rust 的核心理念：**在編譯期發現錯誤**。將 SQL 檢查提前到編譯階段，不僅減少了執行時期錯誤，也讓開發者對資料庫操作有更大的信心。對於需要直接控制 SQL 的專案，SQLx 是最佳選擇。

---

**下一步**：[ORM 框架比較](focus4.md)

## 延伸閱讀

- [SQLx 官方文件](https://www.google.com/search?q=SQLx+Rust+documentation)
- [SQLx 編譯期檢查指南](https://www.google.com/search?q=SQLx+compile+time+checking)
- [SQLx vs Diesel 比較](https://www.google.com/search?q=SQLx+vs+Diesel+Rust)
