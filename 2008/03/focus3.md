# MTV 設計模式

## 前言

Django 採用了獨特的 MTV（Model-Template-View）設計模式。這種模式借鑒了 MVC（Model-View-Controller）思想，但有 Django 自己的實現方式。

## MVC vs MTV

### 傳統 MVC 模式

```python
mvc_pattern = {
    "Model": "負責資料和業務邏輯",
    "View": "負責呈現資料給使用者",
    "Controller": "處理請求，調用 Model 和 View"
}

# 網頁 MVC 流程：
# Request → Controller → Model → Controller → View → Response
```

### Django 的 MTV 模式

```python
mtm_pattern = {
    "Model": "負責資料和業務邏輯（相當於 MVC 的 Model）",
    "Template": "負責呈現（相當於 MVC 的 View）",
    "View": "處理請求，選擇 Template（相當於 MVC 的 Controller）"
}

# Django MTV 流程：
# Request → URL Router → View (Controller) → Model → View → Template → Response
```

## Model

### Django ORM

Django 的 Model 層提供了強大的 ORM 功能：

```python
# models.py

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
```

### 模型欄位類型

```python
django_field_types = {
    "CharField": "單行文字",
    "TextField": "多行文字",
    "IntegerField": "整數",
    "FloatField": "浮點數",
    "BooleanField": "布林值",
    "DateTimeField": "日期時間",
    "ForeignKey": "多對一關係",
    "ManyToManyField": "多對多關係",
    "EmailField": "電子郵件",
    "URLField": "URL"
}
```

### 模型 Meta 類別

```python
model_meta_options = {
    "ordering": "預設排序",
    "verbose_name": "人類可讀的名稱",
    "verbose_name_plural": "複數形式",
    "db_table": "自訂資料表名稱",
    "abstract": "是否為抽象類別"
}
```

## View

### Django Views 的角色

在 Django 中，View 是處理請求的函數或類別：

```python
# views.py

from django.http import HttpResponse
from django.shortcuts import render_to_response

def article_list(request):
    # 處理請求邏輯
    articles = Article.objects.all()
    return render_to_response('articles/list.html', {
        'articles': articles
    })
```

### Function-based Views

```python
def my_view(request):
    if request.method == 'GET':
        # 處理 GET 請求
        return HttpResponse('GET')
    elif request.method == 'POST':
        # 處理 POST 請求
        return HttpResponse('POST')
```

### Request 物件

```python
request_attributes = {
    "method": "HTTP 方法（GET, POST）",
    "GET": "GET 參數",
    "POST": "POST 參數",
    "session": "Session 資料",
    "user": "當前使用者",
    "path": "請求的路徑",
    "COOKIES": "Cookie 資料"
}
```

### Response 物件

```python
response_types = {
    "HttpResponse": "基本回應",
    "render_to_response": "渲染模板後回應",
    "redirect": "重新導向",
    "Http404": "404 錯誤"
}
```

## Template

### Django Template 語法

```html
<!-- 變數輸出 -->
{{ variable_name }}

<!-- 標籤 -->
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}

<!-- 條件 -->
{% if user.is_authenticated %}
    Hello, {{ user.username }}!
{% else %}
    Please login.
{% endif %}

<!-- 註釋 -->
{# 這是註釋 #}
```

### 模板標籤

```python
built_in_tags = {
    "for": "迭代",
    "if/elif/else": "條件",
    "include": "包含其他模板",
    "block/extends": "模板繼承",
    "url": "反解析 URL",
    "csrf_token": "CSRF 防護"
}
```

### 模板過濾器

```html
<!-- 過濾器 -->
{{ name|upper }}          {# 大寫 #}
{{ name|lower }}          {# 小寫 #}
{{ name|truncatewords:5 }} {# 截斷 #}
{{ date|date:"Y-m-d" }}   {# 日期格式化 #}
{{ html|safe }}           {# 標記為安全 HTML #}
```

### 模板繼承

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head><title>{% block title %}My Site{% endblock %}</title></head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- child.html -->
{% extends "base.html" %}
{% block title %}Home Page{% endblock %}
{% block content %}
    <p>Welcome!</p>
{% endblock %}
```

## URL 配置

### URL 模式

```python
# urls.py

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    # 簡單視圖
    (r'^articles/$', 'myapp.views.article_list'),
    (r'^articles/(\d+)/$', 'myapp.views.article_detail'),
)
```

### URL 正則表達式

```python
# 命名組
url(r'^articles/(?P<article_id>\d+)/$', 'article_detail')

# 捕獲參數
url(r'^user/(\w+)/$', 'user_profile')
```

### URL 反解析

```python
# 在 Python 程式碼中
from django.core.urlresolvers import reverse

url = reverse('article_detail', args=[1])
# 輸出：'/articles/1/'

# 在模板中
{% url 'article_detail' article.id %}
```

## 請求-回應流程

### 完整流程圖

```
┌─────────────┐
│   Request   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  urls.py    │ ← URL 匹配
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  views.py   │ ← 業務邏輯
│  (View)     │
└──────┬──────┘
       │
       ├──────┐
       │      │
       ▼      ▼
┌─────────┐ ┌─────────┐
│  Model   │ │ Template│
│  資料    │ │  呈現   │
└────┬────┘ └────┬────┘
       │      │
       └──────┘
            │
            ▼
       ┌─────────────┐
       │   Response  │
       └─────────────┘
```

## 實用範例

### CRUD 操作

```python
# views.py

def article_create(request):
    if request.method == 'POST':
        # 建立新文章
        article = Article(
            title=request.POST['title'],
            content=request.POST['content'],
            author=request.user.username
        )
        article.save()
        return redirect('article_detail', article_id=article.id)
    else:
        return render_to_response('articles/create.html')

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render_to_response('articles/detail.html', {
        'article': article
    })

def article_update(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
        return redirect('article_detail', article_id=article.id)
    return render_to_response('articles/edit.html', {
        'article': article
    })

def article_delete(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.delete()
    return redirect('article_list')
```

---

**延伸閱讀**

- [Django+MTV+pattern](https://www.google.com/search?q=Django+MTV+pattern)
- [Django+Views+tutorial](https://www.google.com/search?q=Django+Views+tutorial)
- [Django+Templates](https://www.google.com/search?q=Django+Templates)