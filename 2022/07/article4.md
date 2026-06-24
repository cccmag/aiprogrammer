# 正則表達式清洗實戰

## 使用正則表達式進行文字清洗的技巧

### 正則表達式的作用

正則表達式是文字清洗中最強大的工具之一。雖然深度學習模型可以處理一定程度的文字雜訊，但正則表達式在精確匹配和替換方面仍然無可取代。

### HTML 標籤去除

```python
import re

def remove_html_advanced(text):
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()
```

### 特殊字元處理

```python
def normalize_chars(text):
    # 全形字母轉半形
    text = re.sub(r'[\uff21-\uff3a]', lambda c: chr(ord(c.group())-0xfee0), text)
    # 全形數字轉半形
    text = re.sub(r'[\uff10-\uff19]', lambda c: chr(ord(c.group())-0xfee0), text)
    # 統一引號
    text = re.sub(r'[\u2018\u2019]', "'", text)
    text = re.sub(r'[\u201c\u201d]', '"', text)
    # 統一破折號
    text = re.sub(r'[—–]', '-', text)
    return text
```

### URL 和 Email 遮罩

```python
def mask_sensitive_info(text):
    text = re.sub(r'https?://[^\s<>"]+', '<URL>', text)
    text = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', '<EMAIL>', text)
    text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>', text)
    return text
```

### 空白與換行處理

```python
def clean_whitespace(text):
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return re.sub(r'[ \t]+', ' ', text).strip()
```

### 中文特化清洗

```python
def clean_chinese_text(text):
    # 保留中文、英文、數字和基本標點
    text = re.sub(r'[^\u4e00-\u9fff\w\s，。！？、；：""''（）【】]', '', text)
    # 中英文之間加空格
    text = re.sub(r'([\u4e00-\u9fff])([a-zA-Z])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])([\u4e00-\u9fff])', r'\1 \2', text)
    return text
```

### 實戰技巧

逐步清洗、測試先行、注意邊界情況、使用 `re.compile` 預編譯提升大規模處理效能。

---

## 延伸閱讀

- [Python re 模組文檔](https://www.google.com/search?q=python+re+module+regular+expression)
- [正則表達式 30 分鐘入門](https://www.google.com/search?q=regular+expression+tutorial+30+minutes)
- [中文文本正規化最佳實踐](https://www.google.com/search?q=chinese+text+normalization+best+practices)
