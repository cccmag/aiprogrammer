# pytest 快速上手

## 前言

pytest 是 Python 生態中最受歡迎的測試框架。與 unittest 相比，pytest 的設計哲學是「簡單測試不需要樣板程式碼」——普通的 Python 函數加上 `assert` 語句就可以成為測試。本文將帶你從零開始使用 pytest。

## 安裝

```bash
pip install pytest
```

驗證安裝：

```bash
pytest --version
```

## 你的第一個 pytest 測試

```python
# test_sample.py
def test_addition():
    assert 1 + 1 == 2

def test_string():
    assert "hello".upper() == "HELLO"
```

執行：

```bash
$ pytest test_sample.py -v
========================== test session starts ==========================
collected 2 items

test_sample.py::test_addition PASSED
test_sample.py::test_string PASSED

========================== 2 passed in 0.02s ===========================
```

## 測試發現規則

pytest 會自動尋找符合以下條件的檔案和函數：

- **檔案**：`test_*.py` 或 `*_test.py`
- **函數**：`test_` 開頭的函數
- **類別**：`Test` 開頭的類別中的 `test_` 開頭的方法

## 重要的命令行選項

```bash
# 詳細輸出
pytest -v

# 在第一個失敗時停止
pytest -x

# 顯示區域變數
pytest -l

# 顯示完整 traceback
pytest --tb=long

# 執行特定的測試
pytest test_module.py::test_function

# 包含標記匹配
pytest -k "add or subtract"

# 跳過慢速測試
pytest -m "not slow"
```

## 使用 Python 類別組織測試

```python
class TestCalculator:
    def test_addition(self):
        assert 1 + 2 == 3

    def test_subtraction(self):
        assert 5 - 3 == 2
```

注意：與 unittest 不同，pytest 的測試類別不需要繼承 `TestCase`，也不需要 `self.assertEqual`——普通的 `assert` 就夠了。

## 使用 fixture

Fixture 是 pytest 最強大的功能之一。它取代了 unittest 中的 `setUp`/`tearDown`：

```python
import pytest

@pytest.fixture
def calculator():
    """提供一個 Calculator 實例"""
    return Calculator("PytestCalc")

def test_add(calculator):
    assert calculator.add(2, 3) == 5

def test_subtract(calculator):
    assert calculator.subtract(5, 2) == 3
```

## 參數化測試

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("pytest", "PYTEST"),
    ("Python", "PYTHON"),
])
def test_upper(input, expected):
    assert input.upper() == expected
```

## 測試例外

```python
def test_raises():
    with pytest.raises(ValueError, match="invalid"):
        int("abc")
```

## 跳過測試

```python
@pytest.mark.skip(reason="功能尚未完成")
def test_future():
    ...

@pytest.mark.skipif(sys.version_info < (3, 10),
                     reason="需要 Python 3.10+")
def test_new_feature():
    ...

@pytest.mark.xfail(reason="已知 Bug")
def test_known_bug():
    assert 1 == 2
```

## conftest.py

`conftest.py` 是 pytest 的共享 fixture 定義檔案。放在目錄中的 `conftest.py` 會自動對該目錄及其子目錄的所有測試生效：

```python
# conftest.py
import pytest
from myapp import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()
```

```python
# test_routes.py（不需要 import conftest）
def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
```

## 外掛推薦

```bash
pip install pytest-cov pytest-xdist pytest-mock
```

| 外掛 | 功能 |
|------|------|
| pytest-cov | 覆蓋率報告 |
| pytest-xdist | 平行執行測試 |
| pytest-mock | Mock 整合 |
| pytest-timeout | 測試超時控制 |
| pytest-html | HTML 報告 |

## 小結

pytest 讓寫測試變得簡單而愉快。你不需要學習複雜的 API——只需要知道 `assert` 和 `pytest.raises`，就可以開始寫測試了。隨著需求增長，你可以逐步引入 fixture、參數化、外掛等高級功能。

## 延伸閱讀

- [pytest 官方入門指南](https://www.google.com/search?q=pytest+getting+started)
- [pytest 命令行選項](https://www.google.com/search?q=pytest+command+line+options)
- [pytest 與 unittest 對比](https://www.google.com/search?q=pytest+vs+unittest+comparison)
