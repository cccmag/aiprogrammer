# 生產級部署最佳實踐

## 1. 引言

從 prototype 到 production，AI 工作流需要跨越多個關鍵障礙：可靠性、安全性、可擴展性與成本控制。本文總結生產級部署的必備實踐。

## 2. 容器化與編排

```python
# Dockerfile 範例
"""
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
```

```python
# Kubernetes 健康檢查端點
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float

start_time = __import__("time").time()

@app.get("/health")
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version="2.1.0",
        uptime_seconds=time.time() - start_time,
    )

@app.get("/ready")
async def readiness() -> dict:
    # 檢查 LLM API 連線
    try:
        await check_llm_connectivity()
        return {"ready": True}
    except Exception:
        return {"ready": False}
```

## 3. 安全配置管理

```python
import os
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class ProductionConfig:
    llm_api_key: str = field(repr=False)
    database_url: str = field(repr=False)
    log_level: str = "INFO"
    max_concurrent_workflows: int = 50
    workflow_timeout_seconds: int = 300

    @classmethod
    def from_env(cls) -> "ProductionConfig":
        required = ["LLM_API_KEY", "DATABASE_URL"]
        missing = [k for k in required if not os.getenv(k)]
        if missing:
            raise ValueError(f"缺少環境變數: {missing}")
        return cls(
            llm_api_key=os.environ["LLM_API_KEY"],
            database_url=os.environ["DATABASE_URL"],
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            max_concurrent_workflows=int(
                os.getenv("MAX_CONCURRENT", "50")
            ),
            workflow_timeout_seconds=int(
                os.getenv("TIMEOUT", "300")
            ),
        )

# 不要將 Secrets 寫入日誌
import logging
config = ProductionConfig.from_env()
logging.info("配置載入完成")
logging.debug(f"API Key 前 4 碼: {config.llm_api_key[:4]}...")
```

## 4. 背景任務佇列

```python
from celery import Celery

celery_app = Celery(
    "workflow",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
)

@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=10,
    acks_late=True,
)
def execute_workflow_task(
    self, workflow_name: str, input_data: dict
) -> dict:
    try:
        result = run_workflow(workflow_name, input_data)
        return result
    except Exception as exc:
        raise self.retry(exc=exc)
```

## 5. 優雅關機

```python
import signal
import asyncio

class GracefulShutdown:
    def __init__(self):
        self.shutdown_event = asyncio.Event()

    def install(self) -> None:
        for sig in (signal.SIGTERM, signal.SIGINT):
            asyncio.get_event_loop().add_signal_handler(
                sig, self._trigger_shutdown
            )

    def _trigger_shutdown(self) -> None:
        print("收到關機訊號，停止接受新任務...")
        self.shutdown_event.set()

    async def wait_for_shutdown(self) -> None:
        await self.shutdown_event.wait()
        print("正在等待進行中的工作流完成...")
        await asyncio.sleep(5)  # 等待進行中任務
        print("關機完成")

async def main():
    shutdown = GracefulShutdown()
    shutdown.install()
    await run_workflow_server()
    await shutdown.wait_for_shutdown()
```

## 6. 資源限制

```python
import resource
import sys

class ResourceGuard:
    def __init__(self):
        self.soft, self.hard = resource.getrlimit(
            resource.RLIMIT_AS
        )

    def set_memory_limit(self, max_bytes: int) -> None:
        resource.setrlimit(
            resource.RLIMIT_AS,
            (max_bytes, self.hard or max_bytes),
        )

    def set_time_limit(self, seconds: int) -> None:
        resource.setrlimit(
            resource.RLIMIT_CPU,
            (seconds, self.hard or seconds + 1),
        )

    @staticmethod
    def watchdog(timeout: int):
        """工作流超時守衛"""
        async def _watch(coro, timeout):
            try:
                return await asyncio.wait_for(coro, timeout=timeout)
            except asyncio.TimeoutError:
                raise TimeoutError(f"工作流超過 {timeout}s 限制")
        return _watch
```

## 7. 監控與警報整合

```python
class AlertManager:
    def __init__(self, webhook_url: str):
        self.webhook = webhook_url

    async def alert_on_failure(
        self, workflow: str, error: str
    ) -> None:
        payload = {
            "title": f"工作流失敗: {workflow}",
            "message": str(error)[:500],
            "severity": "critical",
            "timestamp": time.time(),
        }
        async with httpx.AsyncClient() as client:
            await client.post(self.webhook, json=payload)
```

## 8. 檢查清單

- [ ] Secrets 使用環境變數或 Secrets Manager
- [ ] 設定資源限制與超時
- [ ] 實作健康檢查端點
- [ ] 容器化並設定 resource request/limit
- [ ] 配置優雅關機
- [ ] 使用背景佇列處理非同步任務
- [ ] 設定自動擴展策略
- [ ] 監控與警報就緒

---

**參考資料**
- [12 Factor App 與工作流](https://www.google.com/search?q=12+factor+app+workflow+deployment)
- [Kubernetes 生產最佳實踐](https://www.google.com/search?q=Kubernetes+production+best+practices+workload)
- [Celery 任務佇列](https://www.google.com/search?q=Celery+distributed+task+queue+Python)
