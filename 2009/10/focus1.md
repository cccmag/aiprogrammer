# Ruby 1.9 與 YARV 虛擬機：效能飛躍

## YARV 的由來

### 為什麼需要虛擬機？

Ruby 1.8 的直譯器使用簡單的 tree-walking 解釋器，執行效率較低。YARV（Yet Another Ruby VM）由 SASADA Koichi 開發，提供了位元組碼和虛擬機。

```ruby
# Ruby 1.8：直接解釋
# Ruby 1.9：編譯為 YARV 位元組碼
```

## Ruby 1.9 的效能提升

```ruby
# 效能測試
def fib(n)
  n < 2 ? n : fib(n-1) + fib(n-2)
end

# Ruby 1.8.6: ~26 秒
# Ruby 1.9.1: ~5 秒
# 提升: 5x+
```

| 操作 | Ruby 1.8 | Ruby 1.9 | 提升 |
|------|----------|----------|------|
| 方法調用 | 100% | 200% | 2x |
| 區塊執行 | 100% | 300% | 3x |
| 字串操作 | 100% | 250% | 2.5x |

## 位元組碼展示

```ruby
# 查看 YARV 位元組碼
require 'pp'
pp RubyVM::InstructionSequence.compile(<<-CODE).disasm
def hello
  puts "Hello, World!"
end
CODE

# 輸出：
# == disasm: <RubyVM::InstructionSequence:hello@-> <compiled>
# 0000 trace            1
# 0002 putsstring       "Hello, World!"
# 0004 putself
# 0006 send             :puts, 1
# 0009 trace            1
# 0011 leave
```

## 字串編碼

```ruby
# Ruby 1.9 的編碼改進
str = "中文"
str.length     # => 2（字元數）
str.encoding   # => #<Encoding:UTF-8>

# 強制指定編碼
str = "中文".force_encoding("GBK")
str.length  # => 4
```

## 結語

Ruby 1.9 的 YARV 虛擬機讓 Ruby 從「優雅但緩慢」變成了「優雅且高效」。

---

*本篇文章為「AI 程式人雜誌 2009 年 10 月號」焦點系列之一。*