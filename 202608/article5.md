# Rust 微服務架構最佳實踐

## 前言

微服務架構已成為現代後端系統的主流風格，而 Rust 憑藉其零成本抽象、所有權模型與靜態編譯特性，正在這個領域快速崛起。本文將從實戰角度出發，探討如何使用 Rust 生態系中的 Tokio、Axum、Tonic 等工具，建構生產級的微服務系統。

## 1. 為什麼 Rust 適合微服務

### 效能與資源效率

Rust 編譯為原生機器碼，無 GC 暫停開銷，在同等硬體下可比 Go 或 Java 節省 40-60% 的記憶體用量。對於需要密集啟動與縮放的容器化部署，這意味著更低的基礎設施成本。

### 編譯期安全性

所有權系統在編譯階段消滅了資料競爭（data race）與空指標解引用。在微服務的分散式環境中，執行期錯誤的排查成本極高，Rust 能將大量潛在錯誤提前到編譯期捕捉。

### 靜態連結與單一二進位

Rust 專案可編譯為靜態連結的單一二進位檔案，無需依賴特定版本的 libc 或執行期環境。這使得 Docker 映像可以基於 `scratch` 或 `alpine`，映像大小常控制在 10MB 以內，大幅減少攻擊面。

```dockerfile
# 多階段建置範例
FROM rust:1.85-slim-bookworm AS builder
WORKDIR /app
COPY . .
RUN cargo build --release --bin user-service

FROM gcr.io/distroless/cc-debian12
COPY --from=builder /app/target/release/user-service /app/
CMD ["/app/user-service"]
```

## 2. 服務拆分策略與模組劃分

### 依據領域邊界拆分

微服務拆分的核心原則是「領域驅動設計」（DDD）中的有界上下文（Bounded Context）。一個典型的電子商務系統可拆分為：

- **user-service**：使用者註冊、認證、權限
- **product-service**：商品目錄、庫存
- **order-service**：訂單建立、狀態管理
- **payment-service**：金流處理
- **notification-service**：電子郵件、推播通知

### Rust 工作空間（Workspace）組織

使用 Cargo workspace 管理多個服務的共享程式碼：

```
monorepo/
├── Cargo.toml          # [workspace]
├── libs/
│   ├── common/          # 共享型別、錯誤定義
│   ├── proto/           # protobuf 定義與生成的 stub
│   └── tracing-utils/   # 可觀測性基礎設施
├── services/
│   ├── user-service/
│   ├── order-service/
│   └── gateway/
└── docker-compose.yml
```

共享函式庫應保持輕量，避免服務間產生隱式耦合。proto 目錄集中管理 gRPC 的 `.proto` 檔案，並透過 build script 自動生成 Rust 程式碼。

## 3. 服務間通訊

### gRPC（Tonic）

Tonic 是 Rust 生態中最成熟的 gRPC 框架，基於 Tokio 與 hyper 建構。適用於需要嚴格型別合約與高效序列化的內部服務通訊。

```rust
// proto/user.proto
service UserService {
    rpc GetUser (GetUserRequest) returns (User);
}

// 服務端實作
#[tonic::async_trait]
impl UserService for UserServiceImpl {
    async fn get_user(
        &self,
        request: Request<GetUserRequest>,
    ) -> Result<Response<User>, Status> {
        let id = request.into_inner().user_id;
        let user = self.repository.find_by_id(id).await?;
        Ok(Response::new(user))
    }
}
```

### HTTP（Axum）

Axum 以其模組化設計與提取器（extractor）機制成為 Rust 當今最受歡迎的 Web 框架。適合對外 API 以及不需要嚴格合約的內部通訊。

```rust
use axum::{Router, extract::Path, Json};
use serde::Deserialize;

async fn get_user(Path(id): Path<Uuid>) -> Json<User> {
    // ...
}

let app = Router::new()
    .route("/users/:id", axum::routing::get(get_user));
```

### Message Queue

非同步通訊（事件驅動）使用訊息佇列如 RabbitMQ（lapin 套件）或 Kafka（rdkafka 套件）。適用於訂單建立後觸發通知、發票開立等不需即時回應的流程。

```rust
use lapin::{Connection, ConnectionProperties, BasicProperties};
use tokio_amqp::LapinTokioExt;

let conn = Connection::connect(
    "amqp://guest:guest@rabbitmq:5672/%2f",
    ConnectionProperties::default().with_tokio(),
).await?;

let channel = conn.create_channel().await?;
channel.basic_publish(
    "",
    "order.created",
    BasicProperties::default(),
    payload.as_bytes(),
    BasicPublishOptions::default(),
).await?;
```

### 通訊策略的選擇原則

| 場景 | 建議方案 | 理由 |
|------|---------|------|
| 查詢使用者資料 | gRPC | 型別安全、高效 |
| 對外 RESTful API | Axum | 生態成熟、開發效率高 |
| 事件通知（非同步） | Message Queue | 解耦、可靠傳遞 |
| 即時資料串流 | WebSocket / gRPC Stream | 雙向通訊 |

## 4. API Gateway 模式

API Gateway 作為系統的統一入口，負責路由、認證、速率限制與請求轉換。

### 使用 Axum 實作 Gateway

