# 自然語言處理概述

## 什麼是 NLP？

自然語言處理（Natural Language Processing, NLP）是人工智慧與計算語言學的交叉領域，專注於讓電腦夠理解、詮釋與生成人類語言。從簡單的拼字檢查到複雜的機器翻譯，都是 NLP 的應用範圍。

## NLP 的核心任務

### 1. 斷詞（Tokenization）

將文字切成有意義的最小單位。英文以空格分詞，中文則需要更複雜的演算法。

```python
# 英文斷詞
text = "Hello, world!"
tokens = text.split()
print(tokens)  # ['Hello,', 'world!']
```

### 2. 詞性標注（Part-of-Speech Tagging）

每個詞彙標記其語法角色（名詞、動詞、形容詞等）。

```python
import nltk
text = "The cat sat on the mat"
tokens = nltk.word_tokenize(text)
tagged = nltk.pos_tag(tokens)
print(tagged)
# [('The', 'DT'), ('cat', 'NN'), ('sat', 'VBD'), ('on', 'IN'), ('the', 'DT'), ('mat', 'NN')]
```

### 3. 命名實體識別（Named Entity Recognition）

識別文本中的人名、地名、組織名等特定實體。

```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying a startup in San Francisco")
for ent in doc.ents:
    print(ent.text, ent.label_)
# Apple ORG
# San Francisco GPE
```

### 4. 情感分析（Sentiment Analysis）

判斷文字的情感傾向（正向、負向或中立）。

```python
from textblob import TextBlob
text = "I love this product, it's amazing!"
blob = TextBlob(text)
print(blob.sentiment)
# Sentiment(polarity=0.65, subjectivity=0.75)
```

## NLP 的挑戰

### 歧義性（Ambiguity）

同一個詞在不同上下文可能有意義：
- "The bank is closed"（銀行）
- "The river bank is muddy"（河岸）

### 多義性（Polysemy）

一個詞可能有多種解釋，需要語境理解。

### 諷刺與反語（Sarcasm）

「太好了，又堵車了！」表面正向但實際負向。

## 現代 NLP 的發展

2013 年 Word2Vec 的出現是重要轉捩點。詞嵌入將詞彙映射到稠密向量空間，捕捉語意關係。

2017 年的 Transformer 架構更帶來重大突破：
- 完全基於注意力機制
- 可平行化訓練
- 更容易處理長距離依賴

## 總結

NLP 已從規則系統、統計方法發展到深度學習時代。Word2Vec、CNN、RNN、LSTM、Transformer 等技術接連出現，推動著領域快速前進。下期我們將深入探討文字預處理技術。