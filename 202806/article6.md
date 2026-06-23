# 推論服務水平擴展

## 單節點瓶頸

當 LLM 推論服務的使用者從個位數成長到數百人時，單一 GPU 很快就達到極限：

- **GPU 記憶體**：LLaMA-70B 至少需 140 GB（FP16），單張 A100 80GB 放不下
- **計算吞吐**：單卡每秒最多處理數十個 token
- **佇列延遲**：請求堆積時，尾延遲（tail latency）暴增

## 水平擴展架構

```python
import asyncio
import random

class InferenceRouter:
    """Simple load balancer for inference workers"""

    def __init__(self, workers):
        self.workers = workers  # List of (host, port, capacity)

    def select_worker(self, prompt_len: int):
        """Select least-loaded worker"""
        available = [w for w in self.workers if w[2] > prompt_len]
        return min(available, key=lambda w: w[2]) if available else None

    async def dispatch(self, prompt: str):
        worker = self.select_worker(len(prompt))
        if worker is None:
            return {"error": "all workers busy"}
        host, port, _ = worker
        result = await self.call_worker(host, port, prompt)
        self.workers[self.workers.index(worker)] = (
            host, port, worker[2] - len(prompt))
        return result

    async def call_worker(self, host, port, prompt):
        await asyncio.sleep(0.1)  # simulated inference
        return f"result_{len(prompt)}"
```

## 請求排隊策略

```python
from collections import deque

class RequestQueue:
    def __init__(self, max_concurrent=4):
        self.queue = deque()
        self.active = 0
        self.max_active = max_concurrent

    async def enqueue(self, request):
        self.queue.append(request)
        return await self.schedule()

    async def schedule(self):
        while self.active >= self.max_active:
            await asyncio.sleep(0.01)

        request = self.queue.popleft()
        self.active += 1
        try:
            return await self.process(request)
        finally:
            self.active -= 1

    async def process(self, request):
        """Simulate model inference with dynamic batching"""
        await asyncio.sleep(random.uniform(0.05, 0.2))
        return f"processed: {request}"
```

## 張量並行與管線並行

多卡部署需要分散式推理策略：

```python
def simulate_tensor_parallel(shard_count: int, hidden_dim: int):
    """Simulate tensor parallelism across GPUs"""
    shard_size = hidden_dim // shard_count
    all_reduce_cost = 0.1 * shard_count  # communication overhead
    compute_cost = 1.0 / shard_count     # linear speedup
    total_cost = compute_cost + all_reduce_cost
    print(f"TP-{shard_count}: compute={compute_cost:.3f}, "
          f"comm={all_reduce_cost:.3f}, total={total_cost:.3f}")
    return 1.0 / total_cost

for s in [1, 2, 4, 8]:
    simulate_tensor_parallel(s, 8192)
```

## 部署方案比較

| 方案 | 擴展性 | 複雜度 | 適用場景 |
|------|-------|-------|---------|
| 單卡 + 排隊 | 低 | 低 | 原型驗證 |
| 水平擴展 + LB | 高 | 中 | 生產服務 |
| 張量並行 | 中 | 高 | 超大模型 |

## 延伸閱讀

- [vLLM 分散式推理](https://www.google.com/search?q=vLLM+distributed+inference)
- [TensorRT LLM 多卡部署](https://www.google.com/search?q=TensorRT+LLM+multi+GPU)
- [LLM 服務架構模式](https://www.google.com/search?q=LLM+serving+architecture+patterns)

水平擴展是處理大規模推論請求的核心手段。搭配智慧路由、請求排隊、以及張量並行，可以從單卡服務平滑過渡到數百卡的大型推理叢集。
