# REST API 設計最佳實踐

## 1. RESTful 路由

```ruby
# config/routes.rb
map.resources :tweets

# 產生的路由
# GET    /tweets       => index
# POST   /tweets       => create
# GET    /tweets/:id   => show
# PUT    /tweets/:id   => update
# DELETE /tweets/:id   => destroy
```

## 2. 回應格式

```ruby
# 支援多種格式
respond_to do |format|
  format.html # index.html.erb
  format.xml  { render xml: @tweets }
  format.json { render json: @tweets }
end
```

## 3. 錯誤處理

```ruby
class TweetsController < ApplicationController
  rescue_from ActiveRecord::RecordNotFound, with: :not_found

  private

  def not_found
    respond_to do |format|
      format.json { render json: { error: "找不到資源" }, status: 404 }
    end
  end
end
```

## 4. 分頁

```ruby
# 使用 will_paginate
@tweets = Tweet.paginate(
  page: params[:page] || 1,
  per_page: params[:per_page] || 20
)

# 回應中加入分頁資訊
render json: {
  tweets: @tweets,
  total_pages: @tweets.total_pages,
  current_page: @tweets.current_page
}
```

## 5. 版本控制

```ruby
# 路由版本控制
map.resources :tweets, :path_prefix => "api/v1"

# 控制器名稱空間
namespace :api do
  namespace :v1 do
    resources :tweets
  end
end
```

## 6. 認證

```ruby
# HTTP Basic Auth
authenticate_or_request_with_http_basic do |username, password|
  User.authenticate(username, password)
end

# API Key 認證
before_filter :authenticate_api_key, except: [:index, :show]
```

---

**參考資料**
- [REST API Design](https://www.google.com/search?q=REST+API+design+best+practices+Rails)
- [Rails respond_to](https://www.google.com/search?q=Rails+respond_to+format+json+xml)
- [API Authentication Methods](https://www.google.com/search?q=API+authentication+Rails+2008)