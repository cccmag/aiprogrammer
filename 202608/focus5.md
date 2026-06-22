# Redis 整合

## 快取、工作佇列與會話管理（2017-2026）

### 前言

Redis 是現代 Web 服務的核心元件。它不僅僅是一個快取——它還是工作佇列、會話儲存、速率限制器和發布/訂閱系統。Rust 生態中的 `redis-rs` 程式庫提供了一個安全且高效的非同步 Redis 用戶端。

### redis-rs 用戶端

`redis-rs` 是 Rust 生態中最流行的 Redis 用戶端，2024 年新增了完整的非同步支援：

```rust
use redis::aio::ConnectionManager;
use redis::AsyncCommands;

// 建立連線管理器
let client = redis::Client::open("redis://127.0.0.1:6379")?;
let mut conn = ConnectionManager::new(client).await?;

// 基本操作
conn.set("key", "value").await?;
let value: String = conn.get("key").await?;

// 過期時間
conn.set_ex("session:token", "user_data", 3600).await?; // 1 小時過期

// 原子操作
let count: i64 = conn.incr("visitor_count", 1).await?;
```

### 連線池與連線管理器

與直接建立連線不同，生產環境應該使用 Connection Manager：

```rust
use redis::aio::ConnectionManager;
use redis::cluster::ClusterClient;

// 單例模式：Connection Manager 自動處理重連
let manager = ConnectionManager::new(client).await?;

// Redis Cluster
let nodes = vec![
    "redis://127.0.0.1:7000",
    "redis://127.0.0.1:7001",
    "redis://127.0.0.1:7002",
];
let cluster_client = ClusterClient::new(nodes)?;

// 使用 Clone 在任務間共享
let shared_manager = manager.clone();
tokio::spawn(async move {
    shared_manager.set("key", "value").await.unwrap();
});
```

### 快取策略

**Cache-Aside 模式**：

```rust
async fn get_user(db: &Pool, cache: &mut ConnectionManager, id: u64) -> Result<User, Error> {
    // 1. 先檢查快取
    let cache_key = format!("user:{}", id);
    if let Some(user) = cache.get::<_, Option<String>>(&cache_key).await? {
        return Ok(serde_json::from_str(&user)?);
    }
    
    // 2. 快取未命中，查詢資料庫
    let user = sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1", id)
        .fetch_one(db)
        .await?;
    
    // 3. 寫入快取
    let json = serde_json::to_string(&user)?;
    cache.set_ex(&cache_key, json, 300).await?; // 5 分鐘過期
    
    Ok(user)
}
```

**Cache Invalidation**：

```rust
// 更新用戶時使快取失效
async fn update_user(
    db: &Pool, 
    cache: &mut ConnectionManager, 
    id: u64, 
    name: &str
) -> Result<User, Error> {
    let user = sqlx::query_as::<_, User>(
        "UPDATE users SET name = $1 WHERE id = $2 RETURNING *",
        name, id
    )
    .fetch_one(db)
    .await?;
    
    // 使快取失效（也可以更新快取）
    let cache_key = format!("user:{}", id);
    cache.del(&cache_key).await?;
    
    Ok(user)
}
```

### 工作佇列

使用 Redis List 來實現簡單的工作佇列：

```rust
// 生產者
async fn enqueue_job(conn: &mut ConnectionManager, job: Job) -> Result<(), Error> {
    let json = serde_json::to_string(&job)?;
    conn.rpush::<_, _, i64>("job_queue", &json).await?;
    Ok(())
}

// 消費者
async fn process_jobs(conn: &mut ConnectionManager) -> Result<(), Error> {
    loop {
        // BLPop：阻塞式彈出，沒有任務時等待
        let result: Option<String> = conn.blpop("job_queue", 0.0).await?;
        
        if let Some((_, json)) = result {
            if let Ok(job) = serde_json::from_str::<Job>(&json) {
                process_job(job).await;
            }
        }
    }
}
```

**進階工作佇列（使用 rsmq）**：

```rust
use rsmq_async::Rsmq;

let rsmq = Rsmq::new(redis_url).await?;
rsmq.create_queue("email_queue", None, None).await?;

// 發送訊息
rsmq.send_message("email_queue", json, None).await?;

// 接收訊息
let msg = rsmq.receive_message::<EmailPayload>("email_queue", None).await?;
```

