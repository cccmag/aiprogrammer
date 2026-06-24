# 資料清洗與正規化

## 從 HTML 到乾淨文字

### 為什麼需要資料清洗

從網路爬取得到的原始資料充滿了雜訊：HTML 標籤、JavaScript 程式碼、CSS 樣式、廣告內容、導航列等。這些非文本元素不僅佔用儲存空間，更會嚴重干擾語言模型的訓練。一項研究顯示，未經清洗的 Common Crawl 資料中，約有 30% 的內容是非自然語言的。

資料清洗的目標是從原始 HTML 中提取出純粹的自然語言文本，同時盡可能保留原始語義。

### HTML 標籤去除

第一層清洗是移除所有 HTML 和 XML 標籤。最直接的方法是使用正則表達式：

```python
import re

def strip_html(html):
    clean = re.sub(r'<[^>]+>', '', html)
    return clean
```

然而，這方法有明顯缺點：它無法處理 `<script>` 和 `<style>` 區塊中的非文本內容。更好的做法是先移除這些特殊區塊：

```python
def strip_html_advanced(html):
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'\s+', ' ', html).strip()
    return html
```

使用專用的 HTML 解析庫（如 BeautifulSoup 的 `.get_text()` 方法）通常能獲得更好的結果，因為它們能正確處理 HTML 實體（如 `&amp;`）和特殊結構。

### 文字正規化

文字正規化是將不同形式的文字統一到標準格式的過程，包括：

**統一編碼：**
```python
text = text.encode('utf-8', errors='ignore').decode('utf-8')
```

**全形轉半形：**
全形字母和數字在中文網頁中經常出現，需要轉換為半形。

```python
def fullwidth_to_halfwidth(text):
    result = []
    for char in text:
        code = ord(char)
        if 0xFF01 <= code <= 0xFF5E:
            result.append(chr(code - 0xFEE0))
        elif code == 0x3000:
            result.append(' ')
        else:
            result.append(char)
    return ''.join(result)
```

**空白字元統一：**
將各種空白字元（tab、不換行空格等）統一為普通空格。

### 敏感資訊遮蔽

在構建公開語料庫時，需要遮罩個人資訊以保護隱私：

- **Email 地址**：替換為 `<EMAIL>` 標記
- **URL**：替換為 `<URL>` 標記
- **IP 地址**：替換為 `<IP>` 標記
- **電話號碼**：替換為 `<PHONE>` 標記

```python
def mask_pii(text):
    text = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', '<EMAIL>', text)
    text = re.sub(r'https?://\S+', '<URL>', text)
    text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>', text)
    return text
```

### 常見清洗管線

一個完整的清洗管線通常包含以下步驟：

1. 移除 HTML/XML 標籤
2. 移除 JavaScript 和 CSS 區塊
3. 解碼 HTML 實體
4. 統一編碼為 UTF-8
5. 全形轉半形
6. 移除控制字元
7. 遮罩敏感資訊
8. 合併多餘空白
9. 移除空行和過短行

---

## 延伸閱讀

- [Python re 正則表達式教程](https://www.google.com/search?q=python+re+regular+expression+tutorial)
- [Unicode 正規化說明](https://www.google.com/search?q=unicode+normalization+NFC+NFD)
- [資料清洗最佳實踐](https://www.google.com/search?q=data+cleaning+best+practices+NLP)
