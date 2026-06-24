# 完整 Web 服務

## 從 API 設計到部署的實戰指南（2024-2026）

### 前言

前面幾篇分別介紹了 Tokio、Axum、SQLx、SeaORM 和 Redis。本篇將整合這些套件，展示如何建構一個完整的生產級 Web 服務。

### 專案結構

一個成熟的 Rust Web 服務應該有清晰的層級劃分：

```
my-api/
├── Cargo.toml
├── src/
│   ├── main.rs          # 應用入口
│   ├── lib.rs           # 模組匯出
│   ├── config.rs        # 環境設定
│   ├── router.rs        # 路由定義
│   ├── handlers/        # 請求處理器
│   │   ├── mod.rs
│   │   ├── posts.rs
│   │   └── users.rs
│   ├── models/          # 資料模型
│   │   ├── mod.rs
│   │   └── post.rs
│   ├── repositories/    # 資料存取層
│   │   ├── mod.rs
│   │   └── post_repo.rs
│   ├── services/        # 業務邏輯層
│   │   ├── mod.rs
│   │   └── post_service.rs
│   └── middleware/       # 中介軟體
│       ├── mod.rs
│       └── auth.rs
├── migrations/          # 資料庫遷移
├── tests/              # 整合測試
└── Dockerfile          # 部署設定
```

### 錯誤處理

統一的錯誤處理是 API 設計的關鍵：

```rust
// 統一的 API 錯誤
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("Not found: {0}")]
    NotFound(String),
    
    #[error("Unauthorized")]
    Unauthorized,
    
    #[error("Validation error: {0}")]
    Validation(String),
    
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    
    #[error("Internal error: {0}")]
    Internal(String),
}

// 自動轉換為 HTTP 回應
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg.clone()),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "Unauthorized".into()),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg.clone()),
            AppError::Database(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Database error".into()),
            AppError::Internal(msg) => (StatusCode::INTERNAL_SERVER_ERROR, msg.clone()),
        };
        
        Json(ErrorResponse {
            error: message,
            status: status.as_u16(),
        }).into_response()
    }
}
```

### 認證與授權（JWT）

```rust
use jsonwebtoken::{encode, decode, Header, Validation, EncodingKey, DecodingKey};
use serde::{Serialize, Deserialize};
use chrono::{Utc, Duration};

#[derive(Debug, Serialize, Deserialize)]
pub struct Claims {
    pub sub: String,    // user email
    pub exp: usize,     // expiration
    pub iat: usize,     // issued at
    pub role: String,   // user role
}

pub struct JwtService {
    secret: String,
}

impl JwtService {
    pub fn create_token(&self, email: &str, role: &str) -> Result<String, AppError> {
        let now = Utc::now();
        let claims = Claims {
            sub: email.to_string(),
            exp: (now + Duration::hours(24)).timestamp() as usize,
            iat: now.timestamp() as usize,
            role: role.to_string(),
        };
        
        encode(
            &Header::default(), 
            &claims, 
            &EncodingKey::from_secret(self.secret.as_bytes())
        ).map_err(|e| AppError::Internal(e.to_string()))
    }
}
```

### 依賴注入與狀態管理

```rust
// 應用狀態
#[derive(Clone)]
pub struct AppState {
    pub db: PgPool,
    pub cache: ConnectionManager,
    pub jwt: Arc<JwtService>,
    pub config: Arc<AppConfig>,
}

// 在 main 中初始化
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = AppConfig::from_env()?;
    
    let db = PgPoolOptions::new()
        .max_connections(100)
        .connect(&config.database_url)
        .await?;
    
    let redis_client = redis::Client::open(&config.redis_url)?;
    let cache = ConnectionManager::new(redis_client).await?;
    
    let state = AppState {
        db,
        cache,
        jwt: Arc::new(JwtService::new(&config.jwt_secret)),
        config: Arc::new(config),
    };
    
    // 運行 migration
    sqlx::migrate!().run(&state.db).await?;
    
    // 啟動服務
    let app = create_router(state);
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    axum::serve(listener, app).await?;
    
    Ok(())
}
```

### Repository 模式

