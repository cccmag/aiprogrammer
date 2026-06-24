# Ruby 1.9 新功能與效能改進（2008）

## YARV：全新的虛擬機

### 前言

Ruby 1.9 最大的變革是引入了 YARV（Yet Another Ruby Virtualmachine）。不同於 1.8 的直譯器執行方式，YARV 將 Ruby 程式碼編譯為位元組碼再執行。

### 位元組碼執行範例

```ruby
# Ruby 1.8：直譯器逐步執行
# Ruby 1.9：編譯為 YARV 位元組碼

# 查看 YARV 位元組碼
require 'disasm'
puts RubyVM::InstructionSequence.disasm(lambda { 1 + 2 })

# 輸出類似：
# == disasm: <RubyVM::InstructionSequence:0x8f5e030>===
# 0000 trace            1                                               (   1)
# 0002 putobject        1
# 0004 putobject        2
# 0006 opt_plus         <ic:0>
# 0008 trace            1
# 0010 leave
```

### 效能基準測試

| 測試項目 | Ruby 1.8 | Ruby 1.9 | 提升幅度 |
|---------|----------|----------|----------|
| fib(30) 遞迴 | 12.3s | 2.1s | 5.9x |
| 字串串接 | 1.2s | 0.4s | 3.0x |
| 雜湊查詢 | 0.8s | 0.3s | 2.7x |

## 新的語法特性

### Lambda 語法簡化

```ruby
# Ruby 1.8
lambda { |x| x * 2 }
proc { |x| x * 2 }

# Ruby 1.9：箭頭 lambda
->(x) { x * 2 }

# 額外引數處理
->(x, y, *z, w) { [x, y, z, w] }
```

### 雜湊鍵引數

```ruby
# Ruby 1.9 支援雜湊鍵作為方法引數
def connect(host:, port: 80, ssl: false)
  puts "Connecting to #{host}:#{port} (ssl=#{ssl})"
end

connect(host: "example.com", port: 443, ssl: true)
```

### 字串編碼強化

```ruby
# Ruby 1.9 的編碼支援
str = "中文"
str.encoding        # => #<Encoding:UTF-8>
str.encode("Big5") # 轉換編碼

# 明確指定原始碼編碼
# -*- coding: utf-8 -*-
```

## 纖程（Fibers）

```ruby
# Ruby 1.9 引入纖程，輕量級並發
fiber = Fiber.new do
  Fiber.yield "first"
  Fiber.yield "second"
  "done"
end

puts fiber.resume  # => "first"
puts fiber.resume  # => "second"
puts fiber.resume  # => "done"
```

---

**下一步**：[MVC 架構模式深度探索（2008）](focus3.md)

## 延伸閱讀

- [Ruby 1.9 YARV Performance](https://www.google.com/search?q=Ruby+1.9+YARV+performance+benchmark)
- [Ruby 1.9 New Features](https://www.google.com/search?q=Ruby+1.9+new+features+fibers+encoding)
- [Ruby VM Internals](https://www.google.com/search?q=Ruby+virtual+machine+YARV+internals)