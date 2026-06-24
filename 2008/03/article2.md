# WSGI 標準

## 前言

WSGI（Web Server Gateway Interface，PEP 333）是 Python Web 開發中最重要的標準之一。它定義了 Web 伺服器和 Web 應用程式之間的介面，讓不同的伺服器和框架可以互相搭配使用。

## WSGI 的設計目標

### 為何需要 WSGI？

```python
wsgi_design_goals = {
    "簡單性": "易於理解和實作",
    "通用性": "適用於所有 Python Web 框架",
    "可組合性": "支援中介軟體",
    "脫鉤": "伺服器和框架解耦"
}
```

### 簡化示意圖

```
┌────────────────┐      ┌────────────────┐      ┌────────────────┐
│  Web 伺服器   │  WSGI  │  WSGI 應用    │  WSGI  │  Framework     │
│  (Apache,     │◄─────►│  (你自己的     │◄─────►│  (Django,      │
│   nginx)      │        │   WSGI app)    │        │   Flask)       │
└────────────────┘        └────────────────┘        └────────────────┘
```

## WSGI 介面定義

### 應用介面

```python
# WSGI 應用是一個可呼叫物件（函數或類別）

def application(environ, start_response):
    """
    environ: 包含請求資訊的字典
    start_response: 用於開始 HTTP 回應的函數
    """
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return [b'Hello World!']
```

### environ 字典

```python
# environ 包含所有請求資訊

environ_keys = {
    "REQUEST_METHOD": "GET, POST, PUT, DELETE",
    "SCRIPT_NAME": "應用程式的前綴路徑",
    "PATH_INFO": "請求的路徑",
    "QUERY_STRING": "URL 查詢字串",
    "SERVER_NAME": "伺服器名稱",
    "SERVER_PORT": "伺服器埠",
    "HTTP_*": "HTTP 標頭（如 HTTP_USER_AGENT）",
    "wsgi.input": "請求主體的檔案物件",
    "wsgi.errors": "錯誤輸出",
    "wsgi.url_scheme": "http 或 https"
}
```

### start_response

```python
# start_response 函數

def start_response(status, response_headers, exc_info=None):
    """
    status: HTTP 狀態字串，如 '200 OK'
    response_headers: HTTP 標頭列表
    exc_info: 錯誤資訊（可選）
    """
    pass
```

## 最簡單的 WSGI 應用

### Hello World

```python
def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<html><body>Hello, World!</body></html>']
```

### 處理請求參數

```python
def app(environ, start_response):
    # 取得查詢參數
    from urllib.parse import parse_qs

    query = environ.get('QUERY_STRING', '')
    params = parse_qs(query)

    name = params.get('name', ['World'])[0]

    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    start_response(status, headers)

    response = f'<html><body>Hello, {name}!</body></html>'
    return [response.encode('utf-8')]
```

## WSGI 中介軟體

### 什麼是中介軟體？

```python
# 中介軟體同時是伺服器也是應用

class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # 在請求前處理
        environ['middleware_added'] = 'value'

        # 呼叫下一層
        response = self.app(environ, start_response)

        # 在回應後處理
        return response
```

### 常見中介軟體功能

```python
middleware_functions = {
    "Session 管理": "處理使用者 session",
    "認證": "檢查使用者登入狀態",
    "路由": "根據 URL 分發到不同應用",
    "快取": "快取回應結果",
    "除錯": "顯示錯誤資訊"
}
```

## WSGI 伺服器

### 標準的 WSGI 伺服器

```python
wsgi_servers = {
    "wsgiref": "Python 標準庫（僅用於開發）",
    "gunicorn": "Unix 伺服器，生產可用",
    "uwsgi": "高效能，C 實作",
    "mod_wsgi": "Apache 模組"
}
```

### 使用 wsgiref（開發環境）

```python
# wsgiref.simple_server 範例

from wsgiref.simple_server import make_server

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'Hello!']

httpd = make_server('', 8000, app)
print("Serving on port 8000...")
httpd.serve_forever()
```

## Framework 支援

### Django 的 WSGI

```python
# Django 的 wsgi.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
```

### Flask 的 WSGI

```python
# Flask 本身相容 WSGI

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello!'

# Flask 應用本身就是一個 WSGI 應用
```

## 環境變數擴展

### CGI 與 WSGI

```python
# WSGI 源自 CGI，但有所擴展

cgi_to_wsgi = {
    "REQUEST_METHOD": "REQUEST_METHOD (相同)",
    "SCRIPT_NAME": "對應 PATH_INFO 的前綴",
    "PATH_INFO": "對應 REQUEST_URI 的路徑部分",
    "QUERY_STRING": "QUERY_STRING (相同)"
}
```

## 常見模式

### 靜態檔案

```python
import os

def app(environ, start_response):
    path = environ['PATH_INFO'].lstrip('/')

    # 安全的靜態檔案服務
    if '..' in path:
        start_response('403 Forbidden', [])
        return [b'Forbidden']

    full_path = os.path.join('/var/www', path)

    if os.path.isfile(full_path):
        with open(full_path, 'rb') as f:
            start_response('200 OK', [('Content-Type', 'application/octet-stream')])
            return [f.read()]
    else:
        start_response('404 Not Found', [])
        return [b'Not Found']
```

### 簡單路由

```python
routes = {
    '/': 'home',
    '/about': 'about',
    '/contact': 'contact'
}

def app(environ, start_response):
    path = environ['PATH_INFO']

    handler = routes.get(path)
    if handler:
        response = globals()[handler]()
    else:
        start_response('404 Not Found', [])
        response = b'Not Found'

    return response
```

## 錯誤處理

### 異常處理

```python
def app(environ, start_response):
    try:
        # 正常處理
        result = handle_request(environ)

        start_response('200 OK', [('Content-Type', 'text/html')])
        return [result.encode('utf-8')]

    except HTTPException as e:
        start_response(e.status, e.headers)
        return [e.body.encode('utf-8')]

    except Exception as e:
        # 記錄錯誤
        log_error(e)

        start_response('500 Internal Server Error', [])
        return [b'Internal Server Error']
```

---

**延伸閱讀**

- [PEP+333+WSGI+specification](https://www.google.com/search?q=PEP+333+WSGI+specification)
- [WSGI+tutorial](https://www.google.com/search?q=WSGI+tutorial)
- [WSGI+servers+Python](https://www.google.com/search?q=WSGI+servers+Python)