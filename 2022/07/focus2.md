# 網頁爬蟲技術：requests + BeautifulSoup

## 從 HTTP 到結構化資料

### 請求與回應的基本流程

網頁爬蟲的核心是模擬瀏覽器向伺服器發送 HTTP 請求，並解析伺服器返回的 HTML 內容。Python 中最常用的工具組合是 `requests` 和 `BeautifulSoup`。

`requests` 負責處理 HTTP 協定的細節，包括 GET/POST 請求、Cookie 管理、Session 維持等。一個基本的 GET 請求只需要一行程式碼：

```python
import requests
response = requests.get('https://example.com')
html = response.text
```

`BeautifulSoup` 負責將 HTML 字串解析為可操作的樹狀結構，支援透過標籤名稱、CSS 類別、ID、屬性等各種方式定位元素。

### requests 進階用法

在實際爬蟲中，需要處理更複雜的情境：

**自訂請求頭：**
許多網站會阻擋沒有 User-Agent 的請求。透過自訂請求頭可以偽裝成真實瀏覽器。

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
}
response = requests.get(url, headers=headers)
```

**Session 與 Cookie：**
需要登入或維持狀態的網站，可以使用 Session 物件自動管理 Cookie。

```python
session = requests.Session()
session.post('https://example.com/login', data={'user': 'abc', 'pass': '123'})
response = session.get('https://example.com/dashboard')
```

**錯誤處理與重試：**
網路請求可能因各種原因失敗，良好的錯誤處理機制是爬蟲的必備功能。

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

### BeautifulSoup 解析技巧

BeautifulSoup 支援多種解析器，其中最常用的是 `lxml`（速度快）和內建的 `html.parser`（不需額外安裝）。

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'lxml')

# 透過標籤名稱查找
title = soup.find('title').text

# 透過 CSS 類別查找
articles = soup.find_all('div', class_='article')

# 透過屬性查找
links = soup.find_all('a', href=True)

# CSS 選擇器
main_content = soup.select_one('div.main-content')
```

### 爬蟲策略與最佳實踐

**尊重 Robots.txt：**
在發起爬取前，應先檢查目標網站的 `robots.txt` 文件，了解哪些路徑允許爬取。

**請求間隔與限速：**
過快的請求頻率可能導致 IP 被封鎖。加入隨機延遲可以降低被偵測的風險。

```python
import time
import random

time.sleep(random.uniform(1, 3))
```

**增量爬取：**
對於需要定期更新的語料庫，增量爬取可以大幅節省頻寬和時間。透過記錄已爬取的 URL 和最後修改時間，只爬取新增或變更的頁面。

### 常見問題與解決方案

1. **中文亂碼**：使用 `response.encoding` 或 `chardet` 自動偵測編碼
2. **動態內容**：網頁內容由 JavaScript 渲染時，需要使用 Selenium 或 Playwright
3. **驗證碼**：可考慮使用 OCR 服務或手動繞過
4. **IP 封鎖**：使用代理池輪換 IP 地址

---

## 延伸閱讀

- [Python requests 庫官方文檔](https://www.google.com/search?q=python+requests+library+documentation)
- [BeautifulSoup 4 官方文檔](https://www.google.com/search?q=beautifulsoup+4+documentation)
- [Robots.txt 協定說明](https://www.google.com/search?q=robots+txt+protocol+explained)
