# 年度回顧資料分析實作

## 前言

為了量化呈現 2023 年計算機科學領域的發展狀況，我們編寫了一個 Python 腳本 `year_review_2023.py`，用於生成年度統計報表、計算成長率，並以格式化方式輸出報告。

本程式所在的目錄為：[_code/](_code/)

---

## 原始碼

完整的 Python 實作請參考：[_code/year_review_2023.py](_code/year_review_2023.py)

```python
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
```

---

## 執行結果

```
> python3 year_review_2023.py

========================================================================
  2023 CS YEAR IN REVIEW — Annual Data Report
========================================================================
Metric                                    2022       2023        Growth
------------------------------------------------------------------------
ChatGPT MAU                                   0    180.0M          N/A
GitHub Copilot Users                       1.0M      1.8M         80.0%
Hugging Face Models                      150.0K    450.0K        200.0%
Quantum Qubits Record                       433      1121       158.89%
Rust Crates.io Packages                   120.0K    145.0K        20.83%
Kubernetes Stars on GitHub                100.0K    115.0K        15.0%
OpenAI Valuation ($B)                       29        90        210.34%
AI Startup Funding ($B)                      47        63        34.04%
========================================================================
Total categories: 8
Report generated: 2023-12-31
========================================================================

========================================================================
  CATEGORY BREAKDOWN
========================================================================
AI & ML                  Avg Growth:   205.17%
Developer Tools          Avg Growth:    47.5%
Infrastructure           Avg Growth:    89.86%
Finance                  Avg Growth:    34.04%
========================================================================
```

---

## 程式說明

### 數據結構

我們使用 Python dict 儲存各項目的 2022 和 2023 年數據。每個條目包含兩個年份的數值，方便進行對比分析。

### 成長率計算

`compute_growth()` 函式計算從 2022 年到 2023 年的成長百分比。對於分母為零的情況（如 ChatGPT MAU），返回 `inf` 並在報告中顯示為 `N/A`。

### 數字格式化

`format_number()` 將大數值轉換為易讀的字串格式（如 180.0M、1.0B）。

### 分類報告

`category_report()` 按類別匯總平均成長率，幫助識別哪些領域在 2023 年成長最快。

---

## 自訂與擴展

您可以輕鬆擴展此腳本：

1. **添加更多指標**：在 `data` 字典中新增條目
2. **新增類別**：在 `categories` 字典中新增分類
3. **修改日期範圍**：調整函式以支援更多年份
4. **輸出格式**：修改 `print_report()` 以輸出 CSV 或 JSON 格式

---

## 延伸閱讀

- [Python 數據分析基礎](https://www.google.com/search?q=Python+data+analysis+tutorial)
- [2023 年技術統計](https://www.google.com/search?q=2023+technology+statistics+growth)

---

*本篇文章為「AI 程式人雜誌 2023 年 12 月號」年度回顧系列補充文章。*
