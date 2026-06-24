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

// ─── Database Init ─────────────────────────────────────────────────

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

// ─── Router ────────────────────────────────────────────────────────

fn create_router(state: AppState) -> Router {
    Router::new()
        .route("/api/posts", get(list_posts).post(create_post))
        .route("/api/posts/{id}", get(get_post).put(update_post).delete(delete_post))
        .with_state(state)
}

// ─── Main ──────────────────────────────────────────────────────────

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt()
        .with_env_filter("miniblog=info,tower_http=info")
        .init();

    let database_url =
        std::env::var("DATABASE_URL").unwrap_or_else(|_| "sqlite::memory:".to_string());

    let pool = SqlitePool::connect(&database_url).await?;
    init_db(&pool).await?;

    let state = AppState { db: pool };
    let app = create_router(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    tracing::info!("miniblog listening on {}", listener.local_addr()?);
    axum::serve(listener, app).await?;

    Ok(())
}

// ─── Tests ─────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use axum::{
        body::Body,
        http::{Request, Method},
    };
    use tower::ServiceExt;

    async fn setup_test_app() -> Router {
        let pool = SqlitePool::connect("sqlite::memory:").await.unwrap();
        init_db(&pool).await.unwrap();

        // Seed data
        let id = Uuid::new_v4().to_string();
        sqlx::query("INSERT INTO posts (id, title, content, author, created_at) VALUES (?, ?, ?, ?, ?)")
            .bind(&id)
            .bind("Test Post")
            .bind("Test Content")
            .bind("Alice")
            .bind(&chrono::Utc::now().to_rfc3339())
            .execute(&pool)
            .await
            .unwrap();

        let state = AppState { db: pool };
        create_router(state)
    }

    #[tokio::test]
    async fn test_list_posts() {
        let app = setup_test_app().await;

        let response = app
            .oneshot(Request::builder().uri("/api/posts").body(Body::empty()).unwrap())
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = axum::body::to_bytes(response.into_body(), usize::MAX).await.unwrap();
        let list: PostList = serde_json::from_slice(&body).unwrap();
        assert!(list.total >= 1);
    }

    #[tokio::test]
    async fn test_create_post() {
        let app = setup_test_app().await;

        let body = serde_json::to_string(&CreatePost {
            title: "New Post".into(),
            content: "New Content".into(),
            author: "Bob".into(),
        })
        .unwrap();

        let response = app
            .oneshot(
                Request::builder()
                    .method(Method::POST)
                    .uri("/api/posts")
                    .header("content-type", "application/json")
                    .body(Body::from(body))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::CREATED);
    }

    #[tokio::test]
    async fn test_get_post_not_found() {
        let app = setup_test_app().await;

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/api/posts/nonexistent-id")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::NOT_FOUND);
    }

    #[tokio::test]
    async fn test_delete_post() {
        let pool = SqlitePool::connect("sqlite::memory:").await.unwrap();
        init_db(&pool).await.unwrap();
        let id = Uuid::new_v4().to_string();
        sqlx::query("INSERT INTO posts (id, title, content, author, created_at) VALUES (?, ?, ?, ?, ?)")
            .bind(&id)
            .bind("To Delete")
            .bind("")
            .bind("test")
            .bind(&chrono::Utc::now().to_rfc3339())
            .execute(&pool)
            .await
            .unwrap();
        let state = AppState { db: pool };
        let app = create_router(state);

        let response = app
            .oneshot(
                Request::builder()
                    .method(Method::DELETE)
                    .uri(&format!("/api/posts/{}", id))
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }
}
