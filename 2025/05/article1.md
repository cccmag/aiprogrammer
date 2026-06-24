# HTTP 方法與狀態碼

## HTTP 方法概述

HTTP 定義了一組請求方法（也稱為 HTTP 動詞），指示對資源要執行的操作。正確使用 HTTP 方法是設計 RESTful API 的基礎。

### 五大常用方法

**GET**：取得資源

GET 是最常見的 HTTP 方法，用於從伺服器取得資源。GET 請求不應有副作用（僅讀取資料），且回應可以被快取。

```python
import requests
response = requests.get('https://api.github.com/users/octocat')
data = response.json()
print(data['login'], data['public_repos'])
```

**POST**：建立資源

POST 用於建立新資源。每次 POST 請求通常會建立一個新的資源實例，因此不是冪等的——多次送出會建立多個資源。

```python
new_post = {'title': 'Hello', 'body': 'This is a new post'}
response = requests.post('https://jsonplaceholder.typicode.com/posts',
    json=new_post)
print(response.status_code)  # 201
```

**PUT**：更新資源

PUT 用於完整更新指定資源。PUT 是冪等的——多次發送相同的 PUT 請求結果相同。

```python
update = {'title': 'Updated', 'body': 'New content'}
response = requests.put('https://jsonplaceholder.typicode.com/posts/1',
    json=update)
```

**PATCH**：部分更新

PATCH 用於部分更新資源，只傳送需要修改的欄位。

```python
patch_data = {'title': 'Only title changed'}
response = requests.patch('https://jsonplaceholder.typicode.com/posts/1',
    json=patch_data)
```

**DELETE**：刪除資源

DELETE 用於刪除指定資源。成功後通常回傳 200 OK 或 204 No Content。

```python
response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
print(response.status_code)  # 200
```

## HTTP 狀態碼

狀態碼分為五大類，每類代表一種回應類型：

### 2xx 成功

| 狀態碼 | 名稱 | 說明 |
|--------|------|------|
| 200 | OK | 請求成功 |
| 201 | Created | 資源建立成功（POST） |
| 204 | No Content | 成功但無回應內容（DELETE） |

### 3xx 重新導向

| 狀態碼 | 名稱 | 說明 |
|--------|------|------|
| 301 | Moved Permanently | 資源已永久移動 |
| 302 | Found | 暫時重新導向 |
| 304 | Not Modified | 資源未更改（快取） |

### 4xx 客戶端錯誤

| 狀態碼 | 名稱 | 說明 |
|--------|------|------|
| 400 | Bad Request | 請求格式錯誤 |
| 401 | Unauthorized | 需要認證 |
| 403 | Forbidden | 無權限存取 |
| 404 | Not Found | 資源不存在 |
| 405 | Method Not Allowed | 不支援的 HTTP 方法 |
| 409 | Conflict | 資源衝突（如重複建立） |
| 422 | Unprocessable Entity | 驗證失敗 |
| 429 | Too Many Requests | 請求過於頻繁 |

### 5xx 伺服器錯誤

| 狀態碼 | 名稱 | 說明 |
|--------|------|------|
| 500 | Internal Server Error | 伺服器內部錯誤 |
| 502 | Bad Gateway | 上游伺服器錯誤 |
| 503 | Service Unavailable | 服務暫時不可用 |
| 504 | Gateway Timeout | 上游伺服器逾時 |

## 實戰：處理狀態碼

```python
import requests

def fetch_user(user_id):
    url = f'https://jsonplaceholder.typicode.com/users/{user_id}'
    response = requests.get(url)

    if response.status_code == 200:
        user = response.json()
        return {'success': True, 'data': user}
    elif response.status_code == 404:
        return {'success': False, 'error': '使用者不存在'}
    elif response.status_code == 500:
        return {'success': False, 'error': '伺服器錯誤'}
    else:
        return {'success': False, 'error': f'未知錯誤：{response.status_code}'}

print(fetch_user(1))
print(fetch_user(999))
```

## 冪等性與安全性

HTTP 方法可以按照冪等性和安全性分類：

```python
# 安全方法：不改變資源狀態
GET, HEAD, OPTIONS

# 冪等方法：多次執行效果相同
GET, PUT, DELETE, HEAD, OPTIONS

# 非冪等方法：多次執行效果不同
POST, PATCH
```

安全方法不應有副作用，冪等方法確保重試安全。

---

## 延伸閱讀

- [HTTP 方法 MDN 文件](https://www.google.com/search?q=HTTP+request+methods+MDN)
- [HTTP 狀態碼完整列表](https://www.google.com/search?q=HTTP+status+codes+list)
- [RESTful API 設計](https://www.google.com/search?q=RESTful+API+design+best+practices)
