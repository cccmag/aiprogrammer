# Python 網頁框架概覽

## 前言

Python 是最受歡迎的 Web 開發語言之一，擁有從全功能框架到微型框架的完整生態系統。2008 年時，Django 已經確立了其旗艦地位，而 TurboGears 和 Pylons 等框架也各有特色。

## Python Web 框架歷史

### 早期發展

```python
python_web_history = {
    "1999": "Zope 1.0，第一個主流 Python Web 框架",
    "2000": "SkunkWeb, PSP",
    "2002": "Karrigell, Python Paste",
    "2003": "TurboGears 概念形成",
    "2005": "Django 公開發布（Lawrence Journal-World）",
    "2006": "Pylons 專案啟動"
}
```

### 框架分類

```python
framework_categories = {
    "全功能框架": ["Django", "TurboGears", "Zope"],
    "微框架": ["CherryPy", "web.py", "Bottle"],
    "元件框架": ["Pylons", "Repoze"],
    "非同步框架": ["Twisted Web", "Nevow"]
}
```

## Django

### Django 的起源

```python
django_origin = {
    "開發者": "Lawrence Journal-World 報社",
    "時間": "2003-2005",
    "名稱": "來自爵士吉他手 Django Reinhardt",
    "特點": "適合新聞網站和內容管理系統"
}
```

### Django 的哲學

```python
django_philosophy = {
    "MTV 模式": "Model-Template-View",
    "原則": [
        "明確勝於隱晦",
        "簡單勝於複雜",
        "同性質勝於異質"
    ],
    "特點": "內建管理介面、ORM、模板系統"
}
```

### Django 的組成部分

```python
django_components = {
    "ORM": "物件關聯對應",
    "Template": "樣板引擎",
    "URL Router": "網址路由",
    "Admin": "自動管理介面",
    "Forms": "表單處理",
    "Cache": "快取框架",
    "Authentication": "認證系統"
}
```

## TurboGears

### 設計理念

```python
turbogears_design = {
    "概念": "最佳化工具的組合",
    "核心": "CherryKit + MochiKit + SQLAlchemy + Kid",
    "特點": "你可以只使用需要的元件"
}
```

### 元件整合

```python
turbogears_components = {
    "ORM": "SQLAlchemy",
    "Template": "Kid 或 Genshi",
    "JavaScript": "MochiKit",
    "WSGI": "Paste",
    "Microformat": "使用標準而非自訂"
}
```

## Pylons

### 輕量級設計

```python
pylons_philosophy = {
    "目標": "極度的彈性和控制",
    "核心": "Paste + Routes + SQLAlchemy",
    "模板": "可以選擇任何模板系統",
    "適合": "想要自己選擇元件的開發者"
}
```

### 與 Django 的比較

```python
django_vs_pylons = {
    "Django": {
        "哲學": "Batteries included",
        "優點": "快速開發、完整文件",
        "缺點": "預設選擇可能不適合所有情況"
    },
    "Pylons": {
        "哲學": "Provide choices",
        "優點": "彈性、選擇自由",
        "缺點": "需要自己做更多決定"
    }
}
```

## CherryPy

### 微框架的代表

```python
cherrypy_features = {
    "大小": "極簡的核心",
    "功能": "完整的 WSGI 支援",
    "設計": "物件導向的 URL 映射",
    "範例": "以裝飾器定義 URL"
}
```

### CherryPy 範例

```python
import cherrypy

class HelloWorld:
    @cherrypy.expose
    def index(self):
        return "Hello World!"

    @cherrypy.expose
    def greet(self, name):
        return f"Hello {name}!"

cherrypy.quickstart(HelloWorld())
```

## 其他框架

### web.py

```python
webpy_concept = {
    "作者": "Aaron Swartz",
    "哲學": "簡單到不能再簡單",
    "缺點": "社群較小，文件有限"
}
```

### Grok

```python
grok_framework = {
    "基礎": "Zope 3",
    "目標": "降低 Zope 的學習曲線",
    "特點": "基於約定優於設定"
}
```

## 選擇指南

### 根據需求選擇

```python
framework_selection = {
    "內容管理網站": "Django（內建 Admin）",
    "快速原型": "CherryPy, web.py",
    "企業應用": "Django, TurboGears",
    "極度客製化": "Pylons",
    "Zope 愛好者": "Grok"
}
```

### 比較表

| 框架 | 學習曲線 | 彈性 | 生態 | 適合場景 |
|------|----------|------|------|----------|
| Django | 中等 | 中等 | 完整 | CMS、電子商務 |
| TurboGears | 中等 | 高 | 良好 | 資料庫導向應用 |
| Pylons | 陡 | 極高 | 一般 | 自訂需求強的應用 |
| CherryPy | 簡單 | 高 | 較小 | 微服務、API |

## WSGI：連接的標準

### WSGI 的重要性

```python
wsgi_importance = {
    "定義": "Web Server Gateway Interface",
    "好處": "框架和伺服器解耦",
    "影響": "幾乎所有 Python Web 框架都支援 WSGI"
}
```

### WSGI 簡介

```python
# 最簡單的 WSGI 應用

def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)
    return [b'Hello World!']
```

## 模板引擎

### Django Template

```python
django_template = {
    "特點": "簡單的語法，強調分離",
    "缺點": "無法執行任意 Python 程式碼"
}
```

### 其他選擇

```python
template_engines = {
    "Jinja2": "受 Django 啟發，更快",
    "Mako": "非常快，但語法像 PHP",
    "Genshi": "XML 為基礎，適合結構化內容",
    "Kid": "簡單的 XML 模板"
}
```

## 未來展望

### 2008 年後的發展

```python
future_trends = {
    "2009": "Bottle 微框架發布",
    "2010": "Flask 發布，席捲社群",
    "2011": "Django 1.3 Class-based Views",
    "2013": "Django REST framework 崛起"
}
```

---

**延伸閱讀**

- [Python+web+frameworks+comparison](https://www.google.com/search?q=Python+web+frameworks+comparison)
- [Django+vs+Rails](https://www.google.com/search?q=Django+vs+Rails)
- [WSGI+tutorial](https://www.google.com/search?q=WSGI+tutorial)