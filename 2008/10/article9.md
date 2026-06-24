# Rails 安全性考量

## 1. Mass Assignment

```ruby
# 防止大量賦值
class User < ActiveRecord::Base
  attr_protected :admin  # 阻止 :admin 屬性被外部設定
end

# 或使用 attr_accessible（需要 gem）
attr_accessible :name, :email, :password
```

## 2. SQL 注入

```ruby
# 不安全
User.where("name = '#{params[:name]}'")

# 安全：使用參數化查詢
User.where("name = ?", params[:name])
User.where(name: params[:name])
```

## 3. XSS 防護

```erb
<!-- 自動跳脫 -->
<%= @post.content %>

<!-- 原始 HTML（小心使用）-->
<%= raw(@post.content) if @post.trusted? %>
```

## 4. CSRF 防護

```ruby
# 在表單中自動加入 CSRF token
<%= form_for @post do |f| %>
  <%= f.hidden_field :authenticity_token, value: form_authenticity_token %>
<% end %>

# 取消特定控制的 CSRF
skip_before_filter :verify_authenticity_token, only: [:api_action]
```

## 5. Session 安全

```ruby
# config/initializers/session_store.rb
ActionController::Base.session_store = :active_record_store

# 設定 secure cookie
cookies[:token], secure: true, httponly: true
```

## 6. 密碼儲存

```ruby
# 不要儲存明文密碼
# 使用 hash + salt
require 'digest/sha2'

class User < ActiveRecord::Base
  before_save :hash_password

  def hash_password
    self.password_salt = SecureRandom.base64(16)
    self.password_hash = Digest::SHA256.hexdigest(password + password_salt)
  end
end
```

---

**參考資料**
- [Rails Security Guide](https://www.google.com/search?q=Rails+security+mass+assignment+injection)
- [OWASP Top 10](https://www.google.com/search?q=OWASP+top+10+web+security)
- [CSRF Protection Rails](https://www.google.com/search?q=Rails+CSRF+protection+authenticity+token)