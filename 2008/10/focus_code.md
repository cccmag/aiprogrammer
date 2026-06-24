# 程式實作：Rails MVC 實作範例

## 簡介

本實作展示 Rails MVC 架構的核心概念，包含 Model、View、Controller 的互動。完整程式碼在 `_code/rails_mvc.rb`。

## Model 層：Post 模型

```ruby
class Post
  attr_accessor :id, :title, :content, :author, :created_at, :published

  def initialize(attrs = {})
    @id = attrs[:id]
    @title = attrs[:title] || ""
    @content = attrs[:content] || ""
    @author = attrs[:author] || "Anonymous"
    @created_at = attrs[:created_at] || Time.now
    @published = attrs[:published] || false
  end

  def to_h
    { id: @id, title: @title, content: @content,
      author: @author, created_at: @created_at, published: @published }
  end

  def summary(length = 100)
    @content.length > length ? @content[0...length] + "..." : @content
  end
end
```

## View 層：HTML 產生器

```ruby
class PostView
  def initialize(post)
    @post = post
  end

  def render
    <<~HTML
      <article class="post">
        <h1>#{@post.title}</h1>
        <div class="meta">作者：#{@post.author} | #{@post.created_at.strftime("%Y-%m-%d")}</div>
        <div class="content">#{@post.content}</div>
      </article>
    HTML
  end

  def render_list
    <<~HTML
      <li>
        <a href="/posts/#{@post.id}">#{@post.title}</a>
        <span class="author">#{@post.author}</span>
      </li>
    HTML
  end
end
```

## Controller 層：路由與動作

```ruby
class PostsController
  @@posts = []
  @@next_id = 1

  def self.index
    posts = @@posts.select(&:published)
    output = "<h1>文章列表</h1><ul>"
    posts.each { |p| output += PostView.new(p).render_list }
    output + "</ul>"
  end

  def self.show(id)
    post = @@posts.find { |p| p.id == id.to_i }
    if post
      PostView.new(post).render
    else
      "<h1>找不到文章</h1>"
    end
  end

  def self.create(params)
    post = Post.new(
      id: (@@next_id += -1),
      title: params[:title],
      content: params[:content],
      author: params[:author] || "Anonymous",
      published: true
    )
    @@posts << post
    "文章已建立：#{post.title}"
  end
end
```

## 路由系統

```ruby
class Router
  @@routes = {
    "GET" => {},
    "POST" => {}
  }

  def self.draw
    yield Router
  end

  def self.get(path, controller, action)
    @@routes["GET"][path] = [controller, action]
  end

  def self.post(path, controller, action)
    @@routes["POST"][path] = [controller, action]
  end

  def self.route(method, path)
    @@routes[method][path]
  end
end
```

## 執行方式

```bash
cd _code
python3 rails_mvc.rb
```

## 延伸練習

1. **新增驗證**：在 Post 模型中加入標題不能為空的驗證
2. **分頁功能**：為 index 動作加入分頁支援
3. **搜尋**：新增搜尋功能，過濾文章標題和內容
4. **評論系統**：建立 Comment 模型和一對多關聯
5. **RESTful 路由**：實作完整的 RESTful 路由與控制器動作