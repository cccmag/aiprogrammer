# Rails 路由與 RESTful 設計（2008）

## RESTful 路由

### 前言

Rails 的路由系統遵循 RESTful 原則，將 HTTP 方法（GET、POST、PUT、DELETE）對應到資源的 CRUD 操作。

### Resources 路由

```ruby
# config/routes.rb
map.resources :posts
map.resources :users, :has_many => :posts
map.resources :posts, :has_many => :comments, :as => :article_comments
```

### 生成的路由

| HTTP 方法 | 路徑 | Controller#動作 | 用途 |
|-----------|------|-----------------|------|
| GET | /posts | posts#index | 列表 |
| GET | /posts/:id | posts#show | 顯示 |
| GET | /posts/new | posts#new | 新增表單 |
| POST | /posts | posts#create | 建立 |
| GET | /posts/:id/edit | posts#edit | 編輯表單 |
| PUT | /posts/:id | posts#update | 更新 |
| DELETE | /posts/:id | posts#destroy | 刪除 |

## 自訂路由

### 巢狀資源

```ruby
map.resources :users do |users|
  users.resources :posts, :comments
end

# 產生的路徑：
# /users/:user_id/posts
# /users/:user_id/posts/:id
```

### 會員與集合動作

```ruby
map.resources :posts, :member => { :vote => :post, :favorite => :get },
                          :collection => { :search => :get, :export => :post }

# /posts/:id/vote (POST)
# /posts/:id/favorite (GET)
# /posts/search (GET)
# /posts/export (POST)
```

### 路徑與 URL 輔助方法

```ruby
# 路徑輔助方法
posts_path           # => /posts
post_path(@post)     # => /posts/1
new_post_path        # => /posts/new

# 巢狀路徑
user_post_path(@user, @post)  # => /users/1/posts/1
```

## 名稱空間

```ruby
# 管理後台
map.namespace :admin do |admin|
  admin.resources :posts, :users
end

# /admin/posts
# Admin::PostsController
```

## 路由約束

```ruby
map.with_options :constraints => { :subdomain => /admin/ } do |admin|
  admin.resources :posts
end

map.posts 'posts/:year/:month', :controller => 'posts',
  :action => 'index',
  :constraints => { :year => /\d{4}/, :month => /\d{1,2}/ }
```

---

**下一步**：[ActionView 與模板系統（2008）](focus6.md)

## 延伸閱讀

- [Rails RESTful Routing](https://www.google.com/search?q=Rails+RESTful+routing+resources)
- [Rails Routes Documentation](https://www.google.com/search?q=Rails+routes+dynamic+segments)
- [REST API Design](https://www.google.com/search?q=REST+API+design+best+practices+2008)