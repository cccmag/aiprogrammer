# ActionView 與模板系統（2008）

## ERB 模板

### 前言

ActionView 負責產生 HTML 輸出。Rails 預設使用 ERB（Embedded Ruby）模板，將 Ruby 程式碼嵌入 HTML。

### 程式碼區塊

```erb
<%# 不輸出結果 %>
<% (1..5).each do |i| %>
  <p>數字：<%= i %></p>
<% end %>

<%# 輸出結果 %>
<%= @user.name %>
<%= render :partial => "user", :collection => @users %>
```

### 表單輔助方法

```erb
<% form_for @user do |f| %>
  <p>
    <%= f.label :name, "名稱" %>
    <%= f.text_field :name %>
    <%= f.error_message_on :name %>
  </p>
  <p>
    <%= f.label :email %>
    <%= f.text_field :email %>
  </p>
  <p>
    <%= f.submit "儲存" %>
  </p>
<% end %>
```

## Partials（局部範本）

### 建立 Partial

```erb
<%# app/views/posts/_post.html.erb %>
<article class="post">
  <h2><%= post.title %></h2>
  <div class="content"><%= post.content %></div>
  <footer>由 <%= post.author %> 發表</footer>
</article>
```

### 渲染 Partial

```erb
<%# 渲染集合 %>
<%= render :partial => "post", :collection => @posts, :spacer_template => "divider" %>

<%# 簡化語法（ Rails 3+ ）%>
<%= render @posts %>

<%# 帶區域變數 %>
<%= render :partial => "post", :locals => { :featured => true } %>
```

## Layouts（版面配置）

### 應用程式 Layout

```erb
<%# app/views/layouts/application.html.erb %>
<!DOCTYPE html>
<html>
<head>
  <title><%= title %></title>
  <%= stylesheet_link_tag :all %>
  <%= javascript_include_tag :defaults %>
  <%= csrf_meta_tag %>
</head>
<body>
  <header><%= render "shared/header" %></header>
  <main><%= yield %></main>
  <footer><%= render "shared/footer" %></footer>
</body>
</html>
```

### 控制器的 Layout

```ruby
class PostsController < ApplicationController
  layout "admin", except: [:index, :show]
end
```

## Helper 函式

### 文字輔助

```erb
<%= truncate(@post.content, length: 150, separator: " ") %>
<%= excerpt(@post.content, "關鍵詞", radius: 100) %>
<%= simple_format(@post.content) %>
<%= highlight(@post.content, "Ruby") %>
```

### 數字與日期

```erb
<%= number_to_currency(123456.78) %>           <%# $123,456.78 %>
<%= number_to_human_size(1048576) %>            <%# 1 MB %>
<%= distance_of_time_in_words(1.minute ago) %>  <%# less than a minute %>
<%= time_ago_in_words(3.days.ago) %>             <%# 3 days %>
```

---

**下一步**：[Rails 生態系插件與 Gem（2008）](focus7.md)

## 延伸閱讀

- [Rails ActionView Helpers](https://www.google.com/search?q=Rails+ActionView+helper+methods)
- [ERB Templates](https://www.google.com/search?q=ERB+template+Rails+partials+layouts)
- [Form Helper Documentation](https://www.google.com/search?q=Rails+form+helpers+form_for)