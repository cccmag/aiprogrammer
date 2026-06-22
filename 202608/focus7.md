# AI + Rust Web 開發

## AI 輔助建立全端應用（2025-2026）

### 前言

AI 輔助開發已經從「生成程式碼片段」進化到「從自然語言到完整應用」。本期焦點的主題——Tokio + Axum + SQLx 生態——是 AI 輔助 Rust 開發的完美場景，因為這些套件的 API 設計一致且慣例明確。

### AI 如何輔助 Rust Web 開發

#### 1. 從自然語言到專案骨架

開發者描述需求，AI 自動生成完整的專案結構：

```
提示：Create a Rust web service with Axum + SQLx + PostgreSQL
- POST /api/posts - create a post
- GET /api/posts - list posts (paginated)
- GET /api/posts/{id} - get post by id
- PUT /api/posts/{id} - update post
- DELETE /api/posts/{id} - delete post
- JWT authentication

AI 生成的結果：
├── Cargo.toml（依賴全部正確）
├── src/main.rs（Tokio runtime + Axum router）
├── src/models/post.rs（結構體 + SQLx 映射）
├── src/handlers/posts.rs（5 個 CRUD handler）
├── src/auth/jwt.rs（Token 生成與驗證）
├── src/middleware/auth.rs（Axum 中介軟體）
├── migrations/（SQL migration 檔案）
└── tests/api_tests.rs（HTTP 整合測試）
```

#### 2. AI 自動生成 CRUD 程式碼

Rust Web 開發中最常見的任務——CRUD——AI 可以全自動生成：

```rust
// AI 生成的 Handler（以 Axum 的慣例風格）
async fn create_post(
    State(state): State<AppState>,
    AuthUser(user): AuthUser,
    Json(input): Json<CreatePost>,
) -> Result<(StatusCode, Json<Post>), AppError> {
    let post = sqlx::query_as!(
        Post,
        "INSERT INTO posts (title, content, author_id) 
         VALUES ($1, $2, $3) RETURNING *",
        input.title,
        input.content,
        user.id,
    )
    .fetch_one(&state.db)
    .await?;
    
    // 使快取失效
    state.cache.del("posts:list").await?;
    
    Ok((StatusCode::CREATED, Json(post)))
}
```

#### 3. 資料庫 Schema 設計

開發者用自然語言描述資料需求，AI 生成 SQL migration：

```
提示：Design a database for a blog with users, posts, comments, and tags.
Each user can have many posts, each post can have many comments and many tags.

AI 生成的 migration：
```

```sql
-- 20260801000001_create_users.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 20260801000002_create_posts.sql
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 20260801000003_create_comments.sql
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    post_id UUID NOT NULL REFERENCES posts(id),
    author_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 20260801000004_create_tags.sql
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
    post_id UUID NOT NULL REFERENCES posts(id),
    tag_id UUID NOT NULL REFERENCES tags(id),
    PRIMARY KEY (post_id, tag_id)
);
```

#### 4. 除錯與最佳化

當 Rust 編譯器報錯時，AI 可以分析錯誤並提供修復：

```
錯誤：error[E0277]: the trait bound `AppError: IntoResponse` is not satisfied

AI 分析：AppError 沒有實作 IntoResponse trait，
需要在 AppError 上實作 IntoResponse（或使用 axum::response::IntoResponse）

AI 提供的修復：
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            AppError::NotFound(m) => (StatusCode::NOT_FOUND, m.clone()),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "Unauthorized".into()),
            AppError::Internal(m) => (StatusCode::INTERNAL_SERVER_ERROR, m.clone()),
        };
        Json(json!({ "error": message })).into_response()
    }
}
```

### 實戰案例：用 AI 建構部落格 API

以下是使用 AI（OpenCode）從零開始建構部落格 API 的記錄：

**Step 1: 初始化專案**

```bash
$ opencode "Create a new Rust project called blog-api with Axum, SQLx, and JWT auth"
```

AI 生成 Cargo.toml、專案結構和基礎程式碼。

**Step 2: 設計資料模型**

```bash
$ opencode "Add User and Post models with SQLx compile-time checking"
```

AI 生成 models 模組和對應的 SQL migration。

**Step 3: 實作 API**

```bash
$ opencode "Implement CRUD handlers for posts with pagination and JWT auth middleware"
```

AI 生成 handlers、middleware 和 router。

**Step 4: 測試**

```bash
$ opencode "Generate integration tests for all API endpoints"
```

AI 生成完整的測試套件。

**Step 5: 除錯**

```bash
$ cargo check  # 編譯器報錯
$ opencode "Fix compilation errors"
```

AI 分析錯誤並修復所有編譯問題。

### AI + Rust Web 開發的優勢

**1. Rust 的型別系統讓 AI 更容易「理解」程式碼**

與動態語言不同，Rust 的型別系統提供了明確的合約——AI 可以精確知道每個函式的輸入和輸出型別：

```rust
// AI 可以根據型別簽名推斷函式的行為
async fn get_post(
    State(db): State<PgPool>,  // 型別告訴 AI 這是資料庫連線
    Path(id): Path<Uuid>,      // 型別告訴 AI 這是路徑參數
) -> Result<Json<Post>, AppError> {
    // AI 知道需要查詢資料庫，返回 Post 或錯誤
}
```

**2. 編譯器是 AI 的安全網**

AI 生成的 Rust 程式碼會經過編譯器檢查——記憶體安全、型別安全、非同步正確性。這意味著 AI 的錯誤不會偷偷潛入生產環境。

**3. 慣例驅動開發**

Axum、SQLx、SeaORM 等框架有清晰的慣例——Extractor/Responder 模式、Repository 模式、Service 層。AI 可以學習這些模式並自動應用。

### AI 輔助開發的局限性

**1. 理解業務邏輯**

AI 擅長生成 CRUD 程式碼，但對於複雜的業務邏輯（如多步驟交易、狀態機轉換）需要人類的指導。

**2. 安全性考量**

AI 生成的認證/授權程式碼需要人類審查——SQL 注入（雖然 SQLx 已經防止）、JWT 簽名、密碼雜湊等。

**3. 架構決策**

大型應用的架構設計（微服務 vs 單體、CQRS、事件溯源）需要人類的經驗。

### 未來展望

1. **AI + Rust Web 開發將成為常態**：生成 CRUD、測試、文件的效率提升 10x
2. **從 REST 到完整產品**：AI 不僅生成 API，還能生成前端、部署配置、監控面板
3. **AI 驅動的架構演進**：AI 可以分析應用效能並建議架構改進
4. **Rust 專屬的 AI 模型**：針對 Rust 生態（Tokio、Axum、SQLx）微調的 AI 模型

### 小結

AI + Rust 的組合是 Web 開發的理想選擇——AI 提供生產力，Rust 提供安全性。開發者從「寫程式碼的人」轉變為「指導 AI 的人」，專注於業務邏輯和架構設計，而不是 CRUD 樣板程式碼。

這不僅僅是效率的提升，更是開發模式的變革——**從手動編寫到 AI 協作，從執行時期錯誤到編譯期保證**。

---

## 延伸閱讀

- [OpenCode - AI for Rust](https://opencode.ai)
- [Axum + SQLx 實戰教學](https://www.google.com/search?q=Axum+SQLx+tutorial+2026)
- [AI 輔助資料庫設計](https://www.google.com/search?q=AI+database+design+tools)
