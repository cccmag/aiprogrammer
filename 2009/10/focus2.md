# Rails 3.0 開發中：Merb 合併

## Rails 3.0 的願景

### Merb 合併

Rails 3.0 吸收了 Merb 的設計理念，帶來了更模組化的架構。

```ruby
# Rails 3.0 的模組化
# 核心 actionpack, activerecord, activesupport
# 可選：JRuby 支援, 編譯引擎
```

## 主要改進

### 效能優化

```ruby
# Rails 3.0 效能改進

# 1. 更快的新增（create）
# 2. 更少的記憶體使用
# 3. 更好的查詢緩存

# 效能對比 Rails 2.3
# 請求處理：快 15-20%
# 記憶體使用：少 10-15%
```

### API 清理

```ruby
# Rails 3.0 的 API 清理

# 統一的查詢介面
# ActiveRecord::Relation
User.where(:name => "張三").limit(10)

# 更好的作用域
scope :active, where(:active => true)
```

## 結語

Rails 3.0 將是自 Rails 1.0 以來最大的版本更新。

---

*本篇文章為「AI 程式人雜誌 2009 年 10 月號」焦點系列之一。*