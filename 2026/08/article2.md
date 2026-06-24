# Axum 生態成熟：從 API 到微服務

## 前言

2021 年，Tokio 團隊推出了 Axum —— 一個奠基於 Tower 與 Tokio 之上的 Web 框架。五年後的今天，Axum 已經從實驗性專案成長為 Rust 非同步 Web 生態中最活躍的框架之一，不僅在 API 伺服器站穩腳步，更逐步滲透到微服務架構的核心地帶。

## 從 2021 到 2026：Axum 的進化路線

Axum 的第一個公開版本（v0.1）於 2021 年 7 月釋出，當時僅提供最基礎的路由與處理器功能。2022 年的 v0.5 引入了巢狀路由（nesting）與共用狀態（shared state），讓大型專案得以模組化組織程式碼。v0.6 加入了 `State` 萃取器，從此 handler 可以透過型別安全的方式存取應用狀態，不再需要 `Extension` 的型別抹除。

2023 年的 v0.7 是重要的里程碑——萃取器大規模重構、`IntoResponse` trait 標準化、以及對 Tower `Service` trait 的直接相容。這讓 Axum 得以無縫嵌入既有的 Tower 中介軟體鏈，第三方 crate 也可以輕鬆撰寫自訂中介軟體。

2024 年的 v1.0 正式版釋出，API 穩定化承諾讓生產環境採用率大幅攀升。v1.0 的遷移成本極低，從 v0.7 升級幾乎不需要修改業務邏輯，這在 Rust 框架中實屬罕見。2025 年到 2026 年間，社群貢獻開始加速：`axum-extra` 匯集了 protobuf 路由、typed header、自訂 JSON 錯誤格式等實驗性功能；`axum-sessions`、`axum-login`、`axum-test` 等輔助 crate 形成了完整的周邊生態。2026 年初釋出的 v2.0 引入了改良的 WebSocket 背壓機制、原生 OpenTelemetry 整合、以及更靈活的錯誤處理模型。

## 框架比較：Axum vs. Actix Web vs. Rocket vs. Warp

在 Rust Web 框架的版圖中，Axum 並非最早登場，卻在短時間內取得了驚人的社群採用率。以下是截至 2026 年的關鍵比較：

**Actix Web** 仍然保有極致的吞吐效能，其 actor 模型在大量短連線的 I/O 密集型場景中持續領先。TechEmpower 基準測試中 Actix Web 位居前段班，Axum 則穩定在中上區段，差距通常在 10% 以內。但 Actix 的抽象模型與標準 Rust 非同步生態的整合較為封閉——Actix 使用自己的 `Actor` 系統而非 Tower 的 `Service` 抽象，當需要接入 Tower 中介軟體或 Tonic gRPC 時，整合成本明顯高於 Axum。

**Rocket** 以其編譯時路由檢查與禮儀性 API 著稱，編譯器可以在路由表產生錯誤時給出清晰的人類可讀訊息。但 Rocket 對 Rust 夜版（nightly）的長期依賴讓部分保守團隊卻步，雖然 0.5 版後已全面擁抱 stable Rust 與 tokio，但生態遷移的慣性已經讓許多開發者轉向 Axum。

**Warp** 以 filter 組合子（combinator）的設計哲學吸引了函數式風格的開發者。在大型專案中，filter 鏈的型別簽章變得極其複雜——一個包含五層組合的路由可能產生數十字的型別簽章，編譯錯誤訊息難以閱讀。Axum 以傳統的 handler + extractor 模式降低了學習曲線，萃取器各自實作 `FromRequestParts` 或 `FromRequest`，編譯器產生的型別簽章遠比 filter 組合簡單。

Axum 的核心競爭力在於它**不是**一個從零打造的框架，而是 Tower 生態的自然延伸。開發者學習 Axum 的同時，也在學習 Tokio 與 Tower 的通用抽象——這筆知識投資可以複用於 gRPC、跨服務通訊、甚至自訂非同步中介軟體。這也是 Axum 在生態佔有率上快速追趕 Actix Web 的根本原因。