### Pub/Sub 模式

```rust
use redis::aio::ConnectionManager;
use redis::AsyncCommands;

// 發布者
async fn publish_event(conn: &mut ConnectionManager, event: Event) {
    let json = serde_json::to_string(&event).unwrap();
    conn.publish::<_, _, i64>("events", json).await.unwrap();
}

// 訂閱者
async fn subscribe_events(conn: &mut ConnectionManager) {
    let mut pubsub = conn.as_pubsub().await.unwrap();
    pubsub.subscribe("events").await.unwrap();
    
    loop {
        let msg = pubsub.next_message().await.unwrap();
        let payload: String = msg.get_payload().unwrap();
        println!("Event: {}", payload);
    }
}
```

### 會話管理

```rust
use axum::extract::FromRequestParts;
use redis::aio::ConnectionManager;

// 使用 Redis 儲存會話
struct Session {
    user_id: u64,
    token: String,
}

async fn create_session(conn: &mut ConnectionManager, user_id: u64) -> Result<String, Error> {
    let token = uuid::Uuid::new_v4().to_string();
    let session = Session { user_id, token: token.clone() };
    let json = serde_json::to_string(&session)?;
    
    // 會話儲存在 Redis，1 小時過期
    conn.set_ex(&format!("session:{}", token), json, 3600).await?;
    
    Ok(token)
}

// 驗證會話
async fn validate_session(conn: &mut ConnectionManager, token: &str) -> Option<Session> {
    let key = format!("session:{}", token);
    let json: Option<String> = conn.get(&key).await.ok().flatten();
    
    if let Some(json) = json {
        if let Ok(session) = serde_json::from_str::<Session>(&json) {
            // 延長過期時間
            conn.expire(&key, 3600).await.ok();
            return Some(session);
        }
    }
    None
}
```

### 速率限制

```rust
// 滑動視窗速率限制
async fn check_rate_limit(
    conn: &mut ConnectionManager, 
    user_id: u64, 
    limit: u32, 
    window_secs: u64
) -> Result<bool, Error> {
    let key = format!("ratelimit:{}", user_id);
    let now = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_secs();
    let window_start = now - window_secs;
    
    // 使用 Redis 有序集合實現滑動視窗
    let count: i64 = redis::cmd("ZCOUNT")
        .arg(&key)
        .arg(window_start)
        .arg(now)
        .query_async(conn)
        .await?;
    
    if count >= limit as i64 {
        return Ok(false); // 超出限制
    }
    
    // 記錄此次請求
    let _: i64 = redis::cmd("ZADD")
        .arg(&key)
        .arg(now)
        .arg(now)
        .query_async(conn)
        .await?;
    
    // 設定過期時間，自動清理
    let _: i64 = conn.expire(&key, window_secs * 2).await?;
    
    Ok(true)
}
```

### 效能比較

| 操作 | 直接 DB（PostgreSQL） | Redis 快取 | 加速比 |
|------|---------------------|-----------|--------|
| 讀取單筆記錄 | 3-5ms | <1ms | 5-10x |
| 讀取 100 筆 | 10-20ms | 1-2ms | 10x |
| 寫入單筆記錄 | 5-10ms | <1ms | 5-10x |
| 計數器原子操作 | 5ms (SELECT + UPDATE) | <0.5ms | 10x+ |

### 小結

Redis 是現代 Web 服務的「瑞士軍刀」——它不僅僅是一個快取，還是工作佇列、會話管理和速率限制的核心元件。Rust 的 redis-rs 程式庫提供了安全、高效的非同步介面，與 Tokio/Axum 生態完美整合。

**最佳實踐**：
1. 使用 Connection Manager 而非原始連線
2. 快取時設定合理的 TTL
3. 寫入時考慮快取失效策略
4. 使用 Pipeline 減少網路往返
5. 監控 Redis 記憶體使用和命中率

---

**下一步**：[完整 Web 服務](focus6.md)

## 延伸閱讀

- [redis-rs 文件](https://www.google.com/search?q=redis-rs+Rust+documentation)
- [Redis 快取策略](https://www.google.com/search?q=Redis+caching+strategies)
- [Rust + Redis 實戰](https://www.google.com/search?q=Rust+Redis+production+tips)
