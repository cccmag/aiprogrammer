# Selenium 自動化測試

## 前言

Selenium 是 Web 應用程式自動化測試的標準工具，支援多種瀏覽器與程式語言。

## 安裝設定

```bash
pip install selenium
```

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```

## 基本操作

```python
from selenium import webdriver

def test_basic():
    driver = webdriver.Firefox()
    try:
        driver.get('http://example.com')
        
        # 取得標題
        title = driver.title
        assert 'Example' in title
        
        # 找到元素
        element = driver.find_element(By.ID, 'search')
        
        # 輸入文字
        element.send_keys('test query')
        
        # 點擊按鈕
        button = driver.find_element(By.NAME, 'submit')
        button.click()
        
        # 等待結果
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'results'))
        )
        assert result.is_displayed()
    finally:
        driver.quit()
```

## 元素定位方式

```python
# ID
driver.find_element(By.ID, 'element-id')

# Name
driver.find_element(By.NAME, 'element-name')

# Class Name
driver.find_element(By.CLASS_NAME, 'class-name')

# XPath
driver.find_element(By.XPATH, '//div[@id="container"]//a')

# CSS Selector
driver.find_element(By.CSS_SELECTOR, 'div.container a')

# Link Text
driver.find_element(By.LINK_TEXT, 'Click Here')

# Partial Link Text
driver.find_element(By.PARTIAL_LINK_TEXT, 'Click')
```

## 表單操作

```python
def test_form():
    driver = webdriver.Firefox()
    try:
        driver.get('http://example.com/form')
        
        # 文字輸入
        driver.find_element(By.NAME, 'username').send_keys('testuser')
        driver.find_element(By.NAME, 'password').send_keys('password123')
        
        # 下拉選單
        from selenium.webdriver.support.ui import Select
        select = Select(driver.find_element(By.NAME, 'country'))
        select.select_by_visible_text('Taiwan')
        
        # 核取方塊
        checkbox = driver.find_element(By.NAME, 'agree')
        if not checkbox.is_selected():
            checkbox.click()
        
        # 提交表單
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # 驗證成功訊息
        success = WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'message'), 'Success')
        )
        assert success
    finally:
        driver.quit()
```

## 等待策略

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 顯式等待
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'submit-btn'))
)

# 組合條件
condition = EC.and_(
    EC.element_to_be_clickable((By.ID, 'btn')),
    EC.text_to_be_present_in_element((By.ID, 'btn'), 'Submit')
)
element = WebDriverWait(driver, 10).until(condition)
```

## 頁面滾動與截圖

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def test_advanced():
    driver = webdriver.Firefox()
    try:
        driver.get('http://example.com')
        
        # 滾動頁面
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        
        # 截圖
        driver.save_screenshot('page.png')
        
        # 取得元素截圖
        element = driver.find_element(By.ID, 'chart')
        element.screenshot('element.png')
        
        # 截圖整頁
        from selenium.webdriver.support.ui import WebDriverWait
        driver.execute_script('window.scrollTo(0, 0);')
    finally:
        driver.quit()
```

## 遠端執行

```python
from selenium import webdriver
from selenium.webdriver.remote.desired_capabilities import DesiredCapabilities

def test_remote():
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME
    )
    try:
        driver.get('http://example.com')
    finally:
        driver.quit()
```

## 延伸閱讀

- [Selenium 官方文檔](https://www.google.com/search?q=selenium+webdriver+tutorial+2016)
- [Python Selenium 教學](https://www.google.com/search?q=python+selenium+testing+2016)
- [Selenium 最佳實踐](https://www.google.com/search?q=selenium+best+practices+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*