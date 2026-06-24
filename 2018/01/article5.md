# 測試與除錯技巧

## 簡介

好的程式需要良好的測試和除錯機制。本篇介紹 Python 的測試框架和除錯技巧。

## assert 斷言

```python
def add(a, b):
    return a + b

# 基本斷言
assert add(1, 2) == 3
assert add(0, 0) == 0
assert add(-1, 1) == 0

# 帶訊息的斷言
assert add(1, 2) == 3, "加法應該正確"

# 觸發 AssertionError
# assert 1 + 1 == 3, "這會失敗"
```

## pytest 測試框架

### 安裝

```bash
pip install pytest
```

### 基本測試

```python
# test_calculator.py
def add(a, b):
    return a + b

def test_add_positive():
    assert add(1, 2) == 3

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 0) == 0
```

### 執行測試

```bash
pytest test_calculator.py
pytest test_calculator.py -v      # 詳細模式
pytest test_calculator.py -x      # 遇錯即停
pytest test_calculator.py -k add   # 只執行名稱包含 add 的測試
```

### 參數化測試

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (-2, -3, -5),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### 拋出例外的測試

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("除數不能為零")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError, match="除數不能為零"):
        divide(10, 0)
```

### fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15

def test_average(sample_data):
    assert sum(sample_data) / len(sample_data) == 3
```

## unittest 標準庫

```python
import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_divide(self):
        self.assertRaises(ZeroDivisionError, divide, 10, 0)

if __name__ == "__main__":
    unittest.main()
```

## 除錯技巧

### print 除錯

```python
def buggy_function(n):
    result = 1
    for i in range(n):
        result *= i
        print(f"i={i}, result={result}")  # 除錯輸出
    return result
```

### assert 除錯

```python
def safe_divide(a, b):
    assert b != 0, "除數不能為零"
    return a / b
```

### logging 模組

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process(data):
    logger.debug(f"Processing: {data}")
    result = data * 2
    logger.info(f"Result: {result}")
    return result
```

## pdb 除錯器

### 設定中斷點

```python
import pdb

def buggy_function(n):
    result = 0
    pdb.set_trace()  # 設定中斷點
    for i in range(n):
        result += i
    return result

buggy_function(5)
```

### pdb 命令

| 命令 | 說明 |
|------|------|
| n | 執行下一行 |
| s | 進入函式 |
| c | 繼續執行 |
| p 變數 | 印出變數值 |
| l | 顯示目前程式碼 |
| q | 結束除錯 |

### IPython 除錯

```bash
pip install ipdb
python -m ipdb script.py
```

## IDE 除錯

### VS Code

1. 在程式碼左側點擊設定中斷點
2. 按 F5 開始除錯
3. 使用除錯工具列逐步執行

### PyCharm

1. 點擊行號左側設定中斷點
2. 按 Shift+F9 開始除錯
3. 使用 Variables、Watches 檢視變數

## 練習題

1. 為以下函式寫單元測試：
```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

2. 使用 logging 模組重構你的程式碼
3. 使用 pdb 找出以下程式的錯誤：
```python
def find_max(numbers):
    max = numbers[0]
    for n in numbers:
        if n > max:
            max = n
    return max
```