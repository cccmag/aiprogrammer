# AI Agent 框架在 Rust 中的實現

## 1. AI Agent 的興起與 Rust 的定位

2025 年被稱為「AI Agent 元年」，從 AutoGPT 到 Claude Computer Use，AI 從被動問答轉向主動執行任務的代理人模式。Agent 不再是單純的 LLM 呼叫包裝，而是具備工具呼叫、記憶管理、任務規劃與自我反思能力的自主系統。

在這波浪潮中，Rust 的定位耐人尋味。AI Agent 的上游——LLM 推理——主戰場在 Python（PyTorch、vLLM、transformers），但 Agent 框架的中下游：排程、並行、工具呼叫、記憶儲存、網路服務，恰恰是 Rust 的強項。Rust 無 GC、零成本抽象、所有權系統帶來的記憶體安全，以及 Tokio 提供的非同步生態，讓它成為構建高效能 Agent Runtime 的理想語言。

更重要的是，Rust 的型別系統能在編譯期捕捉許多 Python 執行期才會爆發的錯誤——對 Agent 這種涉及多工具、多 LLM 呼叫的複雜系統來說，這意味著更低的生產除錯成本與更高的生產環境穩定性。

## 2. Rust Agent 框架對比：AgentRS、Rig、LangChain Rust

目前 Rust 生態中有三個主要 Agent 框架值得關注：

### AgentRS

AgentRS 是最接近 Python LangChain 思維的 Rust 框架，提供 Chain、Tool、Memory 等抽象。它的設計目標是「LangChain 的 Rust 版本」，API 風格明顯受到 LangChain 影響。但由於 Rust 的所有權與生命週期限制，AgentRS 的動態排程靈活性不如 Python 版，且社群活躍度較低，更新速度偏慢。

### Rig

Rig 是目前 Rust Agent 框架中最受矚目的新星。它由 MongoDB 的 Rust 工程師發起，設計上更「Rust native」——大量使用泛型與 trait 來達成編譯期多型，而非 Box\<dyn\> 的執行期動態分派。Rig 支援 OpenAI、Anthropic、Cohere 等多家 LLM 後端，內建向量儲存抽象，並提供流暢的 chain 語法。版本迭代活躍，社群成長快速。

### LangChain Rust

LangChain 官方維護的 Rust SDK，定位較低階——主要提供 LLM 呼叫封裝與基本的 Chain 能力，Agent 層的 Tool 與 Memory 仍在開發中。適合需要與 LangChain Python 版共享邏輯的專案，或作為其它框架的底層依賴。

| 特性 | AgentRS | Rig | LangChain Rust |
|------|---------|-----|----------------|
| Agent 支援 | ✅ Chain-based | ✅ Tool + Memory | ⚠️ 開發中 |
| LLM 後端 | OpenAI | OpenAI / Anthropic / Cohere / Ollama | OpenAI / Anthropic |
| 向量儲存 | 無 | ✅ 內建抽象 | 需外部整合 |
| 非同步 | Tokio | Tokio | Tokio |
| 成熟度 | 實驗性 | Beta | Alpha |

## 3. Agent 核心元件的 Rust 實作

無論框架如何包裝，一個完整的 Agent 系統都離不開四個核心元件。以下從 Rust 的實作角度逐一探討。

### Tool

Tool 是 Agent 與外界互動的介面。在 Rust 中，Tool 通常實作為一個 trait：

```rust
#[async_trait]
pub trait Tool: Send + Sync {
    fn name(&self) -> &str;
    fn description(&self) -> &str;
    fn parameters(&self) -> Vec<Parameter>;
    async fn call(&self, input: serde_json::Value) -> Result<String, ToolError>;
}
```

關鍵在於 `Send + Sync`——Agent 可能同時呼叫多個 Tool，Rust 的型別系統保證了工具層級的執行緒安全，這是 Python 需要依賴工程紀律才能達成的。

### Memory

Memory 儲存對話歷史與 Agent 的長期知識。Rust 實作上常見的策略是分層：TokenMemory（最近 N 個 token）、WindowMemory（最近 K 輪對話）、SummaryMemory（摘要壓縮）。Rig 對 Memory 的 trait 設計如下：

```rust
#[async_trait]
pub trait Memory: Send + Sync {
    async fn save(&mut self, msg: Message) -> Result<()>;
    async fn load(&self) -> Result<Vec<Message>>;
    async fn clear(&mut self) -> Result<()>;
}
```

利用 Rust 的 `VecDeque` 實現滑動視窗記憶，無需 GC 即可達到零開銷的記憶體管理。

### Chain

Chain 是將 LLM 呼叫、Tool 執行、Memory 讀寫串聯起來的管線。Rig 的 chain 語法大量使用泛型來串接型別：

```rust
let response = rig::chain!(model, tool)
    .prompt("查詢本季銷售數據")
    .await?;
```

`chain!` 巨集在編譯期展開為型別安全的 Pipeline，每個階段的輸入輸出型別都經過檢查——這種安全網是 Python 的動態 chain 無法提供的。

### Planner

Planner（或稱 Agent 循環）決定 Agent 何時該呼叫工具、何時該回覆使用者。ReAct（Reason + Act）是最常見的模式。Rust 實作 ReAct 循環時，利用 `loop + match` 的組合，配合 LLM 回應中的 structured output（JSON / function call）來驅動決策：

