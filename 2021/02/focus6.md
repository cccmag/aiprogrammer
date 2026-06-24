# TorchText 與資料處理

## TorchText 簡介

TorchText 是 PyTorch 的文字處理工具庫，提供：

- 數據集下載與處理
- 常見 NLP 任務的資料管線
- 預處理工具

## 基本使用

```python
from torchtext.data import Field, TabularDataset

TEXT = Field(tokenize='spacy', lower=True)
LABEL = Field(sequential=False)

train, test = TabularDataset.splits(
    path='data/',
    train='train.csv',
    test='test.csv',
    format='csv',
    fields=[('text', TEXT), ('label', LABEL)]
)
```

## 預處理範例

```python
from torchtext.data.utils import ngrams_iterator

def preprocess_text(text, ngrams=2):
    tokens = text.split()
    return list(ngrams_iterator(tokens, ngrams))
```

## 內建數據集

```python
from torchtext.datasets import SST

# Stanford Sentiment Treebank
train_iter, val_iter, test_iter = SST()
```

## Vocabulary 構建

```python
TEXT.build_vocab(train, max_size=25000, vectors='glove.6B.300d')
```

## DataLoader

```python
from torchtext.data import BucketIterator

train_loader = BucketIterator(
    train,
    batch_size=32,
    sort_key=lambda x: len(x.text)
)
```

---

## 延伸閱讀

- [TorchText 官方文檔](https://www.google.com/search?q=TorchText+documentation)
- [NLP+資料處理教學](https://www.google.com/search?q=torchtext+nlp+tutorial)
- [文字預處理最佳實踐](https://www.google.com/search?q=text+preprocessing+NLP+best+practices)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*