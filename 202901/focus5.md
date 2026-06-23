# 錯誤處理與恢復策略（2024-2029）

## 讓 Agent 系統優雅地失敗

### 前言

LLM 本質上是不確定的——同樣的輸入可能產生不同的輸出。這使得 Agent 工作流的錯誤處理成為核心挑戰。

### Try-Except 模式

最直接的錯誤處理：

```python
# 基本錯誤處理
def safe_agent(task):
    try:
        return llm(task)
    except LLMError as e:
        return fallback_response(f"LLM 暫不可用：{e}")
    except ValueError as e:
        return handle_invalid_input(task)
```

### Retry with Backoff

LLM 調用失敗時的重試策略：

```python
# 指數退避重試
def retry_with_backoff(task, max_retries=3):
    for attempt in range(max_retries):
        try:
            return llm(task)
        except RateLimitError:
            wait = 2 ** attempt
            time.sleep(wait)
    raise MaxRetriesExceeded(task)
```

### 驗證與回退（Validation & Fallback）

驗證 LLM 輸出格式，無效時回退：

```python
# 輸出驗證 + 回退
def validated_llm(task, output_schema):
    for _ in range(3):
        result = llm(task)
        if validate(result, output_schema):
            return result
    # 全部失敗，使用預設值回退
    return output_schema.default()
```

### 分支恢復（Branch Recovery）

工作流中某一步失敗時，走備用分支：

```python
# 分支恢復
def branch_recovery_workflow(task):
    # 主路徑
    result = main_path(task)
    if not is_valid(result):
        logger.warn(f"主路徑失敗，切換備份路徑")
        result = backup_path(task)
    if not is_valid(result):
        return human_escalation(task)
    return result
```

### 檢查點機制

2027 年後，長時間工作流普遍使用檢查點：

```python
# Checkpoint-based recovery
class CheckpointWorkflow:
    def __init__(self):
        self.checkpoints = {}
    
    def step(self, step_name, fn, *args):
        if step_name in self.checkpoints:
            return self.checkpoints[step_name]
        result = fn(*args)
        self.checkpoints[step_name] = result
        return result

wf = CheckpointWorkflow()
wf.step("research", research_agent, topic)
wf.step("write", write_agent, wf.checkpoints["research"])
```

### 錯誤分類與處理矩陣

| 錯誤類型 | 處理策略 | 恢復時間 |
|---------|---------|---------|
| LLM 超時 | 重試（指數退避） | 數秒 |
| 輸出格式錯誤 | 重新生成 + 驗證 | 即時 |
| 工具調用失敗 | 切換備用工具 | 即時 |
| 邏輯不一致 | 反思循環修正 | 1-3 輪 |
| 安全違規 | 立即停止 + 人工審查 | 即時 |

### 小結

錯誤處理的核心原則：**快速失敗、優雅恢復、人類兜底**。

---

**下一步**：[工作流監控與最佳化](focus6.md)

## 延伸閱讀

- [LLM 應用的錯誤處理](https://www.google.com/search?q=LLM+application+error+handling+strategies)
- [Agent 系統可靠性設計](https://www.google.com/search?q=reliable+agent+system+design+patterns)
- [工作流恢復機制](https://www.google.com/search?q=workflow+recovery+checkpoint+LLM)
