# CSRF 跨站請求偽造

## CSRF 原理

當使用者在已登入的狀態下訪問惡意網站時，該網站可以強制使用者的瀏覽器向目標網站發送請求。由於瀏覽器會自動攜帶目標網站的 Cookie，請求會被視為合法。

```
1. 使用者登入 example.com，伺服器設定 Session Cookie
2. 使用者訪問 evil.com
3. evil.com 的頁面包含：<img src="https://example.com/api/transfer?to=hacker&amount=10000">
4. 瀏覽器發送請求到 example.com，自動攜帶 Session Cookie
5. example.com 收到請求，以為是使用者本人操作，執行轉帳
```

## 同步器 Token 模式

最廣泛使用的 CSRF 防護機制：

### 伺服器端產生 Token

```python
import secrets

@app.route('/form')
def show_form():
    # 產生 CSRF Token
    token = secrets.token_urlsafe(32)
    session['csrf_token'] = token
    return render_template('form.html', token=token)
```

### 在表單中包含 Token

```html
<form method="POST" action="/submit">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  <!-- 其他表單欄位 -->
  <button type="submit">提交</button>
</form>
```

### 驗證 Token

```python
from flask import session, request, abort

@app.route('/submit', methods=['POST'])
def submit():
    token = session.get('csrf_token')
    if not token or token != request.form.get('csrf_token'):
        abort(403)
    # 處理請求...
```

## 客製化 Header 驗證

由於跨域請求無法設定自定義 Header，可以使用這個特性：

```javascript
// 客戶端發送請求時加入自定義 Header
fetch('/api/data', {
    method: 'POST',
    headers: {
        'X-CSRF-Token': csrfToken,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
```

```python
@app.route('/api/data', methods=['POST'])
def api_data():
    token = session.get('csrf_token')
    if not token or token != request.headers.get('X-CSRF-Token'):
        abort(403)
```

## SameSite Cookie

現代瀏覽器支援 SameSite Cookie，可以完全阻止 CSRF：

```python
# Flask 設定 SameSite Cookie
resp.set_cookie('session_id', session_id, samesite='Strict')
```

- `Strict`：完全阻止跨站請求
- `Lax`：允許導航請求（如點擊連結），但阻止其他跨站 POST 請求
- `None`：不限制（需配合 HTTPS 與 Secure）

## 雙重送出 Cookie

另一種不需要伺服器儲存 Token 的方法：

```python
# 伺服器產生 Token 並設定到 Cookie 中
resp.set_cookie('csrf_token', token)

# 客戶端從 Cookie 讀取並在請求中發送
fetch('/api/submit', {
    headers: {
        'X-CSRF-Token': getCookie('csrf_token')
    }
})

# 伺服器比較 Cookie 和請求參數中的 Token
```

## AJAX 請求的 CSRF 防護

```javascript
// 在每個 AJAX 請求中包含 CSRF Token
function csrfSafeMethod(method) {
    return /^(GET|HEAD|OPTIONS)$/.test(method);
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !settings.crossDomain) {
            xhr.setRequestHeader('X-CSRF-Token', csrfToken);
        }
    }
});
```

## 驗證 Referer Header

檢查請求的來源：

```python
@app.before_request
def check_referer():
    if request.method == 'POST':
        if request.referrer and not request.referrer.startswith(request.host_url):
            abort(403)
```

不過攻擊者可以操控 Referer，所以不建議作為唯一的防護手段。

## 密鑰確認

對於重要操作，要求使用者重新輸入密碼或確認操作：

```python
@app.route('/transfer', methods=['POST'])
def transfer():
    if not session.get('confirmed'):
        return redirect('/confirm_transfer')
    # 執行轉帳...
```

## 常用框架的 CSRF 防護

```python
# Flask-WTF（推薦）
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# Django（內建，需開啟）
# settings.py 中新增 'django.middleware.csrf.CsrfViewMiddleware'
```

## 參考資源

- https://www.google.com/search?q=CSRF+跨站請求偽造+防護+Token+SameSite+Cookie+2016
- https://www.google.com/search?q=CSRF+Synchronizer+Token+雙重送出+Cookie+原理+實現
- https://www.google.com/search?q=Flask+CSRF+防護+Flask-WTF+設定+驗證+範例