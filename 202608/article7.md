# MCP 協議與 Rust 服務整合

## 從 API 到協議：AI 與服務的溝通橋樑

2025 年底，Anthropic 聯合多家 AI 與工具廠商正式發佈了 **Model Context Protocol（MCP）1.0**，這是大型語言模型與外部工具／資料來源之間的第一個開放標準協議。不同於傳統 REST API 需要為每次整合撰寫客製化程式碼，MCP 提供了一套統一的生命週期管理與呼叫約定，讓 AI Agent 可以動態發現、授權、呼叫外部工具。本文將從協議核心概念出發，逐步展示如何在 Rust 生態系中實作一個生產就緒的 MCP Server。

## MCP 1.0 的核心概念

MCP 的設計哲學可以歸納為一句話：**讓模型理解工具，而不只是讓工程師寫程式碼**。傳統 API 整合中，開發者必須手動將 API 文件轉換為 LLM 可理解的 function calling schema；MCP 將這個過程標準化為協議層的協商機制。

MCP 1.0 定義了三種主要角色：

- **MCP Host**：LLM 應用程式的載體，例如 Claude Desktop、VS Code 外掛、或自訂的 LLM Agent 框架。Host 負責發起連線、管理會話、並將使用者的自然語言查詢轉化為協議操作。
- **MCP Client**：Host 與 Server 之間的一對一通訊端。Client 建立與 Server 的連線後，執行初始化握手、能力協商、以及工具呼叫的生命週期管理。
- **MCP Server**：公開特定功能（工具、資源、提示樣板）的輕量級服務。每個 Server 獨立運作，可以是一個本機子程序、一個 Docker 容器、或一個遠端 HTTP 服務。

通訊協議建立在 JSON-RPC 2.0 之上，支援 `stdio`（適合本機子程序）與 `Streamable HTTP`（適合遠端服務）兩種傳輸層。初始化階段雙方交換 `ServerCapabilities` 與 `ClientCapabilities`，確認支援的功能集合後，才進入正常的工具呼叫流程。

值得一提的是 MCP 對 **授權（Authorization）** 的原生支援。在初始化握手後，Client 可以要求 Server 進入授權流程——這對於企業環境中需要 OAuth 2.0 或 API Key 驗證的場景至關重要。授權狀態由 Server 端管理，Client 端僅負責轉發授權請求給使用者。

## 架構拆解：Tool、Resource、Prompt

MCP 定義了三種核心原語（primitives），對應不同的互動模式：

### Tool（工具）

Tool 是 MCP 最核心的原語，對應 LLM 的 function calling。每個 Tool 包含名稱（唯一識別）、描述（讓模型理解何時該使用它）、輸入 schema（JSON Schema 格式）、以及一個非同步的執行函式。

```rust
pub struct Tool {
    pub name: String,
    pub description: String,
    pub input_schema: serde_json::Value,
    pub handler: Box<dyn Fn(serde_json::Value) -> ToolResult + Send + Sync>,
}
```

Tool 的執行結果可以是文字、資源引用（`ResourceContents`）、或錯誤。Server 在 `list_tools` 回覆中回報所有可用工具，Client 透過 `call_tool` 觸發執行。Tool 不保證冪等性——也就是說，同樣的輸入可能產生不同的結果（例如查詢當前時間或發送郵件）。

### Resource（資源）

Resource 代表 Server 可以提供的結構化資料，通常用於 RAG 場景。每個 Resource 有 URI 與 MIME type，Client 透過 `read_resource` 取得內容。Resource 可以是靜態檔案、資料庫查詢結果、或動態產生的資料。

### Prompt（提示樣板）

Prompt 是預先定義的提示樣板，Server 可以公開一組帶有參數插槽的提示模板。Client 使用 `get_prompt` 取得渲染後的提示文字。這在 IDE 外掛或專業領域工具中特別有用——例如，一個 SQL 資料庫 MCP Server 可以提供「分析慢查詢」的提示模板。

## rust-mcp-sdk：Rust 生態的 MCP 實作

