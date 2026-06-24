# Corpus Tools 完整實作

## 前言

Corpus Tools 是一個展示語料庫處理核心流程的 Python 工具集，模擬從網頁爬取到語料庫建置的完整管線。

---

## 原始碼

完整的 Python 實作請參考：[_code/corpus_tools.py](_code/corpus_tools.py)

```python
import re
from collections import Counter

def mock_scrape(url):
    return """<html><body><h1>Hello</h1><p>Test</p><script>x</script><style>.c{}</style></body></html>"""

def strip_html(html):
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    return re.sub(r'<[^>]+>', ' ', html)

def clean_text(text):
    text = re.sub(r'https?://\S+', '<URL>', text)
    text = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', '<EMAIL>', text)
    return re.sub(r'\s+', ' ', text).strip().lower()

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def dedup(items):
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]

def demo():
    html = mock_scrape("https://example.com")
    text = strip_html(html)
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    print(f"Tokens: {tokens}")
    print(f"Freq: {Counter(tokens).most_common(5)}")
    print(f"Unique: {dedup(tokens)}")

if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
Tokens: ['hello', 'test']
Freq: [('hello', 1), ('test', 1)]
Unique: ['hello', 'test']
```

---

## 各函式說明

### mock_scrape(url)
模擬網頁爬取。實際應用中會被 `requests.get(url).text` 取代。

### strip_html(html)
依序移除 `<script>`、`<style>` 及所有 HTML 標籤。

### clean_text(text)
將 URL 和 Email 替換為標記，合併空白，轉為小寫。

### tokenize(text)
使用正則 `\b\w+\b` 進行分詞。

### dedup(items)
使用集合保持順序的去重工具。

---

## 延伸閱讀

- [Python requests 官方文檔](https://www.google.com/search?q=python+requests+library+tutorial)
- [BeautifulSoup 解析 HTML](https://www.google.com/search?q=BeautifulSoup+HTML+parsing+tutorial)
- [Common Crawl 開放語料庫](https://www.google.com/search?q=Common+Crawl+open+web+corpus)

---

*本篇文章為「AI 程式人雜誌 2022 年 7 月號」主題系列補充文章。*
