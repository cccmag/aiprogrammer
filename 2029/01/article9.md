# 工作流成本最佳化

## 1. 引言

LLM API 的成本隨用量線性成長——一個未經最佳化的工作流每天可能消耗數百美元。成本最佳化不是事後補救，而應從設計階段就納入考量。

## 2. Token 用量監控

```python
from dataclasses import dataclass, field

@dataclass
class TokenAccount:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_cost: float = 0.0

class TokenTracker:
    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},   # 每百萬 token
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
    }

    def __init__(self):
        self.accounts: dict[str, TokenAccount] = {}

    def record(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> float:
        if model not in self.accounts:
            self.accounts[model] = TokenAccount()
        account = self.accounts[model]
        account.prompt_tokens += prompt_tokens
        account.completion_tokens += completion_tokens
        pricing = self.PRICING.get(model, {"input": 1.0, "output": 2.0})
        cost = (
            prompt_tokens * pricing["input"]
            + completion_tokens * pricing["output"]
        ) / 1_000_000
        account.total_cost += cost
        return cost
```

## 3. 模型選擇策略

```python
class ModelSelector:
    def __init__(self, tracker: TokenTracker):
        self.tracker = tracker

    def select_model(self, task_difficulty: str) -> str:
        mapping = {
            "simple": "gpt-4o-mini",    # $0.15/M tokens
            "medium": "claude-3-haiku",  # $0.25/M tokens
            "complex": "gpt-4o",         # $2.50/M tokens
        }
        return mapping.get(task_difficulty, "gpt-4o-mini")

    async def classify_difficulty(
        self, task: str
    ) -> str:
        # 使用快速便宜的模型判斷難度
        # ...
        return "medium"
```

## 4. 快取策略

```python
import hashlib
import json
from functools import lru_cache

class ResponseCache:
    def __init__(self, maxsize: int = 1000):
        self.cache: dict[str, str] = {}
        self.maxsize = maxsize
        self.hits = 0
        self.misses = 0

    def _make_key(self, prompt: str, model: str) -> str:
        return hashlib.sha256(
            f"{model}:{prompt}".encode()
        ).hexdigest()

    def get(self, prompt: str, model: str) -> str | None:
        key = self._make_key(prompt, model)
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def set(self, prompt: str, model: str, response: str) -> None:
        key = self._make_key(prompt, model)
        if len(self.cache) >= self.maxsize:
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = response

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
```

## 5. 批次處理

```python
import asyncio

class BatchProcessor:
    def __init__(self, max_batch_size: int = 10):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.max_batch_size = max_batch_size
        self.batch_interval = 0.5  # 秒

    async def submit(self, item: dict) -> asyncio.Future:
        future = asyncio.get_event_loop().create_future()
        await self.queue.put((item, future))
        return future

    async def _batch_loop(self) -> None:
        while True:
            batch = []
            deadline = asyncio.get_event_loop().time() + self.batch_interval
            while len(batch) < self.max_batch_size:
                remain = deadline - asyncio.get_event_loop().time()
                if remain <= 0:
                    break
                try:
                    item, future = await asyncio.wait_for(
                        self.queue.get(), timeout=remain
                    )
                    batch.append((item, future))
                except asyncio.TimeoutError:
                    break

            if batch:
                # 批次呼叫 LLM API
                prompts = [b[0]["prompt"] for b in batch]
                responses = await self._batch_call_llm(prompts)
                for (_, future), response in zip(batch, responses):
                    future.set_result(response)
```

批次處理可節省 30–50% 的 API 成本，因為供應商對批次請求提供折扣。

## 6. 提示詞壓縮

```python
class PromptCompressor:
    def __init__(self, max_context: int = 4000):
        self.max_context = max_context

    def compress(self, prompt: str, priority_sections: list[str]) -> str:
        if len(prompt) <= self.max_context:
            return prompt

        # 保留優先區段
        lines = prompt.split("\n")
        important = []
        for section in priority_sections:
            important.extend(
                l for l in lines if section in l
            )

        # 壓縮非優先內容
        compressed = []
        for line in lines:
            if line in important:
                compressed.append(line)
            elif len(line) > 100:
                compressed.append(line[:50] + "...")

        result = "\n".join(compressed)
        if len(result) > self.max_context:
            result = result[:self.max_context]
        return result
```

## 7. 成本儀表板

```python
class CostDashboard:
    def __init__(self, tracker: TokenTracker):
        self.tracker = tracker

    def daily_report(self) -> str:
        report = ["=== 成本日報 ==="]
        total = 0.0
        for model, account in self.tracker.accounts.items():
            subtotal = account.total_cost
            total += subtotal
            report.append(
                f"{model}: ${subtotal:.2f} "
                f"(輸入 {account.prompt_tokens:,} / "
                f"輸出 {account.completion_tokens:,} tokens)"
            )
        report.append(f"總計: ${total:.2f}")
        return "\n".join(report)

    def cost_per_task(self, task_id: str) -> float:
        return self.tracker.accounts.get(task_id, TokenAccount()).total_cost
```

## 8. 最佳化檢查清單

- [ ] 為不同任務選擇合適的模型（mini vs 全尺寸）
- [ ] 實作回應快取，避免重複查詢
- [ ] 批次處理非即時請求
- [ ] 壓縮冗長提示詞
- [ ] 設定每日成本上限警報
- [ ] 定期審查 token 使用報告

---

**參考資料**
- [LLM 成本估算與最佳化](https://www.google.com/search?q=LLM+API+cost+optimization+token+management)
- [提示詞壓縮技術](https://www.google.com/search?q=prompt+compression+LLM+cost+saving)
- [批次推論策略](https://www.google.com/search?q=batch+inference+LLM+API+discount)