## Tower 中介軟體生態

Tower 是 Axum 的基石，但它並非 Axum 專屬——Tower 是 Rust 生態中非同步服務的中立抽象層。它定義了 `Service` 與 `Layer` 這兩個核心 trait，讓中介軟體可以像樂高積木一般組合。截至 2026 年，Tower 生態已經涵蓋：

- **限流（Rate Limiting）**：`tower-governor` 實作漏桶與令牌桶演算法，`tower-http` 內建的 rate limit layer 提供基於 IP 或自訂鍵的限流。
- **熔斷（Circuit Breaker）**：`tower` 的 `CircuitBreaker` 監控連續失敗次數，達到閾值後自動切斷流量，並在冷卻期後嘗試恢復。
- **負載均衡（Load Balancing）**：`tower` 內建的 `Balance` 與 `p2c`（Power of Two Choices）演算法，適合在動態服務拓撲中快速選擇後端。
- **重試與超時**：`tower` 的 `Retry` 支援自訂策略（指數退避、jitter），`Timeout` 為每個請求設定獨立超時，`Buffer` 層則提供 bounded channel 作為工作佇列。
- **分散式追蹤**：`tower-http` 的 `TraceLayer` 搭配 `tracing` crate，可自動記錄請求方法、URI、狀態碼、處理耗時，並延伸至 OpenTelemetry 與 Grafana Tempo/Jaeger。
- **指標收集**：`tower-http` 可與 Prometheus 或 OpenTelemetry metrics SDK 繫結，自動導出請求計數、延遲分佈、錯誤率等關鍵指標。
- **傳輸層強化**：CORS、壓縮（brotli/gzip/deflate）、敏感資訊遮罩的日誌記錄、靜態檔案服務等超過 20 個開箱即用的中介軟體。

值得一提的是 `tower-http` 的設計哲學——每個中介軟體都是一個獨立的 feature flag，編譯時只引入需要的部分。一個只啟用 `cors` 與 `trace` 的 Axum 服務，其二進制檔案增量僅約數百 KB。

## WebSocket 與 SSE 的原生支援

即時通訊已是現代 Web 應用的標配。Axum 從 v0.7 開始內建 WebSocket 支援，透過 `axum::extract::ws::WebSocketUpgrade` 萃取器，可以在 handler 中以寥寥數行程式碼建立 WebSocket 連線：

```rust
async fn ws_handler(ws: WebSocketUpgrade) -> Response {
    ws.on_upgrade(|socket| async move {
        let (mut sender, mut receiver) = socket.split();
        while let Some(Ok(msg)) = receiver.recv().await {
            sender.send(msg).await.unwrap();
        }
    })
}
```

上述實作即為完整的 echo 伺服器。Axum 的 WebSocket 實作支援文字與二進制 frame、ping/pong 心跳、以及關閉 frame 的正確處理。內建的 `WebSocketClose` 型別讓應用層可以優雅地控制連線生命週期。

SSE（Server-Sent Events）同樣獲得一級支援。`axum::response::sse::Sse` 讓伺服器可以將事件串流以標準 HTTP 回應的形式推送給客戶端：

```rust
async fn sse_handler() -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let stream = async_stream::stream! {
        loop {
            yield Ok(Event::default().data("heartbeat"));
            tokio::time::sleep(Duration::from_secs(1)).await;
        }
    };
    Sse::new(stream).keep_alive(KeepAlive::default())
}
```

SSE 的典型場景包括即時通知推播、LLM token 串流（如 OpenAI 風格的 response streaming）、以及儀表板的即時資料更新。Axum 的實作自動處理了 SSE 規格中的 `Last-Event-Id` 與重連邏輯。

這兩個功能在 Axum 1.x 中已經相當穩定，並在 v2.0 中引入了背壓感知（backpressure-aware）的串流控制。`WebSocket` 與 `Sse` 內部改用 bounded channel，當消費者處理速度落後時，傳送端會自動降速或斷開連線，避免慢速消費者拖垮伺服器記憶體。

