# Ruby on Rails 1.2：REST 與多國語言

## 前言

2007 年 1 月，Ruby on Rails 1.2 發布。這是 Rails 發展史上重要的里程碑，引入了 RESTful 路由和多國語言支援。

## RESTful 路由

Rails 1.2 正式支援 REST 架構：

```ruby
# config/routes.rb
ActionController::Routing::Routes.draw do |map|
  map.resources :posts
  map.resources :comments, :belongs_to => :post
end

# 產生的路由：
# GET    /posts          posts#index
# POST   /posts          posts#create
# GET    /posts/new      posts#new
# GET    /posts/1         posts#show
# PUT    /posts/1         posts#update
# DELETE /posts/1         posts#destroy
```

## 多國語言支援

Rails 1.2 引入的 Internationalization API：

```ruby
# config/locales/zh-TW.yml
zh-TW:
  posts:
    index:
      title: "文章列表"
    show:
      published: "發佈於 %{date}"
```

```ruby
# 在視圖中使用
<%= t('.title') %>
<%= t('.published', :date => @post.created_at) %>
```

## 新功能

- ActiveResource：RESTful Web 服務用戶端
- 更好的 Ajax 支援
- 改進的錯誤處理

## 結語

Rails 1.2 的 REST 支援，奠定了「慣例優於設定」原則在 API 設計中的應用。這種設計方式至今仍是 Web API 的主流。

---

## 延伸閱讀

- [Rails+1.2+REST+support](https://www.google.com/search?q=Rails+1.2+REST+support)
- [Ruby+on+Rails+Internationalization](https://www.google.com/search?q=Ruby+on+Rails+Internationalization+1.2)

---