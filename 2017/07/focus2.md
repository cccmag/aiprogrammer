# 文字預處理技術

## 為什麼要預處理？

原始文字資料充滿雜訊：標點、大小寫、HTML 標籤、停用詞等。預處理是 NLP 專案中最重要的步驟之一，直接影響模型成效。

## 基礎預處理流程

### 1. 轉換為小寫

統一大小寫，減少詞彙量。

```python
text = "Hello WORLD"
text_lower = text.lower()
print(text_lower)  # "hello world"
```

### 2. 移除標點與特殊字元

```python
import re
text = "Hello, world! How are you? #NLP"
text_clean = re.sub(r'[^\w\s]', '', text)
print(text_clean)  # "Hello world How are you NLP"
```

### 3. 移除數字

```python
text = "I have 3 apples and 5 oranges"
text_no_digits = re.sub(r'\d+', '', text)
print(text_no_digits)  # "I have  apples and  oranges"
```

## 中文預處理特別之處

中文沒有空格分隔，因此需要斷詞（Tokenization）。

### jieba 斷詞

```python
import jieba
text = "自然語言處理是人工智慧的重要領域"
words = jieba.cut(text)
print("/".join(words))
# 自然語言/處理/是/人工智慧/的/重要/領域
```

### 繁體中文斷詞注意事項

```python
import jieba
jieba.set_dictionary('dict.txt.big')  # 繁體字典
text = "機器學習與深度學習"
words = jieba.cut(text)
print("/".join(words))
```

## 停用詞（Stop Words）

移除常見但無資訊價值的詞彙。

### 英文停用詞

```python
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
text = "This is a sample sentence showing stop word filtering"
tokens = text.split()
filtered = [w for w in tokens if w not in stop_words]
print(filtered)
# ['This', 'sample', 'sentence', 'showing', 'stop', 'word', 'filtering']
```

### 中文停用詞

```python
stop_words = set(['的', '了', '是', '在', '和', '我', '有'])
text = "機器學習是人工智慧的重要技術"
words = jieba.cut(text)
filtered = [w for w in words if w not in stop_words]
print(filtered)
```

## 詞形還原（Lemmatization）與詞幹提取（Stemming）

### Stemming（詞幹提取）

將詞彙簡化到詞根形式：

```python
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
print(stemmer.stem("running"))   # run
print(stemmer.stem("development"))  # develop
```

### Lemmatization（詞形還原）

考慮詞性的詞形還原，更準確但較慢：

```python
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize("running", "v"))  # run
print(lemmatizer.lemmatize("better", "a"))  # good
```

## N-gram 特征

相鄰 N 個詞的組合，可捕捉局部語境：

```python
from nltk import ngrams
text = "the quick brown fox jumps"
tokens = text.split()
bigrams = list(ngrams(tokens, 2))
trigrams = list(ngrams(tokens, 3))
print(bigrams)
# [('the', 'quick'), ('quick', 'brown'), ('brown', 'fox'), ('fox', 'jumps')]
```

## 完整預處理流程

```python
import re
import jieba

def preprocess_text(text, language='en'):
    # 1. 小寫化
    text = text.lower()

    # 2. 移除特殊字元
    text = re.sub(r'[^\w\s]', '', text)

    # 3. 移除數字
    text = re.sub(r'\d+', '', text)

    # 4. 斷詞
    if language == 'zh':
        words = jieba.cut(text)
    else:
        words = text.split()

    return words

text_en = "Hello, World! I have 3 apples."
text_zh = "我愛機器學習"

print(preprocess_text(text_en, 'en'))
print(preprocess_text(text_zh, 'zh'))
```

## 總結

文字預處理是 NLP 的基石。常見步驟包括：清理、分詞、移除停用詞、詞形還原。中文處理更需注意斷詞。下期我們將探討詞嵌入與 Word2Vec 的原理。