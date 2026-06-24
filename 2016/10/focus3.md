# BDD 行為驅動開發（2008-2016）

## 前言

行為驅動開發（Behavior-Driven Development, BDD）由 Dan North 在 2008 年提出，是 TDD 的延伸，強調用自然語言描述行為。

## BDD 的核心概念

BDD 使用 Gherkin 語法描述行為：

```gherkin
Feature: 使用者登入
  Scenario: 使用正確帳密登入
    Given 我在登入頁面
    When 我輸入 "user@example.com" 和 "password123"
    Then 我應該看到歡迎訊息
    And 我應該登入成功
```

## Python BDD 實作：behave

```python
# features/steps/login_steps.py
from behave import given, when, then

@given('我在登入頁面')
def step_on_login_page(context):
    context.page = LoginPage()

@when('我輸入 "{email}" 和 "{password}"')
def step_enter_credentials(context, email, password):
    context.page.login(email, password)

@then('我應該看到歡迎訊息')
def step_see_welcome(context):
    assert context.page.has_welcome_message()

@then('我應該登入成功')
def step_login_success(context):
    assert context.page.is_logged_in()
```

```gherkin
# features/login.feature
Feature: 使用者登入功能

  Scenario: 有效憑證登入
    Given 我在登入頁面
    When 我輸入 "user@example.com" 和 "correct_password"
    Then 我應該看到歡迎訊息
    And 我應該登入成功

  Scenario: 無效憑證登入
    Given 我在登入頁面
    When 我輸入 "user@example.com" 和 "wrong_password"
    Then 我應該看到錯誤訊息
    And 我不應該登入成功
```

## JavaScript BDD 實作：Cucumber + Protractor

```javascript
// features/login.feature
Feature: Login Feature
  Scenario: Valid login
    Given I am on the login page
    When I fill in "email" with "user@example.com"
    And I fill in "password" with "password123"
    And I press "Login"
    Then I should see "Welcome"
    And I should be logged in
```

```javascript
// step_definitions/login_steps.js
const { Given, When, Then } = require('cucumber');

Given('I am on the login page', function() {
  return this.page.navigateToLogin();
});

When('I fill in {string} with {string}', function(field, value) {
  return this.page.fillField(field, value);
});

When('I press {string}', function(button) {
  return this.page.pressButton(button);
});

Then('I should see {string}', function(message) {
  return this.page.assertTextPresent(message);
});
```

## BDD vs TDD

| 面向 | TDD | BDD |
|------|-----|-----|
| 目標 | 技術正確性 | 業務行為 |
| 語法 | 程式碼 | 自然語言 |
| 受眾 | 開發者 | 開發者 + 產品 + QA |
| 工具 | JUnit, pytest | Cucumber, Behave |

## BDD 的價值

1. **跨團隊溝通**：非技術人員也能理解規格
2. **文件即測試**：規格文件不會過時
3. **驗收測試**：直接對應使用者故事

## 相關資源

- [Cucumber BDD 官網](https://www.google.com/search?q=cucumber+BDD+behavior+driven+development)
- [Behave Python BDD](https://www.google.com/search?q=behave+python+BDD+tutorial)
- [Gherkin 語法參考](https://www.google.com/search?q=gherkin+language+reference)

## 結語

BDD 將測試從技術層面提升到業務層面，讓整個團隊都能用共同語言討論系統行為。

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*