# pytest 進階測試

## 現代 Python 測試的黃金標準

### 前言

pytest 是 Python 生態中最受歡迎的測試框架。根據 JetBrains 的 2025 年開發者調查，超過 80% 的 Python 開發者使用 pytest。它的成功來自於一個簡單的設計哲學：**測試應該是簡單、直覺、沒有樣板程式碼的**。

### pytest 的設計哲學

與 unittest 不同，pytest 不需要你繼承任何類別。任何以 `test_` 開頭的函數都是測試：

```python
# 這是一個有效的 pytest 測試
def test_addition():
    assert 1 + 1 == 2

def test_string_operation():
    assert "hello".upper() == "HELLO"
```

不需要 import unittest，不需要繼承 TestCase，不需要使用 self.assertEqual。普通的 `assert` 語句就可以——pytest 會透過斷言內省（assertion introspection）機制自動提供豐富的錯誤訊息。

### pytest 的核心優勢

**詳細的斷言訊息**

當測試失敗時，pytest 會顯示詳細的上下文：

```
E   assert 2 + 2 == 5
E    +  where 2 + 2 = 4
```

**自動測試發現**

pytest 自動尋找當前目錄下所有 `test_*.py` 或 `*_test.py` 檔案，執行其中所有 `test_` 開頭的函數或方法。

**豐富的外掛生態**

pytest 有超過 1000 個外掛，涵蓋覆盖率、並行執行、Flask/Django 測試、HTTP 模擬等場景。

### Fixture 機制

pytest 的 fixture 是取代 unittest 中 `setUp`/`tearDown` 的現代方案：

```python
import pytest

@pytest.fixture
def calculator():
    return Calculator("TestCalc")

def test_addition(calculator):
    assert calculator.add(1, 2) == 3

def test_subtraction(calculator):
    assert calculator.subtract(5, 3) == 2
```

Fixture 的關鍵特性：

- **依賴注入**：測試函數透過參數宣告依賴，pytest 自動注入
- **作用域控制**：`scope="function"`（預設，每個測試重新建立）、`"class"`、`"module"`、`"session"`
- **自動使用**：`@pytest.fixture(autouse=True)` 自動對所有測試生效
- **Teardown 支援**：使用 `yield` 代替 `return`，`yield` 之後的程式碼在測試結束後執行

```python
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()  # 測試結束後自動清理
```

### conftest.py

`conftest.py` 是 pytest 的共享 fixture 定義檔案。放在某個目錄下的 `conftest.py` 中的 fixture，對該目錄及其子目錄的所有測試都可用：

```python
# tests/conftest.py
@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()
```

```python
# tests/test_routes.py
def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
```

### 參數化測試

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### 外掛生態

pytest 的外掛透過 `pip install` 安裝後自動啟用：

| 外掛 | 用途 |
|------|------|
| pytest-cov | 程式碼覆蓋率報告 |
| pytest-xdist | 平行執行測試 |
| pytest-mock | unittest.mock 的 pytest 整合 |
| pytest-flask | Flask 應用測試 |
| pytest-django | Django 應用測試 |
| pytest-httpx | HTTPX 用戶端模擬 |
| pytest-benchmark | 基準測試 |

### 自訂標記（Custom Markers）

```python
@pytest.mark.slow
def test_heavy_computation():
    ...

@pytest.mark.skip(reason="功能尚未完成")
def test_future_feature():
    ...
```

執行特定標記的測試：

```bash
pytest -m slow          # 執行 slow 標記的測試
pytest -m "not slow"    # 跳過 slow 標記的測試
```

### 小結

pytest 之所以成為 Python 測試的事實標準，不是因為它有什麼殺手級功能，而是因為它讓寫測試這件事變得簡單、愉快。當開發者不需要思考「測試框架怎麼用」，而是專注於「我要測試什麼」時，測試的品質和數量自然會提升。

---

**下一步**：[測試驅動開發 TDD](focus4.md)

## 延伸閱讀

- [pytest 官方文件](https://www.google.com/search?q=pytest+documentation)
- [pytest fixture 深入](https://www.google.com/search?q=pytest+fixture+deep+dive)
- [pytest 外掛列表](https://www.google.com/search?q=pytest+plugins+list)
