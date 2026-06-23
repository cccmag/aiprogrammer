# Function Calling 設計模式

## 從提示工程到工具使用

Function Calling 讓 LLM 不只是生成文字，還能呼叫外部 API。核心流程：模型收到使用者問題 → 決定呼叫哪個函式 → 解析參數 → 執行並回傳結果。

## 基本實作

```python
import json

functions = [
    {
        "name": "get_weather",
        "description": "查詢指定城市的當前天氣",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    }
]

def call_llm_with_tools(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        functions=functions
    )
    if response.choices[0].finish_reason == "function_call":
        func = response.choices[0].message.function_call
        return execute_function(func.name, json.loads(func.arguments))
    return response.choices[0].message.content
```

## 工具註冊器模式

```python
class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, schema, handler):
        self._tools[name] = {"schema": schema, "handler": handler}

    def call(self, name, **kwargs):
        return self._tools[name]["handler"](**kwargs)

registry = ToolRegistry()
registry.register("search_web", {...}, web_search)
registry.register("calculate", {...}, calculator)
```

## 錯誤處理策略

- 參數缺失：要求模型補齊 required 欄位
- 執行失敗：回傳錯誤訊息讓模型重新生成
- 遞迴呼叫：限制 max_tool_calls 防止無限循環

Function Calling 是 Agent 系統的基礎，更多設計細節請見 https://www.google.com/search?q=LLM+function+calling+design+patterns。
