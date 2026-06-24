# 測試自動生成與執行（2018-2028）

## 測試生成的問題

軟體測試長期是開發流程中最耗時但最容易被忽略的環節。2018 年的一份研究顯示，開發者平均花費 35% 的時間在測試上，但測試覆蓋率仍然低於 60%。

傳統的自動測試工具（如 EvoSuite、Randoop）使用隨機搜尋和符號執行：

```python
# Randoop 風格的隨機測試生成
def randoop_generate(cls):
    tests = []
    for _ in range(1000):
        args = [random_value_for(p) for p in cls.params]
        try:
            result = cls(*args)
            tests.append((cls, args, result))
        except Exception:
            pass  # 異常也被視為測試結果
    return tests
```

問題：隨機生成的測試缺乏**語義覆蓋**——它們測試了語法路徑，但無法理解程式應該做什麼。

## 2020：Regression Testing with AI

DiffBlue 和 SapFix 開始使用機器學習生成的測試來捕捉回歸錯誤：

```python
class AITestGenerator:
    def generate_unit_test(self, function):
        signature = self.analyze_signature(function)
        spec = self.extract_spec(function.docstring)
        return self.model.generate(
            f"# 為 {function.name} 生成 pytest 測試\n# 規格：{spec}"
        )
```

## 2023：LLM-Based 測試生成

2023 年，GPT-4 和 GitHub Copilot 開始支援「一鍵生成測試」。LLM 的優勢在於能理解**意圖**：

```python
# 給定一個函式，AI 自動生成邊界案例測試
def test_calculate_discount():
    assert calculate_discount(100, 'vip', 6) == 70     # VIP >5年
    assert calculate_discount(100, 'vip', 3) == 85     # VIP ≤5年
    assert calculate_discount(100, 'regular', 1) == 95 # 一般
    assert calculate_discount(0, 'vip', 10) == 0       # 邊界
    assert calculate_discount(-10, 'regular', 1) == -9.5  # 負數
```

## 2025：自動化測試驅動開發

AI TDD 工具讓程式碼和測試協同生成：AI 先依規格生成測試（紅燈），再生成實現（綠燈），最後重構——全自動循環。

## 2026-2028：自我修復測試

2026-2028 年，測試系統開始具備**自我修復**能力：

```python
class SelfHealingTestSuite:
    def run(self):
        for test in self.tests:
            try:
                test.run()
            except AssertionError as e:
                if self.ai_analyze.is_feature_change(e):
                    self.ai_generate_fix(test, e)  # 自動修復測試
```

## 延伸閱讀

- [DiffBlue AI Test Generation](https://www.google.com/search?q=DiffBlue+AI+test+generation+2020)
- [EvoSuite Search-Based Test Generation](https://www.google.com/search?q=EvoSuite+test+generation)
- [ChatGPT Unit Test Generation](https://www.google.com/search?q=ChatGPT+unit+test+generation+2023)
- [Self-Healing Test Automation](https://www.google.com/search?q=self+healing+test+automation+AI)

---

*本篇文章為「AI 程式人雜誌 2028 年 1 月號」主題系列之三。*