Rust 社群在 MCP 標準化過程中同步開發了 [rust-mcp-sdk](https://crates.io/crates/rust-mcp-sdk)，這是最完整的 Rust MCP 實作。截至 2026 年中，該 crate 已達到 v0.4 穩定版本，支援完整的協議規範。

### 核心模組

```
rust-mcp-sdk
├── transport       // 傳輸層：stdio、HTTP、自訂
│   ├── StdioTransport
│   └── HttpTransport
├── protocol        // JSON-RPC 訊息封裝與解封
│   ├── messages    // Request、Response、Notification、Error
│   └── initialize  // 初始化握手與能力協商
├── server          // Server 端抽象
│   ├── McpServer   // Server trait
│   ├── Router      // 路由註冊
│   └── handler     // Tool、Resource、Prompt handler
├── client          // Client 端抽象
└── types           // 共用型別：Tool、Resource、Prompt 等
```

SDK 的設計遵循 Tower 風格的 `Service` trait，這讓它可以與 Axum、Tonic 等框架無縫整合。傳輸層是 SDK 中最靈活的部分——`Transport` trait 只有兩個方法：

```rust
#[async_trait]
pub trait Transport: Send + Sync {
    async fn send(&self, message: JsonRpcMessage) -> Result<()>;
    async fn receive(&self) -> Result<Option<JsonRpcMessage>>;
}
```

正因為這個極簡的抽象，MCP Server 可以部署在任何訊息通道之上——stdio、TCP、WebSocket、甚至 Kafka。

## 用 Axum 建立一個 MCP Server

以下是一個完整的 MCP Server 範例，它公開兩個工具：一個查閱系統時間，一個執行數學計算。我們使用 Axum 作為 HTTP 傳輸層。

首先在 `Cargo.toml` 中加入相依性：

```toml
[dependencies]
rust-mcp-sdk = { version = "0.4", features = ["axum"] }
axum = "0.8"
tokio = { version = "2", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tracing = "0.1"
tracing-subscriber = "0.3"
```

接著是 Server 的主程式：

```rust
use rust_mcp_sdk::{
    server::{McpServer, Router},
    transport::axum::{AxumTransport, McpAxumRouter},
    types::{
        CallToolRequest, CallToolResponse, ListToolsResponse,
        Tool, ContentType,
    },
};
use axum::{routing::post, Router as AxumRouter};
use std::sync::Arc;
use serde_json::json;

#[tokio::main]
async fn main() {
    tracing_subscriber::init();

    // 定義工具一：取得系統時間
    let time_tool = Tool::new(
        "get_time",
        "取得伺服器當前 UTC 時間",
        json!({
            "type": "object",
            "properties": {},
            "required": []
        }),
        |_params| async move {
            let now = chrono::Utc::now();
            CallToolResponse::text(
                json!({"utc_time": now.to_rfc3339()}).to_string()
            )
        },
    );

    // 定義工具二：簡單算術
    let calc_tool = Tool::new(
        "calculator",
        "執行加減乘除四則運算",
        json!({
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"},
                "op": {
                    "type": "string",
                    "enum": ["+", "-", "*", "/"]
                }
            },
            "required": ["a", "b", "op"]
        }),
        |params| async move {
            let a = params["a"].as_f64().unwrap_or(0.0);
            let b = params["b"].as_f64().unwrap_or(0.0);
            let result = match params["op"].as_str() {
                Some("+") => a + b,
                Some("-") => a - b,
                Some("*") => a * b,
                Some("/") if b != 0.0 => a / b,
                _ => return CallToolResponse::error("不支援的運算"),
            };
            CallToolResponse::text(json!({"result": result}).to_string())
        },
    );

    // 建立 MCP Router 並註冊工具
    let mut router = Router::new();
    router.add_tool(time_tool);
    router.add_tool(calc_tool);

    // 使用 Axum 傳輸層
    let mcp_service = Arc::new(McpServer::new(router));
    let axum_router = AxumRouter::new()
        .route("/mcp", post(move |body| {
            let svc = mcp_service.clone();
            async move {
                AxumTransport::handle_request(svc, body).await
            }
        }));

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000").await.unwrap();
    tracing::info!("MCP Server 啟動於 http://127.0.0.1:3000/mcp");
    axum::serve(listener, axum_router).await.unwrap();
}
```

這個 Server 啟動後，任何 MCP Client（例如 Claude Desktop、VS Code 的 MCP 擴充、或自訂的 LLM Agent）都可以透過 `http://127.0.0.1:3000/mcp` 連線並使用 `get_time` 與 `calculator` 兩個工具。

初始化握手階段，Server 會自動回報 `list_tools` 結果。Client 收到工具清單後，LLM 會根據使用者的自然語言輸入自動選擇適當的工具並填入參數。整個過程對使用者而言是透明的——他們只會問「台北現在幾點？」或「計算 3.14 乘以 2 的平方」，而不需要知道後端呼叫了哪個工具。

## MCP + SQLx：讓 AI 安全查詢資料庫

MCP 最強大的應用場景之一是讓 LLM 安全地查詢關係型資料庫。透過 SQLx 的編譯期 SQL 檢查與 MCP 的權限管控，我們可以打造一個兼具安全性與靈活性的資料庫查詢服務。

關鍵設計原則有三：

1. **唯讀隔離**：SQL Agent 只能使用連線池中的唯讀帳號，DML 操作（INSERT、UPDATE、DELETE）在 Server 端被嚴格過濾。MCP Server 可以透過 middleware 層對 SQL 語句進行語法分析，攔截非 SELECT 語句。
2. **查詢限制**：每個查詢的結果行數與執行時間都設有上限，防止惡意或失控查詢耗盡資料庫資源。
3. **Schema 預覽**：MCP 的 Resource 原語可以用來暴露資料庫的 table schema，讓 LLM 在生成 SQL 之前先理解資料結構。

受篇幅所限，以下是資料查詢工具的簡化實作：

```rust
async fn query_database(
    sql: String,
    pool: &sqlx::PgPool,
) -> CallToolResponse {
    // 安全檢查：僅允許 SELECT
    let trimmed = sql.trim().to_uppercase();
    if !trimmed.starts_with("SELECT") {
        return CallToolResponse::error("僅允許 SELECT 查詢");
    }

    // 執行查詢，限制 100 行
    let rows = sqlx::query(&sql)
        .fetch_all(pool)
        .await;

    match rows {
        Ok(rows) => {
            let results: Vec<serde_json::Value> = rows
                .iter()
                .map(|row| {
                    // 轉換為 JSON 格式
                    row_to_json(row)
                })
                .collect();
            CallToolResponse::text(
                serde_json::to_string_pretty(&results).unwrap()
            )
        }
        Err(e) => CallToolResponse::error(format!("SQL 錯誤：{e}")),
    }
}
```

將這個函式包裝為 MCP Tool 後，LLM 可以根據使用者的自然語言問題自動產生對應的 SQL 語句並執行查詢，同時所有操作都被限制在唯讀的安全邊界內。企業可以進一步在 middleware 中加入 SQL 語法分析器，封鎖 `pg_sleep`、大量 JOIN、或無索引查詢等危險模式。

## 企業應用場景

MCP 在企業環境中的價值不僅僅是「讓 AI 呼叫 API」。以下是幾個已在大規模生產環境中驗證的場景：

### 內部知識庫 RAG

企業可以將內部 Wiki、技術文件、程式碼庫包裝為 MCP Resource Server。LLM Host（如企業內部的 AI 助理）透過標準協議讀取相關文件片段，不需要為每種文件格式撰寫自訂的載入器。架構統一的 Resource 介面，讓 RAG pipeline 的維護成本大幅降低。

### DevOps 自動化

MCP Tool 可以對接 Kubernetes API、Terraform、PagerDuty、Slack 等基礎設施工具。一個統一的 MCP Server 可以同時提供查詢 Pod 狀態、擴縮容、查看日誌等功能。開發者不再需要在多個控制臺之間切換，只需用自然語言對 AI 助理下達指令。

### 資料分析儀表板

將資料庫查詢工具與繪圖工具結合成 MCP 服務鏈。使用者說「上個月的每日訂單趨勢」，LLM 自動查詢資料庫、計算聚合資料、並呼叫繪圖工具生成圖表。每個步驟都是標準化的 MCP Tool，可以獨立測試與置換。

## MCP 的未來發展

MCP 1.0 雖然填補了 AI 與工具之間標準化通訊的空白，但協議仍在快速演進中。以下幾個方向值得關注：

**傳輸層多樣化**：目前 stdio 與 HTTP 是唯二的標準傳輸方式，但社群正在推動 WebSocket、gRPC、以及基於訊息佇列的非同步傳輸。對於長時間執行的工具（如資料管道或模型訓練任務），非同步傳輸是必要的能力。

**工具鏈結（Tool Chaining）**：當前 MCP 的工具呼叫是平坦的——一次請求呼叫一個工具。但在複雜任務中，工具之間需要資料傳遞與流程控制。MCP 社群正在提案「工作流程（Workflow）」，允許 Server 定義多步驟的工具組合。

**串流回應（Streaming）**：當工具產生大量資料（例如資料庫查詢結果或日誌檔案），目前必須等待完整回應後才能傳回給 Client。串流回應的加入將顯著改善大資料量場景的使用者體驗。

**安全性框架**：工具授權目前在協議層僅有基本支援。未來預計引入更細粒度的存取控制，包括工具層級的 RBAC、API Key 自動輪換、以及稽核日誌的標準格式。

對於 Rust 開發者而言，MCP 提供了一個難得的機會：在 AI 工具整合這個快速增長的新領域中，以型別安全、高效能的 Rust 服務搶佔先機。無論是為現有系統新增 MCP 相容層，還是從零打造專屬的 AI Agent 後端，rust-mcp-sdk 與 Axum 的組合都是一條值得投入的技術路線。
