# miniblog：用 Axum + SQLx 打造 RESTful API

## 概述

本文展示如何使用 Rust 生態的核心套件——Axum、SQLx、Tokio——建構一個完整的部落格 REST API。這個專案示範了生產級 Rust Web 服務的標準模式。

## 專案簡介

**miniblog** 是一個簡單的部落格 API，支援：
- 文章 CRUD（建立、讀取、更新、刪除）
- SQLite 後端（可切換到 PostgreSQL）
- 統一的錯誤處理與回應格式
- 完整的 API 測試

## 技術棧

| 層級 | 套件 | 用途 |
|------|------|------|
| 執行時期 | Tokio | 非同步 I/O 與排程 |
| Web 框架 | Axum | HTTP 路由與中介軟體 |
| 資料庫 | SQLx (SQLite/PostgreSQL) | 非同步資料庫存取 |
| 序列化 | Serde + serde_json | JSON 序列化/反序列化 |
| 唯一 ID | UUID | 主鍵生成 |

## 核心設計

### 1. 應用狀態（AppState）

```rust
#[derive(Clone)]
struct AppState {
    db: SqlitePool,  // 資料庫連線池
}
```

`AppState` 是 Axum 的依賴注入機制。所有 Handler 通過 `State(state): State<AppState>` 存取共用狀態。

### 2. 統一回應格式

所有 API 回應採用統一的格式：

```json
{
  "success": true,
  "data": { ... },       // 成功時的回應資料
  "error": null          // 失敗時的錯誤訊息
}
```

### 3. 錯誤處理

```rust
enum AppError {
    NotFound(String),    // 404
    Database(String),    // 500
    BadRequest(String),  // 400
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, msg) = match self {
            Self::NotFound(m) => (StatusCode::NOT_FOUND, m),
            Self::BadRequest(m) => (StatusCode::BAD_REQUEST, m),
            Self::Database(m) => (StatusCode::INTERNAL_SERVER_ERROR, m),
        };
        (status, Json(ApiResponse::<()>::err(msg))).into_response()
    }
}
```

### 4. 資料庫初始化

```rust
async fn init_db(pool: &SqlitePool) -> Result<(), sqlx::Error> {
    sqlx::query(
        "CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL DEFAULT '',
            author TEXT NOT NULL DEFAULT 'anonymous',
            created_at TEXT NOT NULL
        )",
    )
    .execute(pool)
    .await?;
    Ok(())
}
```

## API 端點

| 方法 | 路徑 | 功能 | 狀態碼 |
|------|------|------|--------|
| GET | `/api/posts` | 列出所有文章 | 200 |
| POST | `/api/posts` | 建立新文章 | 201 |
| GET | `/api/posts/{id}` | 取得單篇文章 | 200/404 |
| PUT | `/api/posts/{id}` | 更新文章 | 200/404 |
| DELETE | `/api/posts/{id}` | 刪除文章 | 200/404 |

## 完整程式碼

