# Calculator 測試範例

## 概述

本文展示如何使用 Python 的 `unittest` 和 `pytest` 對一個簡單的 `Calculator` 類別進行測試。這個範例涵蓋了單元測試的核心概念：基本運算測試、邊界條件測試、例外處理測試、歷史記錄測試，以及測試之間的隔離。

## 專案簡介

**Calculator** 是一個簡單的計算機類別，支援：
- 基本運算（加、減、乘、除、次方）
- 運算歷史記錄
- 除零錯誤處理
- 鏈式運算

## 核心類別設計

```python
class Calculator:
    def __init__(self, name="Default"):
        self.name = name
        self.history = []

    def add(self, a, b): ...
    def subtract(self, a, b): ...
    def multiply(self, a, b): ...
    def divide(self, a, b): ...
    def power(self, a, b): ...
    def get_last_result(self): ...
    def clear_history(self): ...
```

## 測試策略

### 1. unittest 測試

```python
class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator("TestCalc")

    def test_add_positive(self):
        self.assertEqual(self.calc.add(3, 5), 8)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
```

### 2. pytest 風格測試

```python
def test_pytest_add():
    calc = Calculator()
    assert calc.add(2, 2) == 4

def test_pytest_divide_by_zero():
    import pytest
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(1, 0)
```

### 3. 執行結果

```
Calculator Demo
============================================================
add(10, 20)     = 30
subtract(50, 15)= 35
multiply(6, 7)  = 42
divide(100, 4)  = 25.0
power(3, 4)     = 81

unittest 結果: 19 測試, 0 失敗, 0 錯誤
發現 7 個 pytest 風格測試函數
全部測試通過！
```

## 測試要點

### setUp 確保測試隔離

每次測試前建立新的 Calculator 實例，避免測試之間的狀態汙染：

```python
def setUp(self):
    self.calc = Calculator("TestCalc")
```

### 例外測試

```python
def test_divide_by_zero(self):
    with self.assertRaises(ValueError):
        self.calc.divide(10, 0)
```

### 邊界條件

```python
def test_add_zero(self):
    self.assertEqual(self.calc.add(0, 0), 0)

def test_multiply_by_zero(self):
    self.assertEqual(self.calc.multiply(7, 0), 0)

def test_power_zero(self):
    self.assertEqual(self.calc.power(5, 0), 1)
```

### 狀態測試

```python
def test_history_tracking(self):
    self.calc.add(1, 2)
    self.calc.multiply(3, 4)
    self.assertEqual(len(self.calc.history), 2)

def test_get_last_result_empty(self):
    self.assertIsNone(self.calc.get_last_result())
```

## 從這裡開始

```bash
cd _code
python3 testing.py    # 執行 demo 和所有測試
python3 -m pytest testing.py  # 使用 pytest 執行
```

## 延伸挑戰

- 加入 `modulo`（取餘數）運算和對應測試
- 加入 `sqrt`（平方根）運算，處理負數輸入的例外
- 使用 `@parameterized.expand` 或 pytest 的 `@pytest.mark.parametrize` 重構重複測試
- 加入 `unittest.mock` 模擬外部日誌服務

---

## 延伸閱讀

- [完整程式碼](_code/testing.py)
- [unittest 官方文件](https://www.google.com/search?q=Python+unittest+documentation)
- [pytest 官方文件](https://www.google.com/search?q=pytest+documentation)
