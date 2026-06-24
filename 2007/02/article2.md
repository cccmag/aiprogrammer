# Django 0.96：Python Web 框架成熟

## 前言

Django 在 2007 年持續發展，版本 0.96 展示了這個 Python Web 框架的成熟。

## Django 的設計哲學

```python
# Django 核心原則
DJANGO_PHILOSOPHY = {
    "MTV 模式": "Model-Template-View",
    "DRY": "Don't Repeat Yourself",
    "快速開發": "Convention over Configuration",
    "元件完整": "ORM、表單、管理介面"
}
```

## Django 0.96 的功能

```python
# Django ORM 範例
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)

# 查詢
books = Book.objects.filter(author__name__contains='John')
```

## 結論

Django 0.96 展示了 Python 在 Web 開發領域的成熟，为日後 Python Web 生態的繁榮奠定基礎。

---

*本篇文章為「AI 程式人雜誌 2007 年 2 月號」文章集錦系列。*