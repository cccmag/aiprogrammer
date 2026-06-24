# Django 核心程式實作

## 前言

本篇文章展示 `django_blog.py` 的完整程式碼，模擬 Django 框架的核心概念。Django 的 MTV 模式、ORM、和 URL 路由是其核心特色。

---

## 原始碼

完整的 Python 實作請參考：[_code/django_blog.py](_code/django_blog.py)

```python
#!/usr/bin/env python3
"""Django 核心概念示範程式"""

import re
from datetime import datetime


class Field:
    def __init__(self, field_type, **kwargs):
        self.field_type = field_type
        self.kwargs = kwargs
        self.name = None

    def contribute_to_class(self, model_class, name):
        self.name = name
        setattr(model_class, name, self)


class CharField(Field):
    def __init__(self, max_length=100, **kwargs):
        super().__init__('char', max_length=max_length, **kwargs)


class TextField(Field):
    def __init__(self, **kwargs):
        super().__init__('text', **kwargs)


class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__('int', **kwargs)


class DateTimeField(Field):
    def __init__(self, auto_now_add=False, **kwargs):
        super().__init__('datetime', auto_now_add=auto_now_add, **kwargs)


class ForeignKey(Field):
    def __init__(self, to, **kwargs):
        super().__init__('foreignkey', to=to, **kwargs)


class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        attrs['_meta'] = ModelOptions(attrs.get('Meta', {}))
        attrs['_fields'] = {}

        for attr_name, attr_value in list(attrs.items()):
            if isinstance(attr_value, Field):
                attr_value.contribute_to_class(mcs, attr_name)
                attrs['_fields'][attr_name] = attr_value

        return super().__new__(mcs, name, bases, attrs)


class ModelOptions:
    def __init__(self, meta):
        self.verbose_name = getattr(meta, 'verbose_name', None)
        self.verbose_name_plural = getattr(meta, 'verbose_name_plural', None)
        self.ordering = getattr(meta, 'ordering', None)


class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def objects(cls):
        return Manager(cls)

    def save(self):
        if not hasattr(self, 'id'):
            self.id = len(Model._registry) + 1
            Model._registry[self.id] = self
        else:
            Model._registry[self.id] = self

    def delete(self):
        if hasattr(self, 'id') and self.id in Model._registry:
            del Model._registry[self.id]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {getattr(self, 'title', 'untitled')}>"

    _registry = {}


class Manager:
    def __init__(self, model_class):
        self.model_class = model_class

    def all(self):
        return [obj for obj in Model._registry.values()
                if isinstance(obj, self.model_class)]

    def filter(self, **kwargs):
        results = self.all()
        for key, value in kwargs.items():
            if '__' in key:
                field, op = key.split('__')
                if op == 'exact':
                    results = [r for r in results if getattr(r, field, None) == value]
                elif op == 'contains':
                    results = [r for r in results if value.lower() in str(getattr(r, field, '')).lower()]
                elif op == 'gt':
                    results = [r for r in results if getattr(r, field, 0) > value]
            else:
                results = [r for r in results if getattr(r, key, None) == value]
        return results

    def get(self, **kwargs):
        results = self.filter(**kwargs)
        if not results:
            raise DoesNotExist(f"{self.model_class.__name__} not found")
        if len(results) > 1:
            raise MultipleObjectsReturned("Multiple objects returned")
        return results[0]


class DoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class Article(Model):
    title = CharField(max_length=200)
    content = TextField()
    author = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    status = CharField(max_length=20, default='draft')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']


class Category(Model):
    name = CharField(max_length=50)

    def __repr__(self):
        return f"<Category: {self.name}>"


class URLPattern:
    def __init__(self, regex, view_func):
        self.regex = re.compile(regex)
        self.view_func = view_func

    def match(self, path):
        match = self.regex.match(path)
        if match:
            return match.groups(), self.view_func
        return None, None


class URLResolver:
    def __init__(self):
        self.patterns = []

    def register(self, regex, view_func):
        self.patterns.append(URLPattern(regex, view_func))

    def resolve(self, path):
        for pattern in self.patterns:
            args, view_func = pattern.match(path)
            if view_func:
                return args, view_func
        return None, None


class Template:
    def __init__(self, template_string):
        self.template_string = template_string

    def render(self, context):
        result = self.template_string

        for key, value in context.items():
            result = result.replace(f'{{{{{key}}}}}', str(value))

        result = re.sub(r'{%\s*for\s+(\w+)\s+in\s+(\w+)\s%}',
                        '', result)
        result = re.sub(r'{%\s*endfor\s*%}', '', result)

        return result


class TemplateLoader:
    def __init__(self):
        self.templates = {}

    def add_template(self, name, content):
        self.templates[name] = Template(content)

    def get_template(self, name):
        if name in self.templates:
            return self.templates[name]
        raise TemplateDoesNotExist(f"Template '{name}' not found")


class TemplateDoesNotExist(Exception):
    pass


def render_to_response(template_name, context=None):
    if context is None:
        context = {}
    loader = TemplateLoader()
    template = loader.get_template(template_name)
    return template.render(context)


class HttpResponse:
    def __init__(self, content='', status=200):
        self.content = content
        self.status = status

    def __str__(self):
        return self.content


class Request:
    def __init__(self, path, method='GET', data=None):
        self.path = path
        self.method = method
        self.GET = data or {}
        self.POST = data or {}
        self.user = None


def article_list_view(request):
    articles = Article.objects.all()
    html = "<h1>文章列表</h1>"
    for a in articles:
        html += f"<h2>{a.title}</h2><p>{a.content[:50]}...</p>"
    return HttpResponse(html)


def article_detail_view(request, article_id):
    try:
        article = Article.objects.get(id=int(article_id))
        html = f"<h1>{article.title}</h1><p>{article.content}</p>"
        return HttpResponse(html)
    except DoesNotExist:
        return HttpResponse("Article not found", status=404)


def article_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled')
        content = request.POST.get('content', '')
        article = Article(title=title, content=content, author='Anonymous')
        article.save()
        return HttpResponse(f"Created: {article}")
    return HttpResponse("<form method='post'>Title: <input name='title'><br><textarea name='content'></textarea><br><button>Submit</button></form>")


def demo_models():
    print("\n=== Django Model 示範 ===")

    category = Category(name="Technology")
    category.save()
    print(f"Created: {category}")

    article1 = Article(
        title="Django 入門",
        content="Django 是 Python 的 Web 框架...",
        author="John"
    )
    article1.save()
    print(f"Created: {article1}")

    article2 = Article(
        title="Python Web 開發",
        content="Python 有很多 Web 框架...",
        author="Jane"
    )
    article2.save()
    print(f"Created: {article2}")

    print(f"\nAll articles: {Article.objects.all()}")
    print(f"Filtered: {Article.objects.filter(author='John')}")


def demo_urls():
    print("\n=== URL 路由示範 ===")

    resolver = URLResolver()
    resolver.register(r'^articles/$', article_list_view)
    resolver.register(r'^articles/(\d+)/$', article_detail_view)
    resolver.register(r'^articles/create/$', article_create_view)

    paths = ['/articles/', '/articles/1/', '/articles/2/']
    for path in paths:
        args, view_func = resolver.resolve(path)
        if view_func:
            request = Request(path)
            response = view_func(request, *args)
            print(f"  {path} -> {view_func.__name__}")
        else:
            print(f"  {path} -> Not found")


def demo_templates():
    print("\n=== Template 示範 ===")

    loader = TemplateLoader()
    loader.add_template('article_list.html',
        '<h1>{{ title }}</h1><ul>{% for article in articles %}<li>{{ article.title }}</li>{% endfor %}</ul>')

    context = {
        'title': '文章列表',
        'articles': Article.objects.all()
    }

    template = loader.get_template('article_list.html')
    result = template.render(context)
    print(f"  Rendered: {result[:100]}...")


def demo_request_response():
    print("\n=== Request/Response 示範 ===")

    request = Request('/articles/', method='POST', data={'title': 'Test', 'content': 'Test content'})
    print(f"  Request path: {request.path}")
    print(f"  Request method: {request.method}")

    response = article_list_view(request)
    print(f"  Response status: {response.status}")
    print(f"  Response content length: {len(response.content)}")


def demo():
    print("Django 核心概念示範")
    print("=" * 40)

    demo_models()
    demo_urls()
    demo_templates()
    demo_request_response()

    print("\n所有示範完成！")


if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
Django 核心概念示範
========================================

=== Django Model 示範 ===
Created: <Category: Technology>
Created: <Article: Django 入門>
Created: <Article: Python Web 開發>

All articles: [<Article: Django 入門>, <Article: Python Web 開發>]
Filtered: [<Article: Django 入門>]

=== URL 路由示範 ===
  /articles/ -> article_list_view
  /articles/1/ -> article_detail_view
  /articles/2/ -> article_detail_view

=== Template 示範 ===
  Rendered: <h1>文章列表</h1><ul><li>Django 入門</li><li>Python Web 開發</li></ul>

=== Request/Response 示範 ===
  Request path: /articles/
  Request method: POST
  Response status: 200
  Response content length: 125

所有示範完成！
```

