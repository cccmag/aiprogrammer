# pytest 核心概念與外掛生態

## 為何選擇 pytest？

pytest 是 Python 社群中最受歡迎的測試框架，原因在於其简洁的 API、強大的功能、以及豐富的外掛生態。不同於 unittest 的類別導向風格，pytest 採用函數導向設計，讓測試程式碼更加直觀。

## 基本的測試函數

```python
def test_addition():
    assert 1 + 1 == 2

def test_string_concatenation():
    assert "Hello, " + "World" == "Hello, World"
```

pytest 會自動發現以 `test_` 開頭的檔案和函數，無需繁瑣的測試類別包裝。

## Fixtures：測試的依賴注入

Fixtures 是 pytest 最強大的功能之一，用於提供測試所需的依賴：

```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "test", "value": 42}

def test_with_fixture(sample_data):
    assert sample_data["value"] == 42
```

Fixture 可以設定作用域（function、class、module、session），控制生命週期和共享範圍。

## 參數化測試

一次定義，多種輸入：

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

這大大減少了重複程式碼，同時確保測試矩陣的完整性。

## 外掛生態

pytest 的價值在於其龐大的外掛生態：

- **pytest-cov**：整合 coverage.py，產生覆蓋率報告
- **pytest-xdist**：平行化測試執行，加速測試套件
- **pytest-mock**：整合 unittest.mock，提供更便捷的 Mock API
- **pytest-asyncio**：支援非同步測試
- **pytest-django / pytest-flask**：Web 框架專屬外掛

## 斷言重寫

pytest 採用智慧型斷言重寫，當斷言失敗時，會提供豐富的上下文資訊，包括變數值、比較過程等。這極大地改善了偵錯體驗。

## 結論

pytest 的設計哲學是「簡單的事情簡單做，複雜的事情可能做」。掌握其核心概念，能讓你快速建立有效的測試策略。