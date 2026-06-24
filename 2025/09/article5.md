# pytest fixture 與 conftest

## 前言

Fixture 是 pytest 最核心的功能之一。它提供了一個強大的依賴注入系統，讓測試可以宣告它需要的資源，而 pytest 負責管理這些資源的建立、共享和清理。`conftest.py` 則讓 fixture 可以在多個測試檔案之間共享。

## 什麼是 Fixture？

Fixture 是一個由 `@pytest.fixture` 裝飾器標記的函數，它提供測試所需的資源：

```python
import pytest

@pytest.fixture
def db_connection():
    """建立資料庫連線"""
    conn = create_database_connection()
    yield conn  # 測試執行
    conn.close()  # 測試後清理
```

測試函數透過參數名稱宣告它需要的 fixture：

```python
def test_query_user(db_connection):
    result = db_connection.query("SELECT * FROM users")
    assert len(result) > 0
```

## Fixture 的作用域

Fixture 可以控制它的生命週期：

```python
@pytest.fixture(scope="function")  # 預設：每個測試重新建立
def fresh_data():
    return {"counter": 0}

@pytest.fixture(scope="class")     # 每個測試類別共用
def class_level_resource():
    return ExpensiveResource()

@pytest.fixture(scope="module")    # 每個模組共用
def module_level_resource():
    return DatabaseConnection()

@pytest.fixture(scope="session")   # 整個測試階段共用一次
def global_config():
    return load_configuration()
```

選擇作用域的原則：**作用域越小，測試越隔離；作用域越大，測試越快**。

## Autouse Fixture

有時候你需要一個 fixture 自動對所有測試生效，而不需要在每個測試中宣告它：

```python
@pytest.fixture(autouse=True)
def setup_test_environment():
    """每個測試前自動設定環境變數"""
    os.environ["TESTING"] = "true"
    yield
    del os.environ["TESTING"]

# 測試不需要宣告這個 fixture
def test_environment():
    assert os.environ.get("TESTING") == "true"
```

## Fixture 參數化

Fixture 本身也可以參數化，讓測試使用不同的 fixture 實例：

```python
@pytest.fixture(params=["sqlite", "postgresql"])
def database(request):
    if request.param == "sqlite":
        return create_sqlite_connection()
    elif request.param == "postgresql":
        return create_postgresql_connection()
```

當 fixture 被參數化時，所有依賴它的測試都會對每個參數執行一次。

## conftest.py：共享 Fixture

`conftest.py` 是 pytest 的共享設定檔案。它的特殊之處在於：

- 不需要 import——pytest 會自動載入
- 其中的 fixture 對所在目錄及其子目錄的所有測試可用

典型的專案結構：

```
tests/
├── conftest.py          # 全域 fixture
│   ├── fixture app
│   └── fixture client
├── test_auth/
│   ├── conftest.py      # auth 專用 fixture
│   └── test_login.py
└── test_api/
    ├── conftest.py      # API 專用 fixture
    └── test_users.py
```

## conftest.py 範例

```python
# tests/conftest.py
import pytest
from myapp import create_app, db

@pytest.fixture(scope="session")
def app():
    """建立應用實例"""
    return create_app()

@pytest.fixture
def client(app):
    """提供測試用戶端"""
    return app.test_client()

@pytest.fixture(autouse=True)
def setup_database():
    """確保資料庫測試隔離"""
    db.create_all()
    yield
    db.drop_all()
```

## Fixture 的最佳實踐

**保持 fixture 簡單**：一個 fixture 只負責一件事。如果你的 fixture 既建立資料庫連線又插入測試資料，考慮拆分成兩個 fixture。

**明確宣告依賴**：fixture 可以依賴其他 fixture：

```python
@pytest.fixture
def user(db_session):
    user = User(name="Alice")
    db_session.add(user)
    db_session.commit()
    return user

def test_user_profile(user, client):
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
```

**使用 Yield 實現清理**：`yield` 之前的程式碼是「設定」，之後的程式碼是「清理」：

```python
@pytest.fixture
def temp_file():
    f = tempfile.NamedTemporaryFile(delete=False)
    yield f.name
    os.unlink(f.name)  # 測試結束後刪除檔案
```

## 小結

Fixture 和 conftest 是 pytest 的核心競爭力。Fixture 提供了一個優雅的方式來管理測試資源，conftest 讓 fixture 可以在整個測試專案中共享。掌握這兩者，你就可以寫出乾淨、可維護、高效率的測試程式碼。

## 延伸閱讀

- [pytest fixture 官方文件](https://www.google.com/search?q=pytest+fixture+documentation)
- [conftest.py 最佳實踐](https://www.google.com/search?q=pytest+conftest+best+practices)
- [fixture 作用域深入理解](https://www.google.com/search?q=pytest+fixture+scope+explained)
