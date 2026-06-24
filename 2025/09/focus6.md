# 整合測試與端到端測試

## 從單一元件到完整系統的測試策略

### 前言

單元測試確保每個元件單獨工作正常，但元件之間的協作才是軟體系統真正複雜的地方。整合測試（Integration Testing）和端到端測試（End-to-End Testing）補足了單元測試無法覆蓋的空白——它們驗證了元件之間的互動是否如預期般工作。

### 單元測試 vs 整合測試 vs E2E 測試

| 層級 | 測試對象 | 優點 | 缺點 |
|------|---------|------|------|
| 單元測試 | 單一函數/類別 | 快速、穩定、精確定位 | 無法發現整合問題 |
| 整合測試 | 多個元件的協作 | 發現介面問題 | 比單元測試慢 |
| E2E 測試 | 完整使用者流程 | 最接近真實使用場景 | 慢、不穩定、維護成本高 |

### 整合測試的策略

整合測試的核心問題是：**應該整合到什麼程度？**

**大爆炸整合（Big Bang）**

一次整合所有元件。問題是：當測試失敗時，很難判斷是哪個元件出了問題。

**由上而下（Top-Down）**

從頂層（UI/API）開始，逐步加入底層元件。上層使用 Mock，底層逐步替換為真實實作。

**由下而上（Bottom-Up）**

從底層元件開始測試，逐步往上整合。先測試資料庫存取層，再測試業務邏輯層，最後測試 API 層。

**三明治整合（Sandwich）**

結合由上而下和由下而上，兩端同時進行，在中間會合。

### 資料庫整合測試

資料庫測試是最常見的整合測試場景。以下是一些最佳實踐：

**使用測試資料庫**

永遠不要對生產資料庫執行測試。使用專門的測試資料庫或記憶體資料庫（如 SQLite `:memory:`）：

```python
import sqlite3
import pytest

@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INT, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")
    yield conn
    conn.close()

def test_query_user(db):
    cursor = db.execute("SELECT name FROM users WHERE id = 1")
    assert cursor.fetchone()[0] == "Alice"
```

**事務回滾**

在每個測試後使用資料庫事務回滾，確保測試之間的隔離：

```python
@pytest.fixture
def db_session(connection):
    connection.begin()
    yield connection
    connection.rollback()  # 復原所有變更
```

### API 整合測試

對於 Web 應用，API 測試是整合測試的核心。以 Flask 為例：

```python
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    response = client.post("/api/users", json={
        "name": "Bob",
        "email": "bob@example.com"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Bob"
```

### 端到端測試

端到端測試模擬真實使用者的操作流程。最常用的工具是 Selenium 和 Playwright。

**Selenium 範例**：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_user_login():
    driver = webdriver.Chrome()
    driver.get("https://example.com/login")
    
    driver.find_element(By.ID, "username").send_keys("alice")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "login-button").click()
    
    assert "Dashboard" in driver.title
    driver.quit()
```

**Playwright 範例**（更現代、更穩定）：

```python
from playwright.sync_api import sync_playwright

def test_user_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.com")
        page.fill("#search", "Python testing")
        page.click("#search-button")
        assert page.locator(".result").count() > 0
        browser.close()
```

### E2E 測試的最佳實踐

**少而精**

E2E 測試應該專注於「關鍵使用者旅程」（Critical User Journeys）——登入、註冊、下單、付款等核心流程。不要試圖用 E2E 測試覆蓋所有邊界情況。

**使用 Page Object 模式**

```python
class LoginPage:
    def __init__(self, page):
        self.page = page
    
    def navigate(self):
        self.page.goto("https://example.com/login")
    
    def login(self, username, password):
        self.page.fill("#username", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
    
    def is_logged_in(self):
        return self.page.locator(".user-profile").is_visible()

def test_login(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("alice", "password123")
    assert login_page.is_logged_in()
```

**隔離測試數據**

每個 E2E 測試應該建立自己的測試數據，不要依賴其他測試的狀態。測試執行順序不應該影響結果。

**處理非同步操作**

```python
def test_async_operation(page):
    page.click("#start-job")
    # 等待非同步操作完成
    page.wait_for_selector(".job-complete", timeout=10000)
    assert page.locator(".job-complete").is_visible()
```

### 測試資料的管理

測試資料是整合測試中最棘手的問題之一。常見的策略：

- **Factory Boy**：自動產生測試資料
- **Fixtures**：每個測試的固定資料集
- **資料庫種子**：每次測試前匯入標準資料
- **API 錄製/回放**：使用 VCR.py 等工具錄製外部 API 的回應

### 小結

整合測試和 E2E 測試是測試策略中不可或缺的一層。單元測試告訴你「每個零件是否正常」，整合測試告訴你「零件之間能否協作」，E2E 測試告訴你「整個系統是否能滿足使用者需求」。三層測試相輔相成，共同構築軟體品質的防線。

---

**下一步**：[CI/CD 與自動化測試](focus7.md)

## 延伸閱讀

- [整合測試最佳實踐](https://www.google.com/search?q=integration+testing+best+practices)
- [Playwright Python 文件](https://www.google.com/search?q=Playwright+Python+documentation)
- [Selenium 與 WebDriver](https://www.google.com/search?q=Selenium+WebDriver+tutorial)
