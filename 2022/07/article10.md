# 從原始網頁到訓練語料

## 建構端到端的語料處理管線

### 管線設計原則

從原始網頁到可用的訓練語料，需要經過一系列精心設計的處理步驟。管線設計應遵循模組化、可重複、可監控、容錯四大原則。

### 完整的處理管線

```python
class CorpusPipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, name, func):
        self.steps.append((name, func))

    def run(self, documents):
        results = []
        for doc in documents:
            current = doc
            for _, func in self.steps:
                current = func(current)
            results.append(current)
        return results
```

### 步驟一：網頁爬取

```python
def fetch_page(url):
    import requests
    from urllib.robotparser import RobotFileParser
    rp = RobotFileParser()
    rp.set_url(url + '/robots.txt')
    rp.read()
    if not rp.can_fetch('CorpusBot/1.0', url):
        return None
    response = requests.get(url, timeout=10)
    return response.text
```

### 步驟二：HTML 清洗

先移除 `<script>` 和 `<style>` 區塊，再移除所有 HTML 標籤，最後解碼 HTML 實體。

```python
def clean_html(html):
    import re, html as html_mod
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', html)
    return html_mod.unescape(text).strip()
```

### 步驟三：文字正規化

統一 Unicode 編碼（NFKC）、遮罩 Email 和 URL、合併多餘空白。

### 步驟四：語言識別與品質過濾

使用 langdetect 識別語言，並根據文字長度、重複率、字母比例進行品質評估。只保留高品質的目標語言文本。

### 步驟五：去重

使用 SHA256 雜湊進行精確去重，再用 MinHash 進行近似去重，最後進行行級去重移除模板內容。

### 步驟六：格式轉換

將處理後的語料轉換為 JSONL 格式，每行包含文字內容和元數據。

```python
import json

def save_as_jsonl(documents, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps({'text': doc, 'source': 'common_crawl',
                                'timestamp': '2022-07'},
                               ensure_ascii=False) + '\n')
```

### 品質監控指標

管線執行中應持續監控爬取成功率、平均文字長度、語言分布、去重率、最終產出量。

---

## 延伸閱讀

- [端到端 NLP 管線設計](https://www.google.com/search?q=end+to+end+NLP+pipeline+design)
- [大規模語料處理最佳實踐](https://www.google.com/search?q=大规模语料处理最佳实践)
- [資料管線監控與品質管理](https://www.google.com/search?q=data+pipeline+monitoring+quality+management)
