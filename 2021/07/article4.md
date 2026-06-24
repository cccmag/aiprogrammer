# 自然語言處理的資料預處理

資料預處理是 NLP 專案成功的關鍵。本文介紹常見的預處理技術。

## 1. 文字清洗

```python
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  # 移除 URL
    text = re.sub(r'@\w+', '', text)       # 移除 @mentions
    text = re.sub(r'#\w+', '', text)       # 移除 hashtags
    text = re.sub(r'[^\w\s]', '', text)    # 移除標點
    text = re.sub(r'\s+', ' ', text)        # 規範空白
    return text.strip()
```

## 2. 分詞

```python
def tokenize(text, method='whitespace'):
    if method == 'whitespace':
        return text.split()
    elif method == 'punctuation':
        return re.findall(r'\w+', text.lower())
    return text.split()
```

## 3. 去除停用詞

```python
stop_words = set(['the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being'])

def remove_stopwords(tokens):
    return [t for t in tokens if t not in stop_words]
```

## 4. 詞幹化和詞形還原

```python
from nltk.stem import PorterStemmer, WordNetLemmatizer

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

print(stemmer.stem("running"))   # run
print(lemmatizer.lemmatize("running", pos='v'))  # run
```

## 5. 結論

良好的預處理能顯著提升模型效能，是 NLP 專案的重要基礎。

---

## 延伸閱讀

- [NLTK 文档](https://www.google.com/search?q=NLTK+documentation+python)
- [spaCy 官網](https://www.google.com/search?q=spaCy+NLP+library)