# 測試與除錯

## pytest 基礎

```bash
pip install pytest
```

```python
# test_math.py
import pytest

def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0

def test_add_strings():
    with pytest.raises(TypeError):
        add("hello", 1)
```

```bash
pytest test_math.py
```

## 斷言

```python
def test_assertions():
    assert x == 3
    assert x > 0, "x must be positive"
    assert x in [1, 2, 3]
    assert isinstance(x, int)
```

## Fixtures

```python
@pytest.fixture
def sample_data():
    return {"name": "test", "value": 42}

def test_with_fixture(sample_data):
    assert sample_data["value"] == 42
```

## 參數化測試

```python
@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

## 除錯技巧

```python
import pdb

def buggy_function(x):
    result = x * 2
    pdb.set_trace()  # 中斷點
    return result

# 常用 pdb 命令
# n: 下一行
# s: 進入函式
# c: 繼續執行
# p variable: 印出變數
```

## Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def function_with_logging(x):
    logger.debug(f"Input: {x}")
    result = x * 2
    logger.info(f"Result: {result}")
    return result
```

## 異常處理

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    print("Clean up")
```

## 總結

良好的測試習慣提升代碼品質：
- 使用 pytest 編寫單元測試
- 利用 fixtures 管理測試資料
- 參數化減少重複測試
- pdb 和 logging 幫助除錯