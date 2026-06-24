# 快取機制與效能優化

## 1. 頁面快取

```ruby
# 快取整個頁面
caches_page :index, :show

# 過期時間
caches_page :index, :expires_in => 1.hour
```

## 2. 動作快取

```ruby
# 經過控制器，快取動作輸出
caches_action :index, :show

# 快取過期
expire_action :posts_url
expire_action :post_url(@post)
```

## 3. 片斷快取

```erb
<% cache do %>
  <%= render @posts %>
<% end %>
```

```erb
<!-- 快取特定片段 -->
<% cache("sidebar_#{current_user.id}") do %>
  <%= render "sidebar/profile" %>
<% end %>
```

## 4. Rails.cache

```ruby
# 讀寫快取
Rails.cache.write("key", "value", expires_in: 1.hour)
Rails.cache.read("key")
Rails.cache.fetch("key") { compute_value }

# 刪除
Rails.cache.delete("key")
Rails.cache.clear
```

## 5. Redis 快取後端

```ruby
# config/environment.rb
config.cache_store = :redis_store, "redis://localhost:6379/0"
```

## 6. SQL 查詢優化

```ruby
# 避免 N+1 查詢
# 不好
@posts.each { |p| puts p.author.name }

# 好（使用 eager_load）
@posts = Post.includes(:author).all
@posts.each { |p| puts p.author.name }
```

---

**參考資料**
- [Rails Caching Guide](https://www.google.com/search?q=Rails+caching+fragment+action+page)
- [Rails Performance Optimization](https://www.google.com/search?q=Rails+performance+optimization+caching)
- [N+1 Query Problem](https://www.google.com/search?q=N+1+query+problem+Rails+includes)