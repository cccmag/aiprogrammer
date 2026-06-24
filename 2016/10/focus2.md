# TDD 開發方法論（2003-2016）

## 前言

測試驅動開發（Test-Driven Development, TDD）由 Kent Beck 在 2003 年提出，強調「紅、綠、重構」的開發循環。

## TDD 核心循環

```
1. 寫一個會失敗的測試（Red）
2. 寫最少量程式碼讓測試通過（Green）
3. 重構程式碼（Refactor）
重複循環
```

## 實際範例：驗證登入功能

### 第一步：Red（寫失敗的測試）

```python
# test_login.py
import pytest

def test_login_with_valid_credentials():
    auth = AuthService()
    result = auth.login("user@example.com", "password123")
    assert result.is_authenticated == True
    assert result.token is not None

def test_login_with_invalid_credentials():
    auth = AuthService()
    result = auth.login("user@example.com", "wrong")
    assert result.is_authenticated == False
```

### 第二步：Green（寫最少量程式碼）

```python
# auth.py
class AuthResult:
    def __init__(self, authenticated, token=None):
        self.is_authenticated = authenticated
        self.token = token

class AuthService:
    def login(self, email, password):
        # 最簡單的通過實作
        if email == "user@example.com" and password == "password123":
            return AuthResult(True, "mock_token")
        return AuthResult(False)
```

### 第三步：Refactor（重構）

```python
# 重構後的 auth.py
class AuthResult:
    def __init__(self, authenticated, token=None):
        self.is_authenticated = authenticated
        self.token = token

class AuthService:
    def __init__(self, user_repo, token_generator):
        self.user_repo = user_repo
        self.token_generator = token_generator
    
    def login(self, email, password):
        user = self.user_repo.find_by_email(email)
        if user and user.verify_password(password):
            token = self.token_generator.generate(user)
            return AuthResult(True, token)
        return AuthResult(False)
```

## TDD 的優點

1. **及早發現問題**：錯誤在產生的當下就被捕捉
2. **更好的設計**：被迫思考 API 設計
3. **文件化**：測試就是規格說明
4. **安心重構**：有測試保護，快速發現回歸

## TDD 的挑戰

1. 學習曲線陡峭
2. 對UI與系統整合較難適用
3. 需要紀律，堅持不跳過測試

## TDD vs 傳統開發

| 面向 | 傳統開發 | TDD |
|------|----------|-----|
| 測試時機 | 開發後 | 開發前 |
| 測試覆蓋 | 往往不足 | 自然高覆蓋 |
| 重構信心 | 低 | 高 |
| 開發速度 | 前期快 | 前期慢，後期快 |

## 相關資源

- [Kent Beck TDD 原著](https://www.google.com/search?q=Kent+Beck+Test+Driven+Development)
- [TDD 教學資源](https://www.google.com/search?q=test+driven+development+tutorial+2016)
- [Python pytest TDD](https://www.google.com/search?q=python+tdd+pytest+tutorial)

## 結語

TDD 不是銀彈，但在多數場景下能顯著提升程式碼品質與可維護性。從今天開始，試著在寫新功能前先寫測試。

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*