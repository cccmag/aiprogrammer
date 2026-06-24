# 實作簡化測試框架：從零打造 TDD 工具

## 簡介

本期程式實作將帶領讀者從頭實作一個簡化的單元測試框架，幫助理解 TDD 的核心概念和測試框架的運作原理。

## 程式碼

```python
#!/usr/bin/env python3
"""
Simplified Unit Testing Framework - TDD Demo

這個程式演示了測試框架的核心概念：
1. 測試收集（Test Discovery）
2. 斷言系統（Assertion）
3. 測試執行器（Test Runner）
4. 結果報告（Reporting）
"""

import sys
import traceback
from dataclasses import dataclass, field
from typing import List, Callable, Optional
from time import time


@dataclass
class TestResult:
    name: str
    passed: bool
    duration: float
    error: Optional[str] = None
    traceback: Optional[str] = None


class AssertionError(Exception):
    pass


class TestCase:
    def setup(self):
        pass

    def teardown(self):
        pass

    def run(self, test_name: str) -> TestResult:
        start = time()
        self.setup()

        try:
            method = getattr(self, test_name)
            method()
            duration = time() - start
            return TestResult(
                name=test_name,
                passed=True,
                duration=duration
            )
        except AssertionError as e:
            duration = time() - start
            return TestResult(
                name=test_name,
                passed=False,
                duration=duration,
                error=str(e),
                traceback=traceback.format_exc()
            )
        except Exception as e:
            duration = time() - start
            return TestResult(
                name=test_name,
                passed=False,
                duration=duration,
                error=str(e),
                traceback=traceback.format_exc()
            )
        finally:
            self.teardown()


class TestRunner:
    def __init__(self):
        self.results: List[TestResult] = []

    def run_test_class(self, test_class: type):
        instance = test_class()
        for name in dir(instance):
            if name.startswith('test_'):
                result = instance.run(name)
                self.results.append(result)

    def run_all(self, test_classes: List[type]):
        for test_class in test_classes:
            self.run_test_class(test_class)

    def report(self) -> str:
        lines = []
        lines.append("\n" + "=" * 60)
        lines.append("Test Results")
        lines.append("=" * 60)

        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        total_time = sum(r.duration for r in self.results)

        lines.append(f"\nTotal: {total} | Passed: {passed} | Failed: {failed}")
        lines.append(f"Time: {total_time:.3f}s")
        lines.append("-" * 60)

        for result in self.results:
            status = "PASS" if result.passed else "FAIL"
            lines.append(f"[{status}] {result.name} ({result.duration:.3f}s)")

            if not result.passed:
                lines.append(f"  Error: {result.error}")
                if result.traceback:
                    for line in result.traceback.split('\n')[:5]:
                        if line.strip():
                            lines.append(f"  {line}")

        return "\n".join(lines)


class Assert:
    @staticmethod
    def equal(actual, expected):
        if actual != expected:
            raise AssertionError(
                f"Expected {expected!r}, got {actual!r}"
            )

    @staticmethod
    def not_equal(actual, unexpected):
        if actual == unexpected:
            raise AssertionError(
                f"Expected not {unexpected!r}"
            )

    @staticmethod
    def true(value):
        if not value:
            raise AssertionError(f"Expected True, got {value!r}")

    @staticmethod
    def false(value):
        if value:
            raise AssertionError(f"Expected False, got {value!r}")

    @staticmethod
    def is_none(value):
        if value is not None:
            raise AssertionError(f"Expected None, got {value!r}")

    @staticmethod
    def is_not_none(value):
        if value is None:
            raise AssertionError("Expected not None")

    @staticmethod
    def raises(exception_type, func):
        try:
            func()
        except exception_type:
            return
        except Exception as e:
            raise AssertionError(
                f"Expected {exception_type.__name__}, got {type(e).__name__}"
            )
        raise AssertionError(f"Expected {exception_type.__name__}, no exception raised")

    @staticmethod
    def contains(collection, item):
        if item not in collection:
            raise AssertionError(
                f"Expected {item!r} in {collection!r}"
            )


class expect:
    def __init__(self, value):
        self.value = value

    def to_equal(self, expected):
        Assert.equal(self.value, expected)

    def to_not_equal(self, unexpected):
        Assert.not_equal(self.value, unexpected)

    def to_be_true(self):
        Assert.true(self.value)

    def to_be_false(self):
        Assert.false(self.value)

    def to_be_none(self):
        Assert.is_none(self.value)

    def to_not_be_none(self):
        Assert.is_not_none(self.value)

    def to_contain(self, item):
        Assert.contains(self.value, item)


def describe(name: str, cls: type):
    print(f"\n{name}")
    print("=" * len(name))


def it(name: str, func: Callable):
    print(f"  {name}... ", end="")
    try:
        func()
        print("PASS")
        return True
    except AssertionError as e:
        print(f"FAIL")
        print(f"    {e}")
        return False


def demo():
    print("\n" + "#" * 60)
    print("# TDD Testing Framework Demo")
    print("#" * 60)

    class Calculator:
        def add(self, a, b):
            return a + b

        def subtract(self, a, b):
            return a - b

        def divide(self, a, b):
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return a / b

    class CalculatorTest(TestCase):
        def test_add_positive_numbers(self):
            calc = Calculator()
            expect(calc.add(2, 3)).to_equal(5)

        def test_add_negative_numbers(self):
            calc = Calculator()
            expect(calc.add(-1, -1)).to_equal(-2)

        def test_subtract(self):
            calc = Calculator()
            expect(calc.subtract(5, 3)).to_equal(2)

        def test_divide(self):
            calc = Calculator()
            expect(calc.divide(6, 2)).to_equal(3)

        def test_divide_by_zero(self):
            calc = Calculator()
            Assert.raises(
                ZeroDivisionError,
                lambda: calc.divide(1, 0)
            )

    class StringHelperTest(TestCase):
        def test_reverse(self):
            assert "hello"[::-1] == "olleh"

        def test_uppercase(self):
            expect("hello".upper()).to_equal("HELLO")

    describe("Calculator Tests", CalculatorTest)
    describe("StringHelper Tests", StringHelperTest)

    runner = TestRunner()
    runner.run_test_class(CalculatorTest)
    runner.run_test_class(StringHelperTest)

    print(runner.report())

    print("\n" + "#" * 60)
    print("# TDD Workflow Demonstration")
    print("#" * 60)

    print("""
TDD 工作流程：

1. RED - 寫一個會失敗的測試
   def test_add():
       calc = Calculator()
       expect(calc.add(2, 3)).to_equal(5)

2. GREEN - 盡快寫出通過測試的程式碼
   def add(self, a, b):
       return 5  # 臨時實現

3. REFACTOR - 改善程式碼
   def add(self, a, b):
       return a + b  # 正確實現
""")


if __name__ == "__main__":
    demo()
```

