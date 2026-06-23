# 沙箱安全設計

## 為什麼需要沙箱

程式碼執行 Agent 若無安全限制，可能造成檔案刪除、命令注入、資訊外洩等嚴重後果。沙箱提供隔離執行環境。

## 沙箱等級

| 等級 | 隔離方式 | 適用場景 |
|------|----------|----------|
| L0 | 純文字生成，不執行程式碼 | 原型驗證 |
| L1 | subprocess + timeout | 個人使用 |
| L2 | Docker 容器 | 團隊協作 |
| L3 | gVisor / Firecracker | 生產環境 |

## Docker 沙箱實作

```python
import docker

class DockerSandbox:
    def __init__(self):
        self.client = docker.from_env()
        self.image = "python:3.11-slim"
        self.allowed_imports = {"math", "json", "csv", "re", "collections"}

    def execute(self, code):
        # 注入安全策略
        wrapper = f"""
import sys
{self._build_safety_policy()}

{code}
"""
        container = self.client.containers.run(
            self.image,
            f"python -c '{wrapper}'",
            mem_limit="256m",
            cpu_period=100000,
            cpu_quota=50000,
            network_disabled=True,
            read_only=True,
            remove=True,
            timeout=30
        )
        return container.decode()

    def _build_safety_policy(self):
        return """
def __builtins_check__(name):
    denied = {'eval', 'exec', 'compile', '__import__', 'open'}
    if name in denied:
        raise SecurityError(f'禁止呼叫: {name}')
"""
```

## 資源限制策略

- CPU: 限制 cgroup cpu_quota
- 記憶體: mem_limit
- 網路: 預設關閉，白名單開放
- 檔案系統: read-only root，唯寫 /tmp
- 系統呼叫: seccomp 過濾

## 安全檢查清單

禁止 os.system、subprocess、socket、ctypes 等模組。對所有輸出做消毒後才回傳給上層。詳見 https://www.google.com/search?q=LLM+code+sandbox+security。
