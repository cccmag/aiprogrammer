# 文章 6：自然語言處理導論

## 前言

自然語言處理（Natural Language Processing, NLP）是人工智慧與語言學的交叉領域。本章節介紹 NLP 的基本概念與發展。

## 什麼是 NLP

NLP 旨在讓電腦理解、解釋、和生成人類語言。

## NLP 的層次

| 層次 | 說明 | 範例 |
|------|------|------|
| 語音學 | 聲音的科學 | 音素識別 |
| 形態學 | 字的結構 | 詞根、前綴、後綴 |
| 語法學 | 句子的結構 | 句法分析 |
| 語義學 | 詞句的意義 | 詞義消歧 |
| 語用學 | 上下文與意圖 | 對話理解 |

## NLP 任務

### 1. 文字分類

```python
texts = ["This is great", "I hate it", "Amazing"]
labels = [1, 0, 1]  # positive, negative, positive

model.fit(texts, labels)
prediction = model.predict(["I love it"])  # 1
```

### 2. 情感分析

```python
review = "This movie is fantastic!"
sentiment = analyze_sentiment(review)
print(sentiment)  # positive
```

### 3. 機器翻譯

```python
english_text = "Hello, how are you?"
chinese_text = translate(english_text, src='en', tgt='zh')
print(chinese_text)  # 你好，你好嗎？
```

### 4. 命名實體識別

```python
text = "John works at Google in California"
entities = ner(text)
# [('John', 'PERSON'), ('Google', 'ORG'), ('California', 'LOCATION')]
```

### 5. 問答系統

```python
question = "What is the capital of Taiwan?"
answer = qa_system.answer(question)
print(answer)  # Taipei
```

## 傳統方法 vs 深度學習

| 特性 | 傳統方法 | 深度學習 |
|------|----------|----------|
| 特徵 | 手工設計 | 自動學習 |
| 表現 | 基於統計 | 基於向量 |
| 需要資料 | 較少 | 大量 |

## NLP 工具

- **NLTK**：Python 自然語言工具包
- **spaCy**：工業級 NLP 庫
- **Stanford NLP**：多語言 NLP 工具
- **gensim**：主題建模與詞向量

## 詞向量

將詞語映射到向量空間：

```python
from gensim.models import Word2Vec

sentences = [['king', 'queen', 'man', 'woman']]
model = Word2Vec(sentences, size=100, window=5, min_count=1)

king_vector = model.wv['king']
queen_vector = model.wv['queen']
similarity = model.wv.similarity('king', 'queen')
```

## 總結

NLP 是人工智慧的重要應用領域。從規則系統到深度學習，NLP 技術經歷了巨大演變，現在已能完成翻譯、問答、生成等多種任務。

## 延伸閱讀

- https://www.google.com/search?q=NLP+natural+language+processing+introduction
- https://www.google.com/search?q=word+embeddings+word2vec+explained