# BDD 與行為驅動開發：從測試到規格

## BDD 的起源

### 從 TDD 到 BDD

2003 年，Dave Astels 在文章「又一個 TDD 文章？」中提出了一個觀點：TDD 應該是關於設計和規範，而不是關於測試。這是 BDD（Behavior-Driven Development）運動的開始。

```
TDD 的問題：

1. 「測試」這個詞有誤導性
   - TDD 不是為了「測試」程式
   - 而是为了「規範」行為

2. 術語不一致
   - test_xxx vs should_xxx
   - 開發者之間沒有共同語言

3. 業務人員無法理解
   - unit test 是給開發者看的
   - 業務人員需要不同的視角
```

### Dan North 與 JBehave

2004 年，Dan North 創建了 JBehave，這是第一個專門的 BDD 框架。他確定了 BDD 的核心語法和術語。

```
BDD 關注點：

1. 行為而非測試
   - 「這個系統的行為是什麼？」
   - 而非「這個類別通過測試了嗎？」

2. 通用語言
   - 開發者、測試者、業務人員都能理解
   - 使用領域術語（Ubiquitous Language）

3. 實例化需求
   - 用具體例子說明抽象需求
   - 「例如：當用戶登入時密碼錯誤，顯示錯誤訊息」
```

## BDD 的核心概念

### Given-When-Then 語法

```gherkin
Feature: 用戶登入

  Scenario: 成功登入
    Given 用戶在登入頁面
    And 用戶輸入正確的帳號 "admin"
    And 用戶輸入正確的密碼 "password"
    When 用戶點擊登入按鈕
    Then 用戶應該看到歡迎訊息
    And 用戶應該進入管理後台

  Scenario: 密碼錯誤
    Given 用戶在登入頁面
    And 用戶輸入帳號 "admin"
    And 用戶輸入錯誤的密碼 "wrong"
    When 用戶點擊登入按鈕
    Then 用戶應該看到錯誤訊息 "密碼錯誤"
    And 用戶應該仍在登入頁面
```

### 語法解釋

```
Given（前提條件）：
- 描述系統的初始狀態
- 「在什麼情況下」

When（操作）：
- 描述觸發的行為
- 「做什麼」

Then（預期結果）：
- 描述預期的行為結果
- 「預期什麼」
```

## BDD 工具生態

### 主要工具

```markdown
BDD 工具生態（2009年）：

Ruby 生態：
- RSpec - Ruby 測試框架
- Cucumber - Gherkin 解析器
- Steak - Ruby 的 Cucumber 替代

Java 生態：
- JBehave - Java BDD 框架
- Concordion - 規格化測試

Python 生態：
- Behave - Gherkin 解析器
- Lettuce - Python BDD
- freshen - Python 的 BDD

JavaScript 生態：
- Jasmine - JavaScript BDD 框架
- Mocha - 靈活的測試框架
- Cucumber.js - JavaScript Gherkin

其他：
- NBehave (.NET)
- SpecFlow (.NET)
- Behat (PHP)
```

## Cucumber 與 Gherkin

### Gherkin 語法

```gherkin
# Gherkin 是 Cucumber 使用的領域特定語言

Feature: 購物車功能

  Scenario: 添加商品到購物車
    Given 用戶瀏覽商品頁面
    And 商品 "iPhone" 價格為 20000 元
    When 用戶點擊「加入購物車」
    Then 購物車應顯示 1 件商品
    And 購物車總金額為 20000 元

  Scenario: 修改數量
    Given 用戶購物車中有 1 件 "iPhone"
    When 用戶將數量改為 3
    Then 購物車總金額為 60000 元

  Scenario Outline: 計算折扣
    Given 商品價格為 <price> 元
    And 購買數量為 <quantity>
    When 套用 <discount>% 折扣
    Then 總金額應為 <total> 元

    Examples:
      | price | quantity | discount | total |
      | 1000  | 2        | 0        | 2000  |
      | 1000  | 2        | 10       | 1800  |
      | 1000  | 2        | 50       | 1000  |
```

### Step Definitions

```ruby
# Ruby + Cucumber
Given("用戶瀏覽商品頁面") do
  visit products_path
end

Given("商品 {string} 價格為 {int} 元") do |name, price|
  @product = Product.create!(name: name, price: price)
end

When("用戶點擊「加入購物車」") do
  click_button "加入購物車"
end

Then("購物車應顯示 {int} 件商品") do |count|
  expect(page).to have_content("#{count} 件商品")
end
```

```python
# Python + Behave
@given('用戶瀏覽商品頁面')
def step_impl(context):
    context.browser.get('/products')

@given('商品 "{name}" 價格為 {price} 元')
def step_impl(context, name, price):
    Product.objects.create(name=name, price=price)

@when('用戶點擊「加入購物車」')
def step_impl(context):
    context.browser.find_element_by_id('add-to-cart').click()

@then('購物車應顯示 {count} 件商品')
def step_impl(context, count):
    assert context.browser.find_element_by_id('cart-count').text == count
```

## BDD 的價值

### 從不同角度看待軟體

```
傳統 TDD：
┌──────────────────────────────────┐
│ class UserService               │
│   def authenticate(...)         │
│     # 驗證使用者                 │
│   end                           │
│                                 │
│   def test_authenticate         │
│     # 測試方法                   │
│   end                           │
└──────────────────────────────────┘

BDD：
┌──────────────────────────────────┐
│ Feature: 用戶認證               │
│   Scenario: 正確密碼             │
│     Given 用戶在登入頁面         │
│     When 輸入正確密碼            │
│     Then 登入成功                │
└──────────────────────────────────┘
```

### 橋接技術與業務

```markdown
BDD 的價值：

1. 通用語言
   - 業務人員可以讀懂規格
   - 開發者可以驗證實作

2. 實例化需求
   - 抽象需求具體化
   - 減少誤解

3. 文件即測試
   - Gherkin 文件永遠最新
   - 測試失敗時文件過時

4. 持續對話
   - 促進團隊溝通
   - 共同的驗收標準
```

## BDD 與 TDD 的關係

### 兩者互補

```python
# BDD（驗收測試）- 高層次
Feature: 用戶管理
  Scenario: 建立新用戶
    Given 管理員登入系統
    When 點擊「建立用戶」
    Then 用戶建立成功

# TDD（單元測試）- 低層次
def test_user_creation_with_valid_data():
    user = User.create(name="John", email="john@example.com")
    assert user.id is not None
    assert user.name == "John"
```

### 測試策略

```
測試策略金字塔：

        ▲
       /│\         BDD - 驗收測試
      / │ \        （少量，跨系統）
     /  │  \
    /───┼───\     整合測試
   /    │    \    （適量）
  /─────┼─────\   單元測試 + TDD
 /      │      \  （大量）
────────┴────────
```

## 結語

BDD 將 TDD 的原則推廣到了更廣的範圍。不僅是開發者在撰寫測試，連業務人員也參與了規格的定義。

下一篇文章將介紹 RSpec 與 Ruby 測試生態，這是 BDD 在 Ruby 世界的實作。

---

## 延伸閱讀

- [BDD 起源與概念](https://www.google.com/search?q=BDD+behavior+driven+development+origin)
- [Cucumber 文件](https://www.google.com/search?q=Cucumber+Gherkin+documentation)
- [RSpec BDD 框架](https://www.google.com/search?q=RSpec+Ruby+BDD+framework)
- [Given-When-Then 語法](https://www.google.com/search?q=Given-When-Then+BDD+syntax)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」焦點系列之一。*