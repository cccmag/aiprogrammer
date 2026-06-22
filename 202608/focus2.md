# Axum Web 框架

## 現代 Rust Web 框架的設計（2021-2026）

### 前言

Axum 是 Tokio 團隊開發的 Web 框架，於 2021 年 7 月首次發布。與其前輩（Actix Web、Rocket、Warp）不同，Axum 的設計理念是「**用 Rust 的型別系統來表達 Web 應用的結構**」。

### Axum 的核心設計

**Extractor（提取器）**：

Axum 最核心的創新是 Extractor 模式——HTTP 請求的各個部分通過 Rust 的 trait 系統來提取：

```rust
use axum::{extract::{Path, Query, Json}, http::StatusCode};
use serde::Deserialize;

#[derive(Deserialize)]
struct Pagination {
    page: Option<u32>,
    limit: Option<u32>,
}

// 提取器組合：路徑參數 + 查詢參數 + JSON 請求體
async fn create_post(
    Path(user_id): Path<u64>,
    Query(pagination): Query<Pagination>,
    Json(body): Json<CreatePost>,
) -> Result<Json<Post>, StatusCode> {
    // 編譯器保證所有提取都正確處理
    let post = Post::new(user_id, body).await?;
    Ok(Json(post))
}
```

每個提取器都是一個 trait，可以組合和自訂：

```rust
// 自訂提取器
struct AuthUser {
    id: u64,
    role: String,
}

impl<S> FromRequestParts<S> for AuthUser
where
    S: Send + Sync,
{
    type Rejection = StatusCode;

    async fn from_request_parts(
        parts: &mut http::request::Parts,
        state: &S,
    ) -> Result<Self, Self::Rejection> {
        // 從 Authorization header 解析用戶
        let token = parts
            .headers
            .get("Authorization")
            .and_then(|v| v.to_str().ok())
            .ok_or(StatusCode::UNAUTHORIZED)?;
        // ... 驗證 token
        Ok(AuthUser { id: 1, role: "admin".into() })
    }
}
```

**Responder（回應器）**：

類似地，回應也是通過 trait 來處理：

```rust
use axum::response::{IntoResponse, Json};
use serde::Serialize;

#[derive(Serialize)]
struct ApiResponse<T> {
    success: bool,
    data: Option<T>,
    error: Option<String>,
}

// 統一回應格式
impl<T: Serialize> IntoResponse for ApiResponse<T> {
    fn into_response(self) -> axum::response::Response {
        Json(self).into_response()
    }
}
```

### Axum vs 其他 Rust Web 框架

| 特性 | Axum | Actix Web | Rocket | Warp |
|------|------|-----------|--------|------|
| 非同步支援 | Tokio | Tokio/自建 | Tokio | Tokio |
| 型別安全路由 | ✅ 靜態路由 | ✅ | ✅ | 🟡 宏 |
| 中介軟體生態 | Tower | actix-web | Rocket | 自建 |
| 學習曲線 | 中等 | 中等 | 低 | 高（Filter） |
| Extractor 模式 | ✅ 核心 | 🟡 基礎 | ✅ Rocket | 🟡 基礎 |

### Tower 生態系統

Axum 建構在 Tower 生態之上——一個模組化的中介軟體框架：

```rust
use tower::ServiceBuilder;
use tower_http::{
    cors::CorsLayer,
    compression::CompressionLayer,
    trace::TraceLayer,
    limit::RequestBodyLimitLayer,
};

let middleware_stack = ServiceBuilder::new()
    .layer(TraceLayer::new_for_http())           // 日誌
    .layer(CompressionLayer::new())              // Gzip
    .layer(CorsLayer::permissive())              // CORS
    .layer(RequestBodyLimitLayer::new(1024 * 1024)) // 1MB 限制
    .into_inner();
```

Tower 的中介軟體像洋蔥一樣層層包裹：

```
請求 → Trace → CORS → Compression → 路由 → Handler → 回應
```

### Axum 0.10：WebSocket 與 SSE

2026 年發布的 Axum 0.10 引入了原生 WebSocket 和 SSE 支援：

```rust
// WebSocket
async fn ws_handler(
    ws: WebSocketUpgrade,
) -> Response {
    ws.on_upgrade(|mut socket| async move {
        while let Some(msg) = socket.recv().await {
            if let Ok(msg) = msg {
                socket.send(msg).await.unwrap();
            }
        }
    })
}

// Server-Sent Events
async fn sse_handler() -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let stream = async_stream::stream! {
        loop {
            yield Ok(Event::default().data("heartbeat"));
            tokio::time::sleep(Duration::from_secs(1)).await;
        }
    };
    Sse::new(stream)
}
```

### 路由設計

Axum 的路由是型別安全的——每個路由的 path 參數在編譯時就確定：

```rust
use axum::{
    routing::{get, post},
    Router,
};

let app = Router::new()
    .route("/api/posts", get(list_posts).post(create_post))
    .route("/api/posts/{id}", get(get_post).put(update_post).delete(delete_post))
    .route("/api/posts/{id}/comments", get(list_comments).post(create_comment))
    .with_state(AppState::new());
```

### 狀態管理

```rust
#[derive(Clone)]
struct AppState {
    db: Pool<Postgres>,
    cache: redis::aio::ConnectionManager,
    config: Arc<AppConfig>,
}

let app = Router::new()
    .route("/api/posts", get(list_posts))
    .with_state(app_state);

// 在 handler 中取出狀態
async fn list_posts(
    State(state): State<AppState>,
) -> Result<Json<Vec<Post>>, AppError> {
    let posts = state.db.get_posts().await?;
    Ok(Json(posts))
}
```

### 實戰範例：完整的 CRUD API

```rust
async fn create_post(
    State(db): State<Pool<Postgres>>,
    Json(input): Json<CreatePost>,
) -> Result<(StatusCode, Json<Post>), AppError> {
    let post = sqlx::query_as!(
        Post,
        "INSERT INTO posts (title, content) VALUES ($1, $2) RETURNING *",
        input.title, input.content
    )
    .fetch_one(&db)
    .await?;
    
    Ok((StatusCode::CREATED, Json(post)))
}
```

### Axum 的生產力優勢

與其他語言的 Web 框架相比，Axum 提供的生產力：

- **Rust 的型別安全**：路由參數、請求體、回應格式全部編譯期檢查
- **Tower 生態**：數十個預建的中介軟體
- **OpenAPI 整合**：自動生成 API 文件（utoipa）
- **測試友善**：內建 TestServer

### 小結

Axum 代表了 Rust Web 框架設計的最新成就。它用 Rust 的型別系統來表達 Web 應用的結構——路由、參數、狀態、中介軟體——讓編譯器幫助開發者發現錯誤。結合 Tokio 和 Tower 生態，Axum 提供了一個既安全又高效的 Web 開發體驗。

---

**下一步**：[SQLx 資料庫存取](focus3.md)

## 延伸閱讀

- [Axum 官方文件](https://www.google.com/search?q=Axum+Rust+web+framework)
- [Tower 中介軟體生態](https://www.google.com/search?q=Tower+Rust+middleware)
- [Axum 實戰教學](https://www.google.com/search?q=Axum+Rust+tutorial)
