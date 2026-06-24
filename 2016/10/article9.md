# 安全性測試基礎

## 前言

安全性測試找出系統的安全漏洞，防止惡意攻擊與資料外洩。OWASP 是安全性測試的重要參考。

## 常見安全漏洞

| 漏洞 | 說明 | 測試重點 |
|------|------|----------|
| SQL 注入 | 惡意 SQL 執行 | 輸入驗證 |
| XSS | 跨站腳本攻擊 | 輸出編碼 |
| CSRF | 跨站請求偽造 | Token 驗證 |
| 認證缺失 | 未授权訪問 | 權限檢查 |

## SQL 注入測試

```python
# test_security_sql_injection.py
import pytest
from flask import json

def test_sql_injection_prevention(client):
    malicious_inputs = [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "admin'--",
        "' UNION SELECT * FROM users--"
    ]
    
    for input in malicious_inputs:
        response = client.post('/api/users', json={
            'email': input,
            'name': 'Test'
        })
        # 應被拒絕或消毒
        assert response.status_code in [400, 422]

def test_sql_injection_in_query(client):
    # 嘗試在查詢參數中注入
    response = client.get("/api/users?name=' OR '1'='1")
    
    # 不應返回所有使用者
    data = json.loads(response.data)
    assert len(data) <= 1 or all(u['name'] != "' OR '1'='1" for u in data)
```

## XSS 測試

```python
def test_xss_prevention(client):
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>",
        "javascript:alert('XSS')",
        "<svg onload=alert(1)>"
    ]
    
    response = client.post('/api/users', json={
        'email': 'test@example.com',
        'name': xss_payloads[0]
    })
    
    data = json.loads(response.data)
    # 名稱不應包含未經轉義的腳本標籤
    assert '<script>' not in data.get('name', '')
```

## CSRF 測試

```python
def test_csrf_protection(client):
    # 沒有 CSRF token 的請求應該被拒絕
    response = client.post('/api/settings', json={
        'setting': 'value'
    })
    
    assert response.status_code == 403

def test_csrf_with_valid_token(client):
    # 取得 CSRF token
    token_response = client.get('/api/csrf-token')
    token = json.loads(token_response.data)['token']
    
    # 攜帶有效 token 的請求應該成功
    response = client.post('/api/settings',
        json={'setting': 'value'},
        headers={'X-CSRF-Token': token}
    )
    
    assert response.status_code == 200
```

## 認證與授權測試

```python
def test_authentication_required(client):
    response = client.get('/api/protected')
    assert response.status_code == 401

def test_invalid_credentials(client):
    response = client.post('/api/auth/login', json={
        'email': 'user@example.com',
        'password': 'wrong_password'
    })
    assert response.status_code == 401

def test_authorization_level(client):
    # 以一般使用者身份登入
    user_token = login_as('user@example.com', 'password123')
    
    # 嘗試訪問管理員功能
    response = client.get('/api/admin/users',
        headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403

def test_authorization_admin(client):
    # 以管理員身份登入
    admin_token = login_as('admin@example.com', 'admin_password')
    
    # 訪問管理員功能應該成功
    response = client.get('/api/admin/users',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
```

## 密碼安全測試

```python
def test_password_hashing(client):
    response = client.post('/api/users', json={
        'email': 'new@example.com',
        'password': 'weak'
    })
    # 弱密碼應被拒絕
    assert response.status_code == 400

def test_password_not_in_response(client):
    response = client.post('/api/users', json={
        'email': 'test@example.com',
        'password': 'secret123'
    })
    
    data = json.loads(response.data)
    assert 'password' not in data
    assert 'password_hash' not in data
    assert 'secret123' not in str(data)
```

## 安全測試工具

```bash
# OWASP ZAP 指令列
zap-cli quick-scan http://localhost:3000

# SQLMap SQL 注入檢測
sqlmap -u "http://localhost:3000/api/users?id=1"

# Nmap 連接埠掃描
nmap -sV localhost -p 3000
```

## 安全檢查清單

1. 所有輸入都有驗證
2. SQL 查詢使用參數化
3. 輸出內容適當編碼
4. CSRF token 保護狀態改變操作
5. 認證失敗不回傳過多資訊
6. 密碼使用強雜湊
7. HTTPS 保護敏感傳輸

## 延伸閱讀

- [OWASP 安全性測試指南](https://www.google.com/search?q=owasp+security+testing+guide+2016)
- [SQL 注入防護](https://www.google.com/search?q=sql+injection+prevention+2016)
- [XSS 防護實踐](https://www.google.com/search?q=xss+prevention+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*