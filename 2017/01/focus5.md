# Web 開發框架：Flask、Django 與 Pyramid

## 前言

Python 在 Web 開發領域有著豐富的框架選擇。從微型的 Flask 到全功能的 Django，再到介於兩者之間的 Pyramid，開發者可以根據專案需求選擇最適合的工具。本篇文章比較這三種主流框架的特點和使用場景。

## Flask：微框架的靈活性

### Flask 哲學

Flask 是「微框架」（microframework），核心簡單但擴展性極強：

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/user/<name>')
def greet(name):
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(debug=True)
```

### 模板引擎 Jinja2

Flask 使用 Jinja2 作為模板引擎：

```python
from flask import render_template, request

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
```

```html
<!-- templates/hello.html -->
<!doctype html>
<html>
<head>
    <title>Hello</title>
</head>
<body>
    {% if name %}
        <h1>Hello, {{ name }}!</h1>
    {% else %}
        <h1>Hello, World!</h1>
    {% endif %}
</body>
</html>
```

### 表單處理

```python
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

class MyForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = MyForm()
    if form.validate_on_submit():
        return f'Hello, {form.name.data}!'
    return render_template('form.html', form=form)
```

### RESTful API

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {'id': 1, 'title': 'Buy groceries', 'done': False},
    {'id': 2, 'title': 'Learn Python', 'done': True},
]

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'done': False
    }
    tasks.append(task)
    return jsonify(task), 201
```

## Django：全功能框架

### Django 哲學

Django 強調「含Battery included」——開箱即用，包含 ORM、管理後台、表單處理等：

```python
# myproject/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase.db',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]
```

### 模型定義

```python
# blog/models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', args=[str(self.id)])
```

### 視圖與 URL

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
```

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
```

### Django Admin

Django 強大的管理後台只需要很少的程式碼：

```python
# blog/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content')
    list_filter = ('published_date', 'author')
```

## Pyramid：中型應用的選擇

### Pyramid 哲學

Pyramid 介於 Flask 和 Django 之間，適合中型應用：

```python
# development.ini
from wsgiref.simple_server import make_server
from pyramid.config import Configurator

def hello_world(request):
    return Response('Hello World!')

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/')
    config.add_view(hello_world, route_name='hello')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
```

## 框架比較

| 特性 | Flask | Django | Pyramid |
|------|-------|--------|--------|
| 規模 | 微框架 | 全功能框架 | 中型框架 |
| ORM | 需要另外安裝 | 內建 | 需要另外安裝（SQLAlchemy）|
| Admin | 需要另外安裝 | 內建 | 無（可用 pt附加件）|
| 靈活性 | 極高 | 中等 | 高 |
| 學習曲線 | 低 | 中等 | 中等 |
| 適合專案 | 小型 API、原型 | 大型 Web 應用 | 中型應用 |

### 如何選擇？

```python
# 小型專案、API、微服務 → Flask
# 特點：簡單、靈活、擴展性強

# 大型 Web 應用、電子商務平台 → Django
# 特點：內建功能完整、ORM 強大、管理後台

# 中型應用、需要 SQLAlchemy → Pyramid
# 特點：靈活但有結構、社群穩定
```

## 結論

Python 的 Web 框架生態系非常豐富：

- **Flask** 適合快速開發小型應用和 API，學習曲線平緩
- **Django** 適合大型專案，強調「開箱即用」
- **Pyramid** 適合中型應用，需要更多控制但不想從頭建構

選擇框架時，應根據專案規模、團隊經驗和長期維護需求來綜合考量。

---

## 延伸閱讀

- [Flask 官方文檔](https://www.google.com/search?q=Flask+Python+tutorial+web+development)
- [Django 官方文檔](https://www.google.com/search?q=Django+tutorial+Python+web+framework)
- [Pyramid 官方文檔](https://www.google.com/search?q=Pyramid+Python+web+framework)
- [Python+Web+框架+比較](https://www.google.com/search?q=Python+web+framework+comparison+2017)

---

*本篇文章為「AI 程式人雜誌 2017 年 1 月號」焦點系列之一。*