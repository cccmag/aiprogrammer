# 程式實作：Agent 工作流引擎

## 簡介

本實作建構一個輕量級 Agent 工作流引擎，支援工作流註冊、步驟執行、重試機制、時間測量與執行歷史記錄。完整程式碼在 `_code/workflow_engine.py`。

## 核心元件

### 1. 工作流步驟

```python
@dataclass
class WorkflowStep:
    name: str
    action: Callable
    retry_count: int = 0
    max_retries: int = 3
    timeout: float = 30.0
```

### 2. 工作流引擎

```python
engine = WorkflowEngine()
engine.register(wf)
result = engine.run("content_pipeline")
```

### 3. 內容管線範例

```python
wf = Workflow("content_pipeline", [
    WorkflowStep("research", lambda ctx: research(ctx)),
    WorkflowStep("draft", lambda ctx: draft(ctx)),
    WorkflowStep("review", lambda ctx: review(ctx), max_retries=2),
    WorkflowStep("publish", lambda ctx: publish(ctx)),
])
```

## 執行方式

```bash
cd _code
python3 workflow_engine.py
```

## 延伸練習

1. **新增步驟類型**：加入平行執行步驟（Fan-out / Fan-in）
2. **人機協作點**：實作 Human-in-the-Loop 暫停與恢復機制
3. **持久化儲存**：將工作流狀態儲存到 SQLite 或 Redis
4. **分散式執行**：支援多 Worker 平行執行工作流
5. **Web 儀表板**：用 FastAPI 建立工作流執行視覺化介面
