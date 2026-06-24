# URL 路由與 Views

## 前言

Django 的 URL 路由系統將網址映射到對應的 Views 處理函數。靈活且清晰的 URL 設計是良好 Web 應用的基礎。

## Django URL 配置

### 基本結構

```python
# mysite/urls.py

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    # 格式：(正則表達式, 視圖函數)
    (r'^$', 'mysite.views.home'),
    (r'^about/$', 'mysite.views.about'),
    (r'^contact/$', 'mysite.views.contact'),
)
```

### 命名 URL

```python
# 定義 URL 時指定名稱
urlpatterns = patterns('',
    url(r'^articles/$', 'myapp.views.article_list', name='article_list'),
    url(r'^articles/(?P<article_id>\d+)/$', 'myapp.views.article_detail', name='article_detail'),
)
```

## URL 正則表達式

### 基本模式

```python
# 簡單匹配
(r'^articles/$', views.article_list)  # 精確匹配 /articles/

# 捕獲參數
(r'^articles/(\d+)/$', views.article_detail)  # 捕獲數字 ID
# 存取：views.article_detail(request, article_id)

# 命名捕獲
(r'^articles/(?P<article_id>\d+)/$', views.article_detail)
# 存取：views.article_detail(request, article_id=article_id)
```

### 常見模式

```python
url_patterns_examples = {
    # 文章詳情：/articles/123/
    r'^articles/(?P<id>\d+)/$',

    # 使用者個人頁面：/user/john/
    r'^user/(?P<username>\w+)/$',

    # 年月結構：/2008/03/
    r'^(?P<year>\d{4})/(?P<month>\d{2})/$',

    # 可選部分：/page(/page)?
    r'^page(/page)?/$',

    # 結尾斜線：/about/ 或 /about（都匹配）
    r'^about/?$',
}
```

## Views 函數

### 基本 View

```python
# views.py

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to my site!")

def article_list(request):
    articles = Article.objects.all()
    html = '<br>'.join([a.title for a in articles])
    return HttpResponse(html)
```

### 請求物件

```python
def example_view(request):
    # HTTP 方法
    method = request.method  # 'GET' 或 'POST'

    # GET 參數
    page = request.GET.get('page', 1)

    # POST 參數
    name = request.POST.get('name', '')

    # 路徑
    path = request.path  # '/articles/'

    # Cookie
    session_id = request.COOKIES.get('sessionid')

    return HttpResponse(f"Method: {method}")
```

### 回應物件

```python
from django.http import HttpResponse, HttpResponseRedirect, Http404

# 基本回應
return HttpResponse("Hello!")

# HTML 回應
return HttpResponse("<html><body>Hello!</body></html>")

# JSON 回應
import json
return HttpResponse(json.dumps({'data': 'value'}), content_type='application/json')

# 重新導向
return HttpResponseRedirect('/articles/')

# 404 錯誤
raise Http404("Article not found")
```

## 類別型 Views

### 簡介

```python
# Django 1.5 之前，類別型 Views 還不支援
# 這裡先介紹函數型 Views

# 函數型 View 是 2008 年 Django 的主流
```

## Template 渲染

### render_to_response

```python
from django.shortcuts import render_to_response
from django.template import RequestContext

def article_list(request):
    articles = Article.objects.all()
    return render_to_response('myapp/article_list.html', {
        'articles': articles
    })
```

### 完整渲染（含 context processors）

```python
from django.shortcuts import render

# Django 1.2+（2009年）支援 render
# render 等同於 render_to_response + RequestContext

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'myapp/article_list.html', {
        'articles': articles
    })
```

### 傳遞資料到模板

```python
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render_to_response('myapp/article_detail.html', {
        'article': article,
        'user': request.user,
        'is_owner': article.author == request.user
    })
```

## 快捷函數

### get_object_or_404

```python
from django.shortcuts import get_object_or_404

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render_to_response('myapp/article_detail.html', {
        'article': article
    })

# 如果 Article 不存在，自動返回 404
```

### get_list_or_404

```python
from django.shortcuts import get_list_or_404

def article_list(request):
    # 如果結果為空，返回 404
    articles = get_list_or_404(Article, status='published')
    return render_to_response('myapp/article_list.html', {
        'articles': articles
    })
```

## 錯誤處理

### 自訂錯誤視圖

```python
# urls.py

handler404 = 'mysite.views.page_not_found'
handler500 = 'mysite.views.server_error'

# views.py

def page_not_found(request):
    return render_to_response('404.html')

def server_error(request):
    return render_to_response('500.html')
```

### HTTP 狀態碼

```python
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden

# 200 OK
return HttpResponse("OK")

# 301 永久轉址
return HttpResponsePermanentRedirect('/new-url/')

# 302 暫時轉址
return HttpResponseRedirect('/temp-url/')

# 403 禁止
return HttpResponseForbidden("Access denied")

# 404 找不到
raise Http404

# 500 伺服器錯誤
# Django 預設處理
```

## 登入和權限

### 登入裝飾器

```python
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    return HttpResponse("This is a protected page.")
```

### 權限檢查

```python
from django.contrib.auth.decorators import permission_required

@permission_required('myapp.can_edit_article')
def edit_article(request):
    return HttpResponse("You can edit articles!")
```

## 實用範例

### 分頁

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def article_list(request):
    article_list = Article.objects.all()
    paginator = Paginator(article_list, 10)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render_to_response('myapp/article_list.html', {
        'articles': articles
    })
```

### 表單處理

```python
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # 處理表單資料
            send_email(form.cleaned_data['email'], form.cleaned_data['message'])
            return HttpResponseRedirect('/thanks/')
    else:
        form = ContactForm()

    return render_to_response('contact.html', {
        'form': form
    })
```

---

**延伸閱讀**

- [Django+URL+configuration](https://www.google.com/search?q=Django+URL+configuration)
- [Django+Views+tutorial](https://www.google.com/search?q=Django+Views+tutorial)
- [Django+request+response](https://www.google.com/search?q=Django+request+response)