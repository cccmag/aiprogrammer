# 網路爬蟲實作

## 基本 HTTP 請求

```python
import requests

# GET 請求
response = requests.get("https://api.example.com/data")
print(response.status_code)
print(response.text)
print(response.json())

# 带参数
params = {"page": 1, "limit": 10}
response = requests.get("https://api.example.com/data", params=params)

# POST 請求
data = {"username": "alice", "password": "secret"}
response = requests.post("https://api.example.com/login", data=data)
```

## BeautifulSoup 解析 HTML

```python
from bs4 import BeautifulSoup
import requests

response = requests.get("https://example.com")
soup = BeautifulSoup(response.text, "html.parser")

# 找到第一個元素
title = soup.find("h1")
print(title.text)

# 找到所有元素
links = soup.find_all("a")
for link in links:
    print(link.get("href"))

# CSS 選擇器
content = soup.select(".article-content")
for item in content:
    print(item.text)
```

## 爬蟲範例：天氣預報

```python
import requests
from bs4 import BeautifulSoup

def get_weather(city):
    url = f"https://www.google.com/search?q={city}+天氣"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 找溫度
    temp = soup.find("div", class_="BNeawe")
    if temp:
        print(f"{city}: {temp.text}")

get_weather("台北")
get_weather("北京")
```

## 處理動態載入

對於 JavaScript 動態生成的內容，需要使用 Selenium 或 Splash。

```python
# Selenium 基本用法
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://example.com")

# 等待元素出現
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "content"))
)

print(element.text)
driver.quit()
```

## 儲存資料

```python
import csv
import json

# 儲存為 CSV
data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
]

with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(data)

# 儲存為 JSON
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## 反爬蟲策略

### 常見限制

1. **User-Agent 檢測**：使用真實瀏覽器的 UA
2. **IP 頻率限制**：加入延遲或使用代理
3. **登入驗證**：處理 Cookie 與 Session
4. **CAPTCHA**：可能需要第三方辨識服務

### 應對方法

```python
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
}

# 加入隨機延遲
def crawl_with_delay(url):
    time.sleep(random.uniform(1, 3))
    return requests.get(url, headers=headers)

# 使用 Session 保持 Cookie
session = requests.Session()
session.headers.update(headers)
```

## robots.txt 檢查

```python
import requests

def check_robots(url, target_path):
    from urllib.parse import urljoin

    robots_url = urljoin(url, "/robots.txt")
    response = requests.get(robots_url)

    if response.status_code == 200:
        print(f"robots.txt 存在：{robots_url}")
        # 實際解析 robots.txt...
    else:
        print(f"無 robots.txt")

check_robots("https://example.com", "/api/data")
```

## 總結

網路爬蟲要注意禮貌與法律問題。requests + BeautifulSoup 可應付大部分靜態頁面。動態內容需要 Selenium。注意遵守網站的 robots.txt 與使用條款。