## 微服務架構中的 Axum

當服務數量從個位數成長到數十甚至上百，Axum 在微服務架構中的定位更加清晰。它不是重量級的微服務框架（如 Spring Cloud），而是提供了**建構微服務基礎設施所需的樂高積木**。

### 服務發現（Service Discovery）

Axum 不綁定特定的服務發現機制，但透過 Tower 的抽象層可以輕鬆整合 Consul、etcd、或 Kubernetes API。實務上常見的模式是使用 `tower::discover::ChangeSet` 動態管理後端服務列表：

```rust
let discover = ConsulDiscover::new("my-svc", consul_client);
let balancer = Balance::p2c(discover);
```

當 Consul 中的服務實例增減時，`ChangeSet` 會動態更新內部連線池，無需重新部署。搭配 `tower::load::PeakEwma` 負載衡器，可以實現最少延遲優先的請求路由。

### 負載均衡與熔斷（Load Balancing & Circuit Breaking）

Axum 可以用作 API Gateway 或 Sidecar Proxy 的基礎建構塊。結合 `tower::balance` 與 `tower::retry`，可以在數十行程式碼內建立一個具備重試邏輯與熔斷機制的反向代理：

```rust
let inner = ServiceBuilder::new()
    .retry(RetryPolicy::exponential(Duration::from_millis(100), 3))
    .timeout(Duration::from_secs(5))
    .layer(TraceLayer::new_for_http())
    .service(backend_service);
```

相比於 Nginx 或 Envoy，這種純 Rust 方案的優勢在於零額外依賴、統一的設定格式（Rust 程式碼即設定）、以及與組織內部監控系統的深度整合。

### 分散式追蹤（Distributed Tracing）與可觀測性

`tower-http` 的 `TraceLayer` 與 OpenTelemetry 生態深度整合。只需加入 `TraceLayer` 並設定 OpenTelemetry exporter，即可為每個請求自動產生跨度（span），涵蓋請求處理、資料庫查詢、以及跨服務的 gRPC 呼叫：

```rust
let app = Router::new()
    .route("/api/users", get(list_users))
    .layer(TraceLayer::new_for_http()
        .on_request(|req: &Request<_>, _span: &Span| {
            info!("{} {}", req.method(), req.uri());
        }));
```

在 Kubernetes 環境中，健康檢查也是微服務的基礎設施需求。Axum 透過獨立的 `Router` 處理 `/healthz` 與 `/readyz` 端點，並與主要業務路由分離，避免中介軟體污染影響健康檢查的準確性：

```rust
let health = Router::new()
    .route("/healthz", get(|| async { StatusCode::OK }))
    .route("/readyz", get(ready_check));

let app = Router::new()
    .merge(health)
    .route("/api/v1/orders", get(list_orders));
```

### 設定管理

Axum 社群普遍採用 `dotenvy` 搭配 `serde` 的 Deserialize 來處理設定。結合 `figment` 可以實現多階層的設定合併（環境變數 > 設定檔 > 預設值），並在服務啟動時執行設定驗證。在微服務環境中，每個服務的設定可能來自不同的 ConfigMap 或 Secrets 儲存，這種型別安全的設定管理方式大幅降低了設定錯誤導致的生產事故。

## 混合架構：Axum + Tonic（gRPC）

微服務架構中，RESTful API 與 gRPC 各有擅場：REST 適合外部客戶端與瀏覽器應用，gRPC 則在內部服務間的高效率通訊中佔據主導地位。Axum 與 Tonic 都屬於 Tokio/Tower 生態系，兩者的整合因此異常平滑。

典型的混合架構模式如下：

