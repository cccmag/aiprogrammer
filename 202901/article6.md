# 平行執行與資源管理

## 1. 引言

AI 工作流常需同時處理大量任務——平行分析多份文件、同時呼叫多個 LLM、或並行執行資料處理。有效的資源管理能最大化吞吐量，同時避免 API 速率限制與記憶體爆炸。

## 2. 執行緒池與 Semaphore 控制

```python
import asyncio
from typing import Callable, Any

class RateLimitedExecutor:
    def __init__(
        self, max_concurrent: int = 5, rate_limit: int = 10
    ):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.rate_limit = rate_limit
        self._request_times: list[float] = []

    async def execute(
        self, task_id: str, func: Callable, *args, **kwargs
    ) -> Any:
        async with self.semaphore:
            await self._wait_for_rate_limit()
            print(f"[執行] 任務 {task_id} 開始")
            result = await func(*args, **kwargs)
            print(f"[執行] 任務 {task_id} 完成")
            return result

    async def _wait_for_rate_limit(self) -> None:
        now = asyncio.get_event_loop().time()
        self._request_times = [
            t for t in self._request_times
            if now - t < 1.0
        ]
        if len(self._request_times) >= self.rate_limit:
            wait = 1.0 - (now - self._request_times[0])
            if wait > 0:
                await asyncio.sleep(wait)
        self._request_times.append(now)
```

## 3. 動態併發調整

```python
class AdaptiveConcurrencyController:
    def __init__(
        self,
        min_concurrent: int = 1,
        max_concurrent: int = 20,
        target_latency_ms: float = 2000.0,
    ):
        self.current = min_concurrent
        self.min_concurrent = min_concurrent
        self.max_concurrent = max_concurrent
        self.target_latency = target_latency_ms
        self.latency_history: list[float] = []

    def adjust(self, recent_latency_ms: float) -> int:
        self.latency_history.append(recent_latency_ms)
        if len(self.latency_history) > 10:
            self.latency_history.pop(0)

        avg_latency = sum(self.latency_history) / len(self.latency_history)

        if avg_latency < self.target_latency * 0.7:
            self.current = min(self.current + 1, self.max_concurrent)
        elif avg_latency > self.target_latency:
            self.current = max(self.current - 1, self.min_concurrent)

        print(f"[調整] 平均延遲 {avg_latency:.0f}ms → 併發數 {self.current}")
        return self.current
```

## 4. 工作排程器

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class WorkItem:
    id: str
    priority: int
    payload: dict

class PriorityScheduler:
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue()

    async def submit(self, item: WorkItem) -> None:
        await self.queue.put((item.priority, item))

    async def worker_loop(self) -> None:
        while True:
            _, item = await self.queue.get()
            try:
                print(f"[處理] 優先級 {item.priority}: {item.id}")
                await self._process(item)
            except Exception as e:
                print(f"[錯誤] {item.id}: {e}")
            finally:
                self.queue.task_done()

    async def start(self) -> None:
        self.workers = [
            asyncio.create_task(self.worker_loop())
            for _ in range(self.max_workers)
        ]
```

## 5. 資源隔離與配額

```python
class ResourcePool:
    def __init__(self, max_memory_mb: int = 1024):
        self.max_memory = max_memory_mb
        self.allocated: dict[str, int] = {}

    async def acquire(
        self, task_id: str, memory_mb: int
    ) -> bool:
        if sum(self.allocated.values()) + memory_mb > self.max_memory:
            return False
        self.allocated[task_id] = memory_mb
        return True

    def release(self, task_id: str) -> None:
        self.allocated.pop(task_id, None)

class TaskGroupManager:
    def __init__(self, pool: ResourcePool):
        self.pool = pool

    async def run_with_constraints(
        self, tasks: list[dict]
    ) -> list[Any]:
        results = []
        for task in tasks:
            if await self.pool.acquire(
                task["id"], task.get("memory_mb", 128)
            ):
                try:
                    result = await self._execute(task)
                    results.append(result)
                finally:
                    self.pool.release(task["id"])
        return results
```

## 6. LLM API 速率限制處理

```python
class TokenBucketRateLimiter:
    def __init__(self, rps: float = 10, burst: int = 20):
        self.tokens = burst
        self.burst = burst
        self.refill_rate = rps
        self.last_refill = time.time()

    async def acquire(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(
            self.burst,
            self.tokens + elapsed * self.refill_rate,
        )
        self.last_refill = now

        if self.tokens < 1:
            wait = (1 - self.tokens) / self.refill_rate
            await asyncio.sleep(wait)
            self.tokens = 0
        else:
            self.tokens -= 1
```

## 7. 實務建議

- **Semaphore + 速率限制**：雙層控制避免 API 封鎖
- **自適應演算法**：根據實際延遲動態調整併發數
- **優先級排程**：重要任務優先取得資源
- **記憶體配額**：防止工作流消耗過多記憶體

---

**參考資料**
- [asyncio Semaphore 並發控制](https://www.google.com/search?q=asyncio+Semaphore+concurrency+control+Python)
- [Token Bucket 速率限制演算法](https://www.google.com/search?q=token+bucket+rate+limiting+algorithm)
- [自適應併發控制](https://www.google.com/search?q=adaptive+concurrency+control+distributed+systems)
