# 多模型路由設計

## 前言

不同 LLM 在成本、速度、能力上差異極大。多模型路由（Model Router）能根據任務特性自動選擇最合適的模型，在成本與品質之間取得最佳平衡。

## 路由策略

```python
from enum import Enum
from typing import Optional

class ModelCapability(Enum):
    FAST = "fast"
    BALANCED = "balanced"
    POWERFUL = "powerful"

class ModelRouter:
    def __init__(self):
        self.models = {
            ModelCapability.FAST: "gpt-4o-mini",
            ModelCapability.BALANCED: "gpt-4o",
            ModelCapability.POWERFUL: "claude-3-opus",
        }
        self._rules: list[tuple[str, ModelCapability]] = []

    def add_rule(self, pattern: str, capability: ModelCapability):
        self._rules.append((pattern, capability))

    def route(self, task: dict) -> str:
        task_type = task.get("type", "")
        complexity = task.get("complexity", 0.5)

        for pattern, capability in self._rules:
            if pattern in task_type:
                return self.models[capability]

        if complexity > 0.8:
            return self.models[ModelCapability.POWERFUL]
        elif complexity > 0.4:
            return self.models[ModelCapability.BALANCED]
        return self.models[ModelCapability.FAST]

router = ModelRouter()
router.add_rule("translation", ModelCapability.FAST)
router.add_rule("code_review", ModelCapability.POWERFUL)
router.add_rule("summarization", ModelCapability.BALANCED)
```

## 動態負載平衡

```python
import asyncio
from collections import defaultdict

class LoadBalancedRouter:
    def __init__(self):
        self.latency_history = defaultdict(list)
        self.concurrent_calls = defaultdict(int)
        self.max_concurrent = {"gpt-4o-mini": 50, "gpt-4o": 20, "claude-3-opus": 5}

    async def select_best_model(self, fallback_models: list[str]) -> str:
        for model in fallback_models:
            if self.concurrent_calls[model] < self.max_concurrent.get(model, 10):
                self.concurrent_calls[model] += 1
                return model
        return fallback_models[-1]

    async def call_with_fallback(self, prompt: str, models: list[str]) -> str:
        for model in models:
            try:
                if self.concurrent_calls[model] >= self.max_concurrent.get(model, 10):
                    continue
                self.concurrent_calls[model] += 1
                result = await call_llm(prompt, model=model)
                return result
            except Exception as e:
                continue
            finally:
                self.concurrent_calls[model] -= 1
        raise RuntimeError("All models failed")
```

## 成本感知路由

```python
class CostAwareRouter(ModelRouter):
    def __init__(self, daily_budget: float):
        super().__init__()
        self.daily_budget = daily_budget
        self.spent_today = 0.0

    def route(self, task: dict) -> str:
        base_model = super().route(task)
        if self.spent_today > self.daily_budget * 0.8:
            return self.models[ModelCapability.FAST]
        return base_model

    def record_cost(self, cost: float):
        self.spent_today += cost

    def reset_daily(self):
        self.spent_today = 0.0

router = CostAwareRouter(daily_budget=50.0)

async def smart_llm_call(task: dict) -> str:
    model = router.route(task)
    result = await call_llm(task["prompt"], model=model)
    router.record_cost(result.cost)
    return result.content
```

## 品質評估

```python
class QualityScorer:
    async def score(self, prompt: str, response: str) -> float:
        eval_prompt = f"評估以下回答品質（0-1）：\n問題：{prompt}\n回答：{response}"
        result = await call_llm(eval_prompt, model="gpt-4o")
        return float(result.content.strip())
```

## 結語

多模型路由是平衡成本、速度與品質的核心技術。結合動態負載平衡和成本感知策略，可以在不犧牲使用者體驗的前提下，顯著降低營運成本。

---

**延伸閱讀**

- [LLM 路由策略](https://www.google.com/search?q=LLM+model+routing+strategies)
- [動態模型選擇](https://www.google.com/search?q=dynamic+model+selection+LLM)
- [成本最佳化架構](https://www.google.com/search?q=LLM+cost+optimization+architecture)
