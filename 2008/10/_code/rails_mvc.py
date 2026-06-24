"""
Rails MVC 架構示範 — Model、View、Controller 互動
"""


class Post:
    def __init__(self, attrs=None):
        attrs = attrs or {}
        self.id = attrs.get("id")
        self.title = attrs.get("title", "")
        self.content = attrs.get("content", "")
        self.author = attrs.get("author", "Anonymous")
        self.created_at = attrs.get("created_at") or __import__("datetime").datetime.now()
        self.published = attrs.get("published", False)

    def summary(self, length=100):
        if len(self.content) > length:
            return self.content[:length] + "..."
        return self.content


class PostView:
    def __init__(self, post):
        self.post = post

    def render(self):
        return f"""<article class="post">
  <h1>{self.post.title}</h1>
  <div class="meta">作者：{self.post.author} | {self.post.created_at.strftime("%Y-%m-%d")}</div>
  <div class="content">{self.post.content}</div>
</article>"""

    def render_list(self):
        return f"""<li>
  <a href="/posts/{self.post.id}">{self.post.title}</a>
  <span class="author">{self.post.author}</span>
</li>"""


class PostsController:
    _posts = []
    _next_id = 1

    @classmethod
    def index(cls):
        posts = [p for p in cls._posts if p.published]
        output = "<h1>文章列表</h1><ul>"
        for p in posts:
            output += PostView(p).render_list()
        output += "</ul>"
        return output

    @classmethod
    def show(cls, id):
        post = next((p for p in cls._posts if p.id == int(id)), None)
        if post:
            return PostView(post).render()
        return "<h1>找不到文章</h1>"

    @classmethod
    def create(cls, params):
        post = Post({
            "id": cls._next_id,
            "title": params.get("title", "無標題"),
            "content": params.get("content", ""),
            "author": params.get("author", "Anonymous"),
            "published": True
        })
        cls._posts.append(post)
        cls._next_id += 1
        return f"文章已建立：{post.title}"


def demo():
    print("=== Rails MVC Demo ===\n")

    PostsController.create({"title": "Ruby on Rails 2.2", "content": "Rails 2.2 帶來多執行緒支援和 i18n 功能。", "author": "小明"})
    PostsController.create({"title": "Ruby 1.9 YARV", "content": "YARV 虛擬機將大幅提升 Ruby 效能。", "author": "大華"})
    PostsController.create({"title": "MVC 架構詳解", "content": "Model-View-Controller 分離關注點。", "author": "小美"})

    print("--- Post List ---")
    print(PostsController.index())
    print("\n--- Single Post ---")
    print(PostsController.show(1))
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()