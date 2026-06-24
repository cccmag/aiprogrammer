# 文字預處理

## 分詞與斷詞

文字預處理是 NLP 的第一步，其中分詞（Tokenization）是基本工作。對於英文等有空格分隔的語言，分詞相對簡單；但對於中文、日文等沒有明顯詞邊界的語言，分詞是一個挑戰。

---

## 分詞方法

### 英文分詞

英文分詞相對直接，基於空格和標點符號即可：

```python
import re

def tokenize_english(text):
    """英文分詞"""
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

text = "Natural Language Processing is fascinating!"
tokens = tokenize_english(text)
# ['natural', 'language', 'processing', 'is', 'fascinating']
```

### 中文分詞

中文分詞更為複雜，因為沒有天然的分詞標記：

```
原始句子：我今天去了北京大學
可能的分詞方式：
- 我 / 今天 / 去 / 了 / 北京大學
- 我 / 今天 / 去了 / 北京 / 大學
- 我 / 今天 / 去 / 了 / 北京 / 大學
```

### 分詞策略

**1. 基於詞典的最長匹配**

```python
def longest_match(text, dictionary):
    """正向最大匹配 (FMM)"""
    result = []
    i = 0
    while i < len(text):
        matched = None
        for j in range(len(text), i, -1):
            word = text[i:j]
            if word in dictionary:
                matched = word
                break
        if matched:
            result.append(matched)
            i += len(matched)
        else:
            result.append(text[i])
            i += 1
    return result
```

**2. 機率分詞**

```python
def tokenize_prob(text, model):
    """基於語言模型的分詞"""
    # 使用維特比演算法找最優分詞路徑
    pass
```

**3. 使用現成工具**

```python
# Jieba（結巴分詞）
import jieba
text = "我今天去了北京大學"
tokens = list(jieba.cut(text))
# ['我', '今天', '去', '了', '北京大學']
```

---

## 停用詞移除

停用詞（Stopwords）是在文件中頻繁出現但對語意分析貢獻不大的詞，如「的」、「了」、「在」等。

### 停用詞範例

```python
STOP_WORDS = {
    'english': {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'of', 'and', 'in'},
    'chinese': {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一個'}
}

def remove_stopwords(tokens, language='chinese'):
    """移除停用詞"""
    stops = STOP_WORDS.get(language, set())
    return [t for t in tokens if t not in stops]
```

### 停用詞的問題

停用詞清單並非通用：
- 「北京的」在某些情境可能有重要意義
- 情感分析中，「不」、「沒」等否定詞很重要
- 醫學文本中，常見詞可能攜帶重要資訊

---

## 正規化技術

### 小寫化

```python
def lowercase(text):
    return text.lower()
```

### 詞形歸一化

**Stemming（詞幹提取）**

```python
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
print(stemmer.stem("running"))   # run
print(stemmer.stem("connection")) # connect
print(stemmer.stem("studies"))    # studi
```

**Lemmatization（詞形還原）**

```python
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize("running", "v"))  # run
print(lemmatizer.lemmatize("better", "a"))   # good
```

### 數字處理

```python
import re

def replace_numbers(text):
    """將數字替換為統一標記"""
    return re.sub(r'\d+', '<NUM>', text)

def remove_numbers(text):
    """移除所有數字"""
    return re.sub(r'\d+', '', text)
```

### 標點符號處理

```python
def remove_punctuation(text):
    return ''.join(c for c in text if c not in string.punctuation)
```

---

## 詞性標註與命名實體識別

### 詞性標註（POS Tagging）

```python
from nltk import pos_tag

tokens = ["The", "cat", "is", "sleeping"]
tags = pos_tag(tokens)
# [('The', 'DT'), ('cat', 'NN'), ('is', 'VBZ'), ('sleeping', 'VBG')]

# 常見 POS 標記
# DT: 限定詞  NN: 名詞  VBZ: 動詞第三人稱單數  VBG: 動詞進行式
```

### 中文詞性標註

```python
# 使用 jieba
import jieba.posseg as pseg

words = pseg.cut("習近平在北京召開會議")
for word, flag in words:
    print(f"{word}: {flag}")
# 習近平: nr (人名)
# 在: p (介詞)
# 北京: ns (地名)
# 召開: v (動詞)
# 會議: n (名詞)
```

### 命名實體識別（NER）

```python
import nltk

def ner_example():
    """簡單的命名實體識別"""
    text = "Microsoft CEO Satya Nadella visited Tokyo in 2019."
    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    chunks = nltk.ne_chunk(tags)
    for chunk in chunks:
        if hasattr(chunk, 'label'):
            print(f"{chunk.label()}: {[c[0] for c in chunk]}")
    # GPE: ['Tokyo']
    # ORG: ['Microsoft']
    # PERSON: ['Satya', 'Nadella']
```

---

## 完整的預處理流程

```python
import re
import string
from collections import Counter

class TextPreprocessor:
    def __init__(self, lowercase=True, remove_punct=True,
                 remove_stopwords=False, stem=False):
        self.lowercase = lowercase
        self.remove_punct = remove_punct
        self.remove_stopwords = remove_stopwords
        self.stem = stem
        self.stopwords = set()

    def tokenize(self, text):
        """分詞"""
        if self.lowercase:
            text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def remove_chars(self, tokens):
        """移除字元"""
        result = []
        for token in tokens:
            if self.remove_punct and token in string.punctuation:
                continue
            result.append(token)
        return result

    def remove_stop(self, tokens):
        """移除停用詞"""
        if not self.stopwords:
            return tokens
        return [t for t in tokens if t not in self.stopwords]

    def preprocess(self, text):
        """完整預處理流程"""
        tokens = self.tokenize(text)
        tokens = self.remove_chars(tokens)
        if self.remove_stopwords:
            tokens = self.remove_stop(tokens)
        return tokens

def demo():
    texts = [
        "自然語言處理是人工智慧的重要領域！",
        "Word2Vec 可以學習詞語之間的語意關係。",
        "深度學習促進了 NLP 的快速發展。"
    ]

    preprocessor = TextPreprocessor(lowercase=True, remove_punct=True)
    for text in texts:
        tokens = preprocessor.preprocess(text)
        print(f"原文：{text}")
        print(f"處理：{tokens}")
        print()

if __name__ == "__main__":
    demo()
```

---

## 預處理的常見陷阱

1. **過度清理**：移除太多資訊可能損失語意
2. **忽視上下文**：某些情況下停用詞很重要
3. **編碼問題**：處理中文時注意編碼統一
4. **不平衡資料**：不同類別的文字可能需要不同預處理

---

## 延伸閱讀

- [NLTK 文字預處理](https://www.google.com/search?q=NLTK+text+preprocessing+tutorial)
- [Jieba 分詞工具](https://www.google.com/search?q=jieba+chinese+segmentation)
- [中文分詞方法比較](https://www.google.com/search?q=chinese+word+segmentation+methods)

---

*本篇文章為「AI 程式人雜誌 2019 年 4 月號」系列文章之一。*