1. **邊界服務（Edge Service）**：使用 Axum 對外提供 HTTP/REST API，處理認證、授權、請求驗證，作為外部世界進入微服務網格的單一入口。
2. **內部服務**：使用 Tonic 定義 Protobuf 服務，服務間以 gRPC 通訊。透過 `.proto` 檔案的強型別合約，團隊之間進行契約優先（contract-first）的協作。
3. **雙協定服務**：同一個服務同時綁定 Axum 路由與 Tonic 服務，共用同一個 Tokio runtime 與 Tower 中介軟體層。

實作上，可以讓兩者監聽不同埠，但共用同一份 `Arc<AppState>`：

```rust
let app = Router::new()
    .route("/api/users", get(list_users).post(create_user))
    .layer(TraceLayer::new_for_http())
    .layer(CorsLayer::permissive());

let grpc = tonic::transport::Router::new()
    .add_service(UserServiceServer::new(user_impl));

tokio::spawn(grpc.serve(grpc_addr));
let listener = tokio::net::TcpListener::bind(http_addr).await?;
axum::serve(listener, app).await?;
```

兩種協定的認證、追蹤、限流等跨切面關注點只需實作一次。透過 `Tonic` 的 interceptor 與 Axum 的 middleware 共用同一組狀態，鬆耦合但高效率。

此外，`tonic-web` crate 在 Axum 之上包裝一層 gRPC-Web handler，讓瀏覽器客戶端也可以透過 HTTP/1.1 呼叫 gRPC 服務。這意味著前端團隊可以直接從 TypeScript 呼叫 Protobuf 定義的服務方法，無需在 API Gateway 層重複定義 REST 端點。

另一個關鍵優勢是型別共享。Tonic 從 `.proto` 檔案產生的 Rust 結構體可以直接作為 Axum handler 的 JSON request body：

```rust
async fn create_user_handler(
    Json(proto::CreateUserRequest { name, email }): Json<proto::CreateUserRequest>,
    State(db): State<DbPool>,
) -> Result<Json<proto::User>, AppError> {
    let user = db.create_user(name, email).await?;
    Ok(Json(user))
}
```

從 Protobuf 單一來源衍生的型別同時服務了 gRPC 內部呼叫與 RESTful 外部 API，確保一致性並消除型別重複定義的痛點。Protobuf 的欄位編號規則與 JSON 命名慣例（camelCase vs. snake_case）可以透過 `serde` 屬性輕鬆調和。

## 測試策略

Axum 的測試生態在 2025-2026 年間快速成熟。`axum-test` crate 提供了在記憶體中啟動完整路由樹的能力，無需綁定實際埠號：

```rust
let response = axum_test::TestServer::new(app)?
    .get("/hello/world")
    .await;

assert_eq!(response.status(), StatusCode::OK);
```

v2.0 進一步將測試輔助工具移入核心 crate。測試伺服器支援 cookie 管理、session 注入、WebSocket 連線模擬，讓整合測試的撰寫成本大幅降低。對於需要資料庫的測試，`sqlx::test` 與 Axum 的 `TestServer` 可以同時使用，在同一個測試函數中完成從請求發出到資料驗證的完整流程。

## 總結

Axum 的成功並非偶然。它站在 Tokio 與 Tower 的肩膀上，選擇了「不重造輪子」的務實路線，將關注點集中在 Web 層最關鍵的抽象：路由、萃取器、回應建構。一切圍繞 Tower 的 `Service` trait 運轉，讓整個 Tokio 生態的力量都能為 Axum 所用。

從 2021 年的小眾框架到 2026 年的生態核心，Axum 證明了自己不僅僅是又一個 Rust Web 框架，而是 Tokio 非同步生態在 Web 層的標準面孔。對於正在考慮 Rust Web 技術選型的團隊，Axum 提供的已經不僅僅是「夠用」——從單體 API 到數百服務的微服務網格，Axum 搭配 Tonic 與 Tower 可以覆蓋完整的光譜。在 2026 年的 Rust 生態中，Axum 已經不只是選項之一，而是越來越多的「預設選擇」。

---

*本文為「AI 程式人雜誌」2026 年 8 月號「Rust 生態：Tokio、Axum、資料庫」專題的第二篇文章。*
