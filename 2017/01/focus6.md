# 測試與品質工具：pytest、unittest 與自動化測試

## 前言

測試是軟體品質的守護者。良好的測試習慣可以大幅減少 bug、提升重構信心、加速開發流程。本篇文章介紹 Python 的測試框架和品質工具。

## unittest：標準庫測試框架

### 基本結構

Python 內建的 `unittest` 模組提供了完整的測試框架：

```python
import unittest

class TestMathOperations(unittest.TestCase):

    def setUp(self):
        """每個測試方法執行前的準備工作"""
        self.a = 10
        self.b = 5

    def tearDown(self):
        """每個測試方法執行後的清理工作"""
        pass

    def test_addition(self):
        self.assertEqual(self.a + self.b, 15)

    def test_subtraction(self):
        self.assertEqual(self.a - self.b, 5)

    def test_multiplication(self):
        self.assertEqual(self.a * self.b, 50)

    def test_division(self):
        self.assertEqual(self.a / self.b, 2)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.a / 0

if __name__ == '__main__':
    unittest.main()
```

### 斷言方法

`unittest.TestCase` 提供了豐富的斷言方法：

```python
# 相等性
self.assertEqual(a, b)
self.assertNotEqual(a, b)

# 布林值
self.assertTrue(x)
self.assertFalse(x)

# 例外
self.assertRaises(SomeException)
self.assertRaises(SomeException, func, args)

# 包含
self.assertIn(item, collection)
self.assertNotIn(item, collection)

# 型別
self.assertIsInstance(obj, MyClass)
self.assertIsNone(value)

# 浮點數比較
self.assertAlmostEqual(a, b, places=7)
```

### 測試組織

```python
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_strip(self):
        s = '  hello  '
        self.assertEqual(s.strip(), 'hello')

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

class TestListMethods(unittest.TestCase):

    def test_append(self):
        lst = [1, 2, 3]
        lst.append(4)
        self.assertEqual(lst, [1, 2, 3, 4])

    def test_pop(self):
        lst = [1, 2, 3]
        val = lst.pop()
        self.assertEqual(val, 3)
        self.assertEqual(lst, [1, 2])

if __name__ == '__main__':
    unittest.main()
```

## pytest：簡潔強大的測試框架

### 為什麼選擇 pytest？

pytest 是社群最歡迎的 Python 測試框架，原因：

- 語法簡潔，不需要繁瑣的類別結構
- 自動發現測試檔案
- 豐富的斷言重寫（更具可讀性的錯誤訊息）
- 強大的 fixtures 系統
- 豐富的插件生態

```bash
# 安裝 pytest
pip install pytest

# 執行測試
pytest
pytest tests/
pytest -v                # 詳細輸出
pytest -k "test_name"   # 只執行符合條件的測試
```

### 基本範例

```python
# test_simple.py

def add(a, b):
    return a + b

def test_addition():
    assert add(2, 3) == 5

def test_addition_negative():
    assert add(-1, -1) == -2

def test_addition_mixed():
    assert add(1, -1) == 0
```

### 進階功能

```python
import pytest

# 參數化測試
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_square(input, expected):
    assert input ** 2 == expected

# Fixtures：用於測試準備工作
@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_mean(sample_data):
    assert sum(sample_data) / len(sample_data) == 3

# 標記測試
@pytest.mark.skip(reason="功能尚未實現")
def test_future_feature():
    pass

@pytest.mark.xfail(reason="已知問題")
def test_known_bug():
    assert False

# 警告捕捉
def test_warning():
    with pytest.warns(UserWarning):
        warning_function()
```

### pytest 配置

```ini
# pytest.ini 或 setup.cfg
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow
    integration: marks integration tests
```

## 程式碼覆蓋率

### coverage 工具

```bash
# 安裝
pip install coverage

# 執行並生成覆蓋率報告
coverage run -m pytest

# 查看報告
coverage report

# 生成 HTML 報告
coverage html

# 在 terminal 顯示詳細報告
coverage report -m
```

```python
# .coveragerc
[run]
source = mypackage
omit =
    */tests/*
    */migrations/*

[report]
precision = 2
show_missing = True
skip_covered = False
```

### 覆蓋率解讀

```
Name              Stmts   Miss  Cover
-----------------------------------------
mypackage/__init__    10      2    80%
mypackage/module.py    50     10    80%
-----------------------------------------
TOTAL                60     12    80%
```

## CI/CD 整合

### 在 CI 中執行測試

```yaml
# .travis.yml
language: python
python:
  - "3.6"
install:
  - pip install -r requirements.txt
  - pip install pytest coverage
script:
  - pytest
  - coverage run -m pytest
after_success:
  - coverage report
```

```yaml
# .github/workflows/test.yml (GitHub Actions)
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.6
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest coverage
    - name: Run tests
      run: pytest -v
    - name: Coverage
      run: coverage report
```

## 結論

Python 提供了完善的測試工具鏈：

- **unittest**：標準庫，適合所有專案
- **pytest**：語法簡潔，社群活躍，功能強大
- **coverage**：測試覆蓋率分析必備工具

養成寫測試的習慣是每個專業開發者的必修課。從今天開始，為你的 Python 專案編寫測試吧！

---

## 延伸閱讀

- [pytest 官方文檔](https://www.google.com/search?q=pytest+tutorial+Python+testing)
- [unittest 官方文檔](https://www.google.com/search?q=Python+unittest+tutorial)
- [coverage.py 官方文檔](https://www.google.com/search?q=coverage+py+tutorial+Python)
- [測試驅動開發（TDD）](https://www.google.com/search?q=test+driven+development+Python+tutorial)

---

*本篇文章為「AI 程式人雜誌 2017 年 1 月號」焦點系列之一。*