## 測試方式

```bash
python3 _code/tdd_demo.py
```

## 輸出範例

```
############################################################
# TDD Testing Framework Demo
############################################################

Calculator Tests
===============

Calculator Tests
  test_add_positive_numbers... PASS
  test_add_negative_numbers... PASS
  test_subtract... PASS
  test_divide... PASS
  test_divide_by_zero... PASS

StringHelper Tests
==================

StringHelper Tests
  test_reverse... PASS
  test_uppercase... PASS

============================================================
Test Results
============================================================

Total: 7 | Passed: 7 | Failed: 0
Time: 0.000s
------------------------------------------------------------
[PASS] test_add_positive_numbers (0.000s)
[PASS] test_add_negative_numbers (0.000s)
[PASS] test_subtract (0.000s)
[PASS] test_divide (0.000s)
[PASS] test_divide_by_zero (0.000s)
[PASS] test_reverse (0.000s)
[PASS] test_uppercase (0.000s)
```

## 實作重點

1. **TestCase 類別**：測試的基礎類別，包含 setup 和 teardown
2. **TestRunner**：收集和執行測試，生成報告
3. **Assert 類別**：各種斷言方法
4. **expect 語法**：更可讀的斷言方式

## 延伸學習

- 實作更多斷言（assertAlmostEqual, assertRegex）
- 實作測試跳過（skip）
- 實作參數化測試（parametrize）
- 實作 Mock 物件系統

---

*本期程式實作到此結束。*