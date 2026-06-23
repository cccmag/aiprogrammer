# 程式碼執行 Agent 設計

## Agent 核心循環

程式碼執行 Agent 的典型流程：接收任務 → 生成程式碼 → 執行 → 讀取輸出 → 迭代修正。

## 基礎實作

```python
import subprocess
import tempfile

class CodeAgent:
    def __init__(self, llm):
        self.llm = llm
        self.history = []

    def run(self, task, max_iter=5):
        for i in range(max_iter):
            code = self.llm.generate(self._build_prompt(task))
            result = self._execute(code)
            self.history.append({"code": code, "result": result})
            if self._is_success(result):
                return code
            task = f"修正錯誤：{result}"
        return None

    def _execute(self, code):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.flush()
            try:
                out = subprocess.run(
                    ['python3', f.name],
                    capture_output=True, text=True, timeout=30
                )
                return out.stdout or out.stderr
            except subprocess.TimeoutExpired:
                return "執行超時"
```

## 安全隔離與沙箱

在 production 環境應使用 Docker 或 gVisor 隔離：

```python
def execute_safe(code):
    with tempfile.NamedTemporaryFile(suffix='.py') as f:
        f.write(code.encode())
        f.flush()
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{f.name}:/code/script.py",
             "python:3.11-slim", "python", "/code/script.py"],
            capture_output=True, text=True, timeout=60
        )
        return result.stdout
```

## 錯誤分類與修復策略

Agent 需區分語法錯誤（直接修正）、執行時錯誤（補 try-except）與邏輯錯誤（重寫演算法）。每次迭代應收斂而非發散。

參考 https://www.google.com/search?q=code+execution+agent+LLM+design 獲取更多設計模式。
