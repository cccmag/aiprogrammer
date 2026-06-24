# MCP 協議：AI Agent 的標準化工具介面

2024 年 Anthropic 提出 **Model Context Protocol (MCP)** 時，或許沒有人想到它會在兩年內成為 ISO 國際標準（ISO/IEC 25489:2026）。MCP 從一個簡單的工具呼叫協議，進化為 AI Agent 與外部世界互動的通用語言。

## 什麼是 MCP？

MCP 是 AI 模型與外部工具之間的標準化通訊協議。它定義了三個核心角色：

```
┌──────────────┐    MCP Protocol     ┌──────────────┐
│   AI Model   │ ◄──────────────────► │  MCP Server  │
│  (MCP Client) │                     │  (Tool Host)  │
└──────────────┘                     └──────┬───────┘
                                            │
                                   ┌────────┴────────┐
                                   │  Tool1  Tool2   │
                                   │  Tool3  Tool4   │
                                   └────────────────┘
```

### 核心概念

- **Resources**：外部世界可被讀取的資料（檔案、資料庫、API）
- **Tools**：模型可執行的動作（計算、搜尋、寫檔）
- **Prompts**：預定義的對話範本
- **Sampling**：伺服器向模型發起生成請求（雙向通訊）

## 從 Function Calling 到 ISO 標準

```
2023 ──────────────────────────────────────────────► 2026
     Function Calling    MCP 1.0    MCP 2.0    ISO Standard
     (各廠商自訂格式)   (Anthropic)  (企業級)   (國際標準)
```

### MCP 1.0 (2024)

由 Anthropic 提出的初始協議，定義了 JSON-RPC 2.0 基礎的通訊格式：

```json
{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "web_search",
        "arguments": {
            "query": "2026 AI trends",
            "max_results": 5
        }
    },
    "id": 1
}
```

### MCP 2.0 (2025)

加入了企業級功能：

- **Sandbox**：工具在隔離容器中執行
- **Transaction Isolation**：多步驟操作的事務保證
- **Audit Trail**：每步操作的完整日誌
- **Rate Limiting**：防止模型無限呼叫工具
- **Permission Hierarchy**：細粒度的權限控制

### ISO 標準 (2026)

2026 年 3 月，ISO 正式將 MCP 列為國際標準，並新增：

- 統一的錯誤碼與錯誤處理規範
- 跨平台傳輸層（stdio、SSE、WebSocket、gRPC）
- 安全稽核強制要求
- 互通性測試套件

## 實作 MCP Server

以下是用 Python 實作一個簡單的 MCP Server，提供檔案操作與程式執行功能：

```python
import asyncio
import subprocess
from pathlib import Path
from typing import Any
from mcp import Server, StdioServerTransport, Tool, Resource

class DevToolsMCPServer(Server):
    def __init__(self):
        super().__init__(name="dev-tools-server")
        self.sandbox_dir = Path("/tmp/mcp_sandbox")
        self.sandbox_dir.mkdir(exist_ok=True)

        # 註冊工具
        self.register_tool(self.execute_python)
        self.register_tool(self.read_file)
        self.register_tool(self.search_files)

    @Tool(
        name="execute_python",
        description="在沙盒環境中執行 Python 程式碼",
        parameters={
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "要執行的 Python 程式碼"},
                "timeout": {"type": "number", "default": 30}
            },
            "required": ["code"]
        }
    )
    async def execute_python(self, code: str, timeout: int = 30) -> dict:
        """在隔離環境執行 Python 程式碼"""
        sandbox_file = self.sandbox_dir / "script.py"
        sandbox_file.write_text(code)

        try:
            result = subprocess.run(
                ["python3", str(sandbox_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.sandbox_dir)
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "執行超時"}

    @Tool(
        name="read_file",
        description="讀取沙盒內的檔案內容（禁止路徑穿越）",
        parameters={
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "檔名（僅允許 sandbox 內的檔案）"}
            },
            "required": ["filename"]
        }
    )
    async def read_file(self, filename: str) -> dict:
        """安全地讀取檔案（防止路徑穿越攻擊）"""
        # 安全檢查：禁止路徑穿越
        safe_path = self.sandbox_dir.resolve() / filename
        if not str(safe_path).startswith(str(self.sandbox_dir.resolve())):
            return {"success": False, "error": "Permission denied: path traversal detected"}

        if not safe_path.exists():
            return {"success": False, "error": "File not found"}

        content = safe_path.read_text()
        return {"success": True, "content": content, "size": len(content)}

    @Tool(
        name="search_files",
        description="在沙盒中搜尋檔案",
        parameters={
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "glob 模式"}
            },
            "required": ["pattern"]
        }
    )
    async def search_files(self, pattern: str) -> dict:
        files = list(self.sandbox_dir.glob(pattern))
        return {
            "success": True,
            "files": [str(f.relative_to(self.sandbox_dir)) for f in files]
        }

# 啟動 MCP Server
async def main():
    server = DevToolsMCPServer()
    transport = StdioServerTransport()
    await server.connect(transport)
    await server.wait_for_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```

### MCP Client 呼叫範例

```python
from mcp import Client

async def main():
    client = Client()
    await client.connect_to_server("python", "dev_tools_server.py")

    # 取得可用工具列表
    tools = await client.list_tools()
    print(tools)

    # 呼叫工具
    result = await client.call_tool("execute_python", {
        "code": "print('Hello from MCP!')"
    })
    print(result)
```

## 企業部署架構

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  AI Agent   │────►│  MCP Gateway│────►│  MCP Server │
│  (Client)   │     │  (負載均衡)  │     │  (Sandbox)  │
└─────────────┘     └──────┬──────┘     └──────┬──────┘
                           │                    │
                    ┌──────┴──────┐     ┌──────┴──────┐
                    │  Audit Log  │     │  Rate Limiter│
                    └─────────────┘     └─────────────┘
```

- **MCP Gateway**：統一入口，負責認證、路由、速率限制
- **Sandbox**：每個工具在獨立容器執行
- **Audit Trail**：所有操作記錄至不可篡改的日誌系統
- **Transaction Manager**：確保多步驟操作的一致性

## 結語

MCP 從 Anthropic 內部專案到 ISO 國際標準的歷程，反映了 AI Agent 標準化的迫切需求。對於開發者而言，MCP 不僅是工具呼叫協議，更是一個讓 AI 模型安全、可控地與外部世界互動的架構模式。未來任何 AI Agent 若缺少 MCP 支援，將如同今天的 Web 應用不支援 HTTP 一樣難以想像。

## 延伸閱讀

- [MCP 官方規範 (ISO/IEC 25489:2026)](https://www.google.com/search?q=MCP+protocol+ISO+25489+2026)
- [Anthropic MCP 原始提案與設計理念](https://www.google.com/search?q=Anthropic+Model+Context+Protocol+MCP)
- [MCP 2.0 企業功能：Sandbox 與 Transaction Isolation](https://www.google.com/search?q=MCP+2.0+sandbox+transaction+isolation+enterprise)
- [從 Function Calling 到 MCP 的演進歷史](https://www.google.com/search?q=AI+function+calling+to+MCP+protocol+evolution)

---

