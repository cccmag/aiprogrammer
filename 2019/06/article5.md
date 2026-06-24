# 單元測試：pytest 進階技巧

## 前言

pytest 是 Python 最流行的測試框架。

## 基本使用

```python
import pytest

def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
```

## Fixtures

```python
@pytest.fixture
def sample_data():
    return [1, 2, 3]

def test_sum(sample_data):
    assert sum(sample_data) == 6
```

## Mock

```python
from unittest.mock import patch

@patch('module.function')
def test_with_mock(mock_func):
    mock_func.return_value = 42
    result = module.function()
    assert result == 42
```

## 延伸閱讀

- [pytest 文檔](https://www.google.com/search?q=pytest+tutorial)