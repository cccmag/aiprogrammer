# Pylons 框架

## 前言

Pylons 是一個以極度彈性和自由為設計理念的 Python Web 框架。它讓開發者幾乎可以選擇所有元件，適合需要高度客製化的專案。

## Pylons 的設計哲學

### 「提供選擇」

```python
pylons_philosophy = {
    "核心": "Paste + Routes + SQLAlchemy + 自由選擇模板",
    "設計": "最小限制，最大彈性",
    "目標": "適合有經驗的開發者"
}
```

### 與 Django 的對比

```python
django_vs_pylons = {
    "Django": {
        "風格": "明確的慣例和結構",
        "ORM": "Django ORM",
        "模板": "Django Template",
        "路線": "預設選擇都是最好的"
    },
    "Pylons": {
        "風格": "你決定一切",
        "ORM": "SQLAlchemy 或其他",
        "模板": "任何你喜歡的",
        "路線": "提供工具，讓你選擇"
    }
}
```

## 核心元件

### Paste

```python
# Paste 是 WSGI 伺服器框架

paste_components = {
    "Paste Deploy": "設定和載入 WSGI 應用",
    "Paste Script": "命令列工具",
    "Paste Server": "開發伺服器"
}

# 設定檔範例 (development.ini)
[app:main]
use = egg:Pylons
sqlalchemy.url = sqlite:///dev.db
```

### Routes

```python
# Routes 是靈活的 URL 映射系統

from routes import Mapper

mapper = Mapper()
mapper.connect('home', '/', controller='blog', action='index')
mapper.connect('article', '/article/{slug}',
               controller='blog', action='view')
mapper.connect('archive', '/{year}/{month}/{slug}',
               controller='blog', action='archive',
               requirements={'year': r'\d{4}'})
```

### SQLAlchemy

```python
# Pylons 通常搭配 SQLAlchemy

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'mymodel'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text)
```

## 專案結構

### Pylons 專案範例

```
myproject/
├── development.ini      # 開發環境設定
├── myproject/
│   ├── __init__.py      # 應用工廠
│   ├── config/
│   │   ├── environment.py
│   │   └── middleware.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── blog.py
│   ├── model/
│   │   ├── __init__.py
│   │   └── meta.py
│   ├── lib/
│   │   ├── __init__.py
│   │   └── helpers.py
│   ├── public/           # 靜態檔案
│   │   ├── images/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       ├── base.html
│       └── blog/
│           └── index.html
└── setup.py
```

## Controllers

### 控制器定義

```python
# myproject/controllers/blog.py

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from myproject.lib.base import BaseController

class BlogController(BaseController):

    def index(self):
        """文章列表"""
        c.articles = meta.Session.query(Article).all()
        return render('/blog/index.html')

    def show(self, id):
        """文章詳情"""
        c.article = meta.Session.query(Article).get(int(id))
        if not c.article:
            abort(404)
        return render('/blog/show.html')
```

## Templates

### 模板選擇

```python
# Pylons 不綁定特定模板

template_options = {
    "Mako": "預設，速度快",
    "Genshi": "XML 為基礎",
    "Jinja2": "類似 Django",
    "Kid": "簡單 XML"
}
```

### Mako 範例

```html
<%inherit file="/base.html"/>

<%def name="title()">${article.title}</%def>

<article>
    <h1>${article.title}</h1>
    <div class="meta">
        By ${article.author} on ${article.created_at}
    </div>
    <div class="content">
        ${article.content}
    </div>
</article>
```

## URL 路由

### Routes 映射

```python
# config/routing.py

def make_map():
    map = Mapper()
    map.explicit = False

    # 設定控制器前綴
    map.controller('blog', path_prefix='/blog')

    # 預設路由
    map.connect('{controller}/{action}')
    map.connect('{controller}/{action}/{id}')

    return map
```

## 請求和回應

### Pylons 全域物件

```python
# Pylons 的方便的全域物件

request       # 目前的請求
response      # 目前的回應
session       # 使用者 session
c             # 模板上下文
config        # 設定物件
```

### 處理表單

```python
def submit(self):
    # GET 參數
    name = request.params.get('name')

    # POST 參數
    email = request.POST.get('email')

    # 上傳檔案
    upload = request.POST.get('file')
    if upload.file:
        content = upload.file.read()
```

## 錯誤處理

### HTTP 錯誤

```python
from pylons.controllers.util import abort, redirect

def view(self, id):
    article = get_article(id)
    if not article:
        abort(404, "Article not found")

    if not article.is_published:
        redirect(url('edit_article', id=id))
```

### 自訂錯誤頁面

```python
# config/middleware.py

def make_app(global_conf, **app_conf):
    # 錯誤處理中介軟體
    app = HTTPExceptionsErrorHandler(app, global_conf, **app_conf)

    return app
```

## 優點

### 為何選擇 Pylons

```python
pylons_advantages = {
    "極度彈性": "幾乎所有東西都可以替換",
    "WSGI": "基於 WSGI，與時並進",
    "社群": "有經驗的開發者社群",
    "工具選擇": "用自己習慣的工具"
}
```

## 缺點

### Pylons 的問題

```python
pylons_disadvantages = {
    "學習曲線": "需要自己做很多決定",
    "無 admin": "沒有 Django 的自動 admin",
    "文件分散": "不同元件有不同文件",
    "門檻": "適合有經驗的開發者"
}
```

## Pyramid 的前身

### Pylons 專案的延續

```python
pylons_to_pyramid = {
    "2009": "Pylons 1.0 發布",
    "2010": "Pyramid 1.0 發布（Pylons 內核 + 改進）",
    "現在": "Pyramid 持續維護中"
}
```

---

**延伸閱讀**

- [Pylons+project](https://www.google.com/search?q=Pylons+project)
- [Pylons+vs+Django](https://www.google.com/search?q=Pylons+vs+Django)
- [Pyramid+Python+framework](https://www.google.com/search?q=Pyramid+Python+framework)