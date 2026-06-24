# Ruby 生態：Rails 3.0 開發、Ruby 1.9

## Ruby 1.9.1 效能飛躍

### YARV 虛擬機

```ruby
# Ruby 1.9 vs 1.8 效能

def fib(n)
  n < 2 ? n : fib(n-1) + fib(n-2)
end

# Ruby 1.8.6: ~26 秒
# Ruby 1.9.1: ~5 秒
# 提升：5x+
```

## Rails 3.0 開發

### 主要改進

```ruby
# Rails 3.0（開發中）

# 1. Merb 合併
# - 模組化設計
# - 更好的效能

# 2. 統一的查詢介面
User.where(:name => "張三").limit(10)

# 3. 更好的 JavaScript 整合
# - Unobtrusive JavaScript
# - jQuery 支援

# 4. 安全性改進
# - 更好的 XSS 防護
# - CSRF 保護
```

## Bundler

### 依賴管理

```ruby
# Gemfile（Bundler 0.9）

source :gemcutter
source :rubyforge

gem "rails", "2.3.5"
gem "nokogiri"
gem "jquery-rails"

# 安裝
bundle install
bundle lock
```

## RSpec 2.0

### 新功能

```ruby
# RSpec 2.0

describe User do
  describe "#create" do
    context "with valid attributes" do
      it "creates a new user" do
        expect {
          User.create(name: "張三")
        }.to change(User, :count).by(1)
      end
    end
  end
end
```

## 結語

Ruby 生態在 2009 年繼續繁榮，Rails 3.0 和 Ruby 1.9 的發展為未來打下了基礎。

---

*本篇文章為「AI 程式人雜誌 2009 年 12 月號」焦點系列之一。*