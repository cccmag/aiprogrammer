# Ruby 1.9.1 發布：YARV 虛擬機與效能提升

## 前言

2009 年 1 月，Ruby 1.9.1 正式發布，這是 Ruby 1.9 系列的第一個穩定版本。Ruby 1.9 採用了全新的 YARV 虛擬機，帶來了 2-5 倍的效能提升。

## YARV 的由來

### 為什麼需要虛擬機？

Ruby 1.8 的直譯器使用樹狀語法樹（ParseTree）直接解釋執行，這種方式雖然簡單，但執行效率較低。

```
Ruby 直譯器演進：

Ruby 1.8：
原始碼 → 語法樹 → 直譯執行
（慢，簡單）

Ruby 1.9：
原始碼 → 位元組碼 → YARV 虛擬機執行
（快，複雜）
```

### YARV 的作者

YARV（Yet Another Ruby Virtualmachine）由 SASADA Koichi 於 2004 年開始開發，2007 年被合併入 Ruby 主線。

## Ruby 1.9.1 的效能提升

### 效能對比

```ruby
# 效能測試：計算 Fibonacci 數列

def fib(n)
  n < 2 ? n : fib(n-1) + fib(n-2)
end

# Ruby 1.8.6：26.5 秒
# Ruby 1.9.1：4.8 秒
# 提升：5.5 倍
```

| 測試項目 | Ruby 1.8 | Ruby 1.9 | 提升 |
|---------|---------|---------|------|
| fib(35) | 26.5s | 4.8s | 5.5x |
| 100k 迴圈 | 12.3s | 2.1s | 5.9x |
| String 操作 | 8.2s | 3.4s | 2.4x |
| Regex | 5.6s | 1.9s | 2.9x |

### 位元組碼展示

```ruby
# Ruby 原始碼
def hello
  puts "Hello, World!"
end

# YARV 位元組碼
=>
== disasm: <RubyVM::InstructionSequence:hello@-> <compiled>=====
0000 trace            1
0002 putsstring       "Hello, World!"
0004 putself
0006 send             :puts, 1
0009 trace            1
0011 leave
```

## 字串編碼

### Ruby 1.9 的編碼改進

```ruby
# Ruby 1.8：編碼地獄
str = "中文"
str.length  # => 6（位元組數）

# Ruby 1.9：正規支援
str = "中文"
str.length     # => 2（字元數）
str.encoding   # => #<Encoding:UTF-8>

# 強制指定編碼
str = "中文".force_encoding("GBK")
str.length  # => 4（GBK 位元組數）
```

### 編碼轉換

```ruby
# 字串編碼
str = "hello"
str.encoding  # => #<Encoding:UTF-8>

# 轉換編碼
str.encode("ASCII")  # => "hello"

# 無理截斷
str = "abc"
str.encode("UTF-16BE")  # => "\x00a\x00b\x00c"
```

## Ruby 1.9 的其他改進

### 區塊語法

```ruby
# Lambda 語法改進
# Ruby 1.8
l = lambda { |x| x * 2 }
l.call(5)  # => 10

# Ruby 1.9
l = ->(x) { x * 2 }
l.(5)  # => 10（可以用 .() 調用）
```

### 符號Proc

```ruby
# Ruby 1.9 的 Symbol#to_proc
[1, 2, 3, 4, 5].map(&:to_s)  # => ["1", "2", "3", "4", "5"]

# 等價於
[1, 2, 3, 4, 5].map { |n| n.to_s }
```

### 雜湊增強

```ruby
# Ruby 1.9 允許 hash 作為方法參數
def method(a:, b:, c:)
  puts a, b, c
end

method(a: 1, b: 2, c: 3)
```

## 遷移考量

### 破壞性改變

```ruby
# 1. Object#inspect 改變
# Ruby 1.8: :symbol
# Ruby 1.9: :symbol（保持）

# 2. String#== 行為
# Ruby 1.8: "string" == :string（永遠 false）
# Ruby 1.9: 嚴格類型檢查

# 3. 區塊返回值
# Ruby 1.8: 最後一行
# Ruby 1.9: 最後一行（不變）
```

### 相容性策略

```ruby
# 檢查 Ruby 版本
RUBY_VERSION  # => "1.9.1"

# 條件執行
if RUBY_VERSION >= "1.9"
  # Ruby 1.9+ 代碼
else
  # Ruby 1.8 代碼
end
```

## Rails 3.0 與 Ruby 1.9

Rails 3.0 於 2010 年發布，全面支援 Ruby 1.9。

```bash
# Rails 3.0 需求
ruby >= 1.8.7
（推薦 1.9.2+）
```

## 結語

Ruby 1.9.1 的發布標誌著 Ruby 語言進入了新的時代。YARV 虛擬機帶來的效能提升為 Rails 3.0 和更大的應用奠定了基礎。

## 延伸閱讀

- [Ruby 1.9.1 發布公告](https://www.google.com/search?q=Ruby+1.9.1+release)
- [YARV 虛擬機](https://www.google.com/search?q=YARV+Ruby+virtual+machine)
- [Ruby 1.9 效能測試](https://www.google.com/search?q=Ruby+1.9+performance+benchmark)
- [Ruby 1.9 遷移指南](https://www.google.com/search?q=Ruby+1.9+migration+guide)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」文章系列之一。*