#!/usr/bin/env python3
"""2025 程式人年度回顧 - 數據分析與趨勢報告"""

import json
import math
from datetime import datetime


def generate_language_data():
    """Generate programming language trend data for 2025."""
    languages = {
        "Python":      {"tiobe": 15.8, "github_repos": 8500000,  "growth": 12.5, "jobs": 42000},
        "JavaScript":  {"tiobe": 8.2,  "github_repos": 12000000, "growth": 3.2,  "jobs": 38000},
        "TypeScript":  {"tiobe": 6.5,  "github_repos": 5200000,  "growth": 18.7, "jobs": 28000},
        "Go":          {"tiobe": 3.8,  "github_repos": 1800000,  "growth": 15.3, "jobs": 15000},
        "Rust":        {"tiobe": 2.9,  "github_repos": 950000,   "growth": 22.1, "jobs": 9000},
        "Kotlin":      {"tiobe": 2.1,  "github_repos": 1200000,  "growth": 8.9,  "jobs": 11000},
        "Swift":       {"tiobe": 1.9,  "github_repos": 980000,   "growth": 4.5,  "jobs": 8500},
        "Zig":         {"tiobe": 0.8,  "github_repos": 120000,   "growth": 45.0, "jobs": 1200},
        "Mojo":        {"tiobe": 0.5,  "github_repos": 45000,    "growth": 180.0, "jobs": 500},
    }
    return languages


def generate_ai_tool_data():
    """Generate AI development tool adoption data."""
    tools = {
        "GitHub Copilot":     {"users_m": 5.2, "repos_using": 3800000, "satisfaction": 87},
        "Cursor":             {"users_m": 3.8, "repos_using": 2100000, "satisfaction": 91},
        "Claude Code":        {"users_m": 2.1, "repos_using": 950000,  "satisfaction": 89},
        "OpenCode":           {"users_m": 0.8, "repos_using": 280000,  "satisfaction": 93},
        "Windsurf":           {"users_m": 1.5, "repos_using": 670000,  "satisfaction": 85},
        "Codeium":            {"users_m": 2.8, "repos_using": 1400000, "satisfaction": 82},
    }
    return tools


def compute_trends(languages):
    """Compute growth trends and composite innovation scores."""
    by_growth = sorted(languages.items(), key=lambda x: x[1]["growth"], reverse=True)
    by_tiobe = sorted(languages.items(), key=lambda x: x[1]["tiobe"], reverse=True)

    scores = {}
    for name, data in languages.items():
        scores[name] = (
            data["tiobe"] * 0.3
            + data["growth"] * 0.4
            + math.log10(data["github_repos"] + 1) * 0.3
        )
    by_innovation = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return {
        "by_growth": by_growth,
        "by_tiobe": by_tiobe,
        "by_innovation": by_innovation,
    }


def generate_report(languages, tools, trends):
    """Generate a formatted text report."""
    lines = []
    lines.append("=" * 60)
    lines.append("  2025 程式人年度回顧 — 數據報告")
    lines.append(f"  生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 60)
    lines.append("")

    lines.append("📊 程式語言 TIOBE 排名")
    lines.append("-" * 40)
    for i, (name, data) in enumerate(trends["by_tiobe"], 1):
        bar = "█" * max(1, int(data["tiobe"] / 1.5))
        lines.append(f"  {i}. {name:12s} {data['tiobe']:5.1f}% {bar}")
    lines.append("")

    lines.append("📈 成長率領先者")
    lines.append("-" * 40)
    for name, data in trends["by_growth"][:5]:
        lines.append(f"  {name:12s} +{data['growth']:5.1f}%  (職缺: {data['jobs']:,})")
    lines.append("")

    lines.append("🤖 AI 開發工具採用率")
    lines.append("-" * 40)
    for name, data in tools.items():
        bar = "▓" * max(1, int(data["users_m"]))
        lines.append(f"  {name:18s} {data['users_m']:.1f}M 用戶 {bar}  滿意度: {data['satisfaction']}%")
    lines.append("")

    lines.append("💡 創新綜合評分")
    lines.append("-" * 40)
    for name, score in trends["by_innovation"][:5]:
        stars = "★" * max(1, int(score))
        lines.append(f"  {name:12s} {score:5.1f} {stars}")
    lines.append("")

    return "\n".join(lines)


def demo():
    """Main demo: load data, compute trends, print report."""
    print("正在載入 2025 年度數據...\n")

    languages = generate_language_data()
    tools = generate_ai_tool_data()
    trends = compute_trends(languages)
    report = generate_report(languages, tools, trends)

    print(report)
    print("\n✅ 報告完成")


if __name__ == "__main__":
    demo()
