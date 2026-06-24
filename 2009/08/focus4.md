# RSpec 與 Ruby 測試生態：DSL 測試框架

## RSpec 的起源

### 為什麼需要 RSpec？

Ruby 社群在 2006 年創建了 RSpec，作為 Test::Unit 的替代品。RSpec 採用了 DSL（領域特定語言）設計，讓測試更具可讀性。

```ruby
# Test::Unit 風格
class UserTest < Test::Unit::TestCase
  def test_user_creation
    user = User.create(name: "John", email: "john@example.com")
    assert_equal "John", user.name
    assert user.persisted?
  end
end

# RSpec 風格
describe User do
  describe "#create" do
    it "creates a new user with valid attributes" do
      user = User.create(name: "John", email: "john@example.com")
      user.name.should == "John"
      user.should be_persisted
    end
  end
end
```

### RSpec 的設計理念

```
RSpec 設計原則：

1. 可讀性優先
   - 測試應該像文件一樣可讀
   - 使用自然語言語法

2. 描述行為，而非驗證
   - "describe" 類別或方法
   - "it" 說明預期行為
   - "expect" 表達預期結果

3. 豐富的回報
   - 清晰的失敗訊息
   - 語法高亮
   - 程式碼位置
```

## RSpec 基本語法

### 核心概念

```ruby
# describe - 建立測試群組
describe User do
  # 可以巢狀
  describe ".authenticate" do
    describe "with valid credentials" do
      it "returns the user" do
        user = User.create(email: "test@example.com", password: "secret")
        found = User.authenticate("test@example.com", "secret")
        found.should == user
      end
    end

    describe "with invalid password" do
      it "returns nil" do
        User.create(email: "test@example.com", password: "secret")
        found = User.authenticate("test@example.com", "wrong")
        found.should be_nil
      end
    end
  end
end
```

### 斷言（Matchers）

```ruby
# 相等性
expect(actual).to eq(expected)
expect(actual).to eql(expected)  # 更嚴格
expect(actual).to equal(expected) # 同一物件

# 真假值
expect(actual).to be_true
expect(actual).to be_false
expect(actual).to be_nil
expect(actual).to be_truthy
expect(actual).to be_falsy

# 包含
expect(array).to include(item)
expect(string).to include(substring)
expect(hash).to include(key: value)

# 類型
expect(object).to be_a(String)
expect(object).to be_an_instance_of(String)

# 抛出異常
expect { do_something }.to raise_error(ErrorClass)
expect { do_something }.to raise_error("message")
```

### Hooks

```ruby
describe User do
  # 在所有測試前執行一次
  before(:all) do
    @user = User.create(name: "Test")
  end

  # 每個測試前執行
  before(:each) do
    @user = User.new
  end

  # 每個測試後執行
  after(:each) do
    User.delete_all
  end

  # 所有測試後執行一次
  after(:all) do
    User.delete_all
  end

  # 共享範例
  shared_examples "valid user" do
    it "has a name" do
      expect(@user).to have_name
    end
  end
end
```

## Rails 測試策略

### Rails 测试类型

```ruby
# 1. 單元測試 - Model
describe User do
  describe "#valid?" do
    it "requires email" do
      user = User.new(password: "secret")
      user.should_not be_valid
    end
  end
end

# 2. 請求測試 - Controller
describe UsersController do
  describe "GET #index" do
    it "returns all users" do
      get :index
      assigns(:users).should =~ User.all
    end
  end
end

# 3. 視圖測試 - View
describe "users/index.html.erb" do
  it "displays all users" do
    assign(:users, [User.create(name: "John")])
    render
    rendered.should contain("John")
  end
end

# 4. 整合測試 - Full stack
describe "User workflow" do
  it "creates and displays a user" do
    visit new_user_path
    fill_in "Name", with: "John"
    click_button "Create"
    page.should have_content("John")
  end
end
```

### Factory Girl

```ruby
# 定義工廠
FactoryGirl.define do
  factory :user do
    sequence(:email) { |n| "user#{n}@example.com" }
    name "John Doe"
    password "secret"

    factory :admin do
      role "admin"
    end
  end

  factory :post do
    title "Sample Post"
    body "Post content"
    association :user  # 自動關聯
  end
end

# 使用工廠
describe Post do
  it "creates a valid post" do
    post = FactoryGirl.create(:post, title: "My Post")
    post.user.should be_present
  end
end
```

## 其他 Ruby 測試工具

### Shoulda

```ruby
# Shoulda - 更簡潔的語法
context "User" do
  should_require_attributes :name, :email
  should_protect_attributes :password
  should_have_many :posts
  should_have_one :profile
  should_have_many :comments
  should_validate_uniqueness_of :email
end
```

### Mocha

```ruby
# Mocha - Mock 框架
require 'mocha/setup'

describe User do
  it "sends welcome email" do
    user = User.new(email: "test@example.com")
    Notifier.expects(:deliver_welcome).with(user)

    user.save
  end

  it "fetches from API" do
    User.expects(:fetch_from_api).with("123").returns(mock_user)

    result = User.find_or_fetch("123")

    result.should == mock_user
  end
end
```

### Steak

```ruby
# Steak - Ruby 的 BDD（類似 Cucumber）
feature "User management" do
  scenario "creates a new user" do
    visit new_user_path

    fill_in "Email", with: "new@example.com"
    fill_in "Name", with: "New User"
    click_button "Create"

    page.should have_content("User created")
  end
end
```

## RSpec 與 Mock

### Stubs

```ruby
describe Order do
  it "calculates total with discount" do
    order = Order.new
    order.stub!(discount_rate: 0.1)

    result = order.calculate_total(100)

    result.should == 90
  end
end

# RSpec 3 語法
it "calculates total with discount" do
  order = Order.new
  allow(order).to receive(:discount_rate).and_return(0.1)

  result = order.calculate_total(100)

  expect(result).to eq(90)
end
```

### Mocks

```ruby
describe OrderProcessor do
  it "processes order and sends email" do
    order = double("order")
    mailer = double("mailer")

    allow(order).to receive_messages(
      total: 100,
      customer_email: "customer@example.com"
    )
    allow(mailer).to receive(:deliver)

    processor = OrderProcessor.new(mailer)
    processor.process(order)

    expect(mailer).to have_received(:deliver)
      .with("customer@example.com", order.total)
  end
end
```

## RSpec 配置

```ruby
# spec_helper.rb
RSpec.configure do |config|
  # 包含路徑
  config.include Capybara::DSL, type: :feature

  # 使用 Factory Girl
  config.include FactoryGirl::Syntax::Methods

  # 自訂 Matchers
  config.after(:each) do
    User.delete_all if User.table_exists?
  end
end

# .rspec 檔案
--color
--format documentation
--drb
```

## 結語

RSpec 開創了 Ruby 測試的 DSL 風格，讓測試變得更加可讀和自然。2009 年，RSpec 已經成為 Ruby 社群最重要的測試框架。

下一篇文章將介紹 Cucumber，這是更廣泛的 BDD 工具，可以讓非開發者也參與規格定義。

---

## 延伸閱讀

- [RSpec 官方網站](https://www.google.com/search?q=RSpec+Ruby+testing+framework)
- [RSpec 文件](https://www.google.com/search?q=RSpec+documentation)
- [Factory Girl 文件](https://www.google.com/search?q=Factory+Girl+Ruby)
- [Ruby 測試最佳化](https://www.google.com/search?q=Ruby+testing+best+practices)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」焦點系列之一。*