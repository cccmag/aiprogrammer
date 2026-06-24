# 工作流版本控制

## 1. 引言

工作流不是一次性產物。隨著業務需求變化、提示詞最佳化與 Agent 行為調整，工作流需要像應用程式一樣進行版本管理。良好的版本控制策略能讓團隊安心迭代、快速回滾與稽核變更。

## 2. 程式碼層級版本控制

工作流定義本身就是程式碼，應納入 Git 管理。

```python
# workflow_v1.py
from dataclasses import dataclass
from typing import Protocol

class WorkflowVersion(Protocol):
    version: str
    def execute(self, input_data: dict) -> dict: ...

@dataclass
class WorkflowV1:
    version: str = "1.0.0"

    async def execute(self, input_data: dict) -> dict:
        # 舊版邏輯：直接呼叫單一 LLM
        return {"result": "v1_result", "version": self.version}

@dataclass
class WorkflowV2:
    version: str = "2.0.0"

    async def execute(self, input_data: dict) -> dict:
        # 新版邏輯：先分析再執行
        analysis = await self._analyze(input_data)
        return await self._execute_with_analysis(analysis)
```

## 3. 提示詞版本管理

提示詞是工作流的核心資產，需要獨立的版本控制。

```python
import hashlib
import json
from datetime import datetime

class PromptRegistry:
    def __init__(self):
        self.versions: dict[str, list[dict]] = {}

    def register(
        self, name: str, prompt: str, metadata: dict = None
    ) -> str:
        version_id = hashlib.sha256(
            prompt.encode()
        ).hexdigest()[:12]
        entry = {
            "version": version_id,
            "prompt": prompt,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
        }
        if name not in self.versions:
            self.versions[name] = []
        self.versions[name].append(entry)
        return version_id

    def get_latest(self, name: str) -> dict:
        return self.versions[name][-1]

    def get_version(self, name: str, version_id: str) -> dict:
        for v in self.versions.get(name, []):
            if v["version"] == version_id:
                return v
        raise KeyError(f"版本 {version_id} 不存在")

    def diff(self, name: str, v1: str, v2: str) -> str:
        p1 = self.get_version(name, v1)["prompt"]
        p2 = self.get_version(name, v2)["prompt"]
        # 簡易差異輸出
        return f"差異長度: {len(p2) - len(p1)} chars"
```

## 4. A/B 測試路由

```python
import random

class WorkflowRouter:
    def __init__(self):
        self.routes: dict[str, list[dict]] = {}

    def add_route(
        self,
        workflow_name: str,
        version: WorkflowVersion,
        traffic: float = 0.0,
    ) -> None:
        if workflow_name not in self.routes:
            self.routes[workflow_name] = []
        self.routes[workflow_name].append({
            "version": version,
            "traffic": traffic,
        })

    def route(self, workflow_name: str) -> WorkflowVersion:
        routes = self.routes.get(workflow_name, [])
        if not routes:
            raise ValueError(f"無路由: {workflow_name}")
        total = sum(r["traffic"] for r in routes)
        if total <= 0:
            return routes[0]["version"]
        r = random.uniform(0, total)
        cumulative = 0.0
        for route in routes:
            cumulative += route["traffic"]
            if r <= cumulative:
                return route["version"]
        return routes[-1]["version"]

# A/B 測試範例
router = WorkflowRouter()
router.add_route("data_pipeline", WorkflowV1(), traffic=0.3)
router.add_route("data_pipeline", WorkflowV2(), traffic=0.7)
selected = router.route("data_pipeline")
```

## 5. 資料版本記錄

```python
@dataclass
class ExecutionRecord:
    workflow_name: str
    workflow_version: str
    prompt_versions: dict[str, str]
    input_hash: str
    output: dict
    duration_ms: float
    success: bool

class ExecutionLogger:
    def __init__(self):
        self.records: list[ExecutionRecord] = []

    def log(
        self,
        workflow: WorkflowVersion,
        prompt_registry: PromptRegistry,
        input_data: dict,
        output_data: dict,
        duration: float,
        success: bool,
    ) -> None:
        input_hash = hashlib.sha256(
            json.dumps(input_data, sort_keys=True).encode()
        ).hexdigest()[:12]
        record = ExecutionRecord(
            workflow_name=type(workflow).__name__,
            workflow_version=getattr(
                workflow, "version", "unknown"
            ),
            prompt_versions={
                name: prompt_registry.get_latest(name)["version"]
                for name in prompt_registry.versions
            },
            input_hash=input_hash,
            output=output_data,
            duration_ms=duration,
            success=success,
        )
        self.records.append(record)
```

## 6. 回滾策略

```python
class RollbackManager:
    def __init__(self, router: WorkflowRouter):
        self.router = router
        self.deployment_history: list[dict] = []

    def deploy(self, version: WorkflowVersion) -> None:
        self.deployment_history.append({
            "version": version.version,
            "timestamp": datetime.utcnow().isoformat(),
        })
        self.router.add_route("default", version, traffic=1.0)

    def rollback(self, steps: int = 1) -> WorkflowVersion:
        if len(self.deployment_history) <= steps:
            raise ValueError("無足夠版本可回滾")
        target = self.deployment_history[-(steps + 1)]
        self.deploy(target["version"])
        return target["version"]
```

## 7. 實務建議

- **工作流即程式碼**：所有定義納入 Git 審查
- **提示詞獨立版本**：與程式碼分開管理，方便非工程師協作
- **逐步釋出**：透過 A/B 測試降低風險
- **記錄每個執行版本**：確保可重現與稽核

---

**參考資料**
- [工作流版本管理策略](https://www.google.com/search?q=workflow+versioning+strategy+best+practices)
- [提示詞版本控制工具](https://www.google.com/search?q=prompt+version+management+LLM+workflow)
- [A/B 測試與金絲雀部署](https://www.google.com/search?q=canary+deployment+A+B+testing+workflow)
