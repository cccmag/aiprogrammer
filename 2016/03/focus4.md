# 4. 常見漏洞與防護

## 緩衝區溢位

緩衝區溢位是經典的記憶體安全問題。當寫入資料超過緩衝區邊界時，會覆蓋相鄰的記憶體區域。

### 攻擊原理

攻擊者輸入過長的字串，超過程式預分配的緩衝區空間，覆蓋到函式返回位址。當函式返回時，會跳轉到攻擊者指定的程式碼。

### 防護方法

**位址空間配置隨機化（ASLR）**：隨機化記憶體區段的位址，增加攻擊難度。

**堆疊保護（Stack Canaries）**：在函式返回位址前放入特殊值，檢查是否被破壞。

**不可執行記憶體（NX bit）**：將記憶體頁標記為不可執行，防止注入程式碼執行。

## SQL 注入

攻擊者將惡意 SQL 程式碼插入應用程式的輸入中。

### 攻擊範例

```python
# 不安全的程式碼
query = f"SELECT * FROM users WHERE name = '{username}'"
# 如果 username = "' OR '1'='1"，整個查詢變成永遠為真

# 安全的寫法：使用參數化查詢
cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
```

### 進階攻擊

**UNION 注入**：利用 UNION 取得其他表的資料

**時序盲注入**：根據回應時間推斷資料（如 `IF(1=1, SLEEP(5), 0)`）

### 防護原則

1. 使用參數化查詢（Prepared Statements）
2. 輸入驗證（白名單优于黑名單）
3. 最小權限原則：資料庫帳號不要有過多權限
4. 錯誤訊息不要透露系統資訊

## 跨站腳本（XSS）

攻擊者將惡意腳本注入網頁，當其他使用者訪問時執行。

### XSS 類型

**儲存型 XSS**：惡意內容被永久儲存到目標伺服器（如論壇貼文）

**反映型 XSS**：惡意內容透過 URL 參數傳入，立即反映在回應中

**DOM 型 XSS**：在客戶端 JavaScript 中讀取並執行不安全的使用者輸入

### 防護方法

```python
import html

# Python Flask 範例：自動轉義 Jinja2 模板
from flask import escape
name = escape(user_input)  # 輸出前轉義 HTML 字元
```

```html
<!-- 內容安全策略（CSP）header -->
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com
```

## 跨站請求偽造（CSRF）

攻擊者誘使已驗證的使用者發送惡意請求到目標網站。

### 防護方法

```html
<!-- 在表單中加入 CSRF token -->
<form method="POST">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
</form>
```

```python
# Flask 驗證 CSRF token
from flask_wtf.csrf import validate_csrf
validate_csrf(request.form['csrf_token'])
```

## 會話綁架（Session Hijacking）

攻擊者竊取使用者的 session ID 並假冒該使用者。

### 防護方法

- 使用 HTTPS
- 設定 HttpOnly Cookie（JavaScript 無法讀取）
- 定期更換 session ID
- 設定 session 過期時間
- 驗證 session 持有的其他屬性（如 IP 位址、User-Agent）

## 點擊綁架（Clickjacking）

攻擊者將透明的 iframe 覆蓋在正常網頁上，誘使使用者點擊隱藏的惡意元素。

### 防護方法

```html
<!-- 設定 X-Frame-Options header -->
X-Frame-Options: DENY  <!-- 完全禁止被 frame -->
X-Frame-Options: SAMEORIGIN  <!-- 只允許同源 frame -->
```

```html
<!-- 內容安全策略 -->
Content-Security-Policy: frame-ancestors 'none';
```

## 路徑穿越（Path Traversal）

攻擊者使用 `../` 等方式存取預期外的檔案。

### 防護方法

```python
import os

# 驗證路徑
def safe_read(base_dir, filename):
    filepath = os.path.join(base_dir, filename)
    # 確保解析後的路徑在 base_dir 內
    if not os.path.abspath(filepath).startswith(os.path.abspath(base_dir)):
        raise ValueError("Invalid path")
    return open(filepath).read()
```

## 參考資源

- https://www.google.com/search?q=SQL+注入+XSS+CSRF+漏洞+防護+方法+OWASP+2016
- https://www.google.com/search?q=緩衝區溢位+攻擊+原理+ASLR+堆疊保護+防護
- https://www.google.com/search?q=常見+Web+漏洞+防護+安全+開發+最佳實踐