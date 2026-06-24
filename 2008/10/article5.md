# ActiveSupport 與核心擴展

## 1. 核心擴展

```ruby
require 'active_support/core_ext'

# String 擴展
"hello".titleize           # => "Hello"
"hello_world".camelize    # => "HelloWorld"
"HelloWorld".underscore   # => "hello_world"

# Array 擴展
[1, 2, 3].to_sentence     # => "1, 2, and 3"
[1, 2, 3].in_groups_of(2) # => [[1, 2], [3, nil]]
```

## 2. 時間擴展

```ruby
# 方便的时间操作
Time.now + 1.hour
Date.today + 1.week
1.month.from_now
3.days.ago

# 工作日計算
date = 5.business_days.from_now
```

## 3. Hash 擴展

```ruby
# Deep merge
h1 = { a: { b: 1 } }
h2 = { a: { c: 2 } }
h1.deep_merge(h2)  # => { a: { b: 1, c: 2 } }

# 切片
{ a: 1, b: 2, c: 3 }.slice(:a, :b)  # => { a: 1, b: 2 }
```

## 4. Object 擴展

```ruby
# try 方法
@user.try(:name)  # 避免 nil.name 錯誤

# 屬性查詢
obj.instance_values  # 雜湊形式取得執行個體變數
```

## 5. 類別擴展

```ruby
# Cattr（類別屬性）
class Config
  cattr_accessor :site_name
  self.site_name = "My Site"
end

Config.site_name  # => "My Site"
```

## 6. Integer 擴展

```ruby
5.times { print "Hello " }
10.upto(15).each { |n| print n }
(1..10).step(2).each { |n| print n }
```

---

**參考資料**
- [ActiveSupport Core Extensions](https://www.google.com/search?q=ActiveSupport+core+extensions+Rails)
- [Rails Extensions](https://www.google.com/search?q=Rails+String+Hash+extensions)
- [ActiveSupport Documentation](https://www.google.com/search?q=ActiveSupport+documentation+2008)