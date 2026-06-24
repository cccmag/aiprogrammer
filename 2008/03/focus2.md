# Django 入門

## 前言

Django 是 Python 最受歡迎的全功能 Web 框架。它讓開發者能夠快速建立安全、維護性高的 Web 應用。讓我們從零開始學習 Django。

## 安裝 Django

### 需求環境

```python
django_requirements = {
    "Python": "2.3 或更高",
    "資料庫": "SQLite（內建）、PostgreSQL、MySQL、Oracle",
    "作業系統": "Windows、Linux、Mac OS X"
}
```

### 安裝步驟

```bash
# 使用 easy_install（2008 年的方式）
easy_install Django

# 或使用 pip（後來成為主流）
pip install Django

# 或從原始碼安裝
tar xzf Django-0.96.tar.gz
cd Django-0.96
python setup.py install
```

### 驗證安裝

```python
# 在 Python 直譯器中
import django
print(django.VERSION)  # (0, 96, 1, 'final', 0)
```

## 建立第一個 Django 專案

### django-admin.py

```bash
# 建立新專案
django-admin.py startproject mysite

# 專案結構
# mysite/
# ├── manage.py          # 管理腳本
# └── mysite/
#     ├── __init__.py
#     ├── settings.py     # 設定檔
#     ├── urls.py         # URL 配置
#     └── wsgi.py         # WSGI 入口
```

### 專案目錄結構

```python
project_structure = {
    "manage.py": "管理命令指令碼",
    "settings.py": "Django 設定",
    "urls.py": "URL 到 View 的映射",
    "wsgi.py": "WSGI 應用程式入口"
}
```

## Django 設定

### settings.py 基本設定

```python
# settings.py 核心設定

DEBUG = True  # 開發環境設為 True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # 生產環境需設定

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mysite.db',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    # 加入自己的 app
    'myapp',
]

SECRET_KEY = 'your-secret-key-here'
```

### 啟動開發伺服器

```bash
# 啟動開發伺服器
python manage.py runserver

# 指定埠號
python manage.py runserver 8080

# 允許外部存取
python manage.py runserver 0.0.0.0:8000
```

## 建立 Django App

### App 與專案的區別

```python
app_vs_project = {
    "專案 (Project)": "整個網站設定",
    "應用程式 (App)": "特定功能的模組"
}

# 一個專案可以包含多個應用
# 一個應用可以屬於多個專案
```

### 建立 App

```bash
# 建立新的 app
python manage.py startapp myapp

# 結構：
# myapp/
# ├── __init__.py
# ├── models.py       # 資料模型
# ├── views.py       # 視圖函數
# └── tests.py       # 測試
```

## Django 的 URL 配置

### urls.py

```python
# mysite/urls.py

from django.conf.urls import patterns, include

urlpatterns = patterns('',
    # 首頁
    (r'^$', 'mysite.views.home'),

    # 包含 myapp 的 URL
    (r'^myapp/', include('myapp.urls')),
)
```

## 第一個 View

### views.py

```python
# mysite/views.py

from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response

def home(request):
    return HttpResponse("Hello, World!")

def about(request):
    return HttpResponse("About page")

def current_datetime(request):
    from datetime import datetime
    now = datetime.now()
    html = f"<html><body>It is now {now}.</body></html>"
    return HttpResponse(html)
```

## 使用模板

### 建立模板目錄

```python
# 在專案根目錄建立 templates/
# templates/
# └── myapp/
#     └── index.html
```

### 渲染模板

```python
# mysite/views.py

from django.shortcuts import render_to_response

def index(request):
    return render_to_response('myapp/index.html', {
        'title': 'My App',
        'message': 'Hello from Django!'
    })
```

### 模板語法

```html
<!-- templates/myapp/index.html -->
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
</body>
</html>
```

## Django 管理介面

### 啟動 Admin

```python
# settings.py
INSTALLED_APPS 包含 'django.contrib.admin'
# settings.py
# 設定 MIDDLEWARE_CLASSES 包含相關 Middleware
```

### 建立超級使用者

```bash
python manage.py createsuperuser
```

### 註冊模型到 Admin

```python
# myapp/admin.py

from django.contrib import admin
from myapp.models import Article

admin.site.register(Article)
```

## Django 的開發流程

### 開發步驟

```python
django_development_steps = {
    "1. 定義模型": "在 models.py 中定義資料模型",
    "2. 建立資料表": "python manage.py sqlall + python manage.py syncdb",
    "3. 撰寫 Views": "在 views.py 中實作業務邏輯",
    "4. 配置 URL": "在 urls.py 中設定路由",
    "5. 設計模板": "建立 HTML 模板",
    "6. 測試": "python manage.py test"
}
```

## 資料庫同步

### syncdb 命令

```bash
# 創建資料表
python manage.py syncdb

# 選項：
# --noinput：不詢問任何問題
# --database：指定資料庫
```

### 遷移（2008 年的方式）

```python
# 2008 年 Django 還沒有正式的遷移系統
# 使用 south 等第三方工具

# 或手動：
# python manage.py sqlall myapp  # 查看 SQL
# 手動執行 SQL 來更新資料庫
```

## 常用命令

### manage.py 命令

```python
manage_commands = {
    "runserver": "啟動開發伺服器",
    "syncdb": "同步資料庫",
    "sqlall": "顯示 SQL 語句",
    "shell": "進入 Django shell",
    "test": "執行測試",
    "startapp": "建立新 app",
    "startproject": "建立新專案",
    "dbshell": "進入資料庫命令列"
}
```

---

**延伸閱讀**

- [Django+official+tutorial](https://www.google.com/search?q=Django+official+tutorial)
- [Django+installation+guide](https://www.google.com/search?q=Django+installation+guide)
- [Django+quick+start](https://www.google.com/search?q=Django+quick+start)