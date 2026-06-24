# Rubygems 與依賴管理：Bundler 的誕生

## Rubygems 的問題

### 依賴地獄

```ruby
# Ruby 專案的依賴問題

# 專案 A 需要 gem X >= 1.0
# 專案 B 需要 gem X < 1.0
# 系統同時安裝會衝突
```

## Bundler 的解決方案

```ruby
# Gemfile - Bundler 的依賴宣告

source :gemcutter
source :rubyforge

gem "rails", "2.3.5"
gem "nokogiri"
gem "jquery-rails"
```

```bash
# 安裝所有依賴
bundle install

# 鎖定版本
bundle lock
```

## Bundler 的功能

### 依賴解析

```ruby
# Bundler 自動解決依賴衝突
# 找到所有 gem 的兼容版本組合
```

## 結語

Bundler 解決了 Ruby 長期以來的依賴管理問題。

---

*本篇文章為「AI 程式人雜誌 2009 年 10 月號」焦點系列之一。*