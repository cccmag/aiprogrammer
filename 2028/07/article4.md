# MCP 協議深入

## Model Context Protocol 簡介

MCP 是由 Anthropic 提出的開放協議，定義 LLM 與外部工具／資料源之間的標準介面。類似於 Language Server Protocol (LSP) 但針對 AI Agent。

## 協議核心概念

```
客戶端 (LLM) ←→ MCP Server ←→ 外部資源
```

- **Tools**: 可呼叫的函式（查資料庫、讀檔案）
- **Resources**: 唯讀資料源（文件、API 回傳）
- **Prompts**: 預定義提示模板

## MCP Server 實作範例

```python
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions

app = Server("database-agent")

@app.list_tools()
async def list_tools():
    return [
        {
            "name": "query_sql",
            "description": "執行 SQL 查詢",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "sql": {"type": "string"}
                }
            }
        }
    ]

@app.call_tool()
async def call_tool(name, arguments):
    if name == "query_sql":
        result = db.execute(arguments["sql"])
        return {"content": [{"type": "text", "text": str(result)}]}

async def main():
    async with mcp.server.stdio.stdio_server() as (read, write):
        await app.run(read, write, InitializationOptions(
            server_name="database-agent",
            server_version="1.0.0"
        ))
```

## 與 Function Calling 的差異

MCP 將工具定義從提示詞中抽離為獨立協議，支援動態註冊、類型安全與跨模型相容。傳統 Function Calling 依賴特定 API 格式，MCP 提供統一抽象層。

## 應用場景

- IDE 中 Agent 讀取專案檔案
- 資料庫查詢 Agent
- 檔案系統操作 Agent

更多資訊請見 https://www.google.com/search?q=Model+Context+Protocol+MCP+Anthropic。
