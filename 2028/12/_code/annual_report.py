"""
2028 年度 AI 技術報告 — 多來源分析、關鍵指標、趨勢圖
"""

import math
import random
from dataclasses import dataclass, field
from typing import Optional
from collections import Counter


# --- 1. 年度資料匯總 ---

ANNUAL_EVENTS = [
    ("2028-01", "GPT-6 發布: 百萬級 Context Window"),
    ("2028-02", "Agent-to-Agent 經濟規模達 100 億美元"),
    ("2028-03", "邊緣 AI 晶片出貨量突破 10 億"),
    ("2028-04", "首個 AI 工程師認證制度推出"),
    ("2028-05", "因果 AI 首次用於臨床試驗設計"),
    ("2028-06", "EU AI Act 全面實施"),
    ("2028-07", "開源模型在基準測試上超越閉源"),
    ("2028-08", "AI 可觀測性成為標配"),
    ("2028-09", "全球 AI 市場突破 1 兆美元"),
    ("2028-10", "自主系統在物流業達到 90% 採用率"),
    ("2028-11", "AI 安全漏洞通報機制建立"),
    ("2028-12", "2028 年度回顧"),
]


@dataclass
class AnnualMetric:
    name: str
    q1: float
    q2: float
    q3: float
    q4: float
    unit: str

    def growth(self) -> float:
        return ((self.q4 - self.q1) / self.q1) * 100 if self.q1 != 0 else 0


ANNUAL_METRICS = [
    AnnualMetric("AI Market Size ($B)", 600, 720, 850, 1000, "B USD"),
    AnnualMetric("LLM Accuracy (MMLU %)", 89, 91, 93, 95, "%"),
    AnnualMetric("Agent Adoption (%)", 25, 35, 50, 65, "%"),
    AnnualMetric("Edge AI Devices (B)", 5, 7, 9, 12, "B units"),
    AnnualMetric("AI Safety Incidents", 120, 95, 80, 60, "count"),
]


# --- 2. 年度分析器 ---

class YearlyAnalyzer:
    """Analyze yearly trends and generate insights"""

    def analyze_metrics(self, metrics: list[AnnualMetric]) -> list[dict]:
        insights = []
        for m in metrics:
            growth = m.growth()
            if growth > 50:
                verdict = "Notable"
            elif growth > 20:
                verdict = "Growing"
            elif growth > 0:
                verdict = "Stable"
            else:
                verdict = "Declining"

            insights.append({
                "name": m.name,
                "growth_pct": round(growth, 1),
                "verdict": verdict,
                "q4_value": m.q4,
                "unit": m.unit
            })
        return insights


# --- 3. 年度亮點提取 ---

def extract_highlights(events: list[tuple[str, str]],
                       metrics: list[AnnualMetric]) -> dict:
    """Extract key highlights from the year"""

    top_events = events[:5]
    top_growth = max(metrics, key=lambda m: m.growth())

    return {
        "total_events": len(events),
        "top_events": top_events,
        "fastest_growing": f"{top_growth.name} ({top_growth.growth():+.0f}%)",
        "summary": f"2028 saw {len(events)} major events with "
                   f"{top_growth.name} leading growth at {top_growth.growth():+.0f}%"
    }


# --- 4. 未來預測 ---

def forecast_2029(metrics: list[AnnualMetric]) -> list[dict]:
    """Simple linear forecast for 2029"""
    forecasts = []
    for m in metrics:
        avg_growth = m.growth() / 4  # per quarter
        q1_2029 = m.q4 * (1 + avg_growth / 100)
        forecasts.append({
            "name": m.name,
            "q4_2028": m.q4,
            "predicted_q1_2029": round(q1_2029, 1),
            "unit": m.unit,
            "confidence": random.uniform(0.6, 0.9)
        })
    return forecasts


# --- Demo ---

def demo():
    print("=== 2028 Annual AI Technology Report ===\n")

    # 1. Events Timeline
    print("1. 2028 Timeline:")
    for month, event in ANNUAL_EVENTS:
        print(f"  {month}: {event}")
    print()

    # 2. Metrics
    print("2. Annual Metrics:")
    print(f"{'Metric':<30} {'Q1':>8} {'Q2':>8} {'Q3':>8} {'Q4':>8} {'Growth':>8}")
    print("-" * 70)
    for m in ANNUAL_METRICS:
        print(f"{m.name:<30} {m.q1:>8.0f} {m.q2:>8.0f} {m.q3:>8.0f} "
              f"{m.q4:>8.0f} {m.growth():>+7.0f}%")
    print()

    # 3. Analysis
    print("3. Trend Analysis:")
    analyzer = YearlyAnalyzer()
    insights = analyzer.analyze_metrics(ANNUAL_METRICS)
    for i in insights:
        print(f"  {i['name']}: {i['verdict']} ({i['growth_pct']:+.0f}% → "
              f"{i['q4_value']} {i['unit']})")
    print()

    # 4. Highlights
    print("4. Year Highlights:")
    highlights = extract_highlights(ANNUAL_EVENTS, ANNUAL_METRICS)
    print(f"  Fastest growing: {highlights['fastest_growing']}")
    for event in highlights['top_events']:
        print(f"  📌 {event[1]}")
    print()

    # 5. Forecast
    print("5. 2029 Forecast:")
    forecasts = forecast_2029(ANNUAL_METRICS)
    for f in forecasts:
        print(f"  {f['name']}: {f['q4_2028']} → {f['predicted_q1_2029']} "
              f"{f['unit']} (confidence: {f['confidence']:.0%})")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
