# TurboGears 框架

## 前言

TurboGears 是一個以「最佳工具組合」為設計理念的 Python Web 框架。它整合了多個成熟的元件，讓開發者可以根據需求選擇使用。

## TurboGears 的設計哲學

### 元件整合

```python
turbogears_philosophy = {
    "目標": "使用最好的元件",
    "核心": [
        "SQLAlchemy (ORM)",
        "Genshi (模板)",
        "MochiKit (JavaScript)",
        "Paste (WSGI)"
    ],
    "優點": "每個元件都可以替換"
}
```

### 與 Django 的比較

```python
django_vs_turbogears = {
    "Django": {
        "哲學": "Batteries included",
        "ORM": "Django ORM",
        "模板": "Django Template",
        "JS": "無偏好"
    },
    "TurboGears": {
        "哲學": "Best of breed",
        "ORM": "SQLAlchemy",
        "模板": "Genshi 或 Kid",
        "JS": "MochiKit"
    }
}
```

## 歷史

### 發展歷程

```python
turbogears_history = {
    "2005": "TurboGears 1.0 發布",
    "2006": "快速成長，成為 Django 競爭者",
    "2008": "TurboGears 2.0 開發中"
}
```

## 核心元件

### SQLAlchemy ORM

```python
# 使用 SQLAlchemy 定義模型

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    bio = Column(Text)

# 查詢
users = session.query(User).filter_by(name='John').all()
```

### Genshi 模板

```python
# Genshi 模板範例

from genshi.template import TemplateLoader

loader = TemplateLoader('templates')
tmpl = loader.load('user.html')

stream = tmpl.generate(user=user_obj)
print(stream.render('html', doctype='html-transitional'))
```

### MochiKit JavaScript

```python
# MochiKit 客戶端功能

# 伺服器端仍然返回 HTML
# MochiKit 處理客戶端互動

# MochiKit 的特點：
# - 簡潔的 API
# - 與伺服器 JSON 交換
# - 視覺效果和動畫
```

## 路由系統

### @expose 裝飾器

```python
from turbogears import controllers, expose

class Root(controllers.RootController):
    @expose()
    def index(self):
        return dict()

    @expose(format='json')
    def get_user(self, user_id):
        user = User.get(user_id)
        return dict(user_name=user.name, email=user.email)
```

### URL 映射

```python
# TurboGears 2 的路由

from routes import Mapper

mapper = Mapper()
mapper.connect('home', '/', controller='blog', action='index')
mapper.connect('blog_archive', '/blog/{year}/{month}',
                controller='blog', action='archive')
```

## 資料庫操作

### Model 定義

```python
# 使用 SQLAlchemy 的模型

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User', backref='articles')
```

### CRUD 操作

```python
# 新增
article = Article(title='Hello', content='World')
session.add(article)
session.commit()

# 查詢
articles = session.query(Article).filter(Article.title.contains('Hello')).all()

# 更新
article.title = 'New Title'
session.commit()

# 刪除
session.delete(article)
session.commit()
```

## 視圖和模板

### 控制器

```python
from turbogears import controllers, expose
from turbogears.database import session

class Articles(controllers.Controller):
    @expose('templates/articles/list.html')
    def list(self):
        articles = session.query(Article).all()
        return dict(articles=articles)

    @expose('templates/articles/edit.html')
    def edit(self, article_id):
        article = session.query(Article).get(article_id)
        return dict(article=article)
```

### Genshi 模板

```html
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:py="http://genshi.edgewall.org/">

<head><title>Article List</title></head>
<body>
    <h1>Articles</h1>
    <ul py:for="article in articles">
        <li>
            <a href="/articles/${article.id}">${article.title}</a>
        </li>
    </ul>
</body>
</html>
```

## AJAX 支援

### @expose(format='json')

```python
# TurboGears 的 JSON API

class API(controllers.Controller):
    @expose(format='json')
    def users(self):
        users = session.query(User).all()
        return dict(users=[{
            'id': u.id,
            'name': u.name,
            'email': u.email
        } for u in users])
```

### MochiKit 客戶端

```javascript
// MochiKit 的 AJAX 呼叫

var d = loadJSONDoc('/api/users');
d.addCallback(function(data) {
    data.users.forEach(function(user) {
        // 處理每個使用者
    });
});
```

## 組態設定

### .ini 檔案

```ini
[server:main]
use = egg:Paste#http
host = 0.0.0.0
port = 8080

[app:main]
use = egg:TurboGears
full_stack = true
 sqlalchemy.url = sqlite:///mydb.sqlite
```

## 優點和缺點

### 優點

```python
turbogears_advantages = {
    "元件可替換": "不滿意某個元件可以更換",
    "SQLAlchemy": "功能強大的 ORM",
    "MochiKit": "良好的 AJAX 支援",
    "社群": "活躍的開發社群"
}
```

### 缺點

```python
turbogears_disadvantages = {
    "學習曲線": "需要學習多個元件",
    "版本相容": "元件升級可能需要調整",
    "文件": "比 Django 少"
}
```

## 與其他框架的整合

### TurboGears 2

```python
# TurboGears 2 的設計

tg2_components = {
    "WebOb": "請求/回應處理",
    "Repoze": "認證和授權",
    "Formalchemy": "表單處理"
}
```

---

**延伸閱讀**

- [TurboGears+official+site](https://www.google.com/search?q=TurboGears+official+site)
- [TurboGears+tutorial](https://www.google.com/search?q=TurboGears+tutorial)
- [SQLAlchemy+TurboGears](https://www.google.com/search?q=SQLAlchemy+TurboGears)