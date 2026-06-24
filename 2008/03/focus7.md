# Django 實戰：建立部落格

## 前言

讓我們用 Django 建立一個簡單的部落格系統，涵蓋模型設計、Views 實作和模板建立。

## 專案規劃

### 功能需求

```python
blog_features = {
    "文章列表": "顯示所有已發布的文章",
    "文章詳情": "顯示單篇文章內容",
    "文章管理": "新增、編輯、刪除文章",
    "分類功能": "按分類檢視文章",
    "標籤功能": "為文章添加標籤"
}
```

### 資料模型

```python
# blog/models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '分類'
        verbose_name_plural = '分類'

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已發布'),
    )

    title = models.CharField('標題', max_length=200)
    slug = models.SlugField('網址別名', unique_for_date='publish')
    author = models.CharField('作者', max_length=100)
    category = models.ForeignKey(Category, verbose_name='分類')
    tags = models.ManyToManyField(Tag, verbose_name='標籤')
    content = models.TextField('內容')
    status = models.CharField('狀態', max_length=10,
                              choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField('發布時間')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-publish',)
        verbose_name = '文章'
        verbose_name_plural = '文章'
```

## URL 配置

### blog/urls.py

```python
# blog/urls.py

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('blog.views',
    url(r'^$', 'article_list', name='article_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'article_list_by_date',
        name='article_list_by_date'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        'article_detail', name='article_detail'),
    url(r'^create/$', 'article_create', name='article_create'),
    url(r'^(?P<id>\d+)/edit/$', 'article_edit', name='article_edit'),
    url(r'^(?P<id>\d+)/delete/$', 'article_delete', name='article_delete'),
)
```

## Views 實作

### blog/views.py

```python
# blog/views.py

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext

from blog.models import Article, Category, Tag

def article_list(request):
    """文章列表"""
    articles = Article.objects.filter(status='published')
    paginator = Paginator(articles, 10)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        articles = paginator.page(1)

    return render_to_response('blog/article_list.html', {
        'articles': articles,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    })

def article_detail(request, year, month, slug):
    """文章詳情"""
    article = get_object_or_404(
        Article,
        publish__year=int(year),
        publish__month=int(month),
        slug=slug,
        status='published'
    )

    return render_to_response('blog/article_detail.html', {
        'article': article,
        'categories': Category.objects.all(),
    })

def article_create(request):
    """新增文章"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author', 'Anonymous')
        category_id = request.POST.get('category')

        category = get_object_or_404(Category, pk=category_id)

        article = Article.objects.create(
            title=title,
            content=content,
            author=author,
            category=category,
            status='published',
            publish=datetime.now()
        )

        return HttpResponseRedirect(
            f'/blog/{article.publish.year}/{article.publish.month}/{article.slug}/'
        )

    return render_to_response('blog/article_form.html', {
        'categories': Category.objects.all(),
        'action': 'create'
    })

def article_edit(request, id):
    """編輯文章"""
    article = get_object_or_404(Article, pk=id)

    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.save()
        return HttpResponseRedirect(
            f'/blog/{article.publish.year}/{article.publish.month}/{article.slug}/'
        )

    return render_to_response('blog/article_form.html', {
        'article': article,
        'categories': Category.objects.all(),
        'action': 'edit'
    })

def article_delete(request, id):
    """刪除文章"""
    article = get_object_or_404(Article, pk=id)
    article.delete()
    return HttpResponseRedirect('/blog/')
```

## 模板建立

### base.html

```html
<!-- templates/blog/base.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{% block title %}My Blog{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        header { border-bottom: 2px solid #333; margin-bottom: 20px; }
        article { margin-bottom: 30px; }
        footer { border-top: 1px solid #ccc; margin-top: 40px; padding-top: 10px; }
        .meta { color: #666; font-size: 0.9em; }
        .category { background: #eee; padding: 2px 8px; }
    </style>
</head>
<body>
    <header>
        <h1><a href="/blog/">My Blog</a></h1>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2008 My Blog</p>
    </footer>
</body>
</html>
```

### article_list.html

