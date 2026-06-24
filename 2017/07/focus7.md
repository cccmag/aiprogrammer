# NLP 工具生態系

## Python NLP 工具一覽

2017 年的 NLP 生態系已相當豐富，從基礎的 NLTK 到高效的 spaCy，從統計的 scikit-learn 到深度學習的 Keras/TensorFlow。

## 1. NLTK（Natural Language Toolkit）

老牌 NLP 庫，適合教學與研究。

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# 斷詞
text = "Natural language processing is fascinating."
tokens = nltk.word_tokenize(text)
print(tokens)

# 斷句
sents = nltk.sent_tokenize(text)
print(sents)

# 詞性標注
tagged = nltk.pos_tag(tokens)
print(tagged)

# 詞形還原
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize("running", "v"))  # run
```

## 2. spaCy

現代化、高效率的 NLP 庫，支援多語言。

```python
import spacy
nlp = spacy.load("en_core_web_sm")

text = "Apple is looking at buying a startup in San Francisco"
doc = nlp(text)

# 斷詞與詞性
for token in doc:
    print(token.text, token.pos_, token.dep_)

# 命名實體識別
for ent in doc.ents:
    print(ent.text, ent.label_)

# 依存分析
for token in doc:
    print(token.text, token.head.text, token.dep_)
```

## 3. Gensim

專注於詞向量與文件相似性的庫。

```python
from gensim.models import Word2Vec

# 訓練詞向量
sentences = [
    ['machine', 'learning', 'is', 'powerful'],
    ['deep', 'learning', 'uses', 'neural', 'networks'],
]
model = Word2Vec(sentences, vector_size=100, window=5)

# 相似詞
print(model.wv.most_similar('learning'))

# 文件相似性
from gensim import corpora
from gensim.similarities import MatrixSimilarity

documents = ["machine learning is powerful", "deep learning uses neural networks"]
texts = [doc.lower().split() for doc in documents]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
index = MatrixSimilarity(corpus)
```

## 4. scikit-learn

機器學習的標準庫，也適用於文字分類。

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity

# TF-IDF
vectorizer = TfidfVectorizer(max_features=1000)
tfidf = vectorizer.fit_transform(documents)

# 主題模型 LDA
lda = LatentDirichletAllocation(n_components=5)
lda.fit(tfidf)

# 文件相似性
similarity = cosine_similarity(tfidf[0:1], tfidf)
print(similarity)
```

## 5. TensorFlow/Keras

深度學習框架，可用於構建複雜 NLP 模型。

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

model = Sequential([
    Embedding(input_dim=10000, output_dim=128, input_length=200),
    LSTM(64, return_sequences=True),
    Dropout(0.5),
    LSTM(32),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()
```

## 6. TextBlob

簡單易用的情感分析工具。

```python
from textblob import TextBlob

texts = [
    "I love this product",
    "This is terrible",
    "It's okay, nothing special",
]

for text in texts:
    blob = TextBlob(text)
    sentiment = "正向" if blob.sentiment.polarity > 0 else "負向" if blob.sentiment.polarity < 0 else "中性"
    print(f"{text}: {sentiment} ({blob.sentiment.polarity:.2f})")
```

## 工具選擇指南

| 場景 | 推薦工具 |
|------|----------|
| 教學/研究 | NLTK |
| 生產環境 | spaCy |
| 詞向量 | Gensim |
| 機器學習 | scikit-learn |
| 深度學習 | TensorFlow/Keras |
| 快速原型 | TextBlob |

## 安裝建議

```bash
pip install nltk
pip install spacy
python -m spacy download en_core_web_sm
pip install gensim
pip install scikit-learn
pip install textblob
```

## 實際專案中的組合

```python
# 典型 NLP Pipeline
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1. 使用 spaCy 預處理
nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop])

# 2. TF-IDF 特徵
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(train_texts)

# 3. 訓練分類器
clf = LogisticRegression()
clf.fit(X, y_train)
```

## 總結

Python 的 NLP 生態系非常豐富。選擇合適的工具组合可大幅提昇開發效率。NLTK 適合學習，spaCy 適合生產，Gensim 專精詞向量，scikit-learn 與深度學習框架則負責建模。