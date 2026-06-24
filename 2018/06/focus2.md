# N-gram 語言模型：統計語言模型基礎

## 前言

N-gram 是最經典的統計語言模型。它基於馬可夫假設，透過計算詞序列的頻率來估計機率。

## N-gram 原理

### 馬可夫假設

第 n 個詞只與前 N-1 個詞相關：

```
P(w_n | w_1, ..., w_{n-1}) ≈ P(w_n | w_{n-N+1}, ..., w_{n-1})
```

### N-gram 類型

| 類型 | 公式 | 說明 |
|------|------|------|
| Unigram | P(w) | 每個詞獨立 |
| Bigram | P(w_n \| w_{n-1}) | 考慮前一個詞 |
| Trigram | P(w_n \| w_{n-2}, w_{n-1}) | 考慮前兩個詞 |

## 計算機率

```python
from collections import defaultdict
import re

class NGramLM:
    def __init__(self, n):
        self.n = n
        self.ngram_counts = defaultdict(int)
        self.context_counts = defaultdict(int)

    def tokenize(self, text):
        return re.findall(r'\w+', text.lower())

    def train(self, corpus):
        tokens = self.tokenize(corpus)
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i+self.n])
            context = ngram[:-1]
            self.ngram_counts[ngram] += 1
            self.context_counts[context] += 1

    def probability(self, ngram):
        context = ngram[:-1]
        count = self.ngram_counts[ngram]
        context_count = self.context_counts[context]
        return count / context_count if context_count > 0 else 0

    def predict_next(self, context):
        max_prob = 0
        best_word = None
        for ngram, count in self.ngram_counts.items():
            if ngram[:-1] == context:
                prob = count / self.context_counts[context]
                if prob > max_prob:
                    max_prob = prob
                    best_word = ngram[-1]
        return best_word, max_prob
```

## N-gram 的問題

### 1. 資料稀疏

詞組合眾多，大多是罕見組合。

### 2. 無法捕獲長期依賴

只能考慮前 N-1 個詞。

### 3. 無法處理未知詞

OOV（未知詞）問題。

## 平滑技術

為了解決零機率問題，使用平滑技術：

```python
def simple_good_turing(self, ngram):
    N = sum(self.ngram_counts.values())
    count = self.ngram_counts[ngram]
    count_of_counts = defaultdict(int)

    for c in self.ngram_counts.values():
        count_of_counts[c] += 1

    if count + 1 in count_of_counts:
        return (count + 1) * count_of_counts[count + 1] / count_of_counts[1] / N
    return 1 / N
```

## 結語

N-gram 是語言模型的基础，但有其局限性。這推动了類神經網路語言模型的發展。

---

**延伸閱讀**

- [N-gram 語言模型](https://www.google.com/search?q=ngram+language+model+tutorial)
- [語言模型平滑技術](https://www.google.com/search?q=language+model+smoothing)

---

*本篇文章為「AI 程式人雜誌 2018 年 6 月號」GPT 與生成式 AI 系列之一。*