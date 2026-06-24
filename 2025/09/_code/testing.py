#!/usr/bin/env python3
"""軟體測試範例：Calculator 類別的單元測試與 pytest 測試"""

import unittest
import sys
import io


class Calculator:
    """簡單的計算機類別，用於示範各種測試技術"""

    def __init__(self, name="Default"):
        self.name = name
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a, b):
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def power(self, a, b):
        result = a ** b
        self.history.append(f"{a} ** {b} = {result}")
        return result

    def get_last_result(self):
        if not self.history:
            return None
        return float(self.history[-1].split("= ")[1])

    def clear_history(self):
        self.history.clear()

    def __repr__(self):
        return f"Calculator(name='{self.name}', operations={len(self.history)})"


class TestCalculator(unittest.TestCase):
    """使用 unittest 框架的 Calculator 測試"""

    def setUp(self):
        self.calc = Calculator("TestCalc")

    def test_add_positive(self):
        self.assertEqual(self.calc.add(3, 5), 8)

    def test_add_negative(self):
        self.assertEqual(self.calc.add(-1, 1), 0)

    def test_add_zero(self):
        self.assertEqual(self.calc.add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 3), 7)

    def test_subtract_negative_result(self):
        self.assertEqual(self.calc.subtract(3, 10), -7)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(4, 5), 20)

    def test_multiply_by_zero(self):
        self.assertEqual(self.calc.multiply(7, 0), 0)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_power(self):
        self.assertEqual(self.calc.power(2, 3), 8)

    def test_power_zero(self):
        self.assertEqual(self.calc.power(5, 0), 1)

    def test_history_tracking(self):
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        self.assertEqual(len(self.calc.history), 2)

    def test_get_last_result(self):
        self.calc.add(10, 20)
        self.assertEqual(self.calc.get_last_result(), 30.0)

    def test_get_last_result_empty(self):
        self.assertIsNone(self.calc.get_last_result())

    def test_clear_history(self):
        self.calc.add(1, 2)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.history), 0)

    def test_repr(self):
        r = repr(self.calc)
        self.assertIn("TestCalc", r)


class TestCalculatorExtended(unittest.TestCase):
    """額外的 Calculator 測試"""

    def test_floating_point(self):
        calc = Calculator()
        result = calc.divide(1, 3)
        self.assertAlmostEqual(result, 0.33333, places=4)

    def test_large_numbers(self):
        calc = Calculator()
        self.assertEqual(calc.add(10**9, 10**9), 2 * 10**9)

    def test_chaining_operations(self):
        calc = Calculator()
        result = calc.multiply(calc.add(2, 3), calc.subtract(10, 4))
        self.assertEqual(result, 30)


# pytest-style tests (可被 pytest 自動發現)

def test_pytest_add():
    calc = Calculator()
    assert calc.add(2, 2) == 4

def test_pytest_subtract():
    calc = Calculator()
    assert calc.subtract(5, 3) == 2

def test_pytest_multiply():
    calc = Calculator()
    assert calc.multiply(3, 4) == 12

def test_pytest_divide():
    calc = Calculator()
    assert calc.divide(8, 2) == 4.0

def test_pytest_divide_by_zero():
    import pytest
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(1, 0)

def test_pytest_history():
    calc = Calculator()
    calc.add(1, 1)
    calc.add(2, 2)
    assert len(calc.history) == 2

def test_pytest_history_content():
    calc = Calculator()
    calc.add(3, 4)
    assert calc.history[0] == "3 + 4 = 7"


def demo():
    """執行所有測試並顯示結果"""
    print("=" * 60)
    print("Calculator Demo")
    print("=" * 60)

    calc = Calculator("DemoCalc")
    print(f"\n建立: {calc}")

    print("\n--- 基本運算 ---")
    print(f"add(10, 20)     = {calc.add(10, 20)}")
    print(f"subtract(50, 15)= {calc.subtract(50, 15)}")
    print(f"multiply(6, 7)  = {calc.multiply(6, 7)}")
    print(f"divide(100, 4)  = {calc.divide(100, 4)}")
    print(f"power(3, 4)     = {calc.power(3, 4)}")

    print(f"\n最後結果: {calc.get_last_result()}")
    print(f"歷史記錄: {calc.history}")

    print("\n--- 執行 unittest ---")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCalculatorExtended))
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=2)
    result = runner.run(suite)
    print(f"unittest 結果: {result.testsRun} 測試, {len(result.failures)} 失敗, {len(result.errors)} 錯誤")

    print("\n--- pytest 測試 (透過 unittest 發現) ---")
    test_methods = [m for m in dir(sys.modules[__name__]) if m.startswith("test_pytest_")]
    print(f"發現 {len(test_methods)} 個 pytest 風格測試函數")
    for name in sorted(test_methods):
        try:
            fn = getattr(sys.modules[__name__], name)
            fn()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")

    print("\n" + "=" * 60)
    print("全部測試通過！")
    print("=" * 60)


if __name__ == "__main__":
    demo()
