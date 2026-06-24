# Python Web 歷史

## 前言

Python 在 Web 開發領域有著悠久的歷史。從早期的 CGI 腳本到現代的 WSGI 標準，Python Web 技術經歷了多次演進。

## CGI 時代（1990 年代）

### 最早的 Web 互動

1990 年代，Python 透過 CGI（Common Gateway Interface）與 Web 伺服器互動：

```python
# 典型的 CGI 腳本

#!/usr/bin/env python
import cgi

print("Content-Type: text/html")
print()
print("<html><body>")
print("<h1>Hello, World!</h1>")
print("</body></html>")
```

### CGI 的問題

```python
cgi_problems = {
    "效能": "每個請求都啟動新程序",
    "可擴展性": "大量請求時效能嚴重下降",
    "狀態管理": "無內建 session 支援",
    "安全": "容易有安全漏洞"
}
```

## Web 伺服器 API

### 早期解決方案

```python
# mod_python（Apache 模組）
# 讓 Python 直接在 Apache 中執行

# 優點：
# - 比 CGI 快
# - 可存取 Apache 功能

# 缺點：
# - 與 Apache 緊密耦合
# - 已經停止維護
```

## WSGI 的誕生

### PEP 333：Python Web Server Gateway Interface

2003 年，PEP 333 定義了 WSGI 標準：

```python
# WSGI 介面定義

def app(environ, start_response):
    """最簡單的 WSGI 應用"""
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)
    return [b'Hello World!']
```

### WSGI 的好處

```python
wsgi_benefits = {
    "標準化": "統一的介面，所有框架支援",
    "可交換性": "可以輕鬆更換 Web 伺服器",
    "可測試性": "應用可以在命令列測試",
    "中介軟體": "可以在伺服器和應用之間插入中介軟體"
}
```

## 早期框架

### 2000-2003 年的框架

```python
early_frameworks = {
    "SkunkWeb": "模板為中心",
    "Karrigell": "簡單易用",
    " spyce": "在 HTML 中嵌 Python",
    "Quixote": "早期大型框架之一"
}
```

### Zope

```python
zope_info = {
    "建立": "1998 年",
    "特點": "完整的企業級 CMS",
    "ZODB": "物件導向資料庫",
    "複雜度": "學習曲線陡"
}
```

## Django 的崛起

### 2005 年 Django 公開

```python
django_impact = {
    "來源": "Lawrence Journal-World 報社",
    "發布": "2005 年 7 月（BSD 授權）",
    "特點": "MTV 模式、ORM、管理介面",
    "文件": "完整的文件系統"
}
```

### Django 的影響

Django 確立了 Python Web 開發的標準：
- 明確的專案結構
- ORM 作為核心元件
- 自動產生的管理介面
- URL 配置系統

## TurboGears

### 元件整合框架

```python
turbogears_concept = {
    "出現": "2005 年",
    "哲學": "最佳工具的組合",
    "元件": "SQLAlchemy, Genshi, MochiKit",
    "優點": "可替換元件"
}
```

## 2008 年的框架生態

### 全功能框架

```python
full_stack_2008 = {
    "Django": "MTV 模式， ORM， admin",
    "TurboGears": "元件整合，可擴展",
    "Pylons": "極度彈性， WSGI 優先"
}
```

### 微框架

```python
microframeworks_2008 = {
    "CherryPy": "簡單的物件導向框架",
    "web.py": "極簡主義，程式碼行數少",
    "Bottle": "尚未發布（2009 年）"
}
```

## 模板引擎

### 各類模板系統

```python
template_engines = {
    "Django Template": "簡單安全，分離設計",
    "Mako": "非常快，類似 PHP",
    "Jinja2": "受 Django 啟發，更快",
    "Genshi": "XML 為基礎",
    "Kid": "簡單的 XML 模板"
}
```

## 資料庫 ORM

### SQLAlchemy 的地位

```python
sqlalchemy_status = {
    "建立": "2006 年",
    "設計": "SQL toolkit + ORM",
    "應用": "TurboGears, Pylons 的預設 ORM",
    "特點": "靈活，支援原生 SQL"
}
```

## 未來展望

### 即將到來的變化

```python
upcoming_changes = {
    "2008-09": "Django 1.0 發布",
    "2009": "Flask 發布（微型框架新選擇）",
    "2010": " Pyramid 1.0（Pylons 內核）",
    "2012": "Django 1.4 發布"
}
```

### 雲端和 API

```python
future_directions = {
    "雲端部署": "GAE 支援 Python",
    "REST API": " Django REST framework",
    "即時功能": " WebSocket 支援"
}
```

---

**延伸閱讀**

- [Python+web+history](https://www.google.com/search?q=Python+web+history)
- [CGI+Python+web](https://www.google.com/search?q=CGI+Python+web)
- [Django+history+2008](https://www.google.com/search?q=Django+history+2008)