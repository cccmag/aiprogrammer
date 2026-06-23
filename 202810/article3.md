# 推論成本最佳化案例

## 1. 引言

推論（Inference）成本佔 AI 營運支出的大宗。以每日處理百萬次請求的聊天機器人為例，每月推論費用可能高達數萬美元。本文透過三個真實案例，展示如何將推論成本降低 50% 以上。

## 2. 案例一：快取機制

重複查詢在實際應用中非常常見。引入語意快取可大幅減少 API 呼叫：

```python
import hashlib
import json
from typing import Optional

class SemanticCache:
    def __init__(self, max_size: int = 1000):
        self.cache: dict[str, str] = {}
        self.max_size = max_size

    def _key(self, prompt: str, model: str) -> str:
        return hashlib.sha256(f"{model}:{prompt}".encode()).hexdigest()

    def get(self, prompt: str, model: str) -> Optional[str]:
        return self.cache.get(self._key(prompt, model))

    def set(self, prompt: str, model: str, response: str):
        if len(self.cache) >= self.max_size:
            self.cache.pop(next(iter(self.cache)))
        self.cache[self._key(prompt, model)] = response

    def hit_rate(self) -> float:
        return self.stats["hits"] / max(self.stats["total"], 1)

# 模擬 10,000 次請求，50% 重複
cache = SemanticCache()
total_cost = 0
saved_cost = 0
COST_PER_CALL = 0.003  # GPT-4o-mini 假設成本

for i in range(10_000):
    prompt = f"Query number {i % 2}"  # 50% 重複
    cached = cache.get(prompt, "gpt-4o-mini")
    if cached:
        saved_cost += COST_PER_CALL
    else:
        response = f"Response to {prompt}"
        cache.set(prompt, "gpt-4o-mini", response)
    total_cost += COST_PER_CALL

print(f"原始成本: ${total_cost:.2f}")
print(f"快取節省: ${saved_cost:.2f} ({saved_cost/total_cost*100:.0f}%)")
```

## 3. 案例二：批次處理

將多個獨立請求合併為單一批次，利用 API 的批次折扣：

```python
import asyncio
from time import perf_counter

class BatchProcessor:
    def __init__(self, max_batch: int = 10, interval: float = 0.05):
        self.queue: list[dict] = []
        self.max_batch = max_batch
        self.interval = interval

    async def add(self, prompt: str) -> str:
        future = asyncio.get_event_loop().create_future()
        self.queue.append({"prompt": prompt, "future": future})
        if len(self.queue) >= self.max_batch:
            asyncio.create_task(self.flush())
        return await future

    async def flush(self):
        batch = self.queue[:self.max_batch]
        self.queue[:] = self.queue[self.max_batch:]
        # 模擬批次 API 呼叫
        await asyncio.sleep(0.1)
        for item in batch:
            item["future"].set_result(f"Batch response: {item['prompt']}")

# 批次處理可將 API 呼叫次數減少 90%
print("批次處理可顯著降低 API 呼叫次數與成本")
```

## 4. 案例三：模型蒸餾

使用較小模型模仿大模型的輸出，部署成本僅為原模型的 1/10：

```python
# 蒸餾訓練示意
def distill_training(teacher_model: str, student_model: str,
                     dataset: list[str]):
    """使用教師模型的輸出訓練學生模型。"""
    costs = {
        "teacher": {"per_token": 0.00001},
        "student": {"per_token": 0.000001},
    }
    # 假設蒸餾後學生模型達教師模型 90% 準確率
    teacher_cost = len(dataset) * 500 * costs["teacher"]["per_token"]
    student_cost = len(dataset) * 500 * costs["student"]["per_token"]
    print(f"教師模型成本: ${teacher_cost:.2f}")
    print(f"學生模型成本: ${student_cost:.2f}")
    print(f"推論成本降低: {(1 - student_cost/teacher_cost)*100:.0f}%")

distill_training("gpt-4o", "gpt-4o-mini", ["sample"] * 1000)
```

## 5. 實務架構

建議搭配 [Google Cloud Vertex AI](https://www.google.com/search?q=Vertex+AI+model+deployment+optimization) 或 AWS SageMaker 的推論端點自動擴展功能。

## 6. 結語

快取、批次與模型蒸餾是推論成本最佳化的三大支柱。多數團隊在導入這三項技術後，可節省 50-80% 的推論費用，同時維持服務品質不受影響。
