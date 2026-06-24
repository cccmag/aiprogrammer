# 程式實作：多代理協作框架

## 簡介

本實作從零建構一個多代理協作系統，展示 Agent 角色設計、訊息傳遞、工具使用和任務協調。完整程式碼在 `_code/multi_agent.py`。

## 核心元件

### 1. 訊息協議

Agent 之間透過結構化訊息溝通：

```python
@dataclass
class Message:
    sender: str       # 發送者
    receiver: str     # 接收者
    msg_type: str     # task / result / response / error
    content: str      # 內容
    task_id: str      # 任務 ID
```

### 2. Agent 角色

每個 Agent 有專門的角色定義：

```python
@dataclass
class Agent:
    name: str               # 名稱
    role: str               # 角色（project manager / coder / reviewer / tester）
    system_prompt: str      # 系統提示詞
    tools: ToolRegistry     # 可使用的工具
    inbox: list[Message]    # 收件匣
    memory: list[str]       # 互動記憶
```

### 3. 工具系統

Agent 透過 ToolRegistry 使用工具：

```python
registry = ToolRegistry()
registry.register("search_knowledge", "Search KB", lambda q: f"Results: {q}")
registry.register("calculate", "Do math", lambda expr: eval(expr))
```

### 4. Orchestrator 協調器

Orchestrator 管理訊息路由和工作流程：

```python
orchestrator.run_step("Alice", "Bob", "Write a calculator")
# 自動路由到 Bob → Bob 處理 → 回傳結果
```

## 工作流程範例

```
Alice (PM) → Bob (Coder): 寫計算機程式
Bob (Coder) → Carol (Reviewer): 審查程式碼
Carol (Reviewer) → Bob (Coder): 修復除零錯誤
Bob (Coder) → Dave (Tester): 測試修復
Dave (Tester) → Alice (PM): 全部通過
```

## 執行方式

```bash
cd _code
python3 multi_agent.py
```

## 延伸練習

1. **串接真實 LLM**：用 OpenAI/Claude API 替換 `llm_simulator`
2. **平行執行**：讓多個 Worker Agent 同時處理子任務
3. **動態任務分配**：Orchestrator 根據 Agent 負載分配任務
4. **持久化記憶**：將 Agent 記憶存入向量資料庫
5. **Web UI**：用 Streamlit 建立可視化 Agent 儀表板
