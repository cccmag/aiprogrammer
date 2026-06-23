"""
2029 年度技術報告 — 四年回顧、指標分析、趨勢預測
"""
import math
import random
from dataclasses import dataclass, field

@dataclass
class YearSummary:
    year: int
    milestones: list[str]
    metrics: dict[str, float]

YEARLY_DATA = [
    YearSummary(2026, ["GPT-5", "AutoGen 1.0", "A2A Protocol"], {"market_b": 200, "agents_adopted": 0.1, "accuracy": 0.85}),
    YearSummary(2027, ["Multi-agent boom", "A2A standard", "AI safety EU Act"], {"market_b": 500, "agents_adopted": 0.25, "accuracy": 0.89}),
    YearSummary(2028, ["Agent economy", "Edge AI 1B chips", "Causal AI clinical"], {"market_b": 1000, "agents_adopted": 0.50, "accuracy": 0.93}),
    YearSummary(2029, ["Agent economy $100B", "Quantum ML breakthrough", "AI scientist"], {"market_b": 2000, "agents_adopted": 0.75, "accuracy": 0.96}),
]

def growth_rate(data: list[YearSummary], metric: str) -> float:
    values = [d.metrics.get(metric, 0) for d in data]
    return ((values[-1] - values[0]) / values[0] * 100) if values[0] else 0

def forecast_2030() -> dict:
    return {"market_b": 3500, "agents_adopted": 0.90, "accuracy": 0.98,
            "key_trends": ["Autonomous AI", "Generalist agents", "AI regulation maturity"]}

def demo():
    print("=== 2029 Annual Technology Report ===\n")
    print("  4-Year Summary (2026-2029):")
    for ys in YEARLY_DATA:
        print(f"  {ys.year}: Market=${ys.metrics['market_b']}B, Agent adoption={ys.metrics['agents_adopted']:.0%}, Accuracy={ys.metrics['accuracy']:.0%}")
    for metric in ["market_b", "agents_adopted", "accuracy"]:
        gr = growth_rate(YEARLY_DATA, metric)
        print(f"  {metric} growth (2026-2029): {gr:+.0f}%")
    forecast = forecast_2030()
    print(f"\n  2030 Forecast:")
    print(f"  Market: ${forecast['market_b']}B, Agent adoption: {forecast['agents_adopted']:.0%}")
    print(f"  Key trends: {', '.join(forecast['key_trends'])}")
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
