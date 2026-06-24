# Cucumber 與 Gherkin：驗收測試

## Cucumber 的起源

### 為什麼需要 Cucumber？

Cucumber 由Aslak Hellesøy 於 2008 年創建，目標是讓非開發者也能理解和撰寫測試規格。

```
Cucumber 的設計目標：

1. 可讀性
   - 非開發者也能理解
   - 使用自然語言

2. 協作
   - 業務人員參與規格定義
   - 團隊共同擁有測試

3. 自動化
   - 所有規格都是可執行的
   - 消除文件和測試的脫節
```

## Gherkin 語法

### 基本結構

```gherkin
Feature: 用戶管理

  As an administrator
  I want to manage users
  So that I can control system access

  Background:
    Given a logged in admin
    And the following users exist:
      | name  | email             | role    |
      | John  | john@example.com  | member  |
      | Jane  | jane@example.com  | member  |

  Scenario: View user list
    When I navigate to the user management page
    Then I should see "John"
    And I should see "Jane"
    And I should see 2 users total

  @admin
  Scenario: Delete a user
    Given I am on the user management page
    When I click the delete button for "John"
    Then I should see a confirmation dialog
    When I confirm the deletion
    Then I should see "User deleted"
    And "John" should not be in the user list
```

### 關鍵字

```
Gherkin 關鍵字：

Feature - 功能
Background - 背景（每個 Scenario 前執行）
Scenario - 場景
Scenario Outline - 場景大綱（表格驅動）
  Examples - 範例表格

Given - 前提條件
When - 操作
Then - 預期結果
And - 擴展前一步
But - 擴展前一步（對比語氣）

@tag - 標籤
```

## Step Definitions

### Ruby 實現

```ruby
# features/step_definitions/user_steps.rb

Given("a logged in admin") do
  @admin = FactoryGirl.create(:admin)
  visit new_user_session_path
  fill_in "Email", with: @admin.email
  fill_in "Password", with: @admin.password
  click_button "Sign in"
end

Given("the following users exist:") do |table|
  table.hashes.each do |row|
    User.create!(
      name: row["name"],
      email: row["email"],
      role: row["role"]
    )
  end
end

When("I navigate to the user management page") do
  click_link "User Management"
end

When("I click the delete button for {string}") do |name|
  user = User.find_by_name(name)
  click_link "delete-user-#{user.id}"
end

Then("I should see {string}") do |text|
  expect(page).to have_content(text)
end

Then("I should see {int} users total") do |count|
  expect(page).to have_css(".user-row", count: count)
end

Then(/^"([^"]*)" should not be in the user list$/) do |name|
  expect(page).to_not have_content(name)
end
```

### Python 實現

```python
# features/steps/user_steps.py
from behave import given, when, then

@given('a logged in admin')
def step_impl(context):
    context.admin = UserFactory.create_admin()
    context.browser.visit('/login')
    context.browser.fill('email', context.admin.email)
    context.browser.fill('password', 'password')
    context.browser.click_button('Sign in')

@given('the following users exist:')
def step_impl(context):
    for row in context.table:
        User.objects.create(
            name=row['name'],
            email=row['email'],
            role=row['role']
        )

@when('I navigate to the user management page')
def step_impl(context):
    context.browser.click_link('User Management')

@then('I should see "{text}"')
def step_impl(context, text):
    assert text in context.browser.content
```

## 表格式資料

### Scenario Outline

```gherkin
Feature: 計算折扣

  Scenario Outline: 不同折扣率計算
    Given 商品價格為 <price> 元
    And 會員等级為 <level>
    When 計算折扣
    Then 最終價格為 <result> 元

    Examples:
      | price | level   | result |
      | 1000  | regular | 1000   |
      | 1000  | silver  | 900    |
      | 1000  | gold    | 800    |
      | 2000  | regular | 2000   |
      | 2000  | gold    | 1400   |
```

### 表格轉換

