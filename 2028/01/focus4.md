# 自動程式修復與除錯（2019-2028）

## 自動修復的挑戰

程式除錯一直是軟體開發中最令人沮喪的環節。研究顯示，開發者平均花費 50% 的開發時間在除錯上。自動程式修復（APR）的目標是：找到 bug，然後自動生成修復。

2019 年的 APR 工具（如 GenProg）使用**遺傳程式設計**：

```python
# 遺傳程式設計修復
def genetic_repair(buggy_code, tests):
    population = [mutate(buggy_code) for _ in range(100)]
    for generation in range(50):
        scored = [(score(p, tests), p) for p in population]
        parents = select_top(scored, 20)
        children = crossover(parents)
        population = [mutate(c) for c in children]
    return best(population)
```

問題：搜尋空間太大，修復率極低（< 10%）。

## 2020：模板驅動修復

2020 年，Facebook 的 SapFix 引入了模板驅動的修復方法：

```python
# SapFix 風格的修復模板
REPAIR_TEMPLATES = {
    "null_check": """
        if {expr} is None:
            return default_value
    """,
    "off_by_one": """
        for i in range(len({list})):
            # 修正範圍
            if {list}[i] == {target}:
                return i
        return -1
    """,
    "type_mismatch": """
        try:
            return {expr}
        except TypeError:
            return {default}
    """,
}
```

模板修復顯著提高了效率，但只能處理已知模式。

## 2023：LLM 驅動的修復

GPT-4 的出現讓 APR 發生了質變。LLM 能理解程式碼的**語義**：

```python
# BUG: SQL 注入 — 使用者名稱直接拼接
user = db.query(f"SELECT * FROM users WHERE username='{username}'")

# GPT-4 修復：參數化查詢
user = db.query("SELECT * FROM users WHERE username=?", (username,))
```

## 2024：自動 Bug 修復工具

Sweep AI 和 FixMate 實現了從 issue 到 PR 的全自動 pipeline：理解問題 → 定位程式碼 → 生成修復 → 建立 PR。

## 2025-2026：SWE-Bench 與實證

SWE-Bench 提供了統一的 APR 評估標準。2025 年，AI 在 SWE-Bench 上首次超過 50% 修復率。

```python
def swe_bench_score(patch, tests):
    pass_rate = sum(apply_and_test(patch, t) for t in tests) / len(tests)
    return {"pass_rate": pass_rate, "exact_match": patch == ground_truth}
```

## 2027-2028：預測性修復

最新的 APR 系統不僅能修復已有的 bug，還能**預測可能出現的 bug**：

```python
def predictive_fix(code):
    # AI 分析潛在問題
    vulnerabilities = ai_scan(code)
    for v in vulnerabilities:
        if v.risk_score > 0.8:
            # 在 bug 發生前自動修復
            fix = ai_generate_preventive_fix(code, v)
            code = apply_fix(code, fix)
    return code
```

## 延伸閱讀

- [GenProg Genetic Programming Repair](https://www.google.com/search?q=GenProg+automatic+program+repair)
- [SapFix Facebook Automated Repair](https://www.google.com/search?q=SapFix+Facebook+automated+program+repair+2020)
- [SWE-Bench Benchmark](https://www.google.com/search?q=SWE-Bench+software+engineering+benchmark)
- [GPT-4 Code Repair](https://www.google.com/search?q=GPT-4+code+repair+debugging+2023)

---

*本篇文章為「AI 程式人雜誌 2028 年 1 月號」主題系列之四。*
