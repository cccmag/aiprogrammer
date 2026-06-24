# Templates 樣板系統

## 前言

Django 的模板系統將 Python 程式碼與 HTML 呈現分離，讓設計師和開發者可以協作工作，同時保持程式碼的整潔。

## 模板引擎設定

### 設定

```python
# settings.py

TEMPLATE_DIRS = (
    '/path/to/templates',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
)
```

## 基本語法

### 變數輸出

```html
<!-- 輸出變數 -->
{{ variable_name }}

<!-- 巢狀屬性 -->
{{ article.author.name }}

<!-- 字典查詢 -->
{{ dict.key }}

<!-- 陣列索引 -->
{{ list.0 }}
```

### 標籤

```html
<!-- 控制結構 -->
{% if user.is_authenticated %}
    Hello, {{ user.username }}!
{% else %}
    <a href="/login/">Login</a>
{% endif %}

<!-- 迴圈 -->
{% for item in items %}
    <li>{{ item }}</li>
{% empty %}
    <li>No items</li>
{% endfor %}

<!-- 註解 -->
{% comment %}
    這是多行註解
{% endcomment %}

{# 這是單行註解 #}
```

## 常用標籤

### if/else

```html
{% if condition %}
    <p>Condition is true</p>
{% elif condition2 %}
    <p>Condition2 is true</p>
{% else %}
    <p>Both are false</p>
{% endif %}

<!-- 比較運算 -->
{% if value > 10 %}
    Greater than 10
{% endif %}

<!-- 邏輯運算 -->
{% if user.is_authenticated and user.is_staff %}
    Admin area
{% endif %}
```

### for 迴圈

```html
<!-- 基本迴圈 -->
{% for article in articles %}
    <h2>{{ article.title }}</h2>
    <p>{{ article.summary }}</p>
{% endfor %}

<!-- 迴圈變數 -->
{% for article in articles %}
    <!-- forloop.counter: 1-indexed 計數 -->
    {{ forloop.counter }}. {{ article.title }}
    <!-- forloop.counter0: 0-indexed 計數 -->
    <!-- forloop.first: 是否為第一個 -->
    <!-- forloop.last: 是否為最後一個 -->
    <!-- forloop.revcounter: 反向計數 -->
{% endfor %}

<!-- empty 處理 -->
{% for article in articles %}
    {{ article.title }}
{% empty %}
    <p>No articles found.</p>
{% endfor %}
```

### 處理時間

```html
<!-- now 標籤 -->
{% now "Y" %}  <!-- 輸出：2025 -->
{% now "F j, Y" %}  <!-- 輸出：January 15, 2025 -->
```

## 過濾器

### 語法

```html
{{ variable|filter_name }}
{{ variable|filter1|filter2 }}
{{ variable|filter:"arg" }}
```

### 常用過濾器

```html
<!-- 字串處理 -->
{{ name|upper }}
{{ name|lower }}
{{ name|title }}
{{ text|truncatewords:20 }}
{{ text|truncatechars:50 }}

<!-- 日期格式化 -->
{{ date|date:"Y-m-d" }}
{{ date|date:"F j, Y" }}

<!-- 預設值 -->
{{ value|default:"N/A" }}

<!-- 長さ -->
{{ items|length }}

<!-- 判斷空 -->
{{ value|yesno:"Yes,No,Maybe" }}

<!-- 轉義 -->
{{ html|safe }}
{{ html|escape }}
```

## 模板繼承

### Base 模板

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
    {% block extra_head %}{% endblock %}
</head>
<body>
    <header>
        {% block header %}
            <h1>My Site</h1>
        {% endblock %}
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        {% block footer %}
            <p>&copy; 2008 My Site</p>
        {% endblock %}
    </footer>
</body>
</html>
```

### 繼承模板

```html
<!-- article.html -->
{% extends "base.html" %}

{% block title %}{{ article.title }} - My Site{% endblock %}

{% block content %}
    <article>
        <h1>{{ article.title }}</h1>
        <div class="meta">
            By {{ article.author }} on {{ article.created_at|date:"F j, Y" }}
        </div>
        <div class="body">
            {{ article.content }}
        </div>
    </article>
{% endblock %}
```

## 包含標籤

### include

```html
<!-- 包含另一個模板 -->
{% include "myapp/article_item.html" %}

<!-- 傳遞上下文 -->
{% include "myapp/article_item.html" with article=current_article %}
```

### include 範例

```html
<!-- article_item.html -->
<div class="article-item">
    <h3><a href="/articles/{{ article.id }}/">{{ article.title }}</a></h3>
    <p>{{ article.summary }}</p>
</div>

<!-- 使用時 -->
{% for article in articles %}
    {% include "myapp/article_item.html" %}
{% endfor %}
```

## 載入靜態檔案

### STATIC_URL

```html
<!-- 載入 CSS -->
<link rel="stylesheet" href="{{ STATIC_URL }}css/style.css">

<!-- 載入 JavaScript -->
<script src="{{ STATIC_URL }}js/jquery.js"></script>

<!-- 載入圖片 -->
<img src="{{ STATIC_URL }}images/logo.png">
```

### load staticfiles

```html
{% load staticfiles %}

<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}">
```

## 自訂過濾器和標籤

### 自訂過濾器

```python
# myapp/templatetags/my_filters.py

from django import template

register = template.Library()

@register.filter
def markdown(value):
    # 簡單的 markdown 轉換
    return value.replace('**', '<strong>').replace('**', '</strong>')

@register.filter(name='truncate_words')
def truncate_words(value, arg):
    words = value.split()
    return ' '.join(words[:int(arg)])
```

### 使用自訂過濾器

```html
{% load my_filters %}

{{ text|markdown }}
{{ text|truncate_words:20 }}
```

### 自訂標籤

```python
# myapp/templatetags/my_tags.py

from django import template

register = template.Library()

@register.simple_tag
def current_year():
    import datetime
    return datetime.datetime.now().year

@register.inclusion_tag('myapp/item_list.html')
def show_items(items):
    return {'items': items}
```

## Template載入器

```python
# 自訂模板載入器

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'myapp.template_loader.DatabaseLoader',  # 自訂
)
```

## 樣板除錯

### 錯誤訊息

Django 的錯誤頁面會顯示：
- 例外類型
- 堆疊追蹤
- 模板名稱和行號
- 附近的模板程式碼

### 常用除錯技巧

```html
<!-- 印出所有變數 -->
{% for var in request %}
    {{ var }}: {{ request.var }}
{% endfor %}

<!-- 使用 {% debug %} 標籤 -->
{% debug %}
```

---

**延伸閱讀**

- [Django+Template+tutorial](https://www.google.com/search?q=Django+Template+tutorial)
- [Django+template+tags](https://www.google.com/search?q=Django+template+tags)
- [Django+template+inheritance](https://www.google.com/search?q=Django+template+inheritance)