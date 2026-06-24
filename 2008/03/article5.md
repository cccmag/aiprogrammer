# CherryPy 微框架

## 前言

CherryPy 是一個簡潔但功能完整的 Python Web 框架。它以其簡單的 API 和物件導向的設計，成為微型框架的早期代表。

## CherryPy 簡介

### 設計理念

```python
cherrypy_design = {
    "目標": "一個簡單但完整的 HTTP 框架",
    "特點": "物件導向的 URL 映射",
    "大小": "核心很輕量",
    "版本": "2008 年約 3.0 版本"
}
```

### 基本範例

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

## 物件導向 URL 映射

### 基本原則

```python
# CherryPy 的 URL 對應到物件階層

class Root:
    @cherrypy.expose
    def index(self):
        return "Home"

class Blog:
    @cherrypy.expose
    def index(self):
        return "Blog Home"

    @cherrypy.expose
    def view(self, id):
        return f"Viewing article {id}"

class Root:
    blog = Blog()

# URL 映射：
# / → Root.index
# /blog → Root.blog.index
# /blog/view?id=1 → Root.blog.view
```

### 巢狀物件

```python
class Archives:
    @cherrypy.expose
    def index(self, year):
        return f"Archives for {year}"

    def by_month(self, year, month):
        return f"{year}/{month}"

class Blog:
    archives = Archives()

root = Root()
root.blog = Blog()

# /blog/archives/2018 → Archives.index
# /blog/archives/by_month?year=2018&month=3 → Archives.by_month
```

## 請求和回應

### 請求物件

```python
class MyController:
    @cherrypy.expose
    def submit(self):
        # GET 參數
        name = cherrypy.request.params.get('name')

        # POST 參數
        email = cherrypy.request.body.params.get('email')

        # Header
        user_agent = cherrypy.request.headers.get('User-Agent')

        # Cookie
        session_id = cherrypy.request.cookie.get('session_id')

        return f"Received: {name}, {email}"
```

### 回應物件

```python
class MyController:
    @cherrypy.expose
    def example(self):
        # 設定狀態碼
        cherrypy.response.status = 200

        # 設定標頭
        cherrypy.response.headers['Content-Type'] = 'text/html'

        # 設定 Cookie
        cherrypy.response.cookie['session'] = 'abc123'

        return "Example response"
```

## 內建工具

### 函式工具

```python
# CherryPy 提供的工具

@cherrypy.expose
@cherrypy.tools.gzip()
def compressed(self):
    return "This will be compressed!"

@cherrypy.expose
@cherrypy.tools.staticdir(root='static')
def static(self):
    return "Serving static files"
```

### 工具類型

```python
cherrypy_tools = {
    "gzip": "GZIP 壓縮回應",
    "static": "提供靜態檔案",
    "session": "Session 管理",
    "auth": "Basic 和 Digest 認證",
    "caching": "輸出快取"
}
```

## Session 管理

### 啟用 Session

```python
# 設定
cherrypy.config.update({
    'tools.sessions.on': True,
    'tools.sessions.storage_type': 'ram',
    'tools.sessions.timeout': 60
})

@cherrypy.expose
def login(self, username):
    cherrypy.session['username'] = username
    return f"Logged in as {username}"

@cherrypy.expose
def logout(self):
    username = cherrypy.session.get('username')
    cherrypy.session.clear()
    return f"Goodbye {username}"
```

## 錯誤處理

### 自訂錯誤處理

```python
@cherrypy.expose
def error_page(self):
    raise cherrypy.HTTPError(404, "Page not found")

# 或

def error_handler(self):
    return "Custom error page"

# 設定錯誤處理
cherrypy.config.update({
    'error_page.404': error_handler
})
```

## 設定

### 設定檔案

```ini
[global]
server.socket_host = '0.0.0.0'
server.socket_port = 8080
tools.sessions.on = True

[/]
exposed = True

[/api]
exposed = True
tools.gzip.on = True
```

### 多站台設定

```python
class App:
    @cherrypy.expose
    def index(self):
        return "Main Site"

class AdminApp:
    @cherrypy.expose
    def index(self):
        return "Admin Site"

if __name__ == '__main__':
    cherrypy.tree.mount(App(), '/')
    cherrypy.tree.mount(AdminApp(), '/admin')

    cherrypy.engine.start()
    cherrypy.engine.block()
```

## 插件系統

### 使用插件

```python
# 内建插件
from cherrypy.process import plugins

# 資料庫插件
class DatabasePlugin(plugins.Plugin):
    def start(self):
        self.db = connect_to_database()

    def stop(self):
        self.db.disconnect()

db_plugin = DatabasePlugin(cherrypy.engine)
db_plugin.subscribe()
```

## 優點

### CherryPy 的優點

```python
cherrypy_advantages = {
    "簡單": "易於學習和使用",
    "輕量": "核心很小",
    "完整": "內建伺服器、Session、認證",
    "物件導向": "URL 對應很直觀"
}
```

## 缺點

### CherryPy 的缺點

```python
cherrypy_disadvantages = {
    "社群": "比 Django 小",
    "文件": "相對較少",
    "生態": "缺乏 Django 的完整生態"
}
```

## 應用場景

### 適合使用 CherryPy

```python
cherrypy_use_cases = {
    "REST API": "簡單的 API 伺服器",
    "微服務": "輕量的微服務",
    "原型開發": "快速建立原型",
    "嵌入式": "嵌入在其他應用中"
}
```

---

**延伸閱讀**

- [CherryPy+official+site](https://www.google.com/search?q=CherryPy+official+site)
- [CherryPy+tutorial](https://www.google.com/search?q=CherryPy+tutorial)
- [CherryPy+REST+API](https://www.google.com/search?q=CherryPy+REST+API)