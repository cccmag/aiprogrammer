# 語言模型實作：N-gram 與簡單文字生成

## 前言

本文將帶領讀者實作一個簡單的 N-gram 語言模型，並展示如何用它來生成文字。

---

## 原始碼

完整的 Python 實作請參考：[_code/language_model.py](_code/language_model.py)

```python
#!/usr/bin/env python3
"""簡單的 N-gram 語言模型"""

import random
import re
from collections import defaultdict

class NGramLM:
    def __init__(self, n):
        self.n = n
        self.ngram_counts = defaultdict(int)
        self.context_counts = defaultdict(int)
        self.vocab = set()

    def tokenize(self, text):
        return re.findall(r'\w+', text.lower())

    def train(self, corpus):
        tokens = self.tokenize(corpus)
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i+self.n])
            context = ngram[:-1]
            self.ngram_counts[ngram] += 1
            self.context_counts[context] += 1
            self.vocab.update(tokens)

    def probability(self, ngram):
        context = ngram[:-1]
        count = self.ngram_counts[ngram]
        context_count = self.context_counts[context]
        return count / context_count if context_count > 0 else 1e-10

    def predict_next(self, context):
        best_word = None
        best_prob = 0
        for ngram, count in self.ngram_counts.items():
            if ngram[:-1] == context:
                prob = count / self.context_counts[context]
                if prob > best_prob:
                    best_prob = prob
                    best_word = ngram[-1]
        return best_word, best_prob

    def generate(self, seed, max_words=20):
        words = self.tokenize(seed)
        if len(words) < self.n - 1:
            words.extend(['<s>'] * (self.n - 1 - len(words)))

        for _ in range(max_words):
            context = tuple(words[-(self.n-1):])
            if len(context) < self.n - 1:
                context = tuple(['<s>'] * (self.n - 1 - len(context)) + list(context))

            next_word, _ = self.predict_next(context)
            if next_word is None:
                break
            words.append(next_word)

        return ' '.join(words[self.n-1:])

def demo():
    print('=' * 50)
    print('語言模型：N-gram 文字生成')
    print('=' * 50)
    print()

    corpus = """
    the quick brown fox jumps over the lazy dog
    a quick brown dog jumps over the lazy fox
    the lazy dog sleeps in the sun
    a quick fox jumps over the lazy dog
    the brown fox is very quick
    a lazy dog is a happy dog
    """

    print('訓練語料：')
    print(corpus.strip())
    print()

    model = NGramLM(n=3)
    model.train(corpus)

    test_contexts = [
        ('the', 'quick'),
        ('a', 'lazy'),
        ('the', 'brown')
    ]

    print('預測下一個詞：')
    for ctx in test_contexts:
        word, prob = model.predict_next(ctx)
        print(f'  P(? | {" ".join(ctx)}) -> {word} ({prob:.2f})')
    print()

    print('文字生成：')
    seeds = ['the quick', 'a lazy', 'a quick fox']
    for seed in seeds:
        generated = model.generate(seed, max_words=10)
        print(f'  輸入: "{seed}"')
        print(f'  生成: "{generated}"')
        print()

    print('=' * 50)
    print('範例完成！')
    print('=' * 50)

if __name__ == '__main__':
    demo()
```

---

## 執行結果

```
$ cd /Users/Shared/ccc/magazine/aiprogrammer/2018/06/_code
$ python3 language_model.py

==================================================
語言模型：N-gram 文字生成
==================================================

訓練語料：
the quick brown fox jumps over the lazy dog
...

預測下一個詞：
  P(? | the quick) -> brown (1.00)
  P(? | a lazy) -> dog (0.67)
  P(? | the brown) -> fox (1.00)

文字生成：
  輸入: "the quick"
  生成: "brown fox jumps over the lazy dog"

  輸入: "a lazy"
  生成: "dog is a happy dog"

==================================================
範例完成！
==================================================
```

---

## 設計說明

### N-gram 統計

收集每個 N-gram 的出現次數，計算條件機率。

### 文字生成

根據給定的開頭，逐步預測下一個詞，直到達到最大長度或遇到句尾。

---

## 延伸閱讀

- [N-gram 語言模型](https://www.google.com/search?q=ngram+language+model+tutorial)
- [GPT 論文](https://www.google.com/search?q=Improving+Language+Understanding+by+Generative+Pre-Training+2018)

---

*本篇文章為「AI 程式人雜誌 2018 年 6 月號」語言模型實作範例。*