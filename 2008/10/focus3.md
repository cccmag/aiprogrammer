# MVC 架構模式深度探索（2008）

## 模型-視圖-控制器模式

### 前言

MVC（Model-View-Controller）是 Rails 應用程式的核心架構。這個模式將應用程式分為三個相互交互的層次，實現關注點分離。

### Rails 中的 MVC 對應

| 層次 | Rails 元件 | 職責 |
|------|------------|------|
| Model | ActiveRecord | 資料與商業邏輯 |
| View | ActionView | 使用者介面呈現 |
| Controller | ActionController | 請求處理與流程控制 |

## Model 層：ActiveRecord

### 關聯定義

```ruby
class User < ActiveRecord::Base
  has_many :posts, dependent: :destroy
  has_many :comments, through: :posts
  belongs_to :company

  validates :email, presence: true, uniqueness: true

  def full_name
    "#{first_name} #{last_name}"
  end
end
```

### 查詢介面

```ruby
# 動態查詢方法
User.find_by_email_and_active("test@example.com", true)
User.where("created_at > ?", 1.week.ago).order(:name)

# 命名範圍
class Post < ActiveRecord::Base
  scope :published, -> { where(published: true) }
  scope :recent, -> { order(created_at: :desc).limit(10) }
end
```

## View 層：ActionView

### ERB 模板

```erb
<%# app/views/users/show.html.erb %>
<h1><%= @user.full_name %></h1>

<% @user.posts.each do |post| %>
  <article>
    <h2><%= post.title %></h2>
    <p><%= truncate(post.content, length: 100) %></p>
  </article>
<% end %>
```

### Helper 方法

```ruby
module ApplicationHelper
  def gravatar_url(user, size = 80)
    hash = Digest::MD5.hexdigest(user.email.downcase)
    "https://www.gravatar.com/avatar/#{hash}?s=#{size}"
  end

  def format_date(date)
    content_tag(:span, l(date), title: date.iso8601)
  end
end
```

## Controller 層：ActionController

### RESTful 路由與動作

```ruby
class PostsController < ApplicationController
  before_action :set_post, only: [:show, :edit, :update, :destroy]
  before_action :authenticate, except: [:index, :show]

  def index
    @posts = Post.published.recent
    respond_with @posts
  end

  def show
    respond_with @post
  end

  def create
    @post = Post.new(post_params)
    @post.save
    respond_with @post
  end

  private

  def post_params
    params.require(:post).permit(:title, :content, :published)
  end
end
```

### Flash 訊息

```ruby
# 設定 flash 訊息
redirect_to @post, notice: "文章已發布"
redirect_to @post, alert: "發布失敗"

# 在視圖中顯示
<% if notice %>
  <p class="notice"><%= notice %></p>
<% end %>
```

---

**下一步**：[ActiveRecord 與資料庫抽象層（2008）](focus4.md)

## 延伸閱讀

- [Rails MVC Pattern](https://www.google.com/search?q=Rails+MVC+architecture+pattern)
- [ActiveRecord Associations](https://www.google.com/search?q=ActiveRecord+associations+has_many+belongs_to)
- [ActionController Best Practices](https://www.google.com/search?q=ActionController+best+practices+Rails)