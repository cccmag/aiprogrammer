"""
AI 經濟學與成本分析工具 — API 成本追蹤、模型比較、ROI 評估
"""

import math
import random
import time
from dataclasses import dataclass, field
from typing import Optional


# --- 1. API 成本追蹤 ---

@dataclass
class APICallRecord:
    model: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    cost: float
    timestamp: float = field(default_factory=time.time)


MODEL_PRICING = {
    "gpt-5": {"input": 0.01, "output": 0.03},     # $ per 1K tokens
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "claude-4": {"input": 0.003, "output": 0.015},
    "gemini-2.5": {"input": 0.001, "output": 0.002},
    "llama-4-70b": {"input": 0.0005, "output": 0.001},
}


class CostTracker:
    """Track API costs across models and projects"""

    def __init__(self):
        self.records: list[APICallRecord] = []

    def record_call(self, model: str, prompt_tokens: int,
                    completion_tokens: int, latency_ms: float) -> APICallRecord:
        pricing = MODEL_PRICING.get(model, {"input": 0.001, "output": 0.002})
        cost = (prompt_tokens * pricing["input"] +
                completion_tokens * pricing["output"]) / 1000
        record = APICallRecord(model, prompt_tokens, completion_tokens,
                               latency_ms, round(cost, 6))
        self.records.append(record)
        return record

    def total_cost(self) -> float:
        return sum(r.cost for r in self.records)

    def cost_by_model(self) -> dict[str, float]:
        costs = {}
        for r in self.records:
            costs[r.model] = costs.get(r.model, 0) + r.cost
        return costs

    def summary(self) -> dict:
        return {
            "total_calls": len(self.records),
            "total_cost": round(self.total_cost(), 4),
            "avg_latency_ms": round(sum(r.latency_ms for r in self.records) / max(len(self.records), 1), 1),
            "avg_cost_per_call": round(self.total_cost() / max(len(self.records), 1), 6),
            "by_model": self.cost_by_model()
        }


# --- 2. 模型選擇經濟學 ---

@dataclass
class ModelOption:
    name: str
    cost_per_call: float
    latency_ms: float
    quality_score: float  # 0-1


def optimal_model_selection(task_type: str) -> ModelOption:
    """Recommend best model based on task type"""
    models = {
        "simple": ModelOption("gemini-2.5", 0.0005, 200, 0.85),
        "coding": ModelOption("claude-4", 0.003, 300, 0.95),
        "reasoning": ModelOption("gpt-5", 0.01, 500, 0.98),
        "chat": ModelOption("llama-4-70b", 0.0005, 400, 0.88),
    }
    return models.get(task_type, models["simple"])


# --- 3. ROI 評估 ---

@dataclass
class ROIResult:
    total_investment: float
    total_return: float
    roi: float
    payback_months: float


def calculate_roi(monthly_costs: list[float],
                  monthly_benefits: list[float]) -> ROIResult:
    """Calculate ROI for AI project"""
    total_inv = sum(monthly_costs)
    total_ret = sum(monthly_benefits)
    roi = ((total_ret - total_inv) / total_inv) * 100 if total_inv > 0 else 0

    cumulative = 0
    payback = 0
    for c, b in zip(monthly_costs, monthly_benefits):
        cumulative += b - c
        payback += 1
        if cumulative >= total_inv:
            break

    return ROIResult(total_inv, total_ret, round(roi, 1), payback)


# --- 4. 成本預測 ---

class CostForecast:
    """Predict future costs based on growth rate"""

    def __init__(self, base_cost: float, monthly_growth: float = 0.1):
        self.base = base_cost
        self.growth = monthly_growth

    def forecast(self, months: int = 12) -> list[float]:
        costs = []
        for m in range(months):
            costs.append(round(self.base * (1 + self.growth) ** m, 2))
        return costs


# --- Demo ---

def demo():
    print("=== AI Economics & Cost Analysis ===\n")

    # 1. Cost Tracking
    print("1. API Cost Tracking (100 calls):")
    tracker = CostTracker()
    models = list(MODEL_PRICING.keys())
    for i in range(100):
        model = random.choice(models)
        prompt = random.randint(100, 1000)
        completion = random.randint(50, 500)
        latency = random.uniform(100, 1000)
        tracker.record_call(model, prompt, completion, latency)

    summary = tracker.summary()
    print(f"  Total calls: {summary['total_calls']}")
    print(f"  Total cost: ${summary['total_cost']:.4f}")
    print(f"  Avg latency: {summary['avg_latency_ms']}ms")
    print(f"  Avg cost/call: ${summary['avg_cost_per_call']:.6f}")
    print("  By model:")
    for model, cost in sorted(summary['by_model'].items(), key=lambda x: -x[1]):
        print(f"    {model}: ${cost:.4f}")
    print()

    # 2. Model Selection Economics
    print("2. Model Selection Economics:")
    for task in ["simple", "coding", "reasoning", "chat"]:
        model = optimal_model_selection(task)
        print(f"  {task}: {model.name} (${model.cost_per_call:.4f}/call, "
              f"{model.latency_ms}ms, quality={model.quality_score})")
    print()

    # 3. ROI
    print("3. ROI Analysis (12 months):")
    costs = [5000, 5000, 5500, 5500, 6000, 6000,
             6500, 6500, 7000, 7000, 7500, 7500]
    benefits = [0, 0, 2000, 5000, 8000, 10000,
                12000, 14000, 16000, 18000, 20000, 22000]
    roi = calculate_roi(costs, benefits)
    print(f"  Total investment: ${roi.total_investment:,.0f}")
    print(f"  Total return: ${roi.total_return:,.0f}")
    print(f"  ROI: {roi.roi:.0f}%")
    print(f"  Payback period: {roi.payback_months:.0f} months")
    print()

    # 4. Cost Forecast
    print("4. Cost Forecast (12 months):")
    forecast = CostForecast(1000, 0.08)
    costs = forecast.forecast(12)
    for m, c in enumerate(costs, 1):
        print(f"  Month {m:2d}: ${c:.2f}")
    print(f"  Year total: ${sum(costs):.2f}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
