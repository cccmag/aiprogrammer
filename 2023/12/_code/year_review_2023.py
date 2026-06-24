#!/usr/bin/env python3
"""2023 CS Year in Review — Annual Data Report Generator"""

data = {
    "ChatGPT MAU": {"2022": 0, "2023": 180_000_000},
    "GitHub Copilot Users": {"2022": 1_000_000, "2023": 1_800_000},
    "Hugging Face Models": {"2022": 150_000, "2023": 450_000},
    "Quantum Qubits Record": {"2022": 433, "2023": 1121},
    "Rust Crates.io Packages": {"2022": 120_000, "2023": 145_000},
    "Kubernetes Stars on GitHub": {"2022": 100_000, "2023": 115_000},
    "OpenAI Valuation ($B)": {"2022": 29, "2023": 90},
    "AI Startup Funding ($B)": {"2022": 47, "2023": 63},
}

def compute_growth(v2022, v2023):
    if v2022 == 0:
        return float("inf")
    return round((v2023 - v2022) / v2022 * 100, 2)

def format_number(n):
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f}B"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)

def print_report():
    sep = "=" * 72
    print(sep)
    print("  2023 CS YEAR IN REVIEW — Annual Data Report")
    print(sep)
    print(f"{'Metric':<35} {'2022':>10} {'2023':>10} {'Growth':>12}")
    print("-" * 72)
    for name, vals in data.items():
        v22, v23 = vals["2022"], vals["2023"]
        growth = compute_growth(v22, v23)
        g_str = f"{growth}%" if growth != float("inf") else "   N/A"
        print(f"{name:<35} {format_number(v22):>10} {format_number(v23):>10} {g_str:>12}")
    print(sep)
    print(f"Total categories: {len(data)}")
    print(f"Report generated: 2023-12-31")
    print(sep)

categories = {
    "AI & ML": ["ChatGPT MAU", "Hugging Face Models", "OpenAI Valuation ($B)"],
    "Developer Tools": ["GitHub Copilot Users", "Kubernetes Stars on GitHub"],
    "Infrastructure": ["Quantum Qubits Record", "Rust Crates.io Packages"],
    "Finance": ["AI Startup Funding ($B)"],
}

def category_report():
    sep = "=" * 72
    print(sep)
    print("  CATEGORY BREAKDOWN")
    print(sep)
    for cat, metrics in categories.items():
        total_growth = 0
        count = 0
        for m in metrics:
            v22, v23 = data[m]["2022"], data[m]["2023"]
            g = compute_growth(v22, v23)
            if g != float("inf"):
                total_growth += g
                count += 1
        avg = round(total_growth / count, 2) if count else 0
        print(f"{cat:<25} Avg Growth: {avg:>8}%")
    print(sep)

def demo():
    print_report()
    print()
    category_report()

if __name__ == "__main__":
    demo()
