# Agent 工具生態：從函數呼叫到 MCP 協議

## 前言

工具使用是 AI Agent 與外部世界互動的橋樑。從 OpenAI 的 Function Calling API 到 Anthropic 的 Tool Use，再到最新的 MCP（Model Context Protocol），工具生態正在快速標準化。本文將深入探討工具定義的演進，並從零實作一個工具生態系統。

---

## 一、工具定義標準的演進

### 1.1 OpenAI Function Calling

OpenAI 在 2023 年 6 月推出的 Function Calling 是第一個廣義的 LLM 工具定義標準：

```python
import json
from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查詢指定城市的當前天氣",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名稱，如 Taipei",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                    },
                },
                "required": ["city"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "台北天氣如何？"}],
    tools=tools,
    tool_choice="auto",
)
```

### 1.2 Anthropic Tool Use

Anthropic 的 Tool Use 採用類似的 JSON Schema 格式，但傳遞方式略有不同：

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "查詢天氣",
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"],
            },
        }
    ],
    messages=[{"role": "user", "content": "台北天氣？"}],
)
```

---

## 二、統一工具抽象層

為了兼容不同 LLM 的 Tool 格式，我們可以建立一個統一的抽象層：

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable
import json

class ToolSpec(ABC):
    """工具規格定義"""
    name: str
    description: str
    parameters: Dict[str, Any]

    @abstractmethod
    def execute(self, **kwargs) -> str: ...

class ToolRegistry:
    """工具註冊中心"""
    def __init__(self):
        self._tools: Dict[str, ToolSpec] = {}

    def register(self, tool: ToolSpec):
        self._tools[tool.name] = tool

    def get_openai_tools(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                },
            }
            for t in self._tools.values()
        ]

    def execute(self, name: str, arguments: Dict) -> str:
        tool = self._tools.get(name)
        if not tool:
            return f"錯誤：找不到工具 '{name}'"
        return tool.execute(**arguments)
```

### 實作具體工具

```python
import requests

class WeatherTool(ToolSpec):
    name = "get_weather"
    description = "查詢指定城市的當前天氣"
    parameters = {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名稱"},
        },
        "required": ["city"],
    }

    def execute(self, city: str) -> str:
        # 使用 OpenWeatherMap API
        api_key = os.getenv("WEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather"
        resp = requests.get(url, params={
            "q": city, "appid": api_key, "units": "metric"
        })
        data = resp.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"{city} 天氣：{desc}，溫度：{temp}°C"
```

---

## 三、MCP：Model Context Protocol

### 3.1 MCP 架構概述

MCP（Model Context Protocol）是 Anthropic 於 2024 年底提出的開放協議，旨在標準化 LLM 與外部工具/資料來源的通訊方式。MCP 採用客戶端—伺服器架構：

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   LLM 應用    │────▶│  MCP 客戶端   │────▶│  MCP 伺服器   │
│  （客戶端）    │◀────│  （SDK）      │◀────│  （工具提供者） │
└──────────────┘     └──────────────┘     └──────────────┘
```

MCP 的核心優勢：

| 特性 | Function Calling | MCP |
|------|-----------------|-----|
| 協議類型 | 私有 API | 開放標準 |
| 工具發現 | 靜態定義 | 動態發現 |
| 安全性 | 應用層控制 | 內建安全層 |
| 互通性 | 單一供應商 | 跨供應商 |

### 3.2 MCP 伺服器實作

```python
# 使用 mcp 套件實作一個 MCP 伺服器
from mcp.server import Server, stdio_server
from mcp.types import Tool, TextContent

class CalculatorServer:
    def __init__(self):
        self.server = Server("calculator-server")

    async def run(self):
        async with stdio_server() as (read, write):
            await self.server.run(read, write, self._create_app())

    def _create_app(self):
        app = self.server

        @app.list_tools()
        async def list_tools():
            return [
                Tool(
                    name="calculate",
                    description="執行數學計算",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "數學表達式",
                            },
                        },
                    },
                )
            ]

        @app.call_tool()
        async def call_tool(name: str, arguments: dict):
            if name == "calculate":
                expr = arguments["expression"]
                try:
                    result = eval(expr, {"__builtins__": {}}, {})
                    return [TextContent(str(result))]
                except Exception as e:
                    return [TextContent(f"錯誤：{e}")]
            raise ValueError(f"未知工具：{name}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(CalculatorServer().run())
```

### 3.3 MCP 客戶端使用

```python
from mcp.client import stdio_client

async def use_mcp_tool():
    async with stdio_client(["python", "calculator_server.py"]) as (read, write):
        # 取得可用工具列表
        tools = await write.list_tools()
        print("可用工具：", [t.name for t in tools])

        # 呼叫工具
        result = await write.call_tool("calculate", {"expression": "2 + 3 * 4"})
        print("結果：", result.content[0].text)
```

---

## 四、工具生態的安全考量

### 4.1 權限分級

```python
from enum import Enum

class PermissionLevel(Enum):
    READ_ONLY = 1     # 唯讀，無安全風險
    SAFE = 2          # 安全操作（計算、格式化）
    FILE_ACCESS = 3   # 檔案操作
    NETWORK = 4       # 網路存取
    DANGEROUS = 5     # 系統操作（需人工確認）

class SecureToolRegistry(ToolRegistry):
    def __init__(self):
        super().__init__()
        self.permissions: Dict[str, PermissionLevel] = {}

    def register(self, tool: ToolSpec, level: PermissionLevel):
        super().register(tool)
        self.permissions[tool.name] = level

    def execute(self, name: str, arguments: Dict, current_level: PermissionLevel) -> str:
        required = self.permissions.get(name, PermissionLevel.SAFE)
        if current_level.value < required.value:
            return f"權限不足：需要 {required.name}，當前為 {current_level.name}"
        return super().execute(name, arguments)
```

---

## 結語

從 OpenAI Function Calling 到 MCP 協議，工具定義標準正在從專有走向開放。MCP 作為業界首個開放的工具通訊協議，有望成為 AI Agent 生態的「HTTP」——一個標準化的通訊層，讓不同的 Agent、LLM 和工具之間可以無縫協作。

---

**參考資料**

- OpenAI Function Calling：https://platform.openai.com/docs/guides/function-calling
- Anthropic Tool Use：https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- MCP 規範：https://modelcontextprotocol.io/
- "Toolformer: Language Models Can Teach Themselves to Use Tools", https://arxiv.org/abs/2302.04761
