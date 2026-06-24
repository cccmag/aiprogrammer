# 語言偵測與編碼處理

## 多語言語料庫的語言識別與編碼轉換

### 語言偵測的重要性

在建構多語言語料庫時，語言偵測是品質控制的關鍵步驟。Bloom 的 ROOTS 語料庫涵蓋 46 種語言，OSCAR 支援 166 種語言。如果沒有準確的語言識別，混雜不同語言的資料會嚴重影響模型效能。

### 語言偵測工具

**fastText 語言識別：**
Facebook 開發的 fastText 語言識別模型是目前最快、最準確的工具之一。它使用了一個預訓練的監督式分類器，支援 176 種語言。

```python
import fasttext

# 載入預訓練模型
model = fasttext.load_model('lid.176.bin')

# 預測語言
text = "Natural language processing is fascinating."
predictions = model.predict(text, k=3)
# (['__label__en'], [0.99])

text = "自然語言處理是一門重要的學科"
predictions = model.predict(text, k=3)
# (['__label__zh'], [0.98])
```

**langdetect：**
另一個流行的 Python 庫，基於 Google 的語言檢測演算法：

```python
from langdetect import detect, detect_langs

text = "Bonjour le monde"
print(detect(text))  # 'fr'

# 取得所有可能的語言及其機率
print(detect_langs(text))
# [fr:0.99, en:0.01]
```

**langid.py：**
輕量級的語言識別庫，支援 97 種語言：

```python
import langid

text = "Hello world"
print(langid.classify(text))  # ('en', -42.3)
```

### 編碼偵測與轉換

編碼問題是處理多語言網路資料時的常見挑戰。不同地區的網站可能使用不同的編碼方式：

- 繁體中文網站：Big5（較老舊）、UTF-8
- 簡體中文網站：GB2312/GBK、UTF-8
- 日文網站：Shift-JIS、EUC-JP、UTF-8

```python
import chardet

def detect_and_convert(text_bytes):
    # 偵測編碼
    result = chardet.detect(text_bytes)
    encoding = result['encoding']
    confidence = result['confidence']

    if confidence < 0.5:
        # 不確定的情況，嘗試常用編碼
        for enc in ['utf-8', 'gbk', 'big5', 'shift-jis']:
            try:
                return text_bytes.decode(enc)
            except:
                continue

    # 轉換為 UTF-8
    try:
        return text_bytes.decode(encoding, errors='replace')
    except:
        return text_bytes.decode('utf-8', errors='replace')
```

### 處理混合語言文本

網路內容經常包含多種語言的混合。例如，中文文章中可能包含英文術語和日文專有名詞。處理混合語言文本有以下策略：

1. **主要語言識別**：以佔比最高的語言為準
2. **句子級分類**：對每個句子分別進行語言識別
3. **信心值過濾**：只保留語言識別信心值高於閾值的樣本

```python
def detect_major_language(text, threshold=0.8):
    from langdetect import detect_langs

    try:
        langs = detect_langs(text)
        top_lang = langs[0]
        if top_lang.prob >= threshold:
            return top_lang.lang
        return 'unknown'
    except:
        return 'unknown'
```

### 實務建議

在大規模語料庫建構中：

1. **優先使用 fastText**：速度快、準確率高、支援語言多
2. **批次處理**：避免逐條 API 呼叫，使用批次處理提升效率
3. **人工驗證**：對自動語言識別的結果定期抽樣驗證
4. **統一編碼**：所有文本最終統一為 UTF-8 編碼
5. **錯誤處理**：對無法識別編碼的資料有完善的錯誤處理機制

---

## 延伸閱讀

- [fastText 語言識別模型](https://www.google.com/search?q=fastText+language+identification+pretrained+model)
- [chardet 編碼偵測庫](https://www.google.com/search?q=chardet+python+encoding+detection)
- [Unicode 與編碼處理入門](https://www.google.com/search?q=Unicode+encoding+UTF8+tutorial)