```rust
use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::IntoResponse,
    routing::get,
    Json, Router,
};
use serde::{Deserialize, Serialize};
use sqlx::{FromRow, SqlitePool};
use uuid::Uuid;

// ─── Models ────────────────────────────────────────────────────────

#[derive(Debug, Serialize, Deserialize, FromRow)]
struct Post {
    id: String,
    title: String,
    content: String,
    author: String,
    created_at: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct CreatePost {
    title: String,
    content: String,
    author: String,
}

#[derive(Debug, Deserialize)]
struct UpdatePost {
    title: Option<String>,
    content: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct PostList {
    posts: Vec<Post>,
    total: u64,
}

#[derive(Debug, Serialize)]
struct ApiResponse<T: Serialize> {
    success: bool,
    data: Option<T>,
    error: Option<String>,
}

impl<T: Serialize> ApiResponse<T> {
    fn ok(data: T) -> Self {
        Self { success: true, data: Some(data), error: None }
    }

    fn err(msg: impl Into<String>) -> Self {
        Self { success: false, data: None, error: Some(msg.into()) }
    }
}

// ─── App State ─────────────────────────────────────────────────────

#[derive(Clone)]
struct AppState {
    db: SqlitePool,
}

// ─── Error Handling ────────────────────────────────────────────────

enum AppError {
    NotFound(String),
    Database(String),
    BadRequest(String),
}

impl IntoResponse for AppError {
    fn into_response(self) -> axum::response::Response {
        let (status, msg) = match self {
            Self::NotFound(m) => (StatusCode::NOT_FOUND, m),
            Self::BadRequest(m) => (StatusCode::BAD_REQUEST, m),
            Self::Database(m) => (StatusCode::INTERNAL_SERVER_ERROR, m),
        };
        (status, Json(ApiResponse::<()>::err(msg))).into_response()
    }
}

impl From<sqlx::Error> for AppError {
    fn from(e: sqlx::Error) -> Self {
        Self::Database(e.to_string())
    }
}

// ─── Handlers ──────────────────────────────────────────────────────

async fn list_posts(State(state): State<AppState>) -> Result<Json<PostList>, AppError> {
    let posts = sqlx::query_as::<_, Post>("SELECT * FROM posts ORDER BY created_at DESC")
        .fetch_all(&state.db)
        .await?;

    let total = posts.len() as u64;
    Ok(Json(PostList { posts, total }))
}

async fn get_post(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> Result<Json<ApiResponse<Post>>, AppError> {
    let post = sqlx::query_as::<_, Post>("SELECT * FROM posts WHERE id = ?")
        .bind(&id)
        .fetch_optional(&state.db)
        .await?
        .ok_or_else(|| AppError::NotFound(format!("Post '{}' not found", id)))?;

    Ok(Json(ApiResponse::ok(post)))
}

async fn create_post(
    State(state): State<AppState>,
    Json(input): Json<CreatePost>,
) -> Result<(StatusCode, Json<ApiResponse<Post>>), AppError> {
    if input.title.is_empty() {
        return Err(AppError::BadRequest("Title cannot be empty".into()));
    }

    let id = Uuid::new_v4().to_string();
    let now = chrono::Utc::now().to_rfc3339();

    sqlx::query(
        "INSERT INTO posts (id, title, content, author, created_at) VALUES (?, ?, ?, ?, ?)",
    )
    .bind(&id)
    .bind(&input.title)
    .bind(&input.content)
    .bind(&input.author)
    .bind(&now)
    .execute(&state.db)
    .await?;

    let post = Post {
        id,
        title: input.title,
        content: input.content,
        author: input.author,
        created_at: now,
    };

    Ok((StatusCode::CREATED, Json(ApiResponse::ok(post))))
}

async fn update_post(
    State(state): State<AppState>,
    Path(id): Path<String>,
    Json(input): Json<UpdatePost>,
) -> Result<Json<ApiResponse<Post>>, AppError> {
    let existing = sqlx::query_as::<_, Post>("SELECT * FROM posts WHERE id = ?")
        .bind(&id)
        .fetch_optional(&state.db)
        .await?
        .ok_or_else(|| AppError::NotFound(format!("Post '{}' not found", id)))?;

    let title = input.title.unwrap_or(existing.title);
    let content = input.content.unwrap_or(existing.content);

    sqlx::query("UPDATE posts SET title = ?, content = ? WHERE id = ?")
        .bind(&title)
        .bind(&content)
        .bind(&id)
        .execute(&state.db)
        .await?;

    let updated = sqlx::query_as::<_, Post>("SELECT * FROM posts WHERE id = ?")
        .bind(&id)
        .fetch_one(&state.db)
        .await?;

    Ok(Json(ApiResponse::ok(updated)))
}

async fn delete_post(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> Result<Json<ApiResponse<()>>, AppError> {
    let result = sqlx::query("DELETE FROM posts WHERE id = ?")
        .bind(&id)
        .execute(&state.db)
        .await?;

    if result.rows_affected() == 0 {
        return Err(AppError::NotFound(format!("Post '{}' not found", id)));
    }

    Ok(Json(ApiResponse::ok(())))
}

// ─── Router ────────────────────────────────────────────────────────

fn create_router(state: AppState) -> Router {
    Router::new()
        .route("/api/posts", get(list_posts).post(create_post))
        .route("/api/posts/{id}", get(get_post).put(update_post).delete(delete_post))
        .with_state(state)
}
```

## 測試結果

```
running 4 tests
test tests::test_list_posts ... ok
test tests::test_create_post ... ok
test tests::test_get_post_not_found ... ok
test tests::test_delete_post ... ok

test result: ok. 4 passed; 0 failed
```

## Axum + SQLx 開發的關鍵要點

### 1. 提取器（Extractor）模式

Axum 的 Handler 參數通過提取器（Extractor）自動從 HTTP 請求中提取：

```rust
async fn handler(
    State(state): State<AppState>,  // 從狀態提取
    Path(id): Path<String>,        // 從路徑提取
    Json(input): Json<Input>,       // 從請求體提取
) -> Result<Json<Output>, Error> { ... }
```

每個提取器都是一個 trait——可以組合和自訂。

### 2. 錯誤的統一處理

所有 Handler 都返回 `Result<T, AppError>`，錯誤的格式化和 HTTP 狀態碼由 `AppError::into_response()` 統一處理。

### 3. SQLx 的型別安全

```rust
// 編譯器知道回傳型別是 Vec<Post>
let posts = sqlx::query_as::<_, Post>("SELECT * FROM posts")
    .fetch_all(&pool)
    .await?;
```

### 4. 測試策略

使用 SQLite 記憶體資料庫進行測試——快速、隔離、無需外部依賴：

```rust
let pool = SqlitePool::connect("sqlite::memory:").await.unwrap();
init_db(&pool).await.unwrap();
// ... 插入測試資料 ...
let app = create_router(AppState { db: pool });
```

## 從這裡開始

1. **安裝依賴**：`cargo build`
2. **執行測試**：`cargo test`
3. **啟動服務**：`DATABASE_URL=sqlite:blog.db cargo run`
4. **測試 API**：`curl http://localhost:3000/api/posts`

## 延伸功能（挑戰題）

- 加入分頁查詢（LIMIT/OFFSET）
- 加入 JWT 認證
- 加入 PostgreSQL 支援
- 加入搜尋功能（LIKE 查詢）
- 加入 Redis 快取層
- 加入 Swagger/OpenAPI 文件

---

## 延伸閱讀

- [完整程式碼](_code/src/main.rs)
- [Axum 文件](https://www.google.com/search?q=Axum+Rust+web+framework+documentation)
- [SQLx 文件](https://www.google.com/search?q=SQLx+Rust+SQL+toolkit)
