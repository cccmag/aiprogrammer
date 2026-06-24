# Rails 生態系插件與 Gem（2008）

## 重要的 Gem 套件

### 前言

Rails 的繁榮離不開豐富的插件與 Gem 生態系統。2008 年有許多重要的開源貢獻。

## 認證與授權

### Authlogic

```ruby
# Gemfile
config.gem "authlogic"

# app/models/user.rb
class User < ActiveRecord::Base
  acts_as_authentic
end

# SessionsController
class SessionsController < ApplicationController
  def create
    user = User.find_by_email(params[:email])
    if user && user.valid_password?(params[:password])
      user_session = UserSession.create(user)
      redirect_to dashboard_path
    end
  end
end
```

### RESTful_ACL

```ruby
# 資源存取控制
class PostsController < ApplicationController
  deny_access Unless: ["admin", "author"].include?(current_role),
                 :except => [:index, :show]
  allow_access :all, :only => [:index, :show]
end
```

## 檔案上傳

### Paperclip

```ruby
# Migration
add_column :users, :avatar_file_name, :string
add_column :users, :avatar_content_type, :string
add_column :users, :avatar_file_size, :integer

# Model
class User < ActiveRecord::Base
  has_attached_file :avatar,
    :styles => { :medium => "300x300>", :thumb => "100x100>" },
    :path => ":rails_root/public/assets/:class/:id/:basename.:extension"
end
```

##搜尋引擎

### Thinking Sphinx

```ruby
# 定義索引
class Post < ActiveRecord::Base
  define_index do
    indexes title, content, author
    indexes [category, name], :as => :category
    has created_at
  end
end

# 搜尋
Post.search "Rails", :conditions => { :published => true }
```

## 分頁

### Will Paginate

```ruby
# Controller
@posts = Post.paginate(page: params[:page], per_page: 20)

# View
<%= will_paginate @posts %>

# 自訂連結範圍
<%= will_paginate @posts, :params => { :controller => "articles" } %>
```

## 視圖輔助

### Haml

```haml
# 取代 ERB 的標記語言
.post
  %h2= post.title
  .content= post.content
  .meta
    發表於
    = post.created_at.strftime("%Y-%m-%d")
```

### SimpleForm

```erb
<%= form_for @user do |f| %>
  <%= f.input :name, :label => "名稱" %>
  <%= f.input :email, :required => true %>
  <%= f.button :submit %>
<% end %>
```

---

**下一步**：[結語](end.md)

## 延伸閱讀

- [Rails Plugins Directory](https://www.google.com/search?q=Rails+plugins+gem+2008+authlogic+paperclip)
- [Thinking Sphinx Search](https://www.google.com/search?q=Thinking+Sphinx+Rails+search)
- [Haml Rails Integration](https://www.google.com/search?q=Haml+Sass+Rails+templates)