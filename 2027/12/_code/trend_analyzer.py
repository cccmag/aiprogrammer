"""
AI Technology Trend Analyzer — from scratch in Python

Demonstrates: trend data aggregation, keyword frequency analysis,
sentiment scoring, and interactive report generation.
"""

import math
import random
from dataclasses import dataclass, field
from typing import Optional
from collections import Counter


# ---------------------------------------------------------------------------
# Trend Data
# ---------------------------------------------------------------------------

TREND_ARTICLES = [
    "AutoGen 1.0 released with multi-agent support",
    "A2A protocol standardized by W3C",
    "GPT-5 achieves breakthrough in reasoning",
    "Claude 4 launches with computer use capability",
    "Vector databases reach mainstream adoption",
    "HNSW algorithm optimized for GPU",
    "Multi-modal models become standard API",
    "AI safety guidelines published by OECD",
    "Prompt injection attacks rise 300%",
    "RAG patterns evolve to Agentic RAG",
    "Edge AI deployment grows 5x",
    "AI regulation framework passes in EU",
    "Open source LLMs match proprietary quality",
    "MCP protocol adopted by major vendors",
    "Agent-to-Agent economy emerges",
    "Fine-tuning costs drop 90%",
    "Synthetic data becomes preferred training method",
    "AI-powered code review adopted by enterprises",
]

TREND_MONTHS = ["2027-01", "2027-02", "2027-03", "2027-04", "2027-05",
                "2027-06", "2027-07", "2027-08", "2027-09", "2027-10",
                "2027-11", "2027-12"]


@dataclass
class TrendDataPoint:
    keyword: str
    month: str
    mentions: int
    sentiment: float  # -1 to 1
    source: str


def generate_trend_data() -> list[TrendDataPoint]:
    """Generate simulated trend data for 2027"""
    keywords = ["multi-agent", "vector database", "multi-modal", "AI safety",
                "edge AI", "RAG", "fine-tuning", "regulation"]
    data = []
    for kw in keywords:
        base = random.randint(50, 200)
        for i, month in enumerate(TREND_MONTHS):
            growth = 1.0 + i * 0.08  # upward trend
            noise = random.uniform(0.8, 1.2)
            mentions = int(base * growth * noise)
            sentiment = random.uniform(-0.2, 0.8) + i * 0.02
            data.append(TrendDataPoint(kw, month, mentions,
                                       max(-1, min(1, sentiment)),
                                       "simulated"))
    return data


# ---------------------------------------------------------------------------
# Trend Analysis
# ---------------------------------------------------------------------------

@dataclass
class TrendAnalysis:
    keyword: str
    total_mentions: int
    growth_rate: float  # last month / first month
    avg_sentiment: float
    peak_month: str
    momentum: str  # rising / stable / declining


def analyze_trends(data: list[TrendDataPoint]) -> list[TrendAnalysis]:
    """Analyze trend data for each keyword"""
    results = []
    for kw in set(d.keyword for d in data):
        points = [d for d in data if d.keyword == kw]
        points.sort(key=lambda x: x.month)

        total = sum(p.mentions for p in points)
        first = points[0].mentions if points else 1
        last = points[-1].mentions if points else 1
        growth = last / max(first, 1)

        avg_sent = sum(p.sentiment for p in points) / max(len(points), 1)
        peak = max(points, key=lambda p: p.mentions) if points else None

        if growth > 2.0:
            momentum = "rising"
        elif growth > 1.2:
            momentum = "stable"
        else:
            momentum = "declining"

        results.append(TrendAnalysis(kw, total, growth, avg_sent,
                                     peak.month if peak else "", momentum))
    return sorted(results, key=lambda x: -x.total_mentions)


# ---------------------------------------------------------------------------
# Hot Topic Detection
# ---------------------------------------------------------------------------

def find_hot_topics(data: list[TrendDataPoint], threshold: float = 1.5) -> list[str]:
    """Find keywords with significant recent growth"""
    recent_months = TREND_MONTHS[-3:]
    early_months = TREND_MONTHS[:3]

    hot = []
    for kw in set(d.keyword for d in data):
        recent_mentions = sum(d.mentions for d in data
                              if d.keyword == kw and d.month in recent_months)
        early_mentions = sum(d.mentions for d in data
                             if d.keyword == kw and d.month in early_months)
        ratio = recent_mentions / max(early_mentions, 1)
        if ratio > threshold:
            hot.append(kw)
    return hot


# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------

def generate_report(analyses: list[TrendAnalysis],
                    hot_topics: list[str]) -> str:
    """Generate a markdown trend report"""
    lines = ["# 2027 AI 技術趨勢報告\n"]
    lines.append("## 熱門話題\n")
    for t in hot_topics:
        lines.append(f"- 🔥 {t}")
    lines.append("\n## 各技術趨勢\n")
    for a in analyses:
        icon = {"rising": "📈", "stable": "➡️", "declining": "📉"}.get(a.momentum, "➡️")
        lines.append(
            f"### {a.keyword} {icon}\n"
            f"- 總提及數: {a.total_mentions:,}\n"
            f"- 成長率: {a.growth_rate:.2f}x\n"
            f"- 平均情緒: {a.avg_sentiment:+.2f}\n"
            f"- 高峰月: {a.peak_month}\n"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo():
    print("=== AI Technology Trend Analyzer ===\n")

    data = generate_trend_data()

    analyses = analyze_trends(data)
    print("Trend Analysis:")
    print(f"{'Keyword':<20} {'Total':>8} {'Growth':>8} {'Sentiment':>10} {'Momentum':>12}")
    print("-" * 60)
    for a in analyses:
        print(f"{a.keyword:<20} {a.total_mentions:>8,} {a.growth_rate:>7.2f}x "
              f"{a.avg_sentiment:>+9.2f} {a.momentum:>12}")
    print()

    hot = find_hot_topics(data)
    print(f"Hot Topics (growth > 1.5x in last 3 months):")
    for t in hot:
        print(f"  🔥 {t}")
    print()

    # Print all articles (database)
    print("Article Database (sampled):")
    articles = TREND_ARTICLES
    for a in articles:
        print(f"  📄 {a}")
    print()

    # Generate report
    report = generate_report(analyses, hot)
    print("Generated Report (first 500 chars):")
    print(report[:500])
    print("...")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
