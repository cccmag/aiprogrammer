# 工具使用與 API 整合（2023-2028）

## 從對話到行動

### LLM 的先天限制

語言模型有一個根本限制：**它們只會生成文字，無法直接與外部世界互動**。模型不知道現在幾點、天氣如何、最新的股價是多少——除非這些資訊已經存在於訓練資料中。

```python
# 純文字生成：只能依靠訓練資料
def ask_weather_naive(model, city):
    return model.generate(f"今天{city}的天氣如何？")
    # 如果訓練資料截止於 2024 年，模型無法知道今天的實際天氣
```

### Function Calling 的誕生

2023 年 6 月，OpenAI 發表了 Function Calling 功能。這是生成式 AI 的一個轉捩點——模型不再只是「說話」，還可以「做事」。

```python
# Function calling 的基本模式
functions = [
    {
        "name": "get_weather",
        "description": "取得指定城市的天氣資訊",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "date": {"type": "string"}
            },
            "required": ["city"]
        }
    }
]

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "明天台北會下雨嗎？"}],
    functions=functions
)
```

### 工具整合的架構模式

工具使用的基本流程是一個**循環**：

```python
class ToolUsingAgent:
    def __init__(self):
        self.tools = {
            "search": SearchTool(),
            "calculator": CalculatorTool(),
            "code_executor": CodeExecutor(),
            "database": DatabaseTool()
        }

    def run(self, task):
        messages = [{"role": "user", "content": task}]
        while True:
            response = self.llm.chat(messages, tools=self.tools)
            if response.finish_reason == "stop":
                return response.content
            elif response.finish_reason == "tool_calls":
                for call in response.tool_calls:
                    result = self.tools[call.name].run(**call.args)
                    messages.append({
                        "role": "tool", 
                        "tool_call_id": call.id,
                        "content": result
                    })
```

### 2024：工具生態爆發

2024 年，工具使用成為 LLM 應用的標準模式：

- **MCP（Model Context Protocol）**：Anthropic 提出的標準化工具協議
- **OpenAI GPTs**：自定義工具和知識庫
- **LangChain Tools**：超過 100 種預建工具整合
- **自定義 API 工具**：任何 REST API 都可以包裝為 LLM 工具

### 2025-2026：動態工具發現

模型不再使用預先註冊的工具，而是**動態發現和使用工具**：

```python
class DynamicToolDiscovery:
    def discover_tools(self, api_docs):
        # 模型閱讀 API 文件，自動理解如何使用
        for doc in api_docs:
            tool = self.llm.analyze_api_doc(doc)
            self.tool_registry[tool.name] = tool

    def use_tool(self, task):
        # 模型自主選擇合適的工具
        needed = self.llm.plan_tool_usage(task)
        for step in needed:
            tool = self.tool_registry[step.tool]
            result = tool(**step.args)
```

### 2027-2028：工具組合與工作流程

多工具協同完成複雜任務：

```python
def multi_tool_pipeline(goal):
    # 搜索 → 提取 → 計算 → 視覺化
    raw_data = search_tool.run(goal)
    structured = extractor_tool.run(raw_data)
    analyzed = calculator_tool.run(structured)
    report = visualization_tool.run(analyzed)
    return report
```

### 安全挑戰

工具使用帶來了新的安全問題：

1. **權限控制**：模型不應該能夠刪除檔案或發送郵件
2. **注入攻擊**：惡意輸入可能誘導模型執行危險操作
3. **成本控制**：API 呼叫次數和 Token 消耗需要監控

```python
# 安全工具包裝
class SafeToolWrapper:
    def __init__(self, tool, permissions):
        self.tool = tool
        self.permissions = permissions
        self.call_limit = RateLimiter(100, "hour")

    def run(self, **kwargs):
        if not self.permissions.check(kwargs):
            return "錯誤：無權限執行此操作"
        if not self.call_limit.allow():
            return "錯誤：已超過呼叫限制"
        return self.tool.run(**kwargs)
```

### 小結

工具使用將生成式 AI 從「文字生成器」轉變為「行動執行者」。Function Calling 的出現標誌著 LLM 開始具備與外部世界互動的能力。

---

**下一步**：[程式碼執行與沙箱技術](focus4.md)

## 延伸閱讀

- [OpenAI Function Calling 官方文件](https://www.google.com/search?q=OpenAI+function+calling+guide)
- [MCP: Model Context Protocol](https://www.google.com/search?q=Anthropic+Model+Context+Protocol+MCP)
- [LLM 工具使用的安全問題](https://www.google.com/search?q=LLM+tool+use+security+vulnerabilities)
