# 成本控制與預算管理

## 前言

LLM API 費用隨用量線性成長，若缺乏管控機制，帳單可能迅速失控。本文介紹成本控制與預算管理的實務方法。

## 成本追蹤基礎

```python
from datetime import datetime, date
from collections import defaultdict
from typing import Optional

MODEL_RATES = {
    "gpt-4o":          {"input": 0.01,  "output": 0.03},
    "gpt-4o-mini":     {"input": 0.0015,"output": 0.006},
    "claude-3-opus":   {"input": 0.015, "output": 0.075},
    "claude-3-sonnet": {"input": 0.003, "output": 0.015},
}

def compute_cost(model: str, input_tok: int, output_tok: int) -> float:
    rate = MODEL_RATES.get(model, MODEL_RATES["gpt-4o-mini"])
    return (input_tok / 1000 * rate["input"] +
            output_tok / 1000 * rate["output"])

class BudgetManager:
    def __init__(self, monthly_budget: float):
        self.monthly_budget = monthly_budget
        self.daily_log: dict[str, float] = defaultdict(float)

    def record(self, cost: float):
        today = date.today().isoformat()
        self.daily_log[today] += cost

    def month_spend(self) -> float:
        prefix = date.today().strftime("%Y-%m")
        return sum(v for k, v in self.daily_log.items() if k.startswith(prefix))

    def remaining(self) -> float:
        return self.monthly_budget - self.month_spend()

    def budget_alert(self) -> Optional[str]:
        ratio = self.month_spend() / self.monthly_budget
        if ratio >= 0.9:
            return "budget_critical"
        if ratio >= 0.75:
            return "budget_warning"
        return None
```

## 用量配額

```python
class QuotaEnforcer:
    def __init__(self, budget_mgr: BudgetManager):
        self.budget_mgr = budget_mgr
        self.user_quota: dict[str, float] = defaultdict(float)

    def set_user_quota(self, user_id: str, daily_limit: float):
        self.user_quota[user_id] = daily_limit

    def check_user_quota(self, user_id: str, estimated_cost: float) -> bool:
        today = date.today().isoformat()
        key = f"{user_id}:{today}"
        used = self.user_quota.get(key, 0.0)
        return (used + estimated_cost) <= self.user_quota.get(user_id, float("inf"))

    def enforce(self, user_id: str, model: str, input_tok: int, output_tok: int) -> bool:
        cost = compute_cost(model, input_tok, output_tok)

        if cost > self.budget_mgr.remaining():
            return False

        if not self.check_user_quota(user_id, cost):
            return False

        self.budget_mgr.record(cost)
        today = date.today().isoformat()
        key = f"{user_id}:{today}"
        self.user_quota[key] = self.user_quota.get(key, 0.0) + cost
        return True
```

## 模型降級策略

```python
class ModelDowngrader:
    def __init__(self, budget_mgr: BudgetManager):
        self.budget_mgr = budget_mgr

    def select_model(self, preferred: str, task_type: str) -> str:
        remaining = self.budget_mgr.remaining()
        days_left = max(1, 30 - date.today().day)
        daily_allowance = remaining / days_left

        if daily_allowance < 0.5:
            return "gpt-4o-mini"
        if daily_allowance < 2.0 and preferred != "gpt-4o-mini":
            return "gpt-4o-mini" if task_type != "complex" else "gpt-4o"
        return preferred

downgrader = ModelDowngrader(BudgetManager(200))

async def cost_aware_call(prompt: str, preferred_model: str, task_type: str) -> str:
    model = downgrader.select_model(preferred_model, task_type)
    return await call_llm(prompt, model=model)
```

## 成本報表

```python
class CostReporter:
    def __init__(self, budget_mgr: BudgetManager):
        self.budget_mgr = budget_mgr

    def daily_report(self) -> str:
        today = date.today().isoformat()
        spend = self.budget_mgr.daily_log.get(today, 0)
        return f"本日花費: ${spend:.2f} | 月餘額: ${self.budget_mgr.remaining():.2f}"

    def model_breakdown(self) -> dict:
        return dict(sorted(
            self.budget_mgr.daily_log.items(), key=lambda x: x[1], reverse=True
        )[:10])
```

## 結語

成本控制需要可視化追蹤、預算配額和自動降級機制三管齊下。建立完善的預算管理系統，讓每個 API 呼叫都在掌控之中。

---

**延伸閱讀**

- [LLM 成本管理工具](https://www.google.com/search?q=LLM+cost+management+tools)
- [API 費用估算](https://www.google.com/search?q=LLM+API+pricing+comparison+2026)
- [雲端成本最佳化](https://www.google.com/search?q=cloud+cost+optimization+AI+workloads)
