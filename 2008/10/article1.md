# Ruby 語法基礎與特性

## 1. 動態型別系統

Ruby 是強型別的動態語言，變數型別在執行時決定。

```ruby
x = 42
x = "字串"  # 完全合法，Ruby 變數沒有固定型別

# 給變數加型別註釋（Ruby 3.0+）
x: Integer = 42
```

## 2. 區塊與迭代器

```ruby
# each 迭代
[1, 2, 3].each { |n| puts n }

# map 轉換
squares = [1, 2, 3].map { |n| n * n }  # [1, 4, 9]

# select 過濾
evens = (1..10).select { |n| n.even? }  # [2, 4, 6, 8, 10]

# inject 累計
sum = [1, 2, 3].inject(0) { |acc, n| acc + n }  # 6
```

## 3. 符號（Symbols）

```ruby
# 符號是不可變的識別子，效能優於字串
:hello            # 符號
"hello".to_sym    # 字串轉符號
:hello.to_s       # 符號轉字串

# 雜湊使用符號鍵
user = { name: "小明", age: 25 }
user[:name]       # => "小明"
```

## 4. 類別與模組

```ruby
module Greeting
  def hello
    "你好，#{@name}！"
  end
end

class Person
  include Greeting

  attr_accessor :name, :age

  def initialize(name, age)
    @name = name
    @age = age
  end

  def inspect
    "#<Person #{@name} (#{@age})>"
  end
end
```

## 5. 方法存取控制

```ruby
class BankAccount
  def initialize(balance)
    @balance = balance
  end

  def balance      # 公開讀取
    @balance
  end

  private

  def deduct(fee)  # 私有方法
    @balance -= fee
  end
end
```

---

**參考資料**
- [Ruby Language Basics](https://www.google.com/search?q=Ruby+syntax+basics+blocks+iterators)
- [Ruby Symbols vs Strings](https://www.google.com/search?q=Ruby+symbols+vs+strings+performance)
- [Ruby Classes and Modules](https://www.google.com/search?q=Ruby+class+module+inheritance)