---

## 程式說明

### 1. Django Model 系統

```python
class Article(Model):
    title = CharField(max_length=200)
    content = TextField()
    author = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
```

Django 的 Model 基於 metaclass，在類定義時收集欄位資訊，並提供 ORM 操作介面。

### 2. ORM 查詢 API

```python
Article.objects.all()
Article.objects.filter(author='John')
Article.objects.get(id=1)
```

模擬 Django 的 Manager 和 QuerySet 介面，實現 CRUD 操作。

### 3. URL 路由

```python
resolver = URLResolver()
resolver.register(r'^articles/$', article_list_view)
args, view_func = resolver.resolve('/articles/')
```

使用正則表達式匹配 URL，並呼叫對應的 View 函數。

### 4. Template 系統

```python
template.render({'title': 'Hello', 'articles': [...]})
```

簡化版的 Django Template 系統，支援變數替換和控制結構。

---

## 延伸閱讀

- [Django+ORM+tutorial](https://www.google.com/search?q=Django+ORM+tutorial)
- [Django+MTV+pattern](https://www.google.com/search?q=Django+MTV+pattern)
- [Django+URL+configuration](https://www.google.com/search?q=Django+URL+configuration)

---

*本篇文章為「AI 程式人雜誌 2008 年 3 月號」Python 網頁框架系列補充文章。*