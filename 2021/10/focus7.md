# 整合測試與端對端測試策略

## 不同層級的測試

單元測試驗證最小單位的正確性，整合測試驗證元件之間的協作，端對端測試模擬真實使用者行為。三者形成測試金字塔，各有價值。

## 整合測試的焦點

整合測試關注模組間的介面和互動：

```python
import pytest
from my_app.database import Database
from my_app.user_service import UserService

@pytest.fixture
def db():
    return Database(":memory:")

@pytest.fixture
def user_service(db):
    return UserService(db)

def test_create_and_retrieve_user(user_service):
    user = user_service.create_user("Alice", "alice@example.com")
    retrieved = user_service.get_user(user.id)

    assert retrieved.name == "Alice"
    assert retrieved.email == "alice@example.com"
```

這類測試使用真實資料庫，但可能使用測試專用的配置。

## 測試資料管理

測試資料的設定和清理是整合測試的挑戰：

```python
@pytest.fixture
def clean_db(db):
    """每個測試前清空資料庫"""
    db.clear_all_tables()
    yield db
    db.clear_all_tables()
```

使用 fixtures 管理測試資料的生命週期。

## 隔離與並列

整合測試應該相互隔離：

```python
@pytest.fixture
def unique_email():
    """每次產生唯一的 email"""
    import uuid
    return f"test-{uuid.uuid4()}@example.com"
```

使用唯一識別符避免測試間衝突。

## 端對端測試

端對端測試模擬真實使用者操作：

```python
from selenium import webdriver

def test_user_login():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/login")

    driver.find_element("name", "username").send_keys("testuser")
    driver.find_element("name", "password").send_keys("password123")
    driver.find_element("type", "submit").click()

    assert "Welcome" in driver.page_source
    driver.quit()
```

 Selenium、Playwright、Cypress 等工具常用於 Web 應用的端對端測試。

## API 測試

對於 API，requests 庫是常用選擇：

```python
import requests

def test_api_create_user(api_base_url):
    response = requests.post(
        f"{api_base_url}/users",
        json={"name": "Bob", "email": "bob@example.com"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Bob"
```

可以使用 `pytest-vcr` 記錄和重放 HTTP 互動，加速測試並確保穩定性。

## 测试策略建議

- 單元測試：快速、隔離、多
- 整合測試：覆蓋關鍵路徑、中等數量
- 端對端測試：少量高價值的核心流程

合理的測試組合能在品質保證和開發速度間取得平衡。