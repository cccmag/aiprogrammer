# Django ORM 資料庫操作

## 前言

Django ORM（Object-Relational Mapping）是 Django 框架的核心功能之一，讓開發者可以用 Python 物件的方式操作資料庫，無需撰寫 SQL。

## 定義模型

### 基本模型

```python
# models.py

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag')

    def __unicode__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
```

### 欄位選項

```python
field_options = {
    "null": "是否允許 NULL",
    "blank": "表單驗證是否允許空白",
    "default": "預設值",
    "verbose_name": "人類可讀的名稱",
    "help_text": "幫助文字"
}

# 範例
name = models.CharField(max_length=100, null=True, blank=True, default='Anonymous')
```

## 建立資料表

### syncdb

```bash
# 同步資料庫
python manage.py syncdb

# 顯示將要執行的 SQL
python manage.py sqlall myapp
```

### SQL 輸出範例

```sql
-- 產生的 SQL（SQLite）

CREATE TABLE myapp_author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(75) NOT NULL
);

CREATE TABLE myapp_article (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES myapp_author(id),
    created_at DATETIME NOT NULL
);
```

## CRUD 操作

### Create（新增）

```python
# 方法 1：建立實例後儲存
author = Author(name='John', email='john@example.com')
author.save()

# 方法 2：使用 create
Author.objects.create(name='Jane', email='jane@example.com')

# 方法 3：使用 get_or_create
author, created = Author.objects.get_or_create(
    email='john@example.com',
    defaults={'name': 'John'}
)
```

### Read（讀取）

```python
# 取得所有物件
all_authors = Author.objects.all()

# 取得單一物件（不存在拋出異常）
author = Author.objects.get(pk=1)

# 取得過濾後的結果
articles = Article.objects.filter(author=author)

# 排除
articles = Article.objects.exclude(status='draft')

# 切片（分頁）
first_five = Article.objects.all()[:5]
```

### Update（更新）

```python
# 更新單一物件
article = Article.objects.get(pk=1)
article.title = 'New Title'
article.save()

# 更新多個物件（使用 update）
Article.objects.filter(author=author).update(status='published')
```

### Delete（刪除）

```python
# 刪除單一物件
article = Article.objects.get(pk=1)
article.delete()

# 刪除多個物件
Article.objects.filter(status='draft').delete()
```

## 查詢運算

### 欄位查詢

```python
# 欄位查詢使用雙底線語法

exact = Article.objects.get(title__exact='Hello')
iexact = Article.objects.get(title__iexact='hello')

contains = Article.objects.filter(content__contains='keyword')
icontains = Article.objects.filter(content__icontains='KEYWORD')

startswith = Article.objects.filter(title__startswith='The')
endswith = Article.objects.filter(title__endswith='!')

gt = Article.objects.filter(id__gt=10)
gte = Article.objects.filter(id__gte=10)
lt = Article.objects.filter(id__lt=10)
lte = Article.objects.filter(id__lte=10)

in_list = Article.objects.filter(id__in=[1, 2, 3])
range_query = Article.objects.filter(id__range=(1, 10))
```

### 日期欄位查詢

```python
# 日期相關查詢

year = Article.objects.filter(created_at__year=2008)
month = Article.objects.filter(created_at__month=3)
day = Article.objects.filter(created_at__day=15)

date = Article.objects.filter(created_at__date=datetime.date(2008, 3, 15))
week_day = Article.objects.filter(created_at__week_day=1)  # 週一
```

### Q 物件（複雜查詢）

```python
from django.db.models import Q

# OR 查詢
Article.objects.filter(
    Q(title__contains='Django') | Q(title__contains='Python')
)

# AND 查詢
Article.objects.filter(
    Q(author='John') & Q(status='published')
)

# NOT 查詢
Article.objects.filter(~Q(status='draft'))
```

## 關聯查詢

### ForeignKey（多對一）

```python
# 正向查詢（從 Article 到 Author）
article = Article.objects.get(pk=1)
author_name = article.author.name

# 反向查詢（從 Author 到 Article）
author = Author.objects.get(pk=1)
articles = author.article_set.all()
```

### ManyToManyField（多對多）

```python
# 新增標籤
article = Article.objects.get(pk=1)
article.tags.add(tag1, tag2)

# 查詢標籤
article_tags = article.tags.all()

# 反向查詢
tag = Tag.objects.get(name='Python')
tagged_articles = tag.article_set.all()
```

## 聚合與註標

### 聚合

```python
from django.db.models import Count, Sum, Avg, Max, Min

# 計數
author_article_count = Author.objects.annotate(
    num_articles=Count('article')
)

# 總和、平均、最大、最小
from django.db.models import Sum
total_views = Article.objects.aggregate(total_views=Sum('views'))
```

### 註標（Annotation）

```python
# 為每個 Author 註標其文章數量
authors = Author.objects.annotate(article_count=Count('article'))

for author in authors:
    print(f"{author.name}: {author.article_count} articles")
```

##  Ordering（排序）

```python
# 排序（預設遞增）
articles = Article.objects.order_by('created_at')

# 遞減排序
articles = Article.objects.order_by('-created_at')

# 多欄位排序
articles = Article.objects.order_by('-created_at', 'title')

# 移除預設排序
articles = Article.objects.order_by()
```

## Manager 和 QuerySet

### QuerySet

```python
# QuerySet 特性

# 延遲執行
queryset = Article.objects.filter(status='published')
# SQL 還沒執行

# 評估（實際執行）
articles = list(queryset)
# SQL 在此時執行

# 可鏈接
articles = Article.objects.filter(
    author__name='John'
).exclude(
    status='draft'
).order_by('-created_at')
```

### Manager

```python
# 每個模型預設有一個 objects Manager

# 自訂 Manager
class PublishedManager(models.Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(status='published')

class Article(models.Model):
    # 預設 Manager
    objects = models.Manager()
    # 自訂 Manager
    published = PublishedManager()
```

---

**延伸閱讀**

- [Django+ORM+tutorial](https://www.google.com/search?q=Django+ORM+tutorial)
- [Django+models+fields](https://www.google.com/search?q=Django+models+fields)
- [Django+queryset+API](https://www.google.com/search?q=Django+queryset+API)