```html
<!-- templates/blog/article_list.html -->
{% extends "blog/base.html" %}

{% block title %}文章列表{% endblock %}

{% block content %}
    <h2>文章列表</h2>

    {% for article in articles.object_list %}
        <article>
            <h3>
                <a href="/blog/{{ article.publish|date:'Y' }}/{{ article.publish|date:'m' }}/{{ article.slug }}/">
                    {{ article.title }}
                </a>
            </h3>
            <div class="meta">
                作者：{{ article.author }} |
                分類：<span class="category">{{ article.category }}</span> |
                發布：{{ article.publish|date:'Y-m-d' }}
            </div>
            <p>{{ article.content|truncatewords:50 }}</p>
        </article>
    {% empty %}
        <p>暫無文章。</p>
    {% endfor %}

    <!-- 分頁導航 -->
    {% if articles.has_other_pages %}
        <div class="pagination">
            {% if articles.has_previous %}
                <a href="?page={{ articles.previous_page_number }}">&laquo; 上一頁</a>
            {% endif %}

            <span>第 {{ articles.number }} 頁 / 共 {{ articles.paginator.num_pages }} 頁</span>

            {% if articles.has_next %}
                <a href="?page={{ articles.next_page_number }}">下一頁 &raquo;</a>
            {% endif %}
        </div>
    {% endif %}
{% endblock %}
```

### article_detail.html

```html
<!-- templates/blog/article_detail.html -->
{% extends "blog/base.html" %}

{% block title %}{{ article.title }}{% endblock %}

{% block content %}
    <article>
        <h2>{{ article.title }}</h2>
        <div class="meta">
            作者：{{ article.author }} |
            分類：{{ article.category }} |
            發布：{{ article.publish|date:'Y-m-d H:i' }}
        </div>

        {% if article.tags.all %}
        <div class="tags">
            標籤：
            {% for tag in article.tags.all %}
                <span>{{ tag.name }}</span>
            {% endfor %}
        </div>
        {% endif %}

        <div class="content">
            {{ article.content|linebreaks }}
        </div>
    </article>

    <div class="actions">
        <a href="/blog/{{ article.id }}/edit/">編輯</a> |
        <a href="/blog/{{ article.id }}/delete/" onclick="return confirm('確定要刪除？')">刪除</a> |
        <a href="/blog/">返回列表</a>
    </div>
{% endblock %}
```

### article_form.html

```html
<!-- templates/blog/article_form.html -->
{% extends "blog/base.html" %}

{% block title %}{% if action == 'create' %}新增文章{% else %}編輯文章{% endif %}{% endblock %}

{% block content %}
    <h2>{% if action == 'create' %}新增文章{% else %}編輯文章{% endif %}</h2>

    <form method="post" action="">
        {% csrf_token %}

        <p>
            <label>標題：</label><br>
            <input type="text" name="title" value="{{ article.title|default:'' }}" required size="60">
        </p>

        <p>
            <label>作者：</label><br>
            <input type="text" name="author" value="{{ article.author|default:'' }}" required>
        </p>

        <p>
            <label>分類：</label><br>
            <select name="category">
                {% for cat in categories %}
                    <option value="{{ cat.id }}"
                        {% if article.category_id == cat.id %}selected{% endif %}>
                        {{ cat.name }}
                    </option>
                {% endfor %}
            </select>
        </p>

        <p>
            <label>內容：</label><br>
            <textarea name="content" rows="15" cols="60" required>{{ article.content|default:'' }}</textarea>
        </p>

        <p>
            <button type="submit">儲存</button>
            <a href="/blog/">取消</a>
        </p>
    </form>
{% endblock %}
```

## 管理介面

### blog/admin.py

```python
# blog/admin.py

from django.contrib import admin
from blog.models import Article, Category, Tag

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'publish')
    list_filter = ('status', 'category', 'publish')
    search_fields = ('title', 'content')
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
```

---

**延伸閱讀**

- [Django+blog+tutorial](https://www.google.com/search?q=Django+blog+tutorial)
- [Django+pagination](https://www.google.com/search?q=Django+pagination)
- [Django+admin+tutorial](https://www.google.com/search?q=Django+admin+tutorial)