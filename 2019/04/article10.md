# 情感分析實作：利用預訓練模型判斷評論

## 前言

情感分析是 NLP 的經典應用。本篇文章展示如何使用預訓練模型進行情感分析。

## 任務定義

```
輸入：一句話或一段文字
輸出：Positive / Negative / Neutral
```

## 方法一：使用 BERT

```python
from transformers import BertForSequenceClassification, BertTokenizer
import torch

model_name = 'bert-base-chinese'
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=3)
tokenizer = BertTokenizer.from_pretrained(model_name)

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=128, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()

    labels = {0: 'negative', 1: 'neutral', 2: 'positive'}
    return labels[prediction]
```

## 方法二：使用 fastText

```python
import fasttext

# 訓練模型
model = fasttext.train_supervised('train.txt', epoch=5, lr=0.5, wordNgrams=2)

# 預測
result = model.predict("這產品很好用，强烈推薦")
print(result)  # ('__label__positive', 0.99)
```

## 方法三：使用 TextBlob

```python
from textblob import TextBlob

def sentiment_textblob(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'
```

## 實際應用

```python
class ReviewAnalyzer:
    def __init__(self, method='bert'):
        self.method = method
        if method == 'bert':
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
            self.model = BertForSequenceClassification.from_pretrained(
                'bert-base-chinese', num_labels=3
            )

    def analyze_batch(self, reviews):
        results = []
        for review in reviews:
            sentiment = self.predict_sentiment(review)
            results.append({
                'text': review,
                'sentiment': sentiment
            })
        return results
```

## 結論

利用預訓練模型可以快速建立高質量的情感分析系統。選擇哪種方法取決於需求、資源和精度要求。

---

**延伸閱讀**

- [情感分析教程](https://www.google.com/search?q=sentiment+analysis+tutorial)
- [Transformer 情感分析](https://www.google.com/search?q=transformer+sentiment+analysis)