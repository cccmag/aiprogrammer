# 整合測試與端對端測試（2012-2016）

## 前言

單元測試驗證個別元件，整合測試驗證元件間的互動，端對端測試驗證整個系統的行為。

## 測試金字塔

```
        /\
       /  \      E2E 測試（少量、耗時）
      /----\
     /      \    整合測試（中量）
    /--------\
   /          \  單元測試（大量、快速）
  /____________\
```

## 整合測試實作

### Python：pytest + Flask

```python
# test_integration.py
import pytest
from myapp import create_app
from database import init_db, seed_test_data

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        with app.app_context():
            init_db()
            seed_test_data()
        yield client

def test_get_all_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert data[0]['email'] == 'test@example.com'

def test_create_user(client):
    response = client.post('/api/users', json={
        'email': 'new@example.com',
        'name': 'New User'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['email'] == 'new@example.com'
```

### Node.js：supertest + Express

```javascript
// test/integration/users.test.js
const request = require('supertest');
const app = require('../../app');

describe('User API Integration', () => {
  it('GET /api/users - should return users', async () => {
    const res = await request(app)
      .get('/api/users')
      .expect(200);
    
    expect(res.body.length).toBeGreaterThan(0);
  });
  
  it('POST /api/users - should create user', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'new@test.com', name: 'New User' })
      .expect(201);
    
    expect(res.body.email).toBe('new@test.com');
  });
});
```

## 端對端測試：Selenium

```python
# test_e2e.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_flow():
    driver = webdriver.Firefox()
    try:
        driver.get('http://localhost:3000/login')
        
        # 填入帳密
        driver.find_element(By.NAME, 'email').send_keys('user@example.com')
        driver.find_element(By.NAME, 'password').send_keys('password123')
        driver.find_element(By.ID, 'login-btn').click()
        
        # 等待歡迎訊息
        welcome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'welcome-message'))
        )
        assert '歡迎' in welcome.text
    finally:
        driver.quit()
```

## Docker 容器化測試環境

```bash
# docker-compose.test.yml
version: '3'
services:
  app:
    build: .
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:9.6
  
  redis:
    image: redis:3.2
```

```bash
# 運行測試
docker-compose -f docker-compose.test.yml up -d
docker-compose -f docker-compose.test.yml exec app pytest
```

## Mock 外部服務

```python
# test_with_mocks.py
import responses
from myapp import GitHubClient

@responses.activate
def test_github_api():
    responses.add(
        responses.GET,
        'https://api.github.com/user',
        json={'login': 'testuser', 'id': 123},
        status=200
    )
    
    client = GitHubClient()
    user = client.get_user()
    
    assert user['login'] == 'testuser'
    assert len(responses.calls) == 1
```

## 相關資源

- [Selenium 官網](https://www.google.com/search?q=selenium+webdriver+testing+2016)
- [整合測試最佳實踐](https://www.google.com/search?q=integration+testing+best+practices+2016)
- [Docker 測試環境](https://www.google.com/search?q=docker+testing+environment+2016)

## 結語

完整的測試策略需要單元測試的廣度、整合測試的深度，以及必要的端對端測試覆蓋。

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*