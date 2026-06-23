# Agent 工作流設計模式（2023-2029）

## 七種經過驗證的模式

### 前言

隨著 LLM 能力的提升，開發者總結出幾種可重複使用的工作流設計模式。每種模式在特定場景下最有效。

### 模式一：Prompt 鏈（Chain）

最簡單的模式——將任務分解為線性步驟：

```python
# Prompt Chain
def chain_pipeline(inputs):
    step1 = llm(f"步驟1：{inputs}")
    step2 = llm(f"步驟2：{step1}")
    step3 = llm(f"步驟3：{step2}")
    return step3
```

適合：文件摘要、翻譯管線。

### 模式二：路由（Router）

根據輸入類型動態選擇處理路徑：

```python
# Router Pattern
def router(input_text):
    category = llm(f"分類以下文本：{input_text}")
    handlers = {"技術": tech_handler, "商業": biz_handler, "學術": academic_handler}
    return handlers[category](input_text)
```

### 模式三：平行化（Parallelization）

同時執行多個獨立任務：

```python
# Parallel Execution
def parallel_research(topics):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as pool:
        results = pool.map(lambda t: llm(f"研究：{t}"), topics)
    return list(results)
```

### 模式四：評審循環（Judge-Critic）

LLM 自我改進的基礎模式：

```python
# Judge-Critic Loop
def improve_code(code):
    for _ in range(3):
        critique = llm(f"審查以下程式碼：{code}")
        code = llm(f"根據建議改進：{critique}\n\n原始程式碼：{code}")
    return code
```

### 模式五：工具使用（Tool Use）

Agent 呼叫外部工具的標準模式：

```python
# Tool Use Pattern
tools = {"搜尋": search_web, "計算": calculator, "讀取": read_file}
def tool_agent(task):
    tool_name = llm(f"選擇工具：{tools.keys()}，任務：{task}")
    return tools[tool_name](task)
```

### 模式六：反射（Reflection）

Agent 回顧和修正自己的輸出：

```python
# Reflection Pattern
def reflective_agent(task):
    output = llm(task)
    reflection = llm(f"評估你的輸出：{output}。哪裡可以改進？")
    return llm(f"根據反思重新生成：{reflection}\n\n任務：{task}")
```

### 模式七：記憶（Memory）

具有長期記憶的 Agent，能在多次互動中學習：

```python
# Memory Pattern
class MemoryAgent:
    def __init__(self):
        self.memory = []
    def run(self, task):
        context = self.get_relevant_memory(task)
        response = llm(f"記憶：{context}\n任務：{task}")
        self.memory.append({"task": task, "response": response})
        return response
```

### 小結

這七種模式構成了現代 Agent 工作流的基礎。實際應用中通常混合使用多種模式。

---

**下一步**：[工作流編排引擎](focus3.md)

## 延伸閱讀

- [LLM 應用設計模式](https://www.google.com/search?q=LLM+application+design+patterns+agent)
- [Anthropic 工作流模式](https://www.google.com/search?q=Anthropic+agent+workflow+patterns)
- [多模式 Agent 系統](https://www.google.com/search?q=multi+modal+agent+workflow+design)