```rust
use axum::{
    Router, middleware,
    routing::any,
    http::Request,
};
use tower_http::{
    cors::CorsLayer,
    limit::RequestBodyLimitLayer,
    timeout::TimeoutLayer,
};

async fn proxy_handler(
    req: Request<Body>,
) -> Result<Response<Body>, StatusCode> {
    // 依據路徑前綴轉發至對應服務
    let path = req.uri().path();
    if path.starts_with("/api/users") {
        forward_to("http://user-service:8080", req).await
    } else if path.starts_with("/api/orders") {
        forward_to("http://order-service:8080", req).await
    } else {
        Err(StatusCode::NOT_FOUND)
    }
}

let app = Router::new()
    .route("/api/*path", any(proxy_handler))
    .layer(CorsLayer::permissive())
    .layer(TimeoutLayer::new(Duration::from_secs(30)));
```

### 速率限制與熔斷

使用 `governor` 套件實作令牌桶速率限制，搭配 `tokio::sync::Semaphore` 控制連線池，避免下游服務被突發流量沖垮。

## 5. 可觀測性：Tracing、Metrics、Logging

### Tracing（分散式追蹤）

`tracing`  crate 是 Rust 生態的標準日誌與追蹤框架，搭配 `tracing-opentelemetry` 可將 span 匯出至 Jaeger 或 Tempo。

```rust
use tracing::{info, instrument};

#[instrument(skip(db))]
async fn create_order(db: &DbPool, req: CreateOrderRequest) -> Result<Order> {
    info!("creating order for user {}", req.user_id);
    // ...
}
```

### Metrics（指標）

使用 `metrics`  crate 搭配 `metrics-exporter-prometheus`，暴露 `/metrics` 端點供 Prometheus 抓取：

```rust
use metrics::{counter, histogram};

async fn handle_request() {
    counter!("requests.total", "service" => "order").increment(1);
    let timer = histogram!("request.duration_seconds");
    // ... 業務邏輯 ...
    timer.record(std::time::Instant::now().elapsed());
}
```

### Structured Logging

```rust
use tracing_subscriber::EnvFilter;

tracing_subscriber::fmt()
    .json()
    .with_env_filter(EnvFilter::from_default_env())
    .init();
```

將日誌以 JSON 格式輸出至 stdout，由容器執行期（如 Docker 的 json-file driver 或 Kubernetes 的 Fluentd）統一收集。

### Grafana 儀表板建議指標

- 每個服務的請求速率（QPS）
- P50 / P95 / P99 延遲
- 錯誤率（5xx 比例）
- Tokio 執行器任務數量
- 記憶體與 CPU 使用率

## 6. 部署策略

### Docker 多階段建置

```dockerfile
# 第一階段：編譯
FROM rust:1.85-slim-bookworm AS chef
RUN cargo install cargo-chef
WORKDIR /app

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json
COPY . .
RUN cargo build --release --bin order-service

# 第二階段：最小執行環境
FROM gcr.io/distroless/cc-debian12
COPY --from=builder /app/target/release/order-service /app/order-service
EXPOSE 8080
CMD ["/app/order-service"]
```

`cargo-chef` 利用 Docker layer cache，只在使用者程式碼變更時重新編譯依賴。

### Kubernetes 部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
      - name: order-service
        image: registry.example.com/order-service:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
        startupProbe:
          httpGet:
            path: /ready
            port: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
  ports:
  - port: 8080
```

Rust 服務啟動極快（通常 < 100ms），理論上可將 `startupProbe` 設為極短的 `initialDelaySeconds`，這在 spot instance 滾動更新時是一大優勢。

## 7. 實際案例分析

### Discords 的 Rust 微服務遷移

Discord 在 2020 年將部分 Go 服務遷移至 Rust。其閱讀狀態服務（Read States Service）在改寫為 Rust 後，單一節點的吞吐量提升了 10 倍以上，GC 暫停完全消失。團隊的經驗是：Rust 的學習曲線雖然陡峭，但在延遲與資源敏感場景中回報極大。

### Cloudflare 的 Pingora

Cloudflare 以 Rust 重寫了其代理伺服器家族，取代了 NGINX 為基礎的舊架構。Pingora 專案使用了 Tokio 與自訂的 HTTP 框架，能處理數百萬並行連線。他們的關鍵經驗是：Rust 的所有權模型讓並行程式碼的正確性保證遠高於 C 語言，同時效能完全可比肩。

### 台灣新創的 Rust 採用

國內有多家 FinTech 與 IoT 新創選擇 Rust 作為微服務主力語言。主要原因是：業務合規要求嚴格，Rust 能提供更高的正確性保證；同時靜態連結的特性讓監管審查的二進位分發流程大幅簡化。

## 總結

Rust 微服務架構的優勢可以歸納為三點：

1. **低成本維運**：記憶體用量低、啟動快、映像小，基礎設施成本顯著下降
2. **高正確性**：編譯期檢查消滅了整類錯誤，生產事故大幅減少
3. **生態日趨成熟**：Tokio、Axum、Tonic、tracing 等套件已能支撐生產級需求

對於考慮導入 Rust 微服務的團隊，建議從邊界清晰的獨立服務開始（例如 notification-service 或 webhook-gateway），累積經驗後再逐步擴大範圍。Rust 的學習曲線是真實存在的，但它在生產環境中回饋給團隊的穩定性與效能，值得這份投資。

---

*本文為「AI 程式人雜誌」2026 年 8 月號系列文章第五篇。*