```rust
// 資料存取層
pub struct PostRepository {
    db: PgPool,
}

impl PostRepository {
    pub async fn find_all(&self, page: u32, limit: u32) -> Result<Vec<Post>, AppError> {
        let offset = (page - 1) * limit;
        Ok(sqlx::query_as!(
            Post,
            "SELECT * FROM posts ORDER BY created_at DESC LIMIT $1 OFFSET $2",
            limit as i64,
            offset as i64,
        )
        .fetch_all(&self.db)
        .await?)
    }
    
    pub async fn find_by_id(&self, id: u64) -> Result<Post, AppError> {
        sqlx::query_as!(
            Post,
            "SELECT * FROM posts WHERE id = $1",
            id as i64,
        )
        .fetch_optional(&self.db)
        .await?
        .ok_or_else(|| AppError::NotFound(format!("Post {} not found", id)))
    }
}
```

### 路由與 Handler

```rust
pub fn create_router(state: AppState) -> Router {
    Router::new()
        // 公開路由
        .route("/api/login", post(login))
        .route("/api/register", post(register))
        // 需要認證的路由
        .route("/api/posts", get(list_posts).post(create_post))
        .route("/api/posts/{id}", get(get_post).put(update_post).delete(delete_post))
        // 管理員路由
        .route("/api/admin/users", get(list_users).delete(delete_user))
        // 中介軟體
        .layer(middleware_stack)
        // 狀態
        .with_state(state)
}

// Handler 範例
async fn list_posts(
    State(state): State<AppState>,
    Query(pagination): Query<PaginationParams>,
) -> Result<Json<PaginatedResponse<Post>>, AppError> {
    let posts = state.post_repo.find_all(pagination.page, pagination.limit).await?;
    let total = state.post_repo.count_all().await?;
    
    Ok(Json(PaginatedResponse {
        data: posts,
        page: pagination.page,
        limit: pagination.limit,
        total,
    }))
}
```

### 中介軟體鏈

```rust
// 認證中介軟體
async fn auth_middleware(
    mut req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let token = req.headers()
        .get("Authorization")
        .and_then(|v| v.to_str().ok())
        .and_then(|v| v.strip_prefix("Bearer "))
        .ok_or(StatusCode::UNAUTHORIZED)?;
    
    let claims = validate_token(token).map_err(|_| StatusCode::UNAUTHORIZED)?;
    req.extensions_mut().insert(claims);
    
    Ok(next.run(req).await)
}

// Tower 中介軟體組合
let middleware_stack = ServiceBuilder::new()
    .layer(TraceLayer::new_for_http())
    .layer(CorsLayer::permissive())
    .layer(CompressionLayer::new())
    .layer(from_fn(auth_middleware))
    .into_inner();
```

### 測試

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use axum::{
        body::Body,
        http::{Request, StatusCode},
    };
    use tower::ServiceExt;
    
    #[tokio::test]
    async fn test_create_post() {
        let state = create_test_state().await;
        let app = create_router(state);
        
        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/posts")
                    .header("Content-Type", "application/json")
                    .body(Body::from(r#"{"title":"Test","content":"Test"}"#))
                    .unwrap(),
            )
            .await
            .unwrap();
        
        assert_eq!(response.status(), StatusCode::CREATED);
    }
}
```

### 部署

```dockerfile
# Dockerfile（多階段建置）
FROM rust:latest AS builder
WORKDIR /app
COPY . .
RUN cargo build --release --bin my-api

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates
COPY --from=builder /app/target/release/my-api /usr/local/bin/
CMD ["my-api"]
```

**環境變數設定**：

```bash
# .env
DATABASE_URL=postgres://user:pass@localhost/db
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
RUST_LOG=info
SERVER_HOST=0.0.0.0
SERVER_PORT=3000
```

### 效能與監控

```rust
// Prometheus 指標
use metrics::{counter, histogram};

async fn track_request(handler: impl Handler) -> impl Handler {
    move |req: Request| {
        let start = std::time::Instant::now();
        
        async move {
            let response = handler.call(req).await;
            let duration = start.elapsed();
            
            counter!("http_requests_total", 1);
            histogram!("http_request_duration", duration);
            
            response
        }
    }
}
```

### 小結

完整的 Rust Web 服務不僅僅是路由和 Handler——它涉及錯誤處理、認證、測試、部署、監控等多個層面。Tokio + Axum + SQLx + Redis 的組合提供了一個完整的解決方案，涵蓋了從開發到生產的全流程。

**下一步**：[AI + Rust Web 開發](focus7.md)

## 延伸閱讀

- [Axum 生產部署指南](https://www.google.com/search?q=Axum+production+deployment)
- [Rust Web API 測試](https://www.google.com/search?q=Rust+web+API+testing)
- [Rust 微服務架構](https://www.google.com/search?q=Rust+microservices+architecture)
