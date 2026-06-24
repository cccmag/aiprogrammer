# 測試金字塔策略

## 前言

測試金字塔指導我們如何分配測試資源：底部是大量的單元測試，中間是整合測試，頂部是少量的端對端測試。

## 金字塔結構

```
           /\
          /  \      E2E (5-10%)
         /----\     Integration (20-30%)
        /      \
       /--------\  Unit (60-70%)
      /__________\
```

## 為何需要金字塔

| 層級 | 速度 | 成本 | 信心 |
|------|------|------|------|
| 單元測試 | 快（ms） | 低 | 局部 |
| 整合測試 | 中（s） | 中 | 組件 |
| E2E 測試 | 慢（min） | 高 | 全域 |

## Python 實作

### 單元測試層

```python
# test_models.py
import pytest

class TestUserModel:
    def test_create_user(self):
        user = User(name='Test', email='test@example.com')
        assert user.name == 'Test'
        assert user.email == 'test@example.com'
        assert user.is_active == True
    
    def test_user_validation(self):
        with pytest.raises(ValidationError):
            User(email='invalid-email')
    
    def test_password_hashing(self):
        user = User(password='secret')
        assert user.password_hash != 'secret'
        assert user.verify_password('secret')
        assert not user.verify_password('wrong')
```

### 整合測試層

```python
# test_integration.py
import pytest
from myapp import create_app, db

@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    with app.app_context():
        db.create_all()
    yield app
    db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_api(client):
    response = client.post('/api/users', json={
        'name': 'Test',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    
    response = client.get('/api/users')
    assert response.status_code == 200
    assert len(response.get_json()) == 1
```

### E2E 測試層

```python
# test_e2e.py
from selenium import webdriver

def test_complete_user_flow():
    driver = webdriver.Firefox()
    try:
        driver.get('http://localhost:3000')
        
        # 註冊
        driver.find_element(By.LINK_TEXT, '註冊').click()
        driver.find_element(By.NAME, 'email').send_keys('new@example.com')
        driver.find_element(By.NAME, 'password').send_keys('password123')
        driver.find_element(By.TYPE, 'submit').click()
        
        # 驗證
        assert '成功註冊' in driver.page_source
        
        # 登入
        driver.find_element(By.NAME, 'email').send_keys('new@example.com')
        driver.find_element(By.NAME, 'password').send_keys('password123')
        driver.find_element(By.TYPE, 'submit').click()
        
        # 驗證登入成功
        assert '歡迎' in driver.page_source
    finally:
        driver.quit()
```

## 實戰策略

### 1. 從下而上建構

先建立穩固的單元測試基礎，再逐步增加整合測試與 E2E 測試。

### 2. 識別關鍵路徑

```python
# 識別業務關鍵路徑
CRITICAL_PATHS = [
    'user_registration',
    'payment_processing',
    'order_completion'
]

# 這些路徑需要完整的三層測試覆蓋
```

### 3. 測試隔離

```python
# 使用 fixture 隔離測試
@pytest.fixture
def clean_db():
    db.drop_all()
    db.create_all()
    yield
    db.drop_all()

def test_with_isolation(clean_db):
    # 每個測試都有乾淨的資料庫
    User.create(email='test@example.com')
    assert User.count() == 1
```

## 常見錯誤

1. **過度依賴 E2E**：維護成本高、執行緩慢
2. **忽視整合測試**：單元測試通過但系統整合失敗
3. **測試脆弱**：過度依賴實作細節

## 延伸閱讀

- [測試金字塔策略](https://www.google.com/search?q=test+pyramid+strategy+2016)
- [測試分層最佳實踐](https://www.google.com/search?q=testing+layered+approach+2016)
- [單元測試vs整合測試](https://www.google.com/search?q=unit+vs+integration+testing+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*