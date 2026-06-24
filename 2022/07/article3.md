# 動態網頁爬蟲：Selenium

## 處理 JavaScript 渲染的現代爬蟲技術

### 為什麼需要動態爬蟲

傳統的 HTTP 請求 + HTML 解析模式無法處理現代 Web 應用。越來越多的網站使用 React、Vue、Angular 等框架動態渲染內容，伺服器返回的 HTML 只是一個空殼，真正的內容需要瀏覽器執行 JavaScript 後才能顯示。

### Selenium 基本用法

Selenium 是一個瀏覽器自動化工具，可以啟動真實瀏覽器執行程式碼，模擬人類瀏覽行為。

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://example.com')

wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, 'content'))
)

html = driver.page_source
driver.quit()
```

### 等待策略

動態內容載入需要時間，正確的等待策略是爬蟲穩定性的關鍵。

**顯式等待（推薦）：**
```python
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'load-more'))
)
```

**隱式等待：**
```python
driver.implicitly_wait(10)
```

### 處理無限滾動

模擬滾動以載入更多內容：

```python
def scroll_to_bottom(driver):
    last = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        import time; time.sleep(2)
        new = driver.execute_script("return document.body.scrollHeight")
        if new == last: break
        last = new
```

### Headless 模式

在伺服器環境中使用無頭瀏覽器：

```python
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
```

### 替代方案

Selenium 速度慢、資源消耗高。替代方案包括 Playwright（微軟，速度更快、多瀏覽器支援）、Puppeteer（Google，僅 Chrome）、requests-html（輕量級，內建 JS 渲染）。

### 實務建議

大規模爬取時使用瀏覽器實例池、定期清理快取、加入適當延遲避免觸發反爬蟲機制、監控記憶體使用防止洩漏。

---

## 延伸閱讀

- [Selenium 官方文檔](https://www.google.com/search?q=Selenium+Python+documentation)
- [Playwright Python 使用指南](https://www.google.com/search?q=Playwright+Python+tutorial)
- [無頭瀏覽器比較](https://www.google.com/search?q=headless+browser+comparison+scraping)
