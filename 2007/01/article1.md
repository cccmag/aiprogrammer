# Ruby on Rails 2.0 發布：Web 開發新標準

## 前言

2007 年，Ruby on Rails 社群正準備迎接 Rails 2.0 的發布。這一年見證了 Rails 從一個新興框架成長為主流 Web 開發方案的過程。

## Rails 的崛起背景

### 為何 Rails 如此特別

Ruby on Rails 採用了「Convention over Configuration」的設計哲學，大幅減少開發者需要做的決定數量：

```ruby
# 傳統 PHP 程式碼
<?php
class UserController extends Controller {
    function show($id) {
        $user = UserRepository->find($id);
        include 'views/user/show.php';
    }
}
?>

# Rails 程式碼
class UsersController < ApplicationController
  def show
    @user = User.find(params[:id])
  end
end
# 視圖自動對應 app/views/users/show.html.erb
```

### Rails 的核心原則

```
┌────────────────────────────────────────────────────────┐
│            Ruby on Rails 設計原則                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. Convention over Configuration                    │
│     └─ 命名慣例取代繁瑣設定                             │
│                                                        │
│  2. DRY (Don't Repeat Yourself)                       │
│     └─ 每個知識只出現一次                               │
│                                                        │
│  3. RESTful 架構                                      │
│     └─ 資源導向的 URL 設計                             │
│                                                        │
│  4. 測試驅動開發                                       │
│     └─ 內建完整的測試框架                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Rails 2.0 的新特性

### RESTful 資源支援

Rails 2.0 強化了 RESTful 支援：

```ruby
# config/routes.rb - Rails 2.0 RESTful 路由
ActionController::Routing::Routes.draw do |map|
  map.resources :users do |user|
    user.resources :posts
  end

  map.root :controller => "home"
end

# 自動產生七個標準 RESTful 路由：
# GET    /users           index
# GET    /users/:id       show
# GET    /users/new       new
# POST   /users           create
# GET    /users/:id/edit  edit
# PUT    /users/:id       update
# DELETE /users/:id       destroy
```

### Atom Feed 支援

Rails 2.0 內建 Atom Publishing Protocol 支援：

```ruby
class PostsController < ApplicationController
  respond_to :html, :xml, :atom

  def index
    @posts = Post.all
    respond_with(@posts)
  end
end

# app/views/posts/index.atom.builder
atom_feed do |feed|
  feed.title("My Posts")
  feed.updated(@posts.first.created_at)

  @posts.each do |post|
    feed.entry(post) do |entry|
      entry.title(post.title)
      entry.content(post.body)
    end
  end
end
```

### 多環境設定

Rails 2.0 改進了環境設定：

```ruby
# config/environments/production.rb
config.after_initialize do
  # 生產環境初始化後的設定
end

# 資料庫.yml 支援多環境設定
production:
  adapter: postgresql
  database: myapp_production
  username: deploy
  password: <%= ENV['DB_PASSWORD'] %>
```

## Rails 對產業的影響

### 2007 年的 Web 開發格局

```
┌────────────────────────────────────────────────────────┐
│            2007 年 Web 開發框架選擇                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  企業級：                                              │
│  - Java EE (Spring, Struts)                           │
│  - Microsoft ASP.NET                                 │
│  - PHP (Zend, Symfony)                               │
│                                                        │
│  新興框架：                                            │
│  - Ruby on Rails                                     │
│  - Django (Python)                                   │
│  - Grails (Groovy)                                   │
│                                                        │
│  特點：                                                │
│  - Rails 強調「優雅」與「生產力」                      │
│  - Django 強調「 batteries included」                │
│  - 兩者都推動了 Python/Ruby 的普及                    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Rails 成功的關鍵因素

1. **37signals 的背書**
   - Basecamp 等產品證明 Rails 的能力
   - Getting Real 一書推廣了小而美的開發理念

2. **活躍的社群**
   - 大量插件（gems）
   - 完善的文件
   - 頻繁的版本更新

3. **人才培養**
   - RailsBridge 工作坊
   - PeepCode 等教學網站
   - 大量英文和中文教程

## Rails 2.0 的技術棧

### 標準技術組合

```
┌────────────────────────────────────────────────────────┐
│         Rails 2.0 標準技術棧                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  前端：                                                │
│  - ERB 樣板                                          │
│  - Prototype/Scriptaculous                           │
│  - RJS (Ruby JavaScript)                             │
│                                                        │
│  後端：                                                │
│  - ActiveRecord ORM                                  │
│  - ActionMailer                                      │
│  - ActiveSupport                                     │
│                                                        │
│  資料庫：                                              │
│  - MySQL, PostgreSQL, SQLite                        │
│                                                        │
│  測試：                                                │
│  - Test::Unit                                        │
│  - RSpec (可選)                                       │
│  - Fixtures                                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### ActiveRecord 的魔力

```ruby
# 簡潔的 ORM 操作
class User < ActiveRecord::Base
  has_many :posts
  validates_presence_of :name, :email
end

# 查詢範例
User.find(:all,
  :conditions => ["posts_count > ?", 10],
  :include => :posts,
  :order => "posts_count DESC",
  :limit => 10
)

# 關聯查詢
@user.posts.find(:all, :conditions => ["created_at > ?", 1.week.ago])
```

## Rails 的輝煌與挑戰

### 2007 年的輝煌

- **Twitter** 使用 Rails 建構（雖然後來遷移）
- **Basecamp** 的成功示範
- **GitHub** 選擇 Rails
- Ruby 進入 TIOBE 排行榜前 10

### 批評與挑戰

- **效能問題**：Ruby 直譯執行的速度限制
- **擴展性**：大型網站的 Rails 部署挑戰
- **學習曲線**：Ruby 語法的獨特性
- **商業支援**：相較於 Java/.NET 較少企業支援

## 結論

Rails 2.0 的發布標誌著這個框架的成熟。它不僅改變了 Ruby 語言的命運，更深刻影響了 Web 開發的實踐方式。

「Convention over Configuration」的理念被後來的許多框架借鑒，成為現代 Web 開發的重要原則。

---

## 延伸閱讀

- [Ruby on Rails 2.0 發布說明](https://www.google.com/search?q=Rails+2.0+release+notes)
- [Rails RESTful 路由](https://www.google.com/search?q=Rails+RESTful+routing)
- [Ruby on Rails 歷史](https://www.google.com/search?q=Ruby+on+Rails+history)

---

*本篇文章為「AI 程式人雜誌 2007 年 1 月號」文章集錦系列。*