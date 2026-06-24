# Ruby 的未來：2.0 與 beyond

## Ruby 2.0 規劃

### 預計功能

```ruby
# Ruby 2.0 的規劃（2010年之後）

# 1. 關鍵字參數
def method(name: "default")
end

# 2. Refinements
module MyExtensions
  refine String do
    def camelize
      self.split('_').map(&:capitalize).join
    end
  end
end

# 3. JIT 編譯
# 進一步提升效能
```

## 長期趨勢

### Ruby 的應用領域

```markdown
# Ruby 的主要應用

1. Web 開發（主要領域）
   - Rails
   - Sinatra

2. 自動化腳本
   - Rake
   - Thor

3. 雲端運算
   - Chef
   - Vagrant

4. 行動開發
   - RubyMotion
```

## 結語

Ruby 2.0 將帶來更多新功能，Ruby 的未來仍然光明。

---

*本篇文章為「AI 程式人雜誌 2009 年 10 月號」焦點系列之一。*