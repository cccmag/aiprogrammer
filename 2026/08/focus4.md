# ORM 框架比較

## SeaORM、Diesel、Prisma 的選擇（2018-2026）

### ORM 的必要性

當專案複雜度增加時，直接使用 SQL（如 SQLx）會面臨一些挑戰：

```rust
// 複雜關聯查詢：SQLx 需要手動處理
let user = sqlx::query_as!(
    UserWithPosts,
    r#"
    SELECT u.*, p.id as post_id, p.title, p.content
    FROM users u
    LEFT JOIN posts p ON p.user_id = u.id
    WHERE u.id = $1
    "#,
    user_id
)
.fetch_all(&pool)
.await?;

// ORM：聲明式關聯載入
let user = User::find_by_id(user_id)
    .find_with_related(Post)
    .all(&db)
    .await?;
```

ORM（Object-Relational Mapping）框架在複雜的資料操作中提供了更高的生產力。

### Diesel：同步 ORM 的穩定性

Diesel 是 Rust 最成熟的 ORM 框架，2018 年首次發布：

```rust
// Diesel Schema（自動生成）
table! {
    posts (id) {
        id -> Integer,
        title -> Varchar,
        body -> Text,
        published -> Bool,
        created_at -> Timestamp,
    }
}

// Diesel 查詢
let posts = posts::table
    .filter(posts::published.eq(true))
    .order(posts::created_at.desc())
    .limit(10)
    .load::<Post>(&mut connection)?;
```

**Diesel 的優點**：
- 最成熟的 Rust ORM（2018 年至今）
- 自動 Schema 生成（from database）
- 編譯期查詢檢查
- 豐富的文件和社群
- Migration DSL

**Diesel 的缺點**：
- **同步為主**：非同步支援較晚且不夠完善
- **自訂 DSL**：需要學習 Diesel 特有的查詢語法
- **複雜關聯**：多對多關聯較難處理
- **編譯時間**：複雜查詢會增加編譯時間

### SeaORM：非同步 ORM 的靈活性

SeaORM 是 2022 年崛起的新興 ORM，專為非同步而生：

```rust
use sea_orm::*;
use entity::{post, user};

// 建立關聯查詢
let user_with_posts = User::find_by_id(user_id)
    .find_with_related(Post)
    .all(&db)
    .await?;

// 複雜查詢
let posts = Post::find()
    .filter(post::Column::Published.eq(true))
    .filter(post::Column::CreatedAt.gte(since_date))
    .order_by_desc(post::Column::CreatedAt)
    .paginate(&db, page_size)
    .fetch_page(page_num)
    .await?;

// 交易
db.transaction::<_, DbErr, _>(|txn| {
    Box::pin(async move {
        let user = user::ActiveModel {
            name: Set("Alice".to_owned()),
            ..Default::default()
        };
        let user = user.insert(txn).await?;
        Ok(())
    })
}).await?;
```

**SeaORM 的優點**：
- **原生非同步**：基於 SQLx，使用 Tokio
- **熟悉的 API**：類似 TypeORM/ActiveRecord
- **關聯查詢**：支援 eager/lazy loading
- **Migration**：支援自動和手動 migration
- **類型安全**：與 Rust 型別系統良好整合

**SeaORM 的缺點**：
- **較年輕**：生態不如 Diesel 成熟
- **額外抽象**：效能略低於直接使用 SQLx
- **學習曲線**：需要理解 Active Record 模式

### Prisma：Schema-first 的選擇

Prisma 最初是 TypeScript 的 ORM，2024 年推出了 Rust 原生版本 `prisma-rust`：

```prisma
// Prisma Schema
model User {
  id    Int     @id @default(autoincrement())
  name  String
  email String  @unique
  posts Post[]
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
}
```

```rust
// Prisma Client（自動生成）
let user = client
    .user()
    .find_unique(user::id::equals(1))
    .with(user::posts::fetch(vec![]))
    .exec()
    .await?;
```

**Prisma 的優點**：
- **Schema-first**：資料模型清晰可見
- **自動 Client 生成**：型別安全
- **跨語言**：同一個 Schema 可在 TypeScript/Rust 間共享
- **管理介面**：Prisma Studio 圖形化管理

**Prisma 的缺點**：
- **生成步驟**：每次 Schema 變更需要重新生成 Client
- **靈活性**：複雜查詢不如手寫 SQL
- **依賴**：需要 Node.js 執行環境
- **Rust 生態**：仍在發展中，不如 SeaORM/Diesel 成熟

### 選擇指南

| 專案類型 | 推薦方案 | 原因 |
|---------|---------|------|
| 小型 API、少量表格 | SQLx | 最簡單，無需 ORM 開銷 |
| 中型專案、複雜 CRUD | SeaORM | 非同步 + 類型安全 |
| 大型專案、重關聯查詢 | Diesel | 最成熟，生態最豐富 |
| 跨語言團隊 | Prisma | Schema 共享 |
| 高效能、大量資料 | SQLx | 直接 SQL 的最佳化空間最大 |
| 微服務 | SQLx + 小型模型 | 避免 ORM 的複雜性 |

### 何時不該使用 ORM？

```rust
// ORM 不適合的場景
// 1. 複雜報表查詢
let result = sqlx::query!(
    r#"
    SELECT 
        DATE_TRUNC('month', created_at) as month,
        COUNT(*) as total,
        SUM(amount) as revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_TRUNC('month', created_at)
    ORDER BY month
    "#
)
.fetch_all(&pool)
.await?;

// 2. 大量批次操作
let mut tx = pool.begin().await?;
for batch in records.chunks(1000) {
    sqlx::query("INSERT INTO logs (message, level) VALUES ($1, $2)")
        .bind(batch)
        .execute(&mut *tx)
        .await?;
}
tx.commit().await?;
```

### Rust ORM 的未來

1. **SeaORM 將成為主流**：非同步支援 + 熟悉的 API 使其最適合 Web 開發
2. **Diesel 的非同步化**：Diesel 團隊正在開發 3.0，重點是非同步支援
3. **編譯期檢查的普及**：更多的型別安全檢查將被引入 ORM
4. **AI 生成的整合**：AI 可以自動從自然語言生成 ORM 操作程式碼

### 小結

選擇 ORM 還是直接使用 SQL，取決於專案的具體需求：

- **想要最大控制力？** 用 SQLx
- **想要最大的生產力？** 用 SeaORM
- **想要最大的穩定性？** 用 Diesel
- **想要跨語言共享模型？** 用 Prisma

無論選擇哪種方案，Rust 的型別系統都確保了資料庫操作的安全性——比起動態語言中的 ORM，Rust 的 ORM 在編譯期檢查方面具有本質優勢。

---

**下一步**：[Redis 整合](focus5.md)

## 延伸閱讀

- [SeaORM 官方文件](https://www.google.com/search?q=SeaORM+Rust+documentation)
- [Diesel 官方指南](https://www.google.com/search?q=Diesel+Rust+ORM+guide)
- [Prisma Rust](https://www.google.com/search?q=Prisma+Rust)
