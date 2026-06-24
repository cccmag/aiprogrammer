# 資料品質與過濾策略

## 垃圾偵測、去重、語言識別

### 品質問題的來源

大規模網路語料庫面臨嚴重的品質問題。Common Crawl 的原始資料中，研究估計約有 15-30% 的內容是低品質或無用的。這些垃圾內容的來源包括：

1. **自動生成的頁面**：SEO 垃圾內容、關鍵詞填充頁面
2. **機器翻譯文本**：品質低劣的自動翻譯
3. **重複內容**：相同內容出現在多個網域
4. **非自然語言**：程式碼片段、資料表格
5. **佔位內容**：「Lorem ipsum」類型的範本文字

### 垃圾網頁偵測

垃圾偵測可以從多個維度進行：

**基於內容的過濾：**

```python
def is_low_quality(text):
    # 行長度分布：過短行比例過高
    lines = text.strip().split('\n')
    short_lines = sum(1 for l in lines if len(l) < 30)
    if len(lines) > 0 and short_lines / len(lines) > 0.5:
        return True

    # 內容熵：內容過於重複
    from collections import Counter
    words = text.split()
    if len(words) > 0:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.2:
            return True

    return False
```

**基於元數據的過濾：**

- 頁面標題是否為空或過短
- 內容長度是否小於閾值（通常為 50 字元）
- HTML 標籤與文字的比例是否過高

### 去重策略

大規模語料庫中的重複內容會導致訓練資料的偏差，並浪費計算資源。常用的去重策略包括：

**精確去重：**
使用雜湊值（如 MD5、SHA256）檢測完全相同的文件。速度快、準確率高，但無法檢測近似重複。

**近似去重：**
使用 MinHash 或 SimHash 技術檢測內容相似但非完全相同的文件：

```python
def simhash(text, hashbits=64):
    # 計算文字的 SimHash 值
    v = [0] * hashbits
    for word in set(text.split()):
        h = hash(word)
        for i in range(hashbits):
            if h & (1 << i):
                v[i] += 1
            else:
                v[i] -= 1
    fingerprint = 0
    for i in range(hashbits):
        if v[i] > 0:
            fingerprint |= (1 << i)
    return fingerprint
```

**行級去重：**
對常見語料庫（如 C4）而言，行級去重是一種高效的近似方法：移除在所有文件中出現超過一次的行。這可以有效去除廣告、導航列、版權宣告等重複內容。

### 語言識別

在處理多語言語料庫時，需要準確識別每個文件的語言。常用工具包括：

- **fastText 語言識別模型**：Facebook 開發的輕量級模型，支援 176 種語言
- **langdetect**：Python 庫，基於 Google 的語言檢測演算法
- **langid.py**：另一個 Python 語言識別工具

```python
from langdetect import detect, detect_langs

text = "自然語言處理是一門重要的學科"
lang = detect(text)  # 'zh-cn'
langs = detect_langs(text)  # [zh-cn:0.99, zh-tw:0.01]
```

### Bloom 的過濾管線

BigScience 計畫的 Bloom 模型使用的 ROOTS 語料庫，其過濾管線堪稱典範：

1. **URL 黑名單過濾**：移除已知的垃圾網站
2. **語言識別**：使用 fastText 確定主要語言
3. **品質評分**：基於 perplexity 評估文本品質
4. **個人資訊遮罩**：移除 Email、IP 等敏感資訊
5. **去重**：使用 MinHash 進行近似去重
6. **毒性過濾**：移除仇恨言論和極端內容

---

## 延伸閱讀

- [MinHash 近似去重演算法](https://www.google.com/search?q=MinHash+near+duplicate+detection)
- [fastText 語言識別](https://www.google.com/search?q=fastText+language+identification)
- [BigScience ROOTS 語料庫過濾](https://www.google.com/search?q=BigScience+ROOTS+corpus+filtering)
