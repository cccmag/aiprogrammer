# requests 套件完整指南

## requests 的設計哲學

Python 標準函式庫提供了 `urllib` 模組來處理 HTTP 請求，但它的 API 設計較為底層且使用不便。requests 套件以「HTTP for Humans」為理念，提供了更簡潔、更直覺的 API。

## 安裝

```bash
pip install requests
```

## 所有請求方法

```python
import requests

# 五種主要 HTTP 方法
resp = requests.get('https://httpbin.org/get')
resp = requests.post('https://httpbin.org/post', json={'key': 'value'})
resp = requests.put('https://httpbin.org/put', data={'key': 'value'})
resp = requests.patch('https://httpbin.org/patch', json={'key': 'value'})
resp = requests.delete('https://httpbin.org/delete')
resp = requests.head('https://httpbin.org/get')
resp = requests.options('https://httpbin.org/get')
```

## 請求參數進階用法

### 動態 URL 參數

```python
# 方式一：字串格式化
url = f'https://api.github.com/users/{username}'

# 方式二：params 參數
params = {'q': 'requests library', 'sort': 'stars', 'order': 'desc'}
response = requests.get('https://api.github.com/search/repositories',
    params=params)
print(response.url)
```

### 自訂請求頭

```python
headers = {
    'User-Agent': 'MyApp/1.0 (contact@example.com)',
    'Accept': 'application/vnd.github.v3+json',
    'Accept-Language': 'zh-TW',
}
response = requests.get('https://api.github.com/rate_limit',
    headers=headers)
```

## Cookies 處理

```python
# 發送 Cookies
cookies = {'session_id': 'abc123'}
response = requests.get('https://httpbin.org/cookies', cookies=cookies)

# 讀取回應 Cookies
response = requests.get('https://httpbin.org/cookies/set?name=value')
for key, value in response.cookies.items():
    print(f'{key}: {value}')
```

## 代理設定

```python
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080',
}
response = requests.get('https://api.example.com', proxies=proxies)

# 帶認證的代理
proxies = {
    'https': 'http://user:password@proxy.example.com:8080',
}
```

## SSL 憑證驗證

```python
# 關閉 SSL 驗證（不建議用於正式環境）
response = requests.get('https://self-signed.example.com', verify=False)

# 使用自訂 CA 憑證
response = requests.get('https://api.example.com', verify='/path/to/cert.pem')

# 使用用戶端憑證
response = requests.get('https://api.example.com',
    cert=('/path/to/client.cert', '/path/to/client.key'))
```

## 檔案上傳

```python
# 上傳單一檔案
files = {'file': open('report.pdf', 'rb')}
response = requests.post('https://httpbin.org/post', files=files)

# 上傳多個檔案
files = {
    'file1': ('report.pdf', open('report.pdf', 'rb'), 'application/pdf'),
    'file2': ('photo.jpg', open('photo.jpg', 'rb'), 'image/jpeg'),
}
response = requests.post('https://httpbin.org/post', files=files)
```

## 自訂 Transport Adapter

```python
from requests.adapters import HTTPAdapter

class TimeoutAdapter(HTTPAdapter):
    def __init__(self, timeout=None, *args, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        return super().send(request, **kwargs)

session = requests.Session()
adapter = TimeoutAdapter(timeout=30)
session.mount('https://', adapter)
session.mount('http://', adapter)
```

## 效能與連線池

```python
import requests
from requests.adapters import HTTPAdapter

session = requests.Session()

# 調整連線池大小
adapter = HTTPAdapter(
    pool_connections=100,    # 連線池大小
    pool_maxsize=100,       # 最大連線數
    max_retries=3,          # 重試次數
    pool_block=False        # 是否阻塞等待連線
)
session.mount('https://', adapter)
session.mount('http://', adapter)

# 批次請求
urls = [f'https://jsonplaceholder.typicode.com/posts/{i}' for i in range(1, 11)]
for url in urls:
    resp = session.get(url)
    print(resp.json()['title'])
```

## 常見問題排解

```python
import requests
import logging

# 啟用除錯日誌
logging.basicConfig(level=logging.DEBUG)
requests_log = logging.getLogger('urllib3')
requests_log.setLevel(logging.DEBUG)

# 查看實際傳送的請求
response = requests.get('https://httpbin.org/get')
print(response.request.method)     # GET
print(response.request.url)        # 完整 URL
print(response.request.headers)    # 請求頭
print(response.request.body)       # 請求主體
```

---

## 延伸閱讀

- [requests 官方文件](https://www.google.com/search?q=requests+python+documentation)
- [Advanced requests 用法](https://www.google.com/search?q=python+requests+advanced+usage)
- [Python HTTP 客戶端比較](https://www.google.com/search?q=python+http+client+library+comparison)