```rust
loop {
    let thought = llm.think(&context).await?;
    match thought.action {
        Action::Call(tool_name, args) => {
            let result = tools.call(&tool_name, args).await?;
            context.add_observation(result);
        }
        Action::Reply(answer) => {
            return Ok(answer);
        }
    }
}
```

## 4. 為什麼 Agent 框架選擇 Rust

**效能**：Agent 本質上是密集的 I/O 任務——LLM API 呼叫、資料庫查詢、檔案讀寫。Rust + Tokio 的非同步 runtime 能在大規模並行工具呼叫中展現極低延遲與高吞吐。在需要同時查詢 20 個 API 並彙整結果的情境下，Rust Agent 的資源消耗僅為 Python 版的 1/3 到 1/5。

**安全**：Agent 會執行使用者提供的工具流程，記憶體安全漏洞可能導致任意程式碼執行。Rust 的所有權系統從根本上消滅了 Use-After-Free、Buffer Overflow 等問題。對希望將 Agent 部署到生產環境的團隊而言，這是 Python 難以比擬的優勢。

**並行**：Python 的 GIL 讓真正的並行執行需要 multiprocessing 的 overhead，而 Rust 的 `async`/`await` 配合 Tokio 的 work-stealing scheduler，能讓數百個工具呼叫以近乎零開銷的方式並行。Rig 對 Tool 的 `Send + Sync` 約束確保了每個工具都能安全地跨 task 共享。

## 5. 實際案例：用 Rig 建立一個資料庫查詢 Agent

以下用 Rig（v0.5+）建立一個能解析自然語言、查詢 SQLite 資料庫的 Agent。

```rust
use rig::providers::openai;
use rig::tool::Tool;
use serde::{Deserialize, Serialize};
use serde_json::json;
use sqlx::SqlitePool;

#[derive(Deserialize)]
struct QueryInput {
    sql: String,
}

struct SqliteTool {
    pool: SqlitePool,
}

#[async_trait]
impl Tool for SqliteTool {
    fn name(&self) -> &str { "query_database" }
    fn description(&self) -> &str {
        "執行 SQL 查詢，輸入為 { \"sql\": \"SELECT ...\" }"
    }
    fn parameters(&self) -> Vec<rig::tool::Parameter> {
        vec![rig::tool::Parameter {
            name: "sql".into(),
            param_type: "string".into(),
            description: "SQL 查詢語句".into(),
            required: true,
        }]
    }

    async fn call(&self, input: serde_json::Value) -> Result<String, rig::tool::ToolError> {
        let input: QueryInput = serde_json::from_value(input)
            .map_err(|e| rig::tool::ToolError::ToolCallError(e.into()))?;
        let rows: Vec<serde_json::Value> = sqlx::query_as::<_, serde_json::Value>(&input.sql)
            .fetch_all(&self.pool)
            .await
            .map_err(|e| rig::tool::ToolError::ToolCallError(e.into()))?;
        Ok(serde_json::to_string(&rows).unwrap())
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let pool = SqlitePool::connect("sqlite:sales.db").await?;
    let db_tool = SqliteTool { pool };

    let client = openai::Client::from_env();
    let agent = client
        .agent("gpt-4o")
        .preamble("你是一個 SQL 專家助手。根據使用者的問題，使用 query_database 工具查詢資料庫。請只輸出 SELECT 查詢。")
        .tool(db_tool)
        .build();

    let response = agent
        .prompt("上個月的總營收是多少？")
        .await?;
    println!("{}", response);
    Ok(())
}
```

這個例子展示幾個關鍵點：`SqliteTool` 實作了 `Tool` trait，Agent 初始化時注入工具，執行時 LLM 會自動判斷何時需要呼叫資料庫。`serde_json` 確保了 Tool 輸入輸出的型別安全，`sqlx` 的非同步查詢與 Rig 的 Tokio runtime 無縫整合。

## 6. 與 Python LangChain 的對比分析

Python LangChain 誕生於 2022 年底，經過三年發展已成為 Agent 框架的事實標準。Rig 與其相比各有優劣。

**開發體驗**：Python LangChain 的動態特性讓 prototyping 極快，但大型專案維護成本高。Rust Rig 需要編寫更多型別標註與錯誤處理，編譯時間也是代價，但一旦編譯通過，重構信心遠高於 Python。

**生態系**：LangChain 擁有數百個整合套件（LangChain Hub、LangSmith、LangServe），短期內 Rust 難以追趕。但 Rig 選擇了「少而精」的策略——專注於核心 Agent 元件的品質與效能。

**生產部署**：Python 部署 Agent 服務需要 Gunicorn / Uvicorn + 大量的記憶體。Rust 編譯為單一二進位檔，啟動時間以毫秒計，記憶體 footprint 極低，非常適合 Docker 與 Serverless 環境。

**團隊建議**：
- 新創 / Prototype 階段：Python LangChain 仍然是首選
- 需要高效能生產部署：Rig on Rust 是值得投資的方向
- Python 到 Rust 的遷移路徑：使用 LangChain Rust 作為過渡，逐步將核心 Agent 邏輯 Rust 化

## 結語

AI Agent 框架在 Rust 中的實現仍處於早期階段，但方向已經明確。Rig 代表的「型別安全 + 高效能」路線，正在為 Agent 系統的生產化部署鋪平道路。當 Agent 從 DEMO 走向真實商業場景，Rust 的價值會越來越明顯——穩定、快速、省錢。對於追求工程品質的團隊，現在正是投入 Rust Agent 生態的最佳時機。