```ruby
# 轉換為 Cucumber::Ast::Table
Given("the following users exist:") do |table|
  # table 是一个 Table 物件
  table.hashes.each do |row|
    User.create!(
      name: row['name'],
      email: row['email'],
      role: row['role']
    )
  end
end

# 也可以轉換為 SymbolizedHash
Given("the following users exist:") do |table|
  table.raw.each_with_index do |row, index|
    next if index == 0  # 跳過表頭
    User.create!(
      name: row[0],
      email: row[1],
      role: row[2]
    )
  end
end
```

## 標籤（Tags）

### 使用標籤組織測試

```gherkin
@smoke
Feature: 登入功能

  @smoke @login
  Scenario: 成功登入
    Given 用戶在登入頁面
    ...

  @slow
  Scenario: 處理大量資料
    ...

  @admin @security
  Scenario: 管理員權限
    ...
```

### 執行特定標籤

```bash
# 只執行 @smoke 標籤
cucumber --tags @smoke

# 執行多個標籤（OR）
cucumber --tags '@smoke,@regression'

# 排除標籤
cucumber --tags 'not @slow'

# 組合
cucumber --tags '@smoke and @login'
```

## 與 RSpec 整合

### 混合使用

```ruby
# features/step_definitions/web_steps.rb
# 引入 RSpec Matchers
Then /^I should see "(.*)"$/ do |text|
  page.should have_content(text)
end

Then /^I should see an? (.+) element$/ do |selector|
  page.should have_selector(selector)
end

# 在 Step 中使用 RSpec
Then("the user should exist") do
  User.find_by_email(@email).should be_present
end
```

### 共享步驟

```gherkin
# features/shared_steps/user_steps.rb
Given /^a user with email "([^"]*)" exists$/ do |email|
  @user = User.create!(email: email, password: "password")
end

# 在其他 Feature 中使用
Feature: Password Reset
  Scenario: Reset password
    Given a user with email "test@example.com" exists
    When I request a password reset
    ...
```

## 生態系統

### Cucumber 的多語言實現

```markdown
Cucumber 家族：

1. Cucumber (Ruby)
   - 原始實現
   - 最成熟

2. Cucumber-JVM (Java)
   - Java/JVM 版本
   - 支援 Java、Groovy、Scala

3. Cucumber.js (JavaScript)
   - Node.js 版本
   - Web 測試

4. Behave (Python)
   - Python 實現
   - 類似語法

5. Lettuce (Python)
   - 另一個 Python 實現

6. NBehave (.NET)
   - .NET 版本

7. Cucumber-eclipse (Eclipse)
   - IDE 整合
```

## 最佳實踐

### 組織 Feature 檔案

```bash
features/
├── support/
│   ├── env.rb           # 環境設定
│   ├── hooks.rb         # 生命週期鉤子
│   └── world.rb         # 自訂 World 物件
├── step_definitions/
│   ├── user_steps.rb
│   ├── order_steps.rb
│   └── common_steps.rb
├── pages/               # Page Object 模式
│   ├── login_page.rb
│   └── dashboard_page.rb
└── user_management/
    ├── login.feature
    ├── user_crud.feature
    └── permissions.feature
```

### Page Object 模式

```ruby
# features/pages/login_page.rb
class LoginPage
  include Capybara::DSL

  def visit_login_page
    visit "/login"
  end

  def login_as(email, password)
    fill_in "Email", with: email
    fill_in "Password", with: password
    click_button "Sign in"
  end

  def should_show_error(message)
    expect(page).to have_content(message)
  end
end

# step definitions
Given("I am on the login page") do
  LoginPage.new.visit_login_page
end

When("I login with valid credentials") do
  LoginPage.new.login_as("test@example.com", "password")
end
```

## 結語

Cucumber 將 BDD 的理念帶向了更廣的範圍，讓整個團隊都能參與軟體規格的定義和驗證。

下一篇文章將介紹持續整合與測試覆蓋率，這是將測試實踐規模化的關鍵。

---

## 延伸閱讀

- [Cucumber 官方網站](https://www.google.com/search?q=Cucumber+BDD+framework)
- [Gherkin 語法](https://www.google.com/search?q=Gherkin+syntax+reference)
- [Cucumber Ruby 文件](https://www.google.com/search?q=Cucumber+Ruby+tutorial)
- [Cucumber 最佳化](https://www.google.com/search?q=Cucumber+best+practices)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」焦點系列之一。*