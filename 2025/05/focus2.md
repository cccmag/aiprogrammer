# 使用 requests 呼叫 API

## requests 套件簡介

requests 是 Python 生態系中最受歡迎的 HTTP 客戶端套件。由 Kenneth Reitz 於 2011 年建立，以其簡潔優雅的 API 設計聞名。在 Python 的 HTTP 世界中，requests 以其「讓 HTTP 服務人類」的理念，大幅簡化了網路程式設計的複雜度。

## 安裝與基本用法

```bash
pip install requests
```

### 傳送 GET 請求

```python
import requests

response = requests.get('https://api.github.com/users/octocat')
print(response.status_code)  # 200
print(response.json())       # JSON 回應內容
```

### 請求參數

```python
params = {'q': 'python', 'page': 1, 'per_page': 10}
response = requests.get('https://api.github.com/search/repositories', params=params)
print(response.url)
# https://api.github.com/search/repositories?q=python&page=1&per_page=10
```

## 請求頭與認證

```python
headers = {
    'User-Agent': 'MyApp/1.0',
    'Accept': 'application/json',
}
response = requests.get('https://api.example.com/data', headers=headers)

# HTTP Basic Auth
from requests.auth import HTTPBasicAuth
response = requests.get('https://api.example.com/secure',
    auth=HTTPBasicAuth('username', 'password'))

# Bearer Token
headers = {'Authorization': 'Bearer <token>'}
response = requests.get('https://api.example.com/protected', headers=headers)
```

## POST、PUT、DELETE 請求

```python
# POST 請求（JSON 格式）
data = {'title': 'Hello', 'content': 'World'}
response = requests.post('https://jsonplaceholder.typicode.com/posts',
    json=data)
print(response.status_code)  # 201
print(response.json())

# PUT 請求
data = {'title': 'Updated', 'content': 'Content'}
response = requests.put('https://jsonplaceholder.typicode.com/posts/1',
    json=data)

# DELETE 請求
response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
print(response.status_code)  # 200 或 204
```

### 使用表單資料

```python
response = requests.post('https://httpbin.org/post',
    data={'key1': 'value1', 'key2': 'value2'})
```

## 回應處理

```python
response = requests.get('https://api.github.com/users/octocat')

# 各種回應格式
print(response.text)        # 原始文字
print(response.content)     # 二進位內容
print(response.json())      # 解析 JSON
print(response.headers)     # 回應頭
print(response.cookies)     # Cookies
print(response.elapsed)     # 請求耗時
```

### 檔案下載（串流模式）

```python
response = requests.get('https://example.com/large-file.zip', stream=True)
with open('output.zip', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

## 逾時與例外處理

```python
try:
    response = requests.get('https://api.example.com/data',
        timeout=5)  # 逾時設定（秒）
    response.raise_for_status()  # 4xx/5xx 時拋出例外
except requests.exceptions.Timeout:
    print('請求逾時')
except requests.exceptions.ConnectionError:
    print('連線失敗')
except requests.exceptions.HTTPError as e:
    print(f'HTTP 錯誤：{e}')
except requests.exceptions.RequestException as e:
    print(f'請求失敗：{e}')
```

## Session 物件

Session 物件可以保持連線、共用 cookie 和預設配置：

```python
with requests.Session() as session:
    session.headers.update({'Authorization': 'Bearer <token>'})
    session.params.update({'api_key': 'your-key'})

    resp1 = session.get('https://api.example.com/user')
    resp2 = session.get('https://api.example.com/orders')
    # 兩個請求共用相同的認證資訊
```

## 重試機制

使用 `requests.adapters.HTTPAdapter` 和 `urllib3` 的 Retry：

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(total=3, backoff_factor=0.5,
    status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount('https://', adapter)
session.mount('http://', adapter)

response = session.get('https://api.example.com/unstable')
```

## 真實範例：串接 GitHub API

```python
import requests

def get_user_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    response.raise_for_status()
    repos = response.json()
    for repo in repos:
        print(f"{repo['name']}: {repo['description'] or '無說明'}")

get_user_repos('octocat')
```

---

## 延伸閱讀

- [requests 官方文件](https://www.google.com/search?q=requests+python+library)
- [Python HTTP 請求指南](https://www.google.com/search?q=python+requests+tutorial)
- [GitHub REST API 文件](https://www.google.com/search?q=GitHub+REST+API)
